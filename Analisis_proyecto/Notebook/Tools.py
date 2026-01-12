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

def cargar_datos_el_toque():
    json_dir = "/home/daniela/Documentos/GitHub/Universidad-MATCOM/Analisis_proyecto/Json/El toque"
    paths = alm(json_dir)
    toque_data = {}
    for archivo in paths:
        toque_data[archivo] = call(archivo, paths)
    return toque_data

def cargar_datos_mip():
    json_dir = "/home/daniela/Documentos/GitHub/Universidad-MATCOM/Analisis_proyecto/Json/mipymes.json"
    paths = alm(json_dir)
    data_mipymes = {}
    for archivo in paths:
        data_mipymes[archivo] = call(archivo, paths)
    return data_mipymes

def cargar_datos_Mercatoria():
    json_dir_AM = "/home/daniela/Documentos/GitHub/Universidad-MATCOM/Analisis_proyecto/Json/mercatoria.json"
    paths = alm(json_dir_AM)
    data_mercatoria = {}
    for archivo in paths:
        data_mercatoria[archivo] = call(archivo, paths)

    return data_mercatoria

def pais_moda_arroz(data_mipymes):
    Paises = {}
    marcas = []  
    
    for archivo in data_mipymes: 
        for prod in data_mipymes[archivo]["Products"]["Nutritious"]:
            if "Arroz" in prod or "Rice" in prod:
                marca = data_mipymes[archivo]["Products"]["Nutritious"][prod]["Brand"]
                if marca and marca not in marcas:
                    marcas.append(marca)

    for archivo in data_mipymes:
        for prod in data_mipymes[archivo]["Products"]["Nutritious"]:
            producto_info = data_mipymes[archivo]["Products"]["Nutritious"][prod]
            if producto_info["Brand"] in marcas:
                pais = producto_info["Exporting_Country"]
                if pais in Paises:
                    Paises[pais] += 1
                else:
                    Paises[pais] = 1

    Pais = []
    Contador = []
    for elemento in Paises:
        Pais.append(elemento) 
        Contador.append(Paises[elemento])
    
    return Pais, Contador

def pais_moda_frijoles(data_mipymes):
    Pais = {}
    Brand = []  
    
    for archivo in data_mipymes: 
        for prod in data_mipymes[archivo]["Products"]["Nutritious"]:
            if "Frijoles" in prod or "Lentejas" in prod:
                marca = data_mipymes[archivo]["Products"]["Nutritious"][prod]["Brand"]
                if marca and marca not in Brand:
                    Brand.append(marca)

    for archivo in data_mipymes:
        for prod in data_mipymes[archivo]["Products"]["Nutritious"]:
            producto_info = data_mipymes[archivo]["Products"]["Nutritious"][prod]
            if producto_info["Brand"] in Brand:
                pais = producto_info["Exporting_Country"]
                if pais in Pais:
                    Pais[pais] += 1
                else:
                    Pais[pais] = 1

    Country = []
    Count = []
    for elemento in Pais:
        Country.append(elemento) 
        Count.append(Pais[elemento])
    
    return Country, Count

def media_arit(lista):
    resultado = 0
    for i in lista:
        resultado += i

    return resultado/len(lista)

def varianza(lista):
    resultado = 0
    for i in lista:
        resultado += (media_arit(lista) - i) ** 2
    return resultado/(len(lista))

def mediana(lista):
    arreglo = sorted(lista)
    if len(lista) % 2 != 0:
        mediano = len(lista)//2
    else:
        i = len(lista)//2
        j = len(lista)// 2 - 1
        mediano = (lista[i] + lista[j]) / 2  

