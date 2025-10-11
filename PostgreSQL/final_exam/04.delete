DELETE FROM
	customers
WHERE
	id not in(
		SELECT customer_id FROM orders
	);