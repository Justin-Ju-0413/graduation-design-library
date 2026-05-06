import csv
from pathlib import Path
csv_path = Path(r'C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\soc_bootdiag_sysclk_ila_ila_capture\ila_capture.csv')
with csv_path.open(newline='') as f:
    rows = list(csv.DictReader(f))
rows = [r for r in rows if r['Sample in Buffer'].isdigit()]
cols = ['probe0_pc[31:0]', 'probe1_reset_uart[3:0]', 'probe2_liveness[2:0]', 'probe3_pc_activity[31:0]', 'probe4_nice_csr[31:0]', 'probe5_nice_hs[3:0]', 'probe6_mem_status[2:0]']
print(f'samples={len(rows)}')
for c in cols:
    vals=[]
    for r in rows:
        v=r[c]
        if v not in vals:
            vals.append(v)
    print(f'{c}: unique_count={len(vals)} first_values={", ".join(vals[:16])}')
first=rows[0]
last=rows[-1]
print('first=' + ', '.join(f'{c}={first[c]}' for c in cols))
print('last=' + ', '.join(f'{c}={last[c]}' for c in cols))
# Decode first and last fields
for label, r in [('first', first), ('last', last)]:
    reset=int(r['probe1_reset_uart[3:0]'],16)
    live=int(r['probe2_liveness[2:0]'],16)
    ifu=int(r['probe4_nice_csr[31:0]'],16)
    uart=int(r['probe5_nice_hs[3:0]'],16)
    status=int(r['probe6_mem_status[2:0]'],16)
    print(f'{label}_decoded reset_uart sys_rst_n={(reset>>3)&1} mmcm_locked={(reset>>2)&1} reset_periph={(reset>>1)&1} uart_txd={reset&1}')
    print(f'{label}_decoded liveness ifu_req_seen={(live>>2)&1} ifu_rsp_seen={(live>>1)&1} trap_or_halt={live&1}')
    print(f'{label}_decoded ifu_req_count={(ifu>>16)&0xffff} ifu_rsp_count={ifu&0xffff}')
    print(f'{label}_decoded uart edge_seen={(uart>>3)&1} uart_txd_sync={(uart>>2)&1} gpio17_oe={(uart>>1)&1} gpio17_oval={uart&1}')
    print(f'{label}_decoded status reset_released={(status>>2)&1} core_cgstop={(status>>1)&1} dbg_halt={status&1}')
