import json, re, os, requests
from bs4 import BeautifulSoup

def Mercatoria(start, end, file):
    if file.endswith('.json'):
        filename = file
    else:
        filename = f"{file}.json"
    
    save_dir = './Json/mercatoria/'
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, filename)
    
    products = []

    for page in range(start, end):
        try:
            url = f'https://www.mercatoria.store/catalog?query=arroz&page={page}&sort=popularity'
            response = requests.get(url)
            response.raise_for_status() 
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            for i in soup.select("div.MuiCardContent-root"):
                h3 = i.select_one("h3.MuiTypography-root.MuiTypography-h3.css-p9dpgq")
                p = i.select_one("p.MuiTypography-root.MuiTypography-body1.css-m6tgpv")

                if not h3 or not p:
                    continue
                    
                heading = h3.get_text(strip=True)
                paragraph = p.get_text(strip=True)
                paragraph = paragraph.replace("\xa0", " ").replace("\u00A0", " ")

                match_h = re.match(r"^(.*?)\s*\((.*?)\)$", heading)
                match_p = re.match(r"^([\d\.,]+)\s*([A-Za-z]+)$", paragraph)
                
                if match_h and match_p: 
                    name = match_h.group(1)
                    weight = match_h.group(2)

                    price = match_p.group(1).replace(",", ".")
                    price = float(price)
                    currency = match_p.group(2)

                    if "x" in weight:
                        continue
                        
                    data = {
                        "name": name,
                        "count": weight,
                        "price": price,
                        "currency": currency
                    }

                    products.append(data)
                    
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página {page}: {e}")
            continue
        except Exception as e:
            print(f"Error inesperado en la página {page}: {e}")
            continue

    if os.path.exists(save_path):
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            if isinstance(existing_data, list):
                final_products = existing_data + products
            else:
                final_products = [existing_data] + products
        except json.JSONDecodeError:
            print(f"Advertencia: El archivo {save_path} está corrupto o vacío. Se creará uno nuevo.")
            final_products = products
    else:
        final_products = products

    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(final_products, f, ensure_ascii=False, indent=4)
        print(f"Archivo '{save_path}' actualizado con {len(final_products)} productos.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

Mercatoria(1, 6, 'arroz')