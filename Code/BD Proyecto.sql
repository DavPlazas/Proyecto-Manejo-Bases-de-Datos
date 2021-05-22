-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.2
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: new_database | type: DATABASE --
-- -- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database;
-- -- ddl-end --
-- 

-- object: public.estudiante | type: TABLE --
-- DROP TABLE IF EXISTS public.estudiante CASCADE;
CREATE TABLE public.estudiante (
	id_estudiante integer NOT NULL,
	fecha_nacimiento date NOT NULL,
	estrato smallint,
	sexo char NOT NULL,
	codigo_colegio varchar(15) NOT NULL,
	CONSTRAINT estudiante_pk PRIMARY KEY (id_estudiante)

);
-- ddl-end --
-- ALTER TABLE public.estudiante OWNER TO postgres;
-- ddl-end --

-- object: public.examen | type: TABLE --
-- DROP TABLE IF EXISTS public.examen CASCADE;
CREATE TABLE public.examen (
	id_examen varchar(30) NOT NULL,
	percentil integer NOT NULL,
	puntaje_global integer NOT NULL,
	periodo varchar(10) NOT NULL,
	puntaje_c_naturales integer NOT NULL,
	puntaje_matematicas integer NOT NULL,
	puntaje_sociales integer NOT NULL,
	puntaje_ingles integer,
	puntaje_lectura_critica integer NOT NULL,
	id_estudiante_estudiante integer NOT NULL,
	CONSTRAINT examen_pk PRIMARY KEY (id_examen)

);
-- ddl-end --
-- ALTER TABLE public.examen OWNER TO postgres;
-- ddl-end --

-- object: public.colegio | type: TABLE --
-- DROP TABLE IF EXISTS public.colegio CASCADE;
CREATE TABLE public.colegio (
	codigo varchar(15) NOT NULL,
	nombre_colegio varchar(120) NOT NULL,
	calendario varchar(10),
	genero varchar(10),
	localizacion varchar(10),
	naturaleza varchar(10),
	codigo_m_municipio integer NOT NULL,
	CONSTRAINT colegio_pk PRIMARY KEY (codigo)

);
-- ddl-end --
-- ALTER TABLE public.colegio OWNER TO postgres;
-- ddl-end --

-- object: public.municipio | type: TABLE --
-- DROP TABLE IF EXISTS public.municipio CASCADE;
CREATE TABLE public.municipio (
	codigo_m integer NOT NULL,
	nombre_m varchar(30) NOT NULL,
	numero_evaluados_m integer NOT NULL,
	codigo_d_departamento integer NOT NULL,
	CONSTRAINT municipio_pk PRIMARY KEY (codigo_m)

);
-- ddl-end --
-- ALTER TABLE public.municipio OWNER TO postgres;
-- ddl-end --

-- object: public.departamento | type: TABLE --
-- DROP TABLE IF EXISTS public.departamento CASCADE;
CREATE TABLE public.departamento (
	codigo_d integer NOT NULL,
	nombre_d varchar(30) NOT NULL,
	numero_evaluados_d integer NOT NULL,
	CONSTRAINT departamento_pk PRIMARY KEY (codigo_d)

);
-- ddl-end --
-- ALTER TABLE public.departamento OWNER TO postgres;
-- ddl-end --

-- object: colegio_fk | type: CONSTRAINT --
-- ALTER TABLE public.estudiante DROP CONSTRAINT IF EXISTS colegio_fk CASCADE;
ALTER TABLE public.estudiante ADD CONSTRAINT colegio_fk FOREIGN KEY (codigo_colegio)
REFERENCES public.colegio (codigo) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: municipio_fk | type: CONSTRAINT --
-- ALTER TABLE public.colegio DROP CONSTRAINT IF EXISTS municipio_fk CASCADE;
ALTER TABLE public.colegio ADD CONSTRAINT municipio_fk FOREIGN KEY (codigo_m_municipio)
REFERENCES public.municipio (codigo_m) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: departamento_fk | type: CONSTRAINT --
-- ALTER TABLE public.municipio DROP CONSTRAINT IF EXISTS departamento_fk CASCADE;
ALTER TABLE public.municipio ADD CONSTRAINT departamento_fk FOREIGN KEY (codigo_d_departamento)
REFERENCES public.departamento (codigo_d) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: estudiante_fk | type: CONSTRAINT --
-- ALTER TABLE public.examen DROP CONSTRAINT IF EXISTS estudiante_fk CASCADE;
ALTER TABLE public.examen ADD CONSTRAINT estudiante_fk FOREIGN KEY (id_estudiante_estudiante)
REFERENCES public.estudiante (id_estudiante) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


