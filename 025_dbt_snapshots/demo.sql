# %%

use database demo;
use schema core;

# %%

-- reset state
create or replace table students (
  id           number not null,
  name         string not null,
  house        string not null,
  last_updated timestamp not null
);

insert into students values
(1, 'Harry', 'Gryffindor', current_timestamp()),
(2, 'Draco', 'Slytherin', current_timestamp());

select * from demo.core.students;








# %%

-- check source and snapshot
select * from demo.core.students;
select * from demo.snapshot.students_snapshot
order by id, dbt_valid_from;









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


# %%

# %%

-- clean up
drop table if exists demo.core.students;
drop table if exists demo.snapshot.students_snapshot;
drop schema if exists demo.snapshot;
