SELECT
    id,
    last_name,
    loyalty_card
FROM
    customers
WHERE
    loyalty_card = true
    AND
	(last_name ILIKE '%m%' OR last_name ILIKE '%M%')
ORDER BY
	last_name DESC,
	id;
