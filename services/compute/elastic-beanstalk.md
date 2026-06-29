# AWS Elastic Beanstalk - Best Practices

## Common scenarios
- Production web app needing high availability across multiple Availability Zones -> reliability
- Hardening a default environment for a production security posture (network, encryption) -> security
- Reducing spend on always-on or non-production environments -> cost optimization
- Safe, zero-downtime deployments and automated platform patching -> operational excellence

## 🔒 Security
- **[IAM]** Implement least-privilege access by customizing the managed instance profile, service role, and user policies to only the permissions your workload needs - reduces blast radius from errors or compromise. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security-best-practices.html)
- **[secrets]** Retrieve credentials and API keys at runtime from AWS Secrets Manager or SSM Parameter Store instead of hardcoding them, and never log sensitive values - keeps secrets out of source and log files. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security-best-practices.html)
- **[instance metadata]** Enforce IMDSv2 on environment instances and disable IMDSv1 - session-oriented requests mitigate SSRF and other metadata-access vulnerabilities. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security-best-practices.html)
- **[network]** Place EC2 instances in private subnets and keep only the load balancer in public subnets, using a NAT gateway for outbound calls - instances stay unreachable directly from the internet. [doc](https://aws.amazon.com/blogs/security/hardening-the-security-of-your-aws-elastic-beanstalk-application-the-well-architected-way/)
- **[encryption in transit]** Terminate HTTPS/TLS 1.2+ at the load balancer with an ACM certificate and enable automatic renewal - protects client traffic and removes manual certificate rotation. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html)
- **[encryption at rest]** Encrypt the environment's S3 log/source bucket and create the RDS database directly in RDS with encryption enabled (Beanstalk-created DBs aren't encrypted) - protects data at rest. [doc](https://aws.amazon.com/blogs/security/hardening-the-security-of-your-aws-elastic-beanstalk-application-the-well-architected-way/)
- **[detection]** Track impactful API calls (UpdateEnvironment, TerminateEnvironment) with CloudTrail and enable AWS Config rules to flag noncompliant resources - surfaces security violations after they occur. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security-best-practices.html)

## 🛡️ Reliability
- **[high availability]** Run a load-balanced environment with the Auto Scaling group minimum set to at least 2 instances across multiple Availability Zones - removes the single point of failure and survives an AZ outage. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/nodejs-dynamodb-tutorial.html)
- **[fault tolerance]** Plan for N+1 capacity spread across AZs and let Auto Scaling replace unhealthy instances automatically - keeps serving traffic when an instance or zone fails. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.html)
- **[statelessness]** Design applications as stateless and store persistent data in S3, RDS, DynamoDB, or EFS rather than instance local disk - instances come and go with scaling and failures, so local storage is lost. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html)
- **[data durability]** Decouple the RDS database from the environment lifecycle (Retain deletion policy) so it persists when the environment is terminated - avoids losing your database on environment teardown. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html)
- **[deployments]** Use immutable deployments for production to launch new instances in a separate Auto Scaling group with quick, safe rollback - prevents issues from partially completed rolling deployments. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html)
- **[async work]** For worker environments, monitor the SQS dead-letter queue and alarm on it to isolate and investigate messages that repeatedly fail processing - prevents silent loss of background tasks. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html)

## ⚡ Performance Efficiency
- **[scaling]** Configure Auto Scaling triggers on metrics such as CPU, network I/O, or request load so capacity is added and removed automatically as demand fluctuates - aligns capacity with demand without over-provisioning. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html)
- **[content delivery]** Front static assets and media with Amazon CloudFront backed by S3 - edge caching routes users to the nearest location and reduces latency. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html)
- **[canary]** Use traffic-splitting deployments to send a percentage of traffic to the new version for an evaluation period before shifting all traffic - validates performance and health before full cutover. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)

## 💰 Cost Optimization
- **[purchasing]** Enable EC2 Spot Instances (with a mix of On-Demand base capacity) for stateless, fault-tolerant, or test/dev workloads - Spot capacity is available at a steep discount versus On-Demand. [doc](https://aws.amazon.com/blogs/devops/optimizing-the-cost-of-running-aws-elastic-beanstalk-workloads/)
- **[Spot resilience]** Use the price-capacity-optimized allocation strategy and enable Capacity Rebalancing - chooses pools with the lowest interruption risk and proactively replaces Spot instances before they're reclaimed. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-autoscaling-spot-allocation-strategy.html)
- **[non-prod schedule]** Terminate test and staging environments outside working hours and rebuild them on schedule, after decoupling RDS so the database survives - stops paying for idle environments overnight. [doc](https://aws.amazon.com/blogs/devops/optimizing-the-cost-of-running-aws-elastic-beanstalk-workloads/)
- **[shared infrastructure]** Share a single Application Load Balancer across multiple environments instead of a dedicated ALB per environment - cuts the running cost of load balancers. [doc](https://aws.amazon.com/blogs/containers/amazon-elastic-beanstalk-introduces-support-shared-load-balancers/)

## ⚙️ Operational Excellence
- **[patching]** Enable managed platform updates to apply patch and minor platform versions automatically during a weekly maintenance window with zero downtime - keeps the OS, runtime, and components current without manual effort. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-platform-update-managed.html)
- **[health]** Enable enhanced health reporting so the on-instance health agent evaluates logs and system metrics and surfaces severity and likely causes - enables faster response and safer deployment roll-out decisions. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced.html)
- **[monitoring]** Set CloudWatch alarms on key Elastic Beanstalk and custom application metrics, and stream enhanced health metrics to CloudWatch for historical tracking - gives visibility to detect and act on degradation. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security-best-practices.html)
- **[zero downtime]** Choose a deployment policy that avoids full downtime (rolling, rolling with additional batch, or immutable) according to your availability needs rather than the default all-at-once - prevents loss of service during updates. [doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html)

<!-- meta: last_reviewed=2026-06-29; sources=14 -->
