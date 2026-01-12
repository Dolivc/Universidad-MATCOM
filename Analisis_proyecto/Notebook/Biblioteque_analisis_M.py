import json
import os

def alm(archivo):
    paths = {}
    for i in os.listdir(archivo):
        paths[i.replace(".json","")] = os.path.join(archivo,i)
    return paths

def call(key:str, data:dict[str]):
    with open(data[key]) as json_archivo:
        data_json = json.load(json_archivo)
    return data_json

def cargar_datos():
    json_dir = "/home/daniela/Documentos/GitHub/Universidad-MATCOM/Analisis_proyecto/Json/mipymes.json"
    paths = alm(json_dir)
    data = {}
    for archivo in paths:
        data[archivo] = call(archivo, paths)
    return data



def debug_pais_moda_arroz(data):
    """Versión con prints para ver qué está pasando"""
    Paises = {
        "Mexico": 0,
        "España": 0,
        "Marruecos": 0,
        "Brasil": 0,
        "Polonia": 0,
        "Cuba": 0   
    }
    
    print("=== DEBUG INICIADO ===")
    print(f"Total de archivos en data: {len(data)}")
    
    # Contador de productos nutritivos totales
    total_nutritious = 0
    arroz_encontrado = 0
    
    for archivo in data:
        print(f"\n--- Archivo: {archivo} ---")
        
        # 1. Verificar si la estructura existe
        if "Products" not in data[archivo]:
            print(f"  ERROR: No tiene clave 'Products'")
            continue
            
        if "Nutritious" not in data[archivo]["Products"]:
            print(f"  ERROR: No tiene clave 'Nutritious'")
            continue
        
        # 2. Contar productos
        productos = data[archivo]["Products"]["Nutritious"]
        total_nutritious += len(productos)
        print(f"  Productos Nutritivos: {len(productos)}")
        
        # 3. Ver productos de arroz
        for prod_nombre in productos:
            if prod_nombre in ["Arroz", "Rice"]:
                arroz_encontrado += 1
                print(f"  ¡ENCONTRADO ARROZ! - Nombre: {prod_nombre}")
                print(f"    Marca: {productos[prod_nombre].get('Brand', 'NO TIENE')}")
                print(f"    País: {productos[prod_nombre].get('Exporting_Country', 'NO TIENE')}")
    
    print(f"\n=== RESUMEN ===")
    print(f"Total productos nutritivos: {total_nutritious}")
    print(f"Total productos de arroz/rice encontrados: {arroz_encontrado}")
    return Paises

def media(list):
    return sum(list)/ len(list)

def mediana(list):
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return sum(list)/ 2 
    else:
        return mediana(list[1:-1])
