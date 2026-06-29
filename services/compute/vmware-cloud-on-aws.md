# VMware Cloud on AWS - Best Practices

## Common scenarios
- Lift-and-shift migration of on-premises vSphere workloads to AWS with no re-platforming -> operational excellence
- High-availability production workloads needing host and Availability Zone fault protection -> reliability
- Hybrid cloud and disaster recovery with a managed SDDC failover site -> reliability
- Extending VMware VMs with native AWS services (storage, security, analytics) over the connected VPC -> performance efficiency

## 🔒 Security
- **[Shared responsibility]** Treat the SDDC as a managed service where VMware secures the underlying stack and you secure guest VMs, data, and network rules - prevents coverage gaps because VMC is not agentless-integrated with services like GuardDuty/Inspector. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Identity]** Federate the SDDC with a central identity provider and enforce MFA with least-privilege roles - centralizes authentication and reduces standing access. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Infrastructure protection]** Configure SDDC gateway firewalls, VPC route tables, security groups, and NACLs with a zero-trust, defense-in-depth posture - layered segmentation limits lateral movement between SDDC and VPCs. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Threat detection]** Log SDDC user, network, and application activity and forward to a SIEM or CloudWatch (Aria Operations for Logs, IPFIX, port mirroring) - you own threat detection inside the SDDC. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Vulnerability management]** Scan and patch guest workloads yourself (e.g. with AWS Systems Manager) - VMware patches the SDDC and service components, but in-VM patching is your responsibility. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Compliance integration]** Aggregate VMC and native findings into AWS Security Hub rather than running two parallel systems - unifies the security and compliance landscape across SDDC and VPC. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)

## 🛡️ Reliability
- **[Host resiliency]** Set vSAN FTT to 1 or greater (FTT-2/RAID-6 for clusters of six or more hosts) - VMs with FTT=0 can lose data on host failure, and FTT-1 on large clusters voids the availability guarantee. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Multi-AZ]** Use a stretched cluster with Dual Site Mirroring for workloads needing AZ-level availability - data is synchronously replicated across AZs so vSphere HA restarts VMs in the surviving AZ. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Connectivity]** For production, run at least two virtual interfaces over separate Direct Connect connections terminating at different DX locations, with VPN as backup - eliminates single points of failure in the network path. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Backups]** Back up the WorkloadDatastore (VMs, policies, configurations) and test restores in a location outside the SDDC - infrastructure backups are daily-only with no granular or point-in-time restore. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Change capture]** Record vCenter/NSX configuration changes in change logs and via the VMC API - changes are not backed up until the next daily backup, so capture them to enable recovery. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Disaster recovery]** Implement a DR plan with a pilot-light or on-demand recovery SDDC and cross-Region backups - protects against Region-level disasters and meets regulatory RPO/RTO. [doc](https://aws.amazon.com/blogs/apn/addressing-multiple-disaster-recovery-slas-with-vmware-cloud-on-aws/)
- **[Cross-Region data]** Store S3 backups and replicate FSx/EFS file data across Regions and AZs using AWS DataSync - regional replication is not on by default and must be configured to meet recovery requirements. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)

## ⚡ Performance Efficiency
- **[Co-location]** Deploy the SDDC and the connected VPC in the same Region and AZ as your native AWS workloads - same-AZ traffic over the ENI gives high bandwidth, low latency, and avoids cross-AZ data charges. [doc](https://docs.aws.amazon.com/whitepapers/latest/sddc-deployment-and-best-practices/account-requirements.html)
- **[Dedicated bandwidth]** Use AWS Direct Connect instead of VPN when sustained SDDC-to-on-premises traffic exceeds 1 Gbps or needs consistent latency - VPN cannot match Direct Connect throughput and performance consistency. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[Storage tuning]** Tune vSAN (disk striping, cache policy, per-VM IOPS limits) and choose io2 or gp3 EBS for integrated AWS storage - matches storage performance to workload demand. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-storage-for-vmware-professionals/optimizing-cost-and-performance.html)

## 💰 Cost Optimization
- **[Traffic placement]** Keep SDDC workloads in the same AZ as the dependent AWS resources - cross-AZ and inter-Region traffic to the customer-owned account is billable, so co-location avoids unnecessary data transfer charges. [doc](https://docs.aws.amazon.com/whitepapers/latest/sddc-deployment-and-best-practices/account-requirements.html)
- **[Right-sizing]** Carve SDDC capacity into resource pools and start small, expanding only as demand grows - reduces upfront commitment and aligns spend to usage. [doc](https://aws.amazon.com/blogs/apn/managing-msp-costs-with-vmware-cloud-director-service-multi-tenancy/)
- **[Backup storage]** Store SDDC backups on Amazon S3 via Storage Gateway/File Gateway - lower-cost durable backup target than keeping copies inside the SDDC. [doc](https://aws.amazon.com/blogs/apn/resiliency-design-considerations-and-best-practices-for-vmware-cloud-on-aws/)
- **[DR economics]** Use an on-demand or pilot-light DR SDDC that scales up only during a disaster - pay for a minimal footprint until failover instead of a full idle recovery site. [doc](https://aws.amazon.com/blogs/apn/addressing-multiple-disaster-recovery-slas-with-vmware-cloud-on-aws/)

## ⚙️ Operational Excellence
- **[Tooling consistency]** Migrate with the same VMware tools and processes used on-premises (HCX, vCenter, NSX) - preserves operational consistency and reduces migration risk. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Operations management]** Use AWS Systems Manager to manage VMC operations and patch guest VMs - extends native AWS operational tooling into the SDDC. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)
- **[Incident response]** Maintain runbooks and run game-day exercises for VMC security and operational events - rehearsed response and post-incident root-cause analysis reduce time to recover. [doc](https://aws.amazon.com/blogs/apn/how-to-leverage-the-aws-cloud-adoption-framework-for-vmware-cloud-on-aws/)

<!-- meta: last_reviewed=2026-06-29; sources=8 -->
