CREATE OR REPLACE FUNCTION landmarks_by_proximity(DEC, DEC, INT, INT)
RETURNS SETOF landmarks
AS $$
BEGIN
    RETURN QUERY SELECT id, name, coordinates
        FROM landmarks CROSS JOIN (
            SELECT ST_Point($2,$1)::geography AS ref_geog
        ) AS r
        WHERE ST_DWithin(coordinates, ref_geog, $3)
        ORDER BY ST_Distance(coordinates, ref_geog)
        LIMIT $4;
END;
$$ LANGUAGE plpgsql;

-- SELECT name FROM landmarks CROSS JOIN (SELECT ST_Point(-122.40659186274999,37.797583811500004)::geography AS ref_geog) AS r WHERE ST_DWithin(coordinates, ref_geog, 100000) ORDER BY ST_Distance(coordinates, ref_geog) LIMIT 10;