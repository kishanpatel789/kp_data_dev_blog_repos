{{config(materialized='table',tags=['hogwarts','students'],
schema='analytics')}}with student_base as(select id,first_name,last_name from 
{{ref('student')}}),house_lookup as(select id,house_name from {{source('core','house')}}),
enrollments as(select student_id,class_id,enrolled_at from {{ref('enrollment')}}),aggregated as
(SELECT s.id,s.first_name,s.last_name,h.house_name,count(e.class_id) as class_count,max(e.enrolled_at
) as last_enrolled_at from student_base s left join enrollments e on s.id=e.student_id join house_lookup 
h on s.house_id=h.id group by s.id,s.first_name,s.last_name,h.house_name)select id,first_name,last_name
,house_name,class_count,last_enrolled_at from aggregated order by class_count desc