def mercatoria_moda(data_mercatoria):
    Pais_frij = {}
    Marcas_frij = []
    
    Pais_arroz = {}
    Marcas_arroz = []

    for producto in data_mercatoria['frijoles']:
        nombre = producto["name"]
        if "Frijoles" in nombre or "Lentejas" in nombre or "Chicharos" in nombre:
            marca = producto["Brand"]
            if marca and marca not in Marcas_frij:
                Marcas_frij.append(marca)
    
    for producto in data_mercatoria['frijoles']:
        nombre = producto["name"]
        if "Frijoles" in nombre or "Lentejas" in nombre or "Chicharos" in nombre:
            marca = producto["Brand"]
            if marca in Marcas_frij:
                pais = producto["country_of_origin"]
                if pais in Pais_frij:
                    Pais_frij[pais] += 1
                else:
                    Pais_frij[pais] = 1

    for producto in data_mercatoria['arroz']:
        nombre = producto["name"]
        if "Arroz" in nombre:
            marca = producto["Brand"]
            if marca and marca not in Marcas_arroz:
                Marcas_arroz.append(marca)
    
    for producto in data_mercatoria['arroz']:
        nombre = producto["name"]
        if "Arroz" in nombre:
            marca = producto["Brand"]
            if marca in Marcas_arroz:
                pais = producto["country_of_origin"]
                if pais in Pais_arroz:
                    Pais_arroz[pais] += 1
                else:
                    Pais_arroz[pais] = 1
    
    Country_frij = []
    Count_frij = []
    Country_arroz = []
    Count_arroz = []
    
    for elemento in Pais_frij:
        Country_frij.append(elemento) 
        Count_frij.append(Pais_frij[elemento])
    
    for elemento in Pais_arroz:
        Country_arroz.append(elemento)
        Count_arroz.append(Pais_arroz[elemento])
    
    return Country_frij, Count_frij, Country_arroz, Count_arroz


def promedio_canasta_basica(data_mipymes):
    productos_clave = ["Arroz", "Frijoles", "Aceite", "Azucar", "Sal", "Pollo"]
    P = {}
    
    for archivo in data_mipymes:
        for elemento in data_mipymes[archivo]["Products"]["Nutritious"]:
            for producto in productos_clave:
                if producto.lower() in elemento.lower():
                    precio = data_mipymes[archivo]["Products"]["Nutritious"][elemento]["Date"]["Price"]
                    if producto not in P:
                        P[producto] = [precio]
                    else:
                        P[producto].append(precio)
       
        for elemento in data_mipymes[archivo]["Products"]["Other"]:
            for producto in productos_clave:
                if producto.lower() in elemento.lower():
                    precio = data_mipymes[archivo]["Products"]["Other"][elemento]["Date"]["Price"]
                    if producto not in P:
                        P[producto] = [precio]
                    else:
                        P[producto].append(precio)

    producto = []
    media = []

    for producto_nombre, precios in P.items():
        if precios:
            promedio = media_arit(precios)  
            producto.append(producto_nombre)
            media.append(round(promedio, 1))
    
    return producto, media
    

def heatmap_tabla(data_mercatoria):
    data_toque = cargar_datos_el_toque()
    dollar_value = get_dollar_price(data_toque)
    data_frijoles = data_mercatoria["frijoles"]
    columns = ["Negros", "Blancos", "Pintos", "Colorados", "Lentejas", "Chicharos", "Garbanzos", "Chicharos verdes", "Chicharos amarillos"]
    rows = ["USA", "Brasil", "Argentina", "Cuba", "Mexico", "España", "Canada"]
    table = []
    count = []
    for index in range(len(rows)):
        table.append([])
        count.append([])
        for _ in columns:
            table[index].append(0.)
            count[index].append(0.)
        
    for producto in data_frijoles:
        col = columns.index(producto["Type"])
        row = rows.index(producto["country_of_origin"])
        weight = producto["count"].split("/")[0]
        if "kg" in weight:
            weight = float(weight.split(" ")[0]) * 1000
        else:
            weight = float(weight.split(" ")[0])
            
        table[row][col] += producto["price"]* 1000/weight
        
        count[row][col] += 1

    for i in range(len(rows)):
        for j in range(len(columns)):
            if count[i][j]:
                table[i][j] /= count[i][j]
                table[i][j] = round(table[i][j] * dollar_value, 2)

            else:
                table[i][j] = None

    return table
def yogurt_data(data_mer):
    yogurt = data_mer["yogurt"]
    yogurt_flavors = {}
    yogurt_types = {}
    for producto in yogurt:
        type = "Normal" if producto["Type"] is None else producto["Type"].capitalize()
        flavor = producto["flavor"]
        if type in yogurt_types:
            yogurt_types[type] += 1
        else:
            yogurt_types[type] = 1
        if flavor in yogurt_flavors:
            yogurt_flavors[flavor] += 1
        else:
            yogurt_flavors[flavor] = 1
    return yogurt_flavors, yogurt_types

def get_dollar_price(toque_data):
    usd_values = []
    print(toque_data)
    for day in toque_data["El toque"]["eltoque"]:
        price = day["USD"]
        date = tuple(int(i) for i in day["date"].split("-"))
        usd_values.append((date, float(price)))
    return max(usd_values)[1]