
# Versicherungsdokumenten Analyse Pipeline (Databricks Asset Bundles)

## Projektübersicht

Dieses Projekt demonstriert eine moderne, deklarative Datenpipeline für die **Analyse und Verwaltung von Versicherungsdokumenten**. Es wurde speziell für die Anforderungen des deutschen Versicherungsmarktes konzipiert und verarbeitet simulierte OCR-Rohdaten aus Schadenmeldungen und Policen.

Die Pipeline nutzt **Databricks Asset Bundles (DAB)** für Infrastructure-as-Code, **Serverless Compute** für skalierbare Ausführung, **Unity Catalog Managed Tables** für Data Governance und integriert eine robuste **PII-Maskierung** zur Gewährleistung der DSGVO-Compliance.

---

## Tech Stack

- **Orchestrierung:** Databricks Asset Bundles (DAB) – Deklarative Automation
- **CI/CD:** GitHub Actions (Automatisiertes Testing & Deployment)
- **Compute:** Databricks Serverless Compute (via `environment_key`)
- **Storage:** Unity Catalog Managed Tables (Delta Lake)
- **Sprache & Testing:** Python (PySpark) & Pytest (Unit Tests)
- **Architektur:** Medallion Architecture (Bronze, Silver, Gold)
- **Compliance:** DSGVO-konforme PII-Maskierung (Regular Expressions)

---

## Architektur-Diagramm

```mermaid
graph TD
    A[ OCR-Dokumente<br/>Policen & Schäden] -->|Raw Ingestion| B[Bronze Layer<br/>insurance_bronze]
    B -->|Bereinigung & PII-Maskierung| C[Silver Layer<br/>insurance_silver]
    C -->|Aggregation & Features| D[Gold Layer<br/>insurance_gold]
    D --> E{Output}
    E -->|Business Intelligence| F[ Dashboards]
    E -->|Machine Learning| G[ AI-Modelle]
    
    style A fill:#e1f5ff,stroke:#333,stroke-width:2px
    style B fill:#cd7f32,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#c0c0c0,stroke:#333,stroke-width:2px,color:#000
    style D fill:#ffd700,stroke:#333,stroke-width:2px,color:#000
    style E fill:#9370db,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#90ee90,stroke:#333,stroke-width:2px
    style G fill:#ff6b6b,stroke:#333,stroke-width:2px
    
    subgraph " CI/CD & Quality"
        K[GitHub Actions<br/>Automated Deploy]
        L[Pytest<br/>Unit Tests]
    end
    
    subgraph " Databricks Asset Bundles"
        H[databricks.yml<br/>Declarative Config]
    end
    
    subgraph " Serverless Compute"
        I[environment_key:<br/>serverless_env]
    end
    
    subgraph "Unity Catalog"
        J[Managed Tables<br/>Data Governance]
    end
    
    H -.->|Orchestriert| B
    H -.->|Orchestriert| C
    H -.->|Orchestriert| D
    I -.->|Compute| B
    I -.->|Compute| C
    I -.->|Compute| D
    J -.->|Storage| B
    J -.->|Storage| C
    J -.->|Storage| D
    K -.->|Validiert & Deployt| H
    L -.->|Testet Logik| C

```
#  Architektur-Erklärung

* **Input:** Unstrukturierte OCR-Texte aus Versicherungsdokumenten (z. B. Policen, Schadenmeldungen).
* **Bronze Layer:** Raw Data Ingestion mit Hinzufügen von Metadaten (Ingestions-Zeitstempel, Quell-System).
* **Silver Layer:**
  * Textbereinigung und Normalisierung.
  * DSGVO-Compliance: Automatische PII-Maskierung (z. B. Kundennamen) mittels regulärer Ausdrücke.
  * Feature-Engineering für nachgelagerte KI-Modelle (z. B. Erkennung von "Totalschaden").
* **Gold Layer:** Business-Aggregationen (Metriken pro Versicherungstyp) für Reporting und Modelltraining.
* **Orchestrierung:** Databricks Asset Bundles für deklarative, versionierbare Konfiguration.
* **CI/CD:** GitHub Actions Pipeline für automatisiertes Testing und Deployment bei jedem Push.
* **Testing:** Pytest Unit Tests stellen die Korrektheit der Data-Transformation-Logik sicher.
* **Compute:** Serverless Compute eliminiert Cluster-Management-Overhead und ermöglicht schnelles Scaling.
* **Storage:** Unity Catalog Managed Tables gewährleisten volle Data Lineage und Zugriffskontrolle.

  -----
  ##  Pipeline-Schritte im Detail

### 1. Bronze Layer (Raw Ingestion)
* Nimmt unstrukturierte OCR-Rohdaten auf.
* Fügt Audit-Metadaten (`ingestion_timestamp`, `source_system`) hinzu.
* Speichert die Daten als verwaltete Tabelle (Managed Table) im Unity Catalog.

### 2. Silver Layer (Bereinigung & PII-Maskierung)
* Bereinigt den Text (Lowercase, Entfernung von störenden Sonderzeichen, Beibehaltung von Satzzeichen für die Logik).
* **DSGVO-Feature:** Maskiert personenbezogene Daten (PII) wie Kundennamen automatisch zu `***MASKED***`.
* Extrahiert binäre Features (z. B. `contains_total_loss`) für das Machine Learning.

### 3. Gold Layer (Aggregation)
* Führt Group-by-Aggregationen durch (z. B. Anzahl Schäden pro Versicherungstyp, durchschnittliche Beschreibungslänge).
* Stellt eine saubere, analysierbare Datenbasis für BI-Tools (Power BI, Tableau) oder AI-Modelle bereit.

---

##  Testing & Quality Assurance

Das Projekt nutzt **Pytest** für Unit Tests der **PySpark**-Transformationen. Dies läuft lokal ohne Databricks-Cluster und stellt sicher, dass die Kernlogik (insbesondere die DSGVO-kritische PII-Maskierung) fehlerfrei arbeitet.

## CI/CD Pipeline

Bei jedem Push oder Pull Request auf den `main`-Branch wird automatisch folgender GitHub Actions Workflow (`.github/workflows/databricks-deploy.yml`) ausgeführt:

### Pipeline-Schritte

* **Environment Setup:** Python 3.10, PySpark, Pytest und Databricks CLI werden installiert.
* **Quality Gate:** `pytest tests/ -v` wird ausgeführt. Schlägt ein Test fehl, bricht die Pipeline ab.
* **Validation:** `databricks bundle validate` prüft die Syntax der DAB-Konfiguration.
* **Deployment:** `databricks bundle deploy` lädt den Code in den Databricks Workspace (via Environment Variables für sichere Authentifizierung).
* **Execution:** `databricks bundle run` startet die Pipeline zur Datenverarbeitung.
