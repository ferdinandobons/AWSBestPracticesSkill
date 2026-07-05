# Amazon SNS — Best Practices

## Common scenarios
- Pub/sub fan-out of a single event to multiple SQS queues, Lambda functions, or HTTP(S) endpoints        → Reliability, Performance Efficiency
- Application-to-person notifications (email, SMS, mobile push)        → Operational Excellence
- Strict ordering and exactly-once fan-out for financial or inventory events via FIFO topics        → Reliability
- Decoupling microservices and serverless event-driven architectures        → Reliability, Cost Optimization

## 🔒 Security
- **[Access policy]** Avoid a `Principal` of `"*"` or an empty principal in topic policies unless the topic is intentionally public — scope access to specific accounts, roles, or users instead. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[IAM]** Implement least-privilege access by separating administrator, publisher, and subscriber permissions rather than granting broad `sns:*` to all callers. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[IAM]** Use IAM roles (not long-term credentials embedded in application code or EC2 instances) for applications and AWS services that publish to or manage SNS topics. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Encryption]** Enable server-side encryption (SSE) with AWS KMS on topics carrying sensitive data so messages are encrypted at rest independently of where they're stored. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Encryption]** Enforce HTTPS-only publishing by adding an `aws:SecureTransport` deny condition to the topic policy, since SNS does not reject HTTP publishes by default even on unencrypted topics. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Networking]** Use VPC endpoints (AWS PrivateLink) to restrict topic access to traffic originating from specific VPCs, keeping publish/subscribe traffic off the public internet. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Subscriptions]** Configure HTTP(S) subscriptions to deliver to a domain name rather than a raw IP address so endpoint validation and certificate checks work as expected. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Subscriptions]** Set `AuthenticateOnUnsubscribe` to `true` when confirming subscriptions unless unauthenticated unsubscribe is explicitly required (e.g. email opt-out), otherwise unsubscribe requests can succeed without authentication. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html)
- **[Data protection]** Apply message data protection policies to audit, deny, or de-identify (mask/redact) sensitive data flowing through a topic, rather than relying solely on downstream controls. [doc](https://aws.amazon.com/blogs/security/mask-and-redact-sensitive-data-published-to-amazon-sns-using-managed-and-custom-data-identifiers/)
- **[Data protection]** Never place confidential or sensitive data (e.g. customer emails) into tags, message attributes, or other free-form fields, since these may surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/sns/latest/dg/security.html)
- **[Transport]** Require clients to use TLS 1.2 or later with a cipher suite supporting Perfect Forward Secrecy when connecting to the SNS API. [doc](https://docs.aws.amazon.com/sns/latest/dg/infrastructure-security.html)
- **[Auditing]** Enable AWS CloudTrail logging of SNS API calls (topic creation, subscription changes, publishes) to support security audits and troubleshooting of who made which request. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-logging-monitoring.html)

