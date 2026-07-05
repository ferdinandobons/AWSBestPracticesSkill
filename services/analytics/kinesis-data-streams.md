# Amazon Kinesis Data Streams — Best Practices

## Common scenarios
- Real-time clickstream and application log ingestion        → Performance Efficiency, Cost Optimization
- Change data capture (CDC) and event-driven architectures        → Reliability, Performance Efficiency
- IoT telemetry and sensor data pipelines        → Performance Efficiency, Operational Excellence
- Multi-consumer fan-out for parallel real-time analytics        → Performance Efficiency, Cost Optimization

## 🔒 Security
- **[access control]** Grant only the specific Kinesis actions and stream resources a role or user actually needs — least privilege reduces the blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/streams/latest/dev/security-best-practices.html)
- **[authentication]** Use IAM roles to vend temporary credentials to producer and consumer applications instead of embedding long-term access keys in code or in an S3 bucket. [doc](https://docs.aws.amazon.com/streams/latest/dev/security-best-practices.html)
- **[encryption]** Enable server-side encryption with an AWS KMS key (AWS-managed or customer-managed) to protect data at rest in the stream. [doc](https://docs.aws.amazon.com/streams/latest/dev/server-side-encryption.html)
- **[auditability]** Enable AWS CloudTrail for Kinesis Data Streams so every API call is recorded with the caller identity, source IP, and timestamp for security analysis and forensics. [doc](https://docs.aws.amazon.com/streams/latest/dev/security-best-practices.html)
- **[network isolation]** Use interface VPC endpoints (AWS PrivateLink) so producers and consumers in a VPC reach Kinesis Data Streams without traversing the public internet. [doc](https://aws.amazon.com/kinesis/data-streams/faqs/)
- **[network isolation]** Attach a restrictive VPC endpoint policy to limit which Kinesis actions and streams are reachable through a given endpoint, combined with IAM policies that require access to originate from that endpoint. [doc](https://docs.aws.amazon.com/streams/latest/dev/vpc.html)
- **[cross-account access]** Use resource-based (stream) policies or cross-account IAM roles to share a stream with another account instead of distributing credentials. [doc](https://docs.aws.amazon.com/streams/latest/dev/controlling-access.html)

## 🛡️ Reliability
- **[data durability]** Set the retention period as a safety net long enough for consumers to recover from processing failures or downstream outages before data expires — Kinesis retains records from 24 hours up to 365 days. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html)
- **[capacity changes]** Decrease retention period with care — records older than the new retention become inaccessible almost immediately, unlike increases which take effect gradually. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html)
- **[scaling]** Reshard (split hot shards, merge cold shards) based on CloudWatch metrics or logged partition-key/shard-ID data rather than uniformly doubling all shards, to right-size capacity without overpaying. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding-strategies.html)
- **[capacity mode]** Use on-demand mode for unpredictable or spiky workloads so the stream automatically scales to handle bursts up to double the prior 30-day peak throughput without manual shard management. [doc](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html)
- **[capacity mode]** Retry throttled `PutRecord`/`PutRecords` requests, since on-demand streams can throttle for up to 15 minutes if traffic exceeds double the previous peak within a short window. [doc](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html)
- **[consumer resilience]** Implement duplicate-record handling and correct startup/shutdown/throttling logic in consumer applications, since at-least-once delivery and resharding can produce duplicate or re-delivered records. [doc](https://docs.aws.amazon.com/streams/latest/dev/advanced-consumers.html)
- **[hot shards]** Choose partition keys that distribute traffic evenly (e.g., random or high-cardinality keys) to avoid overloading individual shards and triggering `ProvisionedThroughputExceededException`; use provisioned mode with granular shard splits when a partition key is unavoidably skewed. [doc](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html)

## ⚡ Performance Efficiency
- **[consumer throughput]** Use enhanced fan-out (EFO) consumers when multiple applications must read the same stream at full speed — each EFO consumer gets a dedicated 2 MB/s per shard instead of sharing the default 2 MB/s pool. [doc](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html)
- **[consumer throughput]** Prefer the Kinesis Client Library (KCL) 2.x or later for building consumers, since it automatically subscribes to enhanced fan-out across all shards and handles low-latency push delivery over HTTP/2. [doc](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html)
- **[producer throughput]** Use the Kinesis Producer Library (KPL) for high-throughput or long-running producers, and tune aggregation and retry/rate-limit settings to maximize records per PutRecords call. [doc](https://docs.aws.amazon.com/streams/latest/dev/advanced-producers.html)
- **[ingestion tooling]** Pick the ingestion path that matches the source — KPL for custom high-performance producers, Kinesis agent for log/file ingestion, AWS DMS for CDC, or AWS IoT Core for device data — rather than building a single generic ingestion path for every source type. [doc](https://aws.amazon.com/blogs/big-data/architectural-patterns-for-real-time-analytics-using-amazon-kinesis-data-streams-part-1/)
- **[capacity sizing]** Use the Kinesis Shard Calculator (or the on-demand mode) to size provisioned streams so per-shard 1 MB/s write and 2 MB/s read limits aren't exceeded under expected load. [doc](https://aws.amazon.com/blogs/big-data/architectural-patterns-for-real-time-analytics-using-amazon-kinesis-data-streams-part-1/)
- **[consumer lag]** Monitor `GetRecords.IteratorAgeMilliseconds` (IteratorAge) per consumer and alarm before it approaches the retention period, since a growing iterator age signals the consumer is falling behind and records could expire before being processed. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-consuming-amazon-kinesis-data-streams-using-aws-lambda/)

## 💰 Cost Optimization
- **[capacity mode]** Use provisioned mode with a deliberately sized shard count for steady, predictable workloads to avoid paying for on-demand's automatic headroom. [doc](https://docs.aws.amazon.com/help-panel/KDS/latest/help-panel/kds-data-stream-capacity.html)
- **[capacity mode]** Use on-demand mode for spiky or hands-off workloads instead of over-provisioning shards for peak capacity that sits idle most of the time. [doc](https://aws.amazon.com/blogs/big-data/architectural-patterns-for-real-time-analytics-using-amazon-kinesis-data-streams-part-1/)
- **[resharding]** Merge underutilized ("cold") shards identified from CloudWatch metrics to reduce the per-shard hourly charge without impacting throughput headroom. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding-strategies.html)
- **[monitoring cost]** Enable shard-level (enhanced) CloudWatch metrics only where needed, since stream-level metrics are free but shard-level metrics incur additional CloudWatch charges. [doc](https://docs.aws.amazon.com/help-panel/KDS/latest/help-panel/kds-monitoring.html)
- **[retention]** Keep the default or shortest retention period that meets your recovery and replay requirements, since extended (beyond 24 hours) and long-term (beyond 7 days) retention incur additional charges. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html)
- **[fan-out cost]** Register and deregister enhanced fan-out consumers only for the duration they're needed (e.g., ad hoc backtesting) to avoid paying for idle dedicated throughput. [doc](https://aws.amazon.com/blogs/big-data/retaining-data-streams-up-to-one-year-with-amazon-kinesis-data-streams/)

## ⚙️ Operational Excellence
- **[monitoring]** Integrate with Amazon CloudWatch and monitor stream-level metrics continuously to catch throughput, latency, or error issues before they escalate. [doc](https://docs.aws.amazon.com/help-panel/KDS/latest/help-panel/kds-monitoring.html)
- **[monitoring]** Enable shard-level metrics to pinpoint hot shards or failing consumers at the individual-shard granularity rather than only at the aggregate stream level. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-consuming-amazon-kinesis-data-streams-using-aws-lambda/)
- **[monitoring]** Alarm on `ReadProvisionedThroughputExceeded` to detect when consumers are being throttled, and respond by adding shards or moving to an enhanced fan-out consumer. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-consuming-amazon-kinesis-data-streams-using-aws-lambda/)
- **[scaling operations]** Separate resharding/administrative operations into a dedicated administrative application with broader IAM permissions, keeping producer and consumer applications scoped to only the actions they need. [doc](https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding.html)
- **[scaling operations]** When using `UpdateShardCount`, target a shard count that is a multiple of 25% of the current count for faster, more predictable scaling completion. [doc](https://docs.aws.amazon.com/sdk-for-go/api/service/kinesis/index.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
