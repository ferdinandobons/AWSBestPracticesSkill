# AWS IoT FleetWise — Best Practices

## Common scenarios
- Collecting and standardizing signal data from heterogeneous vehicle fleets        → Performance Efficiency, Cost Optimization
- Running condition-based or time-based data collection campaigns at scale        → Performance Efficiency, Cost Optimization
- Delivering vehicle data to Amazon S3 or Amazon Timestream for fleet analytics and ML        → Security, Reliability
- Auditing and troubleshooting campaign/vehicle configuration changes        → Operational Excellence, Security

## 🔒 Security
- **[IAM]** Grant the minimum possible permissions and avoid `*` wildcards for `Action`/`Resource` in IAM policies attached to roles that manage campaigns, vehicles, and fleets — follow least privilege. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security-best-practices.html)
- **[IAM]** Start from AWS managed policies and then define customer managed policies scoped to your specific use case, using policy conditions (e.g. require SSL) to further restrict access. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer before attaching them to roles used by AWS IoT FleetWise. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Require multi-factor authentication (MFA) for IAM users or the root user who can create, modify, or delete AWS IoT FleetWise resources. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security_iam_id-based-policy-examples.html)
- **[Data handling]** Never put credentials or personally identifiable information (PII) into device names, or into the names/IDs of campaigns, decoder manifests, vehicle models, signal catalogs, vehicles, or fleets, since these can appear in logs. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security-best-practices.html)
- **[Encryption]** Use a customer managed AWS KMS key (instead of the AWS owned key) to encrypt AWS IoT FleetWise data at rest when you need direct control over key policy and rotation. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/encryption-at-rest.html)
- **[Encryption]** Grant the AWS IoT FleetWise service principal only the `kms:GenerateDataKey` and `kms:Decrypt` actions on the customer managed key used for your S3 destination, scoped via key policy. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/controlling-access.html)
- **[Access control]** Scope S3 bucket policies for campaign destinations to a specific campaign ARN (`aws:SourceArn`) and account (`aws:SourceAccount`) rather than granting blanket access to the bucket. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/controlling-access.html)
- **[Access control]** Disable S3 bucket ACLs and enforce Object Ownership on destination buckets if AWS IoT FleetWise fails to deliver data, instead of loosening bucket policy. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/controlling-access.html)
- **[Device security]** Keep vehicle/device clocks in sync so that X.509 certificate expiry validation works correctly and connections aren't rejected due to clock drift. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/security-best-practices.html)
- **[Auditability]** Turn on AWS CloudTrail to record AWS IoT FleetWise API calls (such as `CreateCampaign`, `AssociateVehicleFleet`, `GetModelManifest`) for security analysis and operational troubleshooting. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/logging-using-cloudtrail.html)

## 🛡️ Reliability
- **[Regions]** Create all resources for a given vehicle/campaign (signal catalog, vehicle model, decoder manifest, vehicles, fleets, campaigns) in the same AWS Region, since switching Regions can cause access issues. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/controlling-access.html)
- **[Storage]** Use Amazon Timestream for near-real-time vehicle data and Amazon S3 for data requiring batch processing, and rely on Timestream's cross-AZ/cross-Region backup support (or a custom export via the Timestream SDK) for resilience. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/disaster-recovery-resiliency.html)
- **[Campaign lifecycle]** Explicitly set an end time on approved campaigns rather than leaving them open-ended, since an approved campaign activates immediately and continues indefinitely by default. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/create-campaign.html)

## ⚡ Performance Efficiency
- **[Data collection]** Prefer condition-based (event-based) collection schemes over always-on time-based collection when you only need data around specific triggers, reducing unnecessary data transfer from the vehicle. [doc](https://aws.amazon.com/blogs/iot/collecting-vehicle-data-more-efficiently-with-aws-iot-fleetwise-2/)
- **[Data collection]** Use `minimumTriggerIntervalMs` and `maxSampleCount` in campaign collection schemes to throttle how often and how much data is sent when a signal changes frequently. [doc](https://aws.amazon.com/blogs/iot/collecting-vehicle-data-more-efficiently-with-aws-iot-fleetwise-2/)
- **[Vehicle modeling]** Build a single, well-structured signal catalog (based on COVESA VSS) and reuse it across vehicle models so signals stay consistent across brands, models, and protocols instead of duplicating definitions. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/vehicle-modeling.html)

## 💰 Cost Optimization
- **[Data collection]** Define time- and event-based collection rules (schemes) that select only the signals you need, rather than collecting all vehicle signals, to keep data transfer and downstream storage costs down. [doc](https://aws.amazon.com/blogs/iot/collecting-vehicle-data-more-efficiently-with-aws-iot-fleetwise-2/)
- **[Campaign lifecycle]** Set a defined time range on campaigns instead of leaving them running indefinitely, to avoid open-ended data collection charges. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/create-campaign.html)
- **[Quotas]** Plan campaign, signal, and manifest counts against published service quotas (e.g. 20 campaigns per Region by default, 500 signals per campaign) and request quota increases proactively rather than hitting throttling in production. [doc](https://docs.aws.amazon.com/general/latest/gr/iotfleetwise.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Use Amazon CloudWatch metrics to track AWS IoT FleetWise operational health, including whether service limits are being approached. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/monitoring-overview.html)
- **[Logging]** Enable delivery of AWS IoT FleetWise logs to a CloudWatch log group in the same account and Region as your resources so you get visibility into message-processing failures, such as faulty configuration or client errors. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/logging-cw.html)
- **[Auditability]** Use AWS CloudTrail Event History (or a configured multi-Region trail) to determine who made a given AWS IoT FleetWise API call, from where, and when, for operational troubleshooting. [doc](https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/logging-using-cloudtrail.html)

<!-- meta: last_reviewed=2026-07-05; sources=12 -->
