def media(list):
    return sum(list)/ len(list)

def mediana(list):
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return sum(list)/ 2 
    else:
        return mediana(list[1:-1])
