from gp import *

def test_lectura_unico(leidos):
    conjunto = set()
    for l in leidos:
        conjunto.add((l.equipo, l.abreviatura))
    
    print(conjunto) 

def test_qualy(leidos):
    print (leidos)

def test_campeonato(puntuaciones):
    clasificacion = campeonato(puntuaciones)
    print(clasificacion) 

def test_campeonato_constructores(puntuaciones):
        clasificacion = get_campeonato_constructores(puntuaciones)
        print(clasificacion)

def test_resultados_gp_equipo(gp, equipo):
    resultados = get_resultados_gp_equipo(gp, equipo)
    for r in resultados:
        print(r)

def test_resultados_gp(gp):
    resultados = get_resultados_gp(gp)
    print (resultados)

def test_pos_media_equipo(equipo, decisor = None):
    posiciones = get_pos_media_equipo(equipo, decisor)
    print(posiciones)

def main():
    RESULTADOS_GP= lee_gp('data/gps/gp_austria.csv')
    RESULTADOS_GENERALES = lee_gp('data/gps/puntos.csv')
    QUALY_GP = lee_qualy('data/qualy/qualy_austria.csv')
    #test_lectura_unico(RESULTADOS_GP) #El resultado esperado es 14
    #test_qualy(QUALY_GP) #El resultado esperado es una lista de tuplas con los datos de la clasificacion de la qualy
    #test_campeonato(RESULTADOS_GENERALES) #Esperamos los 3 primeros pilotos del campeonato
    #test_campeonato_constructores(PUNTUACIONES) #
    #test_resultados_gp_equipo('monaco', 'HIS') #Esperamos los 2 pilotos del Vela
    #test_resultados_gp('monaco') #Esperamos todos los resultados del gp de Monaco. Solo se muestran los pilotos, los equipos y las posiciones
    test_pos_media_equipo('WAT', 'q') #Esperamos las posiciones medias de los pilotos del equipo WAT en el campeonato
    

if __name__ == '__main__':
    main()