SELECT
    comic_id,
    (RANDOM() * 10000)::INT AS views,
    LENGTH(REPLACE(title, ' ', '')) * 5 AS cost_eur,
    ROUND((1 + RANDOM() * 9)::numeric, 1) AS review_score,
    CURRENT_DATE AS snapshot_date
FROM {{ ref('dim_comic') }}
