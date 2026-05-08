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
- `build.sh` expects Bash. On the current PowerShell environment, use direct commands or run from a shell that provides `bash`.
- `FYP_FINAL.docx` should still be regenerated after each future thesis source change.
- PPT needs a real PowerPoint visual pass before submission because the automated preview does not guarantee PowerPoint text/layout parity.
- The working tree already contained uncommitted figure/script/document changes before this takeover. Do not revert them without explicit instruction.

## Immediate Next Work

1. Fill title page metadata once proposal code, supervisor, and assessor names are confirmed.
2. Open the PPTX in PowerPoint and do a human visual pass on the actual deck.
3. Decide whether the final defense deck should remain minimal or receive a second visual-design pass with larger figures.
4. Commit or archive the generated deliverables once the title metadata is confirmed.
