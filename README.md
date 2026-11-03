# My_Linkedin_Posts_Analysis_V1

![Untitled design](https://github.com/user-attachments/assets/c8217b07-758d-4c4d-b4d7-6276456ffc2f)

**Title:** LinkedIn Post Engagement Analysis

**Subtitle:** Content Performance and Audience Engagement Insights

**Data Source:** Personal LinkedIn Post Analytics Data

**Tools:** Python, Excel and Power BI 
<code></a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.microsoft.com/en-in/microsoft-365/excel" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg" alt="Microsoft_Excel" width="40" height="40"/>  </a> <a href="https://powerbi.microsoft.com/en-in/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg" alt="powerbi" width="40" height="40"/>


# Methodology

To begin the analysis, I downloaded 92 individual Excel sheets containing engagement data for each LinkedIn post. Using Python, I consolidated these files into a single, unified dataset. To align the data structure with the analysis requirements, I applied the transpose function to reshape the data. Further, I manually preprocessed and cleaned the data in Excel to address any inconsistencies. Finally, I imported the cleaned data into Power BI, where I designed an interactive dashboard to visualize insights in an engaging and accessible format for my audience.

# Analysis Insights

1. Top Content Type: Video posts generated significantly higher engagement than text posts, indicating a preference for multimedia content within my audience.

2. Peak Engagement Times: Engagement rates peaked on weekdays between 10 a.m. and 1 p.m., suggesting the most effective posting times for maximum visibility.

3. Audience Interaction: Posts that included questions or calls to action received higher average comments and shares, showing that engagement is driven by interactive content.

4. Popular Topics: Data-related topics, especially insights on Power BI and Python, attracted the most views and reactions, highlighting audience interest in data analytics and technical skills.

5. Monthly Trends: Engagement was highest in August, with a noticeable increase in views and reactions, potentially indicating seasonal patterns in content consumption.


# Recommendations

1. Increase Video Content: Given the higher engagement for video posts, consider creating more video-based content or incorporating multimedia elements to increase overall engagement.

2. Optimal Posting Schedule: Based on peak engagement times, schedule posts for mid-morning on weekdays to maximize reach and visibility among the target audience.

3. Engage with Interactive Content: To drive more interaction, include questions or prompts in posts, encouraging audience participation and discussions.

4. Focus on High-Interest Topics: Regularly share insights related to data analysis tools like Power BI and Python, as these topics align with audience interests and engagement patterns.

5. Test Content Variations: Experiment with different types of content and track engagement to continuously refine posting strategies based on evolving audience preferences.

   # LinkedIn-Engagement-Connect-Post-Analytics-V2

An end-to-end analytics project that transforms personal LinkedIn export data into structured, traceable datasets for analysing post performance, engagement, and available audience demographics. The workflow covers Excel export ingestion, Python-based ETL and validation, Flask, SQL storage and querying, and Power BI reporting.

The project focuses on solving practical data problems: duplicate exports, inconsistent metric labels, historical snapshots, incomplete demographic coverage, and the need to preserve data lineage from source files to final reports.

## The business problem

LinkedIn provides analytics exports, but the information is distributed across multiple Excel workbooks and worksheets. Files can contain overlapping historical snapshots, inconsistent field labels, and different levels of metric availability.

Analysing this data manually makes it difficult to maintain consistency, compare post performance over time, and trace reported values back to their original source.

This project builds a repeatable analytics workflow to consolidate the exports, standardize the data, preserve historical records, validate the results, and prepare the processed information for reporting.

## Pipeline

```mermaid
flowchart LR
    A[LinkedIn Analytics Exports] --> B[Python Ingestion]
    B --> C[File Inventory and Deduplication]
    C --> D[ETL, Standardization and QA]
    D --> E[Post, Snapshot and Demographic Datasets]
    E --> F[Flask Application Layer]
    F --> G[(SQL Database)]
    G --> H[Power BI Data Model]
    H --> I[Interactive Analytics Dashboard]
```

The Python, Flask, and SQL stages are completed. Power BI is the current reporting and validation phase.

## Data coverage

The V2 pipeline processes a collection of personal LinkedIn analytics exports.

| Dataset attribute | Recorded result |
| --- | ---: |
| Initial Excel workbooks | 204 |
| Unique file hashes identified | 160 |
| Duplicate file instances identified | 44 |
| Processed analytics workbooks / snapshots | 158 |
| Distinct LinkedIn post IDs | 107 |
| Canonical PostAnalytics files in field inventory | 118 |
| Distinct source field names | 127 |

The processed collection excludes exact duplicate files and two additional workbooks that were not part of the analytics dataset.

## What the pipeline handles

### 1. Data ingestion and file management

- Reads LinkedIn analytics Excel exports from the raw-data directory.
- Identifies export types, worksheets, and available fields.
- Generates a file inventory and uses file hashes to detect exact duplicates.
- Extracts post IDs from LinkedIn post URLs where available.
- Maintains source-file information for traceability.

### 2. Historical snapshot management

The same LinkedIn post can appear in multiple exports collected at different points in time.

Rather than overwriting earlier records, the pipeline preserves historical snapshots and creates a separate current-post dataset.

| Dataset | Purpose |
| --- | --- |
| `snapshot_fact` | Preserves available historical analytics snapshots. |
| `posts_current` | Selects one preferred available snapshot for each of the 107 distinct posts. |
| `file_manifest` | Maintains file-level inventory and lineage information. |

**Important:** Current means the newest preferred snapshot available in the collected exports. It does not represent live LinkedIn data.

### 3. Metric extraction and standardization

The pipeline converts extracted performance fields into a standardized long-form structure.

| Attribute | Recorded result |
| --- | ---: |
| Standardized metric rows | 1,751 |
| Standardized metrics | 23 |
| Distinct source / section / label mappings | 38 |
| Missing metric mappings at validation checkpoint | 0 |

Key datasets:

- `raw_fields_long` — extracted source fields before standardization.
- `metrics_long` — standardized metric records.
- `pa_metrics` — PostAnalytics-focused metric subset.

Metric labels such as `Comment` and `Comments`, and `Repost` and `Reposts`, are standardized while retaining source information.

Ambiguous concepts such as `Views` versus `Video views` and `Watch time` versus `Average watch time` are kept separate unless their equivalence can be established.

### 4. Audience demographic extraction

The pipeline also extracts available demographic information from LinkedIn export workbooks.

| Attribute | Result |
| --- | ---: |
| Workbooks containing demographic worksheets | 80 |
| Extracted demographic rows | 1,543 |
| Unique posts represented | 59 |
| Current demographic rows | 423 |
| Historical demographic rows | 1,120 |
| Exact duplicate rows in saved dataset | 0 |
| Missing values in saved dataset | 0 |

The processed demographic dataset is `demographics_snapshot_fact.csv`.

It contains the following fields:

`category`, `value`, `percentage`, `file_name`, `post_id`, `source_type`, `snapshot_ts`, and `is_current`.

A total of 27 percentage values recorded as `< 1%` were preserved as text rather than converted to zero.

Demographic availability is not uniform across posts. A missing demographic worksheet does not mean that the audience segment or activity is zero.

## Data quality and validation

Data quality is treated as part of the pipeline rather than as a final cleanup step.

Key checks include:

- File-hash validation to identify exact duplicate workbooks.
- Post ID extraction and snapshot grouping.
- Source-to-standardized metric mapping checks.
- Manifest and dataset lineage validation.
- Duplicate and missing-value checks on processed demographic data.
- Current versus historical snapshot identification.
- Round-trip validation of the exported demographic dataset.

**Data-handling principle:** Missing metrics remain missing rather than being automatically replaced with zero. Original source labels and file lineage are retained wherever available.

## Power BI dashboard

Power BI is the current stage of the project.

The reporting layer is being developed using the processed analytics datasets and completed SQL stage. The focus is on making post-performance and demographic information easier to explore while preserving the distinction between current and historical records.

The Power BI model and report should be validated for:

- Correct table relationships and dataset grain.
- Accurate post-level and snapshot-level counts.
- Reconciliation of report values against SQL and source exports.
- Correct handling of missing metrics and demographic coverage.
- Consistent filtering across posts, snapshots, and metric categories.

*Add final dashboard screenshots and exact report-page descriptions here once the Power BI implementation is finalized.*

## Tech stack

**Data processing:** Python, pandas, Jupyter Notebook, Excel

**Application layer:** Flask

**Database:** SQL

**Reporting and visualization:** Microsoft Power BI

**Data engineering concepts:** ETL, data validation, file-hash deduplication, data standardization, snapshot management, data lineage, and structured data modelling.

## Key design decisions

- **File hashes for duplicate detection:** Identical files are identified before downstream processing to prevent duplicate exports from inflating the dataset.
- **Post IDs for record grouping:** URL-derived post IDs connect analytics exports belonging to the same LinkedIn post.
- **Historical snapshots are preserved:** Earlier exports are retained instead of being overwritten by the latest available version.
- **Separate current and historical datasets:** This supports different analytical use cases without mixing snapshot history into current post-level reporting.
- **Long-form metric structure:** Standardized metric records provide a flexible structure for handling multiple performance indicators.
- **Conservative metric mapping:** Similar-looking labels are not automatically merged when their definitions may differ.
- **Missing data stays missing:** An unavailable metric or worksheet is not interpreted as zero.
- **Source lineage is retained:** Processed values can be traced back to their original export information.

## Problems addressed during development

| Data problem | Approach |
| --- | --- |
| Duplicate Excel exports | Used file hashes to identify exact duplicates. |
| Multiple exports for the same post | Extracted post IDs and grouped records into snapshots. |
| Historical records being overwritten | Preserved snapshot-level data separately from selected current records. |
| Inconsistent metric labels | Built standardized source-to-metric mappings. |
| Ambiguous metric definitions | Kept potentially different metrics separate until verified. |
| Incomplete demographic coverage | Preserved availability information rather than treating missing worksheets as zero. |
| `< 1%` demographic values | Retained the original text representation. |
| Source-to-output traceability | Maintained file, post, source-type, and snapshot metadata. |

The detailed development history and error-resolution record are maintained in the project documentation.

## Repository structure

```text
├── data/
│   ├── raw/                  # Original LinkedIn export workbooks
│   └── processed/            # Validated and transformed datasets
│
├── notebooks/                # Python ingestion, ETL and QA
│
├── app/                      # Flask application
│
├── sql/                      # SQL database scripts and queries
│
├── powerbi/                  # Power BI report and related assets
│
├── docs/
│   ├── images/               # Dashboard screenshots
│   └── LinkedIn_Post_Analytics_Project_Documentation_v1_1.docx
│
└── README.md
```

*Repository structure is illustrative. Adjust folder names to match the actual files committed to GitHub.*

## Running the project

The exact commands and configuration depend on the repository implementation. The general workflow is:

1. Place the LinkedIn analytics export workbooks in the configured raw-data directory.
2. Run the Python ingestion and ETL notebooks or scripts.
3. Review the generated file manifest, processed datasets, and validation results.
4. Run the Flask application using the project's configured environment and dependencies.
5. Configure the SQL database and execute the provided database scripts or loading workflow.
6. Connect Power BI to the configured SQL data source.
7. Refresh the model and validate selected report values against SQL and source exports.

**Data privacy:** This project uses personal LinkedIn analytics exports. Do not commit private exports, credentials, database passwords, or other sensitive information to the public repository. Use `.gitignore` and environment variables for local configuration.

## Limitations

- The analysis is limited to the LinkedIn exports collected by the account owner.
- The pipeline is not a live LinkedIn API integration.
- Historical coverage depends on the dates and availability of the collected exports.
- Demographic data is available for only a subset of posts.
- Demographic percentages represent the segments provided in the exports, not necessarily a complete audience distribution.
- Some metric labels require source-context verification before they can safely be combined.
- Current-post records represent selected local snapshots, not real-time performance.
- Power BI results depend on correct relationships, measures, and snapshot filtering.

## Future improvements

- Complete and validate the Power BI semantic model and report.
- Improve the refresh workflow so new exports can be processed with fewer manual steps.
- Strengthen automated validation and exception reporting.
- Add more historical comparison and post-performance analysis.
- Expand documentation with final dashboard screenshots, model relationships, and measure definitions.
- Improve the deployment and configuration documentation for the Flask and SQL components.

## Project documentation

The detailed project documentation covers the project background, data architecture, ETL methodology, dataset inventory, data-quality checks, known limitations, error-resolution history, and current Power BI development stage.

## Project purpose

Built as a practical portfolio project using personal LinkedIn analytics data to demonstrate data processing, ETL design, application and database integration, data-quality management, and business intelligence reporting.

*Feedback and questions are welcome.*
