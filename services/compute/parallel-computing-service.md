# AWS Parallel Computing Service - Best Practices

## Common scenarios
- Tightly coupled HPC simulations (CFD, weather, FEA, reservoir) on a managed Slurm cluster -> performance, reliability
- Elastic, on-demand scientific and engineering modeling with auto-scaling compute node groups -> cost optimization
- Regulated/compliance-bound HPC (HIPAA, FedRAMP, ITAR) with isolated networking and audit logging -> security, operational excellence

## 🔒 Security
- **[AMIs]** Never use AWS PCS sample AMIs for production; regularly patch the OS, software, and PCS packages in your compute node group AMI - sample AMIs are unsupported and stale images carry vulnerabilities. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Slurm]** Restrict Slurm control and compute nodes with access controls and network restrictions, and enable Slurm authentication so only trusted users submit jobs - limits the blast radius of the scheduler. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Slurm versions]** Keep Slurm updated and subscribe to the PCS docs RSS feed for EOSL notices - clusters running an end-of-support Slurm version are stopped immediately. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Secrets]** Regularly rotate cluster secrets - required for HIPAA and FedRAMP compliance and remediates potential compromises. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Network isolation]** Deploy PCS clusters in a separate VPC and control traffic with security groups and network ACLs - isolates the HPC environment from other workloads. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Private connectivity]** Use AWS PrivateLink interface endpoints / VPC endpoints for traffic between clusters and AWS services - keeps API traffic inside the AWS network instead of the public internet. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Data protection]** Enforce TLS 1.2+ (prefer 1.3) for API access, enable MFA, encrypt data, and keep credentials/PII out of tags and free-form name fields - tag and name data may surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/data-protection.html)
- **[Least privilege]** Use IAM Identity Center or IAM to grant each user only the permissions needed for their job - reduces the impact of compromised credentials. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-iam.html)
- **[Confused deputy]** Add `aws:SourceArn` (cluster ARN) and `aws:SourceAccount` condition keys to resource policies the `pcs.amazonaws.com` principal can assume - prevents another service from being coerced into acting on your resources. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/cross-service-confused-deputy-prevention.html)

## 🛡️ Reliability
- **[Multi-AZ]** Spread compute node group subnets across multiple Availability Zones within a Region - AZs are isolated and let workloads tolerate the loss of a single zone. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/disaster-recovery-resiliency.html)
- **[Capacity assurance]** For tightly coupled or always-on jobs, back On-Demand node groups with On-Demand Capacity Reservations or Capacity Blocks for ML rather than relying on Spot - guarantees instances are available when scheduled. [doc](https://docs.aws.amazon.com/cli/latest/reference/pcs/create-compute-node-group.html)

## ⚡ Performance Efficiency
- **[Storage tiering]** Pair a shared home directory (Amazon EFS) with a high-performance scratch directory (Amazon FSx for Lustre) - separates durable user data from the low-latency, high-throughput I/O that HPC jobs need. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/getting-started.html)
- **[Instance fit]** Map workloads to dedicated compute node groups and queues sized to the job (CPU, single-GPU, multi-GPU) - matching instance types to job profiles avoids over- or under-provisioning per queue. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/getting-started.html)
- **[Detailed metrics]** Enable detailed CloudWatch monitoring in the compute node group launch template for 1-minute instance metrics - finer granularity surfaces performance degradation in long-running calculations faster. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/monitoring-cloudwatch_instances.html)

## 💰 Cost Optimization
- **[Purchase options]** Use Spot or Interruptible Capacity Reservations for fault-tolerant, flexible jobs and reserve On-Demand/ODCR for the scheduler and time-critical work - mixing purchase options cuts cost while protecting SLAs. [doc](https://docs.aws.amazon.com/cli/latest/reference/pcs/create-compute-node-group.html)
- **[Scale to zero]** Set the compute node group scaling configuration `minInstanceCount` to 0 so idle queues scale down - you pay only for instances allocated to running jobs. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/monitoring-cloudwatch_metrics.html)
- **[Utilization tracking]** Watch the `IdleCapacity` and `CapacityUtilization` metrics in the `AWS/PCS` namespace - persistent idle capacity signals over-provisioned node groups to trim. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/monitoring-cloudwatch_metrics.html)

## ⚙️ Operational Excellence
- **[Audit & monitor]** Use CloudWatch Logs and AWS CloudTrail to record cluster and account actions for troubleshooting and auditing - gives a durable record of API calls and operational events. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/security-best-practices.html)
- **[Scheduler logs]** Configure `PCS_SCHEDULER_LOGS` delivery to CloudWatch Logs, S3, or Firehose to capture `slurmctld`, `slurmdbd`, and `slurmrestd` output - centralizes scheduler diagnostics for faster root-cause analysis. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/monitoring_scheduler-logs.html)
- **[Log persistence]** Configure the CloudWatch agent via the launch template to persist instance metrics and logs after termination - CloudWatch data on ephemeral nodes is otherwise lost when instances are terminated. [doc](https://docs.aws.amazon.com/pcs/latest/userguide/monitoring-cloudwatch.html)

<!-- meta: last_reviewed=2026-06-29; sources=14 -->
