# Version Management

This project uses three layers of version tracking:

1. Git commits for ordinary changes.
2. Git tags for locked baselines.
3. Directory-level final packages for submission artifacts.

## Baseline Types

| Type | Naming | Use |
| --- | --- | --- |
| Working commit | normal commit message | Daily document, evidence, script, and organization changes |
| Engineering source baseline | recorded in `02_Source_Repos/CURRENT_BASELINES.md` | Links this library to `riscv_cnn_accelerator` and `e203_hbirdv2` commits |
| Submission baseline | `fyp-final-*` tag | Immutable final hand-in state |
| Final package | `14_final_submit/vN` | Human-readable copy of files to submit or defend from |

## Current Tags

| Tag | Meaning |
| --- | --- |
| `v2.0.0` | Initial graduation design library baseline |
| `v2.1.0` | Board photo, UART screenshot, diagrams, and limitation update |
| `fyp-final-submission-baseline-2026-05-14` | First final-progress freeze |
| `fyp-final-v2-submission-and-defense-baseline-2026-05-14` | finalv2 thesis and latest defense PPT baseline |
| `fyp-final-v2-complete-archive-2026-05-14` | Complete final archive including `thesis_latex` source |

## Commit Message Convention

Use these prefixes:

- `docs:` for README, index, explanation, and traceability updates.
- `thesis:` for thesis text, figures, bibliography, PDF/DOCX build changes.
- `defense:` for PPT, script, QA, and final-defense evidence changes.
- `evidence:` for experiment logs, board captures, screenshots, and verification records.
- `chore:` for cleanup, file movement, upload checks, and Git housekeeping.
- `fix:` for factual corrections or broken references.

## Creating A New Final Baseline

1. Create a new folder such as `14_final_submit/v3`.
2. Copy final thesis, presentation, source snapshot, scripts, and QA into that folder.
3. Generate or update `BASELINE_MANIFEST.txt`.
4. Update:
   - `README.md`
   - `00_Index/README.md`
   - `00_Index/DESIGN_ITERATION_HISTORY.md`
   - `02_Source_Repos/CURRENT_BASELINES.md` if source-code commits changed
   - `10_Final_Defense/Evidence_Package/EVIDENCE_INDEX.md` if claims changed
5. Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_github_upload.ps1 -BaselineDir "14_final_submit\v3"
```

6. Commit with a clear message.
7. Tag the commit:

```powershell
git tag -a fyp-final-v3-complete-archive-YYYY-MM-DD -m "FYP final v3 complete archive"
git push origin codex/fyp-final-closure
git push origin fyp-final-v3-complete-archive-YYYY-MM-DD
```

## Rules For Maintainability

- Keep final packages append-only.
- Never replace a final tag unless intentionally correcting a failed local-only tag before publishing.
- Keep raw evidence in `04_Experiments`.
- Keep report-ready defense material in `10_Final_Defense` and locked copies in `14_final_submit`.
- Keep old material in `_archive` or `Archive` directories instead of deleting it when it explains a decision.
- Use `BASELINE_MANIFEST.txt` to verify large binary deliverables.
