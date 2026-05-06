"""
Update references.bib with DOIs, URLs, and missing fields.
"""
import re
import os

BIB_PATH = r"C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\references.bib"

with open(BIB_PATH, 'r', encoding='utf-8') as f:
    bib = f.read()

# DOI and URL additions for each entry
updates = {
    'RISCV_UNPRIV_SPEC': '  url         = {https://riscv.org/technical/specifications/},\n  note        = {Document Version 20191213}',
    'RISCV_PRIV_SPEC': '  url         = {https://riscv.org/technical/specifications/},\n  note        = {Document Version 20211203}',
    'WATERMAN_PHD': '  url         = {https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-1.html}',
    'ASANOVIC_HOTCHIPS': '  doi         = {10.1109/HOTCHIPS.2014.7478802}',
    'RISCV_READER': '  publisher   = {Strawberry Canyon}',
    'NUCLEI_E203': '  url         = {https://github.com/riscv-mcu/e203_hbirdv2}',
    'NUCLEI_SDK': '  url         = {https://github.com/riscv-mcu/nuclei-sdk}',
    'NUCLEI_E203_DEBUG': '  url         = {https://doc.nucleisys.com/hbirdv2/}',
    'NUCLEI_NICE': '  url         = {https://doc.nucleisys.com/hbirdv2/17_nice.html}',
    'KUNG_SYSTOLIC': '  doi         = {10.1109/MC.1982.1653825},\n  journal     = {IEEE Computer},\n  volume      = {15},\n  number      = {1},\n  pages       = {37--46}',
    'SZE_SURVEY': '  doi         = {10.1109/JPROC.2017.2761740},\n  journal     = {Proceedings of the IEEE},\n  volume      = {105},\n  number      = {12},\n  pages       = {2295--2329}',
    'DIANNAO': '  doi         = {10.1145/2541940.2541967},\n  pages       = {269--284}',
    'EYERISS': '  doi         = {10.1109/JSSC.2016.2616357},\n  journal     = {IEEE Journal of Solid-State Circuits},\n  volume      = {52},\n  number      = {1},\n  pages       = {127--138}',
    'TPU': '  doi         = {10.1145/3079856.3080246},\n  pages       = {1--12},\n  note        = {arXiv:1704.04760}',
    'GEMMINI': '  doi         = {10.1109/DAC18072.2020.9218590},\n  booktitle   = {ACM/IEEE Design Automation Conference (DAC)}',
    'LENET': '  doi         = {10.1109/5.726791},\n  journal     = {Proceedings of the IEEE},\n  volume      = {86},\n  number      = {11},\n  pages       = {2278--2324}',
    'ALEXNET': '  doi         = {10.1145/3065386},\n  booktitle   = {Advances in Neural Information Processing Systems (NeurIPS)},\n  volume      = {25}',
    'JACOB_QUANT': '  doi         = {10.1109/CVPR.2018.00286},\n  booktitle   = {IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}',
    'KRISHNAMOORTHI_QUANT': '  eprint      = {1806.08342},\n  note        = {arXiv:1806.08342}',
    'HAN_DEEPCOMPRESS': '  booktitle   = {International Conference on Learning Representations (ICLR)}',
    'KUON_FPGA_GAP': '  doi         = {10.1109/TCAD.2007.891375},\n  journal     = {IEEE Transactions on Computer-Aided Design},\n  volume      = {26},\n  number      = {2},\n  pages       = {203--215}',
    'ROCKETCHIP': '  url         = {https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-17.html}',
    'GDB_MANUAL': '  url         = {https://sourceware.org/gdb/documentation/}',
    'OPENOCD_MANUAL': '  url         = {https://openocd.org/doc/html/index.html}',
    'XILINX_UG908': '  url         = {https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging}',
    'XILINX_UG901': '  url         = {https://docs.amd.com/r/en-US/ug901-vivado-synthesis}',
    'XILINX_UG904': '  url         = {https://docs.amd.com/r/en-US/ug904-vivado-implementation}',
}

# Apply updates: find each entry and insert doi/url before the closing brace
for key, field_text in updates.items():
    # Find the entry's closing brace
    pattern = rf'(@\w+\{{{key},\n.*?\n\}})'
    match = re.search(pattern, bib, re.DOTALL)
    if match:
        entry = match.group(1)
        # Insert the fields before the closing brace
        new_entry = entry[:-2] + ',\n' + field_text + '\n}'
        bib = bib.replace(entry, new_entry)
        print(f"  Updated: {key}")
    else:
        print(f"  NOT FOUND: {key}")

with open(BIB_PATH, 'w', encoding='utf-8') as f:
    f.write(bib)

print(f"\nUpdated {BIB_PATH}")
print(f"Total DOIs added: {sum(1 for v in updates.values() if 'doi' in v)}")
