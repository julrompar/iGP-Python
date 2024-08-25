from collections import defaultdict, namedtuple
import csv

""" Pos,Piloto,Equipo,Finalizado,Mejor vuelta,Velocidad Máxima,Pit,Pts. Estas son las propiedades del csv de gps.
    La propiedad del csv finalizado no la uso, pero tampoco la quito del documento, por si la necesito en un futuro.
    TODO: Buscarle un uso a la propiedad finalizado (habría que pasarla a segundos, menos la del primer puesto, que puede ser un 
    time, y a partir de ahí, hacer un timedelta o algo así)"""
Carrera = namedtuple('Carrera', 'posicion,piloto,equipo,abreviatura,mejor_vuelta,velocidad_maxima,pitstops,puntos' )

Qualy = namedtuple('Qualy', 'posicion,piloto,equipo,abreviatura,tiempo,diferencia,neumaticos' )
"""Pos,Piloto,Equipo,Mejor Tiempo,Diferencia,Neumáticos. Estas son las propiedades del csv de qualy. La de diferencia no la uso, ya le daré uso en un futuro.
TODO: Buscarle un uso a la propiedad diferencia"""

def lee_gp(fichero):
    
    res = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for l in lector:
            posicion = int(l[0])
            piloto = l[1].strip()
            equipo= l[2].strip()
            splitsBySemicolon = l[4].split(":")
            mejor_vuelta = float(60 * int(splitsBySemicolon[0]) + float(splitsBySemicolon[1]))
            velocidad_maxima = float(l[5])
            pitstops = int(l[6])
            puntos = int(l[7])
            switcher = {
                "Calamardiño RB": "CRB",
                "Frenando Afondo F1 Team": "FER",
                "Hispalis F1 Team": "HIS",
                "Watiki F1 Team": "WAT",
                "Saca Racing": "SAR",
                "Azuaga Martin": "AZM",
                "DaniDesokupa": "DAD"
            }
            tupla = Carrera(posicion,piloto,equipo,switcher.get(equipo),mejor_vuelta,velocidad_maxima,pitstops,puntos)
            res.append(tupla)
    return res

def lee_qualy(fichero):
    res = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for l in lector:
            posicion = int(l[0])
            piloto = l[1].strip()
            equipo= l[2].strip()
            tiempo = l[3].strip()
            diferencia = l[4].strip()
            neumaticos = l[5].strip()
            switcherAbreviatura = {
                "Calamardiño RB": "CRB",
                "Frenando Afondo F1 Team": "FER",
                "Hispalis F1 Team": "HIS",
                "Watiki F1 Team": "WAT",
                "Saca Racing": "SAR",
                "Azuaga Martin": "AZM",
                "DaniDesokupa": "DAD"
            }
            switcherNeumaticos = {
                'SS': 'Superblandos',
                'S': 'Blandos',
                'M': 'Medios',
                'H': 'Duros',
                'I': 'Intermedios',
                'W': 'Lluvia'
            }
            tupla = Qualy(posicion,piloto,equipo,switcherAbreviatura.get(equipo),tiempo,diferencia,switcherNeumaticos.get(neumaticos))
            res.append(tupla)
    return sorted(res, key=lambda x: x.posicion)



def campeonato(puntuaciones):
    res = defaultdict(int)
    for p in puntuaciones:
        res[p.piloto] += p.puntos

    return sorted(res.items(), key=lambda x: x[1], reverse=True)

def get_campeonato_constructores(puntuaciones):
    res = defaultdict(int)
    for p in puntuaciones:
            res[p.equipo] += p.puntos
    
    return sorted(res.items(), key=lambda x: x[1], reverse=True)


def get_clasificacion(puntuaciones, decisor = None):
    if decisor in ['p', 'P', 'Pilotos', 'pilotos']:
        return campeonato(puntuaciones)
    elif decisor in ['c', 'C', 'Constructores', 'constructores']:
        return get_campeonato_constructores(puntuaciones)
    else:
        return get_campeonato_constructores(puntuaciones), campeonato(puntuaciones)

#TODO: Unir estas dos funciones en una sola. También se le puede añadir un parámetro para que devuelva los resultados de la qualy y/o de la carrera

def get_resultados_gp_equipo(gp, equipo):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [d for d in datos if d.equipo == equipo]

def get_resultados_qualy_equipo(gp,equipo):
    datos = lee_qualy('data/qualy/qualy_' + gp + '.csv')
    return [d for d in datos if d.equipo == equipo]

def get_resultados_gp(gp):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [(d.piloto, d.equipo, d.posicion) for d in datos]

def get_resultados_qualy(gp):
    datos = lee_qualy('data/qualy/qualy_' + gp + '.csv')
    return [(d.piloto, d.equipo, d.posicion) for d in datos]

#TODO: Testear esta función y añadir las condiciones a los if a los resultados de los gps (debería funcionar igualmente pero queda más elegante 
# como lo he hecho en el cálculo de las posiciones medias)

