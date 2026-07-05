# Amazon DataZone — Best Practices

## Common scenarios
- Cataloging and governing data assets across AWS accounts and business units        → Security, Operational Excellence
- Publishing data from AWS Glue, Amazon Redshift, and S3 into a business catalog        → Reliability, Operational Excellence
- Enabling self-service discovery and subscription-based data access for analysts        → Security, Cost Optimization
- Automating metadata generation and data source ingestion at scale        → Operational Excellence, Performance Efficiency

## 🔒 Security
- **[access control]** Grant only the permissions required for each Amazon DataZone task instead of broad access — least privilege reduces the blast radius of errors or compromised credentials. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/security-best-practices.html)
- **[credentials]** Use IAM roles with temporary credentials for producer and consumer applications instead of storing long-term AWS credentials in clients or S3 — long-term credentials are not auto-rotated and are high-impact if leaked. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/security-best-practices.html)
- **[monitoring]** Enable AWS CloudTrail to record Amazon DataZone API calls — CloudTrail captures the caller identity, source IP, and request details needed to investigate and audit activity. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/security-best-practices.html)
- **[cross-account access]** Use AWS Resource Access Manager (RAM) when associating AWS accounts with a DataZone domain rather than ad hoc sharing — RAM centralizes and governs cross-account publish/consume permissions. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/security-best-practices.html)
- **[data protection]** Set up individual users through IAM Identity Center or IAM with MFA enabled, rather than sharing account credentials, so each user has only the access their role requires. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/data-protection.html)
- **[data protection]** Require TLS 1.2 (and prefer TLS 1.3) for all communication with Amazon DataZone endpoints to protect data in transit. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/data-protection.html)
- **[data protection]** Avoid putting confidential or sensitive information (such as customer emails) into tags or free-form name fields — this content can surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/data-protection.html)
- **[data protection]** Use Amazon Macie alongside Amazon DataZone to discover and protect sensitive data stored in S3 assets before or after cataloging. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/data-protection.html)
- **[encryption]** Use an AWS KMS customer managed key to encrypt DataZone domain resources and monitor `CreateGrant`, `GenerateDataKey`, `Decrypt`, and `RetireGrant` CloudTrail events to track how DataZone uses that key. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/encryption-rest-datazone.html)
- **[confused deputy prevention]** Use the `aws:SourceAccount` (and where possible `aws:SourceArn`) global condition keys in resource policies for services DataZone integrates with, to prevent cross-service impersonation of your resources. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/crossservicedeputy.html)
- **[fine-grained access]** Apply row- and column-level asset filters on catalog assets so consumers only see the specific records and fields relevant to their role, rather than granting access to entire assets. [doc](https://aws.amazon.com/blogs/big-data/enhance-data-security-with-fine-grained-access-controls-in-amazon-datazone/)
- **[governance]** Use domain unit authorization policies (domain unit creation, project creation, project membership, glossary/metadata-form creation) to enforce who can create entities and publish metadata, keeping catalog standards consistent. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/working-with-domain-units.html)

## 🛡️ Reliability
- **[cross-service integrations]** Design consumers to react to Amazon DataZone's EventBridge events (for example subscription approvals) for asset types outside Lake Formation-managed Glue and Redshift, so downstream fulfillment stays consistent with catalog state. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html)
- **[account associations]** Associate AWS accounts to a domain via RAM-managed associations so producer/consumer account relationships are governed and auditable rather than manually wired per resource. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/security-best-practices.html)

## ⚡ Performance Efficiency
- **[data source scheduling]** Configure data source run schedules with cron expressions and an explicit timezone so ingestion cadence matches source data freshness needs instead of relying on manual, ad hoc runs. [doc](https://docs.aws.amazon.com/datazone/latest/APIReference/API_ScheduleConfiguration.html)
- **[catalog search]** Configure which metadata fields and business glossary terms are searchable in custom metadata forms to keep catalog search fast and relevant as the number of assets grows. [doc](https://aws.amazon.com/datazone/features/data-access/)

## 💰 Cost Optimization
- **[custom blueprints]** Use custom AWS service blueprints with your existing IAM roles and AWS resources instead of default blueprints when you already operate the underlying services, to avoid duplicating infrastructure. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/working-with-custom-blueprint.html)
- **[blueprint governance]** Restrict which projects and domain unit owners can create environment profiles from a given blueprint, since blueprint configurations provision billable AWS resources (VPCs, subnets, database connections) — controlling this limits unnecessary resource sprawl. [doc](https://docs.aws.amazon.com/help-panel/datazone/latest/console/delegated-permissions-hp.html)
- **[serverless integrations]** Favor serverless services (EventBridge, Step Functions, Lambda, SQS) when building workflows around Amazon DataZone subscription and fulfillment events, since a pay-per-use model avoids the overhead of managing dedicated infrastructure for state tracking. [doc](https://aws.amazon.com/solutions/guidance/streamlining-data-access-with-jira-service-management-and-amazon-datazone/)
- **[quotas]** Track data source run limits (25 runs per data source per day by default) when scheduling ingestion jobs, and request quota increases only when genuinely needed rather than over-provisioning run frequency. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/datazone-limits.html)

## ⚙️ Operational Excellence
- **[domain organization]** Structure domain units to mirror your organization's business units (Sales, Marketing, Finance, etc.) so ownership, policies, and catalog navigation align with how teams actually operate. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/working-with-domain-units.html)
- **[metadata standards]** Use metadata forms and glossary creation policies to enforce consistent, standardized metadata across projects rather than letting each project define its own ad hoc structure. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/datazone-concepts.html)
- **[automation]** Use auto-generated business names and descriptions to reduce manual data entry into the catalog, while monitoring usage against the monthly generation quotas. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/autodoc.html)
- **[auditing]** Use Amazon DataZone's usage auditing capabilities to monitor data asset usage across projects and maintain transparency into who is accessing what. [doc](https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
