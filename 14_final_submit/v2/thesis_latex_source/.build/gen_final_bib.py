"""
Extract selected papers from Zotero + essential English refs -> final references.bib
"""
import sqlite3, os, re

db = sqlite3.connect(r'C:\Users\16084\Desktop\zotero_tmp.sqlite')

def get_item(key):
    item = db.execute("""SELECT i.itemID, it.typeName FROM items i
        JOIN itemTypes it ON i.itemTypeID=it.itemTypeID WHERE i.key=?""", (key,)).fetchone()
    if not item: return None

    item_id, etype = item[0], item[1]

    # Title
    t = db.execute("""SELECT fd.value FROM itemData id JOIN fields f ON id.fieldID=f.fieldID
        JOIN itemDataValues fd ON id.valueID=fd.valueID
        WHERE id.itemID=? AND f.fieldName='title'""", (item_id,)).fetchone()
    title = t[0] if t else '?'

    # Authors
    creators = db.execute("""SELECT c.firstName, c.lastName FROM creators c
        JOIN itemCreators ic ON c.creatorID=ic.creatorID
        WHERE ic.itemID=? ORDER BY ic.orderIndex""", (item_id,)).fetchall()
    authors = [f"{f or ''} {l or ''}".strip() for f, l in creators]

    # All fields
    fields = db.execute("""SELECT f.fieldName, fd.value FROM itemData id
        JOIN fields f ON id.fieldID=f.fieldID
        JOIN itemDataValues fd ON id.valueID=fd.valueID
        WHERE id.itemID=?""", (item_id,)).fetchall()
    d = {}
    for fn, fv in fields:
        try: d[fn] = fv.encode('latin-1').decode('utf-8')
        except: d[fn] = fv

    return {
        'key': key, 'type': etype, 'title': title, 'authors': authors,
        'pub': d.get('publicationTitle', d.get('bookTitle', '')),
        'date': (d.get('date', '') or '')[:4],
        'doi': d.get('DOI', ''),
        'vol': d.get('volume', ''), 'issue': d.get('issue', ''),
        'pages': d.get('pages', ''),
        'url': d.get('url', ''),
    }

# ================================================================
# Selected papers from Zotero
# ================================================================
zotero_keys = [
    # Core 7 (user selected)
    ('345VZF5Z', 'diannao2016'),
    ('LFWJ83GS', 'zhou2017cnn'),
    ('FAA9BX5X', 'liu2021riscv'),
    ('Q53E3MI4', 'wang2023xiangshan'),
    ('LAEDE2AN', 'cao2024cnn'),

    # Additional high-quality matches
    ('E594VQGK', 'wang2024riscvcnn'),
    ('UVM2YAWF', 'zhang2021soc'),
    ('DRTCQ3BY', 'liao2021isa'),
    ('MB352RKW', 'jin2026fpga'),
    ('NH4ULS75', 'feng2019lenet5'),
    ('PTUJW3ZL', 'wu2022domestic'),
    ('DKCSMR26', 'chen2024fnt'),
    ('9EWCNFHX', 'wang2021winograd'),
    ('D9AF42FN', 'jigalur2025sparse'),
    ('QHELFVZZ', 'fu2020processor'),
    ('8XXQLFEA', 'gong2023multimode'),
]

zotero_entries = []
for key, citekey in zotero_keys:
    item = get_item(key)
    if not item:
        print(f"  NOT FOUND: {key}")
        continue
    item['citekey'] = citekey
    zotero_entries.append(item)
    print(f"  [{citekey}] {item['title'][:70]}")

print(f"\nZotero entries: {len(zotero_entries)}")

# ================================================================
# Generate BibTeX
# ================================================================
bib_lines = []
bib_lines.append('% Thesis References - RISC-V CNN Accelerator FPGA Prototype')
bib_lines.append('% Generated 2026-05-06 from Zotero + verified sources')
bib_lines.append('')

for item in zotero_entries:
    key = item['citekey']
    etype = item['type']
    title = item['title']
    authors = item['authors']
    pub = item['pub']
    date = item['date']
    doi = item['doi']
    vol = item['vol']
    issue = item['issue']
    pages = item['pages']
    url = item['url']

    # BibTeX type mapping
    bibtype = 'article'
    if etype == 'conferencePaper': bibtype = 'inproceedings'
    elif etype == 'book': bibtype = 'book'

    bib = f"@{bibtype}{{{key},\n"
    bib += f"  title = {{{title}}},\n"

    if authors:
        bib += f"  author = {{{' and '.join(authors)}}},\n"

    if bibtype == 'article' and pub:
        bib += f"  journal = {{{pub}}},\n"
    elif bibtype == 'inproceedings' and pub:
        bib += f"  booktitle = {{{pub}}},\n"
    elif bibtype == 'book' and pub:
        bib += f"  publisher = {{{pub}}},\n"

    if vol: bib += f"  volume = {{{vol}}},\n"
    if issue: bib += f"  number = {{{issue}}},\n"
    if pages: bib += f"  pages = {{{pages}}},\n"
    if date: bib += f"  year = {{{date}}},\n"
    if doi: bib += f"  doi = {{{doi}}},\n"
    if url: bib += f"  url = {{{url}}},\n"

    bib += "}\n"
    bib_lines.append(bib)

