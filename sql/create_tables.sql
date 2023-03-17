CREATE SCHEMA content;
CREATE SCHEMA users;
ALTER ROLE app SET search_path TO users,content,public;
