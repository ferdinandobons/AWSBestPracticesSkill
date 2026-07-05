# AWS Elastic Disaster Recovery — Best Practices

## Common scenarios
- Failing over on-premises or cross-cloud servers to AWS during a disaster        → Reliability, Operational Excellence
- Cross-Region or cross-AZ disaster recovery for AWS-hosted workloads        → Reliability
- Ransomware recovery using point-in-time recovery snapshots        → Reliability, Security
- Migrating servers to AWS using DRS as a migration path        → Reliability, Cost Optimization

## 🔒 Security
- **[access management]** Grant least-privilege access with the DRS managed policies (e.g., AWSElasticDisasterRecoveryAgentInstallationPolicy) instead of broad IAM permissions — limits blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/drs/latest/userguide/identity-access-management.html)
- **[agent installation]** Control who can install the AWS Replication Agent via an assumable IAM role scoped with permission boundaries — installing an agent immediately starts billing and creates replication resources. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[access keys]** Manually delete IAM access keys used for agent installation once agents are running and recovery is validated — AWS does not auto-delete keys except after disconnection. [doc](https://docs.aws.amazon.com/drs/latest/userguide/infrastructure-security.html)
- **[network exposure]** Restrict replication servers to the CIDR range of source servers using security groups, or connect via VPN/Direct Connect instead of the public internet. [doc](https://docs.aws.amazon.com/drs/latest/userguide/infrastructure-security.html)
- **[data protection]** Enable Amazon EBS encryption for replication and recovery volumes. [doc](https://docs.aws.amazon.com/drs/latest/userguide/infrastructure-security.html)
- **[recovery instances]** After recovery, verify only required ports are exposed to the public internet and harden the OS/application packages on recovery instances. [doc](https://docs.aws.amazon.com/drs/latest/userguide/security.html)
- **[DDoS protection]** Activate AWS Shield on the account hosting replication and recovery instances to reduce denial-of-service risk. [doc](https://docs.aws.amazon.com/drs/latest/userguide/security.html)
- **[point-in-time snapshots]** Protect point-in-time (PIT) recovery snapshots from deletion (e.g., via IAM restrictions) since a breach that deletes them removes your ability to recover from an earlier, uncompromised state. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[transport security]** Ensure clients support TLS 1.2+ with perfect-forward-secrecy cipher suites (DHE/ECDHE), which DRS uses for all agent-to-service and replication-server-to-service communication. [doc](https://docs.aws.amazon.com/drs/latest/userguide/infrastructure-security.html)

## 🛡️ Reliability
- **[recovery plan]** Maintain a written, detailed recovery plan covering launch order, validation steps, and DNS re-routing ownership — DRS handles replication and instance launch, but failover routing (e.g., via Amazon Route 53) is your responsibility. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[drills]** Run non-disruptive recovery drills regularly (at least several times a year) and include failback testing, since drills do not affect source replication or performance. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[termination protection]** Enable EC2 termination protection on recovery instances after launch-validation and before re-routing traffic to prevent accidental termination during a real event. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[recovery dos and don'ts]** Never use "Disconnect from AWS" on source servers with active recovery instances — it terminates replication resources and deletes point-in-time recovery points you may still need. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[replication monitoring]** Monitor the Servers list "Ready for recovery" and "Data replication status" columns, and act on servers showing Stalled or persistent Lag. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[event-driven alerting]** Use Amazon EventBridge rules (with Amazon SNS notifications) to automatically alert on replication state changes such as Stalled, Disconnected, or Lag instead of relying on manual console checks. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[scale limits]** Plan account and Region architecture around the 300-concurrently-replicating-source-servers-per-account limit; use multiple staging accounts or target Regions for larger environments. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[multi-account isolation]** Use dedicated AWS accounts for staging areas so other workload activity doesn't compete with, or throttle, disaster recovery replication traffic. [doc](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-of-on-premises-applications-to-aws/disaster-recovery-implementation.html)
- **[network design]** Host the staging area subnet in a different Availability Zone than recovery subnets for in-Region DR, adding redundancy so a single AZ failure doesn't affect both staging and recovery. [doc](https://docs.aws.amazon.com/sap/latest/general/key-considerations.html)
- **[drill compliance at scale]** Track each source server's last drill/recovery date via the `describe-source-servers` API (`lifeCycle.lastLaunch`) and flag servers not tested within your required interval. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[network capacity]** Benchmark source-to-staging network bandwidth before deploying agents at scale, and size for aggregate write throughput across all source servers with headroom for spikes. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)

## ⚡ Performance Efficiency
- **[replication server sizing]** Use dedicated replication servers with higher-IOPS/throughput instance types for high-write-rate source servers (e.g., databases) identified through storage benchmarking, rather than the shared default sizing. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[data reduction]** Exclude high-churn volumes not needed for recovery (such as tempdb or backup disks) using the installer `--devices` parameter to reduce replication load. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[replication server monitoring]** Monitor replication server CPUUtilization and NetworkIn via CloudWatch to determine whether to resize replication server instance types or change EBS disk types. [doc](https://aws.amazon.com/blogs/storage/disaster-recovery-monitoring-of-aws-elastic-disaster-recovery/)
- **[consolidation]** Keep Replication Settings (staging subnet, instance type, dedicated-instance flag) identical across as many source servers as possible so DRS can consolidate them onto shared replication servers efficiently. [doc](https://docs.aws.amazon.com/drs/latest/userguide/individual-replication-settings.html)

## 💰 Cost Optimization
- **[replication server sizing]** Use default instance types for replication servers unless source servers frequently show lag, avoiding over-provisioning. [doc](https://docs.aws.amazon.com/guidance/latest/deploying-cross-region-disaster-recovery-with-aws-elastic-disaster-recovery/monitoring.html)
- **[storage type]** Use automated/optimized disk type selection for staging disks rather than manually over-specifying high-performance volumes. [doc](https://docs.aws.amazon.com/guidance/latest/deploying-cross-region-disaster-recovery-with-aws-elastic-disaster-recovery/monitoring.html)
- **[snapshot retention]** Set point-in-time snapshot retention to the minimum needed for your recovery objectives, and use a dedicated backup solution for long-term retention/archiving instead of DRS. [doc](https://docs.aws.amazon.com/guidance/latest/deploying-cross-region-disaster-recovery-with-aws-elastic-disaster-recovery/monitoring.html)
- **[drill hygiene]** Terminate drill instances promptly after each drill and record termination as an explicit step in the recovery plan, since drill instances accrue standard EC2 charges while running. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[cost visibility]** Activate the AWSElasticDisasterRecoveryManaged cost allocation tag and build cost categories to track and report DRS-related EC2, EBS, and snapshot spend. [doc](https://docs.aws.amazon.com/guidance/latest/deploying-cross-region-disaster-recovery-with-aws-elastic-disaster-recovery/monitoring.html)
- **[consolidation]** Standardize Replication Settings across source servers to enable server consolidation onto shared replication servers, reducing EC2 usage. [doc](https://docs.aws.amazon.com/drs/latest/userguide/individual-replication-settings.html)

## ⚙️ Operational Excellence
- **[monitoring dashboard]** Build a CloudWatch dashboard using DRS metrics (LagDuration, Backlog, DurationSinceLastSuccessfulRecoveryLaunch, ElapsedReplicationDuration, ActiveSourceServerCount) for a single operational view of DR readiness. [doc](https://docs.aws.amazon.com/guidance/latest/deploying-cross-region-disaster-recovery-with-aws-elastic-disaster-recovery/monitoring.html)
- **[automation]** Create recovery network resources (VPCs, subnets, security groups) via a CloudFormation template that can be deployed on demand rather than keeping them running unused, and record the required server/application launch order in the recovery plan. [doc](https://docs.aws.amazon.com/drs/latest/userguide/best_practices_drs.html)
- **[agent deployment at scale]** Automate Replication Agent deployment across many servers using tools like AWS Systems Manager Run Command, deploying in batches and using `--no-prompt` for unattended installs to stay within API limits. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[governance at scale]** Use AWS Organizations and Service Control Policies to enforce consistent IAM guardrails across multiple staging/recovery accounts. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)
- **[service quotas]** Review and proactively request increases for DRS and EC2 service quotas (e.g., 300 concurrently replicating source servers per account, 100 source servers per recovery job) before scaling deployments. [doc](https://docs.aws.amazon.com/drs/latest/userguide/drs-at-scale.html)

<!-- meta: last_reviewed=2026-07-05; sources=10 -->
