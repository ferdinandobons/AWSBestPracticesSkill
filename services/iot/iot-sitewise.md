# AWS IoT SiteWise — Best Practices

## Common scenarios
- Ingesting and modeling industrial equipment data at scale        → Performance Efficiency, Cost Optimization
- Real-time monitoring, alarms, and OEE/KPI dashboards for plant operations        → Reliability, Operational Excellence
- Bridging OPC UA / on-prem historian data to the cloud via SiteWise Edge gateways        → Security, Reliability
- Long-term storage and analytics on historical industrial time-series data        → Cost Optimization, Performance Efficiency

## 🔒 Security
- **[Identity and access]** Grant SiteWise Monitor portal and project users only the minimum set of assets and permissions needed, and remove access promptly when it's no longer required — limits blast radius from compromised or stale accounts. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security-best-practices.html)
- **[Identity and access]** Start from AWS managed policies, then author customer managed least-privilege IAM policies scoped to specific actions, resources, and conditions — reduces over-broad permissions beyond what each workload needs. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Identity and access]** Validate IAM policies with IAM Access Analyzer and require multi-factor authentication (MFA) for IAM users and the root user — catches unintended access grants and hardens account takeover resistance. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Data protection]** Require TLS 1.2 or later (prefer TLS 1.3) with cipher suites that support perfect forward secrecy for all API and gateway connections — protects industrial data in transit from interception. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/infrastructure-security.html)
- **[Data protection]** Encrypt asset property values and aggregates at rest with a customer managed AWS KMS key instead of the default service-managed key — gives you control over key policies, rotation, and auditability. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/key-management.html)
- **[Data protection]** Never place sensitive information such as credentials or PII in asset, model, gateway, portal, project, or dashboard names and descriptions — these free-form fields can surface in logs and billing records. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security-best-practices.html)
- **[SiteWise Edge]** Require authentication credentials on OPC UA servers and select a non-deprecated, encrypted OPC UA message security mode for SiteWise Edge sources — secures industrial data as it moves from OPC UA servers to the gateway. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security-best-practices.html)
- **[SiteWise Edge]** Keep the SiteWise Edge gateway's system software, AWS IoT Greengrass software, and connector packs upgraded to their latest versions — maintaining the edge environment is a customer responsibility and stale software carries known vulnerabilities. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/vulnerability-analysis-and-management.html)
- **[SiteWise Edge]** Turn on disk or file-system encryption on the host running the SiteWise Edge gateway — the connector stores server-certificate private keys and access-control passwords on disk. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security-best-practices.html)
- **[SiteWise Edge]** Keep edge console and SiteWise Monitor application passwords private and enforce a password rotation policy — prevents unauthorized access to edge configuration. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/security-best-practices.html)
- **[Network]** Use interface VPC endpoints (AWS PrivateLink) for both control-plane and data-plane API operations — keeps traffic between your VPC and AWS IoT SiteWise off the public internet. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/vpc-interface-endpoints.html)

## 🛡️ Reliability
- **[Storage tiers]** Set a hot tier retention period longer than your typical low-latency access window before data transitions to warm or cold storage — keeps real-time dashboards, alarms, and monitoring responsive. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/manage-data-storage.html)
- **[Alarms]** Define alarms on asset properties to flag equipment or processes operating outside expected ranges — enables rapid detection and response before issues escalate. [doc](https://aws.amazon.com/blogs/industries/building-a-foundation-for-gxp-regulated-iot-workloads-on-aws/)
- **[Edge resiliency]** Use SiteWise Edge gateways to keep collecting and processing equipment data locally during network latency or outages — keeps production running when cloud connectivity is degraded. [doc](https://aws.amazon.com/blogs/iot/aws-iot-sitewise-2020-in-review/)
- **[Governance]** Enable an AWS CloudTrail trail for AWS IoT SiteWise API activity — supports traceability and forensic investigation of unexpected changes to assets and models. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/logging-using-cloudtrail.html)

## ⚡ Performance Efficiency
- **[Ingestion]** Match the ingestion path to the workload — direct OPC UA via a SiteWise Edge gateway, MQTT via AWS IoT Core rules, direct API calls, or Amazon S3 bulk operations — instead of forcing one method for every source. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/what-is-sitewise.html)
- **[Ingestion]** Use bulk import/export operations through Amazon S3 for creating, updating, or migrating large numbers of assets or asset models — avoids the overhead of many individual API calls. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/what-is-sitewise.html)
- **[Throttling]** Design ingestion and query workloads against published request-rate quotas (e.g., `BatchPutAssetPropertyValue`, `BatchGetAssetPropertyValue`, `BatchGetAssetPropertyAggregates`) and implement retry/backoff for `ThrottlingException` — prevents failed writes and reads under load. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/endpoints-and-quotas.html)
- **[Edge processing]** Apply data reduction such as filters and deadbands at the edge before transmitting to the cloud — cuts bandwidth use and downstream processing load. [doc](https://aws.amazon.com/blogs/iot/aws-iot-sitewise-2020-in-review/)

## 💰 Cost Optimization
- **[Storage tiers]** Reserve the hot tier for data that needs frequent, low-latency access and let retention settings move older data to the warm tier automatically — keeps hot-tier costs aligned to actual real-time access needs. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/manage-data-storage.html)
- **[Storage tiers]** Enable the cold tier (Amazon S3-backed) for rarely accessed historical data and set a warm tier retention period — moves infrequently used data to lower-cost storage instead of keeping it in warm tier indefinitely. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/manage-data-storage.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Track AWS IoT SiteWise health with Amazon CloudWatch metrics published to the `AWS/IoTSiteWise` namespace at one-minute resolution and set CloudWatch alarms on key thresholds — surfaces service issues before they affect operations. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-cloudwatch-metrics.html)
- **[Monitoring]** Send SiteWise Edge gateway and service logs to Amazon CloudWatch Logs with a resource policy scoped to specific resource ARNs where possible — centralizes troubleshooting data while limiting which resources can write logs. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-cloudwatch-logs.html)
- **[Auditability]** Create a CloudTrail trail spanning all Regions to retain an ongoing record of AWS IoT SiteWise API activity, including caller identity and source IP — supports operational review and compliance audits. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/logging-using-cloudtrail.html)
- **[Fleet management]** Use AWS IoT Device Defender to audit connected device fleets against security best practices and detect abnormal behavior — enforces consistent policy across large, distributed SiteWise Edge deployments. [doc](https://docs.aws.amazon.com/iot-sitewise/latest/userguide/vulnerability-analysis-and-management.html)

<!-- meta: last_reviewed=2026-07-05; sources=14 -->
