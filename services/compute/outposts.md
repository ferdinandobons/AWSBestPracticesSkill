# AWS Outposts - Best Practices

## Common scenarios
- Low-latency / local data processing workloads that must run on-premises but stay consistent with AWS APIs -> performance
- Data residency and regulated workloads that cannot leave a physical jurisdiction -> security
- Mission-critical on-premises applications that need high availability and failover during host or network failures -> reliability
- Shared multi-account Outpost where finite compute must be allocated and monitored across teams -> cost

## 🔒 Security
- **[Encryption at rest]** Rely on Outposts always-on encryption and use Amazon EBS encryption with AWS KMS keys for volumes and snapshots - the Nitro Security Key (NSK) wraps the key material so data is unreadable if the device is removed. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/data-protection.html)
- **[Physical access]** Restrict and control physical access to Outpost locations with keys and biometrics, and limit the number of authorized people - removing the NSK or losing access controls is a high-risk path to data exposure. [doc](https://docs.aws.amazon.com/wellarchitected/latest/data-residency-hybrid-cloud-services-lens/drhcsec06-bp02.html)
- **[IAM least privilege]** Start from AWS managed policies, then tighten to customer managed least-privilege policies and add conditions (for example require SSL) - grant only the actions needed on specific resources. [doc](https://docs.aws.amazon.com/outposts/latest/network-userguide/security_iam_id-based-policy-examples.html)
- **[Policy validation]** Validate IAM policies with IAM Access Analyzer and require MFA for privileged actions - over 100 automated checks catch insecure or overly broad permissions before they ship. [doc](https://docs.aws.amazon.com/outposts/latest/network-userguide/security_iam_id-based-policy-examples.html)
- **[In-transit]** Access Outposts APIs only over TLS 1.2 or later (TLS 1.3 recommended) with cipher suites that provide perfect forward secrecy - protects control-plane traffic between your clients and AWS. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/infrastructure-security.html)
- **[Network inspection]** Implement firewall and traffic-inspection controls (by port, CIDR, or protocol) to protect Outpost network resources - block unwanted traffic at the on-premises boundary. [doc](https://docs.aws.amazon.com/wellarchitected/latest/data-residency-hybrid-cloud-services-lens/infrastructure-protection.html)

## 🛡️ Reliability
- **[Power & network]** Provide dual power sources and redundant network connectivity to each Outpost - removes single points of failure in the facility supporting the rack. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/disaster-recovery-resiliency.html)
- **[Spare capacity]** Provision N+1 always-active capacity per instance family for mission-critical workloads - lets EC2 auto recovery fail over to a healthy host when an underlying host fails. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/disaster-recovery-resiliency.html)
- **[Multi-AZ]** Deploy across multiple Outposts, each attached to a different Availability Zone - avoids dependence on a single AZ for control-plane and application resilience. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/disaster-recovery-resiliency.html)
- **[Placement]** Use spread placement groups so interdependent instances land on distinct racks or hosts - reduces the blast radius of correlated hardware failures. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/disaster-recovery-resiliency.html)
- **[Service link]** Create a redundant service link connection (for example via Direct Connect resiliency) for workloads with high-availability requirements - network outages can otherwise disrupt Outpost workflows. [doc](https://aws.amazon.com/blogs/compute/multi-rack-and-multiple-logical-aws-outposts-architecture-considerations-for-resiliency/)
- **[Auto Scaling + ALB]** Run instances behind EC2 Auto Scaling with an Application Load Balancer on the Outpost - distributes traffic and replaces unhealthy instances automatically. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/disaster-recovery-resiliency.html)
- **[Instance store backup]** On Outposts servers, back up instance-store data to Amazon S3 or on-premises storage - instance-store volumes do not persist after instance termination. [doc](https://docs.aws.amazon.com/outposts/latest/server-userguide/disaster-recovery-resiliency.html)

## ⚡ Performance Efficiency
- **[Placement control]** Use Dedicated Hosts auto-placement and host affinity to control instance placement at the hardware level - pins workloads and minimizes the impact of correlated hardware failures. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-optimizations.html)
- **[Capacity layout]** Tune the server capacity layout (homogeneous vs heterogeneous instance types) to match your workload mix - gets the most usable vCPU out of finite Outpost compute. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-optimizations.html)

## 💰 Cost Optimization
- **[Right-size order]** Size the initial Outpost order for current workloads, future growth, and spare capacity for failures - compute and storage are finite and fixed by the assets AWS installs. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-capacity.html)
- **[Capacity tasks]** Reconfigure instance sizes and quantities non-disruptively with capacity tasks as demand shifts, keeping production instances "as-is" - reclaims stranded capacity without re-ordering hardware. [doc](https://docs.aws.amazon.com/outposts/latest/server-userguide/modify-instance-capacity.html)
- **[License reuse]** Use Dedicated Hosts on Outposts to apply existing per-socket, per-core, or per-VM software licenses - avoids buying new licenses for capacity you already own. [doc](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-optimizations.html)
- **[Shared utilization]** In multi-account setups, monitor per-account capacity utilization and enforce soft/hard limits with centralized dashboards - ensures fair allocation and supports chargeback. [doc](https://aws.amazon.com/solutions/guidance/multi-account-outposts-operations-on-aws/)

## ⚙️ Operational Excellence
- **[Capacity monitoring]** Track EC2 and EBS capacity-availability and CapacityExceptions metrics in CloudWatch with alarms - prevents teams from exhausting finite Outpost capacity unnoticed. [doc](https://aws.amazon.com/blogs/mt/monitoring-best-practices-for-aws-outposts/)
- **[Connectivity alarm]** Alarm on the ConnectedStatus service-link metric and BGP status of the local gateway/LNI - surfaces uplink or on-premises network problems before they impact workloads. [doc](https://docs.aws.amazon.com/outposts/latest/server-userguide/outposts-cloudwatch-metrics.html)
- **[Dashboards & reviews]** Build CloudWatch dashboards and review capacity and network trends on a regular cadence - aligns with the Operational Excellence pillar's practice of reviewing metrics over time. [doc](https://aws.amazon.com/blogs/mt/monitoring-best-practices-for-aws-outposts/)
- **[Audit & events]** Capture API activity with CloudTrail and subscribe to AWS Health Dashboard events for service-link and maintenance notifications - gives traceability and early warning of platform changes. [doc](https://docs.aws.amazon.com/outposts/latest/server-userguide/monitor-outposts.html)

<!-- meta: last_reviewed=2026-06-29; sources=15 -->
