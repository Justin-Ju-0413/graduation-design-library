---
name: day-closeout
description: Use when the user finishes a day's work and needs to update the daily status across all tracking files. Trigger phrases: "close out today", "day closeout", "update day status", "end of day", "update task book", "今日收尾", "更新状态", "close the day".
version: 1.0.0
---

# Day Closeout

Updates the daily status across all project tracking files after a day's engineering work.

## Files to Update

### 1. Ten-Day Closure Task Book
`C:\Users\16084\Documents\Graduation_Design_Library\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\TEN_DAY_CLOSURE_TASK_BOOK_2026_04_29.md`

Update the relevant day block:
```text
Status: TODO / IN_PROGRESS / DONE / BLOCKED
Date:
Main output:
Evidence path:
Decision:
Next action:
```

### 2. Five-Day Board Bring-Up Plan
`C:\Users\16084\Documents\Graduation_Design_Library\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\FIVE_DAY_BOARD_BRINGUP_PLAN_2026_04_29.md`

Update the same day block with mirror content.

### 3. Weekly Checklist
`C:\Users\16084\Documents\Graduation_Design_Library\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\WEEKLY_CHECKLIST.md`

Check off completed items if applicable.

### 4. Day Summary Note (if not already written)
Create or update at:
`C:\Users\16084\Documents\Graduation_Design_Library\08_Todo_And_Notes\2026-04-28_To_Final_Defense_Plan\DAY{N}_{DESCRIPTION}_{YYYY_MM_DD}.md`

### 5. Evidence Index (if board work was done)
Update source repo baselines if new commits were made:
`C:\Users\16084\Documents\Graduation_Design_Library\02_Source_Repos\CURRENT_BASELINES.md`
`C:\Users\16084\Documents\Graduation_Design_Library\02_Source_Repos\LOCAL_REPO_STATUS.md`

## Status Block Template

```text
Status: DONE
Date: {today}
Main output: {one-line summary}
Evidence path: {relative path from Library root}
Decision: {key decision made}
Next action: {concrete next step}
```

## Rules
- Only update the current day's block, never past or future days
- If work spans multiple days, only update the day that was worked on
- Mirror the same status in both the ten-day and five-day plans
- If a blocker was found, mark BLOCKED with clear evidence and next hypothesis
- If early finish, note readiness for next day but don't pre-update future blocks
