SELECT
    i.name,
    UPPER(b.name) || '/' || LOWER(c.name) AS promotion,
    'On sale: ' || COALESCE(i.description, '') AS description,
    i.quantity
FROM
    items AS i
    JOIN classifications AS c ON c.id = i.classification_id
    JOIN brands AS b ON i.brand_id = b.id
    LEFT JOIN orders_items AS o_t ON i.id = o_t.item_id
WHERE
    o_t.item_id IS NULL
ORDER BY
    i.quantity DESC,
    i.name ASC;
