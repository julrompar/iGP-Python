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
    return sorted(res, key=lambda x: x.posicion)

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

    return sorted(res.items(), key=lambda x: x[1], reverse=True)[:3]

def get_campeonato_constructores(puntuaciones):
    res = defaultdict(int)
    for p in puntuaciones:
            res[p.equipo] += p.puntos
    
    return sorted(res.items(), key=lambda x: x[1], reverse=True)

def get_resultados_gp_equipo(gp, equipo):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [d for d in datos if d.equipo == equipo]

def get_resultados_gp(gp):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [(d.piloto, d.equipo, d.posicion) for d in datos]

def get_pos_media_equipo(decisor, equipo):

    if decisor == 'c' or  decisor == 'C' or decisor == 'Carrera' or decisor == 'carrera':
        datos_gp = lee_gp('data/gps/puntos.csv')
        pilotos = [p.piloto for p in datos_gp if p.equipo == equipo or p.abreviatura == equipo]
        res = defaultdict(float)
        for p in pilotos:
            posiciones = [d.posicion for d in datos_gp if d.piloto == p]
            res[p] = sum(posiciones) / len(posiciones)
        return sorted(res.items(), key=lambda x: x[1])
    elif decisor == 'q'or decisor == 'Q' or decisor == 'Qualy' or decisor == 'qualy' or decisor == 'Clasificacion' or decisor == 'clasificacion':
        datos_qualy = lee_qualy('data/qualy/qualys.csv')
        pilotos = [p.piloto for p in datos_qualy if p.equipo == equipo or p.abreviatura == equipo]
        res = defaultdict(float)
        for p in pilotos:
            posiciones = [d.posicion for d in datos_qualy if d.piloto == p]
            res[p] = sum(posiciones) / len(posiciones)
        return sorted(res.items(), key=lambda x: x[1])

    





    