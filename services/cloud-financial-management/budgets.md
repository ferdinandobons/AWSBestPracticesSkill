# AWS Budgets — Best Practices

## Common scenarios
- Alerting on actual or forecasted spend overruns for an account or team        → Cost Optimization, Operational Excellence
- Enforcing automated guardrails (deny policies, SCPs, stopping instances) when spend thresholds are breached        → Cost Optimization, Security, Reliability
- Tracking Reserved Instance / Savings Plans utilization and coverage        → Cost Optimization
- Monitoring multi-account or organization-wide budgets that change as OUs and accounts move        → Operational Excellence, Cost Optimization

## 🔒 Security
- **[access control]** Grant users only the specific billing, CloudWatch, and SNS permissions needed to create budgets rather than broad access — least-privilege console access reduces the risk of unauthorized budget or notification changes. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[programmatic access]** Create a dedicated IAM role for programmatic (API) access to Budgets, separate from console users — this lets you define distinct, more precise access boundaries between console and API callers. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[budget actions]** Use the AWS managed policies (for the user and for the Budgets service role) when configuring budget actions instead of hand-rolled policies — AWS keeps these updated as new budget-action capabilities ship, avoiding stale or broken permissions. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[service role]** Scope the IAM service role that Budgets assumes to only the resource-control actions (IAM/SCP application, or targeting specific EC2/RDS instances) it actually needs to execute. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-action-role.html)
- **[SNS notifications]** Restrict the SNS topic access policy for budget alerts with `aws:SourceAccount` and `aws:SourceArn` conditions scoped to your account's budgets, rather than an open `Resource: "*"` publish grant. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-sns-policy.html)
- **[governance]** Tag budgets and use resource- and tag-based IAM policies to scope who can view, edit, or delete specific budgets — this improves governance and auditability for multi-team environments. [doc](https://aws.amazon.com/about-aws/whats-new/2024/05/aws-budgets-resource-tag-based-access-controls/)

## 🛡️ Reliability
- **[Auto Scaling interaction]** Don't rely solely on a budget action that stops EC2 instances inside an Auto Scaling Group — the ASG will relaunch replacement instances, so pair it with a second action that removes the IAM permissions used by the launch configuration/template if you need the stop to hold. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[custom period budgets]** Regularly review and extend end dates on custom period budgets — they do not auto-renew and expire silently, which stops monitoring without any notification. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[organizational changes]** Review and update budget thresholds when a member account leaves an AWS Organization — tracking behavior changes (only post-departure costs are tracked) without any notification being sent. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[SNS delivery]** Confirm the Amazon SNS subscription for budget notifications and keep the topic in the same account as the budget — cross-account SNS delivery for budget alerts isn't supported and unconfirmed subscriptions silently drop notifications. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-sns-policy.html)

## 💰 Cost Optimization
- **[recurring budgets]** Prefer recurring (monthly/quarterly/annual) budgets over fixed time-frame budgets so you don't unexpectedly stop receiving alerts after the period ends. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[custom period alignment]** Align custom period budgets to your actual billing cycle, fiscal year, project duration, or grant period, and combine them with recurring budgets for comprehensive coverage rather than relying on one budget type alone. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[forecast alerts]** Account for the ~5 weeks of usage history AWS needs before forecast-based alerts trigger, and note forecasting for custom period budgets only becomes active within 12 months of the end date — don't depend on forecast alerts firing immediately on a new budget. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[cost dimensions]** Choose the appropriate cost aggregation (blended, unblended, net unblended, amortized, net amortized) and include/exclude refunds, credits, taxes, and support charges deliberately so the budget reflects the cost view your organization actually manages to. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[guardrails]** Use budget actions (deny IAM policies, SCPs, or stopping targeted EC2/RDS instances) at forecasted or actual thresholds to automatically enforce spend limits instead of relying on alerts alone for critical accounts. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html)
- **[RI/Savings Plans tracking]** Set daily utilization or coverage budgets for Reserved Instances and Savings Plans and alert when utilization drops below your target so unused commitments are caught quickly. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- **[baseline monitoring]** Start with a total monthly cost budget to establish baseline monitoring, then layer more granular budgets (by service, linked account, or tag) once usage patterns are understood. [doc](https://aws.amazon.com/solutions/guidance/cloud-financial-management-on-aws/)

## ⚙️ Operational Excellence
- **[update cadence]** Design alerting expectations around the Budgets data refresh cadence (billing data updated at least once, typically up to three times, per day) rather than expecting near-real-time notification. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
- **[reporting]** Configure AWS Budgets Reports to deliver a consolidated view of up to 50 budgets on a daily, weekly, or monthly cadence to stakeholders instead of requiring manual dashboard checks. [doc](https://aws.amazon.com/solutions/guidance/cloud-financial-management-on-aws/)
- **[notification routing]** Route budget alerts through an SNS topic (in addition to email) to integrate with chat tools, ticketing systems, or other automated workflows for faster response. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-sns-policy.html)
- **[tagging]** Tag budgets consistently by team, business unit, or environment to simplify auditing and management as the number of budgets grows across an organization. [doc](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)

<!-- meta: last_reviewed=2026-07-05; sources=7 -->
