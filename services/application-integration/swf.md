# Amazon SWF — Best Practices

## Common scenarios
- Coordinating long-running, multi-step business processes with human intervention steps        → Reliability, Operational Excellence
- Migrating legacy on-premises orchestration/decider-worker workloads to AWS        → Reliability, Performance Efficiency
- Fan-out processing pipelines (e.g., media encoding, image processing) with child workflows        → Performance Efficiency, Reliability
- New application development requiring workflow orchestration        → Cost Optimization, Operational Excellence

## 🔒 Security
- **[access control]** Use IAM identity-based policies scoped to specific domains and actions (with `swf:workflowType.name`/`swf:workflowType.version` condition keys where applicable) rather than granting broad SWF access — limits which domains and workflow/activity types a caller can invoke. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html)
- **[credentials]** Require human users and federated identities to authenticate via temporary credentials (IAM Identity Center or IAM roles) rather than long-term IAM user access keys — reduces the risk of leaked long-lived secrets. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-iam.html)
- **[worker exposure]** Keep workers and deciders behind your firewall and let them reach Amazon SWF only via outbound long-poll HTTP requests — avoids exposing any inbound endpoint for business logic. [doc](https://aws.amazon.com/swf/faqs/)
- **[network isolation]** Use an interface VPC endpoint (AWS PrivateLink) for workflows that must not traverse the public internet — keeps traffic between your VPC and Amazon SWF on the AWS network. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-vpc-endpoints.html)
- **[endpoint policy]** Attach an explicit VPC endpoint policy naming the allowed IAM principals, actions, and domains instead of the default full-access policy — narrows what a compromised host on that VPC can do against Amazon SWF. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-vpc-iam.html)

## 🛡️ Reliability
- **[task assignment]** Rely on Amazon SWF's built-in single-assignment guarantee for tasks instead of building custom locking or deduplication logic across multiple pollers — SWF ensures a task is never duplicated or given to more than one worker. [doc](https://aws.amazon.com/swf/faqs/)
- **[decision serialization]** Run multiple decider instances on the same task list for availability — Amazon SWF serializes decision tasks per workflow execution so concurrent deciders never operate on the same execution simultaneously. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-dev-deciders.html)
- **[history size]** Structure workflows so history stays under 10,000 events (well below the 25,000-event hard quota) and use `ContinueAsNew` or child workflows to restart long-running executions with a fresh history — a smaller history lets deciders fetch and process it faster. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html)
- **[scale-out polling]** Distribute pollers and scheduled tasks across multiple task lists as you approach the 1,000-poller or 2,000-tasks-per-second-per-task-list quotas — avoids `LimitExceededException` and `ACTIVITY_CREATION_RATE_EXCEEDED` errors. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html)
- **[timeouts]** Configure activity and workflow timeouts (schedule-to-start, start-to-close, schedule-to-close, heartbeat) sized to expected task duration — ensures stuck or failed workers are detected and retried instead of blocking the workflow indefinitely. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html)
- **[multi-AZ durability]** Depend on Amazon SWF's built-in replication of workflow execution history and state across multiple Availability Zones — removes the need to build your own state-replication layer for execution durability. [doc](https://aws.amazon.com/swf/faqs/)

## ⚡ Performance Efficiency
- **[long polling]** Use long polling (workers/deciders hold the connection open up to 60 seconds) instead of frequent short polling — reduces empty-poll overhead while still returning tasks with low latency. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-comm-proto.html)
- **[polling architecture]** Run each decider/worker poller in its own thread or process per task list rather than a single thread cycling through multiple task lists — prevents an idle task list's long-poll wait from delaying processing of a busy one. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-comm-proto.html)
- **[worker scaling]** Drive EC2 Auto Scaling for your activity-worker fleet using SWF's `StartToCloseTime`/`ScheduleToCloseTime` CloudWatch metrics — keeps worker capacity aligned with actual workflow/activity load instead of static provisioning. [doc](https://aws.amazon.com/blogs/aws/cloudwatch-metrics-for-simple-workflow/)
- **[task list sharding]** Split high-volume activity or decision workloads across multiple task lists — stays under per-task-list throughput quotas and improves parallel processing. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html)

## 💰 Cost Optimization
- **[polling efficiency]** Favor long polling over short polling — cuts the number of empty API calls against Amazon SWF, lowering request volume and the compute/network cost of running pollers. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dev-comm-proto.html)
- **[retention tuning]** Set the domain's workflow execution retention period (max 90 days) to the minimum your auditing/visibility needs require — avoids paying to retain execution history longer than necessary. [doc](https://aws.amazon.com/swf/faqs/)
- **[service choice]** Evaluate AWS Step Functions first for new workflow orchestration projects, reserving Amazon SWF for cases needing its decider/child-workflow model — avoids building and operating unnecessary custom decider infrastructure. [doc](https://aws.amazon.com/swf/faqs/)

## ⚙️ Operational Excellence
- **[monitoring]** Monitor Amazon SWF's built-in CloudWatch metrics (e.g., `DecisionTaskStartToCloseTime`, `WorkflowsCompleted`, `ScheduleToStartTime`) and alarm on threshold breaches — surfaces stuck deciders/workers or growing backlogs before they affect customers. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/cw-metrics.html)
- **[visibility]** Build monitoring and auto-scaling logic on the SWF visibility APIs (count/list open and closed executions) rather than relying solely on the console — supports mission-critical, high-volume execution fleets. [doc](https://aws.amazon.com/swf/faqs/)
- **[console observability]** Use the AWS Management Console to view and set alarms on workflow/activity metrics and inspect execution histories — gives operators a fast path for day-to-day triage without custom tooling. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/cw-metrics-console.html)
- **[framework choice]** Use the actively maintained Java Flow Framework or the raw SWF API for new decider development instead of the Ruby Flow Framework — the Ruby framework is no longer under active development and won't receive new features. [doc](https://docs.aws.amazon.com/amazonswf/latest/developerguide/resources.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
