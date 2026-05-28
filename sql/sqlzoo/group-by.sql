SELECT actor.name
FROM actor
WHERE actor.id IN (
  SELECT casting.actorid
  FROM casting
  WHERE casting.ord = 1
  GROUP BY casting.actorid
  HAVING COUNT(casting.actorid) >= 15
)
ORDER BY actor.name
