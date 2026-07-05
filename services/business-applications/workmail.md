# Amazon WorkMail — Best Practices

## Common scenarios
- Managed corporate email and calendar for an organization        → Security, Reliability, Operational Excellence
- Regulatory-driven email archiving and eDiscovery        → Security, Operational Excellence
- Mailbox access via Outlook, mobile (EAS), and web client with centralized device policy        → Security
- Planning migration off Amazon WorkMail ahead of end of support        → Operational Excellence

## 🔒 Security
- **[Identity]** Set up individual users with IAM Identity Center or IAM instead of sharing AWS account credentials, and grant only the permissions each administrator needs. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/data-protection.html)
- **[Identity]** Integrate Amazon WorkMail with AWS IAM Identity Center to enable multi-factor authentication (MFA) for mailbox sign-in and centralize user access management. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/improving-security-in-amazon-workmail-with-mfa/)
- **[Transport security]** Require TLS 1.2 (and prefer TLS 1.3) for all client and API connections, since WorkMail has discontinued support for TLS 1.0/1.1. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/infrastructure-security.html)
- **[Transport security]** Use cipher suites with perfect forward secrecy (PFS), such as DHE or ECDHE, for client connections. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/infrastructure-security.html)
- **[Data protection]** Rely on WorkMail's mandatory AWS KMS-backed encryption at rest for mailbox data, and choose the AWS Region that meets your data-locality requirements. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/data-protection.html)
- **[Data protection]** Enable signed or encrypted email for users who need end-to-end message protection beyond WorkMail's default at-rest encryption. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/data-protection.html)
- **[Data protection]** Never place confidential or sensitive information (such as customer email addresses) into tags or free-form text fields when managing WorkMail via console, API, CLI, or SDKs. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/data-protection.html)
- **[Device security]** Configure the organization's mobile device policy to require device/storage-card encryption, enforce password strength and expiration, enable screen-lock timeouts, and wipe devices after repeated failed unlock attempts. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/edit_mobile_policy.html)
- **[Device security]** Use a third-party mobile device management (MDM) solution when you need stronger device posture enforcement than the built-in Exchange ActiveSync mobile device policies provide. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/mdm-integration.html)
- **[Monitoring]** Enable WorkMail audit logging (access control, authentication, availability provider, and mailbox access logs) and deliver logs to CloudWatch Logs, S3, or Data Firehose to detect unauthorized mailbox access. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/an-introduction-to-amazon-workmail-audit-logging/)
- **[Monitoring]** Enable AWS CloudTrail to log WorkMail console and API activity (for example CreateUser, CreateAlias, GetRawMessageContent) for security analysis and change tracking. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/logging-using-cloudtrail.html)
- **[Monitoring]** Periodically review WorkMail audit logs and CloudTrail history for unusual mailbox access or authentication patterns, following the lessons of major cloud-email intrusions. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/how-to-create-a-big-yellow-taxi-to-help-protect-amazon-workmail/)
- **[Governance]** Use Security and Compliance Quick Start guides, AWS Config, and AWS Security Hub CSPM to continuously validate the WorkMail environment against your compliance objectives. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/compliance.html)
- **[User awareness]** Remind end users to never share usernames or passwords and to avoid leaving sensitive information accessible on shared or public computers. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/how-to-create-a-big-yellow-taxi-to-help-protect-amazon-workmail/)

## 🛡️ Reliability
- **[Availability]** Design around the AWS Regions/Availability Zones model that underlies WorkMail so mailbox access is resilient to zonal failures. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/disaster-recovery-resiliency.html)
- **[Compliance archiving]** Enable email journaling and route journaled messages to a durable third-party or SES Mail Manager archive to meet data-retention and eDiscovery requirements even if mailbox data is later lost or altered. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/journaling_overview.html)
- **[Compliance archiving]** Set explicit retention periods and, where required, use your own KMS key when archiving journaled mail in SES Mail Manager. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/email-journaling-with-ses-mail-manager/)
- **[Interoperability]** Use a Custom Availability Provider (Lambda-backed) instead of exposing an on-premises Exchange EWS endpoint to the public internet when sharing free/busy data across organizations. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/enable_interop_wm.html)

## ⚙️ Operational Excellence
- **[Lifecycle planning]** Plan migration off Amazon WorkMail well ahead of the March 31, 2027 end-of-support date, since the service stopped accepting new customers on April 30, 2026 and console/API access ends after the cutoff. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/workmail-end-of-support.html)
- **[Access reviews]** Apply IAM policy best practices — least privilege, managed policies over broad inline policies — when authorizing administrators to manage WorkMail organizations, users, and resources. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/security_iam_id-based-policy-examples.html)
- **[Identity sync]** Keep IAM Identity Center usernames and email addresses aligned with WorkMail user accounts to simplify synchronization and reduce authentication errors. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/improving-security-in-amazon-workmail-with-mfa/)
- **[Migration]** Work with an AWS migration partner and follow the staged create-users, migrate-mailboxes, complete-migration process when moving from Exchange, Microsoft 365, or Google Workspace. [doc](https://docs.aws.amazon.com/workmail/latest/adminguide/migration_overview.html)

<!-- meta: last_reviewed=2026-07-05; sources=16 -->
