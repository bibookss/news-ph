from dagster import define_asset_job

abs_cbn_job = define_asset_job(
    name="abs_cbn_job",
    selection=[
        "abs_cbn_article_index_raw",
        "abs_cbn_article_detail_raw"
    ]
)
