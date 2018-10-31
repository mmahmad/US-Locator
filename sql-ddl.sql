USE ebdb;

CREATE TABLE IF NOT EXISTS political_parties(
  name varchar (50) PRIMARY KEY UNIQUE NOT NULL, 
  current_status bool NOT NULL
);

CREATE TABLE IF NOT EXISTS states(
  name varchar (50) PRIMARY KEY UNIQUE NOT NULL,
  state_code char(2), 
  capital varchar (50),
  total_area bigint,
  current_political_party varchar (50),
  FOREIGN KEY (current_political_party) REFERENCES political_parties(name)
);

CREATE TABLE IF NOT EXISTS cities(
  id int PRIMARY KEY UNIQUE NOT NULL AUTO_INCREMENT,
  name varchar (50) NOT NULL, 
  state varchar (50) NOT NULL,
  FOREIGN KEY (state) REFERENCES states(name)
);

CREATE TABLE IF NOT EXISTS zipcodes(
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  latitude char(20),
  longitude char(20),
  city_id int,
  state varchar (50),
  FOREIGN KEY (city_id) REFERENCES cities(id),
  FOREIGN KEY (state) REFERENCES states(name)
);

CREATE TABLE IF NOT EXISTS crime_stats(
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  violent int,
  non_violent int,
  theft int,
  murder int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(zipcode)
);

CREATE TABLE IF NOT EXISTS home_stats(
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  median_home_value int,
  median_rent int,
  median_sq_ft int,
  value_appreciate_10_yrs int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(zipcode)
);

CREATE TABLE IF NOT EXISTS literacy_stats(
  state varchar(50) PRIMARY KEY UNIQUE NOT NULL,
  avg_education_attainment int,
  number_of_schools int,
  number_of_unis int,
  FOREIGN KEY (state) REFERENCES states(name)
);

CREATE TABLE IF NOT EXISTS employment_stats(
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  median_household_salary int,
  unemployment_rate int,
  job_growth_1_yr int,
  job_growth_10_yrs int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(zipcode)
);

CREATE TABLE IF NOT EXISTS weather_stats(
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  avg_summer_lows int,
  avg_summer_highs int,
  avg_winter_lows int,
  avg_winter_highs int,
  avg_precipitation_per_yr int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(zipcode)
);