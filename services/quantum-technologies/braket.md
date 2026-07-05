# Amazon Braket — Best Practices

## Common scenarios
- Prototyping and debugging quantum circuits before spending on QPU time        → Cost Optimization, Performance Efficiency
- Running iterative hybrid quantum-classical algorithms (VQE, QAOA, QML)        → Reliability, Performance Efficiency, Cost Optimization
- Restricting which users/teams can access specific QPUs, notebooks, or S3 result buckets        → Security, Operational Excellence
- Tracking and capping spend on quantum tasks and hybrid jobs across teams        → Cost Optimization, Operational Excellence

## 🔒 Security
- **[IAM]** Apply least-privilege IAM policies scoped to specific S3 buckets, devices, or actions rather than granting `AmazonBraketFullAccess` broadly — least privilege prevents users from exceeding the access needed for their quantum tasks. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-terms.html)
- **[IAM]** Use IAM roles instead of long-lived credentials when access to Braket resources is only needed temporarily, such as for notebook execution or hybrid job runs. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-terms.html)
- **[IAM]** Attach deny-permissions policies to restrict specific IAM roles from creating quantum tasks (`CreateQuantumTask`), hybrid jobs (`CreateJob`), or reading device details (`GetDevice`) on specified QPUs when access to certain hardware should be limited. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/restrict-access.html)
- **[S3]** Scope IAM policies to the specific `amazon-braket-*` S3 buckets a user needs rather than all buckets in the account, and apply bucket policies to further control access to stored quantum task results. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-manage-access.html)
- **[Networking]** Use Amazon VPC endpoints (AWS PrivateLink) to access Braket from within your VPC without traffic traversing the public internet, reducing exposure to internet-based attacks. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-privatelink.html)
- **[Networking]** Attach a scoped IAM endpoint policy to your VPC endpoint that specifies the exact Braket actions, principals, and resources allowed, instead of leaving it open to all actions. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-privatelink.html)
- **[Networking]** Require clients to support TLS 1.2 (and prefer TLS 1.3) with perfect-forward-secrecy cipher suites (DHE/ECDHE) when calling Braket APIs. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/infrastructure-security.html)
- **[Data protection]** Never place confidential or sensitive information in tags or free-form text fields (such as task or job names), since this data may surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/security.html)
- **[Data protection]** Enable AWS CloudTrail logging with individual IAM users/roles and multi-factor authentication so all API and console activity against Braket is attributable and auditable. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/security.html)
- **[Data protection]** Use a FIPS endpoint if your workload requires FIPS 140-3 validated cryptographic modules when accessing Braket via CLI or API. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/security.html)

## 🛡️ Reliability
- **[Hybrid Jobs]** Debug and validate algorithm logic on a simulator (e.g. SV1) or in local mode before submitting to a QPU, to catch errors cheaply and avoid wasting queued QPU time. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-hybrid-job-decorator.html)
- **[Hybrid Jobs]** Checkpoint intermediate state periodically for long-running hybrid jobs so progress can be recovered rather than restarting the full iterative algorithm after an interruption. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-hybrid-job-decorator.html)
- **[Hybrid Jobs]** Use Hybrid Jobs (rather than standalone tasks issued from your own environment) for iterative variational algorithms that depend on prior quantum results, since quantum tasks from a job get priority queueing on the target QPU and more predictable runtimes. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)
- **[Hybrid Jobs]** Package software and dependencies in a Bring-Your-Own-Container (BYOC) image to make hybrid job execution reproducible and avoid dependency/version drift between runs. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-hybrid-job-decorator.html)
- **[Queueing]** Check device queue depth and queue position via the SDK or console before submitting quantum tasks or hybrid jobs, to anticipate wait time on a given QPU. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-task-when.html)

## ⚡ Performance Efficiency
- **[Simulators]** Match the simulator to the workload: SV1 for full state-vector simulation up to 34 qubits, DM1 for noise simulation up to ~16-17 qubits, or TN1 for higher-entanglement circuits up to 50 qubits. [doc](https://aws.amazon.com/braket/getting-started/)
- **[Hybrid Jobs]** Use built-in MPI support to run local simulators across multiple instances within a single hybrid job when simulating large numbers of circuits. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-hybrid-job-decorator.html)
- **[Hybrid Jobs]** Use parametric circuits submitted from a hybrid job, since certain QPUs automatically apply parametric compilation to improve algorithm runtimes. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-hybrid-job-decorator.html)
- **[Task submission]** Batch related circuits into a single program set (single task with multiple executables) instead of submitting many individual tasks, cutting per-circuit overhead and total runtime. [doc](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-introduces-program-sets-enabling-customers-to-run-quantum-programs-up-to-24x-faster/)
- **[Concurrency]** Exploit on-demand simulators' support for concurrent circuit execution (e.g. SV1 supports up to 100 concurrent circuits) by splitting large batches of tasks to run in parallel instead of sequentially. [doc](https://aws.amazon.com/blogs/quantum-computing/exact-simulation-of-quantum-enhanced-signature-kernels-for-financial-data-streams-prediction-using-amazon-braket/)

## 💰 Cost Optimization
- **[Cost tracking]** Instrument notebooks and hybrid jobs with the Braket SDK `Tracker()` utility to get near-real-time estimated cost for QPU shots/tasks and simulator duration before costs accrue. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-pricing.html)
- **[Budgets]** Set per-QPU spending limits and configure budget notifications so quantum experiment costs cannot silently exceed allocated budgets. [doc](https://aws.amazon.com/blogs/quantum-computing/introducing-a-cost-control-solution-for-amazon-braket/)
- **[Governance]** For teams or grant-funded accounts, use the open-source Braket cost-control solution to automatically revoke quantum-task-creation permissions from specific IAM users/groups/roles once a configured spend threshold is reached. [doc](https://aws.amazon.com/blogs/quantum-computing/introducing-a-cost-control-solution-for-amazon-braket/)
- **[Task submission]** Combine multiple circuits into a single program set rather than submitting them as separate tasks — this collapses the per-task fee into one charge and can meaningfully reduce total cost for large batches. [doc](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-introduces-program-sets-enabling-customers-to-run-quantum-programs-up-to-24x-faster/)
- **[Hybrid Jobs]** Prefer Hybrid Jobs for iterative algorithms so classical compute resources are automatically released after completion, avoiding charges for idle instances left running in a self-managed environment. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)
- **[Reservations]** Use Braket Direct reserved device access (billed hourly) instead of per-task/per-shot pricing for workloads with heavy, sustained QPU usage where reservation hours are more cost-efficient than incremental task fees. [doc](https://aws.amazon.com/braket/pricing/)

## ⚙️ Operational Excellence
- **[Monitoring]** Monitor Braket workloads with Amazon CloudWatch metrics and enable EventBridge notifications to be alerted automatically when quantum tasks or hybrid jobs complete, instead of polling. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-monitor-metrics.html)
- **[Auditing]** Enable AWS CloudTrail trails for Braket to capture a full record of API calls (who, when, from where) for governance and incident investigation, since event history alone only retains recent events. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-ctlogs.html)
- **[Auditing]** Use CloudTrail-delivered EventBridge events (`source: aws.braket`) to build automated reactions to specific Braket API calls, such as alerting on spending-limit changes. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-braket.html)
- **[Access control]** Restrict which notebook instances, devices, and S3 buckets individual users can reach by attaching scoped IAM policies rather than relying on the broad `AmazonBraketFullAccess` managed policy in shared/multi-team accounts. [doc](https://docs.aws.amazon.com/braket/latest/developerguide/braket-manage-access.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
