# TruthLens Intelligence: Data Flow Diagrams (DFD)

This document contains standard Data Flow Diagrams spanning three depth levels, meticulously designed for Academic Submission (Review 3). 

**Diagram Key & Symbology:**
- **Rectangles (Gray):** External Entities (User, Admin)
- **Circles (Blue):** Processes and Compute Subsystems
- **Databases (Yellow):** Data Stores (MongoDB, CSVs, Pickle Files)
- **Arrows:** Directional Data Exchanges

---

## ✦ LEVEL 0: Context Diagram
*Provides a high-level overview of the entire system boundary and its relationships with external entities.*

```mermaid
graph TD
    classDef entity fill:#e2e8f0,stroke:#64748b,stroke-width:2px,color:#0f172a,border-radius:4px
    classDef process fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    
    User["External Entity: User"]:::entity
    Admin["External Entity: Admin"]:::entity
    System(("0.0<br/>TruthLens Intelligence System<br/>(AI Fake News Detector)")):::process

    User -- "News Text / URL Input" --> System
    System -- "Prediction Result<br/>(Fake/Real + Confidence)" --> User
    
    Admin -- "Dispute Resolution &<br/>Retrain Execution Commands" --> System
    System -- "Logs, Analytics &<br/>Model State Feedback" --> Admin
```

---

## ✦ LEVEL 1: System Breakdown
*Deconstructs the system into its primary subsystems: ML Prediction Engine, Dispute Systems, and the Retraining Pipeline.*

```mermaid
graph TD
    classDef entity fill:#e2e8f0,stroke:#64748b,stroke-width:2px,color:#0f172a
    classDef process fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    classDef datastore fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e

    User["User"]:::entity
    Admin["Admin"]:::entity

    P1(("1.0 Input<br/>Processing")):::process
    P2(("2.0 Data<br/>Preprocessing")):::process
    P3(("3.0 ML Prediction<br/>Engine")):::process
    P4(("4.0 Result<br/>Generation")):::process
    P5(("5.0 User Feedback<br/>Handling")):::process
    P6(("6.0 Dispute<br/>Management System")):::process
    P7(("7.0 Admin Console<br/>& Monitoring")):::process
    P8(("8.0 Model Retraining<br/>Pipeline")):::process

    DS1[("D1: News Dataset<br/>(CSV Files)")]:::datastore
    DS2[("D2: User History<br/>(MongoDB)")]:::datastore
    DS3[("D3: Disputes Collection<br/>(MongoDB)")]:::datastore
    DS4[("D4: Trained Model<br/>(model.pkl)")]:::datastore

    User -- "Raw Input" --> P1
    P1 -- "Normalized Text" --> P2
    P2 -- "Cleaned Tokens" --> P3
    DS4 -- "Loaded Weights/TF-IDF" --> P3
    P3 -- "Classification Arrays" --> P4
    P4 -- "Structured Output" --> User
    
    User -- "Implicit/Explicit Feedback" --> P5
    P5 -- "Agree (Log to History)" --> DS2
    P5 -- "Disagree (Submit Dispute)" --> P6
    P6 -- "New Pending Dispute" --> DS3
    
    Admin -- "Monitor Analytics" --> P7
    DS2 -- "Usage Stats" --> P7
    DS3 -- "Dispute Logs" --> P7
    P7 -- "Dashboards/Insights" --> Admin
    
    Admin -- "Resolve & Assign Label" --> P6
    P6 -- "Status: Resolved" --> DS3

    Admin -- "Trigger Batch Retrain" --> P8
    DS1 -- "Baseline Static Dataset" --> P8
    DS3 -- "Verified Dispute Data" --> P8
    P8 -- "Updated ML Weights" --> DS4
```

---

## ✦ LEVEL 2: Detailed Internal Workflows
*Zooms into the critical individual processes demonstrating text logic and database maneuvers step-by-step.*

