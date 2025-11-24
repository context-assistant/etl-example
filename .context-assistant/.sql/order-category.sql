SELECT * FROM order_table
    JOIN category on order_table.product_id = category.id
LIMIT 100