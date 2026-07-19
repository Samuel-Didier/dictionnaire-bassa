#!/usr/bin/env python3
# This script translates English glosses from ASJP Bassa wordlist to French using deep-translator.
# It expects 'bassa_2.json' in the same directory and outputs 'data/bassa.json' and 'data/bassa.csv'.

import json
from deep_translator import GoogleTranslator
import csv

def main():
    with open('bassa_2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    results = []
    for entry in data:
        # Assuming entry has 'concept' and 'gloss' fields; adapt as needed.
        word = entry.get('concept', '')
        gloss_en = entry.get('gloss', '')
        gloss_fr = GoogleTranslator(source='en', target='fr').translate(gloss_en) if gloss_en else ''
        results.append({"mot": word, "définition": gloss_fr, "exemple": None})
    # Write JSON
    with open('data/bassa.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    # Write CSV
    with open('data/bassa.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['mot', 'définition', 'exemple'])
        for r in results:
            writer.writerow([r['mot'], r['définition'], r['exemple']])

if __name__ == '__main__':
    main()
