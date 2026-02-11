from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = (
    spark.read
    .format("xml")
    .option("rowTag", "venda")
    .load("s3://datalake/raw/vendas_portal/")
)

df = df.select(
    col("id").cast("int").alias("venda_id"),
    col("nsu"),
    col("usuario_id").cast("int"),
    col("bandeira_id").cast("int"),
    col("data_venda").cast("date"),
    col("valor").cast("decimal(10,2)")
)

df.write.mode("overwrite").parquet(
    "s3://datalake/curated/vendas_portal/"
)
