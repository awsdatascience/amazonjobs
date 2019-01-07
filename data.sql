create schema amazon;

select nspname from pg_catalog.pg_namespace;
-- Amazon data
CREATE TABLE amazon.amazonjobs (
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
-- CREATE TABLE amazon.amazonjobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

SELECT * FROM pg_catalog.pg_tables;

SET CLIENT_ENCODING TO 'utf8';

\COPY amazon.amazonjobs FROM 'C:/Users/gouzouni/PycharmProjects/amazonjobs/amazon.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  amazon.amazonjobs_2
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
from amazon.amazonjobs am;
-- create table amazon.amazonjobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from amazon.amazonjobs am;
--Apple data

CREATE TABLE amazon.applejobs (
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
-- CREATE TABLE amazon.applejobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

SELECT * FROM pg_catalog.pg_tables;

SET CLIENT_ENCODING TO 'utf8';

\COPY amazon.applejobs FROM 'C:/Users/VN689M/apple.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  amazon.applejobs_2
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
from amazon.applejobs am;
-- create table amazon.applejobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from amazon.applejobs am;

--Facebook data

CREATE TABLE amazon.facebookjobs (
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
-- CREATE TABLE amazon.facebookjobs ( job_id text NULL, title text NULL, department text NULL, "location" text NULL, to_date date NULL, to_timestamp timestamp NULL, url text NULL, company_intro text NULL, role_description text NULL, listings text NULL ); 

SELECT * FROM pg_catalog.pg_tables;

SET CLIENT_ENCODING TO 'utf8';

\COPY amazon.facebookjobs FROM 'C:/Users/VN689M/facebook.csv' WITH DELIMITER ‘,’ CSV HEADER;

create table  amazon.facebookjobs_2
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
from amazon.facebookjobs am;
-- create table amazon.facebookjobs_2 as select am.job_id, am.title, am.department, am."location", am.to_date, am.to_timestamp, am.url, am.company_intro, am.role_description, replace(am.listings, '\', ' back_slsh ') listings from amazon.facebookjobs am;
