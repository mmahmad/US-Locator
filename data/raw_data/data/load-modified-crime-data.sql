-- DROP TABLE county_crime_data;

CREATE TABLE if not exists county_crime_data (
	id int primary key auto_increment,
    county varchar(40),
    state_code char(2),
    violent_crimes_total int,
    murders int,
    rapes int,
    robberies int,
    assaults int,
    burglaries int,
    larceny_thefts int,
    vehicle_thefts int
);

LOAD DATA LOCAL INFILE '/Volumes/Media/OneDrive - University of Illinois - Urbana/Fall2018/411/Project/Final/data/modified_crime_data.csv' 
INTO TABLE county_crime_data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(county, state_code, @v3, @v4, @v5 , @v6, @v7, @v8, @v9, @v10)
SET
violent_crimes_total = nullif(@v3,''),
murders = nullif(@v4,''),
rapes = nullif(@v5,''),
robberies = nullif(@v6,''),
assaults = nullif(@v7,''),
burglaries = nullif(@v8,''),
larceny_thefts = nullif(@v9,''),
vehicle_thefts = nullif(@v10,'')
;

-- select * from county_crime_data;