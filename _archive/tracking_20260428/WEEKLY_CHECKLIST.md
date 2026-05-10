# Weekly Checklist To Final Defense

## Active Ten-Day Closure Checkpoints

Track the current ten-day task book:

- `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`

Daily checkpoints:

- Day 1: freeze `soc_sysclk_ila` interpretation and `probe_pc` conclusion.
- Day 2: build CPU boot diagnostic ILA and classify CPU state.
- Day 3: build minimal `hello_e203` image and bitstream.
- Day 4: validate `hello_e203` on board with UART/ILA evidence.
- Day 5: start CNN/NICE board validation or close the hello blocker.
- Day 6: close CNN/NICE runtime evidence or package full-SoC fallback.
- Day 7: close CPU-only vs accelerator performance and 10x wording.
- Day 8: close INT8/model accuracy scope and MNIST/LeNet-5 boundary.
- Day 9: synchronize thesis chapters, figures, and evidence index.
- Day 10: prepare final defense PPT line, notes, QA, and evidence package.

Daily closeout requirement:

- Update the current day block in `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`.
- Archive command, bit/ltx, timing report, ILA summary, CSV, UART note, conclusion, and next action for every board run.

## Week of 2026-04-28

- Freeze current status.
- Confirm branch and commit baseline.
- Prepare hello_e203 plan.
- Prepare current evidence index.
- Start thesis outline and references.
- Follow the active five-day board bring-up plan:
  - Day 1: freeze `soc_sysclk_ila` interpretation and clarify PC/UART signals.
  - Day 2: build CPU boot diagnostic ILA and classify CPU state.

Done when:

- current status can be explained in one minute
- all open board tasks are listed honestly
- Day 1 and Day 2 status blocks are updated in `FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`
- Day 1 and Day 2 status blocks are mirrored in `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`

## Week of 2026-05-01

- Build and test `hello_e203`.
- Generate hello bitstream.
- Collect UART/LED/ILA evidence if board access is available.
- Draft thesis Introduction and Related Work.
- Continue the active five-day board bring-up plan:
  - Day 3: build the minimal `hello_e203` board image.
  - Day 4: validate `hello_e203` on board with UART and ILA evidence.
  - Day 5: start CNN/NICE board validation or write the hello blocker report.
- At each day closeout, archive command, bit/ltx, timing report, ILA summary, CSV, UART note, conclusion, and next action.

Done when:

- either hello board evidence is collected or the exact blocker is recorded
- Chapter 1 and Chapter 2 notes exist
- Day 3 through Day 5 status blocks are updated in `FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`
- Day 3 through Day 5 status blocks are mirrored in `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`

## Week of 2026-05-06

- Run `cnn_accel_demo` board attempt.
- Collect UART software/hardware comparison.
- Capture cycle count and speedup.
- Draft Architecture, RTL, and full-SoC chapters.
- Complete Day 6 through Day 8 from `TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`.

Done when:

- CNN board evidence exists or the exact failing step is known
- thesis technical chapters have first drafts
- performance and accuracy/model-scope wording is evidence-backed

## Week of 2026-05-12

- Finish thesis draft.
- Prepare final PPT.
- Prepare evidence package.
- Prepare QA.
- Complete any remaining Day 9 or Day 10 closure outputs.

Done when:

- final PPT has all key evidence pages
- thesis draft is ready for review

## Week of 2026-05-19

- Revise thesis and PPT.
- Rehearse final defense.
- Prepare short version and emergency backup answers.

Done when:

- 8 to 12 minute presentation is stable
- Q&A can be answered without searching files
