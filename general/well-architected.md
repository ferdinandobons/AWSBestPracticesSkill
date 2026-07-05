# AWS Well-Architected Framework — Best Practices

## Operational Excellence

- **[Change management]** Make infrastructure and application changes through automation rather than manual processes — this keeps changes to your infrastructure tracked and reviewable, reducing human error. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Workload design]** Design workloads with operations in mind so status and health are observable throughout the lifecycle — this increases the likelihood of business success by enabling effective event response and continuous improvement. [doc](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- **[Reviews]** Review workloads against the six pillars with the AWS Well-Architected Tool and save a milestone at each review — this creates a trail of architectural decisions through the application lifecycle. [doc](https://aws.amazon.com/blogs/mt/scaling-well-architected-reviews-with-the-aws-well-architected-tool/)
- **[Continuous improvement]** Update the improvement plan and re-measure the workload's risk profile after each round of changes — this shows the concrete effect of remediation on high- and medium-risk issues. [doc](https://docs.aws.amazon.com/wellarchitected/latest/userguide/tutorial.html)

## Security

- **[Identity foundation]** Implement least privilege, enforce separation of duties, centralize identity management, and eliminate reliance on long-term static credentials — this strengthens your identity foundation and reduces the blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Traceability]** Monitor, alert on, and audit actions and changes to your environment in real time and integrate log and metric collection with automated investigation — this maintains traceability across the workload. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Defense in depth]** Apply security controls at every layer, from network edge and VPC to compute, operating system, application, and code — this avoids reliance on any single control point. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Automation]** Define and manage security controls as code in version-controlled templates — this lets security mechanisms scale automatically as the workload grows. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Data protection]** Classify data into sensitivity levels and apply encryption, tokenization, and access control appropriate to each level, in transit and at rest — this ensures protection matches the actual risk of the data. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Data handling]** Use mechanisms and tooling to reduce or eliminate direct human access to sensitive data — this lowers the risk of mishandling or accidental modification. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Incident readiness]** Prepare incident management and investigation processes in advance and run incident-response simulations — this increases the speed of detection, investigation, and recovery when a real event occurs. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-design.html)
- **[Identity and access management]** Manage human and machine identities separately and grant permissions using least privilege, enforcing MFA and strong password requirements for human users — this ensures only the right identities have access under the right conditions. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-iam.html)
- **[Credential management]** Use temporary, limited-privilege credentials such as those issued by AWS STS or IAM Identity Center instead of long-term static credentials for programmatic access — this reduces the exposure window if credentials are leaked. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-iam.html)

## Reliability

- **[Automated recovery]** Monitor workloads for key performance indicators tied to business value and trigger automation when a threshold is breached — this enables automatic notification, tracking, and remediation of failures. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Recovery testing]** Use automation to simulate failures or recreate past failure scenarios and validate recovery procedures before an incident occurs — this exposes failure pathways you can fix ahead of a real outage. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Horizontal scaling]** Replace single large resources with multiple smaller ones and distribute requests across them — this reduces the impact of any single failure on the overall workload. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Capacity management]** Monitor demand and utilization and automate the addition or removal of resources to match it — this avoids the resource saturation and over-/under-provisioning that guessing capacity causes. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Change management]** Manage infrastructure changes, including changes to the automation itself, through automation — this keeps every change trackable and reviewable. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
- **[Fault isolation]** Build systems as multiple independent replicas and contain common failure modes to a single fault container — this lets you remove a failing replica from service without affecting customers. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/rapidly-recover-from-application-failures-in-a-single-az/)
- **[Recovery-oriented operations]** Prioritize recovering the application to a healthy state, such as removing a failing replica, before investigating root cause — this reduces mean time to recovery and limits customer impact. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/rapidly-recover-from-application-failures-in-a-single-az/)

## Performance Efficiency

- **[Managed technology]** Consume advanced technologies such as NoSQL databases, media transcoding, and machine learning as managed services rather than operating them yourself — this frees your team to focus on product development instead of resource provisioning. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- **[Global reach]** Deploy workloads across multiple AWS Regions around the world — this provides lower latency and a better experience for globally distributed customers at minimal cost. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- **[Serverless]** Prefer serverless architectures over managing physical servers for compute and hosting — this removes operational burden and can lower transactional cost at cloud scale. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- **[Experimentation]** Use virtual, automatable resources to run comparative tests across instance types, storage, and configurations — this lets you validate performance choices before committing to a design. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- **[Resource selection]** Choose the technology approach that best matches your data access patterns, such as database or storage type — this aligns the underlying mechanics with how the workload actually reads and writes data. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- **[Data-driven design]** Gather data across the architecture, from high-level design to resource configuration, and revisit choices on a cyclical basis — this keeps the workload aligned with continually evolving AWS services. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)

## Cost Optimization

- **[Financial management]** Invest dedicated time and resources into Cloud Financial Management capability — this builds the knowledge, programs, and processes needed to run a cost-efficient organization. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html)
- **[Consumption model]** Pay only for the computing resources you consume and stop non-production resources, such as dev/test environments, when they are not in use — this scales spend directly with actual usage. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html)
- **[Efficiency measurement]** Measure the business output of a workload against its delivery cost — this shows the gains from increased output, added functionality, or reduced cost. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html)
- **[Managed services]** Offload undifferentiated heavy lifting, such as data center operations and OS management, to AWS managed services — this lets your team focus on customers and the business instead of IT infrastructure. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html)
- **[Cost attribution]** Analyze and attribute expenditure accurately to workloads and owners — this enables measuring ROI and gives workload owners the ability to optimize their own resources. [doc](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/design-principles.html)

## Sustainability

- **[Impact measurement]** Measure and model the environmental impact of a cloud workload across its full lifecycle, including customer use and eventual decommissioning — this lets you establish KPIs and evaluate ways to reduce impact. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html)
- **[Sustainability goals]** Set long-term, per-workload sustainability goals, such as reduced compute or storage per transaction, and plan for growth — this ensures scaling reduces impact intensity per unit rather than increasing it. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html)
- **[Utilization]** Right-size workloads and eliminate idle resources to maximize hardware utilization — a single host running at higher utilization is more energy-efficient than multiple underutilized hosts due to baseline power draw. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html)
- **[Region selection]** Choose AWS Regions with lower carbon intensity and size resources to actual workload needs — this reduces environmental impact compared with over-provisioning for uptime margin. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html)
- **[Efficient technology adoption]** Continually monitor and adopt new, more efficient hardware and software offerings, and design for flexibility — this allows rapid adoption of upstream efficiency improvements from AWS and partners. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html)

## Common scenarios

- Starting a new workload review: use the AWS Well-Architected Tool to define the workload, answer the pillar questions, and generate an improvement plan before build-out begins.
- Preparing for a compliance or audit cycle: run a Well-Architected review focused on the Security and Reliability pillars and save a milestone to document the state at time of audit.
- Reducing a growing AWS bill: revisit the Cost Optimization pillar's consumption model and cost-attribution practices to identify idle or oversized resources before purchasing commitments.
- Expanding to new geographies: apply the Performance Efficiency pillar's global-deployment guidance alongside the Sustainability pillar's Region carbon-intensity guidance.

<!-- meta: last_reviewed=2026-07-05; sources=10 -->
