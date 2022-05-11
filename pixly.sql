from app import db
from models import User, Message, Follows, Likes

DROP DATABASE IF EXISTS pixly;
CREATE DATABASE pixly;
\connect pixly;

CREATE TABLE customers (
    id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    image_key text NOT NULL,
    image_url text NOT NULL,
    image_location text
    model text
    time_stamp text
);

-- def getmetadata:
--     SELECT location,model,time from photos where id = $1

-- #get metadata from upload-front end




-- def postimage:
--     post logic
--     insert into photos location = url, time ,model

