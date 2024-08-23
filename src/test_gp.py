from gp import *

def test_lectura_unico(leidos):
    print(len(leidos)) 


def test_campeonato(puntuaciones):
    clasificacion = campeonato(puntuaciones)
    print(clasificacion) 

def test_resultados_gp_equipo(gp, equipo):
    resultados = get_resultados_gp_equipo(gp, equipo)
    for r in resultados:
        print(r)

def test_resultados_gp(gp):
    resultados = get_resultados_gp(gp)
    print (resultados)

def main():
    RESULTADOS_GP= lee_gp('data/gp_monaco.csv')
    PUNTUACIONES = lee_puntos('data/puntos.csv')
    #test_lectura_unico(RESULTADOS_GP) #El resultado esperado es 14
    test_campeonato(PUNTUACIONES) #Esperamos los 3 primeros pilotos del campeonato
    #test_resultados_gp_equipo('monaco', 'HIS') #Esperamos los 2 pilotos del Vela
    #test_resultados_gp('monaco') #Esperamos todos los resultados del gp de Monaco. Solo se muestran los pilotos, los equipos y las posiciones
    

if __name__ == '__main__':
    main()