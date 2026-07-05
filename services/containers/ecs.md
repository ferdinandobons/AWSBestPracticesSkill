# Amazon ECS — Best Practices

## Common scenarios
- Running microservices with per-service scaling and isolation        → Reliability, Cost Optimization
- Deploying containers on serverless compute without managing servers        → Operational Excellence, Cost Optimization
- Migrating containerized workloads that need mission-critical high availability        → Reliability, Security
- Batch or interruption-tolerant containerized jobs        → Cost Optimization, Performance Efficiency

## 🔒 Security
- **[IAM]** Enforce least privilege on ECS resource policies — use resource-level permissions so only specific roles can act on specific clusters/task definition families. [doc](https://aws.amazon.com/blogs/security/security-considerations-for-running-containers-on-amazon-ecs/)
- **[IAM]** Give each task definition family its own task role instead of sharing roles — limits blast radius so a compromised service can't reach another service's resources. [doc](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/application.html)
- **[IAM]** Separate the task execution role from the task role — the execution role lets ECS pull images/write logs/read secrets, the task role is used by application code; never merge their permissions. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-ecs-iam-role-overview.html)
- **[IAM]** Audit ECS API access continuously with AWS CloudTrail and remove unused IAM users, roles, and groups. [doc](https://aws.amazon.com/blogs/security/security-considerations-for-running-containers-on-amazon-ecs/)
- **[Secrets]** Store API keys, database credentials, and other secret material in Secrets Manager or encrypted Systems Manager Parameter Store parameters — never in environment variables in plaintext or baked into images. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html)
- **[Secrets]** Prefer Secrets Manager over Parameter Store when you need automatic rotation, generated random secrets, or cross-account sharing. [doc](https://aws.amazon.com/blogs/security/security-considerations-for-running-containers-on-amazon-ecs/)
- **[Network]** Use the `awsvpc` network mode so each task gets its own elastic network interface and can be assigned its own security group — this is the only mode that supports task-level security groups and is required for Fargate. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-network.html)
- **[Network]** Isolate strictly-separated workloads into different VPCs, and use AWS PrivateLink interface endpoints for ECS and ECR when tasks run in environments without internet egress. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-network.html)
- **[Network]** Encrypt traffic in transit — terminate TLS with SNI-enabled ALB/NLB listeners using ACM certificates, or implement end-to-end TLS to the container for sensitive workloads. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-network.html)
- **[Network]** Enable VPC Flow Logs on subnets running long-lived tasks to analyze and audit network traffic patterns. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-network.html)
- **[Container image]** Build minimal or distroless images, and use multi-stage Docker builds to strip build tools and unnecessary binaries, reducing the attack surface. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Container image]** Scan container images for vulnerabilities (e.g., Amazon ECR native scanning) on every push, and rebuild or delete images with HIGH/CRITICAL findings. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Container image]** Enable immutable image tags in Amazon ECR so a tag can never be overwritten with a different (potentially compromised) image. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Container image]** Encrypt images pushed to Amazon ECR with a customer managed KMS key when the default AWS-managed key doesn't meet your compliance needs. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Runtime]** Run containers as a non-root user by setting the `USER` directive, and lint Dockerfiles in CI/CD to fail builds missing it. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Runtime]** Use a read-only root filesystem on containers and explicitly define writable mount points, reducing what an attacker can tamper with at runtime. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Runtime]** Avoid running containers as `privileged` on EC2 launch type, and set the container agent's `ECS_DISABLE_PRIVILEGED` variable to `true` where privileged mode isn't required. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Runtime]** Drop unnecessary Linux capabilities from containers beyond Docker's default set to shrink the effective permissions available if a container is compromised. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)

