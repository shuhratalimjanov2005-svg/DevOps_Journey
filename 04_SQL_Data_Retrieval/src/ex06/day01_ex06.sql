SELECT 
    t1.action_date, 
    (SELECT name FROM person WHERE id = t1.person_id) AS person_name
FROM (
    SELECT order_date AS action_date, person_id FROM person_order
    INTERSECT
    SELECT visit_date, person_id FROM person_visits
) AS t1
ORDER BY action_date ASC, person_name DESC;
