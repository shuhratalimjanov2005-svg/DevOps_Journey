-- Первый запрос с операторами сравнения
SELECT name, rating
FROM pizzeria
WHERE rating >= 3.5 AND rating <= 5.0
ORDER BY rating;

-- Второй запрос с ключевым словом BETWEEN
SELECT name, rating
FROM pizzeria
WHERE rating BETWEEN 3.5 AND 5.0
ORDER BY rating;