## 🛡️ Reliability
- **[High availability]** Spread tasks across at least three Availability Zones where possible — this delivers a better availability/cost trade-off than two AZs and matches the pattern ECS itself uses internally. [doc](https://aws.amazon.com/blogs/containers/amazon-ecs-availability-best-practices/)
- **[High availability]** Enable Availability Zone rebalancing for multi-task services so ECS automatically redistributes tasks after an AZ disruption or imbalance, without manual intervention. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-rebalancing.html)
- **[Capacity]** Over-provision capacity with headroom (targeting roughly 60–80% utilization) so autoscaling latency doesn't cause saturation during traffic bursts or AZ failover. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/capacity-availability-best-practice.html)
- **[Deployment]** Design application shutdown to handle `SIGTERM` gracefully — stop accepting new work and finish or checkpoint in-flight work before ECS sends `SIGKILL`. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-considerations.html)
- **[Deployment]** Run a single application process per container so the container lifecycle matches the process lifecycle, letting ECS reliably detect and replace crashed processes. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-considerations.html)
- **[Deployment]** Tag container images with unique, immutable identifiers (e.g., git SHA) rather than relying on `latest`, so rollbacks target a known-good, reproducible image. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-considerations.html)

## ⚡ Performance Efficiency
- **[Sizing]** Size Fargate tasks by summing container-level CPU/memory reservations and rounding up to the nearest supported Fargate task size, rather than over-allocating arbitrarily. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-size-best-practice.html)
- **[Sizing]** Set explicit CPU and memory limits on EC2-launch-type tasks so no single task can starve others of shared host resources. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
- **[Autoscaling]** Use Application Auto Scaling with CloudWatch (or Prometheus) metrics such as CPU/memory utilization, or custom metrics like queue depth or request count, to scale ECS services to match demand. [doc](https://aws.amazon.com/ecs/faqs/)
- **[Cluster scaling]** On EC2 launch type, use ECS cluster auto scaling with capacity providers so ECS manages Auto Scaling group capacity automatically to meet task demand. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/capacity-cluster-speed-up-ec2.html)

## 💰 Cost Optimization
- **[Compute]** Use Fargate Spot for interruption-tolerant workloads to run tasks on spare capacity at a steep discount versus standard Fargate pricing. [doc](https://aws.amazon.com/blogs/compute/deep-dive-into-fargate-spot-to-run-your-ecs-tasks-for-up-to-70-less/)
- **[Compute]** Define a capacity provider strategy that blends FARGATE and FARGATE_SPOT (or multiple EC2 capacity providers) with base and weight settings to balance cost savings against availability requirements. [doc](https://aws.amazon.com/blogs/containers/optimizing-amazon-elastic-container-service-for-cost-using-scheduled-scaling/)
- **[Right-sizing]** Regularly right-size task and container CPU/memory using recommendations (e.g., from Compute Optimizer) instead of leaving tasks over-provisioned. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/optimizer-ecs-fargate.html)
- **[Scaling]** Avoid excessive over-provisioning for burst absorption beyond your actual availability requirements — headroom has a direct cost trade-off, so size it to your real SLOs rather than by default. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/capacity-availability-best-practice.html)

## ⚙️ Operational Excellence
- **[Observability]** Enable CloudWatch Container Insights with enhanced observability to get task/container-level metrics, correlate logs with deployments, and speed up root-cause analysis. [doc](https://aws.amazon.com/blogs/aws/container-insights-with-enhanced-observability-now-available-in-amazon-ecs/)
- **[Observability]** Configure containerized applications to write logs to `stdout`/`stderr` and route them via the `awslogs` driver to CloudWatch Logs, decoupling log handling from application code. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-considerations.html)
- **[Monitoring]** Establish a monitoring baseline (CPU/memory reservation and utilization at cluster, service, and task levels) before defining alarms, so scaling and alerting thresholds reflect real steady-state behavior. [doc](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_monitoring.html)
- **[CI/CD]** Automate ECS deployments through a CI/CD pipeline rather than manual console changes, limiting direct human write-access to clusters and task definitions. [doc](https://aws.amazon.com/blogs/security/security-considerations-for-running-containers-on-amazon-ecs/)
- **[Architecture]** Split unrelated business components into separate task definition families (each with its own IAM role) instead of one large task definition, so services can be scaled, deployed, and secured independently. [doc](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/application.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
