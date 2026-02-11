from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = (
    spark.read
    .format("xml")
    .option("rowTag", "bandeira")
    .load("s3://datalake/raw/bandeiras/")
)

df = df.select(
    col("id").cast("int").alias("bandeira_id"),
    col("nome")
)

df.write.mode("overwrite").parquet(
    "s3://datalake/curated/bandeiras/"
)
