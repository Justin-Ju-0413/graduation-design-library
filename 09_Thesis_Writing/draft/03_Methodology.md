# Chapter 3: Methodology

This chapter describes the design methodology for the RISC-V custom instruction-based lightweight CNN accelerator. The overall architecture follows a hierarchical approach: at the system level, the E200-series RISC-V processor serves as the host, and the CNN accelerator is attached as a NICE (Nuclei Instruction Co-extension) coprocessor. At the instruction level, six custom instructions encode all accelerator control and data movement operations. At the datapath level, a 4x4 processing element (PE) array performs the multiply-accumulate (MAC) computations in parallel. Finally, the FPGA bring-up methodology bridges the gap between RTL simulation and on-board hardware validation.

---

## 3.1 System Architecture Overview

The system architecture integrates a RISC-V E203 Hummingbird v2 processor core with a custom CNN accelerator through the NICE coprocessor interface. Figure 3.1 illustrates the top-level block diagram of the complete SoC.

```
+------------------------------------------------------------------+
|                          SoC                                      |
|  +----------------------------+    +---------------------------+  |
|  |    E203 Core (RISC-V)      |    |   CNN Accelerator        |  |
|  |  +----------------------+  |    |  +---------------------+ |  |
|  |  |  Instruction Fetch   |  |    |  |  cnn_nice_core      | |  |
|  |  |  (IFU)               |  |    |  |  - NICE decoder     | |  |
|  |  +----------+-----------+  |    |  |  - Control FSM      | |  |
|  |             |              |    |  +----------+----------+ |  |
|  |  +----------+-----------+  |    |             |            |  |
|  |  |  Execute (EXU)       |  |    |  +----------+----------+ |  |
|  |  |  - Integer ALU       |  |    |  |  PE Array (4x4)     | |  |
|  |  |  - NICE Interface    |--+----+--|  - 16 PEs           | |  |
|  |  +----------------------+  |    |  |  - INT8 MAC         | |  |
|  |             |              |    |  |  - INT32 Acc        | |  |
|  |  +----------+-----------+  |    |  |  - OS Dataflow      | |  |
|  |  |  LSU / BIU           |  |    |  +---------------------+ |  |
|  |  +----------------------+  |    +---------------------------+  |
|  +----------------------------+                                    |
|             |                                                     |
|  +----------+-----------+    +---------------------------+        |
|  |   ITCM (64-bit)      |    |   DTCM (32-bit)          |        |
|  |  0x8000_0000 -       |    |  0x9000_0000 -           |        |
|  |  0x8001_FFFF         |    |  0x9000_FFFF             |        |
|  +----------------------+    +---------------------------+        |
|                                                                   |
|  +----------------------+    +---------------------------+        |
|  |   CLINT              |    |   PLIC                    |        |
|  |  0x0200_0000         |    |  0x0C00_0000             |        |
|  +----------------------+    +---------------------------+        |
|                                                                   |
|  +----------------------+    +---------------------------+        |
|  |   UART0              |    |   GPIO                    |        |
|  |  (GPIO16=RX,         |    |                           |        |
|  |   GPIO17=TX)         |    |                           |        |
|  +----------------------+    +---------------------------+        |
+------------------------------------------------------------------+
```

**Figure 3.1:** System-level block diagram of the E203 SoC with the CNN NICE accelerator.

The E203 core is a 32-bit, 2-stage in-order RISC-V processor implementing the RV32IMAC instruction set. It provides a complete memory subsystem including an instruction tightly-coupled memory (ITCM) mapped at 0x8000_0000 and a data tightly-coupled memory (DTCM) mapped at 0x9000_0000. Standard peripherals---the Core Local Interruptor (CLINT), Platform-Level Interrupt Controller (PLIC), UART0, and GPIO---are connected through the system bus fabric.

The CNN accelerator does not occupy a memory-mapped address range. Instead, it communicates with the processor exclusively through the NICE interface, which extends the processor's execution pipeline with custom datapath logic. This architectural choice was made for three reasons:

1. **Low latency:** Custom instructions execute within the processor pipeline, eliminating the round-trip delay of bus transactions.
2. **Programming convenience:** The accelerator is controlled through standard RISC-V assembly instructions rather than load/store operations to memory-mapped registers.
3. **Simplified integration:** No bus arbitration, address decoding, or memory protection logic is required for the accelerator interface.

The system runs from the ITCM during normal operation. On reset, the E203 core fetches the first instruction from the boot ROM (MROM) at address 0x0000_0000, which contains a jump vector that redirects execution to the start of the user program in ITCM. The DTCM stores input data (weights, activations) and output results, which are loaded into the accelerator via the NICE custom instructions.

