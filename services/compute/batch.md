# AWS Batch — Best Practices

## Common scenarios
- Large-scale HPC and scientific computing (genomics, epidemiology, simulations)        → Performance Efficiency, Cost Optimization
- Machine learning training and batch inference pipelines        → Performance Efficiency, Cost Optimization
- Nightly/overnight ETL and data-processing batch jobs        → Reliability, Operational Excellence
- Media rendering and other bursty, parallelizable workloads        → Cost Optimization, Reliability

## 🔒 Security
- **[IAM policies]** Start from AWS managed policies and narrow to least-privilege customer-managed policies for AWS Batch actions — reduces blast radius of over-permissioned users and workloads. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM policies]** Add IAM policy conditions (e.g. require SSL, restrict to specific services) to further scope AWS Batch access — limits how and from where permissions can be used. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM policies]** Validate identity-based policies with IAM Access Analyzer before attaching them — catches overly permissive or non-functional statements before they reach production. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Execution role]** Grant the Amazon ECS/Fargate execution role only the permissions it needs (ECR pull, CloudWatch Logs) via `AmazonECSTaskExecutionRolePolicy` plus targeted inline additions — avoids a broad role shared across unrelated job types. [doc](https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html)
- **[Networking]** Deploy Fargate and EC2 compute environments in private subnets with a NAT gateway instead of assigning public IPs — keeps job containers off the public internet. [doc](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-with-fargate-using-the-aws-cli.html)
- **[Networking]** Use dedicated security groups scoped to the minimum required access instead of default security groups for compute environments — prevents unintended lateral access. [doc](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-with-fargate-using-the-aws-cli.html)
- **[Networking]** Use VPC interface endpoints for AWS Batch and related service calls where possible — keeps control-plane traffic off the public internet. [doc](https://docs.aws.amazon.com/batch/latest/userguide/vpc-interface-endpoints.html)
- **[Container images]** Store container images in Amazon ECR (private) rather than public repositories — a self-managed or public repository can throttle or fail under thousands of concurrent job pulls. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice3.html)
- **[Auditing]** Enable AWS CloudTrail logging for AWS Batch API calls to track who submitted, modified, or cancelled jobs and compute resources — supports incident investigation and compliance audits. [doc](https://docs.aws.amazon.com/batch/latest/userguide/logging-using-cloudtrail.html)

## 🛡️ Reliability
- **[Retry strategy]** Configure a `retryStrategy` with 1–3 automated attempts (up to 10) on job definitions or submissions — recovers automatically from transient failures, non-zero exit codes, or Spot reclamations. [doc](https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html)
- **[Retry strategy]** Use `evaluateOnExit` conditions to retry only on specific reasons (e.g. host/Spot interruption) and exit immediately on application errors — avoids wasting attempts retrying deterministic failures. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)
- **[Spot workloads]** Keep individual job runtime to 30 minutes or less, or checkpoint longer jobs, when running on Amazon EC2 Spot — significantly reduces the impact of Spot interruptions. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)
- **[Spot workloads]** Choose the `SPOT_CAPACITY_OPTIMIZED` or `SPOT_PRICE_CAPACITY_OPTIMIZED` allocation strategy and diversify across compatible instance families/sizes — pulls from deeper Spot capacity pools and lowers interruption rates. [doc](https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html)
- **[Fallback]** Route interrupted Spot jobs to an On-Demand queue via an EventBridge rule and a Lambda/Step Functions resubmission workflow — preserves throughput for workloads that can't tolerate repeated interruption. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice5.html)
- **[Scaling at scale]** Diversify On-Demand instance types, sizes, and Availability Zones separately from Spot pools — maintains Spot pool depth and availability instead of competing for the same capacity. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice5.html)
- **[Large workloads]** Check and, if needed, raise Amazon EC2 and Amazon EBS quotas per Region before scaling to tens of thousands of vCPUs, and scale up gradually (e.g. 50k → 200k → 500k vCPUs) to surface bottlenecks early — prevents jobs from stalling on quota limits or undiscovered scaling issues. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice2.html)
- **[Array jobs]** Design array jobs expecting that failed child jobs are retried individually, not the whole array — build idempotent per-child logic so partial retries don't corrupt shared state. [doc](https://aws.amazon.com/blogs/hpc/understanding-the-aws-batch-termination-process/)

