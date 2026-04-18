# TruthLens Intelligence: Review 2 Data Flow Diagram (DFD)

Here is the Level 1 Data Flow Diagram illustrating the core workflow, data processes, and storage interactions completed during the Review 2 phase.

```mermaid
graph TD
    %% Styling
    classDef entity fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#bbf,stroke:#333,stroke-width:2px;
    classDef datastore fill:#dfd,stroke:#333,stroke-width:2px;

    %% External Entities
    U["User"]:::entity
    API["Live News API"]:::entity
    
    %% Processes
    P1("1.0 Authentication Process"):::process
    P2("2.0 Input Processing"):::process
    P3("3.0 ML Prediction Engine"):::process
    P4("4.0 History Management"):::process
    P5("5.0 Dashboard Rendering"):::process
    
    %% Data Stores
    D1[("D1 MongoDB: Users")]:::datastore
    D2[("D2 MongoDB: History")]:::datastore
    D3[("D3 Model: TF-IDF")]:::datastore
    
    %% Data Flows - Auth
    U -- "Credentials" --> P1
    P1 -- "Verify/Save Data" --> D1
    D1 -- "Auth Confirmation" --> P1
    P1 -- "JWT Token" --> U
    
    %% Data Flows - Input & Analysis
    U -- "Text or URL + JWT" --> P2
    P2 -- "Cleaned Text Data" --> P3
    D3 -- "TF-IDF Vectors" --> P3
    P3 -- "Confidence Score" --> P4
    
    %% Data Flows - Storage & History
    P4 -- "User ID & Prediction Data" --> D2
    D2 -- "User's Past Searches" --> P4
    
    %% Data Flows - Dashboard
    P4 -- "Current Score & History" --> P5
    API -- "Global Live Headlines" --> P5
    P5 -- "Complete UI Web Interface" --> U
```

### DFD Components Explained:
- **Entities (Pink):** The `User` interacts with the system, and the external `Live News API` feeds real-time data into the dashboard.
- **Processes (Blue):** Represent the core Flask logic created in Review 2 (handling tokens, extracting URLs, running the ML model, and rendering templates).
- **Data Stores (Green):** Represents the MongoDB collections mapping users and their histories, as well as the Machine Learning model file used for text vectorization.
