# -*- coding: utf-8 -*-
"""
Created on Sat May 22 21:35:49 2021

@author: David
"""

#Funcion para determinar el promedio obtenido en el area de ingles por departamentos
def avgIngles():
    return ''' select avg(x.puntaje_ingles)::real as promingles, d.nombre_d as departamento from 
    ((((examen x inner join estudiante e on x.id_estudiante=e.id_estudiante)
    inner join colegio c on c.codigo=e.codigo_colegio)inner join municipio m on m.codigo_m=c.codigo_m_municipio)
    inner join departamento d on d.codigo_d=m.codigo_d_departamento) 
    where x.puntaje_ingles is not null group by d.nombre_d;'''

#Promedio de cada asignatura para los hombres(H)
def avgSubjectsM():
    return ''' select e.sexo,avg(x.puntaje_c_naturales)::real as promNaturales,
    avg(x.puntaje_matematicas)::real as promMatematicas,
    avg(x.puntaje_sociales)::real as promSociales,
    avg(x.puntaje_ingles)::real as promIngles,
    avg(x.puntaje_lectura_critica)::real as promLectura 
    from examen x inner join estudiante e on e.id_estudiante=x.id_estudiante 
    group by e.sexo having e.sexo<>'-' and e.sexo='M';'''

#Promedio de cada asignatura para las mujeres(F)
def avgSubjectsF():
    return ''' select e.sexo,avg(x.puntaje_c_naturales)::real as promNaturales,
    avg(x.puntaje_matematicas)::real as promMatematicas,
    avg(x.puntaje_sociales)::real as promSociales,
    avg(x.puntaje_ingles)::real as promIngles,
    avg(x.puntaje_lectura_critica)::real as promLectura 
    from examen x inner join estudiante e on e.id_estudiante=x.id_estudiante 
    group by e.sexo having e.sexo<>'-' and e.sexo='F' '''

