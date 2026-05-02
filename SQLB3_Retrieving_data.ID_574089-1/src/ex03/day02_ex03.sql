WITH days AS (
    SELECT generate_series('2022-01-01'::date, '2022-01-10'::date, '1 day')::date AS missing_date
)
SELECT 
    d.missing_date
FROM 
    days d
LEFT JOIN 
    (SELECT visit_date FROM person_visits WHERE person_id = 1 OR person_id = 2) AS pv
    ON d.missing_date = pv.visit_date
WHERE 
    pv.visit_date IS NULL
ORDER BY 
    d.missing_date ASC;
