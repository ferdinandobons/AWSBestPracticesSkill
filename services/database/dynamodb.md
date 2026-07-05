# Amazon DynamoDB — Best Practices

## Common scenarios
- High-scale key-value and document workloads for web/mobile apps        → Performance Efficiency, Cost Optimization
- Serverless application backends (Lambda + API Gateway + DynamoDB)        → Reliability, Performance Efficiency
- Multi-region active-active applications needing low-latency global access        → Reliability
- Time-series and high-volume event ingestion        → Performance Efficiency, Cost Optimization

## 🔒 Security
- **[encryption at rest]** Rely on DynamoDB's default encryption at rest, and choose an AWS owned, AWS managed, or customer managed KMS key based on how much control you need over key rotation and auditing. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-preventative.html)
- **[authentication]** Use IAM roles rather than long-term credentials for applications and services accessing DynamoDB, since roles provide temporary, automatically rotated access keys. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-preventative.html)
- **[authorization]** Attach least-privilege IAM policies scoped to specific DynamoDB actions and resources rather than granting broad table access. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-preventative.html)
- **[fine-grained access]** Use IAM policy conditions to restrict access down to specific items and attributes (attribute-based access control) instead of granting table-wide read/write access. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-preventative.html)
- **[network isolation]** Use gateway or interface VPC endpoints (AWS PrivateLink) so traffic between your VPC and DynamoDB never traverses the public internet. [doc](https://aws.amazon.com/dynamodb/features/)
- **[monitoring]** Enable AWS CloudTrail to log both control-plane and data-plane DynamoDB API activity for audit and security investigation. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-detective.html)
- **[key usage auditing]** Monitor AWS managed KMS key usage via CloudTrail when using KMS-based encryption at rest, to track who accessed encryption keys and when. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices-security-detective.html)

