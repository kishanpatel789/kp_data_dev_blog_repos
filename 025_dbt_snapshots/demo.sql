# %%

use database demo;
use schema core;

alter warehouse compute_wh resume;

alter warehouse compute_wh suspend;

# %%

-- reset state
create or replace table students (
  id           number not null,
  name         string not null,
  house        string not null,
  last_updated timestamp not null
);

delete from students;

insert into students values
(1, 'Harry', 'Gryffindor', current_timestamp()),
(2, 'Draco', 'Slytherin', current_timestamp());

# %%

-- new record
insert into students values
(3, 'Hermione', 'Gryffindor', current_timestamp());


# %%

-- modify record
update students
set name = 'hARRy', last_updated = current_timestamp()
where id = 1;

# %%

-- delete record
delete from students
where id = 2;

select * from students;

# %%

-- show tables in schema demo.core;
