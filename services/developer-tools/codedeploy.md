# AWS CodeDeploy — Best Practices

## Common scenarios
- Automating code deployments to EC2 or on-premises fleets        → Reliability, Operational Excellence
- Blue/green or canary traffic shifting for Lambda and ECS releases        → Reliability, Operational Excellence
- Rolling out application updates with automatic health-based rollback        → Reliability
- Zonal, fault-isolated deployments across Availability Zones        → Reliability

## 🔒 Security
- **[IAM]** Grant CodeDeploy service roles only the managed policy scoped to the compute platform in use (`AWSCodeDeployRole`, `AWSCodeDeployRoleForECS`/`AWSCodeDeployRoleForECSLimited`, or the Lambda equivalent) rather than broad permissions — least privilege limits blast radius if the role is compromised. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html)
- **[IAM]** Restrict the EC2 instance profile's Amazon S3 permissions to only the buckets that hold your application revisions and the CodeDeploy agent installer, instead of `Resource: "*"` — avoid granting broad `s3:Get*`/`s3:List*` access. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-iam-instance-profile.html)
- **[Access control]** Use IAM resource-level permissions to scope which users can deploy or view specific CodeDeploy applications and deployment groups — prevents accidental deployment to the wrong application. [doc](https://aws.amazon.com/codedeploy/faqs/)
- **[Data protection]** Require TLS 1.2 or later (TLS 1.3 recommended) for all API calls to CodeDeploy and sign requests with IAM credentials or temporary STS credentials rather than long-lived access keys. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/infrastructure-security.html)
- **[Data protection]** Enable AWS CloudTrail to log CodeDeploy API and user activity, and never place confidential or sensitive information in tags or free-form name fields since they can surface in logs or billing data. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/data-protection.html)
- **[Identity]** Set up individual IAM users or IAM Identity Center identities with MFA instead of sharing root or broad credentials for triggering deployments. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[Rollback]** Enable automatic rollback on a deployment group so failed deployments or triggered CloudWatch alarms automatically redeploy the last known-good revision. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-server.html)
- **[Rollback]** Always keep previously deployed application revisions available (in S3 or your repository) so a rollback can succeed — CodeDeploy rolls back by redeploying a prior revision, not by reverting in place. [doc](https://aws.amazon.com/codedeploy/faqs/)
- **[Monitoring]** Associate CloudWatch alarms (up to ten per deployment group) with deployment groups and grant the service role CloudWatch permissions so CodeDeploy automatically stops a deployment when a monitored metric breaches its threshold. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html)
- **[Traffic shifting]** Use canary or linear deployment configurations for Lambda and ECS compute platforms to expose a small percentage of traffic to the new version before full rollout, reducing blast radius from bad releases. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/primary-components.html)
- **[Availability]** Configure the minimum number of healthy hosts (or `zonal-config`) for EC2/On-Premises deployments so a deployment doesn't take down more capacity than your workload can tolerate. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations-create.html)
- **[Zonal deployments]** Use CodeDeploy zonal configuration to deploy one Availability Zone at a time, containing the blast radius of a bad deployment to a single AZ and aligning recovery with an AZ-independent architecture. [doc](https://aws.amazon.com/blogs/devops/fault-isolated-zonal-deployments-with-aws-codedeploy/)
- **[Auto Scaling integration]** Avoid manually creating or editing the Auto Scaling lifecycle hooks that CodeDeploy manages — configuration errors here can break the integration and cause deployment loops on transient failures. [doc](https://aws.amazon.com/blogs/devops/under-the-hood-aws-codedeploy-and-auto-scaling-integration/)
- **[Auto Scaling integration]** Monitor Auto Scaling launch/terminate notifications closely during deployments to catch a bad target revision before it causes a repeated instance launch-and-terminate cycle. [doc](https://aws.amazon.com/blogs/devops/under-the-hood-aws-codedeploy-and-auto-scaling-integration/)

## ⚙️ Operational Excellence
- **[Lifecycle hooks]** Validate AppSpec file hook scripts (e.g., `ApplicationStop`, `BeforeInstall`, `AfterInstall`) return exit code 0 on success and keep script logic idempotent, since the CodeDeploy agent logs each hook's status and fails the deployment on nonzero exit. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/application-specification-files.html)
- **[Testing]** Use the `codedeploy-local` CLI to validate and debug an AppSpec file and its hook scripts on a local or test instance before shipping a revision through the live deployment pipeline. [doc](https://aws.amazon.com/blogs/devops/how-to-test-and-debug-aws-codedeploy-locally-before-you-ship-your-code/)
- **[Agent management]** Install or start the CodeDeploy agent as the last step of instance launch scripts (user data/cfn-init) so deployments don't race against unfinished dependency installation. [doc](https://aws.amazon.com/blogs/devops/under-the-hood-aws-codedeploy-and-auto-scaling-integration/)
- **[Monitoring]** Centralize CodeDeploy agent and deployment logs in Amazon CloudWatch Logs instead of reviewing logs instance-by-instance, and automate monitoring wherever possible rather than relying on manual checks. [doc](https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring.html)
- **[Troubleshooting]** When an Auto Scaling–integrated deployment fails, disassociate the Auto Scaling group from the deployment group before troubleshooting to stop repeated instance launch/terminate cycles, then re-associate once the target revision is verified. [doc](https://aws.amazon.com/blogs/devops/under-the-hood-aws-codedeploy-and-auto-scaling-integration/)
- **[Compliance monitoring]** Use AWS Config rule `codedeploy-deployment-group-auto-rollback-enabled` to continuously verify that auto-rollback stays enabled across all deployment groups. [doc](https://docs.aws.amazon.com/config/latest/developerguide/codedeploy-deployment-group-auto-rollback-enabled.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
