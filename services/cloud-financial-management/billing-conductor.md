# AWS Billing Conductor — Best Practices

## Common scenarios
- AWS Partner chargeback for resold AWS usage to end customers        → Cost Optimization, Security
- Internal showback/chargeback of cloud costs to business units or subsidiaries        → Cost Optimization, Operational Excellence
- Custom pricing plans and markups/discounts for billing groups        → Cost Optimization
- Multi-level billing transfer for distributors and downstream sellers        → Reliability, Operational Excellence

## 🔒 Security
- **[access control]** Restrict AWS Billing Conductor access to the payer or management account, and grant IAM users the ability to list Organizations accounts only when they need to create billing groups or view KPIs — the service is only reachable from the payer/management account context. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)
- **[programmatic access]** Create a dedicated IAM user or role specifically for programmatic (API) access to Billing Conductor, separate from console users, so console and API access can be governed with distinct, more precise policies. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)
- **[credentials]** Avoid using the AWS account root user for day-to-day Billing Conductor administration, and prefer temporary credentials via IAM roles or federation over long-term IAM user credentials. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/security-iam.html)
- **[least privilege]** Use the documented Billing Conductor identity-based policy examples (full/read-only console access, API access, CUR access) as the basis for scoping permissions rather than granting broad billing permissions. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/security_iam_id-based-policy-examples.html)

## 🛡️ Reliability
- **[primary account selection]** Choose a primary account for each standalone billing group that will remain in your AWS Organizations for the entire billing period — if it joins or leaves mid-month, pro forma billing data for the whole group is unavailable for the affected days. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)
- **[billing group lifecycle]** Recreate the billing group (rather than reuse it) after its primary account leaves the Organization, since the group is marked for deletion the following month — set up a new primary account before the next billing period to preserve continuity of pro forma billing. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)
- **[account moves mid-period]** Expect billing group costs to be recomputed retroactively for the full billing period when accounts move between billing groups mid-month — plan reporting and reconciliation around this recomputation behavior instead of treating it as an anomaly. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)

## 💰 Cost Optimization
- **[pricing plans]** Use AWS managed pricing plans (`BasicPricingPlan`, `Passthrough`) where they fit your use case instead of building custom pricing plans from scratch, and remember an empty custom pricing plan defaults all usage to Billing Conductor base rates. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/abc-pricingplan.html)
- **[pricing rule design]** Design pricing rules deliberately, since more granular (service-specific) rules run before global rules and rules do not stack — structure markups/discounts per pricing plan to avoid unintended cumulative effects. [doc](https://aws.amazon.com/blogs/aws-cloud-financial-management/questions-and-answers-on-aws-billing-conductor/)
- **[custom line items]** Use custom line items to allocate support fees, shared service costs, managed service fees, taxes, credits, and RI/Savings Plans savings distribution, choosing itemized vs. consolidated computation rules based on how granular the chargeback needs to appear on the bill. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/create-cli.html)
- **[rate analysis]** Use the billing group margin report to regularly compare applied pro forma rates against actual AWS rates, ensuring your chargeback/showback model tracks intended margins over time. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html)
- **[Passthrough switching]** When switching a billing transfer group to or from the Passthrough pricing plan, account for the fact that the switch updates the current month's cost data retroactively and that existing Cost and Usage Report configurations stop receiving new data and must be recreated. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/abc-pricingplan.html)

## ⚙️ Operational Excellence
- **[reporting cadence]** Account for the update cadence when building operational processes: current-month custom line items reflect within 24 hours, while items applied to a prior billing period can take up to 48 hours to appear in Cost and Usage Reports or the Bills page. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)
- **[per-billing-group CUR]** Configure a separate AWS Cost and Usage Report for each billing group so downstream FinOps tooling and customer-facing reports reflect the correct pro forma cost data per group. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html)
- **[budgets and alerts]** Have accounts and organizations in billing groups create budgets against their pro forma spend so stakeholders are alerted when actual or forecasted showback/chargeback costs exceed expected limits. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html)
- **[change notifications]** Monitor the email notifications Billing Conductor sends on configuration changes (e.g., a primary account leaving Organizations, a new linked account auto-joining a billing group) and act promptly to keep billing group membership accurate. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html)
- **[multi-level billing transfer]** For two-level billing transfer arrangements, have the bill transfer receiver account manually configure the billing group in the bill source accounts' Organizations, since only the bill transfer account sends invitations and this configuration step is required for correct downstream visibility. [doc](https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html)

<!-- meta: last_reviewed=2026-07-05; sources=7 -->
