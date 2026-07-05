# Amazon Kendra — Best Practices

## Common scenarios
- Enterprise search across SharePoint, S3, Confluence, and other repositories        → Security, Operational Excellence
- Retrieval Augmented Generation (RAG) grounding for generative AI assistants        → Performance Efficiency, Reliability
- Secure knowledge search where results must respect source-system permissions        → Security
- Sizing and scaling an index for variable or growing query/document volume        → Reliability, Cost Optimization

## 🔒 Security
- **[access control]** Grant Amazon Kendra IAM roles only the minimum privileges required for the specific job (e.g. data source access, log destination) and audit these permissions regularly and after any application change — limits blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/kendra/latest/dg/security-best-practices.html)
- **[access control]** Strictly control role-based access control (RBAC) permissions for Amazon Kendra applications and administrators. [doc](https://docs.aws.amazon.com/kendra/latest/dg/security-best-practices.html)
- **[access control]** Never add Amazon Kendra as a trusted principal in an S3 bucket policy; instead use IAM roles (with a trust policy allowing Kendra to assume the role) to grant data-source access — avoids accidentally granting broad permissions to an arbitrary principal. [doc](https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html)
- **[data protection]** Set up individual users with IAM Identity Center or IAM instead of sharing account credentials, and require multi-factor authentication (MFA) on every account. [doc](https://docs.aws.amazon.com/kendra/latest/dg/data-protection.html)
- **[data protection]** Enforce TLS 1.2 (recommend TLS 1.3) with cipher suites that support perfect forward secrecy (DHE/ECDHE) for all client communication with Amazon Kendra. [doc](https://docs.aws.amazon.com/kendra/latest/dg/infrastructure-security.html)
- **[data protection]** Encrypt indexed data at rest with a customer-managed AWS KMS key rather than relying on the default AWS-owned key, when you need auditable, revocable control over key usage. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-amazon-kendra/)
- **[data protection]** Never place confidential or sensitive information (such as customer email addresses) in tags or free-form text fields (e.g. a Name field) — this data can end up in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/kendra/latest/dg/data-protection.html)
- **[data protection]** Set up API and user activity logging with AWS CloudTrail, and use FIPS endpoints when FIPS 140-3 validated cryptographic modules are required for CLI/API access. [doc](https://docs.aws.amazon.com/kendra/latest/dg/data-protection.html)
- **[network isolation]** Create an interface VPC endpoint (AWS PrivateLink) for Amazon Kendra so traffic between your VPC and the service does not traverse the public internet and instances don't need public IP addresses. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-amazon-kendra/)
- **[network isolation]** Scope the VPC endpoint policy to only the specific Kendra actions (e.g. `Query`) and principals a workload needs, aligning with least privilege. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-amazon-kendra/)
- **[document-level access]** Use token-based user access control (user context filtering) together with data-source-collected access control lists (ACLs) so search results are filtered to only the documents a given user or group is authorized to read. [doc](https://aws.amazon.com/blogs/machine-learning/building-a-secure-search-application-with-access-controls-using-amazon-kendra/)
- **[document-level access]** For custom connectors or the `BatchPutDocument` API, use the Principal Store to centrally manage user-to-group mappings instead of pushing full group membership on every query — simplifies keeping ACL-based filtering correct as identities change across repositories. [doc](https://aws.amazon.com/blogs/machine-learning/simplify-secure-search-solutions-with-the-new-principal-store-for-secure-search-in-amazon-kendra/)

## 🛡️ Reliability
- **[capacity planning]** Observe query usage patterns (queries per day and peak queries per second) for several weeks before dimensioning an index, then balance built-in adaptive bursting for short spikes against added query capacity units for sustained peaks. [doc](https://aws.amazon.com/blogs/machine-learning/scale-your-amazon-kendra-index/)
- **[capacity planning]** Monitor document count and storage usage with CloudWatch or the console, and add storage capacity units proactively as data grows, since capacity can be added or removed but not reduced below what's already in use. [doc](https://aws.amazon.com/blogs/machine-learning/scale-your-amazon-kendra-index/)
- **[throttling]** Handle `ThrottlingException` from the Query API with client-side retry/backoff (e.g. the SDK's built-in retry behavior) for requests that exceed provisioned and bursting capacity. [doc](https://aws.amazon.com/blogs/machine-learning/scale-your-amazon-kendra-index/)
- **[automation]** Automate query capacity unit scaling with Amazon EventBridge scheduled events and AWS Lambda based on observed business-hour usage patterns instead of manually resizing capacity. [doc](https://aws.amazon.com/blogs/machine-learning/automatically-scale-amazon-kendra-query-capacity-units-with-amazon-eventbridge-and-aws-lambda/)
- **[edition choice]** Use Enterprise Edition (or GenAI Enterprise Edition) rather than Developer Edition for production workloads — Developer Edition is intended for proof-of-concept use and is not recommended for production. [doc](https://docs.aws.amazon.com/kendra/latest/dg/hiw-index-types.html)

## ⚡ Performance Efficiency
- **[relevance]** Tune search relevance by boosting the importance of specific fields or attributes (e.g. document freshness, view counts, authoritative data source) at the index or query level, increasing the `Importance` value in small increments and comparing results against previous queries. [doc](https://docs.aws.amazon.com/kendra/latest/dg/tuning.html)
- **[relevance]** Make fields you intend to boost searchable/facetable in the index first (e.g. an `author` field), since relevance tuning only affects ranking, not whether a document is included in results. [doc](https://aws.amazon.com/blogs/machine-learning/relevance-tuning-with-amazon-kendra/)
- **[index selection]** Choose a GenAI Enterprise Edition index for Retrieval Augmented Generation and Retrieve API use cases — it uses hybrid keyword/semantic search and re-ranker models for higher retrieval accuracy than the other index types. [doc](https://docs.aws.amazon.com/kendra/latest/dg/hiw-index-types.html)

## 💰 Cost Optimization
- **[edition choice]** Start with Developer Edition to explore and prototype an application cost-efficiently, and only move to Enterprise Edition when the workload needs production-level storage, query throughput, or availability. [doc](https://aws.amazon.com/blogs/machine-learning/getting-started-with-the-amazon-kendra-sharepoint-online-connector/)
- **[capacity planning]** Size query and storage capacity units to actual observed usage patterns (queries per second, document counts) rather than over-provisioning, and remove unused capacity units when usage drops. [doc](https://aws.amazon.com/blogs/machine-learning/scale-your-amazon-kendra-index/)
- **[index selection]** Consider a GenAI Enterprise Edition index, which offers smaller and more granular capacity units and a lower starting price than Basic Enterprise Edition, to be more efficient with capacity utilization. [doc](https://docs.aws.amazon.com/kendra/latest/dg/hiw-index-types.html)

## ⚙️ Operational Excellence
- **[monitoring]** Use Amazon CloudWatch metrics to track index health, including document synchronization status and the number of documents that failed to be indexed, and set alarms on thresholds you define. [doc](https://docs.aws.amazon.com/kendra/latest/dg/cloudwatch-metrics.html)
- **[monitoring]** Use the data-source and document CloudWatch Logs streams to get detail on index synchronization jobs and per-document processing issues during ingestion. [doc](https://aws.amazon.com/blogs/industries/fsi-services-spotlight-featuring-amazon-kendra/)
- **[auditing]** Enable AWS CloudTrail to capture all Amazon Kendra API calls (console and programmatic), including request parameters, source IP, and caller identity, for troubleshooting and security investigation. [doc](https://docs.aws.amazon.com/kendra/latest/dg/incident-response.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
