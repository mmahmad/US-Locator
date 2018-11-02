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
  id int AUTO_INCREMENT PRIMARY KEY,
  zipcode char(12) PRIMARY KEY UNIQUE NOT NULL,
  latitude char(20),
  longitude char(20),
  city_id int,
  state varchar (50),
  FOREIGN KEY (city_id) REFERENCES cities(id),
  FOREIGN KEY (state) REFERENCES states(name)
);

CREATE TABLE IF NOT EXISTS crime_stats(
  zipcode int NOT NULL PRIMARY KEY,
  violent int,
  non_violent int,
  theft int,
  murder int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(id)
);

CREATE TABLE IF NOT EXISTS home_stats(
  zipcode int NOT NULL PRIMARY KEY,
  median_home_value int,
  median_rent int,
  median_sq_ft int,
  value_appreciate_10_yrs int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(id)
);

CREATE TABLE IF NOT EXISTS literacy_stats(
  state varchar(50) PRIMARY KEY UNIQUE NOT NULL,
  avg_education_attainment int,
  number_of_schools int,
  number_of_unis int,
  FOREIGN KEY (state) REFERENCES states(name)
);

CREATE TABLE IF NOT EXISTS employment_stats(
  zipcode int PRIMARY KEY NOT NULL,
  median_household_salary int,
  unemployment_rate int,
  job_growth_1_yr int,
  job_growth_10_yrs int,
  FOREIGN KEY (zipcode) REFERENCES zipcodes(id)
);

CREATE TABLE IF NOT EXISTS weather_stats(
  zipcode_id int PRIMARY KEY NOT NULL,
  avg_temp FLOAT,
  min_monthly_lows FLOAT,
  max_monthly_highs FLOAT,
  FOREIGN KEY (zipcode_id) REFERENCES zipcodes(id)
);

create table if not exists users(
	id int primary key auto_increment,
    username varchar(50) unique not null,
    passwd varchar(100) not null,
    salt varchar(100) not null
    );
    
create table if not exists favorites(
    id int primary key auto_increment,
	user_id int not null,
    zipcode_id int,
    foreign key (user_id) references users(id),
    foreign key (zipcode_id) references zipcodes(id)
);