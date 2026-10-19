from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, length

def run():
    spark = SparkSession.builder.getOrCreate()
    
    # UNITY CATALOG: Lesen aus Managed Table
    df_silver = spark.read.table("insurance_silver")
    
    # Aggregation für BI und AI
    df_gold = df_silver.groupBy("insurance_type").agg(
        count("policy_id").alias("total_claims"),
        avg(length("cleaned_text")).alias("avg_description_length"),
        count(col("contains_total_loss")).alias("total_loss_count")
    )
    
    # UNITY CATALOG: Speichern als Managed Table
    df_gold.write.format("delta").mode("overwrite").saveAsTable("insurance_gold")
    print("✅ Gold Layer Aggregation erfolgreich in Unity Catalog geschrieben.")

if __name__ == "__main__":
    run()
