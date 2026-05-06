# AI Image Generation Prompts for Thesis Figures

Use Nanobanana AI. All outputs should be professional academic quality: clean vector style, serif fonts, consistent color palette.

---

## 1. System Architecture Diagram (Figure 2.1)
**Replaces:** `fig3_1_soc_architecture.png`

```
Draw a professional academic system architecture block diagram for an FPGA SoC.
Title: "E203 SoC with NICE CNN Accelerator — System Architecture"

Left block (blue): "E203 RISC-V Core (RV32IMAC)" with sub-blocks "IFU" and "EXU + NICE Interface". Label "2-stage pipeline, Machine Mode".

Middle block (green): "CNN Accelerator" with sub-blocks "NICE Decoder + Control FSM" and "4×4 PE Array (INT8 MAC)". Label "NICE Interface".

Right-top block (purple): "ITCM 64KB (64-bit) @ 0x8000_0000" and "DTCM 64KB @ 0x9000_0000".

Right-bottom block (gray): "UART0 @ 0x1001_3000" and "GPIO".

Bottom bar (dark gray): "AHB Bus Fabric".

Three peripherals on bus: "CLINT @ 0x0200_0000", "PLIC @ 0x0C00_0000", "Boot ROM (MROM) @ 0x0000_0000".

Bidirectional arrow (orange, double-headed) between CPU and Accelerator labeled "NICE Req / Rsp".

Vertical lines from each block to the AHB Bus bar. IMPORTANT: lines must route AROUND peripherals, not THROUGH them.

Color scheme: soft pastels with dark borders, professional academic style. No Comic Sans. Use consistent font sizes.
```

---

## 2. PE Microarchitecture (Figure 2.3)
**Replaces:** `fig3_3_pe_microarchitecture.png`

```
Draw a professional academic diagram of a Processing Element (PE) microarchitecture.
Title: "Processing Element (PE) Microarchitecture"

Top-to-bottom data flow:
1. Inputs: "W (INT8, 8-bit signed weight)" from top, "D (INT8, 8-bit signed activation)" from left
2. "INT8 Multiplier" block (light blue) with formula "W[7:0] × D[7:0] → P[15:0]"
3. "ReLU (optional)" block (light red/pink) with text "if en_relu && result < 0 then 0"
4. "INT32 Accumulator" block (light yellow) with text "acc ← acc + P (signed)" and note "(reset on acc_clr)"
5. Output: "Result (INT32)"

CRITICAL: Draw an orange FEEDBACK LOOP (circular/loop arrow) from the Accumulator output back to its input, labeled "accumulate". This represents the feedback nature of accumulation. Do NOT draw a straight bypass arrow.

Control signals from left: "acc_clr" (red), "en" (gray).

All blocks clearly separated with space between them. NO text overlap. Arrows between blocks. Professional academic style with consistent line weights.
```

---

## 3. PE Array Organization (Figure 2.4)
**Replaces:** `fig3_4_pe_array.png`

```
Draw a 4×4 systolic processing element array diagram.
Title: "4×4 Systolic Processing Element Array"
Subtitle: "Output-Stationary Dataflow"

Draw a 4-row × 4-column grid of PE blocks (each labeled "PE 0,0", "PE 0,1" etc.). Use alternating light green shades. PE labels must be clearly readable, minimum font equivalent to 10pt.

Weight inputs from TOP: W[0], W[1], W[2], W[3] flow DOWN through each column. Show vertical arrows along the left side of each column.

Activation inputs from LEFT: D[0], D[1], D[2], D[3] flow RIGHT through each row. Show horizontal arrows along the top of each row.

Results from BOTTOM of each column flow into a "Tree Adder" block on the right. Output labeled "Result (INT32)".

Clean grid layout with consistent spacing. No text overlap. Professional academic style.
```

---

## 4. Packed INT8 Data Format (Figure 2.5)
**Replaces:** `fig3_5_packed_format.png`

```
Draw a professional diagram showing how 4 INT8 values are packed into one 32-bit register.
Title: "Packed INT8 Data Format for WLOAD and DLOAD Instructions"

Show a horizontal bar representing a 32-bit register [31:0], divided into 4 equal segments of 8 bits each:

| Byte 3 [31:24] | Byte 2 [23:16] | Byte 1 [15:8] | Byte 0 [7:0] |
| Value[3] (INT8) | Value[2] (INT8) | Value[1] (INT8) | Value[0] (INT8) |

Below each segment, show:
- Bit range label (e.g., "[31:24]", "[23:16]", "[15:8]", "[7:0]")
- INT8 designation (e.g., "Value[3]", "Value[2]", "Value[1]", "Value[0]")

Below the bar, show an example:
"Example: rs1 = 0x12 0x34 0xAB 0xCD"
→ Value[3]=0x12, Value[2]=0x34, Value[1]=0xAB, Value[0]=0xCD

CRITICAL: Bit numbers below the bar must use CONSISTENT annotation. Use either all starting boundary (0, 8, 16, 24) or all ending boundary (7, 15, 23, 31). Do NOT mix them. Recommended: show [31:24], [23:16], [15:8], [7:0].

Arrow indicating "WLOAD / DLOAD packs 4×INT8 → 32-bit register". 

Clean layout, professional academic style. Large readable fonts. No overlap.
```

---

## 5. FPGA Board Photo (Figure 3.1 or Appendix)
**Replaces:** `fig_fpga_board.jpg`

```
This is a PHOTO, not an AI-generated image.

Instructions for retaking:
1. Clean the desk surface
2. Remove ALL USB cables and jumper wires from the board
3. Place the Davinci Pro A7-100T FPGA board flat on a clean white/gray surface
4. Take photo from directly above (top-down view)
5. Ensure good even lighting, no shadows
6. The entire board must be visible, no obstructions at edges
7. Save at minimum 1200px wide, sharp focus
```

---

## Additional Chart Fixes (Matplotlib — will be handled by code)

**Figure 3.3 (Speedup Bar):** Make the speedup bar thinner (narrower width). Y-axis labels too bold — reduce font weight.

**Figure 3.4 (ILA NICE Activity):** Instruction labels (CLEAR, WLOAD, DLOAD, COMP, RSTAT) need to be larger font and better aligned. Currently crowded at top right.

**Figure 3.2 (ILA PC Trace):** Annotation text for "hello_e203 Execution", "Done Loop" needs slightly larger font.

**Figure 3.x (Timing Closure):** Legend box overlapping green annotation — already fixed by moving legend to upper left and annotation lower.
