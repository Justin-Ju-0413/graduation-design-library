# Design Iteration History

This file is the traceability map for the graduation project. It explains how the design evolved, where each milestone is recorded, and which files should be used to understand or reproduce the final result.

## Current Final State

- Library branch: `codex/fyp-final-closure`
- Current library commit: `6028b48`
- Complete final archive tag: `fyp-final-v2-complete-archive-2026-05-14`
- Final package: `14_final_submit/v2`
- Thesis source snapshot: `14_final_submit/v2/thesis_latex_source`
- Active source repositories:
  - `riscv_cnn_accelerator`: `codex/a7-bringup-v2-main`
  - `e203_hbirdv2`: `codex/a7-bringup-v2-soc`
- Final engineering truth: RTL, full-SoC simulation, hello_e203 board validation, CNN/NICE board validation, and NICE rs2 bug-fix board verification are recorded with evidence.

## Version Timeline

| Stage | Date | Library Ref | Design Meaning | Evidence / Files |
| --- | --- | --- | --- | --- |
| Initial library baseline | 2026-05-06 | `v2.0.0`, `748d04a` | Created the graduation design library structure for the RISC-V CNN accelerator FPGA prototype. | `README.md`, `00_Index/`, early thesis and project structure |
| Board/figure expansion | 2026-05-06 | `v2.1.0`, `65c8ec4` | Added FPGA board photo, UART screenshot, AI-generated diagrams, and updated limitations. | `thesis_latex/figures/`, `_archive/09_Thesis_Writing_archived_20260507/` |
| Structure cleanup | 2026-05-07 | `cb5628e`, `11d1ff9` | Reorganized project folders, archived old work, and cleaned presentation/history layout. | `_archive/`, `05_Presentation/Archive/`, `07_Backups/` |
| Thesis figure quality pass | 2026-05-07 to 2026-05-08 | `a50e183`, `192042a`, `30b1958` | Fixed cross-references, unified PDF/DOCX figures, and improved ILA/PC trace readability. | `thesis_latex/figures/`, `thesis_latex/chapters/` |
| NICE rs2 bug discovery and verification | 2026-05-09 | `5af7bef`, `6694990`, `21c7a6d` | Recorded the rs2 index capture issue, the E203 decode fix, software hardening, and board verification evidence. | `02_Source_Repos/CURRENT_BASELINES.md`, `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/` |
| Final thesis and defense asset build | 2026-05-09 to 2026-05-11 | `d900d9c`, `f565333`, `52aad72` | Polished final figures, corrected resource data, reviewed thesis, and slimmed Git history. | `thesis_latex/`, `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md`, `DASHBOARD.html` |
| First final submission freeze | 2026-05-14 | `fyp-final-submission-baseline-2026-05-14`, `09ddc52` | Captured the working final defense and requirement material state. | `10_Final_Defense/`, `11_FYP_requirement/`, `tools/vision.js` |
| Final v2 thesis and defense baseline | 2026-05-14 | `fyp-final-v2-submission-and-defense-baseline-2026-05-14`, `ad85ff4` | Locked finalv2 thesis DOCX, thesis PDF reference, final defense PPT, script, and QA into `14_final_submit/v2`. | `14_final_submit/v2/README.md`, `14_final_submit/v2/BASELINE_MANIFEST.txt` |
| Complete final archive | 2026-05-14 | `fyp-final-v2-complete-archive-2026-05-14`, `043c6f0` | Added the complete `thesis_latex` source tree into the final v2 package for reproducibility. | `14_final_submit/v2/thesis_latex_source/` |
| File management and upload hardening | 2026-05-14 | `6028b48` | Cleaned empty folders, updated README/index files, added upload checks and binary Git attributes. | `README.md`, `.gitignore`, `.gitattributes`, `scripts/check_github_upload.ps1` |

## Engineering Iteration Chain

| Engineering Step | What Changed | Current Evidence |
| --- | --- | --- |
| RTL/NICE unit behavior | Verified custom instruction behavior before full SoC integration. | `04_Experiments/RTL_Simulation/2026-04-23_baseline_rerun/rtl_sim_results.txt` |
| Full-SoC SDK simulation | Verified software-driven E203/NICE integration in simulation. | `04_Experiments/FullSoC_Simulation/2026-04-23_baseline_rerun/fullsoc_sim_results.txt` |
| Board clock/JTAG/ILA bring-up | Isolated board clock, reset, and ILA capture behavior. | `04_Experiments/Board_BringUp/2026-04-28_board_connection_check/` |
| hello_e203 board validation | Closed boot-chain and UART validation before CNN/NICE tests. | `04_Experiments/Board_BringUp/2026-04-28_board_connection_check/hello_e203_board_artifacts/` |
| CNN/NICE board validation | Verified CNN v1 software/hardware result match and speedup. | `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/uart_output.txt` |
| NICE rs2 fix | Fixed E203 decoder behavior for NICE rs2 index capture and added software defense. | `02_Source_Repos/CURRENT_BASELINES.md`, `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/BOARD_VERIFICATION.md` |
| LeNet-5 final demonstration | Recorded final board-level LeNet-5 accuracy and explanation for thesis/defense. | `thesis_latex/chapters/04_4_results.tex`, `10_Final_Defense/QA/Final_Defense_QA_Bilingual.md` |

## Artifact Lineage

| Artifact | Working Source | Locked Final Copy |
| --- | --- | --- |
| Thesis source | `thesis_latex/` | `14_final_submit/v2/thesis_latex_source/` |
| Thesis DOCX | `_archive/09_Thesis_Writing_archived_20260507/FYP_Thesis_Final_v2.docx` and `thesis_latex/FYP_FINAL.docx` history | `14_final_submit/v2/thesis/FYP_Thesis_Final_v2_SUBMISSION_BASELINE.docx` |
| Thesis PDF reference | `14_final_submit/main_final.pdf` | `14_final_submit/v2/thesis/main_final_SUBMISSION_REFERENCE.pdf` |
| Defense PPT | `05_Presentation/Final/FYP_Final_Defense_English_Draft.pptx` | `14_final_submit/v2/presentation/FYP_Final_Defense_English_Draft_REPORT_BASELINE.pptx` |
| Defense script | `10_Final_Defense/Final_10min_EN/Final_Defense_Bilingual_Script.docx` | `14_final_submit/v2/presentation/Final_Defense_Bilingual_Script.docx` |
| Defense QA | `10_Final_Defense/QA/Final_Defense_QA_Bilingual.docx` | `14_final_submit/v2/presentation/Final_Defense_QA_Bilingual.docx` |
| Evidence index | `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md` | Referenced by final package and README |

## How To Read The History

1. Start with `README.md` for the current final package.
2. Use this file to understand the design timeline.
3. Use `02_Source_Repos/CURRENT_BASELINES.md` to map library milestones to source-code commits.
4. Use `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md` to verify every thesis/defense claim.
5. Use Git tags for immutable baselines and Git commits for incremental changes.

## Maintenance Rule

- Do not rewrite or delete existing final tags.
- If a new design baseline is created, add a new row to `Version Timeline`.
- If a source-code baseline changes, update `02_Source_Repos/CURRENT_BASELINES.md`.
- If a thesis or PPT claim changes, update `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md`.
- If a final deliverable changes, create a new folder under `14_final_submit/` instead of modifying `14_final_submit/v2` in place.
