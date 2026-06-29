# Amazon EC2 Auto Scaling - Best Practices

## Common scenarios
- Variable or spiky web traffic where capacity must follow the demand curve -> performance, cost
- High-availability fleets that must survive instance and Availability Zone failures -> reliability
- Cost-sensitive, fault-tolerant workloads blending Spot and On-Demand capacity -> cost
- Immutable deployments rolling out new AMIs or launch templates across a fleet -> operational excellence

## 🔒 Security
- **[Least privilege]** Scope IAM policies to specific `autoscaling` actions and use tag-based conditions (for example `autoscaling:ResourceTag/purpose`) rather than broad wildcards - limits who can modify Auto Scaling groups. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/security_iam_id-based-policy-examples.html)
- **[Launch template control]** Restrict who can create and update launch templates and select AMIs to the team responsible for OS and application hardening - enforces change control over the baseline image used by every instance. [doc](https://aws.amazon.com/blogs/publicsector/documenting-the-use-of-amazon-ec2-auto-scaling-groups-in-dod/)
- **[Data protection]** Set up individual identities with IAM Identity Center or IAM, enforce MFA, and require TLS 1.2+ for API calls - protects account credentials and data in transit. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-data-protection.html)
- **[No secrets in metadata]** Never put confidential information into tags or free-form name fields, since that data can surface in billing and diagnostic logs - avoids leaking sensitive values. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-data-protection.html)
- **[Audit]** Enable AWS CloudTrail to log Auto Scaling API and user activity - gives an audit trail of who changed scaling configuration. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-data-protection.html)

## 🛡️ Reliability
- **[Multi-AZ]** Span the Auto Scaling group across multiple Availability Zones and keep at least one instance in each - benefits from geographic redundancy so the group fails over between zones without interruption. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/disaster-recovery-resiliency.html)
- **[Health checks]** Enable and correctly configure Elastic Load Balancing health checks on the group so unhealthy instances are detected and replaced - keeps traffic flowing only to healthy instances. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/disaster-recovery-resiliency.html)
- **[Cross-zone load balancing]** Attach a load balancer and keep cross-zone load balancing enabled so each instance gets similar traffic - limits the impact of load on remaining instances during a failover event. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/disaster-recovery-resiliency.html)
- **[Custom health checks]** Add application-specific custom health checks for conditions the built-in EC2 and ELB checks miss - replaces instances that are running but not truly serving. [doc](https://aws.amazon.com/blogs/compute/how-to-create-custom-health-checks-for-your-amazon-ec2-auto-scaling-fleet/)
- **[Spot resilience]** Enable Capacity Rebalancing to proactively replace Spot Instances that receive a rebalance recommendation before they are interrupted - maintains availability instead of waiting for a failed health check. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html)

## ⚡ Performance Efficiency
- **[Dynamic scaling]** Use dynamic scaling with target tracking policies on a valid utilization metric instead of manual scaling - keeps the group following the demand curve automatically. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_compute_hardware_scale_compute_resources_dynamically.html)
- **[Right metric]** Pick a scaling metric that increases or decreases proportionally to the number of instances, using a custom metric (such as queue depth) when CPU is not representative - avoids scaling on a signal that does not reflect load. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_compute_hardware_scale_compute_resources_dynamically.html)
- **[Predictive scaling]** For cyclical traffic and slow-booting apps, add predictive scaling alongside dynamic scaling to launch capacity ahead of forecasted load - scales faster than reactive policies alone. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html)
- **[Instance warmup]** Set a default instance warmup so newly launched instances are not counted or measured until they stabilize - prevents unpredictable scaling from startup metric spikes. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html)
- **[Warm pools]** Use a warm pool for applications with long boot times so pre-initialized instances are ready to enter service quickly - reduces scale-out latency. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html)

## 💰 Cost Optimization
- **[Mixed instances]** Combine On-Demand and Spot Instances in one group, using Reserved Instances or Savings Plans for baseline load - optimizes cost while meeting scale and performance needs. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html)
- **[Spot allocation]** Use the `price-capacity-optimized` allocation strategy and avoid `lowest-price` - selects Spot pools that are both cheap and least likely to be interrupted. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/allocation-strategies.html)
- **[Instance flexibility]** Be flexible across at least 10 instance types per workload, including earlier generations - gives Auto Scaling more Spot pools to draw from and reduces interruptions. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/mixed-instances-groups-set-up-overview.html)
- **[Scheduled scaling]** Use scheduled actions for predictable, time-based load changes so capacity is added before peaks and removed afterward - avoids over-provisioning during quiet periods. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html)

## ⚙️ Operational Excellence
- **[Immutable updates]** Use instance refresh to roll out new AMIs or launch templates in a rolling fashion, with a canary phase to test on a small set first - releases updates without custom replacement scripts. [doc](https://aws.amazon.com/blogs/compute/introducing-instance-refresh-for-ec2-auto-scaling/)
- **[Lifecycle hooks]** Define lifecycle hooks to run custom actions as instances launch or terminate, such as bootstrapping or draining logs before shutdown - manages instances cleanly through their lifecycle. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html)
- **[Group metrics]** Enable Auto Scaling group metrics collection (1-minute granularity, no extra charge) and set CloudWatch alarms on them - gives visibility into capacity changes and scaling behavior. [doc](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-metrics.html)
- **[Configuration as code]** Manage Auto Scaling groups and launch templates via Infrastructure as Code and patch the base AMI rather than individual instances - keeps the fleet on a standardized, reproducible image. [doc](https://aws.amazon.com/blogs/publicsector/documenting-the-use-of-amazon-ec2-auto-scaling-groups-in-dod/)

<!-- meta: last_reviewed=2026-06-29; sources=18 -->
