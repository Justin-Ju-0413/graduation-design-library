import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

db = sqlite3.connect(r'C:\Users\16084\Desktop\zotero_copy4.sqlite')

items = db.execute("""
    SELECT i.key, i.itemID, it.typeName
    FROM items i JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE it.typeName NOT IN ('note','attachment','annotation')
    ORDER BY i.itemID DESC
""").fetchall()

papers = []
webpages = []

for key, item_id, type_name in items:
    # Title
    title = db.execute("SELECT fd.value FROM itemData id JOIN fields f ON id.fieldID=f.fieldID JOIN itemDataValues fd ON id.valueID=fd.valueID WHERE id.itemID=? AND f.fieldName='title'", (item_id,)).fetchone()
    title = title[0] if title else '?'

    # Authors
    creators = db.execute("SELECT c.firstName, c.lastName FROM creators c JOIN itemCreators ic ON c.creatorID=ic.creatorID WHERE ic.itemID=? ORDER BY ic.orderIndex", (item_id,)).fetchall()
    authors = '; '.join([f"{f or ''} {l or ''}".strip() for f, l in creators])

    # Pub
    pub_row = db.execute("SELECT fd.value FROM itemData id JOIN fields f ON id.fieldID=f.fieldID JOIN itemDataValues fd ON id.valueID=fd.valueID WHERE id.itemID=? AND f.fieldName='publicationTitle'", (item_id,)).fetchone()
    pub = pub_row[0] if pub_row else ''

    # Date
    date_row = db.execute("SELECT fd.value FROM itemData id JOIN fields f ON id.fieldID=f.fieldID JOIN itemDataValues fd ON id.valueID=fd.valueID WHERE id.itemID=? AND f.fieldName='date'", (item_id,)).fetchone()
    date = date_row[0][:4] if date_row else ''

    # DOI
    doi_row = db.execute("SELECT fd.value FROM itemData id JOIN fields f ON id.fieldID=f.fieldID JOIN itemDataValues fd ON id.valueID=fd.valueID WHERE id.itemID=? AND f.fieldName='DOI'", (item_id,)).fetchone()
    doi = doi_row[0] if doi_row else ''

    entry = (key, type_name, title, authors, pub, date, doi)
    if type_name == 'webpage':
        webpages.append(entry)
    else:
        papers.append(entry)

# Also check for XiangShan, Faster R-CNN, and 2024 CNN accelerator
print("=== NEW papers added (searched by keywords) ===")
for key, t, title, authors, pub, date, doi in papers:
    title_lower = title.lower()
    if any(kw in title_lower for kw in ['xiangshan', 'faster r-cnn', 'object detection']):
        print(f"[{key}] {title}")
        print(f"  Authors: {authors}")
        print(f"  Pub: {pub} | Date: {date} | DOI: {doi}")
        print()

# Check specifically for the 7 papers the user listed
user_keys = ['345VZF5Z', 'XDA838GE', 'LFWJ83GS', 'FAA9BX5X']
print("=== User's 7 papers - Zotero status ===")
target_titles = [
    'DianNao family',
    'Eyeriss',
    'Faster R-CNN',
    'XiangShan',
]
for key, t, title, authors, pub, date, doi in papers:
    for target in target_titles:
        if target.lower() in title.lower():
            print(f"[{key}] MATCH: {title[:80]}")
            print(f"  Authors: {authors}")
            print(f"  Pub: {pub} | Date: {date} | DOI: {doi}")
            print()
            break

# Summary
print(f"\n=== SUMMARY ===")
print(f"Total papers/books: {len(papers)}")
print(f"Total webpages (junk): {len(webpages)}")
print(f"\nAll papers:")
for i, (key, t, title, authors, pub, date, doi) in enumerate(papers):
    print(f"[{i+1}] [{key}] {title[:90]}")
    if authors: print(f"    -> {authors[:80]}")
    print(f"    -> {pub[:40]} | {date} | DOI:{doi[:30]}")
    print()

if webpages:
    print("--- Junk ---")
    for key, t, title, authors, pub, date, doi in webpages:
        print(f"  [{key}] {title[:80]}")

db.close()