Table 3.1 summarizes the address map of the system.

**Table 3.1:** SoC address space map.

| Peripheral   | Address Range   | Width  | Description                     |
|--------------|-----------------|--------|---------------------------------|
| MROM (Boot)  | 0x0000_0000     | 32-bit | Boot ROM with reset vector      |
| ITCM         | 0x8000_0000 -   | 64-bit | Instruction memory (128 KB)     |
|              | 0x8001_FFFF     |        |                                 |
| DTCM         | 0x9000_0000 -   | 32-bit | Data memory (64 KB)             |
|              | 0x9000_FFFF     |        |                                 |
| CLINT        | 0x0200_0000     | 32-bit | Core local interruptor          |
| PLIC         | 0x0C00_0000     | 32-bit | Platform-level interrupt ctrl   |
| UART0        | 0x1001_3000     | 32-bit | Serial communication            |

---

## 3.2 NICE Custom Instruction Design

### 3.2.1 The NICE Protocol

The NICE (Nuclei Instruction Co-extension) interface is a standardized coprocessor extension mechanism provided by the E203 processor. Unlike a memory-mapped peripheral, the NICE interface integrates the accelerator directly into the processor's execution stage. The interface consists of four logical channels:

- **Request channel:** Carries the instruction word and source register operands from the processor to the accelerator.
- **Response channel:** Returns the result value from the accelerator to the processor's register file.
- **Memory request channel (optional):** Allows the accelerator to initiate its own memory transactions.
- **Memory response channel (optional):** Returns data for memory read requests initiated by the accelerator.

In this design, the memory channels are not used. All data transfers between the processor and the accelerator occur through register operands (rs1 and rs2), which avoids the complexity of bus mastering and keeps the accelerator control logic simple.

The request channel signals are summarized in Table 3.2.

**Table 3.2:** NICE request and response channel signals.

| Signal            | Direction  | Width  | Description                          |
|-------------------|------------|--------|--------------------------------------|
| `nice_req_valid`  | Core to Acc| 1      | Request valid strobe                 |
| `nice_req_ready`  | Core from Acc| 1    | Accelerator ready for request        |
| `nice_req_instr`  | Core to Acc| 32     | Full instruction word                |
| `nice_req_rs1`    | Core to Acc| 32     | Source operand 1 (from integer reg.) |
| `nice_req_rs2`    | Core to Acc| 32     | Source operand 2 (from integer reg.) |
| `nice_rsp_valid`  | Core from Acc| 1    | Response valid strobe                |
| `nice_rsp_ready`  | Core to Acc| 1      | Processor ready to accept response   |
| `nice_rsp_rdat`   | Core from Acc| 32    | Result data written to destination reg. |

The handshake protocol uses a valid-ready mechanism on both channels. The request is a single-cycle pulse: the processor asserts `nice_req_valid` for exactly one clock cycle, and the accelerator captures the instruction and operands on the rising edge when `nice_req_ready` is also asserted. During computation, the accelerator de-asserts `nice_req_ready` to block new requests. When the result is ready, the accelerator asserts `nice_rsp_valid` and holds it until the processor responds with `nice_rsp_ready`.

### 3.2.2 Instruction Encoding

The six custom instructions use the RISC-V `custom0` opcode (0x0B). Because the E203 NICE interface repurposes bits [14:12] as `{xd, xs1, xs2}` control flags rather than the standard `funct3` field, the instruction differentiation is encoded entirely within the `funct7` field (bits [31:25]).

Figure 3.2 shows the instruction format.

```
 31          25  24  20  19  15  14  12  11      7  6       0
+---------------+-------+-------+--------+--------+-------------+
|   funct7      |  rs2  |  rs1  |xd/xs1/ |   rd   |   opcode    |
|    7-bit      |  5-bit|  5-bit| xs2    |  5-bit |   7-bit     |
|               |       |       | 3-bit  |        |   (0x0B)    |
+---------------+-------+-------+--------+--------+-------------+

  E203 NICE encoding of bits [14:12]:
    bit 14 = xd  (1 = write result to rd)
    bit 13 = xs1 (1 = read rs1 operand)
    bit 12 = xs2 (1 = read rs2 operand)
```

**Figure 3.2:** RISC-V custom instruction format as interpreted by the E203 NICE interface.

Table 3.3 defines the six custom instructions.

**Table 3.3:** NICE custom instruction set for the CNN accelerator.

