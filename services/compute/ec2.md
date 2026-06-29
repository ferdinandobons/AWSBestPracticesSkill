# Amazon EC2 - Best Practices

## Common scenarios
- Stateless web/app tier behind a load balancer that must survive instance and AZ failure -> reliability
- Steady-state always-on compute with predictable baseline usage -> cost optimization
- Fault-tolerant, interruption-flexible batch/CI/HPC processing -> cost optimization
- Internet-facing instances handling sensitive data with strict access control -> security

## 🔒 Security
- **[Access]** Manage access to AWS resources and APIs using identity federation with an identity provider and IAM roles instead of long-lived credentials - removes static keys from instances. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Network]** Implement the least permissive rules for your security groups, allowing only required ports and sources - traffic not explicitly allowed is denied by default. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Metadata]** Require IMDSv2 (token-based sessions) and disable IMDSv1 - adds session authentication and a hop limit that defends against SSRF and reverse-proxy attacks. [doc](https://aws.amazon.com/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/)
- **[Patching]** Regularly patch, update, and secure the guest OS and applications on your instances - keeps the layer you own under the shared responsibility model free of known vulnerabilities. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Vulnerability scanning]** Use Amazon Inspector to automatically discover and scan instances for software vulnerabilities and unintended network exposure - continuous detection instead of point-in-time audits. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Encryption at rest]** Encrypt EBS volumes and snapshots - protects instance data and its backups transparently. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Encryption in transit]** Use TLS to access EC2 APIs and require TLS 1.2 (TLS 1.3 recommended) with perfect-forward-secrecy cipher suites - protects credentials and API calls in flight. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/infrastructure-security.html)
- **[Posture management]** Use AWS Security Hub CSPM controls to monitor EC2 resources against security best practices and standards - flags drift from baseline continuously. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)

## 🛡️ Reliability
- **[Multi-AZ]** Deploy critical components across multiple Availability Zones and replicate data appropriately - AZs fail over without interruption and are more fault tolerant than single-DC designs. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Self-healing]** Use Amazon EC2 Auto Scaling with Elastic Load Balancing health checks so unhealthy instances are replaced automatically and traffic is rerouted to healthy ones. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/disaster-recovery-resiliency.html)
- **[Capacity diversity]** Use as many instance types as your workload allows and spread instances across all AZs in the Region - avoids being blocked by a single constrained capacity pool. [doc](https://aws.amazon.com/blogs/compute/how-to-prepare-your-application-to-scale-reliably-with-amazon-ec2/)
- **[Backup]** Regularly back up EBS volumes with snapshots and create AMIs as launch templates, automating both with Amazon Data Lifecycle Manager or AWS Backup - enables fast, repeatable recovery. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Failover]** Design applications to handle dynamic IP addressing on restart and test instance/volume recovery regularly - verifies that data and services actually restore. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[DR]** Copy AMIs and EBS snapshots across Regions for geographically separated recovery - protects against Region-level disruption. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/disaster-recovery-resiliency.html)

## ⚡ Performance Efficiency
- **[Right sizing]** Analyze CloudWatch CPU, memory, and network data to identify idle and underutilized instances (e.g. max utilization under 40% over four weeks) and resize them - matches capacity to real demand. [doc](https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-right-sizing/tips-for-right-sizing-your-workloads.html)
- **[Memory visibility]** Install the unified CloudWatch agent to collect memory and disk utilization - these metrics aren't available by default and are required for accurate sizing recommendations. [doc](https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-ec2-recommendations.html)
- **[Scaling behavior]** Start scaling earlier, in smaller and more frequent chunks, rather than waiting for large spikes - smooths capacity acquisition and avoids overload of existing instances. [doc](https://aws.amazon.com/blogs/compute/how-to-prepare-your-application-to-scale-reliably-with-amazon-ec2/)

## 💰 Cost Optimization
- **[Commitments]** Use Savings Plans for steady-state usage to get lower prices (up to 72%) for a 1- or 3-year hourly commitment, with flexibility across instance family, size, OS, and Region - cuts spend on predictable baseline load. [doc](https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-reservation-models/savings-plans.html)
- **[Spot]** Run stateless, fault-tolerant, and flexible workloads on EC2 Spot Instances for up to 90% savings, staying diverse across instance types and AZs to reduce interruptions - uses spare capacity cheaply. [doc](https://docs.aws.amazon.com/whitepapers/latest/run-semiconductor-workflows-on-aws/cost-optimization.html)
- **[Right sizing]** Use AWS Compute Optimizer finding reasons to detect over-provisioned CPU, memory, and EBS throughput and move to cheaper instance types - eliminates spend on unused capacity. [doc](https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-ec2-recommendations.html)
- **[Recommendations]** Use AWS Trusted Advisor to inspect your environment for opportunities to save money, improve availability and performance, or close security gaps. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)

## ⚙️ Operational Excellence
- **[Patch automation]** Use AWS Systems Manager Patch Manager with maintenance windows and patch baselines to scan and install OS/application patches across fleets on a schedule - removes manual, error-prone patching. [doc](https://aws.amazon.com/blogs/mt/patching-your-windows-ec2-instances-using-aws-systems-manager-patch-manager/)
- **[Tagging]** Use instance metadata and custom resource tags to track and identify resources - underpins automation, cost allocation, and patch grouping. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Quotas]** Review your EC2 service quotas and request increases in advance of when you'll need them - avoids launch failures during scaling events. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- **[Monitoring]** Monitor and respond to EC2 events using CloudWatch and EC2 monitoring - surfaces health and reachability issues before they cause outages. [doc](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)

<!-- meta: last_reviewed=2026-06-29; sources=11 -->
