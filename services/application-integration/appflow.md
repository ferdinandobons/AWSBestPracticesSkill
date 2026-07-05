# Amazon AppFlow — Best Practices

## Common scenarios
- Bi-directional data sync between SaaS apps (Salesforce, Zendesk, Marketo) and AWS data stores        → Security, Reliability
- Ingesting SaaS data into Amazon S3 / Redshift for analytics without building custom connectors        → Cost Optimization, Operational Excellence
- Private, non-internet-routed transfer of sensitive SaaS data into AWS        → Security
- Scheduled or event-driven incremental data replication pipelines        → Reliability, Performance Efficiency

## 🔒 Security
- **[Encryption]** Use a customer managed AWS KMS key instead of the AWS managed key for connection data and S3-destination data so you retain full control over key policy, rotation, and access revocation. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/data-protection.html)
- **[Networking]** Choose the "Create new connection with AWS PrivateLink" option for supported connectors (e.g. Salesforce, SAP OData) so flow data and metadata/authorization calls never traverse the public internet. [doc](https://aws.amazon.com/blogs/apn/building-secure-and-private-data-flows-between-aws-and-salesforce-using-amazon-appflow/)
- **[Networking]** Require TLS 1.2 or later (TLS 1.3 recommended) and cipher suites with perfect forward secrecy for all clients calling the AppFlow API. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/infrastructure-security.html)
- **[IAM]** Apply least-privilege identity-based policies for flow and connector-profile management, starting from AWS managed policies and narrowing to customer managed policies scoped to specific flows/actions. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Add IAM policy conditions (e.g. require SSL, restrict by source service) to further constrain who can create, modify, or run flows, and validate policies with IAM Access Analyzer. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Enable multi-factor authentication for IAM principals that can manage AppFlow resources, since flow and connector changes can move sensitive data and incur cost. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Data handling]** Never place confidential or sensitive values (e.g. customer emails) into flow names, tags, or other free-form text fields — this data can surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/data-protection.html)
- **[Data handling]** Do not embed credentials in externally supplied URLs used to validate requests to third-party servers. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/data-protection.html)
- **[Auditing]** Enable AWS CloudTrail trails covering AppFlow to capture `CreateFlow`, `CreateConnectorProfile`, `TagResource`, and other API activity for security review and forensics. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/appflow-cloudtrail-logs.html)

## 🛡️ Reliability
- **[Error handling]** Configure `ErrorHandlingConfig` on the destination connector deliberately — decide whether a flow should fail on the first record error or continue processing remaining records, based on how your downstream system tolerates partial writes. [doc](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-appflow-flow-errorhandlingconfig.html)
- **[Monitoring]** Subscribe to AppFlow's EventBridge notifications (`AppFlow Start/End Flow Run Report`, `AppFlow Event/Scheduled Flow Deactivated`) to detect and react automatically when a flow is deactivated due to repeated failures. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/flow-notifications.html)
- **[Incremental transfer]** When using incremental transfer, set a time offset large enough to absorb source-system timestamp latency so records changed close to the scheduled run time aren't missed. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/flow-triggers.html)
- **[Data completeness]** Enable "Import deleted records" where supported so downstream data stores stay consistent with source-system deletions during incremental sync. [doc](https://aws.amazon.com/blogs/big-data/synchronize-your-salesforce-and-snowflake-data-to-speed-up-your-time-to-insight-with-amazon-appflow/)

## ⚡ Performance Efficiency
- **[Transfer mode]** Use incremental transfer with a source timestamp field instead of full transfers on every run, so each execution moves only added or changed records. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/flow-triggers.html)
- **[Initial load]** For a bulk historical backfill outside the default 30-day window, run the flow on demand with a filter for the desired time range first, then switch it to scheduled incremental mode for ongoing runs. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/flow-triggers.html)
- **[Field mapping]** Use bulk field-mapping (CSV upload) for datasets with many fields, and apply data filters to transfer only the fields and records actually needed, reducing processing volume. [doc](https://aws.amazon.com/appflow/getting-started/)

## 💰 Cost Optimization
- **[Transfer mode]** Prefer incremental transfers over repeated full extracts to reduce the volume of data processed and moved on each scheduled run. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/flow-triggers.html)
- **[Filtering]** Apply data filters and field selection so flows transfer only required fields and records instead of entire objects, reducing processed data volume. [doc](https://aws.amazon.com/appflow/getting-started/)

## ⚙️ Operational Excellence
- **[Monitoring]** Monitor the `AWS/AppFlow` CloudWatch metrics (`FlowExecutionsStarted`, `FlowExecutionsFailed`, `FlowExecutionsSucceeded`, `FlowExecutionTime`, `FlowExecutionRecordsProcessed`) per `FlowName` and set alarms on failure counts and execution time. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/monitoring-cloudwatch.html)
- **[Alerting]** Build an automated alerting pipeline (EventBridge rule → Lambda → SNS) off flow failure events so operators are notified without polling the console. [doc](https://aws.amazon.com/blogs/big-data/build-a-modern-data-architecture-on-aws-with-amazon-appflow-aws-lake-formation-and-amazon-redshift/)
- **[IaC]** Manage flows and connector profiles with AWS CloudFormation (`AWS::AppFlow::Flow`, `AWS::AppFlow::ConnectorProfile`) for repeatable, version-controlled deployments alongside the rest of your infrastructure. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html)
- **[Auditing]** Use CloudTrail event history/trails to determine who made a given AppFlow API request, from where, and when, for operational troubleshooting. [doc](https://docs.aws.amazon.com/appflow/latest/userguide/appflow-cloudtrail-logs.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
