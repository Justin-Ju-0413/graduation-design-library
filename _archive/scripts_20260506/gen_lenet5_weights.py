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

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
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

# Quantize weights to INT8
print("\nQuantizing weights to INT8...")

def quantize_tensor(t, name=""):
    """Quantize a tensor to INT8: scale to [-128, 127]"""
    t_np = t.detach().cpu().numpy()
    max_abs = np.max(np.abs(t_np))
    if max_abs == 0:
        max_abs = 1.0
    scale = 127.0 / max_abs
    q = np.clip(np.round(t_np * scale), -128, 127).astype(np.int8)
    # Store scale for dequantization
    return q, float(max_abs / 127.0)

# Extract weights
conv1_weight, conv1_scale = quantize_tensor(model.conv1.weight, "conv1.weight")
conv1_bias = model.conv1.bias.detach().cpu().numpy()
conv1_bias_q, conv1_bias_scale = quantize_tensor(model.conv1.bias)

conv2_weight, conv2_scale = quantize_tensor(model.conv2.weight, "conv2.weight")
conv2_bias = model.conv2.bias.detach().cpu().numpy()
conv2_bias_q, conv2_bias_scale = quantize_tensor(model.conv2.bias)

fc1_weight, fc1_scale = quantize_tensor(model.fc1.weight, "fc1.weight")
fc1_bias, fc1_bias_s = quantize_tensor(model.fc1.bias)

fc2_weight, fc2_scale = quantize_tensor(model.fc2.weight, "fc2.weight")
fc2_bias, fc2_bias_s = quantize_tensor(model.fc2.bias)

fc3_weight, fc3_scale = quantize_tensor(model.fc3.weight, "fc3.weight")
fc3_bias, fc3_bias_s = quantize_tensor(model.fc3.bias)

print(f"Conv1 weight: shape={conv1_weight.shape}, range=[{conv1_weight.min()}, {conv1_weight.max()}]")
print(f"Conv2 weight: shape={conv2_weight.shape}, range=[{conv2_weight.min()}, {conv2_weight.max()}]")
print(f"FC1 weight: shape={fc1_weight.shape}, range=[{fc1_weight.min()}, {fc1_weight.max()}]")
print(f"FC2 weight: shape={fc2_weight.shape}, range=[{fc2_weight.min()}, {fc2_weight.max()}]")
print(f"FC3 weight: shape={fc3_weight.shape}, range=[{fc3_weight.min()}, {fc3_weight.max()}]")

# Generate C header
OUT_DIR = r"C:\Users\16084\Documents\New project\riscv_cnn_accelerator\sw\inc"
os.makedirs(OUT_DIR, exist_ok=True)

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
    write_array(f, "lenet5_conv1_weight", conv1_weight, "6x1x5x5")
    write_array_i32(f, "lenet5_conv1_bias", conv1_bias_q, "6")

    # Conv2: [16, 6, 5, 5] = 2400 weights + 16 biases
    write_array(f, "lenet5_conv2_weight", conv2_weight, "16x6x5x5")
    write_array_i32(f, "lenet5_conv2_bias", conv2_bias_q, "16")

    # FC1: [120, 256] = 30720 weights + 120 biases
    write_array(f, "lenet5_fc1_weight", fc1_weight, "120x256")
    write_array_i32(f, "lenet5_fc1_bias", fc1_bias, "120")

    # FC2: [84, 120] = 10080 weights + 84 biases
    write_array(f, "lenet5_fc2_weight", fc2_weight, "84x120")
    write_array_i32(f, "lenet5_fc2_bias", fc2_bias, "84")

    # FC3: [10, 84] = 840 weights + 10 biases
    write_array(f, "lenet5_fc3_weight", fc3_weight, "10x84")
    write_array_i32(f, "lenet5_fc3_bias", fc3_bias, "10")

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
        img = (test_data[idx][0].numpy() * 255).astype(np.int8).flatten()
        label = test_data[idx][1]
        f.write(f"// Image {idx}, Label: {label}\n")
        f.write(f"static const int8_t mnist_img_{idx}[784] = {{\n  ")
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