## ⚡ Performance Efficiency
- **[Compute environment choice]** Use AWS Fargate when jobs need to start in under 30 seconds and fit within 16 vCPUs/120 GiB memory; use Amazon EC2 when jobs need GPUs, custom AMIs, Elastic Fabric Adapter, or finer control — matches the execution model to the job's real resource and startup requirements. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice4.html)
- **[Container images]** Keep container images small and offload infrequently-changing libraries/files to the AMI (or use bind mounts) — smaller images are fetched and started faster across thousands of concurrent jobs. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice3.html)
- **[Container images]** Keep individual image layers under roughly 2 GB and evenly sized — each layer is pulled by a single thread, so one oversized layer becomes the bottleneck for job startup time. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice3.html)
- **[Storage]** Use Amazon S3 for job input/output/staging data instead of provisioning fixed instance storage — scales throughput automatically with job and instance count. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice2.html)
- **[Job sizing]** Avoid submitting very short (few-second) jobs individually; bin-pack multiple tasks into a single Batch job that iterates over them — scheduling overhead otherwise dominates runtime. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice1.html)
- **[Instance allocation]** Prefer `BEST_FIT_PROGRESSIVE` (or the ordered/prioritized variants) over the default `BEST_FIT` strategy when throughput matters more than strict cost minimization — lets Batch fall back to alternate instance types instead of waiting for the single cheapest type to become available. [doc](https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html)

## 💰 Cost Optimization
- **[Purchasing model]** Use Amazon EC2 Spot for jobs that run 30 minutes or less and tolerate interruption/rescheduling; reserve On-Demand for jobs over an hour with strict SLOs — captures Spot savings without violating latency-sensitive workload requirements. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice5.html)
- **[Purchasing model]** Mix models by submitting to a Spot-backed queue first and falling back to an On-Demand queue only on interruption — captures most of the savings while bounding worst-case delay. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice5.html)
- **[Allocation strategy]** Use the default `BEST_FIT` allocation strategy when minimizing per-job cost matters more than scaling speed — it prefers the lowest-cost instance type that fits the job. [doc](https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html)
- **[Repository]** Use Amazon ECR instead of a self-managed or public registry for job container images at scale — avoids throttling that forces retries and wasted compute time. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice3.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Define a monitoring plan (goals, resources, frequency, alert owners) and establish CloudWatch performance baselines for AWS Batch before scaling — makes anomalies and multi-point failures easier to detect and debug. [doc](https://docs.aws.amazon.com/batch/latest/userguide/logging-and-moritoring-batch.html)
- **[Logging]** Send job logs to Amazon CloudWatch Logs and use the job's log stream link in the console for troubleshooting — centralizes output instead of relying on ephemeral container logs. [doc](https://docs.aws.amazon.com/batch/latest/userguide/review-job-logs.html)
- **[Queue visibility]** Use `GetJobQueueSnapshot`, `ListJobs`/`ListServiceJobs`, and `DescribeJobs`/`DescribeServiceJob` to track queue utilization and per-share consumption — gives early warning of queue backlog or starvation under fair-share policies. [doc](https://docs.aws.amazon.com/batch/latest/userguide/track-capacity-utilization-compute-jobs.html)
- **[Interruption tracking]** Track Spot interruption events (e.g. via the Spot Interruption Dashboard) and correlate them with job retries — informs whether instance diversification or retry tuning is needed. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)

<!-- meta: last_reviewed=2026-07-05; sources=17 -->
