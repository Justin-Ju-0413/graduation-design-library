# Windows Workspace Policy

This file defines how the graduation project should be maintained from now on.

## Core Rule

Windows is the only long-term work center.

- `Graduation_Design_Library` is the master document and presentation center.
- `New project` is the live code workspace.
- Ubuntu is only for development execution, simulation, and board-side tasks.

## What Belongs Where

### Graduation_Design_Library

Use this library for:

- final PPT files
- report scripts
- explanations and QA
- screenshots and archived evidence
- repo baseline notes and project-level summaries

### New project

Use this workspace for:

- source code
- repo-tracked project docs that truly belong to the codebase
- helper tools under `$archive\tools`

Do not keep final presentation deliverables here.

## Repo Hygiene Rule

- Keep both repos on the active baselines.
- Avoid mixing presentation-only files into the repo working tree.
- If presentation material is generated from repo content, keep the final artifact in the library and archive the intermediate copy.

## Sync Rule

- New evidence collected on Ubuntu should be copied back into the Windows library.
- New code changes should be made in the repos, not inside the library.
- New report-ready summaries should be stored in the library, not scattered across repo subfolders.