### A. Prediction Flow
```mermaid
graph TD
    classDef entity fill:#e2e8f0,stroke:#64748b,stroke-width:2px,color:#0f172a
    classDef process fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    classDef datastore fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e

    User["User"]:::entity
    P1_1(("1.1 Extractor<br/>(URL Scraping / Text)")):::process
    P1_2(("1.2 Text NLP Cleaning<br/>(Lemmatization)")):::process
    P1_3(("1.3 Vectorization<br/>(TF-IDF N-grams)")):::process
    P1_4(("1.4 Classification<br/>(Logistic Regression)")):::process
    P1_5(("1.5 Response Mapper<br/>(JSON Output)")):::process
    DS_M[("D4: model.pkl")]:::datastore

    User -- "Input Form" --> P1_1
    P1_1 -- "Raw Strings" --> P1_2
    P1_2 -- "Cleaned Text Corpus" --> P1_3
    P1_3 -- "Numerical Features Array" --> P1_4
    DS_M -- "Vector Vocab. Definitions" --> P1_3
    DS_M -- "Trained LogReg Weights" --> P1_4
    P1_4 -- "Raw Probabilities" --> P1_5
    P1_5 -- "Confidence Scores" --> User
```

### B. Feedback & Dispute Validation Flow
```mermaid
graph TD
    classDef entity fill:#e2e8f0,stroke:#64748b,stroke-width:2px,color:#0f172a
    classDef process fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    classDef datastore fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e

    User["User"]:::entity
    Admin["Admin"]:::entity
    P2_1(("2.1 Evaluate Frontend<br/>Feedback Signals")):::process
    P2_2(("2.2 Initialize<br/>Dispute Ticket")):::process
    P2_3(("2.3 Validate Correct<br/>Label Assignment")):::process
    P2_4(("2.4 Update Dispute<br/>State Manager")):::process
    
    DS_H[("D2: User History Db")]:::datastore
    DS_D[("D3: Disputes Db")]:::datastore

    User -- "Selects 'Accurate' / 'Inaccurate'" --> P2_1
    P2_1 -- "If Accurate" --> DS_H
    P2_1 -- "If Inaccurate" --> P2_2
    P2_2 -- "Commit Pending Dispute" --> DS_D
    
    Admin -- "Review Queued Disputes" --> P2_3
    DS_D -- "Fetch Pending Queries" --> P2_3
    P2_3 -- "Set Approved 'correct_label'" --> P2_4
    P2_4 -- "Persist State: Resolved" --> DS_D
```

### C. Retraining & Overwrite Flow
```mermaid
graph TD
    classDef entity fill:#e2e8f0,stroke:#64748b,stroke-width:2px,color:#0f172a
    classDef process fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a
    classDef datastore fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e

    Admin["Admin"]:::entity
    P3_1(("3.1 Query Resolved<br/>Disputes")):::process
    P3_2(("3.2 Append & Merge<br/>Training Corpus")):::process
    P3_3(("3.3 Refit TF-IDF<br/>Transformers")):::process
    P3_4(("3.4 Train Logistic<br/>Regression Classifier")):::process
    P3_5(("3.5 Snapshot Backups<br/>(shutil archiver)")):::process
    P3_6(("3.6 Model Serialization<br/>(Pickle Dumper)")):::process

    DS_D[("D3: Disputes Db")]:::datastore
    DS_CSV[("D1: Base News CSVs")]:::datastore
    DS_MO[("D5: model_backup.pkl")]:::datastore
    DS_M[("D4: model.pkl")]:::datastore

    Admin -- "POST /admin/retrain" --> P3_1
    DS_D -- "Yields Verified Human Labels" --> P3_1
    DS_CSV -- "Yields Base Training Data" --> P3_2
    P3_1 -- "Inject Resolved Payload" --> P3_2
    P3_2 -- "Large Combined Matrix" --> P3_3
    P3_3 -- "Re-indexed Tensors" --> P3_4
    P3_4 -- "Convergence Checks" --> P3_5
    DS_M -- "Current Production Model" --> P3_5
    P3_5 -- "Archived Version" --> DS_MO
    P3_5 -- "Replaced Payload" --> P3_6
    P3_6 -- "Write New Artifact" --> DS_M
```