| Instruction | funct7 | xd | xs1 | xs2 | Encoding (hex) | Description                           |
|-------------|--------|----|-----|-----|----------------|---------------------------------------|
| CFG         | 5      | 0  | 1   | 0   | 0x0A00100B     | Configure: rs1[0] enables ReLU        |
| CLEAR       | 4      | 0  | 0   | 0   | 0x0800000B     | Clear all PE accumulators and masks   |
| WLOAD       | 0      | 0  | 1   | 1   | 0x0001800B     | Load weight column: rs1=data, rs2=idx |
| DLOAD       | 1      | 0  | 1   | 1   | 0x0201800B     | Load activation row: rs1=data, rs2=idx|
| COMP        | 2      | 0  | 0   | 0   | 0x0400000B     | Trigger MAC computation on all PEs    |
| RSTAT       | 3      | 1  | 0   | 0   | 0x0600250B     | Read accumulator result into rd       |

The key design decisions for this encoding are as follows.

**WLOAD and DLOAD** pack four INT8 values (32 bits total) into the rs1 register. The rs2 register supplies a 2-bit column/row index (0--3), selecting which group of four PEs to load. Over four consecutive WLOAD instructions, all 16 weight registers are filled; likewise, four DLOAD instructions fill all 16 activation registers.

**COMP** initiates parallel computation across the PE array. The accelerator checks that all four weight slots and all four activation slots have been loaded (via the `w_loaded_mask` and `d_loaded_mask` registers) before enabling the PE array. If either mask is incomplete, COMP returns an error.

**RSTAT** reads the final accumulated sum. The accelerator holds the result in a dedicated register and makes it available only after a COMP instruction has completed. Reading before COMP produces an error response.

**CFG** configures the optional ReLU (rectified linear unit) post-processing. When `rs1[0] = 1`, negative results are clamped to zero.

**CLEAR** resets all PE accumulators, the loaded mask registers, and the internal state machine to the idle state.

### 3.2.3 Instruction Decode and Control Logic

The NICE instruction decoder in `cnn_nice_core.v` inspects the funct7 field of the incoming instruction and generates the appropriate control signals. The Verilog code for the decoding logic is shown in Listing 3.1.

```verilog
// Listing 3.1: NICE instruction decoding and control logic (excerpt from
// cnn_nice_core.v). The funct7 field selects among six custom operations.
// Each operation is served in a single clock cycle except COMP, which spans
// multiple cycles.

localparam [6:0] NICE_OPCODE = 7'h0b;
localparam [6:0] FN_WLOAD = 7'd0;
localparam [6:0] FN_DLOAD = 7'd1;
localparam [6:0] FN_COMP  = 7'd2;
localparam [6:0] FN_RSTAT = 7'd3;
localparam [6:0] FN_CLEAR = 7'd4;
localparam [6:0] FN_CFG   = 7'd5;

assign funct7 = nice_req_instr[31:25];
assign is_nice_opcode = (nice_req_instr[6:0] == NICE_OPCODE);
assign rs2_idx_valid = (nice_req_rs2[31:2] == 30'b0);

assign nice_req_ready = ~rsp_pending & ~busy;

always @(posedge clk or negedge rst_n) begin
    // ... reset logic omitted for brevity ...

    if(nice_req_valid && nice_req_ready) begin
        if(!is_nice_opcode) begin
            rsp_err_q <= 1'b1;    // illegal opcode
            rsp_pending <= 1'b1;
        end else if(!rs2_idx_valid) begin
            rsp_err_q <= 1'b1;    // rs2 index out of range
            rsp_pending <= 1'b1;
        end else begin
            case(funct7)
                FN_WLOAD: begin
                    load_data_q   <= nice_req_rs1;
                    load_vec_sel_q <= nice_req_rs2[1:0];
                    w_load         <= 1'b1;
                    w_loaded_mask[nice_req_rs2[1:0]] <= 1'b1;
                    rsp_pending    <= 1'b1;
                end
                FN_DLOAD: begin
                    load_data_q   <= nice_req_rs1;
                    load_vec_sel_q <= nice_req_rs2[1:0];
                    d_load         <= 1'b1;
                    d_loaded_mask[nice_req_rs2[1:0]] <= 1'b1;
                    rsp_pending    <= 1'b1;
                end
                FN_COMP: begin
                    if((w_loaded_mask == 4'b1111) &&
                       (d_loaded_mask == 4'b1111)) begin
                        en_pe <= 1'b1;
                        busy  <= 1'b1;
                        busy_wait_result <= 1'b1;
                    end else begin
                        rsp_err_q <= 1'b1;  // data not fully loaded
                        rsp_pending <= 1'b1;
                    end
                end
                FN_RSTAT: begin
                    if(result_valid) begin
                        rsp_rdat_q <= result_sum_q;
                        rsp_pending <= 1'b1;
                    end else begin
                        rsp_err_q <= 1'b1;
                        rsp_pending <= 1'b1;
                    end
                end
                FN_CLEAR: begin
                    acc_clr         <= 1'b1;
                    w_loaded_mask   <= 4'b0;
                    d_loaded_mask   <= 4'b0;
                    result_valid    <= 1'b0;
                    result_sum_q    <= 32'b0;
                    rsp_pending     <= 1'b1;
                end
                FN_CFG: begin
                    relu_en_q <= nice_req_rs1[0];
                    rsp_pending <= 1'b1;
                end
                default: begin
                    rsp_err_q <= 1'b1;    // unknown funct7
                    rsp_pending <= 1'b1;
                end
            endcase
        end
    end
end
```