# ================================================================
# Add essential English references not in Zotero
# ================================================================
essential_refs = r'''
@techreport{RISCV_UNPRIV_SPEC,
  title = {The {RISC-V} Instruction Set Manual, Volume {I}: Unprivileged Architecture},
  author = {Andrew Waterman and Krste Asanovi{\'c}},
  institution = {RISC-V Foundation},
  year = {2019},
  number = {Document Version 20191213},
  url = {https://riscv.org/technical/specifications/}
}

@techreport{RISCV_PRIV_SPEC,
  title = {The {RISC-V} Instruction Set Manual, Volume {II}: Privileged Architecture},
  author = {Andrew Waterman and Krste Asanovi{\'c}},
  institution = {RISC-V Foundation},
  year = {2021},
  url = {https://riscv.org/technical/specifications/}
}

@article{KUNG_SYSTOLIC,
  title = {Why Systolic Architectures?},
  author = {H. T. Kung},
  journal = {IEEE Computer},
  volume = {15},
  number = {1},
  pages = {37--46},
  year = {1982},
  doi = {10.1109/MC.1982.1653825}
}

@article{SZE_SURVEY,
  title = {Efficient Processing of Deep Neural Networks: A Tutorial and Survey},
  author = {Vivienne Sze and Yu-Hsin Chen and Tien-Ju Yang and Joel S. Emer},
  journal = {Proceedings of the IEEE},
  volume = {105},
  number = {12},
  pages = {2295--2329},
  year = {2017},
  doi = {10.1109/JPROC.2017.2761740}
}

@article{EYERISS,
  title = {{Eyeriss}: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks},
  author = {Yu-Hsin Chen and Tushar Krishna and Joel S. Emer and Vivienne Sze},
  journal = {IEEE Journal of Solid-State Circuits},
  volume = {52},
  number = {1},
  pages = {127--138},
  year = {2017},
  doi = {10.1109/JSSC.2016.2616357}
}

@article{LENET,
  title = {Gradient-Based Learning Applied to Document Recognition},
  author = {Yann LeCun and L{\'e}on Bottou and Yoshua Bengio and Patrick Haffner},
  journal = {Proceedings of the IEEE},
  volume = {86},
  number = {11},
  pages = {2278--2324},
  year = {1998},
  doi = {10.1109/5.726791}
}

@inproceedings{DIANNAO,
  title = {{DianNao}: A Small-Footprint High-Throughput Accelerator for Ubiquitous Machine-Learning},
  author = {Tianshi Chen and Zidong Du and Ninghui Sun and Jia Wang and Chengyong Wu and Yunji Chen and Olivier Temam},
  booktitle = {Proceedings of the 19th International Conference on Architectural Support for Programming Languages and Operating Systems ({ASPLOS})},
  pages = {269--284},
  year = {2014},
  doi = {10.1145/2541940.2541967}
}

@inproceedings{TPU,
  title = {In-Datacenter Performance Analysis of a Tensor Processing Unit},
  author = {Norman P. Jouppi and Cliff Young and Nishant Patil and David A. Patterson},
  booktitle = {Proceedings of the 44th Annual International Symposium on Computer Architecture ({ISCA})},
  pages = {1--12},
  year = {2017},
  doi = {10.1145/3079856.3080246}
}

@article{JACOB_QUANT,
  title = {Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference},
  author = {Benoit Jacob and Skirmantas Kligys and Bo Chen and Menglong Zhu and Matthew Tang and Andrew Howard and Hartwig Adam and Dmitry Kalenichenko},
  booktitle = {IEEE/CVF Conference on Computer Vision and Pattern Recognition ({CVPR})},
  pages = {2704--2713},
  year = {2018},
  doi = {10.1109/CVPR.2018.00286}
}

@manual{NUCLEI_E203,
  title = {{Nuclei} Hummingbird {E203} Processor User Manual},
  author = {{Nuclei System Technology}},
  year = {2020},
  url = {https://github.com/riscv-mcu/e203_hbirdv2}
}

@manual{NUCLEI_NICE,
  title = {{Nuclei} Instruction Co-extension ({NICE}) Interface Specification},
  author = {{Nuclei System Technology}},
  year = {2020},
  url = {https://doc.nucleisys.com/hbirdv2/}
}

@manual{ALIENTEK_DAVINCI,
  title = {Davinci {Pro} {FPGA} Development Board User Manual},
  author = {{ALIENTEK}},
  year = {2022},
  url = {http://www.openedv.com/docs/boards/fpga/}
}

@manual{XILINX_UG908,
  title = {Vivado Design Suite User Guide: Programming and Debugging ({UG908})},
  author = {{AMD Xilinx}},
  year = {2023},
  url = {https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging}
}
'''

bib_lines.append(essential_refs)

# ================================================================
# Write file
# ================================================================
OUT = r"C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\references.bib"
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(bib_lines))

# Count entries
count = len([l for l in bib_lines if l.startswith('@')])
print(f"\nTotal references: {count}")
print(f"Saved to: {OUT}")
db.close()
