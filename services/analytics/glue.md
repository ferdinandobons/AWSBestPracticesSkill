# AWS Glue — Best Practices

## Common scenarios
- Serverless ETL pipelines that transform and load data into a data lake        → Performance Efficiency, Cost Optimization
- Cataloging and discovering datasets across multiple data stores        → Security, Operational Excellence
- Incremental batch or streaming data processing on a recurring schedule        → Reliability, Cost Optimization
- Centralized metadata and fine-grained access control for a data lake        → Security, Reliability

## 🔒 Security
- **[Data Catalog]** Encrypt Data Catalog metadata and connection passwords with AWS KMS keys — protects sensitive schema and credential data at rest. [doc](https://docs.aws.amazon.com/glue/latest/dg/console-data-catalog-settings.html)
- **[ETL jobs]** Configure ETL jobs and development endpoints to write encrypted data at rest using AWS KMS keys, and encrypt job bookmarks and crawler/job logs — extends encryption across the full pipeline, not just the catalog. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-encryption-enforcement-in-aws-glue-using-an-aws-cloudformation-template.html)
- **[IAM]** Grant Glue access through identity-based IAM policies scoped to specific catalog resources (database/table ARNs) rather than broad wildcards — enforces least privilege for ETL and catalog operations. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-aws-glue/)
- **[Data Catalog]** Use resource-level IAM permissions and resource-based Data Catalog policies to restrict which users and roles can access specific databases, tables, and metadata operations — separates metadata access control from the underlying S3 data permissions. [doc](https://aws.amazon.com/blogs/big-data/restrict-access-to-your-aws-glue-data-catalog-with-resource-level-iam-permissions-and-resource-based-policies/)
- **[Data lake governance]** Use AWS Lake Formation to centrally manage and enforce fine-grained (database/table/column-level) permissions for Glue crawlers, ETL jobs, and the Data Catalog — ensures consuming engines like Athena and Redshift Spectrum only see authorized data. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-aws-glue/)
- **[Network]** Use interface VPC endpoints (AWS PrivateLink) to access AWS Glue APIs privately, and require TLS 1.2+ with perfect-forward-secrecy cipher suites for all client connections — keeps API traffic off the public internet and enforces modern transport security. [doc](https://docs.aws.amazon.com/glue/latest/dg/infrastructure-security.html)
- **[Connections]** When connecting Glue jobs to data stores in a VPC, scope database security groups to allow traffic only from the Glue job's security group (self-referencing rule) instead of broad CIDR ranges — limits lateral network exposure. [doc](https://aws.amazon.com/blogs/big-data/connecting-to-and-running-etl-jobs-across-multiple-vpcs-using-a-dedicated-aws-glue-vpc/)

## 🛡️ Reliability
- **[Job design]** Enable job bookmarks with `transformation_ctx` on sources, transforms, and targets so recurring jobs track processed data and avoid reprocessing or duplicating records on rerun. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html)
- **[Monitoring]** Set up Amazon CloudWatch alarms on Glue job metrics for out-of-memory conditions, straggling executors, and data backlog ratios between chained jobs — catches degraded runs before they cause downstream failures. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-glue-job-cloudwatch-alarms.html)
- **[Error handling]** Rely on AWS Glue's default retry behavior (automatic retries before failure notification) and route CloudWatch failure/success events to Lambda or SNS for automated remediation and alerting. [doc](https://aws.amazon.com/glue/faqs/)
- **[Data replication]** For multi-Region resilience, replicate the underlying Amazon S3 data (via S3 replication) alongside the Data Catalog metadata and Lake Formation permissions — metadata alone is not sufficient for a functional backup Region. [doc](https://aws.amazon.com/blogs/big-data/build-a-multi-region-and-highly-resilient-modern-data-architecture-using-aws-glue-and-aws-lake-formation/)

## ⚡ Performance Efficiency
- **[Spark tuning]** Establish a baseline tuning workflow — define performance goals, measure metrics, identify bottlenecks, then iterate — rather than changing parameters ad hoc. [doc](https://docs.aws.amazon.com/glue/latest/dg/performance.html)
- **[Spark tuning]** Scale cluster capacity and use the latest AWS Glue version to benefit from engine-level performance improvements before tuning individual jobs. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/tuning-aws-glue-for-apache-spark/introduction.html)
- **[Spark tuning]** Reduce the amount of data scanned, parallelize tasks, minimize planning overhead, and optimize shuffles and user-defined functions — the core levers for Glue Spark job performance. [doc](https://docs.aws.amazon.com/glue/latest/dg/tuning-aws-glue-for-apache-spark.html)
- **[Diagnostics]** Use the Spark UI (enabled through job configuration) and AWS Glue Observability metrics to pinpoint specific bottlenecks such as skewed partitions or underutilized workers before changing configuration. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-observability.html)
- **[Crawlers]** Enable incremental crawls so crawlers add only new partitions instead of rescanning the entire data source, and use include/exclude paths to limit the scope of each crawl. [doc](https://docs.aws.amazon.com/glue/latest/dg/incremental-crawls.html)
- **[Crawlers]** Generate partition indexes on large partitioned tables to speed up partition lookups for downstream query engines such as Athena, EMR, and Redshift Spectrum. [doc](https://aws.amazon.com/blogs/big-data/efficiently-crawl-your-data-lake-and-improve-data-access-with-aws-glue-crawler-using-partition-indexes/)
- **[Storage format]** Store data in an optimized columnar format such as Parquet on Amazon S3 to reduce data scanned and improve job throughput. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/serverless-etl-aws-glue/best-practices.html)

## 💰 Cost Optimization
- **[Job execution]** Use AWS Glue Flex execution for non-time-sensitive workloads such as preproduction jobs, testing, and batch loads to reduce compute cost when fast startup isn't required. [doc](https://aws.amazon.com/glue/features/)
- **[Job bookmarks]** Enable job bookmarks to process only newly arrived data on each scheduled run instead of a full scan, cutting both data scanned and job duration. [doc](https://aws.amazon.com/blogs/big-data/monitor-optimize-cost-glue-spark/)
- **[Sizing]** Right-size worker type and count, use auto scaling, and set an appropriate job timeout so jobs don't run (and bill) longer than necessary. [doc](https://aws.amazon.com/blogs/big-data/monitor-optimize-cost-glue-spark/)
- **[Version]** Upgrade to the latest AWS Glue version to take advantage of engine efficiency improvements that lower DPU-hour consumption. [doc](https://aws.amazon.com/blogs/big-data/monitor-optimize-cost-glue-spark/)
- **[Cost visibility]** Monitor DPU-hour usage and trends with AWS Cost Explorer (filtered on Glue ETL, Flex, and interactive session usage types) and track individual job run cost via the AWS Glue Studio Monitoring page or the `GetJobRun`/`GetJobRuns` APIs. [doc](https://aws.amazon.com/blogs/big-data/monitor-optimize-cost-glue-spark/)
- **[Crawlers]** Run crawlers only when schema changes are expected (not continuously), use incremental crawls, and scope them with include/exclude paths to minimize crawler runtime and cost. [doc](https://docs.aws.amazon.com/whitepapers/latest/cost-modeling-data-lakes/cost-optimization-in-analytics-services.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Send AWS Glue job metrics and logs to Amazon CloudWatch by default, and enable continuous logging to view real-time job logs during execution for faster troubleshooting. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-cloudwatch.html)
- **[Auditing]** Enable AWS CloudTrail logging for AWS Glue API calls to track which users and roles performed which actions, from where, and when — supports audit and compliance requirements. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-glue.html)
- **[Automation]** Use Amazon EventBridge and CloudWatch Events to trigger automated actions (such as Lambda functions) on job state changes, and chain crawlers and jobs with triggers and workflows to orchestrate multi-step pipelines. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-glue.html)
- **[Observability]** Enable Job Observability Metrics to get deeper insight into per-source and per-sink job behavior, improving triage time for failed or slow runs. [doc](https://docs.aws.amazon.com/glue/latest/dg/monitor-observability.html)

<!-- meta: last_reviewed=2026-07-05; sources=20 -->