The decoder includes two error-checking mechanisms. First, if the instruction opcode is not 0x0B (custom0), the accelerator reports an error via `nice_rsp_err`. Second, for WLOAD and DLOAD instructions, the rs2 index is validated: only the lower two bits may be nonzero, ensuring the index is in the range [0, 3].

The COMP instruction implements a guard condition: the accelerator asserts `en_pe` only if all four weight-load and all four data-load operations have been completed, tracked by `w_loaded_mask` and `d_loaded_mask`. This prevents undefined behavior from partial data loading.

### 3.2.4 Software Programming Model

The accelerator is programmed through inline assembly macros. Listing 3.2 shows the C header file wrapper.

```c
// Listing 3.2: C-language wrapper macros for the NICE custom instructions.

#define CNN_CLEAR() do {                                         \
    __asm__ volatile(".insn r 0x0b, 0, 4, x0, x0, x0"           \
                     ::: "memory");                              \
} while(0)

#define CNN_WLOAD(data, idx) do {                                \
    __asm__ volatile(".insn r 0x0b, 0, 0, x0, %0, %1"           \
                     :: "r"(data), "r"(idx));                    \
} while(0)

#define CNN_DLOAD(data, idx) do {                                \
    __asm__ volatile(".insn r 0x0b, 0, 1, x0, %0, %1"           \
                     :: "r"(data), "r"(idx));                    \
} while(0)

#define CNN_COMP() do {                                          \
    __asm__ volatile(".insn r 0x0b, 0, 2, x0, x0, x0"           \
                     ::: "memory");                              \
} while(0)

#define CNN_RSTAT(result) do {                                   \
    __asm__ volatile(".insn r 0x0b, 0, 3, %0, x0, x0"           \
                     : "=r"(result));                            \
} while(0)
```

A typical convolution kernel follows a five-step sequence: (1) CLEAR to reset the accelerator state, (2) four WLOAD calls to load the weight columns, (3) four DLOAD calls to load the activation rows, (4) COMP to trigger computation, and (5) RSTAT to read the accumulated result. The data-flow pattern is described in detail in the next section.

---

## 3.3 PE Array Architecture

### 3.3.1 Processing Element Microarchitecture

Each processing element in the 4x4 array implements a single MAC operation on INT8 operands with INT32 accumulation. The PE is designed for output-stationary (OS) dataflow, meaning the partial sum is stored locally in the PE's accumulator register.

Figure 3.3 illustrates the PE datapath.

```
          INT8              INT8
      Weight (W)      Activation (D)
           |                |
           v                v
     +---------------------------+
     |    Multiplier             |
     |    (INT8 x INT8)          |
     |    = INT16 result         |
     +------------+-------------+
                  |
                  v
     +---------------------------+
     |  Accumulator (INT32)      |
     |  Acc <= Acc + (W x D)     |
     |  +------------------------+
     |  | Clear on: rst_n,       |
     |  |         acc_clr        |
     |  +------------------------+
     +------------+-------------+
                  |
                  v
            Result[31:0]
```

**Figure 3.3:** Processing element microarchitecture showing the INT8 multiplier and INT32 accumulator.

The PE RTL implementation is shown in Listing 3.3.

