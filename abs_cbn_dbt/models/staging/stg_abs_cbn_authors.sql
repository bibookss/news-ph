with raw as (
  select
    md5(
      json_extract_string(json_response, '$.data.headline') ||
      coalesce(json_extract_string(json_response, '$.data.firstpublished'), '')
    ) as article_uid,
    json_extract(json_response, '$.data.authors') as authors
  from {{ source('raw_abs_cbn_news', 'abs_cbn_article_detail_raw') }}
),

unnested as (
  select
    article_uid,
    json_extract_string(a.value, '$.name') as name,
    json_extract_string(a.value, '$.username') as username,
    json_extract_string(a.value, '$.twitter') as twitter,
    json_extract_string(a.value, '$.facebook') as facebook,
    json_extract_string(a.value, '$.avatar_url') as avatar_url,
    json_extract_string(a.value, '$.biography') as biography
  from raw,
  json_each(authors) as a
)

select * from unnested
where name is not null
