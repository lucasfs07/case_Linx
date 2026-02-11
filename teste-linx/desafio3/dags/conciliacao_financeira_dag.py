from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from datetime import datetime

with DAG(
    dag_id="conciliacao_financeira",
    start_date=datetime(2025, 3, 28),
    schedule_interval=None,
    catchup=False
):

    vendas_portal = GlueJobOperator(
        task_id="vendas_portal",
        job_name="vendas_portal_job"
    )

    vendas_erp = GlueJobOperator(
        task_id="vendas_erp",
        job_name="vendas_erp_job"
    )

    usuarios = GlueJobOperator(
        task_id="usuarios",
        job_name="usuarios_job"
    )

    bandeiras = GlueJobOperator(
        task_id="bandeiras",
        job_name="bandeiras_job"
    )

    [usuarios, bandeiras] >> vendas_portal >> vendas_erp
