from datetime import datetime
import json
import requests


def update_leaflets():
  filename = 'leaflets.json'
  
  # Oficiálna API adresa pre Lidl leták, ktorú sme našli v DevTools
  lidl_api_url = 'https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=online-letak-platny-od-26-10-2026&region_id=0&region_code=0'

  print('Sťahujem čerstvé dáta z Lidl API...')
  try:
    response = requests.get(lidl_api_url, timeout=10)
    
    if response.status_code == 200:
      raw_data = response.json()
      
      # Schwarz API vracia detailnú štruktúru letáku. 
      # Tu si vyskladáme objekt, ktorý presne sedí do našej Android appky:
      leaflet_title = raw_data.get('name', 'Lidl Aktuálny leták')
      
      # Vytvoríme štruktúru pre náš leaflets.json
      parsed_leaflets = [
        {
          "id": "lidl_current",
          "storeId": "lidl",
          "storeName": "Lidl",
          "title": leaflet_title,
          "imageUrl": "https://www.lidl.sk", # Prípadne hlavný obrázok z API
          "validUntil": "Pozri detail letáku",
          "products": [
            {
              "id": "p_api_1",
              "productName": "Dáta úspešne stiahnuté z Lidl API botom",
              "price": 0.00,
              "originalPrice": 0.00,
              "package": "Akcia",
              "discount": "LIVE"
            }
          ],
          "lastScraped": datetime.now().strftime('%d.%m.%Y %H:%M')
        }
      ]

      # Zápis do leaflets.json
      with open(filename, 'w', encoding='utf-8') as f:
        json.dump(parsed_leaflets, f, ensure_ascii=False, indent=2)
        
      print('Súbor leaflets.json bol úspešne aktualizovaný cez Lidl API!')
    else:
      print(f'Chyba pri komunikácii s API: {response.status_code}')

  except Exception as e:
    print(f'Nastala výnimka pri sťahovaní: {e}')


if __name__ == '__main__':
  update_leaflets()
