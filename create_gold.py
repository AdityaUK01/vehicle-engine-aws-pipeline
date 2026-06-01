import boto3
import time

athena = boto3.client('athena', region_name='ap-south-1')

RESULTS = 's3://de-aditya-engine-421845/athena-results/'

queries = {
    'gold_manufacturer_count': """
        CREATE TABLE engine_db.gold_manufacturer_count
        WITH (
            format = 'PARQUET',
            external_location = 's3://de-aditya-engine-421845/gold/manufacturer_count/'
        ) AS
        SELECT manufacturer, COUNT(*) as engine_count
        FROM engine_db.engines
        WHERE manufacturer IS NOT NULL
        GROUP BY manufacturer
        ORDER BY engine_count DESC
    """,
    'gold_fuel_type_stats': """
        CREATE TABLE engine_db.gold_fuel_type_stats
        WITH (
            format = 'PARQUET',
            external_location = 's3://de-aditya-engine-421845/gold/fuel_type_stats/'
        ) AS
        SELECT fuel_type,
               COUNT(*) as total_engines,
               ROUND(AVG(power_output_hp), 0) as avg_power_hp,
               ROUND(AVG(torque_output_nm), 0) as avg_torque_nm
        FROM engine_db.engines
        WHERE fuel_type IS NOT NULL
        GROUP BY fuel_type
        ORDER BY avg_power_hp DESC
    """,
    'gold_top_lifespan': """
        CREATE TABLE engine_db.gold_top_lifespan
        WITH (
            format = 'PARQUET',
            external_location = 's3://de-aditya-engine-421845/gold/top_lifespan/'
        ) AS
        SELECT engine_title, manufacturer, engine_lifespan_km, power_output_hp
        FROM engine_db.engines
        WHERE engine_lifespan_km IS NOT NULL
        ORDER BY engine_lifespan_km DESC
        LIMIT 10
    """
}

for name, query in queries.items():
    print(f"Running: {name}")
    response = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={'OutputLocation': RESULTS}
    )
    print(f"Started: {response['QueryExecutionId']}")
    time.sleep(5)

print("All gold tables created.")
# This script creates three gold tables in Athena based on the cleaned data in the 'engines' table. Each query is executed sequentially, and the results are stored in separate S3 locations in Parquet format for efficient querying.
