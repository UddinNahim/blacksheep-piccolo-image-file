SELECT
  jsonb_build_object(
    'id', p.id,
    'name', p.name,
    'description', p.description,
    'variations', COALESCE(v.variations, '[]'::jsonb)
  )
FROM product p
LEFT JOIN (
  SELECT
    pv.product_id,
    jsonb_agg(
      jsonb_build_object(
        'id', pv.id,
        'sku', pv.sku,
        'price', pv.price,
        'attributes', va.attributes
      )
    ) AS variations
  FROM product_variations pv
  LEFT JOIN (
    SELECT
      pav.variation_id,
      jsonb_object_agg(pan.name, pav.attribute_value) AS attributes
    FROM product_attribute_value pav
    JOIN product_attribute_name pan
      ON pan.id = pav.attribute_id
    GROUP BY pav.variation_id
  ) va
    ON va.variation_id = pv.id
  GROUP BY pv.product_id
) v
  ON v.product_id = p.id
WHERE p.id = 1;

INSERT INTO product (id, name, description) VALUES
(1, 'iPhone 15', 'Latest Apple smartphone'),
(2, 'Samsung Galaxy S23', 'Samsung flagship phone');

INSERT INTO product_variations (id, product_id, sku, price) VALUES
(10, 1, 'IP15-128-RED', 999.99),
(11, 1, 'IP15-256-BLACK', 1099.99),
(20, 2, 'S23-128-GREEN', 899.99);

INSERT INTO product_attribute_name (id, name) VALUES
(1, 'color'),
(2, 'storage'),
(3, 'ram');

INSERT INTO product_attribute_value
(id, variation_id, attribute_id, attribute_value)
VALUES
-- iPhone 15 – 128GB Red
(1, 10, 1, 'Red'),
(2, 10, 2, '128GB'),

-- iPhone 15 – 256GB Black
(3, 11, 1, 'Black'),
(4, 11, 2, '256GB'),

-- Samsung S23 – 128GB Green
(5, 20, 1, 'Green'),
(6, 20, 2, '128GB'),
(7, 20, 3, '8GB');

SELECT jsonb_agg(
  jsonb_build_object(
    'id', p.id,
    'name', p.name,
    'description', p.description,
    'variations', COALESCE(v.variations, '[]'::jsonb)
  )
) AS products
FROM product p
LEFT JOIN (
  SELECT
    pv.product_id,
    jsonb_agg(
      jsonb_build_object(
        'id', pv.id,
        'sku', pv.sku,
        'price', pv.price,
        'attributes', va.attributes
      )
      ORDER BY pv.id
    ) AS variations
  FROM product_variations pv
  LEFT JOIN (
    SELECT
      pav.variation_id,
      jsonb_object_agg(pan.name, pav.attribute_value) AS attributes
    FROM product_attribute_value pav
    JOIN product_attribute_name pan
      ON pan.id = pav.attribute_id
    GROUP BY pav.variation_id
  ) va
    ON va.variation_id = pv.id
  GROUP BY pv.product_id
) v
  ON v.product_id = p.id;
