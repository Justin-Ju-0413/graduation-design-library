"""
Generate INT8-quantized LeNet-5 weights for MNIST as C header files.
Uses PyTorch to train a LeNet-5, then quantizes to INT8.
Weights exported as C arrays compatible with the NICE CNN accelerator.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import numpy as np
import os

print("Training LeNet-5 on MNIST...")

# LeNet-5 architecture (modified for MNIST: 28x28 input, 1 channel)
class LeNet5(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)   # 28x28 -> 24x24
        self.conv2 = nn.Conv2d(6, 16, 5)  # 12x12 -> 8x8
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)  # 24x24 -> 12x12
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)  # 8x8 -> 4x4
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Train
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# C-side: input = pixel - 128, range [-128, 127]
# Training uses EXACT SAME transform: ToTensor->[0,1], *255->[0,255], -128->[-128,127]
# Result: input_scale = 1.0 (C INT8 == training float), zero scale mismatch
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x * 255.0 - 128.0)
])

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./mnist_data', train=True, download=True, transform=transform),
    batch_size=64, shuffle=True
)
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./mnist_data', train=False, transform=transform),
    batch_size=1000
)

model = LeNet5().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

model.train()
for epoch in range(5):
    total_loss = 0
    correct = 0
    total = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += len(data)

    print(f"Epoch {epoch+1}: loss={total_loss/len(train_loader):.4f}, acc={100*correct/total:.2f}%")

# Evaluate
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += len(data)

accuracy = 100 * correct / total
print(f"\nTest accuracy: {accuracy:.2f}%")

# Quantize weights to INT8 with proper per-layer scale calibration
# C-side: input = pixel - 128 (INT8), training: Normalize(0.5,0.5) -> [-1,1]
# C input is 128x larger than training input -> input_scale = 1/128
print("\nQuantizing weights with scale-chain calibration...")

INPUT_SCALE = 1.0  # C INT8 == training float exactly (both use pixel-128)

def quantize_weight(t):
    """Quantize weight tensor to INT8, return (q_int8, scale)"""
    t_np = t.detach().cpu().numpy()
    max_abs = float(np.max(np.abs(t_np)))
    if max_abs == 0:
        max_abs = 1.0
    q = np.clip(np.round(t_np * 127.0 / max_abs), -128, 127).astype(np.int8)
    scale = max_abs / 127.0  # one INT8 unit = scale in FP32
    return q, scale

def quantize_bias(bias_fp, output_scale):
    """Compute INT32 bias = round(bias_fp / output_scale)"""
    b_np = bias_fp.detach().cpu().numpy()
    return np.round(b_np / output_scale).astype(np.int32)

def choose_shift(output_scale):
    """Choose right-shift so INT32_output >> shift fits in INT8 with scale ~1.0.
    After shift: effective_scale = output_scale * 2^shift, should ≈ 1.0"""
    if output_scale <= 0:
        return 8
    shift = int(round(np.log2(1.0 / output_scale)))
    return max(0, min(shift, 24))

# --- Conv1 ---
# input_scale = 1/128 (C INT8 = 128x FP32 training input)
conv1_w_q, conv1_w_scale = quantize_weight(model.conv1.weight)
conv1_out_scale = INPUT_SCALE * conv1_w_scale
conv1_bias_q = quantize_bias(model.conv1.bias, conv1_out_scale)
# Conv1 INT32 output -> rescale for Conv2 INT8 input
c2_input_shift = choose_shift(conv1_out_scale)  # Pool1 output >> shift -> INT8

# --- Conv2 ---
# Conv2 input is INT8 after right-shift, but accumulated over multiple tiles
# Conv2 input_scale = conv1_out_scale * 2^c2_input_shift
conv2_in_scale = conv1_out_scale * (2 ** c2_input_shift)
conv2_w_q, conv2_w_scale = quantize_weight(model.conv2.weight)
conv2_out_scale = conv2_in_scale * conv2_w_scale
conv2_bias_q = quantize_bias(model.conv2.bias, conv2_out_scale)
# Conv2 INT32 output (sum over 6 input ch) -> rescale for FC1 input
# FC works on INT32, no explicit INT8 conversion needed, but shift to prevent overflow
fc1_input_shift = choose_shift(conv2_out_scale)

# --- FC1 ---
fc1_in_scale = conv2_out_scale * (2 ** fc1_input_shift)
fc1_w_q, fc1_w_scale = quantize_weight(model.fc1.weight)
fc1_out_scale = fc1_in_scale * fc1_w_scale
fc1_bias_q = quantize_bias(model.fc1.bias, fc1_out_scale)
fc1_out_shift = choose_shift(fc1_out_scale)

# --- FC2 ---
fc2_in_scale = fc1_out_scale * (2 ** fc1_out_shift)
fc2_w_q, fc2_w_scale = quantize_weight(model.fc2.weight)
fc2_out_scale = fc2_in_scale * fc2_w_scale
fc2_bias_q = quantize_bias(model.fc2.bias, fc2_out_scale)
fc2_out_shift = choose_shift(fc2_out_scale)

# --- FC3 ---
fc3_in_scale = fc2_out_scale * (2 ** fc2_out_shift)
fc3_w_q, fc3_w_scale = quantize_weight(model.fc3.weight)
fc3_out_scale = fc3_in_scale * fc3_w_scale
fc3_bias_q = quantize_bias(model.fc3.bias, fc3_out_scale)
fc3_out_shift = choose_shift(fc3_out_scale)

print(f"Conv1: weight_scale={conv1_w_scale:.6f}, out_scale={conv1_out_scale:.6e}, c2_shift={c2_input_shift}")
print(f"  bias range=[{conv1_bias_q.min()}, {conv1_bias_q.max()}]")
print(f"Conv2: weight_scale={conv2_w_scale:.6f}, in_scale={conv2_in_scale:.6e}, out_scale={conv2_out_scale:.6e}, fc1_shift={fc1_input_shift}")
print(f"  bias range=[{conv2_bias_q.min()}, {conv2_bias_q.max()}]")
print(f"FC1:   weight_scale={fc1_w_scale:.6f}, out_scale={fc1_out_scale:.6e}, shift={fc1_out_shift}")
print(f"  bias range=[{fc1_bias_q.min()}, {fc1_bias_q.max()}]")
print(f"FC2:   weight_scale={fc2_w_scale:.6f}, out_scale={fc2_out_scale:.6e}, shift={fc2_out_shift}")
print(f"  bias range=[{fc2_bias_q.min()}, {fc2_bias_q.max()}]")
print(f"FC3:   weight_scale={fc3_w_scale:.6f}, out_scale={fc3_out_scale:.6e}, shift={fc3_out_shift}")
print(f"  bias range=[{fc3_bias_q.min()}, {fc3_bias_q.max()}]")
print(f"\nCalibrated shifts: c2_in={c2_input_shift}, fc1_in={fc1_input_shift}, fc1_out={fc1_out_shift}, fc2_out={fc2_out_shift}, fc3_out={fc3_out_shift}")

print(f"\nConv1 weight: shape={conv1_w_q.shape}, range=[{conv1_w_q.min()}, {conv1_w_q.max()}]")
print(f"Conv2 weight: shape={conv2_w_q.shape}, range=[{conv2_w_q.min()}, {conv2_w_q.max()}]")
print(f"FC1 weight: shape={fc1_w_q.shape}, range=[{fc1_w_q.min()}, {fc1_w_q.max()}]")
print(f"FC2 weight: shape={fc2_w_q.shape}, range=[{fc2_w_q.min()}, {fc2_w_q.max()}]")
print(f"FC3 weight: shape={fc3_w_q.shape}, range=[{fc3_w_q.min()}, {fc3_w_q.max()}]")

OUT_DIR = r"C:\Users\16084\Documents\New project\riscv_cnn_accelerator\sw\inc"
os.makedirs(OUT_DIR, exist_ok=True)

# Build shift header
shift_header = f"""// Auto-generated calibration shifts for LeNet-5 INT8 inference
// Generated 2026-05-06
#ifndef LENET5_SHIFTS_H
#define LENET5_SHIFTS_H

