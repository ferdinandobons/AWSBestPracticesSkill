# AWS Mainframe Modernization — Best Practices

## Common scenarios
- Replatforming or refactoring COBOL/PL1 mainframe applications (CICS/VSAM/DB2/IMS) to run on AWS        → Reliability, Performance Efficiency
- Running batch jobs, schedulers, and file transfers for migrated mainframe workloads        → Operational Excellence, Cost Optimization
- Securing access to migrated applications, runtime environments, and their database credentials        → Security
- Operating modernized applications with high availability and disaster recovery targets        → Reliability

## 🔒 Security
- **[credentials]** Protect AWS account credentials and provision individual users through IAM Identity Center or IAM, granting each user only the permissions needed for their job duties, and require multi-factor authentication on every account. [doc](https://docs.aws.amazon.com/m2/latest/userguide/data-protection.html)
- **[database secrets]** Store application database credentials in AWS Secrets Manager rather than embedding them in configuration files, and scope the secret's resource policy to allow only the `m2.amazonaws.com` service principal to retrieve it. [doc](https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-other-resources.html)
- **[encryption in transit]** Require TLS 1.2 (and prefer TLS 1.3) with perfect-forward-secrecy cipher suites (DHE or ECDHE) for all client connections to AWS Mainframe Modernization APIs. [doc](https://docs.aws.amazon.com/m2/latest/userguide/infrastructure-security.html)
- **[encryption at rest]** Use a customer managed AWS KMS key for AWS Mainframe Modernization applications and runtime environments when you need control over key policies, rotation, and auditability beyond the default AWS-managed encryption applied to S3, DynamoDB, and EBS resources. [doc](https://docs.aws.amazon.com/m2/latest/userguide/data-protection.html)
- **[least privilege]** Author IAM identity-based policies that grant only the specific `m2:*` actions and resources each user or role needs, following IAM policy best practices, rather than relying on broad or wildcard permissions. [doc](https://docs.aws.amazon.com/m2/latest/userguide/security_iam_id-based-policy-examples.html)
- **[private connectivity]** Create an AWS PrivateLink interface endpoint (`com.amazonaws.{region}.m2`) so applications and administrators reach AWS Mainframe Modernization from your VPC without traversing the public internet, and attach a custom endpoint policy to restrict which principals and actions are allowed. [doc](https://docs.aws.amazon.com/m2/latest/userguide/vpc-interface-endpoints.html)
- **[sensitive data]** Never place confidential or sensitive information such as customer emails into tags or free-form name fields, since this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/m2/latest/userguide/data-protection.html)
- **[audit logging]** Enable AWS CloudTrail trails to capture API calls and user activity against AWS Mainframe Modernization resources for security analysis and compliance auditing. [doc](https://docs.aws.amazon.com/m2/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[multi-AZ design]** Design and operate migrated applications to take advantage of multiple Availability Zones within a Region so they can fail over automatically without interruption, rather than relying on a single-AZ deployment. [doc](https://docs.aws.amazon.com/m2/latest/userguide/disaster-recovery-resiliency.html)
- **[high availability config]** Configure a high-availability runtime environment with a desired instance capacity greater than one so the environment can tolerate instance failure without an outage. [doc](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_m2/CfnEnvironment.html)
- **[disaster recovery]** Architect a warm-standby environment in a separate AWS Region for high-priority mainframe workloads to lower recovery time objective (RTO), aligning the strategy to your required RTO per AWS Well-Architected guidance. [doc](https://aws.amazon.com/solutions/guidance/warm-standby-using-aws-mainframe-modernization-refactor-with-aws-blu-age/)
- **[alerting]** Use Amazon SNS and Amazon SES to deliver notifications and alerts for events that could affect the availability of modernized mainframe applications, so operators are informed promptly of issues. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)

## ⚡ Performance Efficiency
- **[compute sizing]** Choose the compute capacity option (instance type and count) that matches your transactional and batch-processing requirements rather than defaulting to a fixed size, and adjust as workload profiles change. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)
- **[continuous monitoring]** Define and continuously track performance metrics for runtime environments and applications in Amazon CloudWatch to identify and resolve bottlenecks before they affect users. [doc](https://docs.aws.amazon.com/m2/latest/userguide/monitoring-cloudwatch.html)

## 💰 Cost Optimization
- **[built-in utilities]** Use AWS Mainframe Modernization's built-in batch utilities (for example M2SFTP for secure file transfer, M2WAIT, and TXT2PDF) instead of licensing third-party equivalents, to avoid extra licensing costs. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)
- **[cost visibility]** Review AWS Cost Explorer regularly for AWS Mainframe Modernization usage and costs so resource sizing and utilization decisions are based on actual spend data. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)

## ⚙️ Operational Excellence
- **[CI/CD]** Implement an automated continuous integration and continuous delivery pipeline for COBOL or PL/I application changes rather than manual deployment steps, to make releases repeatable and auditable. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)
- **[infrastructure as code]** Manage AWS Mainframe Modernization environments and applications with AWS CloudFormation to get repeatable, standardized deployments instead of manual console configuration. [doc](https://aws.amazon.com/solutions/guidance/operating-mainframe-applications-in-the-cloud-with-aws-mainframe-modernization/)
- **[monitoring]** Monitor AWS Mainframe Modernization with Amazon CloudWatch metrics and CloudWatch Logs, and use CloudTrail for API activity, so operational issues and batch job failures (abends) are surfaced and can trigger alarms for swift remediation. [doc](https://docs.aws.amazon.com/m2/latest/userguide/monitoring-overview.html)
- **[log awareness]** Treat exported application logs in CloudWatch as potentially containing customer-sensitive business or security data, and apply appropriate access controls and retention policies to those log groups. [doc](https://docs.aws.amazon.com/m2/latest/userguide/data-protection.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
