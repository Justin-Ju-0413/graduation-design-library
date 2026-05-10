# 2026-05-09 Codex Takeover Status

## Scope

This file records the current working state after taking over the graduation design library on 2026-05-09.

## Active Project

- Topic: RISC-V custom-instruction based lightweight CNN accelerator with FPGA prototype validation.
- Main writing workspace: `thesis_latex/`.
- Engineering evidence workspace: `04_Experiments/`.
- Final defense workspace: `10_Final_Defense/` and `05_Presentation/`.
- Source repositories:
  - `C:\Users\16084\Documents\New project\riscv_cnn_accelerator`
  - `C:\Users\16084\Documents\New project\e203_hbirdv2`

## Current Technical Truth

- RTL/NICE validation: closed for the tested custom instruction paths.
- Full-SoC SDK simulation: closed for the recorded baseline.
- hello_e203 board validation: closed with UART and ILA evidence.
- CNN/NICE board validation: closed for the CNN v1 demo.
- Latest rs2 index capture fix:
  - `riscv_cnn_accelerator`: `ba847db4ecc6d696e55a5576e3e17164ac83cb97`
  - `e203_hbirdv2`: `1d609725740752b4d4de79a903574b94564538d1`
  - Board evidence: `04_Experiments/Board_BringUp/2026-05-09_nice_rs2_fix_verification/`
  - UART result: SW/HW/Expected all match, speedup 5.282x, `CNN v1 DEMO PASSED`.

## Thesis State

- Source: `thesis_latex/main.tex` plus `thesis_latex/chapters/*.tex`.
- Figures are managed through `thesis_latex/figures/MANIFEST.md`.
- PDF/DOCX builds were verified on Windows PowerShell using direct MiKTeX/Python/Pandoc commands because `bash` is not available in the current shell.
- Generated PDF: `thesis_latex/main_final.pdf`, 73 pages, generated on 2026-05-09 03:13.
- Generated DOCX: `thesis_latex/FYP_FINAL.docx`, regenerated on 2026-05-09 03:13.
- DOCX package check: 16 files under `word/media/`.
- Current LaTeX issues are non-blocking font warnings only: SimSun italic shape substitution and MiKTeX update notices. No overfull boxes, undefined citations, undefined references, or fatal build errors were observed in the latest log.

## Defense Deck State

- English draft deck: `05_Presentation/Final/FYP_Final_Defense_English_Draft.pptx`.
- Deck size: 11 slides with 11 speaker-note pages.
- Package QA: visible slide/notes XML has no Chinese text, no `board evidence pending`, and no slide-number placeholder.
- Preview contact sheet: `05_Presentation/Final/previews/contact_sheet.png`.
- Limitation: preview PNGs are lightweight script-generated approximations; no PowerPoint/LibreOffice parity render was available in this environment.

## Evidence Package State

- Evidence index: `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md`.
- All evidence paths listed in the index were checked as existing.
- CNN v1 UART source confirms: CPU 1516 cycles, accelerator 287 cycles, speedup 5.282x, SW/HW/Expected output `12 23 0 19`, and `CNN v1 DEMO PASSED`.

## Open Risks

- Title page placeholders still exist in `thesis_latex/main.tex`:
  - `[Proposal Code]`
  - `[Supervisor Name]`
  - `[Assessor Name]`
- PPT needs a real PowerPoint visual pass before submission.
- Plagiarism check not yet submitted.

## Completed Since Takeover (2026-05-10)

- Figure naming aligned: all fig4_X filenames match thesis numbering
- Table 4.6 resource data corrected to Vivado report values (LUTRAM 2843→219, FF 12807→12752, BRAM 36→35.5, BUFG 4→5)
- LeNet-5 board result (10/10 accuracy) added to Ch4 with PuTTY screenshot
- UART Y-axis fixed from float to integer ticks
- Dashboard updated: rstat_result, performance_data, accuracy_verify → done
- Workspace cleaned: ~300 temp/duplicate files deleted, old tracking plans archived
- 75-page PDF compiled, cross-references verified

## Remaining Before Submission (May 20)

1. Fill title page metadata (Proposal Code / Supervisor / Assessor).
2. PowerPoint visual pass on defense deck.
3. Plagiarism check + originality report.
4. QA preparation + rehearsal for oral defense.
5. Final `bash build.sh all` for PDF + DOCX.
