# AWS Elemental MediaConnect — Best Practices

## Common scenarios
- Live video contribution and transport of broadcast feeds into and across the AWS Cloud        → Reliability, Performance Efficiency
- Securely sharing live content with partners/customers via entitlements        → Security, Cost Optimization
- Building resilient, redundant transport paths for mission-critical live streams        → Reliability
- Distributing live sources to multiple downstream destinations (MediaLive, NDI receivers, on-prem)        → Performance Efficiency, Operational Excellence

## 🔒 Security
- **[Network access]** Scope each flow source's CIDR block as precisely as possible, including only the IP addresses that should contribute content — an overly broad CIDR allows outside parties to send content into the flow. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Encryption]** Encrypt flow sources, outputs, and entitlements in transit using static key encryption (via AWS Secrets Manager), SPEKE, or SRT password encryption, choosing the option that matches whether you control both endpoints or are sharing with an external partner. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/data-protection.html)
- **[Encryption]** When creating an SRT password in Secrets Manager, use a strong policy — minimum 10 characters (up to 80), at least three of uppercase/lowercase/numbers/symbols, and never identical to your account name or email. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Transport security]** Ensure clients accessing the MediaConnect API support TLS 1.2 (TLS 1.3 recommended) with perfect-forward-secrecy cipher suites such as DHE or ECDHE. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/infrastructure-security.html)
- **[IAM]** Start from AWS managed policies and move toward least-privilege customer-managed policies, granting only the actions needed on specific flow/entitlement resources. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Add IAM policy conditions (e.g., require SSL, restrict to calls made through a specific AWS service) to further scope access beyond action/resource grants. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer before deploying them, and require MFA for any human users/roles that can manage MediaConnect resources. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/security_iam_id-based-policy-examples.html)
- **[Networking]** For VPC sources and outputs, scope security groups tightly: inbound rules should allow only the specific private IP of the sending resource, and for combined source/output VPC interfaces on CDI flows the security group must be self-referential. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/vpc-interface-security-groups.html)
- **[Networking]** Dedicate a VPC specifically to AWS Media Services rather than sharing one broadly — this preserves IP address availability, simplifies security group rules, and reduces the risk of a network administrator accidentally deleting an in-use elastic network interface. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Entitlement sharing]** When sharing content across accounts via entitlements, prefer SPEKE (a third-party CA platform manages/rotates keys) over static key encryption when you need time-limited or revocable access, since static keys require manually notifying every party on rotation. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/data-protection.html)

## 🛡️ Reliability
- **[Redundancy]** Create flows in at least two different Availability Zones and add a second source to each flow so MediaConnect can pull redundant packets or fail over completely if one source degrades. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Source failover]** Use Merge mode (combining two binary-identical, SMPTE ST 2022-7–compliant sources) for graceful, packet-level recovery from single-source loss, and tune the recovery window to balance added latency against error-correction headroom. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/source-failover.html)
- **[Source failover]** Use Failover mode (primary/backup source switching) when sources are not binary-identical or when using SRT, since SRT does not support Merge mode. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/source-failover.html)
- **[Packet loss protection]** Use Forward Error Correction (FEC) or ARQ-based protocols such as Zixi or RTP-FEC to minimize packet loss between source and destination, since packet loss occurs even on fully managed networks like the AWS Cloud. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Monitoring]** Configure CloudWatch alarms on flow source health metrics (e.g., dropped/unrecovered packets) so degraded sources are surfaced and can trigger failover or operator response before viewers are impacted. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Monitoring]** Capture MediaConnect events (alerts, health status) from Amazon EventBridge into CloudWatch Logs to combine metrics with event context for a complete observability picture. [doc](https://aws.amazon.com/blogs/media/capturing-aws-elemental-mediaconnect-events-with-amazon-cloudwatch-logs/)

## ⚡ Performance Efficiency
- **[Protocol selection]** Choose the transport protocol based on network conditions and distance — Zixi or SRT for long-distance, high-availability links; RTP-FEC when self-healing from corruption/packet loss is needed; plain RTP or RIST when encryption is not required and bandwidth efficiency matters more. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/protocols.html)
- **[Bandwidth planning]** Keep transport stream flows within an aggregate output bandwidth of 400 Mb/s (source bitrate × number of outputs), counting dual-destination ST 2110 JPEG XS outputs twice. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Managed outputs]** For flows sending to MediaLive via managed outputs, keep the aggregate bitrate at or below 160 Mbps across managed and transport-stream outputs combined. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[NDI outputs]** Monitor for over-subscription signs (dropped frames, stuttering, dropped NDI connections) as you scale NDI receivers, and calculate aggregate NDI output + receiver bandwidth against the flow size's total throughput capacity (large flow size supports up to 2.5 Gbps). [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[NDI outputs]** Limit NDI configuration to a single interface adapter per VPC — multiple VPC interfaces can confuse the NDI discovery server and cause unexpected routing behavior. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)
- **[Gateways]** When starting multiple bridges programmatically via the API, start no more than 10 at a time and issue additional requests for larger batches. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/best-practices.html)

## 💰 Cost Optimization
- **[Tagging]** Apply consistent tags (e.g., CostCenter, Environment, Project) to flows, sources, outputs, and entitlements, and activate them as cost allocation tags to attribute MediaConnect spend accurately in AWS Billing and Cost Management. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/tagging.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Use CloudWatch metrics (retained 15 months, down to 1-second resolution for most flow metrics) to track flow health and performance trends, and build dashboards/alarms around them. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/monitor-with-cloudwatch.html)
- **[Auditing]** Enable AWS CloudTrail to capture MediaConnect API calls, so you can identify which users/accounts made changes, the source IP, and when — essential for troubleshooting unexpected flow configuration changes. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/monitor.html)
- **[Event-driven ops]** Use Amazon EventBridge to build automated, event-driven responses to MediaConnect state changes and alerts rather than relying on manual console monitoring. [doc](https://docs.aws.amazon.com/mediaconnect/latest/ug/monitor.html)
- **[Secret rotation]** When using static key encryption for entitlements shared across accounts, plan the operational process for key rotation up front — all parties (granter and subscriber) must update in sync, or downstream decryption fails. [doc](https://aws.amazon.com/blogs/media/improve-operational-processes-for-aws-elemental-mediaconnect-using-aws-cdk/)
- **[Infrastructure as code]** Automate provisioning of the flows, IAM roles, Secrets Manager secrets, and KMS keys involved in cross-account entitlement sharing (e.g., via AWS CDK) instead of manual console setup, to reduce configuration drift and manual key-sharing risk. [doc](https://aws.amazon.com/blogs/media/improve-operational-processes-for-aws-elemental-mediaconnect-using-aws-cdk/)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
