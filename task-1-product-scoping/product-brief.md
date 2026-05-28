# Product Brief: Task 1 — Product Scoping

## 1. Problem Statement
One fundamental question — **"How is our marketing performing across channels right now, and where should we focus?"** — currently has no reliable, fast, or consistent answer. 

Currently, the process depends on a single person who must manually open 3 to 5 separate tools (Google Analytics, Meta Ads, LinkedIn Ads, HubSpot, etc.), export data, align dates, and assemble a report. This manual overhead creates several issues:
- **High latency**: Data is only compiled weekly or monthly.
- **Inconsistency**: Output and calculations vary by analyst.
- **Single point of failure**: Dependance on manual extraction.

The real issue is not just the lack of a dashboard, but **data fragmentation and manual ownership**.

---

## 2. Primary User
**Internal Analyst / Account Manager** (not the end client).
- **Rationale**: If the internal agency team does not trust, adopt, or use the tool daily, it will never be successful or ready for client exposure. Solving the internal team's pain first establishes a baseline of trust and validates the schema.
- **Client-facing portal** is explicitly deferred to **v2**.

---

## 3. Scope of v1

### What v1 Does (In Scope)
*   **Brand & Date Selection**: Ability to select a client brand and date range.
*   **Channel-Level Performance**: View high-level metrics across all channels (Paid Social, Paid Search, Organic, Email) in a single unified view.
*   **"Where to Focus" Signal**: Simple visual highlights of the top-performing and underperforming channels based on a primary metric (e.g., ROAS, CTR, or Conversion Rate).
*   **Data Freshness Indicator**: Explicit and prominent visibility of when data was last updated (e.g., *"Last updated: 2 hours ago"*) on every screen.
*   **Source Attribution**: Badges or labels indicating which tool generated each metric (e.g., `"via Meta Ads"`).

### What v1 Does NOT Do (Out of Scope)
| Feature | Why it's out of scope |
|---|---|
| **Client-Facing Portal** | Internal trust and schema stability must be established first. |
| **AI-Generated Recommendations** | Adds technical complexity; incorrect suggestions would destroy user trust. |
| **Automated Scheduled Reports** | Will be built in a future phase once the data pipelines are fully stable. |
| **Multi-Brand Comparison View** | Scope creep; focus on single-brand depth first. |
| **Historical Trend Charts** | Secondary to the primary, immediate question of current performance. |
| **Alert / Anomaly Detection** | V2 feature once historical baselines and thresholds are established. |
| **Mobile Web Layout** | Primarily an internal tool used on desktop computers; desktop optimization is sufficient. |

---

## 4. Data Layer Architecture

### The Constraint
**The martech/marketing team will not change the tools they use.** The tool must adapt to their current workflow rather than forcing them to adapt to the tool.

### V1 Staging Layer: Google Sheets
- **The Strategy**: Every analyst is already highly proficient in Google Sheets. Instead of direct API integrations, the team will export CSVs from their respective tools and paste them into a **standardized Google Sheets template**.
- **Why Google Sheets?**
  1. **Low Friction**: Leveraging existing analyst skill sets.
  2. **Speed to Market**: We can deploy and validate the application logic in days instead of weeks of OAuth setup.
  3. **Zero Infrastructure Cost**: No database host or data lake ingestion pipeline required for v1.
  4. **Source Schema Definition**: Serves as a perfect sandbox to refine and stabilize the data model.

### V2 Path: Direct API Connectors
Once the schema is stable and the tool is adopted, we will swap the Google Sheets staging layer for direct API connectors (Meta Marketing API, Google Analytics Admin/Data API, etc.). Because the v1 schema is standardized, this transition will be a **data source swap, not an application rebuild**.

---

## 5. Standardized Data Schema
The Google Sheet template forces all input data to conform to this strict, flat schema:

| Field | Type | Description |
|---|---|---|
| `date` | DATE | Reporting date (standardized to `YYYY-MM-DD` timezone offset) |
| `brand` | STRING | Client brand name (supports multi-tenant views) |
| `channel` | STRING | Broad channel category (e.g., `paid_social`, `paid_search`, `organic`, `email`) |
| `platform` | STRING | Specific source platform (e.g., `Meta`, `Google`, `LinkedIn`, `HubSpot`) |
| `impressions` | INTEGER | Number of impressions recorded |
| `clicks` | INTEGER | Number of clicks recorded |
| `spend` | FLOAT | Spend in local currency |
| `conversions` | INTEGER | Total conversions recorded |
| `revenue` | FLOAT | Attributed revenue generated |
| `source_tool` | STRING | Name of the originating source system (used for audit trails) |
| `loaded_at` | TIMESTAMP | Timestamp of when the row was loaded into staging |

---

## 6. Trust Metrics & Verification
To drive analyst adoption, the tool implements active trust mechanisms:
1. **Freshness Prominence**: Data freshness is always displayed. If the data is older than a set threshold, an amber warning banner is displayed.
2. **Explicit Lineage**: Every single chart and numeric card is attributed back to its originating platform.
3. **Suspicious Data Warnings (Anomalies)**: The tool automatically flags anomalies (e.g., `spend > 0` but `impressions == 0`) rather than rendering invalid data.
4. **Validation Layer**: The staging reader rejects rows that do not strictly comply with the schema format, reporting error lines to the analyst.

---

## 7. Success Metric
An internal account manager or analyst can answer the question *"How is [brand] performing across channels this week, and where should we focus?"* in **under 2 minutes** without opening any other tool. The output is consistent and identical, regardless of who runs the query.

---

## 8. What We Would Revisit With More Time
- **Direct API Feasibility**: Validate the required API permissions and scopes for Google Analytics 4 and Meta Ads to map out the exact OAuth requirements.
- **Analyst Interviews**: Conduct UX feedback sessions with 2–3 internal analysts to refine metric cards and layout.
- **Dynamic "Where to Focus" Logic**: Develop tailored baseline rules (e.g., comparing current performance to a rolling 7-day average) since "good" performance is relative to each client's specific campaign goals.
- **Lightweight DB Staging**: Assess if a serverless database (e.g., BigQuery or SQLite) should be introduced from day one instead of Google Sheets, to automate ingestion earlier.
