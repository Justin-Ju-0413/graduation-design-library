import csv
from pathlib import Path
p=Path(r'C:\Users\16084\Documents\Graduation_Design_Library\04_Experiments\Board_BringUp\2026-04-28_board_connection_check\hello_sysclk_ila_ila_capture\ila_capture.csv')
rows=list(csv.DictReader(p.open()))[1:]
print('samples', len(rows))
cols=['probe0_pc[31:0]','probe1_reset_uart[3:0]','probe2_liveness[2:0]','probe3_pc_activity[31:0]','probe4_nice_csr[31:0]','probe5_nice_hs[3:0]','probe6_mem_status[2:0]']
for c in cols:
    vals=[r[c] for r in rows]
    uniq=[]
    for v in vals:
        if v not in uniq: uniq.append(v)
    print(c, 'unique_count', len(set(vals)), 'first_values', ','.join(uniq[:16]))
print('first', {c:rows[0][c] for c in cols})
print('last', {c:rows[-1][c] for c in cols})

def bits(hexs,width):
    v=int(hexs,16)
    return [(v>>i)&1 for i in reversed(range(width))]
for label,row in [('first',rows[0]),('last',rows[-1])]:
    b=bits(row['probe1_reset_uart[3:0]'],4)
    print(label,'reset_uart sys_rst_n=%d mmcm_locked=%d reset_periph=%d uart_txd=%d'%tuple(b))
    b=bits(row['probe2_liveness[2:0]'],3)
    print(label,'liveness ifu_req_seen=%d ifu_rsp_seen=%d trap_or_halt=%d'%tuple(b))
    v=int(row['probe4_nice_csr[31:0]'],16)
    print(label,'ifu_req_count=%d ifu_rsp_count=%d'%(v>>16,v&0xffff))
    b=bits(row['probe5_nice_hs[3:0]'],4)
    print(label,'uart edge_seen=%d uart_txd_sync=%d gpio17_oe=%d gpio17_oval=%d'%tuple(b))
    b=bits(row['probe6_mem_status[2:0]'],3)
    print(label,'status reset_released=%d core_cgstop=%d dbg_halt=%d'%tuple(b))
