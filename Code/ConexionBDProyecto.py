# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:28:45 2021

@author: David
"""

import psycopg2

try:
    conexion = psycopg2.connect(user="postgres",
                                password="Veneno2003",
                                database="proyecto",
                                host="localhost",
                                port="5432")
    print("Conexion exitosa!")
    sql1 = """  select * from departamento; """
    sql2 = """ select * from municipio; """
    sql3 = """ select * from colegio;"""
    sql4 = """ select * from estudiante;"""
    sql5 = """ select * from examen;"""
    cursor=conexion.cursor()
    cursor.execute(sql1)
    departamentos=cursor.fetchall()
    print("--------DEPARTAMENTO----- \n")
    for i in departamentos:
        print("Codigo_d: ",i[0]," Nombre_d: ",i[1]," Numero_evaluados_d: ",i[2])
    cursor.execute(sql2)
    municipios=cursor.fetchmany(1000)
    print("\n-------MUNICIPIO---------\n")
    for j in municipios:
        print("Codigo_m: ",j[0]," Codigo_d_departamento: ",j[1],
              " Nombre_m: ",j[2]," Numero_evaluados: ",j[3])
    cursor.execute(sql3)
    colegios=cursor.fetchmany(1000)
    print("\n-------COLEGIO---------\n")
    for k in colegios:
        print("Codigo: ",k[0]," Nombre_colegio ",k[2],
              " Localizacion:  ",k[5]," Naturaleza:  ",k[6])
    cursor.execute(sql4)
    estudiantes=cursor.fetchmany(1000)
    print("\n-------ALGUNOS ESTUDIANTES---------\n")
    for n in estudiantes:
        print("id_estudiante: ",n[0]," sexo: ",n[1]," fecha_nacimiento: ",n[2])
    cursor.execute(sql5)
    examenes=cursor.fetchmany(1000)
    print("\n-------ALGUNOS EXAMENES---------\n")
    for p in examenes:
        print("Id_examen: ",p[0]," Percentil: ",p[1]," Puntaje_global: ",p[2])
           
except psycopg2.Error as e:
    print("Error al consultar",e)
    
finally:
    cursor.close()
    conexion.close()
    print("Conexion cerrada")

