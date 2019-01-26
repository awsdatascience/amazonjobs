create schema datascience;

-- select nspname from pg_catalog.pg_namespace;

-- Amazon data
CREATE TABLE datascience.amazonjobs (
	job_id text NULL,
	title text NULL,
	department text NULL,
	"location" text NULL,
	to_date date NULL,
	to_timestamp timestamp NULL,
	url text NULL,
	company_intro text NULL,
	role_description text NULL,
	listings text NULL
);
-- CREATE TABLE datascience.amazonjobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

-- SELECT * FROM pg_catalog.pg_tables;

SET CLIENT_ENCODING TO 'utf8';

\COPY datascience.amazonjobs FROM '~/PycharmProjects/amazonjobs/amazon.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  datascience.amazonjobs_2
as select 
	am.job_id,
	am.title,
	am.department,
	am."location",
	am.to_date,
	am.to_timestamp,
	am.url,
	am.company_intro,
	am.role_description,
	replace(am.listings, '\', ' back_slsh ') listings
from datascience.amazonjobs am;
		
-- create table datascience.amazonjobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from datascience.amazonjobs am;

-- Apple data
CREATE TABLE datascience.applejobs (
	job_id text NULL,
	title text NULL,
	department text NULL,
	"location" text NULL,
	to_date date NULL,
	to_timestamp timestamp NULL,
	url text NULL,
	company_intro text NULL,
	role_description text NULL,
	listings text NULL
);
-- CREATE TABLE datascience.applejobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

-- SELECT * FROM pg_catalog.pg_tables;

\COPY datascience.applejobs FROM '~/apple.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  datascience.applejobs_2
as select 
	am.job_id,
	am.title,
	am.department,
	am."location",
	am.to_date,
	am.to_timestamp,
	am.url,
	am.company_intro,
	am.role_description,
	replace(am.listings, '\', ' back_slsh ') listings
from datascience.applejobs am;
-- create table datascience.applejobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from datascience.applejobs am;

--Facebook data

CREATE TABLE datascience.facebookjobs (
	job_id text NULL,
	title text NULL,
	department text NULL,
	"location" text NULL,
	to_date date NULL,
	to_timestamp timestamp NULL,
	url text NULL,
	company_intro text NULL,
	role_description text NULL,
	listings text NULL
);
-- CREATE TABLE datascience.facebookjobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

-- SELECT * FROM pg_catalog.pg_tables;

\COPY datascience.facebookjobs FROM '~/facebook.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  datascience.facebookjobs_2
as select 
	am.job_id,
	am.title,
	am.department,
	am."location",
	am.to_date,
	am.to_timestamp,
	am.url,
	am.company_intro,
	am.role_description,
	replace(am.listings, '\', ' back_slsh ') listings
from datascience.facebookjobs am;
-- create table datascience.facebookjobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from datascience.facebookjobs am;
