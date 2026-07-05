# AWS CodeCommit — Best Practices

## Common scenarios
- Hosting private Git repositories for source code and binaries with tight IAM-based access control        → Security, Operational Excellence
- Enforcing code-review gates (pull requests, approval rules) before merging to protected branches        → Operational Excellence, Reliability
- Triggering CI/CD pipelines and Lambda automation from repository push/branch events        → Operational Excellence, Reliability
- Granting cross-account or federated access to shared repositories        → Security

## 🔒 Security
- **[IAM]** Start from AWS managed policies and move to least-privilege customer-managed policies scoped to specific repositories, actions, and conditions rather than granting broad `codecommit:*` access. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/security-iam.html)
- **[IAM]** Use IAM Access Analyzer to validate identity-based policies against IAM best practices and catch overly permissive grants before attaching them. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/security-iam.html)
- **[IAM]** Require multi-factor authentication (MFA) for IAM principals accessing sensitive repositories, and enforce it with an `aws:MultiFactorAuthPresent` condition in policies to prevent accidental or unauthorized pushes. [doc](https://aws.amazon.com/blogs/devops/secure-aws-codecommit-with-multi-factor-authentication/)
- **[IAM]** Prefer temporary credentials from IAM roles or federated identities over long-lived IAM user access keys for both console and Git-client access. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/security-iam.html)
- **[Cross-account access]** For sharing repositories across accounts, grant access through IAM roles with scoped trust policies and resource-restricted permissions rather than distributing credentials, and use resource ARN conditions to limit which repositories a role can reach in multi-tenant setups. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/cross-account.html)
- **[Network]** Restrict CodeCommit API and Git access to specific source IP ranges or specific VPCs/VPC endpoints using policy conditions, isolating repository access to trusted networks. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/infrastructure-security.html)
- **[Transport]** Require clients to use TLS 1.2 or later with cipher suites that support perfect forward secrecy (e.g. DHE or ECDHE) for all API and Git connections. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/infrastructure-security.html)
- **[Encryption]** Use a customer-managed AWS KMS key instead of the default AWS-managed `aws/codecommit` key when you need to control key rotation, access policy, or auditing of the key used to encrypt repository data at rest. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/encryption.html)
- **[Auditing]** Enable AWS CloudTrail across all regions to capture CodeCommit API calls (including `GitPull`/`GitPush`) for a durable, searchable audit trail of who accessed or changed which repository. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/integ-cloudtrail.html)

## 🛡️ Reliability
- **[Code review]** Apply approval rule templates across repositories so pull requests to protected branches (e.g. `main`) require a defined minimum number of approvals before merge, preventing unreviewed changes from reaching production branches. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/approval-rule-templates.html)
- **[Branch protection]** Use branch filters in approval rule templates to apply stricter approval requirements to production branches while allowing lighter-weight rules for development branches. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/approval-rule-templates.html)
- **[Backup/DR]** Maintain an independent backup strategy (scheduled `git clone`/`git pull` mirroring to another store, or cross-region replication via Lambda/EventBridge) since CodeCommit does not provide a built-in backup or point-in-time-restore feature. [doc](https://aws.amazon.com/codecommit/faqs/)
- **[Backup/DR]** For disaster recovery or multi-region CI/CD, replicate repository contents to a target repository in another region using event-driven automation (e.g. Lambda triggered by repository state-change events) rather than relying on manual syncs. [doc](https://aws.amazon.com/blogs/devops/build-serverless-aws-codecommit-workflows-using-amazon-cloudwatch-events-and-jgit/)
- **[Durability]** Rely on CodeCommit's underlying storage on Amazon S3 and Amazon DynamoDB, which redundantly stores encrypted repository data across multiple facilities, for high availability and durability of committed data. [doc](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/aws-codecommit.html)

## ⚙️ Operational Excellence
- **[Automation]** Use repository triggers (to Amazon SNS or AWS Lambda) or EventBridge notification rules to automate downstream actions—CI builds, deployment pipelines, chat notifications—in response to push, branch, tag, comment, and pull-request events instead of polling for changes. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-notify-sns.html)
- **[Automation]** Prefer notification rules (integrated with EventBridge, and able to target Chatbot/Slack/Chime) over legacy pre-November-2019 console notifications, and migrate any remaining legacy notifications since they cannot be recreated once deleted. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-repository-email.html)
- **[Monitoring]** Monitor repository activity and health using the full observability stack together: EventBridge/CloudWatch Events for near-real-time state-change events, CloudWatch Logs for log-based alerting, and CloudTrail for API-level history. [doc](https://docs.aws.amazon.com/codecommit/latest/userguide/monitoring-overview.html)
- **[Code review]** Standardize pull-request workflows (feature branch → pull request → review/comment → merge) and integrate automated review tooling such as Amazon CodeGuru Reviewer alongside human approval rules to catch defects before merge. [doc](https://aws.amazon.com/blogs/devops/automate-code-reviews-with-amazon-codeguru-reviewer/)
- **[Governance]** Apply consistent naming/prefixing conventions to repositories (e.g. by team or project) and scope IAM roles to those prefixes so access patterns and audits remain manageable as the number of repositories grows. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/give-sagemaker-notebook-instances-temporary-access-to-a-codecommit-repository-in-another-aws-account.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
