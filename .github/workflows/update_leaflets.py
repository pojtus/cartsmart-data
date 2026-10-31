from datetime import datetime
import json
import os


def update_leaflets():
  filename = 'leaflets.json'

  # 1. Načítame existujúci JSON súbor, ak existuje
  if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as f:
      try:
        data = json.load(f)
      except json.JSONDecodeError:
        data = []
  else:
    data = []

  print(f'Načítaných {len(data)} letákov z repozitára.')

  # 2. Tu by v budúcnosti prebiehalo sťahovanie/scraping rešeršov z webov obchodov.
  # Pre túto chvíľu ukážeme, že skript žije a aktualizuje časovú pečiatku (timestamp),
  # aby GitHub Action videla zmenu v súbore a urobila commit.
  current_time = datetime.now().strftime('%d.%m.%Y %H:%M')

  for leaflet in data:
    # Pridáme/aktualizujeme informáciu, kedy naposledy bot overil leták
    leaflet['lastScraped'] = current_time

  # 3. Zápis aktualizovaných dát naspäť do leaflets.json
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

  print(
      f'Súbor {filename} bol úspešne aktualizovaný a pripravený pre mobilnú'
      ' appku!'
  )


if __name__ == '__main__':
  update_leaflets()
