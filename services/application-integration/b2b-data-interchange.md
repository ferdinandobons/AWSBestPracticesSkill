# AWS B2B Data Interchange — Best Practices

## Common scenarios
- Transforming inbound X12 EDI documents from trading partners into JSON/XML for downstream apps and data lakes        → Reliability, Operational Excellence
- Generating outbound X12 EDI (e.g. 810 Invoice, 835 Claim Payment) from JSON/XML exported by ERP or claims systems        → Reliability, Performance Efficiency
- HIPAA-eligible healthcare EDI workflows carrying PII/PHI (837 claims, 835 remittances) between payers and providers        → Security
- Event-driven EDI pipelines that trigger ETL, notifications, or acknowledgements on transformation success/failure        → Operational Excellence, Reliability

## 🔒 Security
- **[IAM]** Set up individual IAM Identity Center or IAM users/roles with least-privilege permissions for B2B Data Interchange instead of sharing root or broad account credentials. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)
- **[IAM]** Require multi-factor authentication (MFA) on accounts and roles that can manage profiles, transformers, and partnerships. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)
- **[Networking]** Enforce TLS 1.2 at minimum (TLS 1.3 recommended) for all communication with AWS B2B Data Interchange and related resources. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)
- **[Networking]** Use an AWS PrivateLink interface VPC endpoint to call B2B Data Interchange APIs privately, and attach a security group to the endpoint network interfaces to control which traffic can reach it, since VPC endpoint policies are not supported for this service. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/vpc-interface-endpoints.html)
- **[Data protection]** Encrypt input/output Amazon S3 buckets used for EDI documents and data files, and configure the corresponding AWS KMS key policy when using SSE-KMS so B2B Data Interchange can decrypt inputs and encrypt outputs during transformation. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/b2bi-prereq.html)
- **[Data protection]** Configure S3 bucket policies for both input and output buckets (copy the policy generated when creating a trading capability) rather than hand-writing broad permissions, then validate with the console's input/output setup checks. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/b2bi-prereq.html)
- **[Data protection]** Never place confidential or sensitive information (e.g. trading-partner contact details) into tags or free-form text fields such as name fields, since this data can surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)
- **[Data protection]** Do not embed credentials in externally supplied URLs used to validate requests to trading-partner or third-party servers. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)
- **[Confused deputy]** Add `aws:SourceArn` and `aws:SourceAccount` condition keys to S3 bucket and KMS key resource policies that grant B2B Data Interchange access, to prevent cross-service confused-deputy scenarios. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/cross-service-confused-deputy-prevention.html)
- **[Malware protection]** Use Amazon GuardDuty malware scanning on inbound EDI documents as they land in Amazon S3 to catch malicious payloads before downstream processing. [doc](https://aws.amazon.com/b2b-data-interchange/faqs/)
- **[Compliance]** For healthcare workloads carrying PHI/PII (e.g. 837/835 transactions), rely on B2B Data Interchange's HIPAA eligibility and pair it with encryption at rest/in transit and secured S3 bucket access policies to maintain compliance. [doc](https://aws.amazon.com/b2b-data-interchange/faqs/)
- **[Auditing]** Enable AWS CloudTrail to capture API calls and user activity against B2B Data Interchange resources for security review and forensics. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[Availability]** Rely on B2B Data Interchange's built-in Availability Zone redundancy (up to 3 AZs with redundant fleets per AZ) rather than building custom multi-AZ failover logic. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/disaster-recovery-resiliency.html)
- **[Large files]** Enable EDI splitting on transformers that may receive multi-transaction inbound files, which raises the supported file size from 150 MB to 5 GB and lets each transaction be validated and processed independently. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/edi-split-overview.html)
- **[Acknowledgements]** Use B2B Data Interchange's automatic X12 functional acknowledgements (TA1, 997, 999) and route them back to trading partners via EventBridge-triggered delivery so partners get timely confirmation or rejection of their transactions. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/transform-outbound-variations.html)
- **[Event-driven processing]** Subscribe to per-transaction "Split Transformation Completed" and "Split Transformation Failed" EventBridge events so failures in one transaction of a batched file don't block or hide successful processing of the others. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/edi-split-overview.html)
- **[Quotas]** Track account quotas (profiles, trading capabilities, transformers, partnerships) and request increases proactively before scaling trading-partner onboarding, since several quotas are adjustable but file-size limits are not. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/b2bi-quotas.html)

## ⚡ Performance Efficiency
- **[Large files]** Configure `X12SplitOptions` on transformers handling large batched EDI files so multiple transactions are split and processed independently instead of as one large monolithic document. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/edi-split-overview.html)
- **[Mapping]** Use JSONata or XSLT mappings scoped only to the fields your downstream systems actually need, rather than passing through the full service-defined JSON/XML structure, to reduce output file size and downstream processing effort. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/transform-variations.html)
- **[AI-assisted mapping]** Use generative AI-assisted EDI mapping with representative EDI and JSON/XML sample pairs to accelerate mapping development, and review the accuracy score before promoting generated mappings to production. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/generative-ai-assisted-mapping.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Use Amazon CloudWatch to track B2B Data Interchange metrics in real time and set alarms on thresholds that indicate transformation problems. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/monitoring-overview.html)
- **[Logging]** Send logs to Amazon CloudWatch Logs and archive them for durability so transformation and validation activity is available for troubleshooting and long-term audit. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/monitoring-overview.html)
- **[Event-driven automation]** Consume B2B Data Interchange's EventBridge events for successful and failed transformations to trigger downstream AWS Glue ETL jobs, Lambda functions, or Step Functions workflows, and to send automated notifications (e.g. via SNS) on validation or parsing failures. [doc](https://aws.amazon.com/about-aws/whats-new/2024/03/aws-b2b-data-interchange-publishes-events-amazon-eventbridge/)
- **[Auditing]** Use AWS CloudTrail trails to identify which users or roles performed B2B Data Interchange API actions, from which source IP, and when, to support operational investigations. [doc](https://docs.aws.amazon.com/b2bi/latest/userguide/monitoring-overview.html)
- **[Partnership management]** Use a single partnership per trading partner to customize interchange (ISA) and functional group (GS) header details, delimiters, and outbound validation settings, keeping per-partner configuration centralized and auditable via its detailed logs. [doc](https://aws.amazon.com/b2b-data-interchange/faqs/)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
