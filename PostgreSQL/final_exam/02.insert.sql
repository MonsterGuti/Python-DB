INSERT INTO items (name, quantity, price, description, brand_id, classification_id)
SELECT
	'Item' || r.created_at AS name,
	r.customer_id AS quantity,
	r.rating * 5 AS price,
	NULL AS description,
	r.item_id AS brand_id,
	(SELECT MIN(item_id) FROM reviews) AS classification_id
FROM
	reviews AS r
ORDER BY
	r.item_id
LIMIT
	10;