# Amazon Pinpoint — Best Practices

## Common scenarios
- Multi-channel marketing campaigns and customer journeys (email, SMS, push, in-app)        → Reliability, Operational Excellence
- Mobile/web app analytics and event collection for engagement segmentation        → Reliability, Security
- Transactional and campaign messaging with delivery tracking across Regions        → Reliability, Cost Optimization
- Planning a migration off Amazon Pinpoint before end of support        → Operational Excellence, Reliability

## 🔒 Security
- **[IAM]** Create an individual IAM user or role for each person or system that manages Amazon Pinpoint resources (projects, campaigns, journeys, phone numbers, pools, configuration sets) instead of sharing or using AWS account root credentials. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-best-practices.html)
- **[IAM]** Grant each user or role only the minimum permissions needed for their duties, and use IAM groups to manage permissions consistently across multiple users. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-best-practices.html)
- **[IAM]** Rotate IAM credentials used to access Amazon Pinpoint APIs on a regular basis. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/security-best-practices.html)
- **[Encryption]** Rely on Amazon Pinpoint's default encryption at rest (AWS KMS-managed keys) for configuration data, endpoint data, analytics data, and imported data — no separate action is required, but confirm it meets your compliance needs. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/security-data-protection-encryption.html)
- **[Data protection]** Use TLS 1.2 at minimum (TLS 1.3 recommended) for all communication with Amazon Pinpoint APIs. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-data-protection.html)
- **[Data protection]** Never place confidential or sensitive data, such as customer email addresses, into tags or free-form text fields (e.g., project/campaign names) — this content can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-data-protection.html)
- **[Data protection]** Enable AWS CloudTrail logging for Amazon Pinpoint API and console activity to support auditing and incident investigation. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-data-protection.html)
- **[Data protection]** Use multi-factor authentication (MFA) on accounts with access to Amazon Pinpoint, and consider Amazon Macie to help discover and secure sensitive data if you export Pinpoint data to Amazon S3. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/security-data-protection.html)

## 🛡️ Reliability
- **[Event stream]** Enable the Amazon Pinpoint event stream (to Kinesis Data Streams or Kinesis Data Firehose) so you have delivery status for campaigns, email, and SMS to track delivery rates and troubleshoot failures. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/bestpractices.html)
- **[Multi-Region]** When designing a multi-Region architecture, plan explicitly for replicating and synchronizing event stream data across Regions. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/bestpractices.html)
- **[Retry strategy]** Use exponential backoff when retrying failed Amazon Pinpoint API calls rather than retrying immediately. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/bestpractices.html)
- **[Retry strategy]** Tailor retry and monitoring logic to each channel's delivery semantics — push notifications confirm success/failure in real time, while SMS and email deliveries and their acknowledgments can be delayed by minutes or hours due to factors outside AWS's control (e.g., carrier redelivery). [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/bestpractices.html)
- **[Infrastructure as code]** Replicate Amazon Pinpoint infrastructure across Regions using CloudFormation to keep configuration consistent and minimize human error, while accounting for the capabilities CloudFormation doesn't cover (journeys, SMS origination identities) and using Lambda-backed custom resources or API calls to fill the gap. [doc](https://docs.aws.amazon.com/pinpoint/latest/archguide/bestpractices.html)
- **[Journeys]** Avoid deleting segments or endpoints that are referenced by an active journey — doing so can stop the journey prematurely or drop participants, which also corrupts journey analytics (dropped vs. removed participants become indistinguishable). [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/journeys-best-practices.html)
- **[Journeys]** Maintain a dedicated test segment and use Pinpoint's journey testing feature to validate journeys and messages before publishing them to a full audience. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/journeys-best-practices.html)
- **[Campaigns]** Send a test campaign (to a small test segment, specific endpoint IDs, or device tokens) before sending to the full target segment, to catch content or configuration errors early. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/practice-makes-perfect-testing-campaigns-before-you-send-them/)

## ⚡ Performance Efficiency
- **[Segmentation]** Use multiple smaller segments combined via multivariate split activities within a journey, rather than one large segment, to reduce processing time for message activities and better tailor the experience per group. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/journeys-best-practices.html)
- **[Segmentation]** Use comparative, matching, and date-based dimensional segment filters to precisely target audiences instead of over-broad segments that waste send volume on unlikely-to-convert recipients. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/segments-dimensional.html)

## 💰 Cost Optimization
- **[Journeys]** Use custom attributes and precise segment membership to keep journey audiences targeted, avoiding unnecessary message sends to participants unlikely to engage. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/journeys-best-practices.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Configure Amazon CloudWatch for Amazon Pinpoint to track campaign delivery, endpoint registration, and import job status, and create CloudWatch alarms (e.g., on campaign message failure counts) to get notified of delivery problems. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/monitoring.html)
- **[Monitoring]** Track the specific CloudWatch metrics exported for message delivery, endpoints, import jobs, one-time passwords, and events to build targeted dashboards and alarms rather than relying on ad hoc log review. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/monitoring-metrics.html)
- **[Quotas]** Review Amazon Pinpoint's project, API request, campaign, email, endpoint, journey, segment, and SMS/voice quotas ahead of scaling usage, and request quota increases proactively for quotas that are eligible. [doc](https://docs.aws.amazon.com/pinpoint/latest/developerguide/quotas.html)
- **[Migration planning]** Plan migration off Amazon Pinpoint ahead of the October 30, 2026 end-of-support date — engagement features (endpoints, segments, campaigns, journeys, analytics) are recommended to move to Amazon Connect Customer proactive engagement/outbound campaigns or Customer Profiles, event collection to Amazon Kinesis, and email sending to Amazon SES; SMS/MMS/push/WhatsApp/voice APIs continue under AWS End User Messaging and are unaffected. [doc](https://docs.aws.amazon.com/pinpoint/latest/userguide/migrate.html)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
