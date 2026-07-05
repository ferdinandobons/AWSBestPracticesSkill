# Amazon Managed Service for Apache Flink — Best Practices

## Common scenarios
- Real-time stream processing and analytics on Kinesis/Kafka data        → Performance Efficiency, Reliability
- Stateful streaming applications (aggregations, joins, windowing)        → Reliability, Cost Optimization
- Continuous SQL/Python/Scala analytics via Studio notebooks        → Operational Excellence, Performance Efficiency
- Event-driven pipelines feeding S3, Firehose, or downstream databases        → Security, Reliability

## 🔒 Security
- **[IAM]** Grant the application's service execution role only the least-privilege permissions needed for its sources and sinks — avoid broad wildcard actions. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/security-best-practices.html)
- **[credentials]** Use IAM roles for application access to Kinesis, Firehose, S3, or MSK instead of embedding long-term credentials in code or JARs — store any non-IAM secrets (e.g., database passwords) in AWS Secrets Manager. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[encryption]** Implement server-side encryption on dependent resources (Kinesis streams, Firehose delivery streams, S3 buckets) — the service's own data at rest and in transit is already encrypted and cannot be disabled, but dependent resources are not covered automatically. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/security-best-practices.html)
- **[encryption]** Use a customer-managed KMS key for durable application storage (checkpoints/snapshots) and running application state — this gives you direct control over key rotation and access instead of relying solely on AWS-owned keys. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/data-protection.html)
- **[networking]** Connect the application to a VPC with private subnets when it must reach private resources such as an Amazon MSK cluster — VPC-connected applications have no internet access unless the VPC configuration explicitly allows it. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/vpc.html)
- **[auditability]** Enable AWS CloudTrail for the service — it records the request, source IP, principal, and timing of every API call, letting you trace who changed an application and when. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/security-best-practices.html)

## 🛡️ Reliability
- **[fault tolerance]** Keep checkpointing enabled in production — it provides fault tolerance during scheduled maintenance, service issues, and dependency failures. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[fault tolerance]** Set `SnapshotsEnabled` to `false` during development/troubleshooting and `true` once stable in production, taking snapshots several times a day — a snapshot is created on every stop, which is risky while the app is unhealthy but valuable for clean production restarts. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[connectors]** Use Kinesis connector version 1.15.2 or newer when running Flink runtime 1.15+ — older versions can cause consistency issues or break the Stop-with-Savepoint flow needed for clean updates. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[state management]** Avoid changing `maxParallelism` on an existing application unless necessary — doing so prevents restoring from previously taken snapshots, so the app can only be restarted without a snapshot. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/how-scaling.html)
- **[time semantics]** Apply a watermark strategy with `withIdleness` when reading from Kinesis or Kafka sources with idle shards/partitions — this prevents idle subtasks from stalling event-time progress and blocking time windows from closing. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[coding]** Never call `system.exit()` in application code or user-defined functions — throw an `Exception`/`RuntimeException` instead so the service can handle job failure and restart correctly. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)

## ⚡ Performance Efficiency
- **[parallelism]** Monitor sources and sinks with CloudWatch and verify they are sufficiently provisioned and not throttled — under-provisioned dependencies limit application throughput regardless of Flink parallelism. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[parallelism]** Tune per-operator parallelism with `setParallelism` instead of relying on a single application-wide value — uniform parallelism across all operators can bottleneck some and over-provision others, especially at high scale. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[parallelism]** Restructure sources with few shards/partitions to pass raw bytes and rebalance before deserializing when application parallelism exceeds shard count — this spreads deserialization work across all subtasks instead of leaving most idle. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[scaling]** Size `ParallelismPerKPU` deliberately for I/O-bound or blocking operations — a higher value increases parallel tasks scheduled per KPU and improves utilization of allocated compute. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/how-scaling.html)
- **[packaging]** Keep the uber JAR minimal by excluding runtime-provided dependencies, test-only dependencies, unused libraries, and static data/metadata (load these from S3 at runtime instead) — this reduces JAR size and improves deployment/restart times. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[logging]** Avoid logging every processed record — per-record logging causes severe bottlenecks and backpressure in the processing pipeline. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)

## 💰 Cost Optimization
- **[scaling]** Disable automatic scaling during testing to manually tune `Parallelism` and `ParallelismPerKPU` first — this finds the right sizing baseline before you enable autoscaling for variable production throughput. [doc](https://aws.amazon.com/blogs/big-data/real-time-cost-savings-for-amazon-managed-service-for-apache-flink/)
- **[scaling]** Use scheduled scaling instead of reactive metric-based scaling when workload peaks are predictable by time of day or day of week — this avoids unnecessary KPU allocation during off-peak periods. [doc](https://aws.amazon.com/blogs/big-data/enable-metric-based-and-scheduled-scaling-for-amazon-managed-service-for-apache-flink/)
- **[fit-for-purpose]** Evaluate whether your workload genuinely needs Flink's stateful capabilities (joins, deduplication, exactly-once, windowing) before adopting it — stateless or high-latency-tolerant workloads may run more cheaply on simpler compute such as AWS Lambda or containers. [doc](https://aws.amazon.com/blogs/big-data/real-time-cost-savings-for-amazon-managed-service-for-apache-flink/)
- **[state size]** Monitor checkpoint size and duration trends, including their rate of change — growing checkpoints consume more compute cycles and storage for checkpointing, increasing cost over time. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/monitoring.html)

## ⚙️ Operational Excellence
- **[monitoring]** Build a monitoring plan that covers source ingestion, consumption lag, and sink delivery, not just Flink-internal metrics — this catches problems anywhere along the pipeline, not only inside the Flink job. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/monitoring.html)
- **[monitoring]** Track `records_lag_max`/`millisBehindLatest`, `cpuUtilization`/`heapMemoryUtilization`, `downtime`, and `lastCheckpointSize`/`lastCheckpointDuration` (plus their rate of change) — together these surface consumer lag, resource pressure, outages, and state-growth problems early. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/monitoring.html)
- **[alarms]** Create CloudWatch alarms on resource utilization, checkpoint metrics, and application status changes — proactive alarms catch emerging problems before they fully unravel and become harder to mitigate. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/monitoring-metrics-alarms.html)
- **[logging]** Enable CloudWatch Logs for the application — this lets you debug runtime issues and see when job status transitions to `FAILED`. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)
- **[operator hygiene]** Set an explicit UUID on every stateful operator — this lets operator state be reliably matched across application upgrades and code changes instead of relying on auto-generated IDs that can shift. [doc](https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
