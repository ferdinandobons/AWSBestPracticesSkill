# AWS Wickr — Best Practices

## Common scenarios
- End-to-end encrypted messaging, calling, and file sharing for regulated or sensitive teams        → Security
- Retaining internal and external conversations to meet FRA/NARA or other compliance obligations        → Security, Operational Excellence
- Federating securely with external partners, contractors, and guest users        → Security
- Auditing administrative and API activity across a Wickr network        → Security, Operational Excellence

## 🔒 Security
- **[IAM]** Implement least-privilege access and create specific IAM roles/templates dedicated to Wickr administrative actions rather than reusing broad roles. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/security-best-practices.html)
- **[Console access]** Require users to authenticate to the AWS Management Console first before accessing the Wickr console, and never share personal console credentials. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/security-best-practices.html)
- **[Authentication]** Protect AWS account credentials and provision individual users through AWS IAM Identity Center or IAM so each user has only the permissions needed for their role. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/data-protection.html)
- **[Authentication]** Enable multi-factor authentication (MFA) on every account used to administer Wickr. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/data-protection.html)
- **[SSO]** Configure single sign-on using an OIDC-based identity provider (Microsoft Entra/Azure AD, Okta, or Amazon Cognito) paired with MFA for an added layer of authentication security. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/sso-configuration.html)
- **[SSO]** Record the company ID generated during SSO configuration and migrate to the new, more secure SSO redirect URI before the March 9, 2026 deadline. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/configure-sso.html)
- **[Security groups]** Organize users into security groups and apply tailored policies for password complexity, messaging, calling, and federation settings per group rather than a single network-wide policy. [doc](https://aws.amazon.com/wickr/features/)
- **[Federation]** Use restricted federation modes (permitted networks list) instead of unrestricted global federation when communication should be limited to specific external networks. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-wickr-2024-02-01.html)
- **[Device management]** Reset passwords and remotely delete user profiles promptly for lost or stolen devices to reduce the risk of data exposure. [doc](https://aws.amazon.com/blogs/security/aws-wickr-achieves-fedramp-moderate-authorization/)
- **[Networking]** Use AWS PrivateLink interface VPC endpoints (wickr-admin, wickr-messaging, wickr-calling) to keep traffic between your VPC and Wickr off the public internet, and pair with VPN for mobile or on-premises clients. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/privatelink-overview.html)
- **[Networking]** Enable Private DNS Names on Wickr VPC endpoints, since all Wickr PrivateLink endpoints currently require it. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/privatelink-overview.html)
- **[Data protection]** Use TLS 1.2 at minimum (TLS 1.3 recommended) for all communication with AWS resources related to Wickr. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/data-protection.html)
- **[Data protection]** Never place confidential or sensitive information (such as customer email addresses) into tags or free-form text/name fields, since this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/data-protection.html)
- **[Compliance]** Use a FIPS endpoint when FIPS 140-3 validated cryptographic modules are required for CLI or API access to Wickr. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/data-protection.html)
- **[Data retention]** Configure and activate data retention for the network so all messages and files are captured to an external store (local storage or Amazon S3) per your organization's compliance policy, since Wickr itself never accesses message content. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide-classic/data-retention.html)
- **[Data retention]** Secure the data retention bot deployment using AWS Secrets Manager for credentials and AWS KMS for encryption, and scope its IAM policy to only the resources it needs. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide-classic/configure-data-retention.html)

## 🛡️ Reliability
- **[Data resiliency]** Rely on the multi-Availability-Zone AWS global infrastructure underlying Wickr for fault tolerance, and pair it with Wickr data retention modules for backup and recovery of conversation data. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide/disaster-recovery-resiliency.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Enable AWS CloudTrail logging for Wickr to capture API calls and console actions, including caller identity, source IP, and timestamp, for operational visibility and audit. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide-classic/logging-using-cloudtrail.html)
- **[Monitoring]** Deliver CloudTrail events for Wickr to an Amazon S3 bucket via a trail for durable, continuous logging rather than relying solely on the 90-day CloudTrail Event History. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide-classic/monitoring-overview.html)
- **[Data retention]** Monitor data retention metrics and events for the Wickr network to confirm the retention bot is running and capturing all required conversations. [doc](https://docs.aws.amazon.com/wickr/latest/adminguide-classic/data-retention.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
