select
    _id,
    headline,
    extra.slugline_url,
    firstpublished,
    body_html
from public.abs_cbn_article_detail_raw