## 🛡️ Reliability
- **[Delivery]** Attach a dead-letter queue (Amazon SQS) to subscriptions so messages that exhaust the delivery retry policy are preserved instead of discarded. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html)
- **[Delivery]** Design subscribers to handle SNS's built-in retry behavior (up to 100,015 retries over 23 days for SQS/Lambda endpoints; a bounded backoff schedule for HTTP/SMTP/SMS/mobile push) rather than implementing redundant custom retry logic at the same layer. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html)
- **[Delivery]** Distinguish client-side delivery failures (stale subscription metadata, deleted endpoints, restrictive endpoint policies — not retried) from server-side failures (endpoint unavailable — retried), and keep subscription endpoints and their resource policies in sync to avoid silent client-side drops. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html)
- **[Fan-out]** Place an SQS queue between an SNS topic and each subscriber service (topic-queue-chaining) so a subscriber outage or slow consumer doesn't cause message loss, and so consumers can scale independently. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html)
- **[Ordering]** Use FIFO topics with SQS FIFO queue subscribers when strict ordering and deduplication are required, since standard topics only offer best-effort ordering and at-least-once delivery. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html)
- **[Ordering]** Use per-entity message group IDs on FIFO topics so ordering is preserved within each logical entity without serializing unrelated messages against each other. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-grouping.html)
- **[Recovery]** Enable message archiving and replay on FIFO topics (retention up to 365 days) to recover from downstream subscriber failures or resynchronize systems by replaying a time window of messages. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-archiving-replay.html)
- **[Durability]** Rely on SNS's multi-AZ message storage (messages are durably stored across multiple Availability Zones before publish is acknowledged) rather than building custom durability workarounds. [doc](https://docs.aws.amazon.com/sns/latest/dg/disaster-recovery-resiliency.html)
- **[Compliance/DR]** Subscribe an Amazon Data Firehose delivery stream to a topic to archive all messages to durable storage (e.g. Amazon S3) for long-term retention and later analysis. [doc](https://docs.aws.amazon.com/sns/latest/dg/firehose-example-use-case.html)

## ⚡ Performance Efficiency
- **[Filtering]** Apply subscription filter policies so each subscriber receives only the messages it needs, offloading routing logic from publishers and reducing unnecessary invocations/processing downstream. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-filtering.html)
- **[FIFO]** Subscribe SQS standard queues (instead of FIFO queues) to a FIFO topic when best-effort ordering is acceptable, to lower cost and share queues across workloads that don't need strict FIFO semantics. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html)
- **[Fan-out]** Use the native SNS-to-SQS fan-out pattern instead of custom multi-cast logic in publishers, letting SQS act as a buffering load balancer in front of consumer fleets that scale independently. [doc](https://aws.amazon.com/blogs/compute/monitor-amazon-sns-based-applications-end-to-end-with-aws-x-ray-active-tracing/)
- **[Tracing]** Enable AWS X-Ray active tracing on SNS topics in fan-out architectures so the full request path across SNS, SQS, and downstream services is reconstructed in the CloudWatch service map. [doc](https://aws.amazon.com/blogs/compute/monitor-amazon-sns-based-applications-end-to-end-with-aws-x-ray-active-tracing/)

## 💰 Cost Optimization
- **[Encryption]** Use AWS-managed KMS keys where a customer-managed key isn't specifically required, since SNS SSE incurs no additional SNS charge beyond standard AWS KMS request costs. [doc](https://aws.amazon.com/blogs/compute/encrypting-messages-published-to-amazon-sns-with-aws-kms/)
- **[Filtering]** Push message routing into subscription filter policies rather than delivering every message to every subscriber and filtering downstream, since filtered-out messages aren't delivered (or billed for delivery) to that subscriber. [doc](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-filtering.html)
- **[Archiving]** Route long-term message retention needs through a Firehose subscription to S3/Redshift/OpenSearch instead of building custom archival consumers. [doc](https://docs.aws.amazon.com/sns/latest/dg/firehose-example-use-case.html)
- **[Monitoring]** Use built-in SNS CloudWatch metrics (no additional SNS charge) to validate filter policies and delivery health instead of provisioning separate custom instrumentation. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Configure CloudWatch alarms on key metrics such as `NumberOfNotificationsFailed` to get proactive notification of delivery degradation instead of discovering failures downstream. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html)
- **[Monitoring]** Enable delivery status logging (success/failure feedback to CloudWatch Logs) per protocol (HTTP, Lambda, Firehose, SQS, application endpoints) to capture dwell times and failure reasons for troubleshooting. [doc](https://docs.aws.amazon.com/sns/latest/dg/msg-status-sdk.html)
- **[Auditing]** Combine CloudTrail API logging with CloudWatch topic metrics to audit who changed subscriptions/topics and observe real-time delivery health together. [doc](https://docs.aws.amazon.com/sns/latest/dg/sns-logging-monitoring.html)
- **[Cross-account/region]** Account for the added latency and configuration requirements when delivering messages to a subscriber (SQS queue or Lambda function) in a different account or Region than the topic. [doc](https://docs.aws.amazon.com/sns/latest/dg/message-delivery.html)

<!-- meta: last_reviewed=2026-07-05; sources=19 -->