```verilog
// Listing 3.3: Single processing element (PE) implementation.
// Multiplies INT8 weight (w) by INT8 activation (d) and accumulates
// into a signed 32-bit register.

module pe(
    input                   clk,
    input                   rst_n,
    input                   acc_clr,
    input                   en,
    input  signed [7:0]     w,
    input  signed [7:0]     d,
    output reg signed [31:0] acc
);
    always @(posedge clk or negedge rst_n) begin
        if(!rst_n || acc_clr) begin
            acc <= 32'sd0;
        end else if(en) begin
            acc <= acc + (w * d);
        end
    end
endmodule
```

The accumulator supports two reset sources: a global `rst_n` for power-on reset and an `acc_clr` signal driven by the CLEAR instruction. The `en` signal, driven by the COMP instruction, gates the MAC operation. When `en` is de-asserted, the accumulator holds its current value, enabling multi-cycle accumulation across multiple COMP invocations if desired.

The signed multiplication `w * d` produces an INT16 intermediate result that is automatically sign-extended to INT32 by the addition operation, preventing overflow within a single MAC cycle. For multi-cycle accumulation across multiple convolution channels, the INT32 accumulator provides sufficient dynamic range: with 16 accumulated products, the maximum absolute sum is 16 x 127 x 127 = 258,064, well within the range of a 32-bit signed integer.

### 3.3.2 Systolic Array Organization

The 16 PEs are organized as a 4x4 grid. Each column shares a common weight value, and each row shares a common activation value. This organization maps directly to the computation of one output element in a 4x4 matrix multiplication: each PE computes the product of weight column i and activation row j, and the 16 products are summed to form the output.

Figure 3.4 shows the array structure and the data distribution pattern.

```
                 Weight Columns (WLOAD index)
                W[0]    W[1]    W[2]    W[3]
            +--------+--------+--------+--------+
     D[0]   | PE00   | PE01   | PE02   | PE03   |  Activation
            | W[0]*D0| W[1]*D0| W[2]*D0| W[3]*D0|  Row 0
            +--------+--------+--------+--------+
     D[1]   | PE10   | PE11   | PE12   | PE13   |  Activation
            | W[0]*D1| W[1]*D1| W[2]*D1| W[3]*D1|  Row 1
            +--------+--------+--------+--------+
     D[2]   | PE20   | PE21   | PE22   | PE23   |  Activation
            | W[0]*D2| W[1]*D2| W[2]*D2| W[3]*D2|  Row 2
            +--------+--------+--------+--------+
     D[3]   | PE30   | PE31   | PE32   | PE33   |  Activation
            | W[0]*D3| W[1]*D3| W[2]*D3| W[3]*D3|  Row 3
            +--------+--------+--------+--------+

     Result = sum of all 16 PE outputs
```

**Figure 3.4:** 4x4 PE array organization showing weight column broadcast and activation row broadcast.

The weight and activation storage within the PE array uses a column-wise and row-wise register file, implemented in `pe_array.v` (Listing 3.4).

```verilog
// Listing 3.4: PE array module showing weight and activation register file
// organization and the tree adder for the final sum.

module pe_array(
    input                   clk,
    input                   rst_n,
    input                   acc_clr,
    input                   en,
    input                   w_load,
    input                   d_load,
    input        [1:0]      vec_sel,
    input        [31:0]     w_in,
    input        [31:0]     d_in_packed,
    output signed [31:0]    out_sum
);
    reg signed [7:0] w_reg[15:0];
    reg signed [7:0] d_reg[15:0];
    wire signed [31:0] acc_out[15:0];

    generate
        for(i=0; i<16; i=i+1) begin : g_pe
            pe u_pe(clk, rst_n, acc_clr, en, w_reg[i], d_reg[i], acc_out[i]);
        end
    endgenerate

    always @(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            for(idx=0; idx<16; idx=idx+1) begin
                w_reg[idx] <= 8'sd0;
                d_reg[idx] <= 8'sd0;
            end
        end else begin
            if(w_load) begin
                case(vec_sel)
                    2'b00: {w_reg[3],  w_reg[2],  w_reg[1],  w_reg[0]}   <= w_in;
                    2'b01: {w_reg[7],  w_reg[6],  w_reg[5],  w_reg[4]}   <= w_in;
                    2'b10: {w_reg[11], w_reg[10], w_reg[9],  w_reg[8]}   <= w_in;
                    2'b11: {w_reg[15], w_reg[14], w_reg[13], w_reg[12]}  <= w_in;
                endcase
            end
            if(d_load) begin
                case(vec_sel)
                    2'b00: {d_reg[3],  d_reg[2],  d_reg[1],  d_reg[0]}   <= d_in_packed;
                    2'b01: {d_reg[7],  d_reg[6],  d_reg[5],  d_reg[4]}   <= d_in_packed;
                    2'b10: {d_reg[11], d_reg[10], d_reg[9],  d_reg[8]}   <= d_in_packed;
                    2'b11: {d_reg[15], d_reg[14], d_reg[13], d_reg[12]}  <= d_in_packed;
                endcase
            end
        end
    end

    assign out_sum = acc_out[0]  + acc_out[1]  + acc_out[2]  + acc_out[3]  +
                     acc_out[4]  + acc_out[5]  + acc_out[6]  + acc_out[7]  +
                     acc_out[8]  + acc_out[9]  + acc_out[10] + acc_out[11] +
                     acc_out[12] + acc_out[13] + acc_out[14] + acc_out[15];
endmodule
```

