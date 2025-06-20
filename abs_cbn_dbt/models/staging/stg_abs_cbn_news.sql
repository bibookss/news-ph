with raw as (
  select * from {{ source('raw_abs_cbn_news', 'abs_cbn_article_detail_raw') }}
),

extracted as (
  select
    json_extract_string(json_response, '$.data._id') as abs_id,
    md5(
      json_extract_string(json_response, '$.data.headline') ||
      coalesce(json_extract_string(json_response, '$.data.firstpublished'), '')
    ) as article_uid,
    json_extract_string(json_response, '$.data.headline') as headline,
    json_extract_string(json_response, '$.data.extra.slugline_url') as slugline_url,
    cast(json_extract_string(json_response, '$.data.firstpublished') as timestamp) as published_at,
    cast(json_extract_string(json_response, '$.data._created') as timestamp) as created_at,
    cast(json_extract_string(json_response, '$.data._updated') as timestamp) as updated_at,
    json_extract_string(json_response, '$.data.description_text') as description,
    json_extract_string(json_response, '$.data.language') as language,
    json_extract_string(json_response, '$.data.profile') as profile,
    cast(json_extract_string(json_response, '$.data.wordcount') as int) as wordcount,
    regexp_replace(json_extract_string(json_response, '$.data.body_html'), '<[^>]+>', '') as body_text_cleaned,
    current_timestamp as loaded_at
  from raw
)

select * from extracted
where published_at is not null
