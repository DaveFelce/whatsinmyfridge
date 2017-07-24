--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3
\connect whatsinmyfridge

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: recipe; Type: TABLE; Schema: public; Owner: whatsinmyfridge
--

CREATE TABLE recipe (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    url character varying(200) NOT NULL,
    ingredients character varying(2000) NOT NULL
);


ALTER TABLE recipe OWNER TO whatsinmyfridge;

--
-- Name: recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: whatsinmyfridge
--

CREATE SEQUENCE recipe_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE recipe_id_seq OWNER TO whatsinmyfridge;

--
-- Data for Name: recipe; Type: TABLE DATA; Schema: public; Owner: whatsinmyfridge
--

COPY recipe (id, name, url, ingredients) FROM stdin;
\.


--
-- Name: recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: whatsinmyfridge
--

SELECT pg_catalog.setval('recipe_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--
