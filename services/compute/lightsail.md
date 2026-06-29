# Amazon Lightsail - Best Practices

## Common scenarios
- Public WordPress / web app on a single VPS instance -> security, reliability
- Highly available multi-instance site behind a Lightsail load balancer -> reliability, performance
- Static media and assets served from a Lightsail bucket + CDN distribution -> performance, cost
- Production MySQL/PostgreSQL on a Lightsail managed database -> reliability, operational excellence

## 🔒 Security
- **[Instance firewall]** Open only the ports your role needs and scope inbound rules to specific source IP addresses or CIDR ranges instead of the whole internet - minimizes the attack surface, especially for SSH/RDP management access. [doc](https://aws.amazon.com/blogs/compute/enhancing-site-security-with-new-lightsail-firewall-features/)
- **[Remote access]** Disable browser-based and remote access (SSH/RDP) when not in use and restrict it by source IP - reduces exposure of management interfaces to unauthorized connections. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-firewall-and-port-mappings-in-amazon-lightsail.html)
- **[IAM]** Start from AWS managed policies then narrow to least-privilege customer policies, add conditions, and validate with IAM Access Analyzer - grants only the permissions a task requires and catches risky policies early. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Buckets]** Keep buckets and objects private by default and rely on S3 account-level Block Public Access - prevents accidental public exposure of stored data regardless of per-object settings. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bucket-security-best-practices.html)
- **[Bucket access]** Attach instances to buckets via resource access instead of storing access keys on the instance, and rotate keys when keys are required - avoids long-lived embedded credentials and the burden of manual rotation. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bucket-security-best-practices.html)
- **[In transit]** Use TLS 1.2 or later (1.3 recommended) with perfect-forward-secrecy cipher suites for all API access and serve site traffic over HTTPS - protects credentials and data in transit. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/infrastructure-security.html)
- **[WAF]** Front internet-facing Lightsail instances with CloudFront or an ALB (via VPC peering) protected by AWS WAF - adds managed rules against SQL injection, XSS, and DDoS that the Lightsail firewall alone cannot provide. [doc](https://aws.amazon.com/blogs/compute/integrating-aws-waf-with-your-amazon-lightsail-instance/)
- **[Metadata]** Enforce IMDSv2 (token-backed sessions) and watch the MetadataNoToken metric for IMDSv1 access - prevents credential theft through server-side request forgery against instance metadata. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-viewing-instance-health-metrics.html)

## 🛡️ Reliability
- **[Backups]** Enable automatic snapshots for instances, disks, and databases, and promote important ones to manual snapshots so they are retained beyond the rolling 7-snapshot limit - gives you point-in-time recovery from corruption or accidental deletion. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-snapshots-in-amazon-lightsail.html)
- **[DR]** Copy snapshots to a second AWS Region - lets you rebuild instances and disks if a Region or Availability Zone becomes unavailable. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/disaster-recovery-resiliency.html)
- **[High availability]** Place multiple instances across different Availability Zones behind a Lightsail load balancer with health checks - keeps the site reachable when a single instance or AZ fails. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/disaster-recovery-resiliency.html)
- **[Database HA]** Choose a high availability database plan for production workloads - provisions a synchronous standby in another AZ with automatic failover during failures and maintenance. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-high-availability-databases.html)

## ⚡ Performance Efficiency
- **[CDN]** Put a Lightsail distribution in front of your instance, load balancer, or bucket to cache static content at edge locations - reduces latency for global users and offloads requests from the origin during traffic spikes. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-content-delivery-network-distributions.html)
- **[Offload media]** Store and serve images, video, and other static assets from a Lightsail bucket plus distribution rather than the instance disk - frees instance CPU and storage to handle dynamic application load. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-using-distributions-with-buckets.html)
- **[Burst capacity]** Watch the CPU sustainable vs burstable zones and BurstCapacity metrics, and size the bundle so steady-state load stays in the sustainable zone - bursting only sustains short spikes, so a chronically burstable instance is undersized. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-viewing-instance-health-metrics.html)

## 💰 Cost Optimization
- **[Right-size]** Establish a metrics baseline and use it to match the instance and database bundle to actual CPU, network, and storage usage - burstable instances let you avoid over-provisioning for occasional peaks. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-viewing-instance-health-metrics.html)
- **[Scale out]** Export snapshots to Amazon EC2 when you outgrow Lightsail bundle limits - moves you to the wider range of EC2 instance types and AWS services instead of overpaying within Lightsail. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-snapshots-in-amazon-lightsail.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Monitor instance, database, load balancer, distribution, and bucket metrics regularly and establish a normal-performance baseline - makes multi-point failures easier to debug when they occur. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-resource-health-metrics.html)
- **[Alarms]** Configure Lightsail alarms with notification thresholds (email/SMS) on key metrics - alerts you when resources operate outside expected bounds before users are impacted. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-viewing-instance-health-metrics.html)
- **[Auditing]** Tag buckets and resources, enable access logging, and record control-plane API activity with AWS CloudTrail - provides the audit trail needed for periodic security and access reviews. [doc](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bucket-security-best-practices.html)

<!-- meta: last_reviewed=2026-06-29; sources=20 -->
