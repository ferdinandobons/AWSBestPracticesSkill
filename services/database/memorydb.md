# Amazon MemoryDB — Best Practices

## Common scenarios
- Redis/Valkey-compatible durable primary database for low-latency workloads        → Reliability, Performance Efficiency
- Session store or leaderboard requiring in-memory speed with durability        → Performance Efficiency, Reliability
- Multi-Region active-active data access for globally distributed applications        → Reliability, Performance Efficiency
- Cost-optimized large datasets with infrequently accessed data        → Cost Optimization

## 🔒 Security
- **[network isolation]** Deploy MemoryDB clusters inside a VPC with private subnets across multiple Availability Zones — isolates the cluster and enables high availability. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/vpcs.mdb.html)
- **[network isolation]** Scope security group rules so only trusted clients can reach the cluster port — prevents unauthorized network access to nodes. [doc](https://aws.amazon.com/memorydb/features/)
- **[encryption in transit]** Require TLS 1.2 or later (TLS 1.3 recommended) with cipher suites supporting perfect forward secrecy (DHE/ECDHE) for client connections — protects data moving between clients and the cluster. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/infrastructure-security.html)
- **[encryption at rest]** Enable at-rest encryption using a customer-managed AWS KMS key for the transaction log and snapshot data — gives you control over key policies and rotation. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/encryption.html)
- **[authentication/authorization]** Use Redis OSS-compatible Access Control Lists (ACLs) to define per-user permissions rather than relying on a single shared credential — enforces least privilege at the data-access level. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/memorydb-security.html)
- **[IAM]** Grant only least-privilege IAM permissions for MemoryDB management actions, starting from AWS managed policies and narrowing with customer-managed policies — reduces blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Add conditions to IAM policies (e.g., require SSL, restrict by service) and validate policies with IAM Access Analyzer — catches overly permissive or non-functional policies before they're attached. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/security_iam_id-based-policy-examples.html)
- **[credentials]** Enable multi-factor authentication (MFA) on accounts used to manage MemoryDB resources — adds a control against credential compromise. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/data-protection.html)
- **[auditability]** Enable AWS CloudTrail logging for MemoryDB API and user activity — provides an audit trail for security investigations and compliance. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/data-protection.html)
- **[data handling]** Never place confidential or sensitive information in tags or free-form name fields — this data can surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/data-protection.html)

## 🛡️ Reliability
- **[high availability]** Configure at least one read replica per shard and enable Multi-AZ so a failed primary is automatically detected and replaced by a replica — minimizes downtime from node or AZ failure. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/faulttolerance.html)
- **[disaster recovery]** Use MemoryDB Multi-Region for applications that need near-zero RTO across AWS Regions, with automatic asynchronous replication and conflict resolution — protects against full Regional outages. [doc](https://aws.amazon.com/blogs/aws/amazon-memorydb-multi-region-is-now-generally-available/)
- **[monitoring]** Monitor the `MultiRegionClusterReplicationLag` metric for Multi-Region clusters and alarm on sustained elevation — signals replication delay or Regional degradation before it affects consistency. [doc](https://aws.amazon.com/blogs/database/build-low-latency-resilient-applications-with-amazon-memorydb-multi-region/)
- **[backup]** Enable automatic daily snapshots with a retention period sized to your recovery needs (up to 35 days) — durably persists data in Amazon S3 for recovery from operational or data-corruption failures. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/snapshots-automatic.html)
- **[capacity planning]** Provision enough free IP addresses in subnet groups before scaling shard or node counts — avoids failed scaling operations from exhausted CIDR ranges. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/components.html)
- **[scaling]** Perform vertical or horizontal scaling (online resharding) rather than recreating clusters — MemoryDB applies these changes without downtime or cluster restarts. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/cluster-resharding-online.html)

## ⚡ Performance Efficiency
- **[sizing]** Start with the minimal number of shards/replicas and node size needed, then scale out based on observed load rather than over-provisioning upfront — matches capacity to actual throughput and latency requirements. [doc](https://aws.amazon.com/blogs/compute/integrating-amazon-memorydb-for-redis-with-java-based-aws-lambda/)
- **[read scaling]** Add read replicas (commonly at least two per shard for read-heavy workloads) to scale read throughput, since MemoryDB serves all writes from the primary and reads from replicas — beyond the workload's needs, extra replicas add cost without further gains. [doc](https://aws.amazon.com/blogs/compute/integrating-amazon-memorydb-for-redis-with-java-based-aws-lambda/)
- **[write scaling]** Increase the number of shards to scale write throughput, since data is partitioned across shards and each shard has its own primary — the correct shard/replica balance should be validated with load testing on a staging environment matching production traffic. [doc](https://aws.amazon.com/blogs/compute/integrating-amazon-memorydb-for-redis-with-java-based-aws-lambda/)
- **[monitoring]** Track `CPUUtilization`, `EngineCPUUtilization`, `Evictions`, `SwapUsage`, `CurrConnections`, and latency metrics in CloudWatch, with alarms set before thresholds are breached — enables corrective action ahead of performance degradation. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/metrics.whichshouldimonitor.html)

## 💰 Cost Optimization
- **[storage tiering]** Use data tiering on R6gd node types for workloads that regularly access only a subset (for example, up to ~20%) of their dataset and can tolerate added SSD-read latency — lowers cost per GB versus memory-only nodes for large, infrequently-accessed datasets. [doc](https://aws.amazon.com/memorydb/features/)
- **[commitment discounts]** Purchase reserved nodes for steady-state workloads to save versus on-demand pricing, choosing a payment option (No/Partial/All Upfront) that fits cash-flow needs — reserved node discounts apply with size flexibility within a node family and Region. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/reserved-nodes-overview.html)
- **[right-sizing]** Regularly review reserved node purchase recommendations (for example via AWS Cost Optimization Hub / Trusted Advisor) to align commitments with actual usage patterns — avoids paying for unused reserved capacity. [doc](https://docs.aws.amazon.com/awssupport/latest/user/cost-optimization-checks.html)
- **[right-sizing]** Avoid over-provisioning replicas or shards beyond what load testing shows is needed — additional nodes beyond the workload's requirement add cost without improving performance. [doc](https://aws.amazon.com/blogs/compute/integrating-amazon-memorydb-for-redis-with-java-based-aws-lambda/)

## ⚙️ Operational Excellence
- **[observability]** Enable and review the full set of MemoryDB CloudWatch metrics (30+ available) and set alarms on key indicators rather than relying on ad hoc checks — supports proactive detection of operational issues. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/monitoring-cloudwatch.html)
- **[change management]** Apply scaling operations (online resharding, vertical scaling) through the supported no-downtime workflows instead of manual cluster recreation — keeps the cluster available during configuration changes. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/cluster-resharding-online.html)
- **[maintenance]** Schedule the snapshot window and maintenance window during low-utilization periods — reduces the operational impact of routine background tasks. [doc](https://docs.aws.amazon.com/memorydb/latest/devguide/snapshots-automatic.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
