# AWS App Runner - Best Practices

## Common scenarios
- Run a containerized web app or API from source code or an image without managing servers -> operational excellence
- Connect a public-facing service to private resources (RDS, ElastiCache) in your VPC -> security
- Expose an internal-only microservice reachable solely from within a VPC -> security
- Auto-scale a bursty API and pause it when idle to control spend -> cost optimization

## 🔒 Security
- **[IAM]** Customize App Runner managed policies and grant only the permissions your users and instance/access roles actually need - least privilege limits blast radius from errors or compromise. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-best-practices.html)
- **[Secrets]** Reference secrets and config from Secrets Manager or SSM Parameter Store as environment variables instead of hardcoding them - App Runner stores only the ARN, so sensitive data stays out of service config and logs. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/env-variable.html)
- **[Image security]** Scan container images for vulnerabilities using Amazon ECR image scanning before deploying - catches known CVEs early in the pipeline. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-best-practices.html)
- **[Edge protection]** Associate an AWS WAF web ACL with the service to filter HTTP(S) requests - guards endpoints against common web exploits and unwanted bots. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/waf.html)
- **[Network isolation]** Use a private service (PrivateLink interface endpoint) for internal workloads so the service is reachable only from designated VPCs and never the public internet. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security.html)
- **[Outbound networking]** Route outbound traffic through a VPC connector and scope its security group's outbound rules to the exact destination endpoints - inbound rules are ignored, so tighten egress. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security.html)
- **[Data protection]** Enforce TLS 1.2+ for API clients, enable MFA on accounts, and never place sensitive data in tags or free-form name fields - those values may surface in billing and diagnostic logs. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-data-protection.html)
- **[Encryption]** Provide a customer-managed KMS key to encrypt stored copies of your source and service logs when an AWS-owned key does not meet compliance needs. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security.html)

## 🛡️ Reliability
- **[High availability]** Deploy in a single Region and let App Runner spread instances across multiple Availability Zones automatically - you inherit AWS fault-tolerance without managing failover. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-resilience.html)
- **[Health checks]** Switch the health check protocol from the default TCP to HTTP with a real application path so App Runner verifies the app responds, not just that the port is open. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/manage-configure-healthcheck.html)
- **[Auto scaling]** Tune MaxConcurrency, MinSize, and MaxSize per workload, raising MinSize for high availability so instances spread across more AZs and warm reserve absorbs traffic spikes. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/manage-autoscaling.html)
- **[Disaster recovery]** For stricter resiliency requirements, run active-active across two Regions with Amazon Route 53 managing traffic - keeps the app serving even during a rare Regional impairment. [doc](https://aws.amazon.com/blogs/containers/architecting-for-resiliency-on-aws-app-runner/)

## ⚡ Performance Efficiency
- **[Right-sizing]** Tune per-instance vCPU/memory together with MaxConcurrency and validate with load testing - matching capacity to the workload avoids both throttling and waste. [doc](https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/)
- **[Tracing]** Enable X-Ray tracing via the observability configuration to find root causes of latency and errors across distributed services. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/monitor.html)

## 💰 Cost Optimization
- **[Idle workloads]** Pause services that are not in use through the console, CLI, or API, and resume on demand - you avoid paying for active compute while idle. [doc](https://aws.amazon.com/blogs/containers/centralized-observability-for-aws-app-runner-services/)
- **[Provisioned reserve]** Keep MinSize only as large as availability needs require - you pay memory for every provisioned instance but CPU only for the active subset, so excess reserve adds cost. [doc](https://docs.aws.amazon.com/cdk/api/v2/dotnet/api/Amazon.CDK.AWS.AppRunner.CfnAutoScalingConfigurationProps.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Set CloudWatch alarms on key App Runner and custom metrics, and track sensitive CloudTrail actions like PauseService and DeleteConnection - detective controls surface incidents fast. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-best-practices.html)
- **[Logging]** Stream application, build, and deployment logs to CloudWatch Logs and use them for debugging and security/access audits. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/security-monitoring.html)
- **[Deployments]** Use automatic deployment for CI/CD, but understand that for code repos only changes inside the configured source directory trigger a deploy - use manual deployment for changes outside it. [doc](https://docs.aws.amazon.com/apprunner/latest/dg/manage-deploy.html)

<!-- meta: last_reviewed=2026-06-29; sources=19 -->
