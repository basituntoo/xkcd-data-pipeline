SELECT
    comic_id,
    title,
    publish_date,
    img_url,
    alt_text
FROM {{ ref('stg_xkcd_comics') }}
