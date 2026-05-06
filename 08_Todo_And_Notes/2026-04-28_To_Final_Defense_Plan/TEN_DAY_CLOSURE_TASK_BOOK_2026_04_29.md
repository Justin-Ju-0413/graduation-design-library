# Ten-Day Closure Task Book

This is the active internal execution task book for closing the graduation project into a defensible minimum final result within ten days.

## Current Baseline

- Date started: 2026-04-29
- Main repo:
  - `riscv_cnn_accelerator`
  - branch `codex/a7-bringup-v2-main`
  - commit `5a76bc7a489759cf650fc050af6d2ca97acbd551`
- SoC repo:
  - `e203_hbirdv2`
  - branch `codex/a7-bringup-v2-soc`
  - commit `3e2f14d4f312903bb1e248ba724403ef8f73ccad`
- Closed evidence:
  - RTL/NICE local regression passed.
  - full-SoC SDK simulation passed with `expected_rstat=19`.
  - Davinci A7 JTAG, programming, UART device visibility, MMCM/reset, and raw `sys_clk` ILA upload are proven.
  - `soc_sysclk_ila` full SoC raw-debug capture passed with reset released and PC/activity/bus probes visible.
  - `probe_pc` is confirmed as IFU inspect PC, not commit PC.
- Active evidence root:
  - `04_Experiments\Board_BringUp\2026-04-28_board_connection_check`

## Ten-Day Final Closure Goal

The final ten-day closure chain is:

`hello_e203 board evidence -> CNN/NICE board or full-SoC fallback evidence -> explainable performance/accuracy metrics -> thesis and defense package`

The preferred result is a board-level `hello_e203` run and a board-level `cnn_accel_demo` run. If board UART or full CNN board execution remains blocked, the acceptable defense closure is a precise board blocker plus reproducible raw-debug/full-SoC evidence that does not overstate the result.

## Daily Tracking Format

Update only the current day block after work is completed or blocked.

```text
Status: TODO / IN_PROGRESS / DONE / BLOCKED
Date:
Main output:
Evidence path:
Decision:
Next action:
```

## Operating Rules

- This task book is the default project entry until the ten-day closure is complete or the priority is explicitly changed.
- The existing five-day board bring-up plan remains the execution subplan for Days 1-5.
- If a day finishes early, continue with the first unfinished task from the next day.
- If a blocker appears, record the blocker, evidence, failed hypothesis, and next hypothesis before switching paths.
- Do not switch to CNN/NICE board validation until hello or an equivalent CPU boot diagnosis is closed.
- Do not claim board-level CNN success without UART, ILA, or other archived board evidence.

## Day 1: Freeze Full SoC Raw-Debug Interpretation

```text
Status: DONE
Date: 2026-04-29
Main output: `soc_sysclk_ila` signal interpretation and `probe_pc` wiring conclusion
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_sysclk_ila_ila_capture`; `08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY1_SOC_SYSCLK_ILA_SIGNAL_INTERPRETATION_2026_04_29.md`
Decision: `probe_pc` is IFU inspect PC, not commit PC; Day 2 must use explicit boot-diagnostic counters and sticky flags.
Next action: Build CPU boot diagnostic ILA.
```

Goal:

- Convert the successful `soc_sysclk_ila` capture into a reliable CPU-state interpretation.

Required output:

- Probe meaning table.
- PC wiring conclusion.
- Day 2 diagnostic probe list.

Acceptance:

- Current board evidence is explainable without overstating software execution.

## Day 2: Build CPU Boot Diagnostic ILA

```text
Status: DONE
Date: 2026-04-29
Main output: `soc_bootdiag_sysclk_ila` build, timing-clean bitstream, board program, and ILA capture
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_artifacts`; `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture`; `08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY2_CPU_BOOT_DIAGNOSTIC_ILA_2026_04_29.md`
Decision: Reset is released, MMCM is locked, raw `sys_clk` ILA upload is captured, no cgstop/debug halt is observed, UART TX stays idle high, direct IFU-to-ITCM counters are zero, and PC activity continues. Proceed to `hello_e203` with boot/preload/UART as the first diagnosis branch if output is silent.
Next action: Build minimal `hello_e203` image with explicit stage markers and raw `sys_clk` ILA observation.
```

Goal:

- Determine whether the CPU fetches instructions, traps, halts, stays in reset, or runs without UART output.

Tasks:

