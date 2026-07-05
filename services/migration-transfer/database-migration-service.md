# AWS Database Migration Service — Best Practices

## Common scenarios
- Homogeneous or heterogeneous database migration to AWS        → Reliability, Performance Efficiency
- Continuous change data capture (CDC) replication to keep source and target in sync        → Reliability, Operational Excellence
- Schema conversion and consolidation of migration tasks for large or partitioned tables        → Performance Efficiency, Cost Optimization
- Secure migration of sensitive data across VPCs and accounts        → Security

## 🔒 Security
- **[access control]** Use IAM identity-based policies and move from AWS managed policies toward least-privilege customer-managed policies for AWS DMS actions — limits who can create, modify, or delete replication resources. [doc](https://docs.aws.amazon.com/dms/latest/userguide/security_iam_id-based-policy-examples.html)
- **[access control]** Add IAM policy conditions (for example, requiring SSL/TLS on requests) and validate policies with IAM Access Analyzer — further restricts access and catches overly permissive statements. [doc](https://docs.aws.amazon.com/dms/latest/userguide/security_iam_id-based-policy-examples.html)
- **[encryption in transit]** Configure SSL/TLS on source and target endpoint connections — protects data as it moves between databases and the replication instance. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html)
- **[encryption at rest]** Use AWS KMS customer managed keys to encrypt replication instance storage and endpoint connection information — gives you control over key policies and rotation instead of relying on the default AWS owned key. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html)
- **[network isolation]** Deploy replication instances inside a VPC and scope security group rules so only required ingress is allowed on source/target endpoints — reduces the network attack surface for migration traffic. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html)
- **[credentials]** Store source and target database credentials in AWS Secrets Manager rather than embedding them in endpoint configuration — centralizes secret storage and avoids hardcoded passwords. [doc](https://aws.amazon.com/dms/features/)
- **[data protection]** Use AWS DMS data masking to obscure sensitive column values before they are loaded into the target — protects sensitive data exposed during migration. [doc](https://aws.amazon.com/dms/features/)

## 🛡️ Reliability
- **[high availability]** Enable the Multi-AZ option for replication instances used in ongoing replication — provisions a synchronously replicated standby that resumes tasks with minimal interruption if the primary fails. [doc](https://docs.aws.amazon.com/dms/latest/userguide/disaster-recovery-resiliency.html)
- **[data integrity]** Turn on data validation for migration tasks so AWS DMS compares source and target data after full load — surfaces discrepancies for resync rather than letting them go unnoticed. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[change capture]** Do not rely on AWS DMS CDC for use cases requiring sub-second or SLA-backed replication latency; use native database replication or purpose-built streaming for strict latency guarantees instead — CDC latency varies with source workload, network, and target ingestion capacity. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[change management]** Stop running AWS DMS tasks before upgrading source or target databases and resume them only after the upgrade completes — avoids replication errors during schema or engine changes. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[testing]** Run a small-scale proof of concept and a full-scale test migration before the production cutover — surfaces environment issues, realistic timelines, and throughput limits early. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[planning]** Run premigration assessments and available diagnostic support scripts before starting a task — identifies potential migration failures in advance. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)

## ⚡ Performance Efficiency
- **[replication instance sizing]** Size the replication instance based on CPU, memory, and network throughput needs, and monitor CloudWatch metrics like CPUUtilization, FreeableMemory, and SwapUsage to confirm it isn't under resource pressure — undersized instances cause CDC latency and swapping. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html)
- **[large tables]** Split large or partitioned tables across multiple tasks using row filtering or partitioned load (for example, by primary key range or date partition) — parallelizes full load and reduces migration time. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[LOB handling]** Use limited LOB mode where possible and create separate tasks for tables with large or frequently updated LOB columns — LOBs otherwise dominate memory usage and slow the rest of the migration. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[target throughput]** Turn off secondary indexes, unnecessary triggers, and (for RDS targets) backups/Multi-AZ during initial load, then re-enable them before or during cutover — removes contention for target write resources while loading. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[source load]** Reduce the number of concurrent tasks or tables per task if the source database is overburdened by full-load table scans or CDC log reads — consolidating tasks lowers change-capture overhead on the source. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[network]** Verify available network throughput and source archive/change-log generation rate between source, replication instance, and target — network or log-generation bottlenecks are common causes of CDC latency. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)

## 💰 Cost Optimization
- **[right-sizing]** Monitor replication instance utilization with CloudWatch metrics and scale the instance up for peak load (initial full load) and back down afterward — avoids paying for oversized capacity outside of peak periods. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[deployment type]** Use a single-AZ replication instance instead of Multi-AZ when the workload can tolerate replication lag and reduced availability — Multi-AZ increases cost and adds performance overhead when high availability isn't required. [doc](https://aws.amazon.com/blogs/database/replication-instance-sizing-for-optimal-database-migrations-with-aws-dms/)
- **[data transfer]** Keep replication instances, source, and target endpoints in the same Availability Zone/Region where possible — cross-AZ, cross-Region, or outbound data transfer incurs standard AWS data transfer charges while same-AZ transfer is free. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[estimation]** Use the AWS Pricing Calculator and AWS DMS pricing documentation to estimate replication instance and log storage costs before migrating — plans capacity against the primary cost drivers (instance hours and storage). [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)

## ⚙️ Operational Excellence
- **[monitoring]** Track host, replication task, and table-level CloudWatch metrics (for example, CDC latency, incoming/committed changes, rows loaded) from the AWS DMS console — gives visibility into task health and sizing decisions throughout the migration. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[alerting]** Configure CloudWatch alarms on key metrics such as FreeableMemory, CPUUtilization, and task latency, and route notifications through Amazon SNS — enables proactive detection of low memory, high CPU, or network disruptions before they stall replication. [doc](https://aws.amazon.com/blogs/database/setting-up-amazon-cloudwatch-alarms-for-aws-dms-resources-using-the-aws-cli/)
- **[troubleshooting]** Use AWS DMS task logs and event notifications to diagnose migration issues — task logs and DMS events surface errors and warnings that might not otherwise change the task's running state. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **[documentation review]** Review the AWS DMS public documentation for your specific source and target endpoints before the first migration — surfaces prerequisites and current engine-specific limitations ahead of time. [doc](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)

<!-- meta: last_reviewed=2026-07-05; sources=8 -->
