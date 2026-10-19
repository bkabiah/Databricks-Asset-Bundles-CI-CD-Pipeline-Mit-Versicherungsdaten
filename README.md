# Versicherung Dokumenten Analyse Pipeline (Databricks Asset Bundles)

## Projektübersicht

Dieses Projekt demonstriert eine moderne, deklarative Datenpipeline für die **Analyse und Verwaltung von Versicherungsdokumenten**. Es wurde speziell für den Versicherungsmarkt konzipiert und verarbeitet simulierte OCR-Rohdaten aus Schadenmeldungen und Policen.

Die Pipeline nutzt **Databricks Asset Bundles (DAB)** für CI/CD, **Serverless Compute** via `environments`, **Unity Catalog Managed Tables** und integriert **PII-Maskierung** für DSGVO-Compliance.

## Tech Stack

- **Orchestrierung:** Databricks Asset Bundles (DAB) - Deklarative Automation
- **Compute:** Databricks Serverless Compute (via `environment_key`)
- **Storage:** Unity Catalog Managed Tables
- **Sprache:** Python (PySpark) & Databricks SDK
- **Architektur:** Medallion (Bronze, Silver, Gold)
- **Compliance:** DSGVO-konforme PII-Maskierung

##  Architektur-Diagramm

```mermaid
graph TD
    A[OCR-Dokumente<br/>Policen & Schäden] -->|Raw Ingestion| B[Bronze Layer<br/>insurance_bronze]
    B -->|Bereinigung & PII-Maskierung| C[Silver Layer<br/>insurance_silver]
    C -->|Aggregation & Features| D[Gold Layer<br/>insurance_gold]
    D --> E{Output}
    E -->|Business Intelligence| F[Dashboards]
    E -->|Machine Learning| G[ AI-Modelle]
    
    style A fill:#e1f5ff
    style B fill:#cd7f32
    style C fill:#c0c0c0
    style D fill:#ffd700
    style E fill:#9370db
    style F fill:#90ee90
    style G fill:#ff6b6b
    
    subgraph " Databricks Asset Bundles (DAB)"
        H[databricks.yml<br/>Declarative Config]
    end
    
    subgraph " Serverless Compute"
        I[environment_key:<br/>serverless_env]
    end
    
    subgraph " Unity Catalog"
        J[Managed Tables<br/>Data Governance]
    end
    
    H -.->|Orchestrierung| B
    H -.->|Orchestrierung| C
    H -.->|Orchestrierung| D
    I -.->|Compute| B
    I -.->|Compute| C
    I -.->|Compute| D
    J -.->|Storage| B
    J -.->|Storage| C
    J -.->|Storage| D

```

## 🏛️ Architektur-Diagramm

```mermaid
graph TD
    A[📄 OCR-Dokumente<br/>Policen & Schäden] -->|Raw Ingestion| B[Bronze Layer<br/>insurance_bronze]
    B -->|Bereinigung & PII-Maskierung| C[Silver Layer<br/>insurance_silver]
    C -->|Aggregation & Features| D[Gold Layer<br/>insurance_gold]
    D --> E{Output}
    E -->|Business Intelligence| F[📊 Dashboards]
    E -->|Machine Learning| G[🤖 AI-Modelle]
    
    style A fill:#e1f5ff
    style B fill:#cd7f32
    style C fill:#c0c0c0
    style D fill:#ffd700
    style E fill:#9370db
    style F fill:#90ee90
    style G fill:#ff6b6b
    
    subgraph "🔧 Databricks Asset Bundles (DAB)"
        H[databricks.yml<br/>Declarative Config]
    end
    
    subgraph "☁️ Serverless Compute"
        I[environment_key:<br/>serverless_env]
    end
    
    subgraph "🏛️ Unity Catalog"
        J[Managed Tables<br/>Data Governance]
    end
    
    subgraph "🔄 CI/CD Pipeline"
        K[GitHub Actions<br/>Automated Deploy]
    end
    
    subgraph "🧪 Testing"
        L[Pytest<br/>Unit Tests]
    end
    
    H -.->|Orchestrierung| B
    H -.->|Orchestrierung| C
    H -.->|Orchestrierung| D
    I -.->|Compute| B
    I -.->|Compute| C
    I -.->|Compute| D
    J -.->|Storage| B
    J -.->|Storage| C
    J -.->|Storage| D
    K -.->|Deploy| H
    L -.->|Testet| C

```


## Architektur & Pipeline-Schritte

### 1. Bronze Layer (Raw Ingestion)
- Nimmt unstrukturierte OCR-Texte aus Versicherungsdokumenten auf
- Fügt Metadaten (Ingestions-Zeitstempel, Quell-System) hinzu
- Speichert als **Unity Catalog Managed Table**

### 2. Silver Layer (Bereinigung & PII Maskierung)
- Bereinigt den Text (Normalisierung, Lowercase)
- **DSGVO-Feature:** Maskiert personenbezogene Daten (PII) wie Kundennamen automatisch
- Feature-Engineering für nachgelagerte AI-Modelle (z.B. "Totalschaden"-Erkennung)

### 3. Gold Layer (Aggregation)
- Erstellt Business-Metriken (Anzahl Schäden pro Versicherungstyp, durchschnittliche Textlänge)
- Dient als Basis für BI-Dashboards und Machine-Learning-Modelltraining

##  Installation & Deployment

### Voraussetzungen
- Python 3.8+
- Databricks CLI (`pip install databricks-cli databricks-sdk`)
- Databricks Personal Access Token (PAT)

### Lokales Setup

bash
# Projekt klonen
git clone <repo-url>
cd insurance_doc_pipeline

# Virtuelle Umgebung erstellen und aktivieren
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Abhängigkeiten installieren
pip install databricks-cli databricks-sdk

# Databricks CLI authentifizieren
databricks configure --token

---
# 📖 Architektur-Erklärung

## 1. Input
Unstrukturierte OCR-Texte aus Versicherungsdokumenten, z. B. Policen und Schadenmeldungen.

## 2. Bronze Layer
- **Raw Data Ingestion:** Import der Rohdaten.
- **Metadaten:** Ergänzung von Informationen wie Ingestions-Zeitstempel und Quell-System.

## 3. Silver Layer
- **Textbereinigung und Normalisierung:** Bereinigung und Vereinheitlichung der OCR-Texte.
- **DSGVO-Compliance:** Automatische PII-Maskierung (z. B. Kundennamen) mithilfe regulärer Ausdrücke.
- **Feature Engineering:** Aufbereitung von Merkmalen für nachgelagerte KI-Modelle, z. B. zur Erkennung von „Totalschaden“.

## 4. Gold Layer
- **Business-Aggregationen:** Erstellung von Kennzahlen pro Versicherungstyp für Reporting und Modelltraining.

## 5. Orchestrierung
- **Databricks Asset Bundles (DABs):** Deklarative und versionierbare Konfiguration der Datenpipelines.

## 6. CI/CD
- **GitHub Actions:** Automatisierte Tests und Deployments bei jedem Push ins Repository.

## 7. Testing
- **Pytest Unit Tests:** Sicherstellung der Korrektheit der Datentransformationslogik.

## 8. Compute
- **Serverless Compute:** Reduzierung des Cluster-Management-Aufwands und automatisches Skalieren der Rechenressourcen.

## 9. Storage
- **Unity Catalog Managed Tables:** Zentrale Verwaltung der Tabellen mit Datenherkunftsverfolgung (*Data Lineage*) und Zugriffskontrolle.