- Add or adjust raw `sys_clk` ILA probes for fetch/ITCM activity, PC-change count, reset release, trap/halt/cgstop flags, UART TX edges, and relevant GPIO/UART pin state.
- Keep default `soc` untouched; use a diagnostic build mode if RTL changes are needed.
- Build bitstream and confirm routed timing is clean.
- Program board and capture ILA CSV if timing is clean.

Required output:

- CPU boot diagnostic bitstream artifacts.
- Timing summary.
- ILA summary and CSV.
- One-line CPU state judgment.

Acceptance:

- ILA upload is `CAPTURED`.
- Evidence distinguishes reset blocked, no fetch, active fetch, trap, halt/cgstop, or UART-only failure.

Failure branch:

- If timing fails, constrain only diagnostic CDC or known clock-as-data paths.
- If ILA upload fails, rerun `heartbeat_mmcm_sysclk_ila` before changing CPU logic.

## Day 3: Build Minimal `hello_e203` Image

```text
Status: DONE
Date: 2026-04-29/30
Main output: hello_e203 image, bitstream, board runtime evidence (ILA: PC in ITCM, UART TX edges), three root causes fixed
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_e203_board_artifacts`; `08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY4_BOOT_DEBUG_FULL_ANALYSIS_2026_04_29.md`
Decision: Three root causes found and fixed: (1) sirv_gnrl_dffs.v #1 delay (sim), (2) ITCM hex byte format vs 64-bit BRAM (sim+board), (3) E203_FORCE_BOOTROM_BOOT not globally visible (board). Board ILA shows PC=0x800000a0+, UART TX edge detected, GPIO17 configured. Day 3 complete.
Next action: Day 4 - capture UART text output via serial terminal, archive complete evidence, commit code.
```

## Day 4: Validate `hello_e203` On Board

```text
Status: DONE
Date: 2026-04-30
Main output: hello_e203 UART output captured, complete evidence archived, code committed to GitHub
Evidence path: `04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_e203_board_artifacts`
Decision: Hello_e203 board validation complete. UART prints three milestone strings as expected. LED0 toggling. All three root causes fixed and committed. Ready for CNN/NICE.
Next action: Day 5 - build cnn_accel_demo, prepare NICE ILA probes, start CNN board validation.
```

Goal:

- Close the minimal board runtime loop.

Tasks:

- Program the hello bitstream.
- Capture UART output or a no-output record.
- Capture ILA CSV from the same run.
- Record LED or stage behavior if available.
- Classify whether the failure, if any, is CPU boot, UART routing, baud, preload, reset, halt, or trap.

Required output:

- `hello_e203_board_artifacts`
- `hello_e203_ila_capture`
- UART screenshot/log or no-output record.
- Board runtime conclusion.

Acceptance:

- Best case: UART prints hello or staged boot text.
- Minimum acceptable case: ILA proves the program reaches a known stage and explains why UART is not visible.

## Day 5: Start CNN/NICE Board Validation Or Close Hello Blocker

```text
Status: TODO
Date: 2026-05-03
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Move from hello evidence to CNN/NICE evidence, or write a precise hello blocker report.

Tasks if hello is successful:

- Build `cnn_accel_demo` image.
- Generate CNN bitstream with raw `sys_clk` ILA observation.
- Prepare probes for NICE CSR, NICE request/response, memory bus, and activity summary.
- Program and capture first CNN/NICE board evidence.

Tasks if hello is still blocked:

- Do not switch to CNN.
- Write blocker report with command history, evidence paths, failed hypotheses, and next hypothesis.

Acceptance:

- CNN/NICE board validation has started with first capture, or hello blocker is specific enough to continue without rediscovery.

## Day 6: Close CNN/NICE Runtime Evidence

```text
Status: TODO
Date: 2026-05-04
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Prove the CNN/NICE software path either on board or through a defensible fallback.

Tasks:

- Attempt board `cnn_accel_demo` UART and ILA capture if Day 5 permits.
- Compare software-visible result with expected `RSTAT` or demo result.
- Capture NICE handshake or CSR activity in ILA.
- If board execution remains blocked, rerun or package the full-SoC regression as fallback evidence.

Required output:

- CNN/NICE board artifacts and capture, or full-SoC fallback evidence package.
- Clear statement of whether the evidence is board-level or simulation-level.

Acceptance:

- A reproducible CNN/NICE result exists with matching expected output, or the exact missing board step is isolated.

## Day 7: Performance And 10x Metric Closure

```text
Status: TODO
Date: 2026-05-05
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Produce an honest CPU-only vs accelerator performance comparison.

