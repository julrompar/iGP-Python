from collections import defaultdict, namedtuple
import csv

Resultado = namedtuple('Resultado', 'posicion,piloto,equipo,mejor_vuelta,velocidad_maxima,pitstops,puntos' )
Puntuacion = namedtuple('Puntuacion', 'piloto,puntos')

def lee_gp(fichero):
    res = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for l in lector:
            posicion = int(l[0])
            piloto = l[1].strip()
            equipo= l[2].strip()
            splitsBySemicolon = l[3].split(":")
            mejor_vuelta = float(60 * int(splitsBySemicolon[0]) + float(splitsBySemicolon[1]))
            velocidad_maxima = float(l[4])
            pitstops = int(l[5])
            puntos = int(l[6])
            tupla = Resultado(posicion,piloto,equipo,mejor_vuelta,velocidad_maxima,pitstops,puntos)
            res.append(tupla)
    return sorted(res, key=lambda x: x.posicion)

def lee_puntos(fichero):
    res = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for l in lector:
            piloto = l[1].strip()
            puntos = int(l[3])
            tupla = Puntuacion(piloto,puntos)
            res.append(tupla)
    return res

def campeonato(puntuaciones):
    res = {}
    for p in puntuaciones:
        if p.piloto in res:
            res[p.piloto] += p.puntos
        else:
            res[p.piloto] = p.puntos

    return sorted(res.items(), key=lambda x: x[1], reverse=True)[:3]


def get_resultados_gp_equipo(gp, equipo):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [d for d in datos if d.equipo == equipo]

def get_resultados_gp(gp):
    datos = lee_gp('data/gp_' + gp + '.csv')
    return [(d.piloto, d.equipo, d.posicion) for d in datos]



    