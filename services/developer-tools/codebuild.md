# AWS CodeBuild — Best Practices

## Common scenarios
- Compiling source and running unit tests as part of a CI pipeline        → Reliability, Operational Excellence
- Building and pushing Docker images to Amazon ECR        → Security, Performance Efficiency
- Running integration tests against resources inside a VPC        → Security, Reliability
- Reducing build duration and spend across many pipelines        → Cost Optimization, Performance Efficiency

## 🔒 Security
- **[IAM]** Create separate, purpose-built service roles per build type (e.g., test vs. release) scoped only to the log groups, buckets, and registries that build actually needs, instead of one broad role reused everywhere. [doc](https://aws.amazon.com/blogs/security/implementing-defense-security-for-aws-codebuild-pipelines/)
- **[IAM]** Use the `codebuild:buildArn` or `codebuild:projectArn` condition keys in identity-based policies so a resource can verify a call originated from a specific build project. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/permissions-conditionkeys-variables.html)
- **[Confused deputy]** Add the `aws:SourceArn` and `aws:SourceAccount` global condition keys to the CodeBuild service role's trust policy to prevent cross-service impersonation (the confused deputy problem). [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/cross-service-confused-deputy-prevention.html)
- **[Secrets]** Store sensitive values (API keys, credentials, tokens) as `SECRETS_MANAGER` or `PARAMETER_STORE` environment variables rather than `PLAINTEXT`, since plaintext variables are visible in the console, CLI, and logs. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
- **[Untrusted contributions]** Do not enable automatic builds on pull requests from untrusted or external contributors — a submitted PR runs inside the build environment and can access repository credentials and other secrets available there. [doc](https://aws.amazon.com/security/security-bulletins/aws-2025-016/)
- **[Trust boundaries]** Classify contributors (internal, external/forked-repo, automated) and apply stricter webhook filtering and approval gates for public or open-source projects that accept untrusted contributions. [doc](https://aws.amazon.com/blogs/security/implementing-defense-security-for-aws-codebuild-pipelines/)
- **[Networking]** Configure an interface VPC endpoint (AWS PrivateLink) for CodeBuild so build traffic stays on the AWS network instead of traversing the public internet. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/use-vpc-endpoints-with-codebuild.html)
- **[Encryption]** Use a customer-managed AWS KMS key to encrypt build artifacts, cache, and logs at rest when you need control over key policy and rotation beyond the AWS-managed default key. [doc](https://aws.amazon.com/blogs/devops/strategies-to-optimize-the-costs-of-your-builds-on-aws-codebuild/)
- **[Data protection]** Never place confidential or sensitive information (customer emails, credentials in URLs) in tags or free-form text fields such as project names, since these can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/data-protection.html)
- **[Logging]** Enable AWS CloudTrail to capture CodeBuild API activity, including who made a request, from what IP, and when, to support audit and incident investigation. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/cloudtrail.html)
- **[Transport security]** Require TLS 1.2 (TLS 1.3 recommended) and cipher suites with perfect forward secrecy (e.g., ECDHE) for all clients calling the CodeBuild API. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/infrastructure-security.html)

## 🛡️ Reliability
- **[Auto-retry]** Set `auto-retry-limit` on a build project so CodeBuild automatically retries a failed build up to the configured number of additional times before you have to intervene manually. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/auto-retry-build.html)
- **[Timeouts]** Set `timeoutInMinutes` to a value appropriate for the workload so a stalled build fails fast and frees the environment instead of running until the default or maximum timeout. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/create-project.html)
- **[Monitoring]** Create CloudWatch alarms on the `FailedBuild` and `Duration` metrics to detect abnormal failure rates or builds that run longer than expected, and route them to Amazon SNS for notification. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/codebuild_cloudwatch_alarms.html)
- **[VPC access]** Configure VPC connectivity (subnets and security groups) only when builds genuinely need to reach private resources such as RDS, ElastiCache, or internal services, and validate connectivity as part of the build rather than assuming reachability. [doc](https://aws.amazon.com/blogs/devops/access-resources-in-a-vpc-from-aws-codebuild-builds/)

## ⚡ Performance Efficiency
- **[Caching]** Enable Amazon S3 caching for small-to-intermediate build artifacts that are more expensive to rebuild than to download, and use local caching (source, Docker layer, or custom cache modes) for large intermediate artifacts that benefit from being immediately available on the build host. [doc](https://aws.amazon.com/blogs/devops/improve-build-performance-and-save-time-using-local-caching-in-aws-codebuild/)
- **[Docker builds]** Push built Docker images to Amazon ECR and pull them back as an external cache source on subsequent builds to reduce image rebuild time beyond what local caching alone provides. [doc](https://aws.amazon.com/blogs/devops/reducing-docker-image-build-time-on-aws-codebuild-using-an-external-cache/)
- **[Compute]** Use reserved capacity fleets for projects where consistently low build-start latency matters, since dedicated instances stay idle and ready rather than being provisioned per build. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/fleets.html)
- **[Resource utilization]** Review CPU, memory, and storage utilization metrics per build or project to right-size the compute type instead of over- or under-provisioning by guesswork. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/monitoring-builds.html)

## 💰 Cost Optimization
- **[Build duration]** Reduce build duration through caching and dependency reuse, since compute charges accrue by the minute — shorter builds directly reduce cost. [doc](https://aws.amazon.com/blogs/devops/strategies-to-optimize-the-costs-of-your-builds-on-aws-codebuild/)
- **[Compute type]** Choose the smallest compute type that satisfies build CPU/memory needs rather than defaulting to a larger instance class, since charges vary by compute type. [doc](https://aws.amazon.com/codebuild/pricing/)
- **[Reserved capacity]** Only provision reserved capacity fleets when reduced build-start latency is worth the tradeoff, since reserved instances incur charges continuously while provisioned, regardless of build activity. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/fleets.html)
- **[Logging]** Be mindful that CloudWatch Logs charges apply to build log storage, and set appropriate log retention instead of retaining build logs indefinitely by default. [doc](https://aws.amazon.com/blogs/devops/strategies-to-optimize-the-costs-of-your-builds-on-aws-codebuild/)
- **[Encryption]** Use the default AWS-managed KMS keys for build artifact/log encryption when you don't need a customer-managed key, since AWS-managed keys are free while customer-managed keys incur KMS charges. [doc](https://aws.amazon.com/blogs/devops/strategies-to-optimize-the-costs-of-your-builds-on-aws-codebuild/)

## ⚙️ Operational Excellence
- **[Monitoring]** Track build counts, success/failure rates, and duration trends at both the project and account level through CloudWatch metrics to spot regressions in pipeline health over time. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/monitoring-builds.html)
- **[Source credentials]** Scope source-provider credentials (Secrets Manager secret or CodeConnections connection) at the source or project level rather than relying solely on account-level default credentials, so different repositories can use differently-scoped tokens. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/multiple-access-tokens.html)
- **[Auditability]** Review CloudTrail log entries for CodeBuild API calls (e.g., `CreateProject`, `StartBuild`) to track configuration changes and investigate anomalous build activity. [doc](https://docs.aws.amazon.com/codebuild/latest/userguide/understanding-service-name-entries.html)

<!-- meta: last_reviewed=2026-07-05; sources=21 -->
