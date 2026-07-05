# AWS Secrets Manager — Best Practices

## Common scenarios
- Storing and auto-rotating database credentials (RDS, Redshift, DocumentDB)        → Security, Reliability
- Replacing hardcoded API keys/tokens in application code with runtime secret retrieval        → Security, Operational Excellence
- Sharing secrets safely across accounts, Regions, or services (Lambda, ECS, EKS)        → Security, Reliability
- Auditing and controlling who can read or change sensitive credentials        → Security, Operational Excellence

## 🔒 Security
- **[Storage]** Store all credentials, API keys, and other sensitive values in Secrets Manager instead of embedding them in code or config files — Secrets Manager encrypts secrets at rest with a key you control and transmits them over TLS on retrieval. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Code hygiene]** Use Amazon CodeGuru Reviewer's secrets detector (or Amazon Q code scanning) to find hardcoded passwords, connection strings, and credentials left in application code. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Encryption]** Use the AWS-managed key `aws/secretsmanager` for most secrets; switch to a customer managed KMS key only when you need cross-account access or a custom key policy. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Encryption]** When using a customer managed key, scope its key policy to the `kms:ViaService` condition for `secretsmanager.<region>.amazonaws.com`, and further restrict it with Secrets Manager encryption-context conditions so the key can only be used through Secrets Manager. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Access control]** Apply least-privilege IAM policies, resource policies, and attribute-based access control (ABAC) to secrets rather than broad wildcard grants. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Access control]** Set `secretsmanager:BlockPublicPolicy: true` on identity policies that allow `PutResourcePolicy`, so no one can attach a resource policy that grants broad/public access to a secret. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Access control]** Avoid relying solely on IP-address conditions (`aws:SourceIp`) to restrict secret access — AWS services acting on your behalf (e.g. a rotation Lambda) call from AWS-internal address space and will be blocked unexpectedly. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Access control]** Use `aws:SourceVpc` / `aws:SourceVpce` conditions to scope access to a specific VPC or VPC endpoint, but verify this doesn't inadvertently block AWS services that access the secret on your behalf outside that VPC. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[CLI]** Avoid passing secret values as plaintext arguments in AWS CLI commands — command shells can log history or expose the last command, so mitigate exposure risk per the CLI guidance before entering sensitive values. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Networking]** Run infrastructure that accesses secrets on private networks and use an interface VPC endpoint for Secrets Manager instead of routing calls over the public internet. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Threat detection]** Enable Amazon GuardDuty to detect anomalous secret access patterns, such as unusual API call sequences or credential use from outside expected networks. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitoring-guardduty.html)

## 🛡️ Reliability
- **[Rotation]** Enable automatic rotation for every secret and rotate at least every 30 days (as often as every four hours) to limit the impact of a compromised credential. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Rotation]** Use the built-in Lambda-based rotation integrations for Amazon RDS, Redshift, and DocumentDB, or managed rotation where available, instead of building custom rotation logic. [doc](https://docs.aws.amazon.com/help-panel/secretsmanager/latest/console/configure-automatic-rotation-pane.html)
- **[Rotation]** Choose a rotation window that ends before midnight UTC on the day it starts, and schedule it during low-traffic periods so rotation doesn't coincide with peak application load. [doc](https://docs.aws.amazon.com/help-panel/secretsmanager/latest/console/configure-automatic-rotation-pane.html)
- **[Resiliency]** Replicate secrets to additional AWS Regions using Secrets Manager's built-in replication to support multi-Region and disaster-recovery architectures. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Client resilience]** Instantiate the Secrets Manager client/cache outside the request path (e.g. outside the Lambda handler) so a warm execution environment reuses cached secrets instead of re-fetching on every invocation. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-java.html)

## ⚡ Performance Efficiency
- **[Caching]** Use a supported client-side caching library (Java, Python, .NET, Go, Rust) or the AWS Parameters and Secrets Lambda Extension to cache secrets locally and refresh only when needed, rather than calling `GetSecretValue` on every use. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Caching]** In Lambda, use the AWS Parameters and Secrets Lambda Extension or the Powertools for AWS Lambda parameters utility, both of which maintain a local cache and return a secret immediately on a cache hit instead of invoking the Secrets Manager API. [doc](https://docs.aws.amazon.com/lambda/latest/dg/with-secrets-manager.html)
- **[Batch retrieval]** Use `BatchGetSecretValue` to retrieve multiple secrets in a single call instead of issuing one `GetSecretValue` call per secret in client-side applications. [doc](https://aws.amazon.com/blogs/security/how-to-use-the-batchgetsecretsvalue-api-to-improve-your-client-side-applications-with-aws-secrets-manager/)
- **[Container/K8s workloads]** Use the native integrations for Amazon ECS, Amazon EKS, and EC2 (or the AWS Workload Credentials Provider) to standardize how workloads consume secrets instead of custom retrieval code per environment. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)

## 💰 Cost Optimization
- **[API calls]** Use client-side caching so repeated reads of the same secret hit the local cache instead of generating a billable `GetSecretValue` API call each time. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-java.html)
- **[Encryption key choice]** Use the no-cost AWS-managed key `aws/secretsmanager` unless cross-account access or a custom key policy specifically requires a customer managed KMS key, which incurs its own monthly and per-API-call charges. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- **[Monitoring]** Track estimated Secrets Manager charges with a CloudWatch billing alarm and use AWS Cost Anomaly Detection to catch unexpected spend from secret count or API-call growth. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitor-secretsmanager-costs.html)
- **[Cost allocation]** Tag secrets with cost allocation tags so spend can be tracked and attributed per project or team. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Enable AWS CloudTrail logging for Secrets Manager to capture all API calls (console and programmatic) plus related events like rotation and secret-version deletion, so unexpected changes can be investigated and rolled back. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitoring.html)
- **[Monitoring]** Use Amazon CloudWatch metrics and alarms, and match Secrets Manager events with Amazon EventBridge, to get notified of rotation failures, unused secrets, or other operational events. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitoring.html)
- **[Compliance]** Use AWS Config rules to continuously monitor secrets for compliance — for example, verifying that rotation is enabled, executing successfully, and completing within the expected duration. [doc](https://aws.amazon.com/secrets-manager/faqs/)
- **[Lifecycle hygiene]** Monitor for secrets that remain unused for an extended period and for secrets scheduled for deletion, so stale or orphaned credentials get reviewed and decommissioned. [doc](https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitoring.html)
- **[Naming]** Use a hierarchical, consistent naming convention for secrets so they remain manageable as the number of secrets scales across teams and environments. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/secure-sensitive-data-secrets-manager-terraform/best-practices.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