// Pool1 output -> Conv2 INT8 input rescaling
#define CONV2_INPUT_RSHIFT {c2_input_shift}

// Conv2 output (INT32) -> FC1 input rescaling (applied in FC1 first stage)
// Note: FC1 internally right-shifts by FC1_OUT_RSHIFT, applied separately
#define FC1_OUT_RSHIFT {fc1_out_shift}
#define FC2_OUT_RSHIFT {fc2_out_shift}
#define FC3_OUT_RSHIFT {fc3_out_shift}

#endif
"""

shift_path = os.path.join(OUT_DIR, "lenet5_shifts.h")
os.makedirs(OUT_DIR, exist_ok=True)
with open(shift_path, 'w') as f:
    f.write(shift_header)
print(f"Shifts saved to: {shift_path}")

# Generate C header

header_path = os.path.join(OUT_DIR, "lenet5_weights.h")

with open(header_path, 'w') as f:
    f.write("// Auto-generated LeNet-5 INT8 quantized weights for MNIST\n")
    f.write(f"// Test accuracy: {accuracy:.2f}%\n")
    f.write("// Generated 2026-05-06\n\n")
    f.write("#ifndef LENET5_WEIGHTS_H\n#define LENET5_WEIGHTS_H\n\n")
    f.write("#include <stdint.h>\n\n")

    def write_array(f, name, arr, shape_str):
        flat = arr.flatten()
        f.write(f"// Shape: {shape_str}, size: {len(flat)}\n")
        f.write(f"static const int8_t {name}[{len(flat)}] = {{\n  ")
        for i, v in enumerate(flat):
            f.write(f"{int(v)}")
            if i < len(flat) - 1:
                f.write(", ")
            if (i + 1) % 16 == 0:
                f.write("\n  ")
        f.write("\n};\n\n")

    def write_array_i32(f, name, arr, shape_str):
        flat = arr.flatten()
        f.write(f"// Shape: {shape_str}, size: {len(flat)}\n")
        f.write(f"static const int32_t {name}[{len(flat)}] = {{\n  ")
        for i, v in enumerate(flat):
            f.write(f"{int(v)}")
            if i < len(flat) - 1:
                f.write(", ")
            if (i + 1) % 8 == 0:
                f.write("\n  ")
        f.write("\n};\n\n")

    # Conv1: [6, 1, 5, 5] = 150 weights + 6 biases
    write_array(f, "lenet5_conv1_weight", conv1_w_q, "6x1x5x5")
    write_array_i32(f, "lenet5_conv1_bias", conv1_bias_q, "6")

    # Conv2: [16, 6, 5, 5] = 2400 weights + 16 biases
    write_array(f, "lenet5_conv2_weight", conv2_w_q, "16x6x5x5")
    write_array_i32(f, "lenet5_conv2_bias", conv2_bias_q, "16")

    # FC1: [120, 256] = 30720 weights + 120 biases
    write_array(f, "lenet5_fc1_weight", fc1_w_q, "120x256")
    write_array_i32(f, "lenet5_fc1_bias", fc1_bias_q, "120")

    # FC2: [84, 120] = 10080 weights + 84 biases
    write_array(f, "lenet5_fc2_weight", fc2_w_q, "84x120")
    write_array_i32(f, "lenet5_fc2_bias", fc2_bias_q, "84")

    # FC3: [10, 84] = 840 weights + 10 biases
    write_array(f, "lenet5_fc3_weight", fc3_w_q, "10x84")
    write_array_i32(f, "lenet5_fc3_bias", fc3_bias_q, "10")

    # Layer dimensions
    f.write("// Layer dimensions\n")
    f.write("#define LENET5_CONV1_IN_CH  1\n")
    f.write("#define LENET5_CONV1_OUT_CH 6\n")
    f.write("#define LENET5_CONV1_KERNEL 5\n")
    f.write("#define LENET5_CONV2_IN_CH  6\n")
    f.write("#define LENET5_CONV2_OUT_CH 16\n")
    f.write("#define LENET5_CONV2_KERNEL 5\n")
    f.write("#define LENET5_FC1_IN   256\n")
    f.write("#define LENET5_FC1_OUT  120\n")
    f.write("#define LENET5_FC2_IN   120\n")
    f.write("#define LENET5_FC2_OUT  84\n")
    f.write("#define LENET5_FC3_IN   84\n")
    f.write("#define LENET5_FC3_OUT  10\n")

    f.write("\n#endif // LENET5_WEIGHTS_H\n")

print(f"\nWeights saved to: {header_path}")
print(f"File size: {os.path.getsize(header_path)} bytes")

# Also export one MNIST test image for verification
print("\nExporting test MNIST images...")
test_data = datasets.MNIST('./mnist_data', train=False, transform=transforms.ToTensor())
img_path = os.path.join(OUT_DIR, "mnist_test_images.h")
with open(img_path, 'w') as f:
    f.write("// MNIST test images (first 10, INT8 quantized)\n")
    f.write("#ifndef MNIST_TEST_IMAGES_H\n#define MNIST_TEST_IMAGES_H\n\n")
    f.write("#include <stdint.h>\n\n")

    for idx in range(10):
        img = (test_data[idx][0].numpy() * 255).astype(np.uint8).flatten()
        label = test_data[idx][1]
        f.write(f"// Image {idx}, Label: {label}\n")
        f.write(f"static const uint8_t mnist_img_{idx}[784] = {{\n  ")
        for i, v in enumerate(img):
            f.write(f"{int(v)}")
            if i < 783:
                f.write(", ")
            if (i + 1) % 16 == 0:
                f.write("\n  ")
        f.write("\n};\n\n")

    f.write(f"static const int8_t mnist_labels[10] = {{")
    for idx in range(10):
        f.write(f"{test_data[idx][1]}")
        if idx < 9: f.write(", ")
    f.write("};\n\n")
    f.write("#endif\n")

print(f"Test images saved to: {img_path}")
print("\nDone!")