def get_resultados(gp,equipo = None, decisor = None):
    if equipo:
        if decisor in ['q', 'Q', 'Qualy', 'qualy', 'Clasificacion', 'clasificacion', 'Clasificación', 'clasificación']:
            return get_resultados_qualy_equipo(gp,equipo)
        else:
            return get_resultados_gp_equipo(gp,equipo)
    else:
        if decisor in ['q', 'Q', 'Qualy', 'qualy', 'Clasificacion', 'clasificacion', 'Clasificación', 'clasificación']:
            return get_resultados_qualy(gp)
        else:
            return get_resultados_gp(gp)


def get_pos_media_carrera(datos,pilotos):
    res = defaultdict(float)
    for p in pilotos:
        posiciones = [d.posicion for d in datos if d.piloto == p]
        res[p] = round(sum(posiciones) / len(posiciones),2)
    return sorted(res.items(), key=lambda x: x[1])

def get_pos_media_qualy(datos,pilotos):
    res = defaultdict(float)
    for p in pilotos:
        posiciones = [d.posicion for d in datos if d.piloto == p]
        res[p] = round(sum(posiciones) / len(posiciones),2)
    return sorted(res.items(), key=lambda x: x[1])

def get_all_posiciones_medias(datos_gp,datos_qualy,pilotos):
    res = defaultdict(float)
    posicionesCarrera = dict(get_pos_media_carrera(datos_gp, pilotos))
    posicionesQualy = dict(get_pos_media_qualy(datos_qualy, pilotos))
    for p in pilotos:
        res[p] = [('Carrera', posicionesCarrera.get(p)), ('Qualy', posicionesQualy.get(p))]
    return sorted(res.items(), key = lambda x: x[1])

'''
@params
equipo: nombre o abreviatura del equipo del que queremos obtener las posiciones medias.
decisor: de manera predeterminada toma el valor None, por lo que nos devuelve las posiciones medias
de los gps y las qualys. Podemos obtener o solo los de los gps o solo los de la qualy pasando un string válido como párametro (mirar las condiciones
del if y elif para ver las opciones permitidas)

@returns
En cualquiera de sus ramas, devuelve una lista de tuplas obtenida a partir de un dict.items(). En los dos primeros casos, cada tupla formada por el piloto y su posición media. Si 
queremos las posiciones medias tanto de la qualy como de la carrera, obtendremos una lista de tuplas, siguiendo las tuplas el siguiente esquema:
(Nombre piloto, [(Carrera, posición media), (Qualy, posición media)]

'''
def get_pos_media_equipo(equipo,decisor= None):
    datos_gp = lee_gp('data/gps/puntos.csv')
    datos_qualy = lee_qualy('data/qualy/qualys.csv')
    pilotos = {p.piloto for p in datos_gp if p.equipo == equipo or p.abreviatura == equipo}

    if decisor in ['c', 'C', 'Carrera', 'carrera']:
        return get_pos_media_carrera(datos_gp,pilotos)
    elif decisor in ['q', 'Q', 'Qualy', 'qualy', 'Clasificacion', 'clasificacion', 'Clasificación', 'clasificación']:
        return get_pos_media_qualy(datos_qualy,pilotos)
    else:
        return get_all_posiciones_medias(datos_gp,datos_qualy,pilotos)
    
"""
@params
equipo: nombre o abreviatura del equipo del que queremos obtener la diferencia de posiciones medias.

@returns
Devuelve una lista de tuplas con la diferencia de posiciones medias entre la qualy y la carrera de los pilotos de un equipo. Si el resultado es negastivo, 
la media de las posiciones en carrera es mayor, por lo que se han perdido puestos en la carrera respecto a la posición de salida en la qualy. Si el resultado es positivo,
la media de las posiciones en carrera es menor, por lo que se han ganado puestos en la carrera respecto a la posición de salida en la qualy.
"""

def get_diferencia_posiciones_medias(equipo):
    datos_gp = lee_gp('data/gps/puntos.csv')
    datos_qualy = lee_qualy('data/qualy/qualys.csv')
    pilotos = {p.piloto for p in datos_gp if p.equipo == equipo or p.abreviatura == equipo}
    posicionesCarrera = dict(get_pos_media_carrera(datos_gp, pilotos))
    posicionesQualy = dict(get_pos_media_qualy(datos_qualy, pilotos))
    res = defaultdict(float)
    for p in pilotos:
        res[p] = round(posicionesQualy.get(p) - posicionesCarrera.get(p),2)
    return sorted(res.items(), key = lambda x: x[1])
        
def get_pilotos_mas_vr(datos):
    res = defaultdict(int)
    for i in range(0,len(datos)+1, 14):
            datosGranPremio = datos[i:i+14]
            for d in datosGranPremio:
                if d.mejor_vuelta == min([d.mejor_vuelta for d in datosGranPremio]):
                    res[d.piloto] += 1
    return sorted(res.items(), key = lambda x: x[1], reverse = True)

    





    