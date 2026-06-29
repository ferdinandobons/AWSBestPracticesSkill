# AWS Lambda — Best Practices

## Common scenarios
- Event-driven processing of S3, DynamoDB, or Kinesis events with many small, single-purpose functions — operations
- Synchronous API backends behind API Gateway with strict latency targets — performance
- Asynchronous and queue/stream workloads needing graceful failure capture and idempotency — reliability
- High-volume functions where memory right-sizing drives the bill — cost

## 🔒 Security
- **[execution role]** Grant only the permissions the function needs (least privilege) and move from AWS managed policies toward customer-managed, function-specific policies as you reach production — limits blast radius if a function is compromised. [doc](https://docs.aws.amazon.com/lambda/latest/dg/security_iam_id-based-policy-examples.html)
- **[resource policy]** Scope invoke permissions to specific source buckets, accounts, or ARNs instead of granting blanket service access — prevents unauthorized event sources from triggering the function. [doc](https://docs.aws.amazon.com/lambda/latest/dg/concepts-basics.html)
- **[IAM validation]** Use IAM Access Analyzer to validate policies and add conditions (e.g. require SSL, restrict by calling service) to further constrain access — catches over-broad grants before they ship. [doc](https://docs.aws.amazon.com/lambda/latest/dg/security_iam_id-based-policy-examples.html)
- **[secrets]** Store secrets and sensitive configuration in AWS Secrets Manager or Systems Manager Parameter Store and load them at runtime, never hard-coded in code or env vars — keeps credentials out of source and deployable across accounts. [doc](https://aws.amazon.com/blogs/compute/operating-lambda-design-principles-in-event-driven-architectures-part-2/)
- **[execution environment]** Do not store user data, events, or security-sensitive state in the execution environment, since it is reused across invocations — avoids data leaks between requests. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[code integrity]** Enable Code Signing with AWS Signer so Lambda only deploys unaltered packages from approved publishers — ensures only trusted code runs in production. [doc](https://aws.amazon.com/blogs/security/best-practices-and-advanced-patterns-for-lambda-code-signing/)
- **[threat detection]** Monitor Lambda configuration with Security Hub CSPM and network activity with GuardDuty Lambda Protection — surfaces misconfigurations and suspicious outbound calls. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 🛡️ Reliability
- **[idempotency]** Write idempotent code that validates and gracefully handles duplicate events — queues are eventually consistent and a function can receive the same event more than once. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[async failures]** Configure a dead-letter queue (SQS/SNS) or an on-failure destination to capture events that exhaust retries — prevents silent data loss and enables later reprocessing. [doc](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html)
- **[stream/queue retries]** Understand the retry behavior of each invoker: stream event source mappings retry the whole batch and block the shard until success or expiry, while SQS uses the queue's visibility timeout and redrive policy — design error handling per source instead of assuming uniform retries. [doc](https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html)
- **[SQS source]** Keep the function's expected runtime below the source queue's visibility timeout — a longer runtime can cause duplicate invocations. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[throttle tolerance]** Apply timeouts, retries, and exponential backoff with jitter for synchronous callers so retried invocations smooth out and Lambda can scale within seconds — reduces end-user throttling during traffic spikes. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[multi-AZ VPC]** When attaching a function to a VPC, place it in subnets across multiple Availability Zones — preserves function availability during an AZ disruption. [doc](https://docs.aws.amazon.com/resilience-hub/latest/userguide/resilience-checks.html)

## ⚡ Performance Efficiency
- **[environment reuse]** Initialize SDK clients and database connections outside the handler and cache static assets in `/tmp` — subsequent invocations on the same instance reuse them, cutting latency and run time. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[connections]** Use the runtime's keep-alive directive to maintain persistent connections — Lambda purges idle connections, and reusing a dead one causes connection errors. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[memory tuning]** Performance-test memory size (which also scales CPU) and set timeouts from load tests — the right configuration shortens duration without over-provisioning. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[cold starts]** For latency-sensitive Java, Python, and .NET functions with long init, enable SnapStart to resume from a cached snapshot; for strict double-digit-millisecond startup SLAs use provisioned concurrency — both reduce cold-start latency. [doc](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
- **[downstream limits]** Know upstream/downstream throughput constraints and use reserved concurrency to cap scaling against dependencies that cannot scale as fast as Lambda — protects fragile backends from overload. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 💰 Cost Optimization
- **[right-sizing]** Right-size memory using AWS Lambda Power Tuning or Compute Optimizer, since over-provisioned memory is a primary cost driver and more memory can also lower duration — find the sweet spot between cost and speed, and re-run it on releases. [doc](https://aws.amazon.com/blogs/compute/understanding-techniques-to-reduce-aws-lambda-costs-in-serverless-applications/)
- **[recursion guard]** Avoid recursive self-invocation; if you see runaway invocations, set reserved concurrency to `0` immediately to throttle the function while you fix the code — prevents unintended invocation volume and escalating cost. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[hygiene]** Delete functions you no longer use — unused functions needlessly count against your deployment package storage limit. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[anomaly detection]** Enable AWS Cost Anomaly Detection to flag unusual account activity — catches cost spikes from misbehaving functions early. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## ⚙️ Operational Excellence
- **[config over code]** Pass operational parameters via environment variables instead of hard-coding values — lets you change behavior across environments without redeploying. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[alarming]** Use CloudWatch metrics and alarms (e.g. on duration and errors) rather than emitting metrics from inside function code — a more efficient way to track function health and catch issues early. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[structured observability]** Emit custom metrics asynchronously with Embedded Metric Format and use structured JSON logging — reduces latency versus synchronous CloudWatch calls and makes logs searchable. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[tracing]** Enable AWS X-Ray active tracing (and Lambda Insights) to detect, analyze, and optimize performance issues across function nodes — gives end-to-end visibility into latency and errors. [doc](https://docs.aws.amazon.com/help-panel/lambda/latest/console/functions-monitoring.html)
- **[stream health]** Alarm on the IteratorAge metric for stream-based functions to detect stalled or lagging shards — surfaces processing backlogs before data ages out. [doc](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- **[testable code]** Separate the handler from core business logic and keep dependencies minimal — improves unit testability and reduces deployment package size and startup time. [doc](https://docs.aws.amazon.com/lambda/latest/dg/java-handler.html)

<!-- meta: last_reviewed=2026-06-29; sources=12 -->
