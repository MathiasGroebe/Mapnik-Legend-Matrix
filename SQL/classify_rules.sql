UPDATE mapnik_styles
SET OwnStyleGroup = 'landcover'
WHERE StyleName LIKE 'landcover%' OR StyleName LIKE 'icesheet%' OR StyleName LIKE 'landuse%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'water'
WHERE StyleName LIKE 'water%' OR StyleName LIKE 'ocean%' OR StyleName LIKE 'marinas%' OR StyleName LIKE 'springs' OR StyleName LIKE 'piers%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'buildings'
WHERE StyleName LIKE 'buildings%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'roads'
WHERE StyleName LIKE 'bridge%' OR StyleName LIKE 'tunnels%' OR StyleName LIKE 'area-barriers' OR StyleName LIKE 'ferry%' OR StyleName LIKE 'turning-circle' 
OR StyleName LIKE 'highway%' OR StyleName LIKE 'roads%' OR StyleName LIKE 'junctions' OR StyleName LIKE 'paths%' OR StyleName LIKE 'railway%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'boundary'
WHERE StyleName LIKE 'admin%' OR StyleName LIKE 'tourism-boundary' OR StyleName LIKE 'necountries' OR StyleName LIKE 'protected-areas%' OR StyleName in ('country-names', 'capital-names', 'state-names');

UPDATE mapnik_styles
SET OwnStyleGroup = 'terrain'
WHERE StyleName LIKE 'cliffs%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'arial'
WHERE StyleName LIKE 'aerialways' OR StyleName LIKE 'guideways' OR StyleName LIKE 'aeroways%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'power'
WHERE StyleName LIKE 'power%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'points'
WHERE StyleName LIKE 'trees%' OR StyleName LIKE 'entrances' OR StyleName LIKE 'stations' OR StyleName LIKE 'addresses';

UPDATE mapnik_styles
SET OwnStyleGroup = 'placenames'
WHERE StyleName LIKE 'placenames%';

UPDATE mapnik_styles
SET OwnStyleGroup = 'amenity'
WHERE StyleName LIKE 'amenity%';
