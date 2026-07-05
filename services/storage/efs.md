# Amazon EFS — Best Practices

## Common scenarios
- Shared, elastic file storage for Linux workloads across EC2, ECS, EKS, and Lambda        → Performance Efficiency, Reliability
- Persistent storage for containerized applications needing a common namespace        → Reliability, Operational Excellence
- Multi-AZ durable storage for regulated or compliance-driven workloads        → Security, Reliability
- Cost-optimized long-term storage for infrequently accessed shared files        → Cost Optimization

## 🔒 Security
- **[Encryption at rest]** Implement the AWS Config managed rule `efs-encrypted-check` to continuously verify file systems are encrypted with AWS KMS. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)
- **[Encryption enforcement]** Use the `elasticfilesystem:Encrypted` IAM condition key in identity-based policies (or an Organizations SCP) to prevent creation of unencrypted file systems. — [doc](https://docs.aws.amazon.com/efs/latest/ug/encryption-at-rest.html)
- **[Encryption in transit]** Mount file systems with the EFS mount helper and the `tls` option so NFS traffic is routed through an encrypted TLS 1.2 tunnel. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)
- **[Encryption in transit]** Use the `aws:SecureTransport` condition key in the EFS file system policy to require TLS for all NFS client connections. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)
- **[Key management]** Use a customer managed KMS key instead of the AWS managed key so you control key policies and grants for multiple users or services. — [doc](https://aws.amazon.com/blogs/industries/financial-services-spotlight-amazon-elastic-file-system/)
- **[Key management]** Configure KMS keys used for EFS encryption with least-privilege, resource-based key policies. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)
- **[Private access]** Use AWS PrivateLink interface VPC endpoints to establish a private connection to the Amazon EFS API instead of traversing the public internet. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)
- **[IAM]** Start from AWS managed policies and progressively narrow to least-privilege customer managed policies for EFS actions. — [doc](https://docs.aws.amazon.com/efs/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Add conditions to identity-based policies (for example, requiring SSL) to further restrict access to EFS actions and resources. — [doc](https://docs.aws.amazon.com/efs/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer to catch overly permissive or non-compliant statements. — [doc](https://docs.aws.amazon.com/efs/latest/ug/security_iam_id-based-policy-examples.html)
- **[Application access]** Use Amazon EFS Access Points to enforce a specific user identity and a fixed root directory per application, rather than granting broad file system access. — [doc](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html)
- **[Application access]** Require the `elasticfilesystem:AccessedViaMountTarget` condition so file system access only occurs through mount targets. — [doc](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html)
- **[Network security]** Restrict mount target security groups to inbound TCP 2049 (NFS) only from the specific client security groups or CIDR ranges that need access, instead of the VPC default security group. — [doc](https://docs.aws.amazon.com/efs/latest/ug/network-access.html)
- **[Network security]** Give each EC2 instance mounting the file system an outbound rule to the mount target on TCP port 2049. — [doc](https://docs.aws.amazon.com/efs/latest/ug/network-access.html)
- **[Compliance monitoring]** Create a CloudWatch alarm on CloudTrail `CreateFileSystem` events to detect and alert when an unencrypted file system is created. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/efs.html)

## 🛡️ Reliability
- **[Backup]** Enable AWS Backup for EFS file systems and test restores regularly to recover from accidental deletion or data corruption. — [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/efs-best-practices.html)
- **[Backup]** Note that AWS Backup for EFS does not provide point-in-time crash-consistency; design recovery expectations accordingly. — [doc](https://aws.amazon.com/blogs/aws/new-replication-for-amazon-elastic-file-system-efs/)
- **[Disaster recovery]** Use Amazon EFS Replication to maintain a read-only copy of a file system in another AWS Region (or the same Region) for business continuity and DR failover/failback. — [doc](https://docs.aws.amazon.com/efs/latest/ug/backup-replication.html)
- **[Disaster recovery]** Monitor the `TimeSinceLastSync` CloudWatch metric to confirm replication is meeting your recovery point objective. — [doc](https://docs.aws.amazon.com/efs/latest/ug/efs-metrics.html)
- **[Multi-AZ resilience]** Use Standard storage classes (not One Zone) for workloads that require data redundancy across multiple Availability Zones. — [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/efs-best-practices.html)
- **[Availability]** Create mount targets in at least two Availability Zones so clients keep access if one AZ becomes unavailable. — [doc](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem-efs.html)
- **[Access resilience]** Create an access point per Availability Zone/function so each instance connects to the nearest mount target. — [doc](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem-efs.html)

## ⚡ Performance Efficiency
- **[Performance mode]** Use General Purpose performance mode rather than Max I/O for lower per-operation latency; Max I/O only benefits very highly parallelized workloads. — [doc](https://docs.aws.amazon.com/efs/latest/ug/performance.html)
- **[Throughput mode]** Use Provisioned Throughput when your workload's throughput requirements are known and consistent. — [doc](https://aws.amazon.com/blogs/storage/performance-analysis-for-different-amazon-efs-throughput-modes-via-amazon-cloudwatch/)
- **[Throughput mode]** Use Elastic Throughput for spiky or unpredictable workloads that use a low percentage of provisioned capacity on average. — [doc](https://aws.amazon.com/blogs/storage/performance-analysis-for-different-amazon-efs-throughput-modes-via-amazon-cloudwatch/)
- **[Monitoring]** Track throughput utilization against calculated or provisioned throughput to decide whether to enable or adjust Provisioned Throughput. — [doc](https://aws.amazon.com/blogs/storage/best-practices-for-using-amazon-efs-for-container-storage/)
- **[Monitoring]** Track IOPS utilization against the General Purpose mode limit, and move to Max I/O or split data across multiple file systems if you approach 100%. — [doc](https://aws.amazon.com/blogs/storage/best-practices-for-using-amazon-efs-for-container-storage/)
- **[Monitoring]** Set an alarm on `BurstCreditBalance` so you're notified before a Bursting-mode file system runs low on burst credits and throughput drops. — [doc](https://aws.amazon.com/blogs/storage/best-practices-for-using-amazon-efs-for-container-storage/)
- **[File layout]** Limit the number of files per directory and use a non-root access point path to improve access performance for compute clients such as Lambda. — [doc](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem-efs.html)

## 💰 Cost Optimization
- **[Lifecycle management]** Enable EFS Lifecycle Management to automatically transition files that haven't been accessed for a set period into the Infrequent Access (or One Zone-IA) storage class. — [doc](https://aws.amazon.com/blogs/aws/optimize-storage-cost-with-reduced-pricing-for-amazon-efs-infrequent-access/)
- **[Lifecycle management]** Review lifecycle policy age-off thresholds periodically and tune them to your actual access patterns rather than leaving defaults indefinitely. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-sap-cost-optimization/storage-optimization-services.html)
- **[Intelligent-Tiering]** Enable EFS Intelligent-Tiering so files automatically move back to Standard/One Zone storage when access patterns change, avoiding repeated manual retiering. — [doc](https://aws.amazon.com/blogs/aws/new-amazon-efs-intelligent-tiering-optimizes-costs-for-workloads-with-changing-access-patterns/)
- **[Storage class selection]** Use One Zone storage classes for workloads that don't require multi-AZ resilience to reduce storage cost versus Standard classes. — [doc](https://aws.amazon.com/blogs/aws/new-amazon-efs-intelligent-tiering-optimizes-costs-for-workloads-with-changing-access-patterns/)
- **[DR cost tuning]** For replication targets used only for disaster recovery, apply an aggressive (short) lifecycle transition period since the data is rarely accessed until failover. — [doc](https://aws.amazon.com/blogs/storage/use-cases-for-amazon-efs-replication/)

## ⚙️ Operational Excellence
- **[Monitoring]** Monitor Amazon EFS with CloudWatch metrics such as throughput, IOPS, burst credit balance, and client connections, and build a dashboard to track them centrally. — [doc](https://docs.aws.amazon.com/efs/latest/ug/monitoring-cloudwatch.html)
- **[Monitoring]** Create CloudWatch alarms on key EFS metrics (for example `PercentIOLimit`, `BurstCreditBalance`) so issues are surfaced proactively instead of discovered after impact. — [doc](https://docs.aws.amazon.com/efs/latest/ug/efs-metrics.html)
- **[Cross-account visibility]** Use CloudWatch cross-account and cross-Region dashboards to centralize monitoring of EFS file systems deployed across multiple accounts and Regions. — [doc](https://aws.amazon.com/blogs/storage/monitoring-amazon-efs-kpis-using-aws-cloudwatch-metrics/)
- **[Manual checks]** Regularly review the EFS console for metered size, mount target count, and lifecycle state as a complement to automated CloudWatch alarms. — [doc](https://docs.aws.amazon.com/efs/latest/ug/monitoring_automated_manual.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
