from dagster import define_asset_job

abs_cbn_raw_job = define_asset_job(
    name="abs_cbn_raw_job",
    selection=["abs_cbn_article_index_raw", "abs_cbn_article_detail_raw"],
)

abs_cbn_staging_job = define_asset_job(
    name="abs_cbn_staging_job",
    selection=["stg_abs_cbn_news", "stg_abs_cbn_authors", "stg_abs_cbn_subjects"],
)
