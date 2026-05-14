# Graduation Design Library

This repository is the Windows-side master library for the final year project:

**Lightweight CNN Accelerator Based on RISC-V Custom Instructions**

It stores final deliverables, thesis sources, defense materials, experiment evidence, requirement documents, and project management notes. The implementation code repositories remain outside this library under `C:\Users\16084\Documents\New project`.

## Current Final Baseline

Use `14_final_submit/v2` as the authoritative final hand-in package.

| Purpose | Path |
| --- | --- |
| Thesis submission baseline | `14_final_submit/v2/thesis/FYP_Thesis_Final_v2_SUBMISSION_BASELINE.docx` |
| Thesis PDF reference | `14_final_submit/v2/thesis/main_final_SUBMISSION_REFERENCE.pdf` |
| Thesis LaTeX source archive | `14_final_submit/v2/thesis_latex_source/` |
| Final defense PPT baseline | `14_final_submit/v2/presentation/FYP_Final_Defense_English_Draft_REPORT_BASELINE.pptx` |
| Final defense script | `14_final_submit/v2/presentation/Final_Defense_Bilingual_Script.docx` |
| Final defense QA | `14_final_submit/v2/presentation/Final_Defense_QA_Bilingual.docx` |
| Baseline checksum manifest | `14_final_submit/v2/BASELINE_MANIFEST.txt` |

Git tag for the complete archive:

`fyp-final-v2-complete-archive-2026-05-14`

## Traceability

| Question | Start Here |
| --- | --- |
| How did the design evolve? | `00_Index/DESIGN_ITERATION_HISTORY.md` |
| How are versions and baselines managed? | `00_Index/VERSION_MANAGEMENT.md` |
| Which source-code commits are active? | `02_Source_Repos/CURRENT_BASELINES.md` |
| Which evidence supports thesis/PPT claims? | `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md` |
| Which files are in the final package? | `14_final_submit/v2/BASELINE_MANIFEST.txt` |

## Folder Map

| Folder | Role |
| --- | --- |
| `00_Index` | Navigation and usage rules |
| `01_Project_Overview` | High-level project overview notes |
| `02_Source_Repos` | External source repository baselines and workspace policy |
| `03_Documents` | Administrative documents, process materials, and weekly reports |
| `04_Experiments` | RTL/full-SoC/board evidence, logs, and verification records |
| `05_Presentation` | Working and historical presentation assets |
| `06_References` | Reference index and bibliography-related notes |
| `07_Backups` | Older working snapshots kept for traceability |
| `08_Todo_And_Notes` | Planning notes and archived task boards |
| `10_Final_Defense` | Final defense preparation workspace |
| `11_FYP_requirement` | CityUHK FYP requirements and extracted text |
| `12_SCUT_requirement` | SCUT process requirements and forms |
| `13_thesis_bak` | Historical thesis backup snapshot |
| `14_final_submit` | Final submission packages and locked baselines |
| `thesis_latex` | Active LaTeX thesis source tree |
| `scripts`, `tools` | Local maintenance and generation helpers |
| `_archive` | Old material retained for audit trail |

## GitHub Upload Rule

Most large file types are ignored by default. Final deliverables under `14_final_submit/v2` and key assets under `05_Presentation/Final` are explicitly allowed and must remain tracked.

Before pushing, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_github_upload.ps1
```

Then check:

```powershell
git status --short
git log --oneline -5
```

Do not remove or rewrite the `14_final_submit/v2` package unless intentionally creating a new final baseline.
