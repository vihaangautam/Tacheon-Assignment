# Thinking Log: Task 1 — Product Scoping

**Date**: May 27, 2026  
**Author**: Data & AI Product Engineer  

---

## 1. Deconstructing the Problem: Symptoms vs. Root Causes

When stakeholders say, *"We need a marketing performance dashboard,"* the immediate engineering instinct is to choose a frontend framework, set up high-performance charts, and hook it up to a database. 

However, a dashboard is merely a visualization of an underlying data pipeline. The actual pain point is not the *lack of visual charts*, but **data fragmentation and manual ownership**.

### The Current Reality (The Pain)
*   **Fragmentation**: Marketing data is locked in siloed platforms (Google Analytics for web sessions, Meta Ads for paid social, LinkedIn Ads for B2B search, HubSpot for CRM/emails).
*   **Manual Overhead**: Every time a client or account manager asks, *"How is our marketing performing across channels right now?"*, an analyst has to manually open 3 to 5 browser tabs, log in to individual portals, download CSV exports, copy-paste them into an Excel workbook, align dates, and write a manual summary.
*   **Inconsistency**: The definition of metrics (e.g. CTR, conversions, ROI) varies slightly depending on who extracts the data and how they calculate it.
*   **High Latency**: Because the extraction process is manual, reports are compiled only once a week or month. Real-time decision-making is impossible.

### The Durable Solution
The dashboard is a symptom-level solution. The real, durable engineering fix is **a lightweight, standardized internal data schema**. 
By introducing a unified data standard, we decouple *how data is captured* from *how data is consumed*. The frontend is just one consumer; automated reports, alerting scripts, and AI optimization engines could be others.

---

## 2. Choosing the Staging Layer: Google Sheets vs. Direct API Integration

A common mistake in v1 product design is building direct API integrations for Meta Ads, Google Analytics, LinkedIn Ads, etc., on day one. 

### Why Direct APIs in v1 are a Trap:
1.  **High Development Overhead**: Standardizing OAuth flows, handling API rate limits, handling token refreshes, and mapping changing API schemas takes weeks of high-complexity work.
2.  **API Fragility**: Martech APIs change frequently. Maintaining 4 separate external integrations creates 4 points of failure before we even validate if the dashboard solves the analyst's problem.
3.  **Process Friction**: The marketing team is already comfortable with their current workflow (manually checking tools). Forcing them to authorize an unvetted tool with their client credentials creates immediate adoption friction.

### The v1 Strategy: Google Sheets as a Staging Layer
Every martech analyst is highly proficient in Google Sheets. It is the universal interface of business. 

*   **Low Friction**: Analysts can continue to perform their standard manual exports, but instead of compiling them into ad-hoc files, they copy-paste them into a **standardized Google Sheet template**.
*   **Speed-to-Value**: We can build, test, and launch the v1 data model and visualization layer in days rather than months.
*   **Schema Validation**: The Google Sheet forces the team to align on a single, shared naming convention (e.g. `brand`, `channel`, `conversions`, `spend`).
*   **Zero-Cost Infrastructure**: No complex database servers or ingestion pipelines to host and pay for initially.

### The v2 Path: Direct API Connectors
Once the schema is stable, the analysts trust the numbers, and the tool is actively used, we swap the Google Sheets staging layer for direct API connectors. Because v1 laid a clean schema foundation, **this is a data source swap, not a rebuild of the application**.

---

## 3. Data Schema Design & Trust Metrics

To ensure data integrity, the standardized staging layer must enforce a strict, flat schema.

### Schema Spec:
*   `date` (DATE): Format `YYYY-MM-DD`. Standardizes all platform-specific timezone offsets.
*   `brand` (STRING): The unique brand/client name. Enables multi-tenant scaling.
*   `channel` (STRING): High-level category (`paid_social`, `paid_search`, `organic`, `email`).
*   `platform` (STRING): Specific source (`Meta`, `Google`, `LinkedIn`, `HubSpot`).
*   `impressions` (INTEGER), `clicks` (INTEGER), `spend` (FLOAT), `conversions` (INTEGER), `revenue` (FLOAT).
*   `source_tool` (STRING): Explicit tracking of origin tool (essential for auditing).
*   `loaded_at` (TIMESTAMP): Ingestion timestamp to identify staleness.

### Trust Metrics (How to make analysts actually use it):
1.  **Visible Freshness**: If an analyst sees a number, they must immediately know *when* it was last updated. A prominent `"Last updated: X hours ago"` banner is non-negotiable.
2.  **Explicit Attribution**: Every metric card should display a small badge indicating its source (e.g., `"via Meta Ads"`).
3.  **Anomaly Highlighting**: If spend is > $0 but impressions are 0, or if data hasn't been updated in 24 hours, the tool must display a clear, non-intrusive warning instead of failing silently.
