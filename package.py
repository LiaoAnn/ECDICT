import os
import sys

import stardict


def format_entry(data):
    lines = []
    # word = data['word'] # Word is the key, usually not repeated in content unless necessary
    phonetic = data.get('phonetic')
    translation = data.get('translation')
    definition = data.get('definition')
    pos = data.get('pos')
    exchange = data.get('exchange')
    tag = data.get('tag')
    collins = data.get('collins')
    oxford = data.get('oxford')
    bnc = data.get('bnc')
    frq = data.get('frq')

    if phonetic:
        lines.append(f"[{phonetic}]")

    if pos:
        lines.append(f"POS: {pos}")

    if translation:
        lines.append(translation)

    if definition:
        lines.append(definition)

    meta = []
    if tag:
        meta.append(f"Tag: {tag}")
    if collins:
        meta.append(f"Collins: {collins}")
    if oxford:
        meta.append(f"Oxford: {oxford}")
    if bnc:
        meta.append(f"BNC: {bnc}")
    if frq:
        meta.append(f"FRQ: {frq}")

    if meta:
        lines.append(" | ".join(meta))

    if exchange:
        lines.append(f"Exchange: {exchange}")

    return "\n".join(lines)


def main():
    csv_file = 'ecdict.csv'
    if not os.path.exists(csv_file):
        print(f"{csv_file} not found, trying ecdict.mini.csv")
        csv_file = 'ecdict.mini.csv'
        if not os.path.exists(csv_file):
            print("No csv file found.")
            return

    print(f"Loading {csv_file}...")
    db = stardict.DictCsv(csv_file)
    print(f"Loaded {len(db)} words.")

    wordmap = {}
    print("Formatting entries...")
    # db is iterable returning (index, word)
    # We need to query data for each word

    # Using db.dumps() to get all words might be faster or just iterating
    # db.__iter__ returns (index, word)

    count = 0
    total = len(db)

    for index, word in db:
        # Query by index is faster if supported, let's check stardict.py
        data = db.query(index)
        # DictCsv.query supports int index
        if data:
            content = format_entry(data)
            wordmap[word] = content

        count += 1
        if count % 10000 == 0:
            print(f"Processed {count}/{total}")

    print("Exporting to StarDict format...")
    stardict.tools.export_stardict(wordmap, 'ecdict', 'ECDICT')
    print("Done. Generated ecdict.idx, ecdict.dict, ecdict.ifo")

    print("Exporting to MDict source format...")
    stardict.tools.export_mdict(wordmap, 'ecdict.txt')
    print("Done. Generated ecdict.txt")


if __name__ == '__main__':
    main()
if __name__ == '__main__':
    main()
if __name__ == '__main__':
    main()
