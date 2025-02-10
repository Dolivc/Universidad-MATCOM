import json
import os
import pandas as pd

def alm(archivo):
    paths = {}
    for i in os.listdir(archivo):
        paths[i.replace(".json","")] = os.path.join(archivo,i)
    return paths

def call(key:str,data:dict[str]):
    with open(data[key]) as json_archivo:
        data = json.load(json_archivo)
    return data
json_dir = "C:\\Users\\flaco\\Documents\\GitHub\\Universidad-MATCOM\\Proyecto_Restaurantes_Bares\\Json"
data = alm(json_dir)

for archivo in data:
    data[archivo] = call(archivo, data)

def media(list):
    return sum(list)/ len(list)

def mediana(list):
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return sum(list)/ 2 
    else:
        return mediana(list[1:-1])
    
def contar_restaurant_dist_prop(data):
    Datagrupada = {}
    locales = []
    cocteles = ["Mojito", "Pinha colada", "Daiquiri", "Cuba libre"]
    for archivo in data:
        for drink in data[archivo]["Menu"]["Beverages"]:
            if drink in cocteles:
                cont = data[archivo]["Name"] + "," + data[archivo]["Ownership"] + "," + data[archivo]["Location"]["District"]
                if cont not in locales:
                    locales.append(cont)
                    datgrup = data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"]
                    if datgrup not in Datagrupada:
                        Datagrupada[datgrup] = 1
                    else:
                        Datagrupada[datgrup] += 1
    Distrito = []
    Propiedad = []
    Contador = []
    for elemento in Datagrupada:
        Distrito.append(elemento.split(",")[0])
        Propiedad.append(elemento.split(",")[1])
        Contador.append(Datagrupada[elemento])

    df2 = pd.DataFrame({
        "Municipio": Distrito,
        "Propiedad": Propiedad,
        "Contador": Contador
    })
    return df2

