from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = (
    spark.read
    .format("xml")
    .option("rowTag", "usuario")
    .load("s3://datalake/raw/usuarios/")
)

df = df.select(
    col("id").cast("int").alias("usuario_id"),
    col("nome")
)

df.write.mode("overwrite").parquet(
    "s3://datalake/curated/usuarios/"
)
