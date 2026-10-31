import json
import os
import requests

# Zoznam všetkých zdrojov letákov pre CartSmart s presnými URL adresami
SOURCES = {
    "lidl": {
        "type": "json_api",
        "url": "https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=online-letak-platny-od-26-10-2026&region_id=0&region_code=0",
    },
    "kaufland": {
        "type": "json_api",
        "url": "https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=SK_sk_KDZ_1020_SK44-LFT&region_id=1020&region_code=1020",
    },
    "tesco": {
        "type": "json_api",
        "url": "https://www.tesco.sk/_next/data/U8AvdpcYs940gnlyz0fIm/akciove-ponuky/letaky-a-katalogy/hypermarkety/tesco-letak-2026-10-28/1.json?leafletType=hypermarkety&storeSlug=&leafletSlug=tesco-letak-2026-10-28&pageNumber=1",
    },
    "billa": {
        "type": "pdf",
        "url": "https://view.publitas.com/64070/3470637/pdfs/b82fead5-3f28-4bd6-bea0-692350accf71.pdf?response-content-disposition=attachment%3B+filename%2A%3DUTF-8%27%27BILLA.sk%2520-%2520BILLA_letak_W44_2026.pdf",
    },
    "kraj": {
        "type": "publitas_json",
        "url": "https://view.publitas.com/terno-letak/w44_letak_kraj_online/page/1/hotspots_data.json?version=ZGEyZDdlNzgxOTczZDRmMGIyYjUzMjhiMTZlMDJiOGJmNWZmZGQxZQ%3D%3D&page=1",
    },
    "terno": {
        "type": "publitas_json",
        "url": "https://view.publitas.com/terno-letak/w44_letak_terno_200x297mm_online/page/1/hotspots_data.json?version=ODYyZmZkYmUxNTcyMDRmZjRiMDgyMzkxNWIxOTRmYzNmYjgwN2YzYw%3D%3D&page=1",
    },
    "coop_jednota": {
        "type": "adobe_json",
        "url": "https://indd.adobe.com/view/publication/ab1dcc8b-548c-4fd3-bc13-ce94fbf9e679/1/content.json",
    },
    "dm_drogerie": {
        "type": "publitas_json",
        "url": "https://journal.mojadm.sk/journal-oktober-2026/page/1/hotspots_data.json?version=ODFhMDllNTg3OGE1NzRmYWRiOTdkMDI4YWYxMTRiN2QyYTJkOWI2MA%3D%3D&page=1",
    },
    "action": {
        "type": "publitas_json",
        "url": "https://sk.publications.action.com/action-week-44-2026/page/1/hotspots_data.json?version=ZDA5NmFlYzc5ODMxN2M0NGY0YTgyZjA0ODI5OTY5NjY5YzE1YTk4ZA%3D%3D&page=1",
    },
}


def aggregate_leaflets():
  consolidated_data = {}

  for store, info in SOURCES.items():
    print(f"Spracovávam reťazec: {store} (Typ: {info['type']})")
    try:
      response = requests.get(info["url"], timeout=15)
      if response.status_code == 200:
        if info["type"] in ["publitas_json", "adobe_json", "json_api"]:
          consolidated_data[store] = response.json()
        elif info["type"] == "pdf":
          consolidated_data[store] = {"pdf_url": info["url"]}
        print(f"-> Úspešne stiahnuté pre {store}")
      else:
        print(f"-> Chyba: HTTP {response.status_code}")
    except Exception as e:
      print(f"-> Výnimka pri sťahovaní {store}: {e}")

  output_filename = "leaflets.json"
  with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(consolidated_data, f, ensure_ascii=False, indent=2)

  print(f"\nHotovo! Všetky dáta uložené do {output_filename}")


if __name__ == "__main__":
  aggregate_leaflets()
