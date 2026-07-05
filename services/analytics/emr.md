# Amazon EMR — Best Practices

## Common scenarios
- Large-scale Spark/Hadoop/Hive ETL and data processing        → Performance Efficiency, Cost Optimization
- Ad hoc big data analytics and interactive querying on a data lake        → Performance Efficiency, Reliability
- Long-running or transient batch processing clusters        → Cost Optimization, Operational Excellence
- Multi-tenant clusters shared across teams or applications        → Security, Operational Excellence

## 🔒 Security
- **[IAM]** Grant least-privilege permissions in the EMR service role, EC2 instance profile, and any runtime roles instead of relying on overly broad defaults — start minimal and add permissions as needed. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/security_iam_service-with-iam-policy-best-practices.html)
- **[IAM]** Use EMRFS runtime roles (fine-grained authorization) on multi-tenant clusters so different users or jobs assume different IAM roles when accessing Amazon S3, instead of inheriting one cluster-wide instance profile. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-securing-amazon-emr/)
- **[Authentication]** Require MFA for sensitive operations and use policy conditions (source IP, time window, SSL/MFA) to further restrict access to EMR resources. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/security_iam_service-with-iam-policy-best-practices.html)
- **[Encryption]** Enable an EMR security configuration to encrypt data at rest in EMRFS/Amazon S3 (SSE-S3, SSE-KMS, or CSE) and on cluster local disks/EBS volumes, and reuse the same configuration across clusters for consistency. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-data-encryption.html)
- **[Encryption]** Use AWS KMS symmetric keys for at-rest encryption of EMRFS and storage volumes, and enable in-transit encryption (TLS/SASL) for data moving between cluster nodes and to Amazon S3. [doc](https://docs.aws.amazon.com/kms/latest/developerguide/services-emr.html)
- **[Network]** Launch clusters in private subnets, restrict security groups so worker nodes only accept traffic from the master node, and use Amazon EMR block public access to prevent clusters from allowing unintended public access on any port. [doc](https://aws.amazon.com/emr/faqs/)
- **[Data protection]** Never place sensitive identifying information in free-form fields (names, tags) since this data can be captured in diagnostic logs; use AWS CloudTrail to log API and user activity for auditing. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/data-protection.html)
- **[Hardening]** Apply CIS controls to a custom AMI when you need root-volume encryption or additional OS hardening beyond what default EMR AMIs provide. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-securing-amazon-emr/)

## 🛡️ Reliability
- **[Spot Instances]** Diversify task fleets across many instance types (aim for roughly 15+) with a capacity-optimized allocation strategy so EMR can replenish capacity from the most available Spot pools when interruptions occur. [doc](https://aws.amazon.com/blogs/big-data/optimizing-amazon-emr-for-resilience-and-cost-with-capacity-optimized-spot-instances/)
- **[Spot Instances]** Run Spot Instances on task nodes rather than core nodes, since task nodes don't hold HDFS data and their loss doesn't force costly Hadoop replication rework. [doc](https://docs.aws.amazon.com/whitepapers/latest/cost-modeling-data-lakes/cost-optimization-in-analytics-services.html)
- **[Spot Instances]** Use the Spot Instance Advisor to select instance types with historically low interruption rates, increasing job fault tolerance. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-running-apache-spark-applications-using-amazon-ec2-spot-instances-with-amazon-emr/)
- **[Availability]** Specify subnet IDs across multiple Availability Zones for instance fleets to increase fault tolerance, even though a given EMR cluster itself runs in a single Availability Zone. [doc](https://aws.amazon.com/blogs/big-data/optimizing-amazon-emr-for-resilience-and-cost-with-capacity-optimized-spot-instances/)

## ⚡ Performance Efficiency
- **[Instance selection]** Benchmark new workloads on general-purpose instance types (e.g., m5, c5) first, monitor OS/YARN metrics for CPU, memory, storage, and I/O bottlenecks, then move to compute-, memory-, or storage-optimized families as needed. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-flexibility.html)
- **[Instance selection]** Avoid instance types with known compatibility gaps (e.g., c7a, c7i, m7i, m7i-flex, r7a, r7i, r7iz, i4i.12xlarge/24xlarge) on older EMR releases; upgrade to EMR 5.36.1+/6.10.0+ to get full performance benefits from newer instance generations. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html)
- **[Storage]** Use EMRFS with Amazon S3 as the primary data layer to decouple compute from storage, letting you size clusters for compute needs and terminate them when idle while data persists in S3. [doc](https://aws.amazon.com/emr/features/hadoop/)
- **[Scaling]** Enable EMR Managed Scaling so Amazon EMR continuously evaluates workload metrics and automatically resizes the cluster for optimal resource utilization and performance instead of relying on static sizing or custom scaling rules. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html)

## 💰 Cost Optimization
- **[Managed Scaling]** Enable EMR Managed Scaling with defined min/max compute limits so clusters scale up during peaks and scale down gracefully during idle periods, reducing costs versus fixed-size clusters. [doc](https://aws.amazon.com/blogs/big-data/reduce-amazon-emr-cluster-costs-by-up-to-19-with-new-enhancements-in-amazon-emr-managed-scaling/)
- **[Spot Instances]** Run task nodes on Spot Instances for interruption-tolerant, checkpointable workloads, reserving On-Demand for time-sensitive jobs that need guaranteed availability. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-resizing-and-automatic-scaling-in-amazon-emr/)
- **[Storage]** Store data in Amazon S3 via EMRFS rather than on-cluster HDFS so you can terminate clusters when not in use and avoid paying for idle compute just to retain storage capacity. [doc](https://aws.amazon.com/emr/features/)

## ⚙️ Operational Excellence
- **[Monitoring]** Configure the CloudWatch agent on EMR to stream custom Hadoop, YARN, and HBase metrics and cluster logs to CloudWatch for real-time visibility into cluster health and performance. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/enhanced-custom-metrics.html)
- **[Monitoring]** Set CloudWatch alarms on key EMR metrics (e.g., cluster idle status, HDFS utilization, node health) to detect and respond to issues proactively. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-manage-cluster-cloudwatch.html)
- **[Logging]** Archive step, job, and task log files to Amazon S3 so you can troubleshoot cluster issues even after the cluster has terminated. [doc](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview-benefits.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
