import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, regexp_replace, trim

# --- Setup ---
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --- Step 1: Read raw CSV from bronze/ ---
INPUT_PATH = "s3://de-aditya-engine-421845/bronze/engine_data_raw.csv"
OUTPUT_PATH = "s3://de-aditya-engine-421845/silver/"

df = spark.read.option("header", "true").option("inferSchema", "true").csv(INPUT_PATH)

print("Raw row count:", df.count())
print("Columns:", df.columns)

# --- Step 2: Clean the data ---

# Remove rows where engine_title is null (useless records)
df = df.filter(col("engine_title").isNotNull())

# Clean engine_lifespan_km — remove ~, spaces, commas → keep only numbers
df = df.withColumn(
    "engine_lifespan_km",
    regexp_replace(col("engine_lifespan_km"), "[^0-9]", "").cast("integer")
)

# Cast numeric columns to correct types
df = df.withColumn("power_output_hp", col("power_output_hp").cast("integer"))
df = df.withColumn("torque_output_nm", col("torque_output_nm").cast("integer"))
df = df.withColumn("displacement_cc", col("displacement_cc").cast("integer"))
df = df.withColumn("year_start", col("year_start").cast("integer"))

# Trim whitespace from string columns
df = df.withColumn("fuel_type", trim(col("fuel_type")))
df = df.withColumn("turbocharging", trim(col("turbocharging")))
df = df.withColumn("manufacturer", trim(col("manufacturer")))

print("Clean row count:", df.count())

# --- Step 3: Write to silver/ as Parquet ---
df.write.mode("overwrite").parquet(OUTPUT_PATH)

print("Written to silver/ as Parquet successfully.")

job.commit()