# AWS CloudShell — Best Practices

## Common scenarios
- Ad-hoc AWS CLI administration from the browser without local credentials        → Security, Operational Excellence
- Quick scripting/automation against AWS resources during troubleshooting        → Reliability, Operational Excellence
- Accessing AWS resources inside a private VPC from a browser-based shell        → Security, Reliability
- Storing small scripts/config files for reuse across sessions        → Cost Optimization, Operational Excellence

## 🔒 Security
- **[access control]** Use IAM permissions and policies to control access to AWS CloudShell so users can perform only the actions (e.g., uploading/downloading files) required by their role — least privilege reduces blast radius of a compromised session. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security-best-practices.html)
- **[access control]** Start from the `AWSCloudShellFullAccess` managed policy and narrow it into a custom least-privilege policy for your use cases rather than granting full access broadly. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security_iam_id-based-policy-examples.html)
- **[network isolation]** Require CloudShell VPC environments and deny creation of public environments when you need to control network access, since public environment network access cannot otherwise be restricted. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/cloudshell-security-faqs.html)
- **[network isolation]** Enforce VPC-only environments with an explicit IAM deny statement on `cloudshell:CreateEnvironment` when `cloudshell:VpcIds` is null, so users cannot fall back to public (unrestricted network) environments. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/aws-cloudshell-vpc-permissions-1.html)
- **[data handling]** Never put sensitive data (e.g., customer emails, credentials) into IAM entity names, tags, or free-form fields used with CloudShell, since these may surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/data-protection.html)
- **[data handling]** Keep the Safe Paste feature enabled (it is on by default) to catch potential security risks in multiline text copied from external sources before it runs in your shell. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security-best-practices.html)
- **[data handling]** Don't include sensitive data in IAM entities such as users, roles, or session names used with CloudShell. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security-best-practices.html)
- **[shared responsibility]** Be familiar with the AWS Shared Responsibility Model before installing third-party applications into the CloudShell compute environment, since you are responsible for what you introduce into it. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security-best-practices.html)
- **[change management]** Prepare rollback mechanisms before editing shell scripts that customize the CloudShell environment, and store code changes in a version control system. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security-best-practices.html)
- **[governance]** Require MFA and use conditions (e.g., enforce SSL/TLS) in IAM policies governing CloudShell access, and validate policies with IAM Access Analyzer to catch overly permissive statements. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/security_iam_id-based-policy-examples.html)
- **[data protection]** Set up API and user activity logging with AWS CloudTrail for CloudShell, and use TLS 1.2 (or preferably TLS 1.3) for all client communication. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[data durability]** Treat CloudShell's $HOME persistent storage as convenience, not durable backup — periodically copy important files from CloudShell to Amazon S3 using AWS CLI calls to protect against data loss. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/disaster-recovery-resiliency.html)
- **[VPC environments]** Remember that CloudShell VPC environments have no persistent storage: the $HOME directory is deleted after 20–30 minutes of inactivity or when the environment is deleted/restarted, so save output externally before the session ends. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/cloudshell-security-faqs.html)
- **[workload fit]** Use CloudShell for interactive, short-lived tasks only — for long-running processes, launch a dedicated compute service (e.g., Amazon EC2) instead, since inactive sessions end after 20–30 minutes and sessions auto-terminate after about 12 hours regardless of activity. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/limits.html)
- **[data retention]** Re-launch CloudShell periodically in each AWS Region you rely on to reset the 120-day persistent-storage retention timer, or explicitly export data you need to keep long-term. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/limits.html)

## ⚙️ Operational Excellence
- **[IAM setup]** Grant CloudShell VPC permissions using the minimal EC2 describe/create permission set (`ec2:DescribeVpcs`, `ec2:DescribeSubnets`, `ec2:DescribeSecurityGroups`, `ec2:DescribeDhcpOptions`, `ec2:DescribeNetworkInterfaces`, `ec2:CreateTags`, `ec2:CreateNetworkInterface`, `ec2:CreateNetworkInterfacePermission`) and also include `ec2:DeleteNetworkInterface` so CloudShell can clean up the ENIs it creates. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/sec-auth-with-identities.html)
- **[monitoring]** Enable an AWS CloudTrail trail for continuous delivery of CloudShell API events to Amazon S3 so you can audit who ran what commands, from which IP, and when. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/logging-and-monitoring.html)
- **[automation]** Use EventBridge event patterns matching `source: aws.cloudshell` / `eventSource: cloudshell.amazonaws.com` to build automated monitoring or alerting on CloudShell API activity. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-cloudshell.html)
- **[persistence hygiene]** Store only frequently used scripts and configuration files in the $HOME directory, understanding that changes outside $HOME are not preserved between sessions. [doc](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
