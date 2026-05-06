"""
Batch fix AI language traces in LaTeX thesis chapters.
Handles:
1. Delete "This chapter provides/describes..." patterns
2. Delete "The remainder of this thesis is organized as follows..."
3. Fix duplicate table/figure labels
4. Convert pseudo-lists to itemize/enumerate
5. Replace overused transition words sparingly
"""
import re
import os

BASE = r"C:\Users\16084\Documents\Graduation_Design_Library\thesis_latex\chapters"


def read_file(filename):
    with open(os.path.join(BASE, filename), 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filename, content):
    with open(os.path.join(BASE, filename), 'w', encoding='utf-8') as f:
        f.write(content)


# ================================================================
# FIX 1: Clean Ch1 - Delete "Thesis Structure" section + AI ending
# ================================================================
print("Fixing 01_1_introduction.tex...")
ch1 = read_file("01_1_introduction.tex")

# Remove the entire "Thesis Structure" section
ch1 = re.sub(
    r'\\section\{Thesis Structure\}.*?(?=\\section\{)',
    '',
    ch1,
    flags=re.DOTALL
)

# Remove "The remainder of this thesis is organized as follows."
ch1 = re.sub(
    r'The remainder of this thesis is organized as follows\.\s*Chapter \d+.*?(?=\\section\{)',
    '',
    ch1,
    flags=re.DOTALL
)

# Remove "This chapter provides the technical foundation..."
ch1 = re.sub(
    r'\n\nThis chapter provides the technical foundation necessary for understanding.*?\.\n',
    '\n',
    ch1,
    flags=re.DOTALL
)

write_file("01_1_introduction.tex", ch1)
print("  Done")

# ================================================================
# FIX 2: Clean Ch2 - Delete AI ending paragraph
# ================================================================
print("Fixing 02_2_background.tex...")
ch2 = read_file("02_2_background.tex")

# Remove "This chapter describes the design methodology..."
ch2 = re.sub(
    r'\n\nThis chapter describes the design methodology for the RISC-V custom instruction-based.*?\.\n',
    '\n',
    ch2,
    flags=re.DOTALL
)

# Remove duplicate Table labels (plain text that duplicates LaTeX \caption)
# Pattern: "Table 2.1: E203 Processor Core Parameters" before \begin{table}
ch2 = re.sub(
    r'\nTable 2\.\d+: .*?\n(?=\\begin\{table\})',
    '\n',
    ch2
)
ch2 = re.sub(
    r'\nTable 2\.\d+: .*?\n(?=\\begin\{table\})',
    '\n',
    ch2
)

write_file("02_2_background.tex", ch2)
print("  Done")

# ================================================================
# FIX 3: Clean Ch3 - Replace "illustrates" / "summarizes"
# ================================================================
print("Fixing 03_3_methodology.tex...")
ch3 = read_file("03_3_methodology.tex")

# Replace "Figure X illustrates" -> "Figure X shows"
ch3 = re.sub(r'Figure (\d+\.\d+) illustrates', r'Figure \1 shows', ch3)

# Replace "Table X summarizes" -> "Table X presents"
ch3 = re.sub(r'Table (\d+\.\d+) summarizes', r'Table \1 presents', ch3)

# Remove duplicate Table labels
ch3 = re.sub(
    r'\nTable 3\.\d+: .*?\n(?=\s*\\begin\{table\})',
    '\n',
    ch3
)

write_file("03_3_methodology.tex", ch3)
print("  Done")

# ================================================================
# FIX 4: Clean Ch4 - Fix "summarizes" and remove speedup chart
# ================================================================
print("Fixing 04_4_results.tex...")
ch4 = read_file("04_4_results.tex")

# Replace "Table X summarizes"
ch4 = re.sub(r'Table (\d+\.\d+) summarizes', r'Table \1 presents', ch4)
ch4 = re.sub(r'Table (\d+\.\d+) lists', r'Table \1 presents', ch4)

# Fix misleading speedup figure caption
ch4 = re.sub(
    r'\\caption\{CNN accelerator benchmark results showing speedup over software-only execution\.\}',
    r'\caption{Estimated CNN accelerator performance relative to software-only execution. Actual cycle-level measurements await resolution of the RSTAT readback issue (Section 5.2).}',
    ch4
)

# Fix RSTAT mismatch description to be more honest
ch4 = re.sub(
    r'RSTAT comparison result did not match the expected software value',
    r'RSTAT readback returned a value inconsistent with the expected software result---this discrepancy indicates a fundamental issue in the result readback path requiring further investigation',
    ch4
)

write_file("04_4_results.tex", ch4)
print("  Done")

# ================================================================
# FIX 5: Clean Ch5 + Ch6 - Reduce "furthermore"/"moreover"
# ================================================================
print("Fixing 05_5_discussion.tex...")
ch5 = read_file("05_5_discussion.tex")

# Replace overused transition words (keep ~50%, replace others with simpler alternatives)
ch5 = re.sub(r'\bFurthermore,?\s+', 'Additionally, ', ch5, count=2)
ch5 = re.sub(r'\bMoreover,?\s+', 'In addition, ', ch5, count=2)

write_file("05_5_discussion.tex", ch5)
print("  Done")

print("Fixing 06_6_conclusion.tex...")
ch6 = read_file("06_6_conclusion.tex")

ch6 = re.sub(r'\bFurthermore,?\s+', 'Additionally, ', ch6, count=2)
ch6 = re.sub(r'\bMoreover,?\s+', 'In addition, ', ch6, count=2)

write_file("06_6_conclusion.tex", ch6)
print("  Done")

print("\nAll AI trace fixes applied!")
