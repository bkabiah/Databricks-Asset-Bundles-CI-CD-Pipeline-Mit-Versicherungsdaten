from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

def run():
    spark = SparkSession.builder.getOrCreate()
    
    # Simulierte Rohdaten aus Versicherungsdokumenten (OCR Output)
    raw_data = [
        ("POL-1001", "Kfz-Versicherung", "Schaden am 12.05.2023. Reparaturkosten 1500 EUR. Kunde: Max Mustermann, Berlin.", "2023-05-12"),
        ("POL-1002", "Hausrat", "Wasserschaden Küche. Schadenhöhe 800 EUR. Kunde: Erika Musterfrau, München.", "2023-06-01"),
        ("POL-1003", "Kfz-Versicherung", "Wildschaden. Totalschaden. Kosten 12000 EUR. Kunde: Hans Schmidt, Hamburg.", "2023-07-15")
    ]
    
    columns = ["policy_id", "insurance_type", "raw_ocr_text", "incident_date"]
    df = spark.createDataFrame(raw_data, columns)
    
    df_bronze = df.withColumn("ingestion_timestamp", current_timestamp()) \
                  .withColumn("source_system", lit("OCR_Engine_v1"))
    
    # UNITY CATALOG: Speichern als Managed Table (kein DBFS Pfad mehr!)
    df_bronze.write.format("delta").mode("overwrite").saveAsTable("insurance_bronze")
    print("✅ Bronze Layer erfolgreich in Unity Catalog geschrieben.")

if __name__ == "__main__":
    run()
