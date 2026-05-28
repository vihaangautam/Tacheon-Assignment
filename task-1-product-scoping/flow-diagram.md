# Flow Diagrams: Task 1 — Product Scoping

This document maps out the User Flow and Data Flow architectures for the v1 internal marketing performance tool.

---

## 1. User Flow Diagram
This flowchart tracks how an internal analyst interacts with the dashboard to quickly answer their primary questions.

```mermaid
flowchart TD
    A[Analyst opens tool] --> B[Selects brand + date range]
    B --> C[Tool reads from Google Sheet / data source]
    C --> D{Data fresh?}
    D -- Yes --> E[Render channel performance view]
    D -- No --> F[Show staleness warning + last known data]
    E --> G[Highlight top performer + underperformer]
    G --> H[Analyst walks away with answer in < 2 min]
```

---

## 2. Data Flow Diagram
This flowchart displays the architecture of the data flow, showing how data moves from original sources to the staging layer and into the standardized internal tool.

```mermaid
flowchart LR
    subgraph Sources ["Existing Tools (unchanged)"]
        GA[Google Analytics]
        Meta[Meta Ads Manager]
        LinkedIn[LinkedIn Ads]
        HubSpot[HubSpot]
    end

    subgraph Staging ["V1 Staging Layer"]
        GS[Google Sheet\nStandardised Template]
    end

    subgraph Tool ["Internal Tool"]
        Reader[Sheet Reader]
        Transform[Standardise + Validate]
        Display[Performance View]
    end

    GA -- manual export --> GS
    Meta -- manual export --> GS
    LinkedIn -- manual export --> GS
    HubSpot -- manual export --> GS
    GS --> Reader --> Transform --> Display
```
