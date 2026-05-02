SELECT 
    m.pizza_name, 
    piz.name AS pizzeria_name, 
    m.price
FROM 
    menu m
JOIN 
    pizzeria piz ON m.pizzeria_id = piz.id
WHERE 
    m.pizza_name IN ('mushroom pizza', 'pepperoni pizza')
ORDER BY 
    m.pizza_name, 
    pizzeria_name;
