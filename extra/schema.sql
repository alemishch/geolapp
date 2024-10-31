--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: metasomatic_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metasomatic_types (
    id integer NOT NULL,
    sample_id integer,
    type_name character varying(255),
    degree_of_metasomatic_working numeric
);


ALTER TABLE public.metasomatic_types OWNER TO postgres;

--
-- Name: metasomatic_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metasomatic_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.metasomatic_types_id_seq OWNER TO postgres;

--
-- Name: metasomatic_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metasomatic_types_id_seq OWNED BY public.metasomatic_types.id;


--
-- Name: ore_compositions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ore_compositions (
    id integer NOT NULL,
    sample_id integer,
    mineral_name character varying(255),
    composition_type_main character varying(50),
    rare boolean,
    percentage_volume numeric
);


ALTER TABLE public.ore_compositions OWNER TO postgres;

--
-- Name: ore_compositions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ore_compositions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ore_compositions_id_seq OWNER TO postgres;

--
-- Name: ore_compositions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ore_compositions_id_seq OWNED BY public.ore_compositions.id;


--
-- Name: photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photos (
    id integer NOT NULL,
    sample_id integer,
    macro_photo text,
    thin_section_photo_with_analyzer text,
    thin_section_photo_without_analyzer text,
    normal_light_photo text,
    reflected_light_photo text
);


ALTER TABLE public.photos OWNER TO postgres;

--
-- Name: photos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.photos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.photos_id_seq OWNER TO postgres;

--
-- Name: photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.photos_id_seq OWNED BY public.photos.id;


--
-- Name: rock_compositions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rock_compositions (
    id integer NOT NULL,
    sample_id integer,
    mineral_name character varying(255),
    composition_type_main character varying(50),
    accessory_type boolean,
    percentage_volume numeric
);


ALTER TABLE public.rock_compositions OWNER TO postgres;

--
-- Name: rock_compositions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rock_compositions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rock_compositions_id_seq OWNER TO postgres;

--
-- Name: rock_compositions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rock_compositions_id_seq OWNED BY public.rock_compositions.id;


--
-- Name: samples; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samples (
    id integer NOT NULL,
    sample_number character varying(50),
    well_id integer,
    rock_type_main character varying(255),
    complex character varying(255),
    full_rock_name text,
    structure text,
    macro_description text,
    ore_mineralization text,
    texture text,
    micro_description text
);


ALTER TABLE public.samples OWNER TO postgres;

--
-- Name: samples_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.samples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.samples_id_seq OWNER TO postgres;

--
-- Name: samples_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.samples_id_seq OWNED BY public.samples.id;


--
-- Name: wells; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wells (
    id integer NOT NULL,
    well character varying(255),
    depth_m numeric,
    ore_zone character varying(255),
    code character varying(50)
);


ALTER TABLE public.wells OWNER TO postgres;

--
-- Name: wells_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.wells_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wells_id_seq OWNER TO postgres;

--
-- Name: wells_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.wells_id_seq OWNED BY public.wells.id;


--
-- Name: metasomatic_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metasomatic_types ALTER COLUMN id SET DEFAULT nextval('public.metasomatic_types_id_seq'::regclass);


--
-- Name: ore_compositions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ore_compositions ALTER COLUMN id SET DEFAULT nextval('public.ore_compositions_id_seq'::regclass);


--
-- Name: photos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos ALTER COLUMN id SET DEFAULT nextval('public.photos_id_seq'::regclass);


--
-- Name: rock_compositions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rock_compositions ALTER COLUMN id SET DEFAULT nextval('public.rock_compositions_id_seq'::regclass);


--
-- Name: samples id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples ALTER COLUMN id SET DEFAULT nextval('public.samples_id_seq'::regclass);


--
-- Name: wells id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wells ALTER COLUMN id SET DEFAULT nextval('public.wells_id_seq'::regclass);


--
-- Name: metasomatic_types metasomatic_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metasomatic_types
    ADD CONSTRAINT metasomatic_types_pkey PRIMARY KEY (id);


--
-- Name: ore_compositions ore_compositions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ore_compositions
    ADD CONSTRAINT ore_compositions_pkey PRIMARY KEY (id);


--
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (id);


--
-- Name: rock_compositions rock_compositions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rock_compositions
    ADD CONSTRAINT rock_compositions_pkey PRIMARY KEY (id);


--
-- Name: samples samples_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples
    ADD CONSTRAINT samples_pkey PRIMARY KEY (id);


--
-- Name: wells wells_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wells
    ADD CONSTRAINT wells_pkey PRIMARY KEY (id);


--
-- Name: metasomatic_types metasomatic_types_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metasomatic_types
    ADD CONSTRAINT metasomatic_types_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.samples(id);


--
-- Name: ore_compositions ore_compositions_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ore_compositions
    ADD CONSTRAINT ore_compositions_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.samples(id);


--
-- Name: photos photos_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.samples(id);


--
-- Name: rock_compositions rock_compositions_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rock_compositions
    ADD CONSTRAINT rock_compositions_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.samples(id);


--
-- Name: samples samples_well_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples
    ADD CONSTRAINT samples_well_id_fkey FOREIGN KEY (well_id) REFERENCES public.wells(id);


--
-- PostgreSQL database dump complete
--

