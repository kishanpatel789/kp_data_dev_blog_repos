# %%
use database demo;
use schema core;

alter warehouse compute_wh resume;

alter warehouse compute_wh suspend;

create
or replace table students (
id number not null,
name string not null,
year number not null,
house string not null,
last_updated timestamp not null
);

select * from demo.core.students;

select * from demo.core.my_first_dbt_model;


show tables in schema demo.core;
