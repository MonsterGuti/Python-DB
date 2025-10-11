CREATE OR REPLACE PROCEDURE udp_update_loyalty_status(min_orders INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers AS c
    SET loyalty_card = TRUE
    WHERE c.id IN (
        SELECT o.customer_id
        FROM orders AS o
        GROUP BY o.customer_id
        HAVING COUNT(o.id) >= min_orders
    );
END;
$$;
