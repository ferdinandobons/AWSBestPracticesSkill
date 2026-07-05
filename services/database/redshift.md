# Amazon Redshift — Best Practices

## Common scenarios
- Enterprise data warehousing and BI reporting at petabyte scale        → Performance Efficiency, Cost Optimization
- Querying data lake files in Amazon S3 alongside warehouse tables (lakehouse)        → Performance Efficiency, Cost Optimization
- ETL/ELT pipelines feeding dashboards and downstream analytics        → Reliability, Operational Excellence
- Intermittent or bursty analytics workloads (dev/test, periodic batch jobs)        → Cost Optimization

## 🔒 Security
- **[network isolation]** Run Amazon Redshift inside a VPC and use security groups to restrict inbound traffic, keeping clusters off the public internet. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/security.html)
- **[public access]** Disable public accessibility on provisioned clusters and Serverless workgroups so connections are only permitted from within your VPC. [doc](https://aws.amazon.com/blogs/security/amazon-redshift-enhances-security-by-changing-default-behavior-in-2025/)
- **[data in transit]** Enforce SSL-enabled connections between client applications and the cluster to encrypt data in transit. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_security-overview.html)
- **[VPC routing]** Enable Enhanced VPC Routing so data traffic between the cluster and other data sources (e.g., Amazon S3) stays within the AWS network instead of the public internet. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/security.html)
- **[encryption at rest]** Turn on cluster encryption so all data in user-created tables is encrypted with AES-256, using either AWS KMS or your own hardware security modules to manage keys. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_security-overview.html)
- **[authentication]** Use IAM for access control, and use federated authentication with a SAML-2.0-compatible identity provider so users can access the warehouse without managing separate database passwords. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/security.html)
- **[authorization]** Map IAM roles to database users and implement least-privilege access with explicit `GRANT` statements and database roles aligned to business functions, rather than broad table-wide access. [doc](https://aws.amazon.com/blogs/big-data/optimize-your-tableau-integration-with-amazon-redshift-serverless/)
- **[fine-grained access]** Combine column-level access control with row-level security (RLS) policies to restrict which users or roles can see specific columns and rows, and keep RLS policy expressions simple to avoid unnecessary performance overhead. [doc](https://docs.aws.amazon.com/redshift/latest/dg/t_rls.html)
- **[sensitive data]** Apply dynamic data masking to selectively mask personal or sensitive data at query time based on job role and permission level. [doc](https://aws.amazon.com/blogs/big-data/optimize-your-tableau-integration-with-amazon-redshift-serverless/)
- **[auditing]** Integrate with AWS CloudTrail to audit all Amazon Redshift API calls for security investigation and compliance. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/security.html)
- **[monitoring]** Use Amazon CloudWatch to track failed login attempts and audit logging in addition to CloudTrail API activity tracking. [doc](https://aws.amazon.com/blogs/big-data/optimize-your-tableau-integration-with-amazon-redshift-serverless/)

## 🛡️ Reliability
- **[node failure]** Rely on Amazon Redshift's automatic detection and replacement of failed nodes, which maintains at least three copies of data (original, replica, and S3 backup) so the cluster can resume quickly. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/amazon-redshift-deep-dive.html)
- **[multi-AZ]** Use Multi-AZ deployment for provisioned RA3 clusters to keep compute resources available in a second Availability Zone, raising the SLA to 99.99% versus 99.9% for single-AZ. [doc](https://docs.aws.amazon.com/redshift/latest/mgmt/managing-cluster-multi-az.html)
- **[backups]** Rely on automatic incremental snapshots (every 8 hours or every 5 GB of data change per node) and configure retention up to 35 days, or a custom schedule, to meet your recovery needs. [doc](https://aws.amazon.com/blogs/big-data/implement-disaster-recovery-with-amazon-redshift/)
- **[long-term retention]** Take manual snapshots for on-demand, indefinitely retained backups needed for compliance, and delete them when no longer required since they accrue storage charges. [doc](https://aws.amazon.com/blogs/big-data/implement-disaster-recovery-with-amazon-redshift/)
- **[centralized backup]** Use AWS Backup to centralize and automate snapshot management and monitoring across multiple Amazon Redshift provisioned clusters. [doc](https://aws.amazon.com/blogs/big-data/implement-disaster-recovery-with-amazon-redshift/)
- **[disaster recovery]** Keep copies of snapshots in another AWS Region so you can restore the cluster there within minutes if a Regional service interruption occurs. [doc](https://docs.aws.amazon.com/whitepapers/latest/data-warehousing-on-aws/amazon-redshift-deep-dive.html)

## ⚡ Performance Efficiency
- **[sort keys]** Choose sort keys that match columns commonly used in `WHERE` clause filters to minimize the amount of data scanned per query. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)
- **[distribution style]** Choose a distribution style (and `DISTKEY` on columns frequently used in `JOIN` predicates) so that related data is collocated on the same node slices, minimizing data movement during query execution. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)
- **[compression]** Let `COPY` choose compression encodings automatically (or use `ANALYZE COMPRESSION`) rather than loading uncompressed data, to reduce I/O and storage. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)
- **[column sizing]** Define primary/foreign key constraints and use the smallest possible column size and appropriate date/time data types, since these choices affect storage and query performance. [doc](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)
- **[data loading]** Use the `COPY` command to load data in parallel across all compute nodes instead of single-row `INSERT` statements, and split files so the file count is a multiple of the cluster's total slice count. [doc](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-techniques-for-amazon-redshift/)
- **[file sizing]** Compress load files (GZIP, LZO, or columnar formats like Parquet/ORC) and target compressed file sizes between 1 MB and 1 GB for optimal `COPY` throughput. [doc](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-techniques-for-amazon-redshift/)
- **[advisor recommendations]** Follow Amazon Redshift Advisor recommendations on distribution style, sort keys, and WLM configuration, since Advisor analyzes actual cluster workload patterns. [doc](https://aws.amazon.com/blogs/apn/best-practices-from-onica-for-optimizing-query-performance-on-amazon-redshift/)
- **[workload prioritization]** Use workload management (WLM) to flexibly manage query priorities and resource allocation so short, fast queries aren't stuck behind long-running ones. [doc](https://aws.amazon.com/blogs/big-data/manage-your-workloads-better-using-amazon-redshift-workload-management/)

## 💰 Cost Optimization
- **[intermittent workloads]** Pause clusters that are only needed at specific times (e.g., periodic ETL or reporting) to suspend on-demand compute billing while retaining storage and data. [doc](https://docs.aws.amazon.com/redshift/latest/mgmt/rs-mgmt-pause-resume-cluster.html)
- **[scheduling]** Automate pause and resume actions on a recurring schedule that matches operational needs instead of leaving clusters running around the clock. [doc](https://aws.amazon.com/blogs/big-data/lower-your-costs-with-the-new-pause-and-resume-actions-on-amazon-redshift/)
- **[reserved capacity]** Purchase Reserved Instances (provisioned) or Reservations (Serverless RPUs) for steady-state, predictable usage to reduce costs versus on-demand pricing. [doc](https://aws.amazon.com/blogs/big-data/getting-the-most-out-of-your-analytics-stack-with-amazon-redshift/)
- **[reservation sizing]** Analyze historical RPU or on-demand usage with the Redshift Serverless dashboard or Cost Explorer before committing to a reservation level, since actual savings depend on how closely the commitment matches real usage. [doc](https://aws.amazon.com/blogs/big-data/save-up-to-24-on-amazon-redshift-serverless-compute-costs-with-reservations/)
- **[data loading efficiency]** Compress load data and load via `COPY` in parallel, since inefficient loads consume more cluster compute resources and increase cost as well as latency. [doc](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-techniques-for-amazon-redshift/)

## ⚙️ Operational Excellence
- **[workload monitoring]** Define WLM query monitoring rules (QMRs) with metrics-based predicates (e.g., runtime, row count, CPU time) to automatically log, hop, or abort queries that exceed performance boundaries. [doc](https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html)
- **[rogue queries]** Use query monitoring rules to detect and manage rogue or runaway queries that would otherwise consume a disproportionate share of cluster resources. [doc](https://aws.amazon.com/blogs/big-data/manage-query-workloads-with-query-monitoring-rules-in-amazon-redshift/)
- **[threshold tuning]** Query the `SVL_QUERY_METRICS_SUMMARY` system view to determine appropriate threshold values before defining new query monitoring rules. [doc](https://aws.amazon.com/blogs/big-data/manage-your-workloads-better-using-amazon-redshift-workload-management/)
- **[table review]** Prioritize table design optimizations (sort keys, distribution, compression) against the tables with the highest scan frequency and size, since large clusters can have thousands of tables. [doc](https://aws.amazon.com/blogs/big-data/amazon-redshift-engineerings-advanced-table-design-playbook-preamble-prerequisites-and-prioritization/)
- **[Well-Architected review]** Use the AWS Well-Architected Data Analytics Lens to assess Amazon Redshift workloads against proven design patterns across security, reliability, performance, cost, and operations. [doc](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/analytics-lens.html)

<!-- meta: last_reviewed=2026-07-05; sources=20 -->
