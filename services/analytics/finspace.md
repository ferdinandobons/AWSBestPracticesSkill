# Amazon FinSpace — Best Practices

## Common scenarios
- Running managed kdb Insights clusters for real-time and historical capital markets time-series analytics        → Reliability, Performance Efficiency, Cost Optimization
- Migrating existing on-premises kdb ticker plants, RDB/HDB, and gateway workloads to a managed AWS environment        → Reliability, Operational Excellence
- Connecting a FinSpace environment to on-premises networks or other VPCs for hybrid data access        → Security, Reliability
- Enforcing fine-grained data access control and auditing for regulated financial data        → Security, Operational Excellence

## 🔒 Security
- **[IAM]** Apply least-privilege IAM policies to restrict FinSpace Managed kdb operations, following general IAM security best practices rather than broad account-wide grants. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/identity-management.html)
- **[Auditing]** Limit access to sensitive and important auditing functions (such as viewing audit data) to a small, deliberately assigned permission group. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/security-best-practices.html)
- **[Sensitive fields]** Never place PHI, PII, or other sensitive identifiers in free-form visible fields such as datastore or job names, including when using the update or bulk import APIs — this data can be captured in diagnostic logs. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/security-best-practices.html)
- **[Credentials]** Avoid using the AWS account root user for FinSpace setup and administration tasks; create individual IAM users or use SSO instead, and enable multi-factor authentication (MFA) on every account. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/data-protection.html)
- **[Encryption at rest]** Specify a customer-owned AWS KMS key when creating a FinSpace environment so all service data and metadata are encrypted with a key you control and can rotate or revoke. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/data-encryption.html)
- **[Transport security]** Require clients to use TLS 1.2 (TLS 1.3 recommended) with cipher suites that support perfect forward secrecy (such as DHE or ECDHE) when calling FinSpace APIs. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/infrastructure-security.html)
- **[Permission groups]** Assign permissions to permission groups rather than directly to individual users, and use the superuser account only for initial setup, switching to scoped application users for day-to-day access. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/concepts-terms.html)
- **[Federation]** Integrate FinSpace with your organization's identity provider using SAML-based single sign-on instead of managing standalone email/password credentials, so authentication follows your central identity governance. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/finspace-security.html)
- **[Network isolation]** Connect FinSpace to your network through a customer-managed transit gateway rather than exposing environments to the public internet, and configure a private NAT gateway path for outbound traffic. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/cno-vpc.html)
- **[Sensitive URLs]** Never embed credentials in URLs passed to FinSpace or other AWS services (console, API, CLI, SDKs), since these can be captured in logs. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/data-protection.html)
- **[Data discovery]** Use Amazon Macie to discover and help secure sensitive personal data stored in the Amazon S3 buckets that back FinSpace datasets. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[Multi-AZ clusters]** Configure Managed kdb Insights clusters with `azMode` set to `MULTI` to deploy across multiple Availability Zones so analytics workloads remain available during critical trading hours. [doc](https://docs.aws.amazon.com/finspace/latest/management-api/API_KxCluster.html)
- **[Backup ownership]** Plan your own cross-AZ/cross-Region backup strategy using the FinSpace SDK to query and export data, since FinSpace itself does not back up data to other Availability Zones or Regions despite being multi-AZ. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/resilience.html)
- **[Redundant connectivity]** When connecting FinSpace to your network via transit gateway, provision the attachment across all Availability Zones supplied by FinSpace to avoid a single point of failure in hybrid connectivity. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/manage-vpc.html)
- **[Autoscaling]** Configure autoscaling for Managed kdb Insights clusters so capacity keeps pace with volatile market conditions instead of relying on fixed, manually sized clusters. [doc](https://aws.amazon.com/finspace/)

## ⚡ Performance Efficiency
- **[Scaling groups]** Run multiple kdb clusters on a shared scaling-group host to place workloads whose memory demand peaks at different times, maximizing utilization compared to one dedicated host per cluster. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/finspace-managed-kdb-scaling-groups.html)
- **[Dataviews for read performance]** Use dataviews with pre-warmed cache and tiered storage for HDB clusters running on scaling groups to accelerate high-performance read access instead of relying on cluster-specific disk cache, which scaling groups don't support. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/kdb-clusters-running-clusters-comparison.html)
- **[Workload isolation trade-off]** Choose dedicated clusters (one host per node) when workloads need strong isolation and guaranteed compute, and reserve scaling groups for workloads that can tolerate shared compute in exchange for higher utilization. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/kdb-clusters-running-clusters-comparison.html)
- **[Cluster sizing]** Select the managed Spark cluster template that matches the size and complexity of the analysis you need to run, rather than defaulting to the largest available template. [doc](https://aws.amazon.com/documentation-overview/finspace/)

## 💰 Cost Optimization
- **[Shared compute]** Consolidate multiple kdb clusters onto scaling groups instead of provisioning a dedicated host per cluster, reducing the fixed compute footprint needed to serve workloads whose resource demands don't conflict throughout the day. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/finspace-managed-kdb-scaling-groups.html)
- **[Tiered caching]** Use dataviews with configurable, tiered storage caching to accelerate only the important queries rather than caching entire datasets, managing the cost of cached capacity. [doc](https://aws.amazon.com/finspace/)
- **[Pay-as-you-go compute]** Rely on FinSpace's pay-as-you-go compute, storage, and caching model for Managed kdb Insights clusters instead of over-provisioning fixed on-premises hardware for peak load. [doc](https://aws.amazon.com/finspace/pricing/)

## ⚙️ Operational Excellence
- **[Managed service benefits]** Rely on FinSpace to handle bi-temporal storage, the data catalog, and Spark cluster management instead of building this undifferentiated infrastructure yourself, focusing engineering effort on integrating data sources. [doc](https://aws.amazon.com/documentation-overview/finspace/)
- **[Health monitoring]** Rely on Managed kdb Insights' continuous monitoring of underlying server health and capacity, which automatically replaces failed servers and applies patches, instead of building custom infrastructure monitoring. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/finspace-managed-kdb.html)
- **[Audit trail]** Create an AWS CloudTrail trail (beyond the default 90-day event history) to retain a durable, ongoing record of all FinSpace API operations and console actions for compliance review. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/logging-cloudtrail-events.html)
- **[Audit reports]** Generate and export FinSpace audit reports, filtered by activity type, time period, user, or dataset, to demonstrate compliance with your data governance policies. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/audit-report.html)
- **[Infrastructure as code]** Manage kdb environments and clusters through the Terraform-integrated FinSpace APIs as part of your CI/CD workflows instead of relying solely on manual console configuration. [doc](https://aws.amazon.com/finspace/)
- **[Identity tracing]** Use the CloudTrail userIdentity element to determine whether FinSpace requests came from a specific user, a federated/temporary role, or another AWS service when investigating operational events. [doc](https://docs.aws.amazon.com/finspace/latest/userguide/logging-cloudtrail-events.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
