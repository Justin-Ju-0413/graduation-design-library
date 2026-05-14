import re
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[1] / "chapters"

WIDTHS = {
    "fig3_1_soc_architecture.png": "0.92",
    "fig3_2_instruction_format.png": "0.88",
    "fig3_2b_instruction_table.png": "0.90",
    "fig3_3_pe_microarchitecture.png": "0.72",
    "fig3_4_pe_array.png": "0.78",
    "fig3_5_packed_format.png": "0.82",
    "fig3_6_build_pipeline.png": "0.92",
    "fig3_7_verification_chain.png": "0.92",
    "fig4_1_fpga_board.jpg": "0.72",
    "fig4_2_ila_pc_trace.png": "0.95",
    "fig4_3_ila_nice_activity.png": "0.95",
    "fig4_4_uart_cnn_v1.png": "0.82",
    "fig4_5_uart_lenet5.png": "0.82",
    "fig4_6_speedup_bar.png": "0.85",
    "fig4_7_resource_fit.png": "0.82",
    "fig4_8_utilization_bar.png": "0.82",
    "fig4_9_timing.png": "0.88",
}

for tex_file in ["03_3_methodology.tex", "04_4_results.tex"]:
    path = CHAPTERS / tex_file
    text = path.read_text(encoding="utf-8")
    for fig_name, width in WIDTHS.items():
        pattern = re.compile(rf'\\\\includegraphics\[width=0\.\d+\\\\textwidth\]\{{figures/{re.escape(fig_name)}\}}')
        def repl(m):
            return f'\\\\includegraphics[width={width}\\textwidth]{{figures/{fig_name}}}'
        text = pattern.sub(repl, text)
    path.write_text(text, encoding="utf-8")
    print(f"Updated {tex_file}")
