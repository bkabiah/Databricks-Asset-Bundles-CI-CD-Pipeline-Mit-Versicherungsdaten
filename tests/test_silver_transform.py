"""
Unit Tests für die Silver Layer PII-Maskierung
Diese Tests laufen lokal ohne Databricks-Cluster
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, lower


@pytest.fixture(scope="module")
def spark():
    """
    Pytest Fixture: Erstellt eine lokale Spark Session für Tests
    """
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("pytest-pyspark-insurance") \
        .config("spark.sql.shuffle.partitions", "1") \
        .getOrCreate()
    
    yield spark
    
    # Cleanup nach allen Tests
    spark.stop()


def test_pii_masking_simple_name(spark):
    """
    Test: Einfacher Name wird korrekt maskiert
    """
    # Arrange
    data = [("POL-1001", "Kunde: Max Mustermann, Berlin")]
    df = spark.createDataFrame(data, ["policy_id", "raw_ocr_text"])
    
    # Act (KORRIGIERTE Logik aus silver_transform.py)
    df_clean = df.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    df_masked = df_clean.withColumn(
        "masked_text", 
        regexp_replace(col("cleaned_text"), "(kunde: )([a-zäöüß ]+)", "$1***MASKED***")
    )
    
    # Assert
    result = df_masked.select("masked_text").collect()[0][0]
    assert "***MASKED***" in result
    assert "Max Mustermann" not in result
    assert "kunde:" in result


def test_pii_masking_german_name(spark):
    """
    Test: Deutscher Name mit Umlauten wird korrekt maskiert
    """
    # Arrange
    data = [("POL-1002", "Kunde: Erika Musterfrau, München")]
    df = spark.createDataFrame(data, ["policy_id", "raw_ocr_text"])
    
    # Act (KORRIGIERTE Logik)
    df_clean = df.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    df_masked = df_clean.withColumn(
        "masked_text", 
        regexp_replace(col("cleaned_text"), "(kunde: )([a-zäöüß ]+)", "$1***MASKED***")
    )
    
    # Assert
    result = df_masked.select("masked_text").collect()[0][0]
    assert "***MASKED***" in result
    assert "Erika Musterfrau" not in result


def test_text_cleaning_removes_special_chars(spark):
    """
    Test: Sonderzeichen werden entfernt (außer : und .)
    """
    # Arrange
    data = [("POL-1003", "Schaden am 12.05.2023! Reparaturkosten: 1500 EUR.")]
    df = spark.createDataFrame(data, ["policy_id", "raw_ocr_text"])
    
    # Act (KORRIGIERTE Logik)
    df_clean = df.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    
    # Assert
    result = df_clean.select("cleaned_text").collect()[0][0]
    assert "!" not in result
    assert ":" in result  # Doppelpunkt bleibt erhalten
    assert "schaden am 12.05.2023" in result


def test_total_loss_feature_extraction(spark):
    """
    Test: Totalschaden-Erkennung funktioniert
    """
    # Arrange
    data = [("POL-1004", "Wildschaden. Totalschaden. Kosten 12000 EUR.")]
    df = spark.createDataFrame(data, ["policy_id", "raw_ocr_text"])
    
    # Act
    df_clean = df.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    df_with_feature = df_clean.withColumn(
        "contains_total_loss", 
        col("cleaned_text").contains("totalschaden")
    )
    
    # Assert
    result = df_with_feature.select("contains_total_loss").collect()[0][0]
    assert result == True


def test_no_total_loss_feature(spark):
    """
    Test: Kein Totalschaden wird korrekt erkannt
    """
    # Arrange
    data = [("POL-1005", "Kleiner Schaden. Reparaturkosten 200 EUR.")]
    df = spark.createDataFrame(data, ["policy_id", "raw_ocr_text"])
    
    # Act
    df_clean = df.withColumn(
        "cleaned_text", 
        lower(regexp_replace(col("raw_ocr_text"), "[^a-zA-Z0-9äöüÄÖÜß\\s\\.:]", ""))
    )
    df_with_feature = df_clean.withColumn(
        "contains_total_loss", 
        col("cleaned_text").contains("totalschaden")
    )
    
    # Assert
    result = df_with_feature.select("contains_total_loss").collect()[0][0]
    assert result == False
