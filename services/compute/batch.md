# AWS Batch - Best Practices

## Common scenarios
- Large-scale HPC and scientific computing (genomics, epidemiology, simulations) -> Cost Optimization
- Fault-tolerant, interruption-tolerant parallel jobs on EC2 Spot -> Reliability
- ML training and image/AI inference at tens of thousands of concurrent jobs -> Performance Efficiency
- Cost-sensitive queued batch processing with no infrastructure to manage -> Cost Optimization

## 🔒 Security
- **[IAM]** Start from AWS managed policies and then move toward least-privilege customer managed policies that grant only the actions, resources, and conditions each workload needs - limits the blast radius of credentials Batch uses to call other services. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer and add conditions (for example require SSL or access only via a specific service) - catches overly permissive grants before they reach production. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Network]** Run job containers in private subnets with a NAT gateway instead of assigning public IPs, and use dedicated security groups with minimal access - keeps compute off the public internet. [doc](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-with-fargate-using-the-aws-cli.html)
- **[Network]** Use an interface VPC endpoint to reach the AWS Batch API and restrict access to specific VPCs or source IPs - isolates control-plane traffic inside the AWS network. [doc](https://docs.aws.amazon.com/batch/latest/userguide/infrastructure-security.html)
- **[Images]** Store container images in Amazon ECR rather than public repositories - gives you private, access-controlled, scannable images for your jobs. [doc](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-with-fargate-using-the-aws-cli.html)
- **[Transport]** Require TLS 1.2 or later (TLS 1.3 recommended) with perfect-forward-secrecy cipher suites for all calls to the Batch API - protects data in transit to the service. [doc](https://docs.aws.amazon.com/batch/latest/userguide/infrastructure-security.html)
- **[Confused deputy]** Use the AWSServiceRoleForBatch service-linked role and add aws:SourceArn / aws:SourceAccount conditions to cross-service trust policies - prevents a confused-deputy escalation across accounts. [doc](https://docs.aws.amazon.com/batch/latest/userguide/security.html)

## 🛡️ Reliability
- **[Retries]** Set 1-3 automated job retries (up to 10) so jobs survive non-zero exit codes, service errors, and Spot reclamations - retried jobs are placed at the front of the queue and rescheduled with priority. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)
- **[Retries]** Use evaluateOnExit conditional retry strategies to retry only on infrastructure causes (for example "Host EC2*") and exit immediately on application failures - avoids wasting compute re-running deterministically broken jobs. [doc](https://aws.amazon.com/blogs/compute/introducing-retry-strategies-for-aws-batch/)
- **[Multi-AZ]** Configure compute environments with subnets in multiple Availability Zones - lets Batch tap more instance pools and spreads the risk of interruptions. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Capacity]** Right-size VPC/subnet CIDRs and confirm EC2, Spot, and EBS service quotas before scaling - too few IP addresses or low quotas leave jobs stuck in RUNNABLE and cap instance count. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Fallback]** Submit to a Spot queue first and fail over to an On-Demand queue (via EventBridge plus Lambda/Step Functions) for interrupted jobs, using different instance types/AZs for On-Demand - keeps strict-SLO work moving without starving Spot pools. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)

## ⚡ Performance Efficiency
- **[Containers]** Keep images small and split layers evenly (about 2 GB max per layer), offloading rarely-changing libraries to the AMI via bind mounts - smaller, balanced layers pull faster and cut job start time. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Registry]** Pull job images from Amazon ECR instead of self-managed or public registries - ECR sustains massive parallel pulls (1M+ vCPUs) where other repos throttle or fall over. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Compute choice]** Use Fargate for jobs that need to start in under 30 seconds with <=4 vCPU and <=30 GiB and no GPU, and EC2 when you need GPUs, EFA, high memory/vCPU, custom AMIs, or maximum throughput - matches the runtime to the workload's real needs. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Scaling]** Scale to very large fleets in steps (for example 50k -> 200k -> 500k -> 1M+ vCPUs) while monitoring with CloudWatch Logs and Embedded Metric Format - surfaces architecture and application bottlenecks early. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Storage]** Use Amazon S3 for job input/output at scale instead of per-instance volumes - it delivers high throughput without pre-provisioning capacity per AZ or instance. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[Job sizing]** Bin-pack very short tasks into jobs that run ~3-5 minutes, and avoid Batch for millisecond-latency needs - reduces scheduling overhead relative to runtime and improves utilization. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)

## 💰 Cost Optimization
- **[Allocation]** For interruption-tolerant work enable Spot and use SPOT_PRICE_CAPACITY_OPTIMIZED (lowest price plus deepest pools) - minimizes both cost and interruption risk versus other strategies. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_batch-readme.html)
- **[Diversification]** Allow Batch to choose from many compatible instance sizes and families (for example c5, c5a, c5n, c5d, m5, m5d) rather than a single type - more pools means better availability and lower price. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)
- **[Job duration]** Keep Spot jobs short (minutes, not hours) or checkpoint long jobs - shorter jobs make interruptions cheaper and reduce wasted re-computation. [doc](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice6.html)
- **[Right-sizing]** Set the compute environment instance type to "optimal" or a tuned set so Batch provisions and bin-packs jobs onto cost-efficient instances - packing multiple jobs onto a larger instance often beats one job per smallest instance. [doc](https://docs.aws.amazon.com/whitepapers/latest/genomics-data-transfer-analytics-and-machine-learning/appendix-g-optimizing-secondary-analysis-compute-cost.html)

## ⚙️ Operational Excellence
- **[Observability]** Ship system, ECS, and application logs to CloudWatch Logs and emit metrics via the Embedded Metric Format - gives the dashboards and alarms needed to catch job and resource issues, especially at scale. [doc](https://aws.amazon.com/blogs/hpc/aws-batch-best-practices/)
- **[AMI lifecycle]** Use enhanced compute-environment updates (service-linked role, a progressive/Spot allocation strategy, updateToLatestImageVersion=true, no pinned AMI ID) to roll forward to patched AMIs - you own guest-OS patching, so automate it instead of leaving stale images. [doc](https://docs.aws.amazon.com/batch/latest/userguide/compute_resource_AMIs.html)
- **[Workload design]** Use multiple job queues with different priorities and define infrastructure with CloudFormation or the CDK - separates workloads cleanly and makes environments reproducible. [doc](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-with-fargate-using-the-aws-cli.html)

<!-- meta: last_reviewed=2026-06-29; sources=9 -->
