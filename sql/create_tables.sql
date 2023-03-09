CREATE SCHEMA content;
CREATE SCHEMA invoice;
ALTER ROLE app SET search_path TO users,content,invoice,public;
