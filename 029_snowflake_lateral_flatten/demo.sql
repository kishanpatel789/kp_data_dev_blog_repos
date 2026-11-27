# %%

alter warehouse compute_wh resume;

use database demo;
use schema core;

# %%

create or replace table students (
  id           number not null,
  name         string not null,
  house_id     number,
  wand         object,
  courses      array
);

insert into students (id, name, house_id, wand, courses)
select
  1,
  'Harry Potter',
  1,
  parse_json('{"wood": "Holly", "core": "Phoenix Feather", "length": 11}'),
  parse_json('["Defense Against the Dark Arts", "Charms"]')
union
select
  2,
  'Hermione Granger',
  1,
  parse_json('{"wood": "Vine", "core": "Dragon Heartstring", "length": 10.75}'),
  parse_json('["Arithmancy", "Transfiguration", "Charms"]')
union
select
  3,
  'Draco Malfoy',
  4,
  parse_json('{"wood": "Hawthorn", "core": "Unicorn Hair", "length": 10}'),
  parse_json('["Potions"]')
;

select id, name, wand, courses from students;

# %%

create or replace table houses (
  id                number not null,
  house_name        string not null,
  primary_color     string,
  secondary_color   string
);

insert into houses (id, house_name, primary_color, secondary_color)
select 1, 'Gryffindor', 'Red', 'Gold'
union
select 2, 'Hufflepuff', 'Yellow', 'Black'
union
select 3, 'Ravenclaw', 'Blue', 'Bronze'
union
select 4, 'Slytherin', 'Green', 'Silver';

select * from houses;

# %%

create or replace table students_nested (
  id           number not null,
  name         string not null,
  courses      array
);

insert into students_nested (id, name, courses)
select
  1,
  'Harry Potter',
  parse_json('[{"name": "Defense Against the Dark Arts", "assignments": ["Read chapter on Boggarts", "Write essay on werewolves"]},
    {"name": "Potions", "assignments": ["Write essay on moonstone use in potion-making"]}]')
union
select
  2,
  'Hermione Granger',
  parse_json('[{"name": "Arithmancy", "assignments": ["Update number chart", "Read textbook chapter 9"]}]')
;

select * from students_nested;




# %%

-- show table
select id, name, wand, courses from students;










-- expand course
select s.id, s.name, c.value::string as course
from students as s,
lateral flatten(s.courses) as c;










-- extract wand characteristics
select s.id, s.name, w.key, w.value::string as value
from students as s,
lateral flatten(s.wand) as w;











# %%
-- flatten only

select *
from table(
  flatten(input => parse_json('["Harry", "Hermione"]'))
);

select *
from table(
  flatten(input => parse_json('{"core": "Phoenix Feather", "length": 11}'))
);


# %%
-- lateral only

select id, name, house_id from students;

select * from houses;

select s.id, s.name, h2.*
from students as s,
lateral(select * from houses h where h.id = s.house_id) as h2;





select s.id, s.name, h.*
from students s inner join houses h where h.id = s.house_id;





# %%
-- back to lateral flatten

select s.id, s.name, c.value::string as course
from students as s,
lateral flatten(s.courses) as c;








# %%
-- advanced: lateral chains

select * from students_nested;






















-- scratch
select id, name, f1.value as course
from students_nested s,
lateral flatten(s.courses) f1;

select id, name, f1.value:name::string as course, f1.value:assignments as assignment
from students_nested s,
lateral flatten(s.courses) f1;

select id, name, f1.value:name::string course, f2.value::string assignment
from students_nested s,
lateral flatten(s.courses) f1,
lateral flatten(f1.value:assignments) f2;
