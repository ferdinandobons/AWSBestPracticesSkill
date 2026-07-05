# AWS Transfer Family — Best Practices

## Common scenarios
- Lift-and-shift of existing SFTP/FTPS/FTP file exchange workflows into AWS    → Security, Reliability
- B2B file exchange with partners requiring post-upload processing (validation, routing, notifications)    → Operational Excellence, Security
- Multi-tenant or SaaS-style managed file transfer platforms serving many external users    → Performance Efficiency, Cost Optimization
- Bridging on-premises or remote SFTP servers into S3/EFS via connectors    → Reliability, Performance Efficiency

## 🔒 Security
- **[data in transit]** Use the latest server security policy (e.g. `TransferSecurityPolicy-2025-03` or FIPS equivalent) with post-quantum hybrid key exchange rather than the account default — the default can lag behind the strongest available ciphers. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/security-policies.html)
- **[host identity]** Provision Transfer Family SFTP servers with at least a 4,096-bit RSA, ED25519, or ECDSA host key, and deprecate weaker legacy host keys once rotated — a weak host key lets an attacker impersonate your server. [doc](https://aws.amazon.com/blogs/security/how-transfer-family-can-help-you-build-a-secure-compliant-managed-file-transfer-solution/)
- **[SFTP connectors]** Apply the current SFTP connector security policy — it limits the MACs, key exchanges, and cipher suites used when connecting to remote servers. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/security-policies-connectors.html)
- **[network access]** Use the `VPC` endpoint type instead of the discontinued `VPC_ENDPOINT` type — it lets you attach security groups and Elastic IPs directly, preserves client source IP for logging, and removes the need for a Network Load Balancer. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/create-server-in-vpc.html)
- **[IAM]** Start from AWS managed policies and narrow to customer-managed, least-privilege policies scoped to specific resources — broad default policies grant more access than most user/workflow roles need. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Assign each service-managed user its own IAM role and policy rather than a broad shared role — this ensures users can only access the folders/buckets they are entitled to. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/users-policies.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer and add conditions such as requiring SSL — this catches overly permissive or non-functional policies before they reach production. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/security_iam_id-based-policy-examples.html)
- **[encryption]** Require SSL/TLS 1.2+ for all client communication and grant the extra IAM permissions needed when the destination S3 bucket uses a customer-managed AWS KMS key — otherwise transfers to KMS-encrypted buckets fail or leave data unprotected. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/encryption-at-rest.html)
- **[data handling]** Never place sensitive identifying information such as account numbers or credentials in free-form configuration fields like server or user names — this data can be captured in diagnostic logs. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/encryption-at-rest.html)
- **[perimeter]** Front custom-identity-provider Transfer Family deployments (API Gateway) with AWS WAF and an IP set — this blocks or allows traffic based on the true client source IP rather than the service's own IP. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/web-application-firewall.html)
- **[auditability]** Enable AWS CloudTrail for all Transfer Family API activity — actions like CreateServer, ListUsers, and StopServer are logged for security and compliance review. [doc](https://aws.amazon.com/blogs/storage/customize-file-delivery-notifications-using-aws-transfer-family-managed-workflows/)

## 🛡️ Reliability
- **[availability]** Deploy Transfer Family servers across multiple Availability Zones (up to 3) rather than a single subnet — this reduces the risk of service disruption during an AZ-level outage. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/disaster-recovery-resiliency.html)
- **[scaling]** Plan for the per-server concurrent session ceiling and distribute high-volume or multi-tenant workloads across multiple servers — a single server's capacity can otherwise become a shared point of saturation. [doc](https://aws.amazon.com/blogs/apn/designing-a-multi-tenant-sftp-server-with-aws-transfer-family/)
- **[SFTP connectors]** Distribute file volume across multiple connectors or use concurrent sessions rather than a single connector queue — each connector has a maximum pending-request queue depth and a request-rate limit that can trigger throttling. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/scale-and-limits-sftp-connector.html)
- **[workflow resilience]** Configure managed workflows' built-in exception handling for every workflow — this defines explicit behavior for failed or partially-uploaded file processing instead of leaving failures unhandled. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/transfer-workflows.html)

## ⚡ Performance Efficiency
- **[SFTP connectors]** Raise `MaxConcurrentConnections` (up to 5) on an SFTP connector when the remote server supports concurrent sessions — this enables parallel transfer operations for large file batches. [doc](https://docs.aws.amazon.com/transfer/latest/APIReference/API_SftpConnectorConfig.html)
- **[latency]** Use latency-based routing across multiple Regional endpoints for geographically distributed end users — this minimizes network latency at the cost of added multi-Region operational overhead. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/disaster-recovery-resiliency.html)
- **[multi-tenant capacity]** Monitor per-tenant usage and introduce throttling or load balancing across additional servers proactively — this avoids hitting shared-server concurrent session limits. [doc](https://aws.amazon.com/blogs/apn/designing-a-multi-tenant-sftp-server-with-aws-transfer-family/)

## 💰 Cost Optimization
- **[endpoint hygiene]** Delete unused server endpoints rather than leaving them stopped — hourly protocol charges continue to accrue as long as a server exists, even while stopped. [doc](https://aws.amazon.com/aws-transfer-family/faqs/)
- **[architecture]** Use a shared/pooled multi-tenant server model instead of one server per tenant where isolation requirements allow it — this reduces per-protocol hourly costs and operational overhead. [doc](https://aws.amazon.com/blogs/apn/designing-a-multi-tenant-sftp-server-with-aws-transfer-family/)
- **[VPC networking]** Reuse shared VPC resources such as NAT gateways and VPC interface endpoints across accounts in an AWS Organization for VPC-based endpoints — this cuts duplicate networking costs. [doc](https://aws.amazon.com/blogs/storage/using-vpc-hosted-endpoints-in-shared-vpcs-with-aws-transfer-family/)
- **[storage tiering]** Apply S3 storage tiering or lifecycle policies to transferred files — this moves infrequently accessed data to lower-cost storage classes automatically. [doc](https://aws.amazon.com/solutions/guidance/detecting-malware-threats-using-aws-transfer-family/)

## ⚙️ Operational Excellence
- **[observability]** Enable structured JSON logging to Amazon CloudWatch for all servers, connectors, and workflows across every protocol — this lets you query user and transfer activity with CloudWatch Logs Insights. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/structured-logging.html)
- **[observability]** Consolidate log streams from multiple Transfer Family servers into a single CloudWatch log group — this enables unified dashboards and cross-server usage metrics. [doc](https://aws.amazon.com/aws-transfer-family/faqs/)
- **[automation]** Use managed workflows or EventBridge file-transfer event notifications to automate post-upload processing — copying, tagging, decryption, custom Lambda steps, and delivery notifications all run without bespoke polling logic. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/transfer-workflows.html)
- **[IaC]** Deploy workflows and server configuration through infrastructure as code — this standardizes and replicates common file-processing patterns consistently across business units. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/transfer-workflows.html)
- **[least privilege for logging]** Use the AWS managed `AWSTransferLoggingAccess` policy for the server's logging role instead of a broader custom policy — it scopes access to only the CloudWatch log actions Transfer Family needs. [doc](https://aws.amazon.com/blogs/storage/implementing-least-privilege-access-in-an-aws-transfer-family-workflow/)
- **[change management]** Wait for the cache refresh and have users reconnect after swapping a workflow association or server config — cached workflow details otherwise mask the change and can be mistaken for a bug. [doc](https://docs.aws.amazon.com/transfer/latest/userguide/create-workflow.html)

<!-- meta: last_reviewed=2026-07-05; sources=20 -->
