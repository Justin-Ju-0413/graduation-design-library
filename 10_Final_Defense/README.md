# Final Defense Center

This folder is the main workspace for the final graduation defense.

The locked final defense baseline is stored in:

- `../14_final_submit/v2/presentation/FYP_Final_Defense_English_Draft_REPORT_BASELINE.pptx`
- `../14_final_submit/v2/presentation/Final_Defense_Bilingual_Script.docx`
- `../14_final_submit/v2/presentation/Final_Defense_QA_Bilingual.docx`

## Defense Story

The final defense should use one consistent story:

I built and verified a lightweight CNN accelerator integrated with the RISC-V E203 soft-core through the NICE custom instruction interface. The RTL and full-SoC simulation paths are closed, and the final package preserves the board-level evidence and defense materials used for submission.

## Main Slide Structure

1. Project background and motivation
2. Research goal and scope
3. System architecture
4. NICE custom instruction path
5. CNN accelerator RTL design
6. RTL simulation and verification evidence
7. Full-SoC SDK integration
8. Full-SoC simulation evidence
9. FPGA bring-up environment
10. Current soft-core debug blocker
11. Summary of completed work
12. Future work and closing

## Required Evidence

- RTL regression screenshot: `[TB_PASS]`
- Full-SoC screenshot: `expected_rstat=19` and `[PHASE4_PASS]`
- Branch and commit baseline
- Architecture diagram
- NICE instruction path diagram
- Board/debug environment screenshot if available

## Defense Preparation Rule

- Say what is completed.
- Say what is still open.
- Keep the board-level debug status honest.
- Use the same technical wording as the thesis.

