select s.name ,h.house_name,p.position_name,  CASE when s.year=1 then 'First Year' when s.year=2 then 'Second Year' when s.year=3 then 'Third Year' else 'Upperclassman' end as year_label FROM students s join houses h on s.house_id=h.id left join positions p on s.position_id=p.id where h.house_name='Gryffindor' and (p.position_name='Seeker' or p.position_name='Keeper') order by s.name ;


SeLeCt S.FIRST_NAME, s.last_name, s.year, h.house_NAME, COUNT(e.class_id) as class_Count, max(e.enrolled_at) AS LAST_ENROLLMENT_DATE FrOm student as S JoIn house as h ON S.house_id = h.id leFT join enrollment as e ON s.id=e.student_id where s.year > 4 and (h.house_NAME = 'Gryffindor' or h.house_NAME = 'Ravenclaw') and e.is_active = TRUE GROUP by s.name,h.house_name having count(e.class_id)>2;
