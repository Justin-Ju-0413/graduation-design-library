# -*- coding: utf-8 -*-
import fitz  # PyMuPDF

pdf_path = "C:/Users/16084/Desktop/sample_courseEng_xq/10731211648503808.pdf"
output_dir = "C:/Users/16084/Desktop/sample_courseEng_xq/"

doc = fitz.open(pdf_path)
print(f"PDF共 {len(doc)} 页")

for page_num in range(len(doc)):
    page = doc[page_num]
    # 300 DPI 高清输出
    mat = fitz.Matrix(300 / 72, 300 / 72)
    pix = page.get_pixmap(matrix=mat)
    out_path = f"{output_dir}10731211648503808_page{page_num + 1}.png"
    pix.save(out_path)
    print(f"已保存: {out_path} ({pix.width}x{pix.height})")

doc.close()
print("转换完成")
