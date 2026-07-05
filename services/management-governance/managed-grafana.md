# Amazon Managed Grafana — Best Practices

## Common scenarios
- Centralized observability dashboards correlating metrics, logs, and traces from CloudWatch, Prometheus, OpenSearch, and X-Ray        → Operational Excellence, Performance Efficiency
- Visualizing operational data from resources inside a private VPC (RDS, self-managed Prometheus, OpenSearch)        → Security, Reliability
- Sharing dashboards and alerting across teams in a multi-account or multi-Region AWS Organization        → Security, Operational Excellence
- Auditing and governing who can view, edit, or administer Grafana workspaces        → Security, Cost Optimization

## 🔒 Security
- **[authentication]** Authenticate users through AWS IAM Identity Center or an existing SAML 2.0 identity provider instead of static credentials — reuses your corporate identity provider's trust relationships and centralizes user lifecycle management. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/authentication-in-AMG.html)
- **[least privilege]** Assign users and groups the least-privilege Grafana role they need (Viewer, Editor, or Admin) and use Teams to scope dashboard and data source access to only the people who need it. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/Grafana-teams.html)
- **[data source permissions]** Prefer service-managed IAM permissions so Amazon Managed Grafana automatically provisions least-privilege, per-data-source IAM roles and policies, rather than hand-maintaining broad customer-managed roles. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html)
- **[cross-account access]** When querying data sources in other accounts, establish an explicit trust relationship between the workspace role and a dedicated data-source role in the target account rather than granting broad cross-account access. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/AMG-manage-permissions.html)
- **[network access]** Restrict inbound network access to workspaces using customer-managed prefix lists and VPC endpoints instead of leaving workspaces open to the public internet. [doc](https://aws.amazon.com/blogs/mt/announcing-inbound-network-access-control-in-amazon-managed-grafana/)
- **[private data sources]** Connect the workspace to your VPC (with per-subnet elastic network interfaces) to query private data sources like OpenSearch domains or RDS databases without exposing them over the public internet. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/AMG-configure-vpc.html)
- **[private API access]** Use interface VPC endpoints powered by AWS PrivateLink to reach the Amazon Managed Grafana API or workspace URL privately from within a VPC, and attach a VPC endpoint policy to control which principals and actions are allowed. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/VPC-endpoints.html)
- **[transport security]** Require TLS 1.2 (and prefer TLS 1.3) with cipher suites that support perfect forward secrecy (such as ECDHE) for all clients connecting to the Amazon Managed Grafana API. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/infrastructure-security.html)
- **[audit logging]** Enable AWS CloudTrail trails (multi-Region) to capture Amazon Managed Grafana control-plane API calls and Grafana-API data-changing calls for compliance and audit tracking beyond the 90-day default event history. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/logging-using-cloudtrail.html)
- **[sensitive data]** Avoid putting confidential or sensitive information into workspace tags, names, or other free-form text fields, since this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/data-protection.html)
- **[API keys]** Treat Grafana API keys like passwords: avoid storing them in plain text and rely on their limited (30-day maximum) lifetime as a security control for automation workflows. [doc](https://aws.amazon.com/blogs/mt/amazon-managed-grafana-is-now-generally-available/)

## 🛡️ Reliability
- **[multi-AZ]** Rely on Amazon Managed Grafana's built-in multi-AZ replication and automatic unhealthy-node replacement instead of building custom failover logic for the Grafana control plane. [doc](https://aws.amazon.com/grafana/features/)
- **[version upgrades]** Test a new Grafana version in a non-production workspace before updating production, since workspace version updates are irreversible and cannot be downgraded. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/AMG-workspace-version-update.html)
- **[plugin compatibility]** After upgrading the workspace's Grafana version, check and update installed plugins individually, since a version update does not automatically update plugins and some may be incompatible with the new version. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/grafana-plugins.html)
- **[VPC routing]** When connecting a workspace to a VPC, verify the VPC can still reach any previously configured public data sources and notification channels, since all traffic is rerouted through the VPC connection once configured. [doc](https://aws.amazon.com/grafana/faqs/)

## ⚡ Performance Efficiency
- **[native integrations]** Use Amazon Managed Grafana's native data source integrations (CloudWatch, Amazon Managed Service for Prometheus, OpenSearch Service, X-Ray, Timestream, IoT SiteWise) so credentials and permissions are auto-provisioned instead of manually configured. [doc](https://aws.amazon.com/grafana/features/)
- **[private connectivity latency]** Keep the Amazon Managed Grafana workspace and its VPC-connected data sources in the same account and Region where possible, using VPC peering or Transit Gateway only when cross-Region or cross-account connectivity is unavoidable, to minimize added network hops and latency. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/AMG-configure-vpc.html)

## 💰 Cost Optimization
- **[user role sizing]** Assign the Viewer role (rather than Editor or Admin) to users who only need to view dashboards, since Amazon Managed Grafana bills per active user and Viewer licenses cost less than Editor/Admin licenses. [doc](https://aws.amazon.com/grafana/pricing/)
- **[active user hygiene]** Regularly review and remove workspace access for users who no longer need it, since only users who actually sign in or call the API during a billing cycle are counted as active and billed. [doc](https://aws.amazon.com/grafana/faqs/)
- **[enterprise plugins]** Enable Amazon Managed Grafana Enterprise plugins only for workspaces and users that need them, since they incur an additional per-active-user charge on top of the base Editor/Viewer license. [doc](https://aws.amazon.com/grafana/faqs/)

## ⚙️ Operational Excellence
- **[teams]** Organize users into Grafana Teams so dashboard and data source permissions are managed at the group level and new members automatically inherit access, instead of granting permissions one dashboard at a time. [doc](https://aws.amazon.com/grafana/features/)
- **[team sync]** Use Team Sync to synchronize IAM Identity Center or SAML identity-provider groups directly with Grafana Teams, keeping access in step with your corporate directory. [doc](https://docs.aws.amazon.com/grafana/latest/userguide/Grafana-teams.html)
- **[staged version updates]** Plan multi-step version upgrades (for example 8.4 → 9.4 → 10.4) and review breaking changes beforehand, since the update process is irreversible and cannot be paused or canceled once started. [doc](https://aws.amazon.com/blogs/mt/amazon-managed-grafana-announces-support-for-grafana-version-10-4/)
- **[event-driven automation]** Use the CloudTrail-delivered EventBridge events for Amazon Managed Grafana (`source: aws.grafana`) to automate responses to workspace configuration or permission changes. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-grafana.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
