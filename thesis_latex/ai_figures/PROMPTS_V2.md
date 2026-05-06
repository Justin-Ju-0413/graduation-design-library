# AI Figure Generation Prompts — V2 (Precise Instructions)

## Figure 2.1: System Architecture (必须严格按以下指令)

```
Draw a clean academic block diagram of an E203 RISC-V SoC with CNN accelerator.

CRITICAL RULES:
1. ITCM and DTCM must be connected in PARALLEL (side by side), NOT in series. Each has its OWN arrow down to the AHB Bus.
2. Only ONE Boot ROM block. Place it on the AHB bus (bottom), NOT in the top-right corner.
3. NICE arrow between CPU and Accelerator must be BIDIRECTIONAL (double-headed arrow ↔).
4. Vertical lines from modules to AHB bus must route AROUND peripherals, never THROUGH them.

LAYOUT (left to right, top to bottom):

LEFT (blue box): "E203 RISC-V Core (RV32IMAC)"
  - Inside: "IFU (Instruction Fetch)" top, "EXU (Execute + NICE)" bottom
  - Small text: "2-stage pipeline, Machine Mode"

MIDDLE (green box): "CNN Accelerator"
  - Inside: "NICE Decoder + Control FSM" top, "4×4 PE Array (INT8 MAC)" bottom
  - Small text: "NICE Interface"
  - Between CPU and Accelerator: orange DOUBLE-HEADED arrow ↔ labeled "NICE Req / Rsp"

RIGHT-TOP (purple box): "Memory"
  - "ITCM 64KB (64-bit) @ 0x8000_0000"
  - "DTCM 64KB @ 0x9000_0000"
  - These TWO blocks side-by-side, EACH with separate arrow down to bus

RIGHT-BOTTOM (gray box): "Peripherals"
  - "UART0 @ 0x1001_3000"
  - "GPIO"

BOTTOM (dark gray full-width bar): "AHB Bus Fabric"

ON THE BUS (small blocks above bus bar):
  - "CLINT @ 0x0200_0000"
  - "PLIC @ 0x0C00_0000"
  - "Boot ROM (MROM) @ 0x0000_0000"

COLORS: Soft pastels (light blue CPU, light green accelerator, light purple memory, light gray peripherals, dark gray bus). Clean black borders. No Comic Sans. 

FONT: All labels readable at 200 DPI. Title at top: "E203 SoC with NICE CNN Accelerator — System Architecture"
```

## Figure 2.3: PE Microarchitecture (必须严格按以下指令)

```
Draw a Processing Element (PE) microarchitecture diagram for a CNN accelerator.

CRITICAL RULES:
1. NO "accumulate" arrow from ReLU to Accumulator. That is WRONG.
2. Accumulator feedback: draw a small CIRCULAR LOOP arrow (↻) INSIDE or NEXT TO the Accumulator block. Label it "accumulate".
3. Data flow: Inputs → Multiplier → ReLU → Accumulator → Output (straight vertical line).
4. ReLU is an OPTIONAL step between Multiplier and Accumulator.

LAYOUT (vertical, top to bottom):

1. "W (INT8, 8-bit signed weight)" — input from TOP
2. "D (INT8, 8-bit signed activation)" — input from LEFT
3. "INT8 Multiplier" block (light blue):
   - Text: "W[7:0] × D[7:0] → P[15:0]"
4. "ReLU (optional)" block (light pink):
   - Text: "if en_relu && result < 0 → 0"
5. "INT32 Accumulator" block (light yellow):
   - Text: "acc ← acc + P (signed)"
   - Small text: "(reset on acc_clr)"
   - Draw a SMALL CIRCULAR ARROW ↻ inside or beside this block labeled "accumulate"
6. "Result (INT32)" — output at BOTTOM

Control signals from LEFT side:
- "acc_clr" (red) → Accumulator
- "en" (gray) → Accumulator

COLORS: Light blue (multiplier), light pink (ReLU), light yellow (accumulator). Dark borders. 

Title: "Processing Element (PE) Microarchitecture"
```

## Figure 2.4: PE Array (必须严格按以下指令)

```
Draw a 4×4 systolic PE array diagram.

CRITICAL RULES:
1. Tree Adder label: if it connects to 4 column outputs, label it "Tree Adder (4-input)". If 16 individual outputs, label "Tree Adder (16-input)" AND draw lines from ALL 16 PEs.
2. Every PE must be clearly labeled with its position: "PE 0,0", "PE 0,1", etc.
3. Weight inputs W[0]–W[3] from TOP, flowing DOWN each column.
4. Activation inputs D[0]–D[3] from LEFT, flowing RIGHT each row.
5. Bottom of each column connects to the Tree Adder.

LAYOUT:

4×4 grid (4 rows, 4 columns) of PE blocks. Each PE block labeled "PE R,C".
Alternating light green / white colors.

TOP: W[0], W[1], W[2], W[3] inputs with arrows pointing DOWN into each column.
LEFT: D[0], D[1], D[2], D[3] inputs with arrows pointing RIGHT into each row.

BOTTOM-RIGHT: One "Tree Adder" block. Arrows from ALL 4 column outputs flowing into it.
Output below: "Result (INT32)"

Title: "4×4 Systolic Processing Element Array"
Subtitle: "Output-Stationary Dataflow"

CLEAN grid. Large readable PE labels. No overlap.
```

## Figure 2.5: Packed INT8 Format (必须严格按以下指令)

```
Draw a data format diagram showing 4 INT8 values packed into one 32-bit register.

CRITICAL RULES:
1. Bit range labels must be CONSISTENT: use either [31:24], [23:16], [15:8], [7:0]
2. Show a horizontal bar divided into 4 equal 8-bit segments.
3. Below each segment: show both the INT8 value name AND the bit range.

LAYOUT:

Horizontal bar [31:0] divided into 4 colored segments:

| [31:24] | [23:16] | [15:8] | [7:0] |
| Value[3] (INT8) | Value[2] (INT8) | Value[1] (INT8) | Value[0] (INT8) |
| Byte 3 | Byte 2 | Byte 1 | Byte 0 |

Below: "Example: rs1 = 0x12_34_AB_CD"
With mapping arrows: 0x12→Value[3], 0x34→Value[2], 0xAB→Value[1], 0xCD→Value[0]

Annotation on left: arrow with text "WLOAD / DLOAD packs 4×INT8 → 32-bit register"

Title: "Packed INT8 Data Format for WLOAD and DLOAD Instructions"

Consistent spacing. Large readable fonts. No tick mark overlap.
```

---

## Steps After Generation
1. Save as: `fig3_1_soc_architecture.png`, `fig3_3_pe_microarchitecture.png`, `fig3_4_pe_array.png`, `fig3_5_packed_format.png`
2. Place in: `thesis_latex/figures/`
3. Overwrite existing files
4. Tell me, I'll rebuild PDF