Tasks:

- Gather CPU-only and accelerator cycle/time data from board, full-SoC simulation, or existing benchmark logs.
- Normalize the comparison at the same clock assumption.
- Build a table with workload, CPU cycles, accelerator cycles, speedup, and evidence source.
- If 10x is not proven, document the measured result and define what remains to meet the original target.

Required output:

- Performance comparison table.
- Evidence path for every number.
- Final statement for thesis/defense wording.

Acceptance:

- The 10x claim is either supported by evidence or replaced with a precise, defensible limitation statement.

## Day 8: Accuracy And Model-Scope Closure

```text
Status: TODO
Date: 2026-05-06
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Close the INT8/Python/C/RTL/full-SoC consistency story and clarify MNIST/LeNet-5 scope.

Tasks:

- Collect Python golden model, C model, RTL TB, and full-SoC result evidence.
- Identify whether current data supports full MNIST/LeNet-5 accuracy, subset accuracy, or only kernel-level correctness.
- Produce a table comparing original task requirement vs achieved evidence.
- Write the exact thesis wording for accuracy and model-scope boundaries.

Required output:

- Accuracy/model-scope note.
- Requirement-vs-evidence table.
- Final wording for paper and defense.

Acceptance:

- No final document can accidentally claim unproven MNIST/LeNet-5 accuracy.

## Day 9: Thesis And Evidence Synchronization

```text
Status: TODO
Date: 2026-05-07
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Synchronize engineering truth into thesis chapters and evidence index.

Tasks:

- Update thesis outline and technical chapter notes.
- Add figures/tables for architecture, NICE protocol, verification stack, board bring-up path, performance, and limitations.
- Link each claim to command, commit, report, waveform, CSV, screenshot, or board note.
- Update source repo baseline docs if new commits were created.

Required output:

- Thesis chapter update note.
- Evidence index.
- Claim-to-evidence mapping.

Acceptance:

- Thesis draft can be written from the evidence package without rediscovering project state.

## Day 10: Final Defense Package

```text
Status: TODO
Date: 2026-05-08
Main output:
Evidence path:
Decision:
Next action:
```

Goal:

- Prepare a final defense package that matches the real engineering evidence.

Tasks:

- Draft or update final PPT main line.
- Prepare per-slide speaker notes.
- Prepare QA on scope gaps: UART, board blocker, 10x, MNIST/LeNet-5, accuracy, and FPGA timing.
- Prepare evidence package index.
- Write final risk/limitation statement.

Required output:

- Final defense outline or deck draft.
- Speaker note draft.
- QA draft.
- Evidence package index.

Acceptance:

- The defense can explain completed work, remaining limits, and next steps without contradicting archived evidence.

## Evidence Archiving Rules

For every board-level run, archive:

- command used
- bitstream
- `.ltx`
- timing report
- route status if available
- ILA summary
- CSV or VCD
- UART screenshot/log or explicit no-output record
- conclusion and next action

For every software/simulation metric, archive:

- command used
- source commit
- log
- expected result
- observed result
- interpretation

## Final Deliverables Checklist

- Board bring-up evidence:
  - JTAG/programming proof
  - MMCM/reset proof
  - raw `sys_clk` ILA proof
  - full SoC raw-debug proof
  - hello board proof or blocker
  - CNN/NICE board proof or fallback
- CNN/NICE evidence:
  - local RTL regression
  - full-SoC regression
  - software result comparison
  - NICE handshake or CSR evidence
- Evaluation evidence:
  - performance table
  - accuracy/model-scope table
  - resource/timing table
- Writing and defense:
  - thesis chapter notes
  - final PPT outline/deck
  - speaker notes
  - QA
  - evidence index

## Closure Paths

Best closure:

- Board `hello_e203` works.
- Board `cnn_accel_demo` works.
- UART and ILA evidence exist.
- Performance and accuracy claims are evidence-backed.

Defensible closure:

- Board raw-debug proves CPU/SoC state.
- Hello or CNN board run is partially closed.
- full-SoC CNN/NICE regression backs functional claims.
- Limitations are explicit and evidence-backed.

Fallback closure:

- Board blocker is isolated and reproducible.
- RTL/NICE and full-SoC baselines are closed.
- Board clock/reset/JTAG/raw-debug evidence is closed.
- Thesis and defense state the boundary honestly.