def conteo_rest_gen(data):
    Datagrupada = {}
    for archivo in data:
        if not (data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"] in  Datagrupada):
            Datagrupada[data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"]]  = 1
        else:
            Datagrupada[data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"]]  += 1

    Distrito = []
    Propiedad = []
    Contador = []
    for elemento in Datagrupada:
        Distrito.append(elemento.split(",")[0])
        Propiedad.append(elemento.split(",")[1])
        Contador.append(Datagrupada[elemento])

    df = pd.DataFrame({
        "Municipio": Distrito,
        "Propiedad": Propiedad,
        "Contador": Contador
    })
    return df

#coctel mas ofrecido
Cocteles = {
    "Pinha colada": 0,
    "Daiquiri": 0,
    "Mojito": 0,
    "Cuba libre": 0
}
validas = ["Pinha colada",
    "Daiquiri",
    "Mojito",
    "Cuba libre"]

for archivo in data:
    for drink in data[archivo]["Menu"]['Beverages']:
        if drink in validas:
            Cocteles[drink] += 1

Bebidas =[]
Cantidad = []

for elemento in Cocteles:
    Bebidas.append(elemento.split(",")[0])
    Cantidad.append(Cocteles[elemento])

def cant_var_daiquiri(data):
    jay = {}
    for archivo in data :
        for bebida in data[archivo]["Menu"]["Beverages"]:
            if "Daiquiri" in bebida:
                if not (data[archivo]["Location"]["District"] + "," + bebida in jay):
                    jay[data[archivo]["Location"]["District"]+ "," + bebida] = 1
    Dist = []
    Conta = []
    for ele in jay:
        Dist.append(ele.split(",")[0])
        Conta.append(jay[ele])
    df383 = pd.DataFrame({
        "Municipio": Dist,
        "Contador": Conta
    })
    return df383

def var_dai(data):
    look = {}
    for archivo in data:
        for drink in data[archivo]["Menu"]["Beverages"]:
            if "Daiquiri" in drink:
                if not (data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"] + "," + drink in  look):
                    look[data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"] + "," + drink]  = 1
                else:
                    look[data[archivo]["Location"]["District"] + "," + data[archivo]["Ownership"] + "," + drink]  += 1
    Distrito = []
    Propiedad = []
    Contador = []
    coctel = []
    for elemento in look:
        Distrito.append(elemento.split(",")[0])
        Propiedad.append(elemento.split(",")[1])
        coctel.append(elemento.split(",")[2])
        Contador.append(look[elemento])
    dfVD = pd.DataFrame({
        "Municipio": Distrito,
        "Propiedad": Propiedad,
        "Coctel" : coctel,
        "Contador": Contador
    })
    return dfVD

def media_coctel(data, lookfor):
    Averages = {}
    for archivo in data:
        for drink in data[archivo]["Menu"]["Beverages"]:
            if drink == lookfor:
                if not (f"{data[archivo]["Location"]["District"]}, {data[archivo]["Ownership"]}, {drink}" in  Averages):
                    Averages[f"{data[archivo]["Location"]["District"]}, {data[archivo]["Ownership"]}, {drink}"] = [data[archivo]["Menu"]["Beverages"][drink]["Price"]]
                else:
                     Averages[f"{data[archivo]["Location"]["District"]}, {data[archivo]["Ownership"]}, {drink}"].append(data[archivo]["Menu"]["Beverages"][drink]["Price"])
            
    for elemento in Averages:
        Averages[elemento]= mediana(Averages[elemento])
    Distrito = []
    Propiedad = []
    Coctel = []
    Mediana = []
    for elemento in Averages:
        Distrito.append(elemento.split(",")[0])
        Propiedad.append(elemento.split(",")[1])
        Coctel.append(elemento.split(",")[2])
        Mediana.append(Averages[elemento])

    dfPC = pd.DataFrame({
        "Municipio": Distrito,
        "Propiedad": Propiedad,
        "Coctel": Coctel,
        "Mediana": Mediana
    })
    return dfPC

def contar_coc_mun(data, see):
    Datagrupada = {}
    locales = []
    for archivo in data:
        for drink in data[archivo]["Menu"]["Beverages"]:
            if drink == see:
                cont = data[archivo]["Name"] + "," + data[archivo]["Location"]["District"]
                if cont not in locales:
                    locales.append(cont)
                    datgrup = data[archivo]["Location"]["District"]
                    if datgrup not in Datagrupada:
                        Datagrupada[datgrup] = 1
                    else:
                        Datagrupada[datgrup] += 1
    Distrito = []
    Contador = []
    for elemento in Datagrupada:
        Distrito.append(elemento.split(",")[0])
        Contador.append(Datagrupada[elemento])

    df2 = pd.DataFrame({
        "Municipio": Distrito,
        "Contador": Contador
    })
    return df2

def rest_com_3(data):
    distritos = ["Habana Vieja", "Plaza", "Playa"]
    datatt = {distrito : 0 for distrito in distritos}
    totalrest = {distrito : 0 for distrito in distritos}
    for archivo in data:
        distrito = data[archivo]["Location"]["District"]
        drinks = data[archivo]["Menu"]["Beverages"]
        if distrito not in distritos:
            continue
        ofrece_todos_los_coct = (
            "Mojito" in drinks and
            "Pinha colada" in drinks and
            "Cuba libre" in drinks and
            "Daiquiri" in drinks
        )
        if ofrece_todos_los_coct:
            datatt[distrito] += 1
    
    Distrito = []
    Contador = []
    for elemento in datatt:
        Distrito.append(elemento.split(",")[0])
        Contador.append(datatt[elemento])

    df30 = pd.DataFrame({
        "Municipio": Distrito,
        "Contador": Contador
    })
    return df30

def conteo_3_gen(data):
    data10 = {
    "Habana Vieja" : 0,
    "Plaza" : 0,
    "Playa" : 0
}
    locales = []
    cocteles = ["Mojito", "Pinha colada", "Daiquiri", "Cuba libre"]
    distritos = ["Habana Vieja", "Plaza", "Playa"]
    for archivo in data:
        if data[archivo]["Location"]["District"] in distritos:
            identificador = [f"{data[archivo]["Name"]}, {data[archivo]["Location"]["District"]}"]
            if identificador not in locales:
                for drink in data[archivo]["Menu"]["Beverages"]:
                    if drink in cocteles:
                        locales.append(identificador)
                        data10[data[archivo]["Location"]["District"]] += 1
                        break
    Distrito = []
    Contador = []
    for elemento in data10:
        Distrito.append(elemento.split(",")[0])
        Contador.append(data10[elemento])

    df80 = pd.DataFrame({
        "Municipio": Distrito,
        "Contador": Contador
    })
    return df80

def conteo_cerveza(data):
    dato = {
    "Habana Vieja" : 0,
    "Plaza" : 0,
    "Playa" : 0
    }
    locales = []
    distritos = ["Habana Vieja", "Plaza", "Playa"]
    for archivo in data:
        if data[archivo]["Location"]["District"] in distritos:
            for drink in data[archivo]["Menu"]["Beverages"]:
                if "Cerveza" in drink:
                    dato[data[archivo]["Location"]["District"]] += 1
                    break
    Distrito = []
    Contador = []
    for elemento in dato:
        Distrito.append(elemento.split(",")[0])
        Contador.append(dato[elemento])

    df50 = pd.DataFrame({
        "Municipio": Distrito,
        "Contador": Contador
    })
    return df50