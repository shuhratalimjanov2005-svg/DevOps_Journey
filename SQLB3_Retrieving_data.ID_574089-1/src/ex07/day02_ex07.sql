SELECT 
    piz.name AS pizzeria_name
FROM 
    person_visits pv
JOIN 
    person p ON pv.person_id = p.id
JOIN 
    pizzeria piz ON pv.pizzeria_id = piz.id
JOIN 
    menu m ON piz.id = m.pizzeria_id
WHERE 
    p.name = 'Dmitriy' 
    AND pv.visit_date = '2022-01-08' 
    AND m.price < 800;
