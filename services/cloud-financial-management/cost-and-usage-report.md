# AWS Cost and Usage Report — Best Practices

## Common scenarios
- Building a single source of truth for hourly, resource-level cost and usage data        → Cost Optimization, Operational Excellence
- Querying billing data at scale with Athena/Redshift/QuickSight for FinOps reporting        → Performance Efficiency, Cost Optimization
- Feeding cost data into cross-account or organization-wide dashboards (CUDOS/CID)        → Operational Excellence, Cost Optimization
- Migrating from legacy CUR to CUR 2.0 / Data Exports for more stable pipelines        → Reliability, Operational Excellence

## 🔒 Security
- **[S3 destination bucket]** Create a dedicated Amazon S3 bucket for Cost and Usage Report delivery — this simplifies future access control and avoids conflicts with unrelated object policies. [doc](https://aws.amazon.com/blogs/aws-cloud-financial-management/querying-your-aws-cost-and-usage-report-using-amazon-athena/)
- **[bucket policy]** Do not edit the auto-applied billingreports.amazonaws.com bucket policy or change bucket ownership after report creation — either action prevents AWS from delivering reports. [doc](https://docs.aws.amazon.com/cur/latest/userguide/cur-s3.html)
- **[bucket policy]** Scope the resource-based bucket policy to the specific `aws:SourceArn` and `aws:SourceAccount` conditions — this ensures only your own report definitions can write to the bucket. [doc](https://docs.aws.amazon.com/cur/latest/userguide/cur-s3.html)
- **[IAM]** Deny IAM user and role access to the CUR S3 bucket for principals who don't need billing visibility — the delivery policy is resource-based and does not itself restrict who else can read the bucket. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/billing-example-policies.html)
- **[AWS Organizations]** Plan for a dedicated data-collection account to own the CUR S3 bucket — cross-account delivery to a bucket owned by another account is not supported. [doc](https://docs.aws.amazon.com/cur/latest/userguide/cur-consolidated-billing.html)

## 🛡️ Reliability
- **[report configuration]** Configure automatic refresh with "overwrite existing report" versioning — downstream consumers then always read a consistent, up-to-date file instead of accumulating stale versions. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_detailed_source.html)
- **[delivery timeline]** Design ingestion pipelines to tolerate up to 24 hours for first delivery and at least one update per day thereafter — mid-month figures are estimates that keep changing until the bill is finalized. [doc](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html)
- **[cumulative reports]** Build ingestion logic that replaces rather than appends monthly data — each in-month report update is cumulative for the whole month, and a new report starts fresh at the next billing period. [doc](https://docs.aws.amazon.com/cur/latest/userguide/understanding-report-versions.html)
- **[post-finalization changes]** Re-pull finalized months instead of caching them permanently — AWS can still update a finalized report for refunds, credits, or Support fees, typically reflected around the 6th–7th of the following month. [doc](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html)
- **[backfill]** Expect a delay before retroactive cost allocation tag changes appear in CUR — backfills only flow through after the normal ~24-hour report refresh cycle. [doc](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-backfill.html)

## ⚡ Performance Efficiency
- **[file format]** Enable Athena/Parquet report data integration — reports are then delivered in compressed, columnar Apache Parquet and auto-partitioned by year and month, reducing data scanned per query. [doc](https://aws.amazon.com/blogs/aws-cloud-financial-management/querying-your-aws-cost-and-usage-report-using-amazon-athena/)
- **[Athena setup]** Use a dedicated S3 bucket and dedicated CUR report specifically for Athena integration — AWS CUR supports only Parquet for Athena and overwrites prior reports in that bucket. [doc](https://docs.aws.amazon.com/cur/latest/userguide/cur-query-athena.html)
- **[query cost]** Query CUR data through Amazon Athena using the Parquet-formatted export rather than raw CSV — this cuts the amount of data scanned per query. [doc](https://aws.amazon.com/blogs/aws-cloud-financial-management/querying-your-aws-cost-and-usage-report-using-amazon-athena/)
- **[analytics pipeline]** Use AWS Glue to catalog and prepare CUR data ahead of Athena/QuickSight analysis — this avoids building and operating a custom data warehouse. [doc](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/cost_monitor_usage_detailed_source.html)

## 💰 Cost Optimization
- **[granularity]** Enable hourly granularity and include resource IDs in the CUR — this gives the most detailed, accurate view of cost and usage for optimization decisions. [doc](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/cost_monitor_usage_detailed_source.html)
- **[report configuration]** Configure the CUR with automatic refresh, overwrite versioning, and Athena/Parquet data integration together — this is the Well-Architected Cost Optimization pillar's recommended baseline configuration. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_detailed_source.html)
- **[storage lifecycle]** Apply S3 Lifecycle policies to older CUR objects to transition or expire them — this controls storage costs for accumulated historical reports. [doc](https://aws.amazon.com/s3/faqs/)
- **[CUR 2.0 / Data Exports]** Migrate to Cost and Usage Report 2.0 via AWS Data Exports and select only needed columns/rows with basic SQL — this reduces the volume of data exported and processed downstream. [doc](https://docs.aws.amazon.com/cur/latest/userguide/dataexports-migrate.html)
- **[Athena query cost]** Keep CUR data in Parquet with year/month partitioning — this lets Athena's per-byte-scanned pricing benefit from partition pruning and columnar compression. [doc](https://aws.amazon.com/blogs/aws-cloud-financial-management/querying-your-aws-cost-and-usage-report-using-amazon-athena/)

## ⚙️ Operational Excellence
- **[detailed data sources]** Configure at least one CUR with hourly granularity and all identifiers and resource IDs — pair it with Cost Explorer's hourly and resource-level data as your organization's detailed cost data source. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_detailed_source.html)
- **[application logging alignment]** Align application logging granularity to at least hourly — this lets business outcomes be correlated directly with CUR cost and usage data. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_detailed_source.html)
- **[dashboards]** Deploy Cloud Intelligence Dashboards (CUDOS/CID) or the built-in Cost and Usage Dashboard on top of CUR/CUR 2.0 data — this gives FinOps, engineering, and executive teams self-service visibility without a custom BI build. [doc](https://docs.aws.amazon.com/guidance/latest/cloud-intelligence-dashboards/cudos-cid-kpi.html)
- **[multi-account]** Centralize CUR delivery into a dedicated data-collection account and replicate to other accounts with S3 replication if needed — CUR cannot be delivered directly cross-account. [doc](https://aws.amazon.com/blogs/mt/visualize-and-gain-insights-into-your-aws-cost-and-usage-with-cloud-intelligence-dashboards-using-amazon-quicksight/)
- **[access management]** Secure dashboard and data access with IAM and AWS IAM Identity Center, and apply QuickSight row-level security where needed — this keeps team-level cost visibility scoped appropriately. [doc](https://docs.aws.amazon.com/guidance/latest/cloud-intelligence-dashboards/cudos-cid-kpi.html)
- **[schema stability]** Prefer CUR 2.0's fixed schema over the legacy CUR's variable, usage-dependent schema — this reduces breakage in downstream ETL and BI pipelines. [doc](https://docs.aws.amazon.com/cur/latest/userguide/dataexports-migrate.html)

<!-- meta: last_reviewed=2026-07-05; sources=14 -->
