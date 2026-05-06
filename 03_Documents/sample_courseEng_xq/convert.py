import sys
import traceback
from markitdown import MarkItDown

md = MarkItDown()

files = [
    ("C:/Users/16084/Desktop/sample_courseEng_xq/课程分学期Excel上传须知.docx", "C:/Users/16084/Desktop/sample_courseEng_xq/须知.md"),
    ("C:/Users/16084/Desktop/sample_courseEng_xq/10738075291455488.pdf", "C:/Users/16084/Desktop/sample_courseEng_xq/pdf1.md"),
    ("C:/Users/16084/Desktop/sample_courseEng_xq/10731211648503808.pdf", "C:/Users/16084/Desktop/sample_courseEng_xq/pdf2.md"),
    ("C:/Users/16084/Desktop/sample_courseEng_xq/2026042621592917.xlsx", "C:/Users/16084/Desktop/sample_courseEng_xq/excel.md"),
]

for src, dst in files:
    try:
        result = md.convert(src)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        print(f"OK: {src}")
    except Exception as e:
        print(f"ERR: {src}")
        traceback.print_exc()
        sys.stdout.flush()
