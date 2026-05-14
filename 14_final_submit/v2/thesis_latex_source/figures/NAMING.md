# Figure Asset Naming

Official thesis figures use:

```text
fig<chapter>_<sequence>_<short_slug>.<ext>
```

Examples:

- `fig3_1_soc_architecture.png`
- `fig4_4_uart_cnn_v1.png`
- `fig4_5_uart_lenet5.png`

Rules:

- Keep official thesis assets in `thesis_latex/figures/`.
- Keep QA renders and contact sheets in `thesis_latex/.build/figure_qa/` or `thesis_latex/qa_preview/`.
- Keep raw experimental screenshots/log-derived evidence in `04_Experiments/` with ASCII descriptive names.
- Move duplicate or superseded material to `_archive/duplicate_assets_YYYYMMDD/` instead of deleting it.
- Do not use short ambiguous names such as `3.1.svg`, Chinese screenshot names, or compatibility aliases such as `fig_uart_output.png` for active thesis figures.
