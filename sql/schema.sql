--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Debian 13.2-1.pgdg100+1)
-- Dumped by pg_dump version 13.2

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

CREATE TABLE public.mortems (
    id integer NOT NULL,
    mortem_name character varying(100) NOT NULL,
    mortem_impact character varying(20) NOT NULL,
    mortem_url character varying(16) NOT NULL,
    mortem_content text NOT NULL,
    mortem_resolution text,
    mortem_tags text,
    mortem_created timestamp without time zone NOT NULL,
    mortem_updated timestamp without time zone NOT NULL,
    user_id integer NOT NULL
);



--
--

CREATE SEQUENCE public.mortems_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE public.mortems_id_seq OWNED BY public.mortems.id;


--
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(10)
);



--
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
--

CREATE TABLE public.support (
    id integer NOT NULL,
    support_subject character varying(100) NOT NULL,
    support_content text NOT NULL,
    support_created timestamp without time zone NOT NULL,
    support_attach bytea,
    user_id integer NOT NULL
);



--
--

CREATE SEQUENCE public.support_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE public.support_id_seq OWNED BY public.support.id;


--
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);



--
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
--

CREATE TABLE public.users (
    id integer NOT NULL,
    user_name character varying(20) NOT NULL,
    user_email character varying(20) NOT NULL,
    user_password character varying(100) NOT NULL,
    user_image character varying(20)
);



--
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
--

ALTER TABLE ONLY public.mortems ALTER COLUMN id SET DEFAULT nextval('public.mortems_id_seq'::regclass);


--
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
--

ALTER TABLE ONLY public.support ALTER COLUMN id SET DEFAULT nextval('public.support_id_seq'::regclass);


--
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
--

ALTER TABLE ONLY public.mortems
    ADD CONSTRAINT mortems_pkey PRIMARY KEY (id);


--
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
--

ALTER TABLE ONLY public.support
    ADD CONSTRAINT support_pkey PRIMARY KEY (id);


--
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_email_key UNIQUE (user_email);


--
--

ALTER TABLE ONLY public.mortems
    ADD CONSTRAINT mortems_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
--

ALTER TABLE ONLY public.support
    ADD CONSTRAINT support_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

