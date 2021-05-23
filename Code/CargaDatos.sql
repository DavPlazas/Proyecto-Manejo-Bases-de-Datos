--DEPARTAMENTO
select * from departamento;

copy departamento (codigo_d,nombre_d,numero_evaluados_d)
from 'C:\Carga datos proyectoBD\Departamento.csv' with delimiter ';' csv header;

--MUNICIPIO
select * from municipio where nombre_m='MAGANGUÉ';

copy municipio (codigo_d_departamento,nombre_m,codigo_m,numero_evaluados_m)
from 'C:\Carga datos proyectoBD\Municipio.csv' with delimiter ';' csv header;

--COLEGIO
select * from colegio;

--ERROR AL CARGAR DATOS: 
--EL TIPO DE DATO INT NO SOPORTA LOS NUMEROS DE LA COLUMNA CODIGO
--POR LO QUE HAY QUE ELIMINAR LOS CONSTRAINT'S PARA CAMBIAR EL TIPO DE DATO
--EN TODAS LAS TABLAS QUE TENGAN RELACION CON COLEGIO.CODIGO.
--TAMBIEN SE PRESENTA UN ERROR CON EL TIPO DE DATO DE LA COLUMNA nombre_colegio
--varchar(30) no es suficiente para algunos nombres de colegios
--ASIMISMO SE PRESENTA UN ERROR CON LA COLUMNA codigo_m_municipio
--PUES ALGUNOS COLEGIOS NO TIENEN UNA IDENTIFICACION PARA VER A QUE
--MUNICIPIO PERTENECEN '-'


--ELIMINAR LA LLAVE FORANEA (CODIGO) EN LA TABLA ESTUDIANTE 
alter table estudiante drop constraint estudiante_codigo_colegio_fkey;

--ELIMINAR EL CONSTRAINT DE PK DE CODIGO EN COLEGIO
alter table colegio drop constraint colegio_pkey;

--UNA VEZ EJECUTADO LO ANTERIOR, SE CAMBIA EL TIPO DE DATO
alter table colegio alter column codigo set data type varchar(15);
alter table estudiante alter column codigo_colegio set data type varchar(15);

--SE DEBE VOLVER A CREAR LOS CONSTRAINT ANTERIORMENTE ELIMINADOS
alter table colegio add constraint colegio_pkey primary key(codigo);

--Foreign key de estudiante
alter table estudiante add constraint estudiante_codigo_colegio_fkey foreign key(codigo_colegio)
references colegio(codigo);

--Cambiar el tipo de dato de nombre_colegio

alter table colegio alter column nombre_colegio set data type varchar(120);

--ERRORES QUE SE PRESENTARON:
--ERROR:  el valor es demasiado largo para el tipo character varying(80)
--CONTEXT:  COPY colegio, línea 152, columna nombre_colegio: «I.E. INSTITUTO EDUCATIVO DE FORMACION INTERCULTURAL COMUNITARIO KWESX UMA KIWE - INFIKUK

--ULTIMO ERROR: HUBO LA NECESIDAD DE BUSCAR LA UBICACION DE ALGUNOS COLEGIOS EN EL PAIS
--PUESTO QUE NO TENIAN codigo_m y dependiendo de su ubicacion, buscar el respectivo codigo_m
--y añadirlo

--POR ULTIMO, SE REALIZA LA CARGA DE DATOS
copy colegio (codigo,nombre_colegio,calendario,genero,localizacion,naturaleza,codigo_m_municipio) 
from 'C:\Carga datos proyectoBD\Colegio2.csv' with delimiter ';' csv header;

select * from colegio;

--ESTUDIANTE
--ERROR CON LAS FECHAS DEL ARCHIVO estudiante
--CAMBIO TOTAL DEL ARCHIVO
--TAMBIEN SE PRESENTA ERROR CON LA COLUMNA estrato
--PUES TIENE LA PALABRA "estrato #" POR LO QUE SE CAMBIA
--ESTO. ALGUNAS FILAS TIENEN COMO VALOR "-", "Sin" EN LA COLUMNA estrato
--POR LO QUE SE ELIGE UN NUMERO PARA EL ESTRATO INDEFINIDO:-1

--CODIGO PARA ARREGLAR LAS FECHAS DE NACIMIENTO:C++ 

--FINALMENTE CARGAR LOS DATOS
copy estudiante(id_estudiante,fecha_nacimiento,estrato,sexo,codigo_colegio)
from 'C:\Carga datos proyectoBD\EstudianteTotal.csv' with delimiter ';' csv header;

select * from estudiante;

--EXAMEN

--ERRORES:
--COLUMNA percentil APARECE EL DATO "-" POR LO QUE SE LE ASIGNA EL VALOR DE UN ENTERO:-1
--EN LA COLUMNA puntaje_ingles APARECE EL DATO NULL
--POR LO QUE SE DEBE ELIMINAR EL CONSTRAINT DE QUE ESTAS COLUMNAS NO SEAN NULL

copy examen(id_examen,percentil,puntaje_global,periodo,puntaje_c_naturales,puntaje_matematicas,
			puntaje_sociales,puntaje_ingles,puntaje_lectura_critica,id_estudiante)
from 'C:\Carga datos proyectoBD\ExamenFinal.csv' delimiter ';' csv header;

alter table examen alter column puntaje_ingles drop not null;

select * from examen;

update departamento set nombre_d = 'SANTAFE DE BOGOTA D.C' where codigo_d = 11

update departamento set nombre_d = 'NORTE DE SANTANDER' where codigo_d = 54

update departamento set nombre_d = 'VALLE DEL CAUCA' where codigo_d = 76
