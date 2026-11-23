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

-- extract course
select s.id, s.name, c.value::string as course
from students as s,
lateral flatten(input => s.courses) as c;

-- extract wand wood
select s.id, s.name, w.value::string as wand_wood
from students as s,
lateral flatten(input => s.wand) as w
where w.key = 'wood';

-- extract wand characteristics
select s.id, s.name, w.key, w.value::string as value
from students as s,
lateral flatten(input => s.wand) as w;


select s.id, s.name, s.wand:wood::string as wand_wood
from students as s;

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
from students s, lateral(select * from houses h where h.id = s.house_id) h2;


select s.id, s.name, h.*
from students s inner join houses h where h.id = s.house_id;
