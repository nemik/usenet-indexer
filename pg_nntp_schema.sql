--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: gtrgm; Type: SHELL TYPE; Schema: public; Owner: nemik
--

CREATE TYPE gtrgm;


--
-- Name: gtrgm_in(cstring); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_in(cstring) RETURNS gtrgm
    AS '$libdir/pg_trgm', 'gtrgm_in'
    LANGUAGE c STRICT;


ALTER FUNCTION public.gtrgm_in(cstring) OWNER TO nemik;

--
-- Name: gtrgm_out(gtrgm); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_out(gtrgm) RETURNS cstring
    AS '$libdir/pg_trgm', 'gtrgm_out'
    LANGUAGE c STRICT;


ALTER FUNCTION public.gtrgm_out(gtrgm) OWNER TO nemik;

--
-- Name: gtrgm; Type: TYPE; Schema: public; Owner: nemik
--

CREATE TYPE gtrgm (
    INTERNALLENGTH = variable,
    INPUT = gtrgm_in,
    OUTPUT = gtrgm_out,
    ALIGNMENT = int4,
    STORAGE = plain
);


ALTER TYPE public.gtrgm OWNER TO nemik;

--
-- Name: difference(text, text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION difference(text, text) RETURNS integer
    AS '$libdir/fuzzystrmatch', 'difference'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.difference(text, text) OWNER TO nemik;

--
-- Name: dmetaphone(text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION dmetaphone(text) RETURNS text
    AS '$libdir/fuzzystrmatch', 'dmetaphone'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.dmetaphone(text) OWNER TO nemik;

--
-- Name: dmetaphone_alt(text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION dmetaphone_alt(text) RETURNS text
    AS '$libdir/fuzzystrmatch', 'dmetaphone_alt'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.dmetaphone_alt(text) OWNER TO nemik;

--
-- Name: gin_extract_trgm(text, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gin_extract_trgm(text, internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gin_extract_trgm'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gin_extract_trgm(text, internal) OWNER TO nemik;

--
-- Name: gin_extract_trgm(text, internal, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gin_extract_trgm(text, internal, internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gin_extract_trgm'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gin_extract_trgm(text, internal, internal) OWNER TO nemik;

--
-- Name: gin_trgm_consistent(internal, internal, text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gin_trgm_consistent(internal, internal, text) RETURNS internal
    AS '$libdir/pg_trgm', 'gin_trgm_consistent'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gin_trgm_consistent(internal, internal, text) OWNER TO nemik;

--
-- Name: gtrgm_compress(internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_compress(internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gtrgm_compress'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_compress(internal) OWNER TO nemik;

--
-- Name: gtrgm_consistent(gtrgm, internal, integer); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_consistent(gtrgm, internal, integer) RETURNS boolean
    AS '$libdir/pg_trgm', 'gtrgm_consistent'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_consistent(gtrgm, internal, integer) OWNER TO nemik;

--
-- Name: gtrgm_decompress(internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_decompress(internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gtrgm_decompress'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_decompress(internal) OWNER TO nemik;

--
-- Name: gtrgm_penalty(internal, internal, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_penalty(internal, internal, internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gtrgm_penalty'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.gtrgm_penalty(internal, internal, internal) OWNER TO nemik;

--
-- Name: gtrgm_picksplit(internal, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_picksplit(internal, internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gtrgm_picksplit'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_picksplit(internal, internal) OWNER TO nemik;

--
-- Name: gtrgm_same(gtrgm, gtrgm, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_same(gtrgm, gtrgm, internal) RETURNS internal
    AS '$libdir/pg_trgm', 'gtrgm_same'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_same(gtrgm, gtrgm, internal) OWNER TO nemik;

--
-- Name: gtrgm_union(bytea, internal); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION gtrgm_union(bytea, internal) RETURNS integer[]
    AS '$libdir/pg_trgm', 'gtrgm_union'
    LANGUAGE c IMMUTABLE;


ALTER FUNCTION public.gtrgm_union(bytea, internal) OWNER TO nemik;

--
-- Name: levenshtein(text, text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION levenshtein(text, text) RETURNS integer
    AS '$libdir/fuzzystrmatch', 'levenshtein'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.levenshtein(text, text) OWNER TO nemik;

--
-- Name: metaphone(text, integer); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION metaphone(text, integer) RETURNS text
    AS '$libdir/fuzzystrmatch', 'metaphone'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.metaphone(text, integer) OWNER TO nemik;

--
-- Name: set_limit(real); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION set_limit(real) RETURNS real
    AS '$libdir/pg_trgm', 'set_limit'
    LANGUAGE c STRICT;


ALTER FUNCTION public.set_limit(real) OWNER TO nemik;

--
-- Name: show_limit(); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION show_limit() RETURNS real
    AS '$libdir/pg_trgm', 'show_limit'
    LANGUAGE c STABLE STRICT;


ALTER FUNCTION public.show_limit() OWNER TO nemik;

--
-- Name: show_trgm(text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION show_trgm(text) RETURNS text[]
    AS '$libdir/pg_trgm', 'show_trgm'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.show_trgm(text) OWNER TO nemik;

--
-- Name: similarity(text, text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION similarity(text, text) RETURNS real
    AS '$libdir/pg_trgm', 'similarity'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.similarity(text, text) OWNER TO nemik;

--
-- Name: similarity_op(text, text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION similarity_op(text, text) RETURNS boolean
    AS '$libdir/pg_trgm', 'similarity_op'
    LANGUAGE c STABLE STRICT;


ALTER FUNCTION public.similarity_op(text, text) OWNER TO nemik;

--
-- Name: soundex(text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION soundex(text) RETURNS text
    AS '$libdir/fuzzystrmatch', 'soundex'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.soundex(text) OWNER TO nemik;

--
-- Name: text_soundex(text); Type: FUNCTION; Schema: public; Owner: nemik
--

CREATE FUNCTION text_soundex(text) RETURNS text
    AS '$libdir/fuzzystrmatch', 'soundex'
    LANGUAGE c IMMUTABLE STRICT;


ALTER FUNCTION public.text_soundex(text) OWNER TO nemik;

--
-- Name: %; Type: OPERATOR; Schema: public; Owner: nemik
--

CREATE OPERATOR % (
    PROCEDURE = similarity_op,
    LEFTARG = text,
    RIGHTARG = text,
    COMMUTATOR = %,
    RESTRICT = contsel,
    JOIN = contjoinsel
);


ALTER OPERATOR public.% (text, text) OWNER TO nemik;

--
-- Name: gin_trgm_ops; Type: OPERATOR CLASS; Schema: public; Owner: nemik
--

CREATE OPERATOR CLASS gin_trgm_ops
    FOR TYPE text USING gin AS
    STORAGE integer ,
    OPERATOR 1 %(text,text) RECHECK ,
    FUNCTION 1 btint4cmp(integer,integer) ,
    FUNCTION 2 gin_extract_trgm(text,internal) ,
    FUNCTION 3 gin_extract_trgm(text,internal,internal) ,
    FUNCTION 4 gin_trgm_consistent(internal,internal,text);


ALTER OPERATOR CLASS public.gin_trgm_ops USING gin OWNER TO nemik;

--
-- Name: gist_trgm_ops; Type: OPERATOR CLASS; Schema: public; Owner: nemik
--

CREATE OPERATOR CLASS gist_trgm_ops
    FOR TYPE text USING gist AS
    STORAGE gtrgm ,
    OPERATOR 1 %(text,text) ,
    FUNCTION 1 gtrgm_consistent(gtrgm,internal,integer) ,
    FUNCTION 2 gtrgm_union(bytea,internal) ,
    FUNCTION 3 gtrgm_compress(internal) ,
    FUNCTION 4 gtrgm_decompress(internal) ,
    FUNCTION 5 gtrgm_penalty(internal,internal,internal) ,
    FUNCTION 6 gtrgm_picksplit(internal,internal) ,
    FUNCTION 7 gtrgm_same(gtrgm,gtrgm,internal);


ALTER OPERATOR CLASS public.gist_trgm_ops USING gist OWNER TO nemik;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: nntp; Tablespace: 
--

CREATE TABLE articles (
    id text NOT NULL,
    group_id bigint,
    subject text,
    poster text,
    date bigint,
    "time" timestamp without time zone
);


ALTER TABLE public.articles OWNER TO nntp;

--
-- Name: file_group_seq; Type: SEQUENCE; Schema: public; Owner: nntp
--

CREATE SEQUENCE file_group_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.file_group_seq OWNER TO nntp;

--
-- Name: file_group; Type: TABLE; Schema: public; Owner: nntp; Tablespace: 
--

CREATE TABLE file_group (
    id bigint DEFAULT nextval('file_group_seq'::regclass) NOT NULL,
    file_id bigint,
    group_id bigint
);


ALTER TABLE public.file_group OWNER TO nntp;

--
-- Name: files_seq; Type: SEQUENCE; Schema: public; Owner: nntp
--

CREATE SEQUENCE files_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.files_seq OWNER TO nntp;

--
-- Name: files; Type: TABLE; Schema: public; Owner: nntp; Tablespace: 
--

CREATE TABLE files (
    id bigint DEFAULT nextval('files_seq'::regclass) NOT NULL,
    subject text,
    name text,
    poster text,
    parts_total integer,
    date bigint,
    "time" timestamp without time zone
);


ALTER TABLE public.files OWNER TO nntp;

--
-- Name: groups_seq; Type: SEQUENCE; Schema: public; Owner: nntp
--

CREATE SEQUENCE groups_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.groups_seq OWNER TO nntp;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: nntp; Tablespace: 
--

CREATE TABLE groups (
    id bigint DEFAULT nextval('groups_seq'::regclass) NOT NULL,
    name text,
    last_article bigint
);


ALTER TABLE public.groups OWNER TO nntp;

--
-- Name: parts; Type: TABLE; Schema: public; Owner: nntp; Tablespace: 
--

CREATE TABLE parts (
    id text NOT NULL,
    file_id bigint,
    bytes bigint,
    number integer
);


ALTER TABLE public.parts OWNER TO nntp;

--
-- Name: articles_pkey; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (id);


--
-- Name: file_group_pkey; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY file_group
    ADD CONSTRAINT file_group_pkey PRIMARY KEY (id);


--
-- Name: files_pkey; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: id; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY parts
    ADD CONSTRAINT id PRIMARY KEY (id);


--
-- Name: parts_id_key; Type: CONSTRAINT; Schema: public; Owner: nntp; Tablespace: 
--

ALTER TABLE ONLY parts
    ADD CONSTRAINT parts_id_key UNIQUE (id);


--
-- Name: files_id_idx; Type: INDEX; Schema: public; Owner: nntp; Tablespace: 
--

CREATE INDEX files_id_idx ON parts USING btree (file_id);


--
-- Name: files_name_trigram_index; Type: INDEX; Schema: public; Owner: nntp; Tablespace: 
--

CREATE INDEX files_name_trigram_index ON files USING gist (subject gist_trgm_ops);


--
-- Name: articles_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nntp
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT articles_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- Name: file_group_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nntp
--

ALTER TABLE ONLY file_group
    ADD CONSTRAINT file_group_file_id_fkey FOREIGN KEY (file_id) REFERENCES files(id);


--
-- Name: file_group_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nntp
--

ALTER TABLE ONLY file_group
    ADD CONSTRAINT file_group_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- Name: parts_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nntp
--

ALTER TABLE ONLY parts
    ADD CONSTRAINT parts_file_id_fkey FOREIGN KEY (file_id) REFERENCES files(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

