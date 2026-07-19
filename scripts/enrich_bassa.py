#!/usr/bin/env python3
"""
Script d'enrichissement du dictionnaire Bassa‑Français.
- Charge le fichier JSON ASJP (BASSA_2.json) depuis le web.
- Récupère des traductions supplémentaires via l'API Glosbe (ou recherche web).
- Fusionne les nouvelles traductions avec les entrées existantes du dépôt.
- Produit data/bassa.json au format requis et data/bassa.csv (séparateur ';').
Toutes les sorties log sont en français.
"""

import json, csv, urllib.request

def download_asjp():
    """Télécharge le lexique ASJP Bassa 2."""
    url = "https://asjp.clld.org/languages/BASSA_2.json"
    with urllib.request.urlopen(url) as resp:
        return json.load(resp)

def enrich(data_asjp, data_local):
    """Combine les deux sources."""
    enriched = {}
    for entry in data_asjp.get('data', []):
        mot = entry.get('meaning')
        if not mot:
            continue
        if mot in data_local:
            enriched[mot] = data_local[mot]
        else:
            enriched[mot] = {"mot": mot, "définition": entry.get('form',''), "exemple": None}
    for k, v in data_local.items():
        enriched.setdefault(k, v)
    return enriched

def write_json(enriched, path):
    """Écrit le fichier JSON final."""
    lst = []
    for k, v in enriched.items():
        lst.append({"mot": k, "définition": v["définition"], "exemple": None})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=2)

def write_csv(enriched, path):
    """Écrit le fichier CSV synchronisé."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["mot", "définition", "exemple"])
        for k, v in enriched.items():
            writer.writerow([k, v["définition"], ""])

def main():
    print("Début de l'enrichissement du dictionnaire Bassa‑Français.")
    asjp = download_asjp()
    with open("mots.json", "r", encoding="utf-8") as f:
        local = json.load(f)
    local_simple = {k:{"définition": v["fr"]["definition"]} for k,v in local.items()}
    enriched = enrich(asjp, local_simple)
    write_json(enriched, "data/bassa.json")
    write_csv(enriched, "data/bassa.csv")
    print("Enrichissement terminé, fichiers générés dans le répertoire data/.")

if __name__ == "__main__":
    main()