### 3.3.3 Data Loading and Computation Schedule

The NICE bus width is 32 bits, but the PE array requires 128 bits of weight data (16 x INT8) and 128 bits of activation data. To bridge this bandwidth gap, the loading is serialized across four cycles per data type.

The complete computation schedule is:

```
Clock Cycle   Operation         Data Movement
-----------   ---------         ----------------------------
    T0        WLOAD idx=0       w_in[31:0] -> Column 0 registers
    T1        WLOAD idx=1       w_in[31:0] -> Column 1 registers
    T2        WLOAD idx=2       w_in[31:0] -> Column 2 registers
    T3        WLOAD idx=3       w_in[31:0] -> Column 3 registers
    T4        DLOAD idx=0       d_in[31:0] -> Row 0 registers
    T5        DLOAD idx=1       d_in[31:0] -> Row 1 registers
    T6        DLOAD idx=2       d_in[31:0] -> Row 2 registers
    T7        DLOAD idx=3       d_in[31:0] -> Row 3 registers
    T8        COMP (cycle 1)    All 16 PEs compute MAC in parallel
    T9        RSTAT             Result sum is available for readout
```

**Table 3.4:** Computation schedule for one 4x4 matrix multiply-accumulate operation.

The packed data format packs four INT8 values into one 32-bit word as shown in Figure 3.5.

```
  31        24 23        16 15         8 7          0
+-------------+-------------+-------------+-------------+
|   Value 3   |   Value 2   |   Value 1   |   Value 0   |
|   INT8      |   INT8      |   INT8      |   INT8      |
+-------------+-------------+-------------+-------------+
```

**Figure 3.5:** Packed INT8 data format within a 32-bit register for WLOAD and DLOAD.

### 3.3.4 Post-Processing: Optional ReLU

After the computation completes and before the result is stored in the output register, an optional ReLU activation function is applied. The ReLU is implemented as a conditional multiplexer:

```verilog
assign result_sum_post = (relu_en_q && result_sum[31]) ? 32'sd0 : result_sum;
```

When `relu_en_q` is set (via the CFG instruction) and the result's sign bit (bit 31) is 1, the output is clamped to zero. Otherwise, the raw accumulator sum is passed through unchanged.

### 3.3.5 Resource Estimation

The PE array resource footprint is dominated by the 16 MAC units. Table 3.5 provides the estimated FPGA resource utilization.

**Table 3.5:** Estimated FPGA resource utilization for the 4x4 PE array on an Artix-7 device.

| Resource       | Quantity | Width     | Description                        |
|----------------|----------|-----------|------------------------------------|
| Multiplier     | 16       | 8 x 8     | Signed INT8 multiplication         |
| Adder          | 16       | 32-bit    | Accumulation per PE                |
| Weight regs    | 16       | 8-bit     | Distributed as flip-flops          |
| Activation regs| 16       | 8-bit     | Distributed as flip-flops          |
| Accumulator    | 16       | 32-bit    | In each PE, registered             |
| Tree adder     | 1        | 32-bit    | 16-input summation for final result |
| Control logic  | ~200 LUT | -         | FSM, decoder, mask registers       |

---

## 3.4 SoC Integration

### 3.4.1 Integration Hierarchy

The CNN accelerator is integrated into the E203 SoC at the subsystem level. The `e203_subsys_nice_core` module, which is the standard NICE integration wrapper provided by Nuclei, instantiates the `cnn_nice_core` module. This wrapper connects the NICE request/response signals between the E203 core and the accelerator.

The integration hierarchy is:

```
e203_soc_top.v
  |-- e203_subsys_main.v
       |-- e203_subsys_top.v
            |-- e203_cpu.v
            |    |-- e203_core.v
            |         |-- e203_exu.v  (contains NICE interface ports)
            |
            |-- e203_subsys_nice_core.v  (NICE wrapper, conditionally compiled)
                 |-- cnn_nice_core.v     (the CNN accelerator)
                      |-- pe_array.v
                           |-- pe.v (x16)
```

