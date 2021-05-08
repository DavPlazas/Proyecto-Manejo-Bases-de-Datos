--Creacion de la base da datos 'proyecto'
-- Database: proyecto

-- DROP DATABASE proyecto;

CREATE DATABASE proyecto
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Colombia.1252'
    LC_CTYPE = 'Spanish_Colombia.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
    
--Creacion de la tabla departamento

create table departamento(
	codigo_d integer, --Identificador de la tabla departamento
	nombre_d varchar(30) not null, --Nombre del departamento
	numero_evaluados_d integer not null, --Numero de estudiantes que presentan la prueba ICFES en el departamento
	primary key(codigo_d) --Constraint Primary Key
);

--Creacion de la tabla municipio

create table municipio(
	codigo_m integer, --Identificador del municipio
	codigo_d_departamento integer  not null, --Llave foranea de la tabla referenciada departamento
	nombre_m varchar(30) not null, --Nombre del municipio
	numero_evaluados_m integer not null, --Numero de estudiantes que presentan la prueba ICFES en el municipio
	primary key(codigo_m), --Constraint Primary Key
	foreign key(codigo_d_departamento) references departamento(codigo_d) --Constraint de Foreign key
);

--Creacion de la tabla Colegio
--IMPORTANTE: REVISAR EL NOMBRE "COLEGIO"
create table colegio(
	codigo integer, --Identificador del colegio
	codigo_m_municipio integer not null, --Llave foranea de la tabla referenciada municipio
	nombre_colegio varchar(30) not null,--Nombre del colegio
	calendario varchar(10), --Cronograma del colegio
	genero varchar(10), --Tipo de sexo de los estudiantes
	localizacion varchar(10), --Ubicacion del establecimiento
	naturaleza varchar(10), --Establecimiento privado o publico
	primary key(codigo), --Constraint Primary key
	foreign key(codigo_m_municipio) references municipio(codigo_m) --Constraint Foreign Key
);

--Creacion de la tabla estudiante

create table estudiante(
	id_estudiante serial, --Identificador del estudiante
	sexo char not null, --Sexo del estudiante
	fecha_nacimiento date not null, --Fecha de nacimiento del estudiante
	estrato smallint, --Identificador del nivel socioeconomico en el que vive el estudiante
	codigo_colegio integer not null, --Llave foranea de la tabla referenciada colegio
	primary key(id_estudiante), --Constraint Primary key
	foreign key(codigo_colegio) references colegio(codigo) --Constraint Foreign key
);

--Creacion de la tabla examen

create table examen(
	id_examen varchar(30), --Identificador de un examen (prueba ICFES Saber-11)
	percentil integer not null, --Porcentaje de la poblacion a la que se supera por el puntaje en el examen
	puntaje_global integer not null, --El puntaje total obtenido en el examen
	periodo varchar(10) not null, --Año y semestre en el que se realiza la prueba
	puntaje_c_naturales integer not null, --Numero de puntos obtenidos en el area de Biologia, Quimica y Fisica
	puntaje_matematicas integer not null, --Numero de puntos obtenidos en el area de matematicas y razonamiento
	puntaje_sociales integer not null, --Numero de puntos obtenidos en el area de sociales y competencias cuidadanas
	puntaje_ingles integer not null, --Numero de puntos obtenidos en el area de ingles
	puntaje_lectura_critica integer not null, --Numero de puntos obtenidos en el area de Lectura Critica
	id_estudiante integer not null, --Llave foranea de la tabla referenciada estudiante
	primary key(id_examen), --Constraint Primary key
	foreign key(id_estudiante) references estudiante(id_estudiante) --Constraint Foreign key
);
