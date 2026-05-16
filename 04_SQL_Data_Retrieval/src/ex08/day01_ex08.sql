SELECT 
    order_date, 
    name  ' (age:'  age || ')' AS person_info
FROM (SELECT person_id AS id, order_date FROM person_order) AS t1
NATURAL JOIN person
ORDER BY order_date, person_info;
