# AWS AppFabric — Best Practices

## Common scenarios
- Normalizing and centralizing SaaS audit logs for SIEM/SOC ingestion        → Security, Operational Excellence
- Cross-application security observability and threat detection        → Security, Reliability
- User access visibility and deprovisioning verification across SaaS apps        → Security, Operational Excellence
- Feeding normalized OCSF data into Amazon Security Lake or a data lake        → Security, Cost Optimization

## 🔒 Security
- **[Identity]** Set up individual users with IAM Identity Center or IAM instead of sharing AWS account credentials, granting each administrator only the permissions needed for their job. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Identity]** Start from AWS managed policies and move toward customer managed, least-privilege policies scoped to specific AppFabric actions and resources. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/security_iam_id-based-policy-examples.html)
- **[Identity]** Add IAM policy conditions (for example requiring SSL/TLS on requests) to further restrict when AppFabric actions are allowed. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/security_iam_id-based-policy-examples.html)
- **[Identity]** Validate IAM policies with IAM Access Analyzer to catch overly permissive or non-functional statements before granting access. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/security_iam_id-based-policy-examples.html)
- **[Identity]** Require multi-factor authentication (MFA) on accounts that can manage AppFabric app authorizations and ingestions. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Data protection]** Choose a customer managed AWS KMS key (instead of the AWS owned key) when creating the app bundle if you need control over key policy, rotation, and auditability of encryption for authorization credentials and ingested data. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/prerequisites.html)
- **[Data protection]** Require TLS 1.2 or later (prefer TLS 1.3) for all client and API connections to AppFabric. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Data protection]** Never place confidential or sensitive information, such as customer email addresses, in tags or free-form text fields (including app bundle or ingestion names), since these may surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Data protection]** Avoid embedding credentials in any URL you provide to AppFabric to validate requests to an external server. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Data protection]** Pair AppFabric with Amazon Macie when audit log destinations land in S3, to discover and secure sensitive data at rest. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Access governance]** Give only read-only IAM permissions to integrators (SIEM/BI tools such as Amazon QuickSight or Splunk) that consume AppFabric-delivered data, rather than granting them AppFabric admin access. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/security-best-practices.html)
- **[Access governance]** Use AppFabric's user access feature to search by corporate email and verify application access or deprovisioning status across all connected SaaS applications, especially during employee offboarding. [doc](https://aws.amazon.com/appfabric/features/)
- **[Monitoring]** Set up AWS CloudTrail to capture API and user activity logs for AppFabric for security analysis and change tracking. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/data-protection.html)
- **[Monitoring]** Enable Amazon CloudWatch metrics for AppFabric (App Authorization Status, Ingestion Destination Status, Data Delivery Latency, Overall Data Delay, Volume of Ingested Data) and configure alarms to detect authorization failures or ingestion disruptions. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/monitoring-cloudwatch.html)
- **[Compliance]** Use AWS Artifact to download third-party audit reports and confirm AppFabric is in scope for the compliance programs your organization requires. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/compliance-validation.html)
- **[Infrastructure]** Ensure any client accessing AppFabric APIs supports TLS 1.2+ and cipher suites with perfect forward secrecy (DHE or ECDHE). [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/infrastructure-security.html)
- **[Infrastructure]** Sign all requests with credentials tied to an IAM principal, or use AWS STS temporary credentials, rather than long-lived static credentials. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/infrastructure-security.html)

## 🛡️ Reliability
- **[Ingestion]** Route each app authorization's audit log ingestion to durable destinations (Amazon S3 or Amazon Data Firehose) and monitor the Ingestion Destination Status metric so delivery failures are caught quickly. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/monitoring-cloudwatch.html)
- **[Ingestion]** For multi-application rollouts, use Ingestions quick setup to configure ingestions consistently to a shared destination (for example one S3 bucket or Firehose stream), reducing configuration drift across app authorizations. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/getting-started-security.html)
- **[Downstream integration]** Send normalized OCSF data through Amazon Data Firehose into Amazon Security Lake to build a durable, queryable, centralized audit trail across your SaaS portfolio. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/security-lake.html)

## ⚙️ Operational Excellence
- **[Normalization]** Use the OCSF normalization option (rather than raw JSON) when downstream tooling supports it, to get consistent field mapping across heterogeneous SaaS applications and reduce custom parsing work. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/ocsf-schema.html)
- **[Enrichment]** Rely on AppFabric's automatic enrichment of audit events with user email addresses (matched from UID) to speed up security incident response and cross-application correlation. [doc](https://aws.amazon.com/appfabric/features/)
- **[Monitoring]** Build CloudWatch dashboards and alarms on AppFabric metrics as part of routine operations, since CloudWatch retains AppFabric statistics for 15 months for trend analysis. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/monitoring-cloudwatch.html)
- **[Access management]** Configure permissions for creating, editing, or deleting the `AWSServiceRoleForAppFabric` service-linked role explicitly, since AppFabric depends on it to deliver metrics and ingested data to your destinations. [doc](https://docs.aws.amazon.com/appfabric/latest/adminguide/using-service-linked-roles.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
