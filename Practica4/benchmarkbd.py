#!/usr/bin/python
# -*- coding: utf-8 -*-

import peewee
from peewee import *
import modelos
from modelos import *
import sys
import time
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

database_proxy = Proxy()  # Create a proxy for our db.
mysql_calculado = False

class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.

database = MySQLDatabase('Chinook', user='root', passwd='1234')

database_proxy.initialize(database)

# Listar todo el contenido de una tabla grande
def lista_track ():
    for track in Track.select():
        print (track.trackid, track.name, track.albumid, track.mediatypeid,
            track.genreid, track.composer, track.milliseconds, track.bytes,
            track.unitprice)

# Listar todo el contenido de una tabla pequeña
def lista_genero ():
    for gen in Genre.select():
        print (gen.genreid, gen.name)

# Hacer una consulta concreta a una tabla grande
def filtrar_track_composer (composer):
    consulta =  Track.select().where(Track.composer == composer)
    for track in consulta:
        print (track.trackid, track.name, track.albumid, track.mediatypeid,
            track.genreid, track.composer, track.milliseconds, track.bytes,
            track.unitprice)

# Hacer una consulta concreta a una tabla pequeña
def filtrar_generos_nombre (nombre):
    consulta = Genre.select().where(Genre.name == nombre)
    for gen in consulta:
        print (gen.genreid, gen.name)

# Introducir un dato en la base de datos pequeña
def introducir_genero (nombre, num):
    nuevo_gen = Genre.create(name=nombre, genreid=num)

# Introducir un dato en la base de datos grande
def introducir_track (idcancion, nombre, album, mediatype, genero, compositor, ms, bt, precio):
    nueva_track = Track.create(trackid=idcancion, name=nombre, albumid=album, mediatypeid=mediatype,
        genreid=genero, composer=compositor, milliseconds=ms, bytes=bt, unitprice=precio)

def borrar_track (idcancion):
    q = Track.delete().where(Track.trackid == idcancion)
    q.execute()

def borrar_genero (idgenero):
    q = Genre.delete().where(Genre.genreid == idgenero)
    q.execute()

def pruebas():
    resultados = []
    tiempos = []

    # Consultar un dato en una base de datos pequeña
    for x in range(0,4):
        antes = time.time()
        filtrar_generos_nombre("World")
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]  # limpiamos la tabla de tiempos   

    # Consultar un dato en una base de datos grande 
    for x in range(0,4):
        antes = time.time()
        filtrar_track_composer("Antonio Vivaldi")
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]  # limpiamos la tabla de tiempos

    #Introducir un dato en la base de datos pequeña
    generos = [(26,"Progressive Death Metal"), (27, "Symphonic Metal"), 
        (28, "Hard Rock"), (29, "Death Metal")]

    for x in range(0,4):
        antes = time.time()
        introducir_genero(generos[x][1], generos[x][0])
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]  # limpiamos la tabla de tiempos

    # Introducir un dato en la base de datos grande
    canciones = [(3504, "The Moor", 347, 4, 26, "Opeth", 685000, 4744929, 0.99),
                 (3505, "Cry For The Moon", 347, 4, 27, "Epica", 350000, 4744929, 0.99),
                 (3506, "Shout At The Devil", 347, 4, 28, "Motley Crue", 195000, 4744929, 0.99),
                 (3507, "War Eternal", 347, 4, 29, "Arch Enemy", 262000, 4744929, 0.99)]

    for x in range(0,4):
        antes = time.time()
        introducir_track(canciones[x][0], canciones[x][1], canciones[x][2],
            canciones[x][3], canciones[x][4], canciones[x][5], canciones[x][6],
            canciones[x][7], canciones[x][8])
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]  # limpiamos la tabla de tiempos

    # Borrar un dato de una base de datos grande
    id_canciones = [3506,3504,3507,3505]

    for x in range(0,4):
        antes = time.time()
        borrar_track(id_canciones[x])
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]

    # Borrar un dato de una base de datos pequeña
    id_generos = [28,26,29,27]

    for x in range(0,4):
        antes = time.time()
        borrar_genero(id_generos[x])
        despues = time.time()
        tiempo = despues - antes
        tiempos.append(tiempo)

    tiempos.reverse()
    tiempos.pop()
    resultados.append(sum(tiempos)/len(tiempos))
    del tiempos[:]

    return resultados

def calcular_res (pruebas):
    resultados = []
    resultados.append(((pruebas[0] + pruebas[1])/2) + pruebas[4])
    resultados.append(((pruebas[2] + pruebas[3])/2) + pruebas[5])
    mysql_calculado = True
    return resultados

if __name__ == '__main__':
    res_mysql = pruebas()

    mysql_calculado = True

    if mysql_calculado:
        database = SqliteDatabase('Chinook')

    res_sqlite = pruebas()

    parametros = ('Consulta DB peque','Consulta DB grande', 'Escritura DB peque', 
        'Escritura DB grande', 'Borrado DB grande', 'Borrado DB peque')
    y_pos = np.arange(len(parametros))
    plt.bar(y_pos, np.array(res_mysql), align='center', color='r', label='MySQL')
    plt.bar(y_pos, np.array(res_sqlite), align='center', color='b', label='SQlite')
    plt.xticks(y_pos, parametros)
    plt.ylabel('segundos')
    plt.legend()
    plt.show()
