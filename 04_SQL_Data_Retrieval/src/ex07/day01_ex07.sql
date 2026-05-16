SELECT 
    order_date, 
    name  '(age:'  age || ')' AS person_info
FROM person_order
JOIN person ON person_order.person_id = person.id
ORDER BY order_date, person_info;
