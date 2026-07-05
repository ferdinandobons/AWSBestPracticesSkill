# Amazon EBS — Best Practices

## Common scenarios
- Persistent block storage for EC2 boot and data volumes        → Reliability, Performance Efficiency
- High-IOPS storage for relational and NoSQL databases running on EC2        → Performance Efficiency, Cost Optimization
- Point-in-time backup and disaster recovery for EC2-based workloads        → Reliability, Security
- Encrypted storage for regulated or compliance-sensitive applications        → Security, Cost Optimization

## 🔒 Security
- **[Encryption at rest]** Encrypt both boot and data EBS volumes so data at rest, data in transit between the instance and the volume, snapshots, and volumes restored from those snapshots are all protected. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ec2-ebs.html)
- **[Encryption by default]** Enable encryption by default for EBS volumes in each Region/account so every newly created volume and snapshot copy is automatically encrypted. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ec2-ebs.html)
- **[Key management]** Use a customer managed KMS key instead of the AWS managed key when you need granular control over who can encrypt/decrypt EBS resources, including key rotation, disabling, and access policies. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/EBSFeatures.html)
- **[Governance]** Implement the AWS Config `encrypted-volumes` managed rule to continuously detect and alert on unencrypted EBS volumes. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ec2-ebs.html)
- **[Tagging]** Tag every EBS volume with a data classification key/value so the correct security and encryption requirements can be determined and enforced per volume. — [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ec2-ebs.html)
- **[Guardrails]** Use IAM policies and AWS Organizations SCPs to prevent creation of unencrypted volumes or volumes using unapproved (older-generation) volume types. — [doc](https://aws.amazon.com/blogs/apn/maximizing-storage-performance-and-savings-with-amazon-ebs-gp3-and-ollion/)
- **[Snapshot protection]** Restrict public access to EBS snapshots and share them only with specific, trusted accounts. — [doc](https://aws.amazon.com/ebs/snapshots/)
- **[Snapshot protection]** Use Amazon EBS Snapshot Lock in governance or compliance mode to protect critical snapshots from accidental or malicious deletion, including ransomware scenarios. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshot-lock.html)

## 🛡️ Reliability
- **[Backup]** Create EBS snapshots on a regular, automated schedule (via AWS Backup or Amazon Data Lifecycle Manager) since AWS does not automatically back up EBS volume data. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)
- **[Backup]** Use Recycle Bin for EBS Snapshots so accidentally or maliciously deleted snapshots can be recovered instead of being permanently lost. — [doc](https://aws.amazon.com/ebs/snapshots/)
- **[High availability]** Design workloads with no single point of failure, since EBS volumes live within a single Availability Zone; pair volumes with cross-AZ application architecture where high availability is required. — [doc](https://aws.amazon.com/ebs/faqs/)
- **[High availability]** Implement automated monitoring, failure detection, and failover mechanisms rather than relying solely on manual intervention. — [doc](https://aws.amazon.com/ebs/faqs/)
- **[Operational readiness]** Prepare documented operating procedures for detaching an unavailable volume and attaching a backup/recovery volume when a failure occurs. — [doc](https://aws.amazon.com/ebs/faqs/)
- **[Status monitoring]** Monitor EBS volume status checks (which run automatically every 5 minutes) to detect impaired volumes and decide whether to run a consistency check before re-enabling I/O. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/monitoring-volume-checks.html)
- **[Status monitoring]** Use the `StatusCheckFailed_AttachedEBS` CloudWatch metric on Nitro instances to detect underlying compute/EBS infrastructure issues, and alarm on it to trigger failover or instance replacement. — [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html)
- **[Auto Scaling resilience]** Configure Auto Scaling groups to detect attached EBS status check failures and automatically replace the affected instance. — [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html)
- **[High availability]** Use EBS Multi-Attach for Provisioned IOPS volumes to share a single volume across up to 16 Nitro-based instances in the same Availability Zone for clustered applications that manage write ordering. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/working-with-multi-attach.html)
- **[Disaster recovery]** Copy EBS snapshots to a separate DR Region and manage retention/cleanup there to meet distance-based disaster recovery requirements. — [doc](https://aws.amazon.com/blogs/compute/automating-amazon-ebs-snapshot-management-with-aws-step-functions-and-amazon-cloudwatch-events/)

## ⚡ Performance Efficiency
- **[Instance pairing]** Use EBS-optimized EC2 instance types so a dedicated network connection serves I/O between the instance and its volumes, minimizing contention with other instance traffic. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-optimization.html)
- **[Capacity matching]** Ensure the combined IOPS/throughput of attached volumes matches or exceeds the instance type's performance limit, since overall performance is bounded by whichever is smaller. — [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html)
- **[Volume type selection]** Choose `io2`/`io2` Block Express for workloads needing the highest, most consistent IOPS and throughput on a single volume, and `gp3` for the best balance of price and performance for most workloads. — [doc](https://aws.amazon.com/ebs/features/)
- **[Scaling beyond a single volume]** Stripe multiple EBS volumes of the same size and performance characteristics (for example with RAID 0/LVM) when a single volume cannot meet required IOPS or throughput. — [doc](https://docs.aws.amazon.com/ebs/latest/userguide/raid-config.html)
- **[Snapshot-restored volumes]** Initialize volumes created from a snapshot (pre-warm by reading every block) to avoid the first-read latency penalty and achieve maximum read performance immediately. — [doc](https://aws.amazon.com/blogs/apn/build-sparse-ebs-volumes-for-fun-and-easy-snapshotting/)
- **[Monitoring]** Track the `VolumeReadOps` and `VolumeWriteOps` CloudWatch metrics against your configured IOPS limit and alarm before the threshold is reached to avoid latency-driven performance degradation. — [doc](https://aws.amazon.com/blogs/storage/valuable-tips-for-monitoring-and-understanding-amazon-ebs-performance-using-amazon-cloudwatch/)

## 💰 Cost Optimization
- **[Volume type migration]** Migrate `gp2` volumes to `gp3`, which offers a lower price per GiB and lets you scale IOPS and throughput independently of volume size. — [doc](https://docs.aws.amazon.com/wellarchitected/latest/microsoft-workloads-lens/msftcost05-bp01.html)
- **[Right-sizing]** Avoid oversizing `gp2` volumes just to reach higher IOPS; on `gp3` you can provision the IOPS/throughput you need without overprovisioning capacity. — [doc](https://docs.aws.amazon.com/wellarchitected/latest/microsoft-workloads-lens/msftcost05-bp01.html)
- **[Recommendations]** Use AWS Compute Optimizer to identify EBS volumes that should be upgraded to newer-generation types (such as `gp3`/`io2`) and to estimate savings before migrating. — [doc](https://aws.amazon.com/blogs/storage/cost-optimizing-amazon-ebs-volumes-using-aws-compute-optimizer/)
- **[Idle resource cleanup]** Identify and remove (or snapshot-and-delete) EBS volumes that have been unattached for an extended period to eliminate unnecessary storage spend. — [doc](https://docs.aws.amazon.com/compute-optimizer/latest/ug/automation-rec.html)
- **[Snapshot lifecycle]** Use Amazon Data Lifecycle Manager to automate snapshot creation, retention, and deletion so outdated backups don't accumulate unnecessary storage cost. — [doc](https://aws.amazon.com/ebs/snapshots/)
- **[Long-term retention]** Move rarely accessed, long-term snapshots to EBS Snapshots Archive for lower-cost storage instead of keeping them in standard snapshot storage. — [doc](https://aws.amazon.com/ebs/snapshots/)
- **[Governance]** Tag EBS volumes consistently to support cost allocation, ownership tracking, and automated sprawl management. — [doc](https://aws.amazon.com/blogs/apn/maximizing-storage-performance-and-savings-with-amazon-ebs-gp3-and-ollion/)

## ⚙️ Operational Excellence
- **[Monitoring]** Use Amazon CloudWatch metrics (delivered automatically at one-minute intervals) to view, analyze, and alarm on EBS volume operational behavior. — [doc](https://docs.aws.amazon.com/whitepapers/latest/optimizing-mysql-on-ec2-using-amazon-ebs/ebs-volume-features.html)
- **[Infrastructure as code]** Define and provision EBS volumes and related resources with CloudFormation or similar IaC tooling to ensure consistent configuration and easier governance at scale. — [doc](https://aws.amazon.com/blogs/apn/maximizing-storage-performance-and-savings-with-amazon-ebs-gp3-and-ollion/)
- **[Compliance auditing]** Use AWS Config to continually assess and audit EBS volume configurations against your organization's standards (for example, flagging non-compliant volume types or missing encryption). — [doc](https://aws.amazon.com/blogs/apn/maximizing-storage-performance-and-savings-with-amazon-ebs-gp3-and-ollion/)
- **[Snapshot governance]** Apply retention rules in Recycle Bin, with exclusion tags for temporary/non-production snapshots, to standardize how long deleted snapshots and AMIs are recoverable. — [doc](https://aws.amazon.com/blogs/storage/reduce-costs-with-customized-delete-protection-for-amazon-ebs-snapshots-and-ebs-backed-amis/)

<!-- meta: last_reviewed=2026-07-05; sources=21 -->