## 🛡️ Reliability
- **[backups]** Enable point-in-time recovery (PITR) so tables can be restored to any second within the last 1–35 days, protecting against accidental writes or deletes. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backup-and-Restore.html)
- **[backups]** Use on-demand backups for long-term retention and regulatory archiving needs in addition to continuous PITR backups. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backup-and-Restore.html)
- **[restore settings]** After restoring a table from backup, explicitly reapply settings that are not carried over automatically, such as auto scaling, streams, and TTL configuration. [doc](https://aws.amazon.com/blogs/database/backup-strategies-for-amazon-dynamodb/)
- **[multi-region]** Use DynamoDB global tables to replicate data across Regions for multi-region resilience, and enable PITR on each replica independently. [doc](https://aws.amazon.com/dynamodb/faqs/)
- **[failover readiness]** Understand your global tables replication model and define clear RPO/RTO targets, then continuously monitor replication health rather than assuming multi-Region presence alone guarantees recovery. [doc](https://aws.amazon.com/blogs/database/best-practices-for-amazon-dynamodb-global-tables-part-1-operational-readiness/)
- **[failover connectivity]** When failing over to another Region, verify that IAM policies, VPC endpoints, security groups, and network ACLs are also correctly configured in the target Region, since these are common causes of failover connectivity failures. [doc](https://aws.amazon.com/blogs/database/best-practices-for-amazon-dynamodb-global-tables-part-2-failover-strategies/)
- **[partition design]** Design partition keys with a large number of distinct values accessed uniformly to avoid hot partitions, since adaptive capacity only helps within a partition's maximum throughput limits. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)

## ⚡ Performance Efficiency
- **[partition keys]** Design and use partition keys effectively so that request traffic is distributed as uniformly as possible across all logical partition key values, in the base table and in every secondary index. [doc](https://aws.amazon.com/blogs/database/make-a-new-years-resolution-follow-amazon-dynamodb-best-practices/)
- **[sort keys]** Use well-designed composite sort keys to gather related data together for efficient querying and to model hierarchical one-to-many relationships. [doc](https://aws.amazon.com/blogs/database/make-a-new-years-resolution-follow-amazon-dynamodb-best-practices/)
- **[secondary indexes]** Use global and local secondary indexes deliberately — sparse indexes and materialized aggregation patterns avoid the added cost and reduced performance of inefficient index usage. [doc](https://aws.amazon.com/blogs/database/make-a-new-years-resolution-follow-amazon-dynamodb-best-practices/)
- **[large items]** Compress large attributes, split large items across multiple items indexed by sort key, or offload large payloads to Amazon S3 (storing only the object reference in DynamoDB) to work within per-item size limits. [doc](https://aws.amazon.com/blogs/database/make-a-new-years-resolution-follow-amazon-dynamodb-best-practices/)
- **[time-series data]** For time-series workloads, break from the single-table guideline and use one table per application per time period so you can tune throughput and manage older data independently. [doc](https://aws.amazon.com/blogs/database/make-a-new-years-resolution-follow-amazon-dynamodb-best-practices/)
- **[write sharding]** Add a random or calculated suffix to partition keys (write sharding) to spread heavy write activity across more partitions when a single logical key would otherwise become a hot spot. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- **[caching]** Add Amazon DynamoDB Accelerator (DAX) in front of read-heavy, low-latency workloads to cut response times and reduce read pressure on the underlying table. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/evaluate-dax-suitability.html)
- **[caching sizing]** Size DAX clusters using expected cache-hit ratio and TTL settings, since a cache miss consumes roughly 10x the cluster resources of a hit. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/dax-cluster-sizing.html)

## 💰 Cost Optimization
- **[capacity mode]** Choose on-demand capacity mode for new or unpredictable workloads, and switch to provisioned capacity with auto scaling once traffic patterns become predictable, to avoid paying for unused throughput. [doc](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/capacity.html)
- **[reserved capacity]** Use reserved capacity for stable, predictable provisioned workloads to reduce steady-state throughput costs. [doc](https://aws.amazon.com/blogs/database/motivations-for-migration-to-amazon-dynamodb/)
- **[scheduled scaling]** Combine auto scaling with scheduled minimum-throughput changes for provisioned tables so capacity increases ahead of known peak periods without throttling delay. [doc](https://aws.amazon.com/blogs/database/optimize-costs-by-scheduling-provisioned-capacity-for-amazon-dynamodb/)
- **[data lifecycle]** Enable Time to Live (TTL) to automatically expire and delete items that are no longer needed, reducing storage costs at no additional charge for in-Region deletes. [doc](https://aws.amazon.com/blogs/database/motivations-for-migration-to-amazon-dynamodb/)
- **[infrequent access]** Use the Standard-Infrequent Access table class for tables holding data that is accessed infrequently, to reduce storage cost. [doc](https://aws.amazon.com/blogs/database/motivations-for-migration-to-amazon-dynamodb/)
- **[caching]** Add a DAX caching layer to reduce reads against the base table for read-heavy workloads, since the reduced table-read cost can outweigh the cost of the cache cluster. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/evaluate-dax-suitability.html)
- **[capacity switching]** For spiky, event-driven traffic (e.g. seasonal peaks), switch a table temporarily to on-demand mode and back to provisioned mode afterward, since DynamoDB allows a mode change once per 24 hours. [doc](https://aws.amazon.com/smart-business/resources-for-smb/database-costs/)

## ⚙️ Operational Excellence
- **[monitoring]** Use CloudWatch metrics and alarms on DynamoDB tables to track throttling, latency, and consumed capacity, and to get notified automatically of anomalies. [doc](https://aws.amazon.com/dynamodb/features/)
- **[hot key detection]** Enable CloudWatch Contributor Insights for DynamoDB to identify the most-accessed and most-throttled partition keys without impacting table performance. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html)
- **[throttling visibility]** Enable Contributor Insights in `throttled-keys-only` mode on production tables to get near real-time visibility into throttling hot keys at minimal monitoring cost. [doc](https://aws.amazon.com/blogs/database/enhanced-throttling-observability-in-amazon-dynamodb/)
- **[change auditing]** Use an Amazon EventBridge rule to monitor DynamoDB control-plane operations (CreateTable, DeleteTable, UpdateTable) and notify via SNS when schema changes occur. [doc](https://aws.amazon.com/blogs/database/enable-fine-grained-access-control-and-observability-for-api-operations-in-amazon-dynamodb/)
- **[Well-Architected review]** Run the Amazon DynamoDB Well-Architected Lens review to get actionable, workload-specific recommendations across all six Well-Architected pillars. [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-wal.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
