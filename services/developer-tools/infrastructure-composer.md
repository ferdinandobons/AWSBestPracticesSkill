# AWS Infrastructure Composer — Best Practices

## Common scenarios
- Visually composing a serverless application architecture from AWS resources        → Operational Excellence, Security
- Generating deployment-ready CloudFormation/SAM templates from a canvas design        → Security, Operational Excellence
- Syncing a canvas design with a local IDE and version control for team development        → Operational Excellence, Reliability
- Connecting a Lambda function to resources inside an existing VPC        → Security, Reliability

## 🔒 Security
- **[Defaults]** Keep the default enhanced-component settings that Infrastructure Composer configures automatically (e.g., S3 `BucketEncryption` and `PublicAccessBlockConfiguration`) rather than removing them — they enable KMS encryption and block public access out of the box. [doc](https://aws.amazon.com/infrastructure-composer/faqs/)
- **[IAM]** Grant users only the minimum read-only console access Infrastructure Composer requires and rely on AWS CloudFormation's own IAM controls to govern deployment of the generated template — Infrastructure Composer itself does not support granular, resource-level, or action-level permissions. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/security_iam_service-with-iam.html)
- **[Authentication]** Use IAM Identity Center or IAM with individual users rather than shared or root credentials, and require multi-factor authentication — this limits blast radius if a single credential is compromised. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/data-protection.html)
- **[Data handling]** Never put confidential or sensitive information (customer emails, credentials, tokens) into resource names, tags, or other free-form text fields on the canvas — this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/data-protection.html)
- **[Auditing]** Enable AWS CloudTrail to log API and user activity — this lets you trace changes made through Infrastructure Composer and subsequent CloudFormation deployments. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/data-protection.html)
- **[Transport security]** Require TLS 1.2 or later (TLS 1.3 recommended) for any tooling or CLI that interacts with Infrastructure Composer projects — this keeps API traffic protected in transit. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/data-protection.html)
- **[VPC]** Reference the correct security group and subnet IDs deliberately (static values or imported parameters) when configuring a Lambda function with an external VPC — misconfigured VPC settings can unintentionally expose or isolate the function. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/using-composer-services-vpc-configure.html)
- **[Review before deploy]** Treat the generated template as a starting point, not a final artifact, and adjust resource configuration (passwords, naming, permissions) before provisioning — this ensures it matches your organization's security and deployment standards. [doc](https://aws.amazon.com/blogs/compute/visually-design-your-application-with-aws-application-composer/)

## 🛡️ Reliability
- **[Multi-AZ by default]** Design resources you compose to rely on the underlying AWS Region/Availability Zone architecture — AWS Regions provide multiple isolated, low-latency-connected Availability Zones that support automatic failover. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/disaster-recovery-resiliency.html)
- **[Local state]** Back up and recover canvas/template history through your own version control system — Infrastructure Composer does not persist project data on the service side, only generating project files saved locally to your machine. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/disaster-recovery-resiliency.html)
- **[Local sync]** Activate local sync mode so canvas changes are continuously written to your local project folder — this reduces the risk of losing in-progress design work if the browser session ends. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/other-services-ide.html)

## ⚙️ Operational Excellence
- **[Version control]** Connect Infrastructure Composer to a project folder tracked in your version control system via local sync mode — this captures every canvas-driven change to the generated template in history. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/other-services-ide.html)
- **[Change review]** Use the Change Inspector (or Template View in the console) to review the exact lines added or removed in your CloudFormation/SAM template before accepting a canvas-driven change — this keeps configuration changes deliberate and traceable. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/using-change-inspector.html)
- **[CI/CD integration]** Export or sync the generated CloudFormation/SAM template into your existing CI/CD pipeline rather than treating the console as the deployment mechanism — this routes deployments through the same review and testing gates as other infrastructure changes. [doc](https://aws.amazon.com/infrastructure-composer/faqs/)
- **[Local development]** Pair local sync with the AWS SAM CLI (or the AWS Toolkit for VS Code) to build, test, and deploy Infrastructure Composer projects locally — this avoids relying solely on console-only workflows. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/other-services-cfn-sam-using.html)
- **[Consistent tooling]** Standardize on either the Infrastructure Composer console or the AWS Toolkit for VS Code integration per team/project — this keeps template structure and local-sync directory conventions consistent across contributors. [doc](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/what-is-composer.html)

<!-- meta: last_reviewed=2026-07-05; sources=10 -->
