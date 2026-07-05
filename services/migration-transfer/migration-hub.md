# AWS Migration Hub — Best Practices

## Common scenarios
- Tracking migration progress across multiple AWS and partner migration tools        → Operational Excellence
- Discovering on-premises servers, dependencies, and sizing before migrating        → Reliability, Operational Excellence
- Grouping discovered servers into applications and migration waves        → Operational Excellence, Reliability
- Attributing migrated resource costs back to source servers or cost centers        → Cost Optimization

## 🔒 Security
- **[access control]** Grant Migration Hub permissions with the AWS managed policies (`AWSMigrationHubFullAccess`, `AWSMigrationHubDiscoveryAccess`, `AWSMigrationHubDMSAccess`) scoped to each user's role instead of broad admin access — least privilege for console/API/CLI users. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/auth-and-access-explained.html)
- **[discovery agents]** Create a dedicated IAM user with only the `AWSApplicationDiscoveryAgentAccess` policy for the Application Discovery Agent's programmatic credentials, rather than reusing broader operator credentials. [doc](https://aws.amazon.com/blogs/mt/manage-your-cloud-journey-from-assessment-to-migration-with-aws-migration-hub/)
- **[custom policies]** Author custom IAM policies for migration tools that need Migration Hub access beyond the predefined policy templates, and attach them only to the specific users or groups that require them. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/policy-templates.html)

## 🛡️ Reliability
- **[home region]** Choose your AWS Migration Hub home Region deliberately before any discovery or migration activity — all write actions (create, notify, associate, disassociate, import, put) must be made from the home Region, and all discovery data is stored there regardless of target migration Regions. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/home-region.html)
- **[discovery]** Use AWS Application Discovery Agent or Agentless Collector (or Migration Hub import) to build a fact-based inventory of servers, performance, and network dependencies before sizing and grouping — avoid relying on outdated spreadsheets or CMDB data for migration decisions. [doc](https://aws.amazon.com/blogs/mt/using-aws-migration-hub-network-visualization-to-overcome-application-and-server-dependency-challenges/)
- **[dependency mapping]** Use Migration Hub network visualization to identify the blast radius of a server or move group before migrating it, so regression testing and required test coverage can be planned for dependent applications. [doc](https://aws.amazon.com/blogs/mt/using-aws-migration-hub-network-visualization-to-overcome-application-and-server-dependency-challenges/)
- **[migration waves]** Group interdependent servers into applications and organize applications into move groups and migration waves so related components are migrated and tested together, reducing the risk of breaking cross-server dependencies. [doc](https://aws.amazon.com/blogs/mt/using-aws-migration-hub-network-visualization-to-overcome-application-and-server-dependency-challenges/)
- **[tool authorization]** Explicitly connect each migration tool (for example AWS Application Migration Service, AWS DMS, or partner tools) to Migration Hub in your home Region — without this authorization Migration Hub cannot track that tool's migration status. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/gs-new-user-migration.html)
- **[service availability]** Confirm current service status before planning new work: AWS Migration Hub is no longer open to new customers as of November 7, 2025, and AWS directs new discovery/migration-tracking needs to AWS Transform. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/migrationhub-availability-change.html)

## 💰 Cost Optimization
- **[cost allocation tags]** Turn on cost allocation tagging so the automatic `aws:migrationhub:source-id` tags Migration Hub applies to migrated EC2 instances and AMIs can be used in AWS Cost Explorer to trace spend back to the originating on-premises server. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/tagging-migration-resources.html)
- **[sizing]** Use Application Discovery Service's collected average and maximum utilization data (rather than assumptions) to drive EC2 instance-type recommendations, avoiding oversized and overpriced target instances. [doc](https://aws.amazon.com/blogs/mt/manage-your-cloud-journey-from-assessment-to-migration-with-aws-migration-hub/)

## ⚙️ Operational Excellence
- **[discovery scope]** Run Application Discovery Agent data collection over a representative period (commonly around 14 days) to capture peak/stress periods, giving more reliable performance data for planning than a short snapshot. [doc](https://aws.amazon.com/blogs/mt/manage-your-cloud-journey-from-assessment-to-migration-with-aws-migration-hub/)
- **[server tagging]** Tag discovered servers in Migration Hub with custom key-value metadata to organize and track migration planning, in addition to (not instead of) AWS resource tags used for cost and governance. [doc](https://docs.aws.amazon.com/application-discovery/latest/userguide/tag-servers.html)
- **[data export]** Export discovery and migration-wave data from Migration Hub (for example via Amazon Athena integration or CLI export tasks) to analyze dependencies and hand off structured migration plans to execution tools like AWS Application Migration Service. [doc](https://aws.amazon.com/blogs/migration-and-modernization/export-aws-migration-hub-data-for-import-into-aws-application-migration-service/)
- **[home region changes]** Treat changing the Migration Hub home Region as a deliberate, disruptive operation — review the impact on in-flight discovery and migration tracking before switching, since historical data association depends on the home Region setting. [doc](https://docs.aws.amazon.com/migrationhub/latest/ug/change-home-region.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
