with raw_news as (
    select *
    from {{ source('raw_news', 'abs_cbn_article_detail_raw') }}
)

select
    _id,
    headline,
    extra ->> 'slugline_url' as slugline_url,
    cast(firstpublished as timestamp) as published_at,
    regexp_replace(body_html, '<[^>]+>', '') as body_text_cleaned,
    md5(headline || coalesce(firstpublished, '')) as article_uid,
    current_timestamp as loaded_at
from raw_news
where firstpublished is not null
