from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, lower

def run():
    spark = SparkSession.builder.getOrCreate()
    
    # Lesen aus Unity Catalog Managed Table
    df_bronze = spark.read.table("insurance_bronze")
    
    # 1. Textbereinigung (BEHÄLT das ":" für die PII-Maskierung)
    df_clean = df_bronze.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    
    # 2. PII Maskierung (DSGVO-Compliance: Maskiert Namen nach "kunde:")
    df_silver = df_clean.withColumn(
        "masked_text", 
        regexp_replace(col("cleaned_text"), "(kunde: )([a-zäöüß ]+)", "$1***MASKED***")
    )
    
    # 3. Feature Engineering für AI-Modelle
    df_silver = df_silver.withColumn(
        "contains_total_loss", 
        col("cleaned_text").contains("totalschaden")
    )
    
    # Speichern als Unity Catalog Managed Table
    df_silver.write.format("delta").mode("overwrite").saveAsTable("insurance_silver")
    print("✅ Silver Layer mit PII-Maskierung erfolgreich in Unity Catalog geschrieben.")

if __name__ == "__main__":
    run()
