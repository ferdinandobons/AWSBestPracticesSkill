# AWS X-Ray — Best Practices

## Common scenarios
- Tracing requests end-to-end across microservices to find latency bottlenecks        → Performance Efficiency, Operational Excellence
- Debugging errors and faults in distributed serverless or containerized applications        → Reliability, Operational Excellence
- Controlling trace volume and spend across high-traffic services        → Cost Optimization, Performance Efficiency
- Restricting who can view or configure traces, groups, and sampling rules        → Security

## 🔒 Security
- **[IAM]** Grant only `AWSXrayReadOnlyAccess` to users who need console/API read access to traces and service graphs, reserving write and configuration permissions for the roles that actually need them. [doc](https://docs.aws.amazon.com/xray/latest/devguide/security_iam_service-with-iam.html)
- **[IAM]** Use the managed `AWSXRayDaemonWriteAccess` policy (upload traces plus limited read for sampling rules) on the role attached to instrumented application resources, rather than granting `AWSXrayFullAccess` for daemon/agent workloads that only need to write. [doc](https://docs.aws.amazon.com/xray/latest/devguide/security_iam_service-with-iam.html)
- **[IAM]** Reserve `AWSXrayFullAccess` (or a custom policy with configuration APIs) for administrators who must manage encryption settings and sampling rules, since the read/write managed policies deliberately exclude those actions. [doc](https://docs.aws.amazon.com/xray/latest/devguide/security_iam_service-with-iam.html)
- **[Tag-based access]** Use `aws:RequestTag`/`aws:ResourceTag`/`aws:TagKeys` condition keys in identity-based policies to restrict who can create, modify, or delete X-Ray groups and sampling rules tagged for sensitive stages (e.g., `stage:prod`). [doc](https://docs.aws.amazon.com/xray/latest/devguide/security_iam_id-based-policy-examples.html)
- **[Encryption]** Configure X-Ray to use a customer-managed AWS KMS key instead of the default `aws/xray` AWS-managed key when you need auditability or the ability to disable the key for compliance reasons. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-encryption.html)
- **[Encryption]** Grant explicit key-usage permissions to callers when using a customer-managed KMS key for encryption, since the X-Ray read/write managed policies do not include KMS permissions. [doc](https://docs.aws.amazon.com/xray/latest/devguide/security_iam_service-with-iam.html)
- **[Networking]** Use a VPC endpoint (AWS PrivateLink) for X-Ray and attach an endpoint policy that allows only `PutTraceSegments` (denying read/configuration actions) so workloads in the VPC can send traces but cannot alter X-Ray configuration or read trace data. [doc](https://aws.amazon.com/blogs/mt/using-vpc-endpoints-for-aws-x-ray/)
- **[Least privilege]** Scope IAM policies for Kubernetes worker nodes or EC2 instances running the X-Ray daemon to only `xray:PutTraceSegments` and `xray:PutTelemetryRecords`, restricted to the specific instance profile or resource ARN. [doc](https://aws.amazon.com/blogs/compute/application-tracing-on-kubernetes-with-aws-x-ray/)

## 🛡️ Reliability
- **[Daemon deployment]** Run the X-Ray daemon (or ADOT/CloudWatch agent collector) as a sidecar container in ECS/EKS tasks so trace relaying is isolated from the main application container and doesn't compete for its resources. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html)
- **[Daemon deployment]** Ensure the X-Ray daemon or collector is running continuously on every host or task that emits traces — if it's down, segment data emitted by the SDK never reaches X-Ray. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html)
- **[Managed integrations]** Prefer AWS services with built-in X-Ray daemon management (Lambda active tracing, Elastic Beanstalk `XRayEnabled`) over self-managed daemons where available, to reduce operational surface area. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-services.html)
- **[Instrumentation coverage]** Instrument every server or endpoint in the application, and add custom subsegments for external systems that can't be auto-instrumented, so a single uninstrumented hop doesn't break end-to-end trace continuity. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/logging-monitoring-for-application-owners/x-ray.html)

## ⚡ Performance Efficiency
- **[Sampling]** Configure sampling rules based on service or request properties rather than relying only on the conservative default rate, so high-value requests (state-changing, transactional) are traced more and low-value high-volume requests (health checks, polling) are traced less. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html)
- **[Sampling]** Define and manage sampling rules centrally in the X-Ray console/API rather than per-application client-side JSON, since centrally managed rules apply consistently and can be updated without redeploying every service. [doc](https://aws.amazon.com/blogs/mt/dynamically-adjusting-x-ray-sampling-rules/)
- **[Adaptive sampling]** Use adaptive sampling (Sampling Boost and Anomaly Span Capture) to automatically raise sampling during anomalies or latency spikes and fall back afterward, so critical diagnostic data isn't missed under normal fixed-rate sampling. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-adaptive-sampling.html)
- **[Annotations]** Use annotations (indexed, max 50 per trace) for values you need to filter or group traces on, and use metadata (not indexed, up to the 64 KB segment limit) for additional context that doesn't need to be searchable. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html)
- **[Instrumentation overhead]** Evaluate the X-Ray SDK for your application's language and use its automatic instrumentation/client patches for downstream calls rather than hand-rolled tracing code, to minimize added complexity and overhead in business logic. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/implementing-logging-monitoring-cloudwatch/application-tracing-xray.html)

## 💰 Cost Optimization
- **[Sampling]** Keep the default conservative sampling rate (first request per second plus 5% of additional requests) or tune it lower for high-volume, low-value traffic to avoid tracing (and paying for) more requests than needed for visibility. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html)
- **[Adaptive sampling]** Use adaptive sampling's bounded, short-duration boosts (up to one minute) with automatic cooldown instead of permanently raising static sampling rates, so you only incur extra sampling cost during actual anomalies. [doc](https://aws.amazon.com/blogs/mt/adaptive-sampling-with-aws-x-ray-to-capture-critical-spans/)
- **[Sampling strategy]** Disable or reduce sampling for high-volume read-only or maintenance calls (health checks, background polling) while tracing state-changing or transaction requests fully, to control cost without losing visibility where it matters. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html)

## ⚙️ Operational Excellence
- **[Modernization]** Plan a migration path to OpenTelemetry-based instrumentation (ADOT) for new and existing applications, since the X-Ray SDKs and daemon entered maintenance mode (security fixes only) and new features are being built OpenTelemetry-first. [doc](https://aws.amazon.com/blogs/mt/aws-x-ray-sdks-daemon-migration-to-opentelemetry/)
- **[Grouping]** Use X-Ray groups with filter expressions to scope service graphs to specific applications or workflows, so teams can monitor performance and errors for their own services without noise from unrelated traces in the account. [doc](https://aws.amazon.com/blogs/developer/deep-dive-into-aws-x-ray-groups-and-use-cases/)
- **[Auditing]** Use the tagging and condition-key mechanisms on X-Ray groups and sampling rules to track and control configuration changes across teams and environments. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-tagging.html)
- **[Instrumentation strategy]** Determine which interface to use (X-Ray SDK, X-Ray API, ADOT, or CloudWatch Application Signals) up front based on your service's compute platform and long-term support needs, rather than mixing approaches ad hoc. [doc](https://docs.aws.amazon.com/xray/latest/devguide/xray-gettingstarted.html)

<!-- meta: last_reviewed=2026-07-05; sources=17 -->
