WITH busy_students as(select s.id,s.name,count(e.class_id) as class_count from students 
s join enrollments e on s.id=e.student_id group by s.id,s.name HAVING count(e.class_id)>3)select * 
fRom busy_students where name like '%Granger%';
