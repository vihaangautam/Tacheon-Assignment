# Task 1: Product Scoping — Marketing Performance Dashboard

This directory contains the product scoping and architectural design documentation for a lightweight, internal marketing performance tool designed for Tacheon/Smacient.

---

## 📂 Document Navigation

*   **[Product Brief](file:///c:/Users/ASUS/OneDrive/Desktop/vscProgram/tacheon%20assignment/task-1-product-scoping/product-brief.md)**: The full product requirements document (PRD) specifying the v1 boundaries, data schema, and trust features.
*   **[Flow Diagrams](file:///c:/Users/ASUS/OneDrive/Desktop/vscProgram/tacheon%20assignment/task-1-product-scoping/flow-diagram.md)**: Mermaid charts representing both user interaction paths and backend data flows.
*   **[Thinking Log](file:///c:/Users/ASUS/OneDrive/Desktop/vscProgram/tacheon%20assignment/task-1-product-scoping/thinking-log.md)**: Raw, unedited developer journal documenting the initial conceptualization, symptom deconstruction, and tool-neutral architecture decisions.

---

## 🎯 Core Architectural Decisions & Trade-Offs

When scoping a v1 martech product, balancing execution speed with long-term durability is the central challenge. Below are the key decisions made and the conscious trade-offs accepted.

### 1. Primary User: Internal Agency Analyst vs. End Client
*   **Decision**: Scope v1 exclusively for internal analysts and account managers.
*   **Why**: The client's trust is secondary to the team's internal trust. If our internal analysts find discrepancies in the data or do not use the tool to make recommendations, the client will never see it. Solving internal pain points is the fastest way to refine and bulletproof the data schema.
*   **Trade-off**: Clients do not get direct access or self-serve reports in v1. They continue to receive manual summaries, though compile time is dramatically reduced.

### 2. Staging Layer: Google Sheets vs. Direct APIs
*   **Decision**: Utilize a standardized Google Sheet template as the v1 staging layer.
*   **Why**: Marketing teams are deeply entrenched in their current tools and workflows. Forcing direct API authorization on Day 1 is a trap: OAuth configurations, rate limiting, and fragile third-party schemas introduce weeks of development overhead before validation. Google Sheets provides a zero-cost, zero-maintenance, highly-flexible interface that analysts already master.
*   **Trade-off**: Data ingestion is not fully automated; analysts must manually export CSVs from platforms and paste them into the template. 

### 3. Feature Scope: Focus Indicators vs. AI Recommendations
*   **Decision**: Focus on simple visual highlights (e.g. top-performing and underperforming channels) and omit AI-generated recommendations.
*   **Why**: Marketing recommendations require deep contextual understanding of a brand's specific business goals. An incorrect or naive automated "AI advice" (e.g. telling a brand to cut spend on a channel that generates high-value, long-cycle offline leads) would instantly destroy user trust.
*   **Trade-off**: The tool acts as a standardized reporter and visualizer, leaving strategic decisions to the human analyst.

---

## 🔄 The Path to v2 (What We'd Revisit)

Given more time and development cycles, the next steps are clearly defined:
1.  **Schema Verification**: Compare our standardized input schema against actual exports from GA4, Meta Ads, and LinkedIn Ads to ensure data compatibility.
2.  **API Connector Swap**: Replace the Google Sheets reader with serverless ETL connectors. Because v1 standardizes the schema, the ingestion swap does not affect the frontend dashboard.
3.  **Dynamic Focus Rule Sets**: Allow analysts to define primary success metrics dynamically per brand (e.g., brand A focuses on ROAS, brand B focuses on CPA).
