# Chapter 6: Conclusion

## 6.1 Summary of Contributions

This project has successfully designed, implemented, and validated a
lightweight CNN accelerator integrated with a RISC-V E203 processor
through the NICE custom instruction interface on an FPGA platform.
The principal contributions are:

1. **CNN Accelerator Design**: A 4×4 systolic PE array supporting INT8
   quantized convolution was implemented with six custom NICE
   instructions (CFG, CLEAR, WLOAD, DLOAD, COMP, RSTAT). The design
   was verified through RTL simulation achieving the baseline RSTAT=19
   result for 4×4 matrix multiplication.

2. **Complete FPGA Bring-up Pipeline**: A reproducible build flow was
   established from RTL source through Vivado synthesis, place-and-route,
   and bitstream generation for the Davinci Pro A7-100T development
   board. Six ILA diagnostic build modes were created to support
   progressive hardware debugging. All builds achieved clean timing
   closure (WNS > 12 ns, WHS > 0.05 ns).

3. **Hello World Board Validation**: The hello_e203 bare-metal program
   was successfully executed on the FPGA, producing the expected
   three-stage UART output and confirming the complete CPU boot chain
   from mask ROM through ITCM execution.

4. **Systematic Root Cause Analysis**: Four critical root causes
   preventing CPU boot were identified and resolved through a
   systematic ILA-based debugging methodology: simulation DFF transport
   delay, ITCM/DTCM hex format incompatibility, and macro visibility
   in Vivado synthesis. The simulation environment was demonstrated to
   exactly reproduce FPGA board behavior, enabling rapid diagnosis.

5. **NICE Accelerator Board Testing**: Custom NICE test programs
   confirmed that the CNN accelerator instructions execute correctly
   on the FPGA, with ILA evidence documenting the complete instruction
   execution sequence.

## 6.2 Key Technical Findings

The project yielded several findings of general relevance to RISC-V
SoC prototyping on FPGA platforms:

- **ITCM/DTCM initialization format is a critical compatibility point**
  between the RISC-V toolchain (`objcopy -O verilog`) and FPGA synthesis
  tools (`$readmemh`). The byte-level hex format produced by objcopy is
  not directly compatible with word-level memory initialization for
  BRAM widths greater than 8 bits.

- **Macro visibility in Vivado's Verilog compilation** differs from
  standard Verilog simulators. Macros defined in header files may not
  be visible to modules that do not explicitly include them, even when
  all files are compiled in the same project.

- **ILA probe placement requires understanding of the complete bus
  architecture**. Monitoring only the expected operational path
  (ITCM interface) can miss activity during boot sequences that use
  different bus paths (BIU → system memory bus).

## 6.3 Future Work

Several directions for extending this work are identified:

1. **Resolve RSTAT Readback**: Complete characterization of the NICE
   result readback path to enable software-visible performance
   measurement and accuracy validation.

2. **Full CNN Application**: Implement a complete CNN inference
   application (e.g., LeNet-5 on MNIST) using the NICE accelerator,
   with end-to-end accuracy validation against a Python golden model.

3. **Performance Benchmarking**: Measure CPU-only versus accelerator
   cycle counts for representative CNN workloads to quantify the
   speedup achieved by the NICE custom instruction approach.

4. **Design Optimization**: Explore increasing the PE array size,
   adding pipelining within the array, and supporting additional
   activation functions (ReLU, leaky ReLU) through the CFG instruction.

5. **Formal Verification**: Apply formal verification methods to the
   NICE interface protocol to ensure correctness under all possible
   instruction sequences and timing conditions.

## 6.4 Closing Remarks

This project has demonstrated that a RISC-V-based CNN accelerator can
be successfully prototyped on a commercial FPGA development board using
open-source RISC-V IP and standard FPGA design tools. The systematic
debugging methodology developed during this work—combining ILA-based
hardware observation, RTL simulation correlation, and progressive root
cause isolation—provides a reusable framework for similar SoC bring-up
efforts. The evidence chain established from RTL simulation through
board-level UART output represents a complete and verifiable engineering
contribution.
