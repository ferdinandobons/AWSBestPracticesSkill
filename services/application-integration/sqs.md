# Amazon SQS — Best Practices

## Common scenarios
- Decoupling microservices and distributed system components        → Reliability, Performance Efficiency
- Buffering work between producers and consumers (e.g., image/order processing)        → Reliability, Cost Optimization
- Fan-out and event-driven processing triggering Lambda consumers        → Performance Efficiency, Operational Excellence
- Handling poison/unprocessable messages without blocking a queue        → Reliability, Operational Excellence

## 🔒 Security
- **[access control]** Grant least-privilege identity- and resource-based policies scoped to specific queues and API actions for administrators, producers, and consumers separately — reduces blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-security-best-practices.html)
- **[encryption]** Enable server-side encryption (SSE) with AWS KMS on queues carrying sensitive data, and grant `kms:GenerateDataKey`/`kms:Decrypt` only to the specific producer/consumer principals that need it — prevents unauthorized access to message content at rest. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-least-privilege-policy.html)
- **[cross-service access]** Use `aws:SourceArn`, `aws:SourceAccount`, and `aws:PrincipalOrgID` condition keys in the queue's KMS key policy and access policy when other AWS services (e.g., S3, SNS) publish to the queue — prevents the cross-service confused-deputy problem. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-least-privilege-policy.html)
- **[network isolation]** Use interface VPC endpoints (AWS PrivateLink) and queue policies restricting access to specific VPCs/VPC endpoints for queues that must never be reachable from the public internet. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-internetwork-traffic-privacy.html)
- **[policy validation]** Validate identity-based policies with IAM Access Analyzer and start from AWS managed policies before narrowing to customer-managed least-privilege policies — catches overly permissive or malformed statements before they're attached. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-basic-examples-of-iam-policies.html)
- **[transport security]** Require clients to use TLS 1.2+ with Perfect Forward Secrecy cipher suites when calling the SQS API — protects messages in transit. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/infrastructure-security.html)

## 🛡️ Reliability
- **[error handling]** Configure a redrive policy with a `maxReceiveCount` high enough to allow legitimate retries, and route failed messages to a dead-letter queue — isolates poison messages so they don't block healthy processing. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- **[DLQ recovery]** Use dead-letter queue redrive to move unconsumed messages back to the source (or another compatible) queue once the consumer issue is fixed, instead of building custom redrive tooling. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html)
- **[visibility timeout]** Set the visibility timeout based on actual processing time (for Lambda consumers, at least 6x the function timeout plus `MaximumBatchingWindowInSeconds`) — avoids duplicate concurrent processing while keeping failure recovery fast. [doc](https://aws.amazon.com/blogs/compute/implementing-aws-well-architected-best-practices-for-amazon-sqs-part-2/)
- **[fail fast]** Monitor queue processing latency and use dead-letter/redrive queues plus spillover queues to shed or reprioritize backlog during traffic spikes or repeated failures — prevents cascading downstream failures. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_fail_fast.html)
- **[ordering vs. throughput]** Choose standard queues for nearly unlimited throughput when strict ordering isn't required, and reserve FIFO queues (with `MessageGroupId`/`MessageDeduplicationId`) for workloads where exact ordering and exactly-once processing are essential — FIFO has lower throughput ceilings. [doc](https://aws.amazon.com/blogs/compute/implementing-aws-well-architected-best-practices-for-amazon-sqs-part-3/)
- **[deduplication]** For single-producer/single-consumer FIFO use cases, enable content-based deduplication and have consumers supply a receive request attempt ID — makes retry sequences faster without breaking ordering. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/single-producer-single-consumer.html)

## ⚡ Performance Efficiency
- **[polling mode]** Use long polling (`ReceiveMessageWaitTimeSeconds` up to 20 seconds) instead of short polling — reduces empty and false-empty responses and returns messages as soon as they're available. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- **[polling architecture]** When long-polling multiple queues, use one dedicated thread per queue rather than a single thread cycling through all queues — prevents one empty queue from delaying message processing on the others. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/best-practices-setting-up-long-polling.html)
- **[scaling consumers]** Scale Auto Scaling group capacity using an SQS-backed target-tracking metric (e.g., backlog per instance) rather than static capacity — keeps consumer throughput aligned with queue depth. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html)

## 💰 Cost Optimization
- **[polling efficiency]** Enable long polling to reduce the number of empty `ReceiveMessage` calls — directly lowers request-based SQS costs. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- **[monitoring for cost]** Track the `NumberOfEmptyReceives` CloudWatch metric to tune poll frequency and identify unnecessary API calls. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html)
- **[cost allocation]** Tag queues with cost allocation tags to track and attribute spend by cost center or workload. [doc](https://aws.amazon.com/sqs/faqs/)
- **[metric-based scaling]** Use CloudWatch metric math for SQS-based Auto Scaling target tracking instead of publishing a custom backlog-per-instance metric — avoids the cost and operational overhead of custom metrics. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html)

## ⚙️ Operational Excellence
- **[monitoring]** Set CloudWatch alarms on `ApproximateNumberOfMessagesVisible` to detect backlog growth, and on messages landing in the dead-letter queue, so operators are alerted before a stuck consumer causes wider impact. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html)
- **[FIFO diagnostics]** Monitor `ApproximateAgeOfOldestMessage` and `ApproximateNumberOfGroupsWithInflightMessages` to diagnose throughput bottlenecks in FIFO queues. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html)
- **[naming hygiene]** Avoid putting sensitive information in queue names, since queue names/URLs can appear in logs and IAM policies. [doc](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/creating-sqs-standard-queues.html)
- **[DLQ triage]** Treat the dead-letter queue as a debugging tool: alarm on new DLQ messages, inspect message contents and logs to find root cause, then redrive once the consumer is fixed. [doc](https://aws.amazon.com/blogs/compute/introducing-amazon-simple-queue-service-dead-letter-queue-redrive-to-source-queues/)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
