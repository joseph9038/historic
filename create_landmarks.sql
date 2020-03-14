
CREATE TABLE landmarks (id SERIAL PRIMARY KEY, name varchar(255) NOT NULL, geom geometry(point,2163) );

CREATE INDEX idx_landmarks ON landmarks USING gist(geom);