# Amazon Personalize — Best Practices

## Common scenarios
- Real-time product/content recommendations served to users on a website or app        → Performance Efficiency, Cost Optimization
- Batch recommendation generation for email campaigns or offline catalogs        → Cost Optimization, Operational Excellence
- Re-ranking a candidate list or filtering out ineligible items with business rules        → Reliability, Security
- Continuously adapting recommendations to evolving user behavior via streamed events        → Reliability, Operational Excellence

## 🔒 Security
- **[IAM]** Create a custom least-privilege IAM policy instead of attaching the AWS managed `AmazonPersonalizeFullAccess` policy — that managed policy grants more permissions than most workloads need. [doc](https://docs.aws.amazon.com/personalize/latest/dg/set-up-required-permissions.html)
- **[IAM]** Apply least-privilege permissions and validate identity-based policies with IAM Access Analyzer — this catches overly broad grants before they're attached to a role. [doc](https://docs.aws.amazon.com/personalize/latest/dg/security_iam_id-based-policy-examples.html)
- **[IAM]** Add IAM policy conditions, such as requiring SSL/TLS or restricting calls to specific AWS services, to identity-based policies — conditions further limit how Amazon Personalize actions can be invoked beyond action/resource scoping alone. [doc](https://docs.aws.amazon.com/personalize/latest/dg/security_iam_id-based-policy-examples.html)
- **[Encryption]** Supply your own AWS KMS key when creating dataset groups — this ensures imported user, item, and interaction data is encrypted with a key you control rather than only the Personalize-managed default key. [doc](https://docs.aws.amazon.com/personalize/latest/dg/data-encryption.html)
- **[Encryption]** Grant the AWS KMS key policy explicit permission for both Amazon Personalize and its IAM service role before referencing the key — without this grant, dataset group creation with a custom key fails. [doc](https://docs.aws.amazon.com/personalize/latest/dg/data-encryption.html)
- **[Data protection]** Never place confidential or sensitive values, such as customer email addresses, into resource names, tags, or other free-form text fields — these may surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/personalize/latest/dg/data-protection.html)
- **[Data protection]** Enforce TLS 1.2, and prefer TLS 1.3, for all communication with AWS resources, and enable AWS CloudTrail logging — this secures data in transit and preserves an audit trail of API and user activity. [doc](https://docs.aws.amazon.com/personalize/latest/dg/data-protection.html)
- **[Governance]** Design input data handling and access policies deliberately — Amazon Personalize does not redact sensitive data from its recommendation output, so upstream controls are the only safeguard. [doc](https://aws.amazon.com/solutions/guidance/patron-engagement-using-amazon-personalize/)

## 🛡️ Reliability
- **[Data quality]** Provide a minimum of 1,000 interaction records across at least 25 unique users, each with at least two interactions, before training — solutions trained below this threshold produce unreliable recommendations. [doc](https://aws.amazon.com/blogs/architecture/architecting-near-real-time-personalized-recommendations-with-amazon-personalize/)
- **[Data quality]** Ensure at least 70% of records are populated for any nullable attribute, and fix inconsistent naming, duplicate categories, or mismatched IDs across datasets before import — these issues can negatively impact recommendations or cause unexpected filtering behavior. [doc](https://docs.aws.amazon.com/personalize/latest/dg/readiness-checklist.html)
- **[Retraining]** Enable automatic training on solutions so they retrain on new bulk or streamed interaction data on a schedule — without it, recommendations grow stale and conversion rates decline. [doc](https://docs.aws.amazon.com/personalize/latest/dg/solution-config-auto-training.html)
- **[Retraining]** Stream real-time interaction events with `PutEvents` rather than relying solely on periodic bulk imports — filters and recommendations then reflect user activity within seconds instead of the up-to-20-minute delay for bulk-imported data. [doc](https://docs.aws.amazon.com/personalize/latest/dg/filter.html)
- **[Capacity]** Track request-rate CloudWatch metrics and raise a campaign's `minProvisionedTPS` proactively before sustained traffic approaches the auto-scaling threshold — there is a short delay while provisioned capacity scales up that can otherwise cause transaction loss. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-personalize-2018-05-22.html)

## ⚡ Performance Efficiency
- **[Use case fit]** Start with a Domain dataset group (VIDEO_ON_DEMAND or ECOMMERCE) when your application matches those domains, and use a Custom dataset group with a matching recipe otherwise — domain resources are pre-configured and optimized for those specific use cases. [doc](https://docs.aws.amazon.com/personalize/latest/dg/use-cases-and-recipes.html)
- **[Filtering]** Apply recommendation filters, including dynamic parameterized filter expressions, to enforce business rules such as excluding purchased or out-of-stock items — this avoids costly post-processing of results in application code. [doc](https://docs.aws.amazon.com/personalize/latest/dg/filter.html)
- **[Evaluation]** Prioritize offline metrics such as mean average precision at K and normalized discounted cumulative gain when comparing solution versions, then validate with online A/B testing before rollout — offline metrics alone don't guarantee real business impact like CTR or conversion gains. [doc](https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/)
- **[Monitoring]** Monitor `GetRecommendationsLatency` and `GetPersonalizedRanking` CloudWatch metrics for campaigns — this surfaces degraded response times or elevated error rates before users are affected. [doc](https://docs.aws.amazon.com/personalize/latest/dg/cloudwatch-metrics.html)

## 💰 Cost Optimization
- **[Campaigns]** Start new campaigns with the default `minProvisionedTPS` of 1 rather than over-provisioning — a higher minimum provisioned TPS sets a higher minimum billing charge regardless of actual traffic. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-personalize-2018-05-22.html)
- **[Campaigns]** Track actual usage with CloudWatch metrics and raise `minProvisionedTPS` incrementally only as sustained traffic justifies it — this avoids paying for capacity you don't yet need. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-personalize-2018-05-22.html)
- **[Campaigns]** Delete campaigns that are no longer in use — campaign costs accrue continuously while a campaign is active regardless of request volume. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-personalize-2018-05-22.html)
- **[Training]** Turn off automatic training on solutions you are no longer actively iterating on — automatic training incurs training costs on every scheduled run whether or not the results are used. [doc](https://docs.aws.amazon.com/personalize/latest/dg/solution-config-auto-training.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Configure CloudWatch alarms with SNS notifications on key metrics such as `DatasetImportJobError`, `SolutionTrainingJobError`, `GetRecommendationsLatency`, and `PutEventsRequests` — this surfaces import, training, and inference failures promptly instead of after the fact. [doc](https://docs.aws.amazon.com/personalize/latest/dg/personalize-monitoring.html)
- **[Data analysis]** Run Amazon Personalize's built-in data quality analysis on imported datasets before training — it identifies deficiencies and suggests remediation, reducing downstream troubleshooting. [doc](https://aws.amazon.com/personalize/faqs/)
- **[Measurement]** Configure metric attributions to report business outcomes, such as click-through rate or purchases, tied to recommendations directly to CloudWatch or S3 — this enables data-driven evaluation of personalization impact. [doc](https://aws.amazon.com/personalize/faqs/)
- **[Lifecycle]** Track solution, solution version, and campaign ARNs through `ListSolutionVersions`/`DescribeSolutionVersion`/`DescribeCampaign` as part of deployment automation, and wait for `ACTIVE` status before requesting recommendations — calling APIs against a resource that isn't yet active fails. [doc](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-personalize-2018-05-22.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
