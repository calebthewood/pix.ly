

DROP DATABASE IF EXISTS pixly;
CREATE DATABASE pixly;
\connect pixly;

CREATE TABLE images (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    image_key text NOT NULL,
    image_url text NOT NULL,
    height text,
    width text
)

CREATE TABLE metadata (
    image_type text NOT NULL,
    image_value text NOT NULL,
    image_id FOREIGN KEY
)

-- def getmetadata:
--     SELECT location,model,time from photos where id = $1

-- #get metadata from upload-front end




-- def postimage:
--     post logic
--     insert into photos location = url, time ,model

