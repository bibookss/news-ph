with raw as (
  select
    md5(
      json_extract_string(json_response, '$.data.headline') ||
      coalesce(json_extract_string(json_response, '$.data.firstpublished'), '')
    ) as article_uid,
    json_extract(json_response, '$.data.subject') as subject_tags
  from {{ source('raw_abs_cbn_news', 'abs_cbn_article_detail_raw') }}
),

unnested as (
  select
    article_uid,
    json_extract_string(s.value, '$.code') as code,
    json_extract_string(s.value, '$.name') as name,
    json_extract_string(s.value, '$.scheme') as scheme
  from raw,
  json_each(subject_tags) as s
)

select * from unnested
where code is not null