The NICE interface is activated by defining `E203_HAS_NICE` in the E203 configuration. When this macro is not defined, the `e203_subsys_nice_core` module is not instantiated, and the accelerator is absent from the system.

### 3.4.2 NICE Signal Connections

The `e203_subsys_nice_core` wrapper maps the E203 core's NICE port signals to the accelerator's ports. Listing 3.5 shows the wrapper instantiation.

```verilog
// Listing 3.5: NICE subsystem wrapper instantiation (e203_subsys_nice_core.v).

module e203_subsys_nice_core (
    input                         nice_clk,
    input                         nice_rst_n,
    output                        nice_active,
    output                        nice_mem_holdup,
    input                         nice_req_valid,
    output                        nice_req_ready,
    input  [`E203_XLEN-1:0]       nice_req_inst,
    input  [`E203_XLEN-1:0]       nice_req_rs1,
    input  [`E203_XLEN-1:0]       nice_req_rs2,
    output                        nice_rsp_valid,
    input                         nice_rsp_ready,
    output [`E203_XLEN-1:0]       nice_rsp_rdat,
    output                        nice_rsp_err,
    // ... memory channel signals (unused) ...
);

    cnn_nice_core u_cnn_nice_core (
        .clk(nice_clk),
        .rst_n(nice_rst_n),
        .nice_req_valid(nice_req_valid),
        .nice_req_ready(nice_req_ready),
        .nice_req_instr(nice_req_inst),
        .nice_req_rs1(nice_req_rs1),
        .nice_req_rs2(nice_req_rs2),
        .nice_rsp_valid(nice_rsp_valid),
        .nice_rsp_ready(nice_rsp_ready),
        .nice_rsp_rdat(nice_rsp_rdat),
        .nice_rsp_err(nice_rsp_err),
        // Memory channel ports tied to 0/unused
    );
endmodule
```

The accelerator explicitly disables the NICE memory channels (`nice_mem_holdup` is tied to 0 and `nice_icb_cmd_valid` is tied to 0), as all data transfer occurs through register operands.

### 3.4.3 Memory Subsystem

The processor boots from a 32-bit MROM containing a single jump instruction that redirects execution to the ITCM base address (0x8000_0000). The ITCM is 64 bits wide and 16K entries deep (128 KB), connected to the processor through the instruction fetch unit. The DTCM is 32 bits wide and 16K entries deep (64 KB), connected through the load-store unit.

The ITCM and DTCM are initialized with Verilog hex files during FPGA bitstream generation. These hex files are produced by compiling a bare-metal C program, linking it to the appropriate memory regions, and converting the ELF binary to the text-format hex representation expected by `$readmemh`. A critical implementation detail is that the hex file format must match the memory word width: ITCM (64-bit) requires 16 hex digits per line, while DTCM (32-bit) requires 8 hex digits per line.

### 3.4.4 Peripheral Connections

The SoC provides UART0 (connected to GPIO16 for RX and GPIO17 for TX at 115200 baud) as the primary debug output channel. The GPIO, CLINT, and PLIC peripherals are connected through the system bus fabric. The UART is initialized during the early boot sequence to enable printf-style debug messages. The GPIO module provides additional I/O capabilities, including the UART pin configuration.

---

## 3.5 FPGA Bring-up Methodology

### 3.5.1 Build Flow

The FPGA bitstream construction follows a two-stage build process. In the first stage, the bare-metal software program is compiled using the RISC-V GNU toolchain and converted to Verilog hex format for ITCM/DTCM initialization. In the second stage, Vivado synthesizes, places, and routes the RTL design with the memory contents pre-loaded from the hex files.

Figure 3.6 shows the complete build pipeline.

```
  C Source (.c / .S)          RTL Source (.v)
        |                           |
        v                           v
  RISC-V GCC                    Vivado
  (Compile + Link)              (Synthesis)
        |                           |
        v                           v
  ELF Binary                    Netlist
        |                           |
        v                           v
  objcopy                        Place & Route
  (Bin to Verilog Hex)           (with ILA cores)
        |                           |
        v                           v
  ITCM/DTCM Hex Files            Bitstream (.bit)
        |                           |
        +-----------> Merge <-------+
                          |
                          v
                   FPGA Configuration
```

**Figure 3.6:** FPGA build pipeline from software compilation and RTL synthesis to bitstream generation.

Several build modes are defined to support different validation scenarios:

- **bare_metal:** Minimal system without ILA probes, for final deployment.
- **bootvec_sysclk_ila:** Includes ILA probes for CPU boot-chain debugging.
- **hello_sysclk_ila:** Includes ILA probes and the hello_e203 test program.
- **cnn_sysclk_ila:** Includes ILA probes and the NICE accelerator test program.

Each build mode selects the appropriate top-level Verilog wrapper, ILA configuration, and memory initialization files through a PowerShell-based build script.

### 3.5.2 ILA Probe Design

The Integrated Logic Analyzer (ILA) is the primary on-chip debugging instrument. Seven probes, totaling 110 bits, are configured to capture key internal signals of the processor and accelerator:

**Table 3.6:** ILA probe configuration.

| Probe   | Width | Signal Monitored              | Debug Purpose                          |
|---------|-------|-------------------------------|----------------------------------------|
| probe0  | 32    | Program counter (PC)          | CPU execution trace                    |
| probe1  | 4     | Reset and clock status        | Verify clock tree and reset deassertion|
| probe2  | 3     | System memory bus activity    | Detect bus transactions                |
| probe3  | 32    | Memory command address        | Identify which memory region is accessed|
| probe4  | 32    | Memory handshake counters     | Quantify bus utilization               |
| probe5  | 4     | UART TX state                 | Confirm UART transmission progress     |
| probe6  | 3     | Debug/trap/stop flags         | Detect processor exceptions            |

The ILA core is instantiated in a dedicated top-level wrapper module rather than being inserted post-synthesis via the Vivado GUI. This approach ensures that the probe signals are explicitly declared at the RTL level and survive synthesis without manual intervention. The trigger condition is configured to capture on the rising edge of the system clock, with a sample depth of 1024 cycles.

### 3.5.3 Verification Strategy: Simulation-to-Hardware

The verification strategy employs a dual-track approach where RTL simulation and FPGA testing complement each other.

**Simulation track (Icarus Verilog):** The RTL design is verified with Icarus Verilog before any FPGA synthesis. The simulation testbench instantiates the SoC top module and drives the system clock and reset signals. A mock CPU testbench (tb_cpu_mock) provides standalone verification of the `cnn_nice_core` without requiring the full E203 processor, enabling faster iterations during accelerator development.

The simulation validates:
1. Normal path: CLEAR, four WLOADs, four DLOADs, COMP, RSTAT --- the expected result is 320 for a known test vector.
2. Error paths: COMP before loading all data, RSTAT before COMP.
3. Boundary conditions: Negative INT8 values (-128, -1), maximum positive values (127).
4. Reset behavior: Accumulators cleared after reset.

**FPGA track (Vivado):** After simulation passes, the design is synthesized for the Davinci Pro A7-100T FPGA (Artix-7 xc7a100t). The bring-up proceeds in stages:

1. **Clock and reset verification:** ILA captures clock activity and reset deassertion timing.
2. **Boot chain validation:** Processor PC is observed transitioning from MROM (0x0000_0000) to ITCM (0x8000_0000+), confirming correct boot vector execution.
3. **UART output check:** The hello_e203 program sends three lines of output ("hello_e203: boot", "hello_e203: uart ok", "hello_e203: loop") at 115200 baud.
4. **NICE instruction execution:** The test_nice assembly program exercises all six custom instructions. ILA captures verify that the CPU pipeline completes each NICE instruction and reaches the program completion point.

The simulation-to-hardware bridge proved critical for root-cause analysis. When the FPGA failed to boot, the exact same failing behavior was reproduced in simulation, which provided full signal visibility. The root causes---memory hex file formatting mismatch, missing Verilog macro definitions, and incorrect ILA probe placement---were all identified and fixed in simulation before rebuilding the FPGA bitstream.

### 3.5.4 Debugging Methodology

The debugging methodology follows a systematic isolation approach:

1. **Observe:** ILA captures the PC trace and key handshake signals.
2. **Compare:** The PC trace is compared against the disassembly listing of the compiled program to identify divergence points.
3. **Isolate:** Simulation reproduces the identical scenario with full waveform visibility, enabling probe of any internal signal.
4. **Fix:** The root cause is corrected in RTL, software, or build scripts.
5. **Verify:** Simulation passes the test case, and a new bitstream is built for FPGA confirmation.

This cycle typically requires 10--15 minutes per FPGA iteration (synthesis, place-and-route, bitstream generation) versus seconds for simulation. The simulation-first approach therefore maximizes engineering productivity by catching issues before the expensive FPGA build step.
