# AWS Elemental MediaLive — Best Practices

## Common scenarios
- Live broadcast and OTT channel encoding to multiple ABR renditions        → Reliability, Performance Efficiency
- Redundant live contribution from remote venues or Elemental Link devices        → Reliability
- Ad insertion, closed captioning, and SCTE-35 marker processing for live streams        → Operational Excellence, Reliability
- Occasional-use or event-driven live streaming (sports, town halls, product launches)        → Cost Optimization

## 🔒 Security
- **[input access control]** Attach an input security group with only the specific upstream CIDR blocks that push content, and avoid overly broad ranges — MediaLive ignores push requests from IP addresses not covered by the group. [doc](https://docs.aws.amazon.com/medialive/latest/ug/working-with-input-security-groups.html)
- **[IAM roles]** Grant the MediaLive trusted entity role least-privilege access to only the specific S3 buckets, MediaPackage channels, or other resources each workflow needs, rather than broad account-wide permissions. [doc](https://docs.aws.amazon.com/medialive/latest/ug/complex-scenario-create-trusted-entity-role-step1.html)
- **[IAM policies]** Start from AWS managed policies and narrow toward least-privilege customer-managed policies, and validate them with IAM Access Analyzer before attaching to roles used by MediaLive. [doc](https://docs.aws.amazon.com/medialive/latest/ug/security_iam_id-based-policy-examples.html)
- **[account access]** Require multi-factor authentication (MFA) for accounts and IAM users that can create, modify, or delete MediaLive channels, since these actions incur cost and affect live output. [doc](https://docs.aws.amazon.com/medialive/latest/ug/security_iam_id-based-policy-examples.html)
- **[transport security]** Ensure clients and integrations communicating with the MediaLive API support TLS 1.2 at minimum (TLS 1.3 recommended) with cipher suites offering perfect forward secrecy. [doc](https://docs.aws.amazon.com/medialive/latest/ug/infrastructure-security.html)
- **[sensitive data]** Never place confidential or sensitive information (e.g., customer emails) into MediaLive tags, channel names, or other free-form text fields, since these may appear in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/medialive/latest/ug/data-retention.html)
- **[output delivery]** Use VPC delivery for channel outputs whose destinations live in your VPC so traffic stays off the public internet boundary. [doc](https://docs.aws.amazon.com/medialive/latest/ug/vpc-out-how-it-works.html)
- **[SRT listener outputs]** Configure a channel security group to restrict inbound connections when using SRT outputs in listener mode, since MediaLive acts as the server accepting external connections. [doc](https://docs.aws.amazon.com/medialive/latest/ug/feature-channel-security-groups.html)
- **[audit trail]** Enable an AWS CloudTrail trail covering MediaLive to capture who created, started, stopped, or deleted channels, and route logs to S3 for retention and analysis. [doc](https://docs.aws.amazon.com/medialive/latest/ug/logging-using-cloudtrail.html)

## 🛡️ Reliability
- **[channel class]** Use a standard channel (dual pipeline across two Availability Zones) instead of single-pipeline for any workflow where continuous output matters, so a single pipeline failure doesn't stop the stream. [doc](https://docs.aws.amazon.com/medialive/latest/ug/class-channel-input.html)
- **[input resiliency]** Configure automatic input failover with two push inputs in an input failover pair to protect against upstream system or network failures. [doc](https://docs.aws.amazon.com/medialive/latest/ug/aif-standard-pipeline-how.html)
- **[combined resiliency]** For maximum resiliency, combine automatic input failover with a standard (dual-pipeline) channel, sourcing four upstream feeds — two per input and two per pipeline. [doc](https://aws.amazon.com/blogs/media/part4-how-to-set-up-a-resilient-end-to-end-live-workflow/)
- **[input loss handling]** Configure input loss behavior (repeat-frame duration, black-frame threshold, and slate/color fill image) deliberately rather than relying on defaults, since a running channel must always encode content even during an upstream outage. [doc](https://docs.aws.amazon.com/medialive/latest/ug/feature-input-loss.html)
- **[Link device redundancy]** Feed a standard channel with two AWS Elemental Link devices for contribution redundancy, and pair with MediaPackage for automatic downstream failover. [doc](https://aws.amazon.com/elemental-link/faqs/)
- **[monitoring]** Subscribe to MediaLive Channel Alert and Channel State Change events via Amazon CloudWatch Events/EventBridge and route them to Amazon SNS so operators are notified in near real time of input loss, audio/video not detected, or pipeline state changes. [doc](https://docs.aws.amazon.com/medialive/latest/ug/monitoring-via-cloudwatch.html)
- **[alert triage]** Review the documented alert catalog (e.g., Audio Not Detected, Video Not Detected, Input Resource is Inaccessible) so on-call staff can distinguish recoverable input issues from configuration errors. [doc](https://docs.aws.amazon.com/medialive/latest/ug/monitor-activity-types-alerts-channels.html)

## ⚡ Performance Efficiency
- **[workflow planning]** Design the workflow output-first — identify required output groups and encode settings before selecting inputs and channel class — to ensure MediaLive can meet the transcoding requirements end-to-end. [doc](https://docs.aws.amazon.com/medialive/latest/ug/container-planning-uss-dss.html)
- **[source compatibility]** Verify upstream source codecs, resolutions, and frame rates are compatible with MediaLive and the target outputs before building the channel, to avoid probe failures at start time. [doc](https://docs.aws.amazon.com/medialive/latest/ug/container-planning-uss-dss.html)
- **[VPC inputs]** Use VPC-supported input types (CDI, RTMP push, RTP) when contribution sources live inside your VPC or on Direct Connect, keeping ingest off the public internet path. [doc](https://docs.aws.amazon.com/medialive/latest/ug/inputs-vpc-support.html)
- **[co-location]** Place channel endpoints and VPC output destinations in the same Availability Zone where possible to avoid extra inter-AZ data transfer and latency. [doc](https://docs.aws.amazon.com/medialive/latest/ug/vpc-out-caseA.html)

## 💰 Cost Optimization
- **[reserved pricing]** For channels, inputs, or outputs running more than 180 hours per month, purchase a 12-month reservation to save up to 75% versus on-demand rates. [doc](https://aws.amazon.com/medialive/pricing/)
- **[usage analysis]** Analyze AWS Cost and Usage Reports with Amazon QuickSight to find the right on-demand/reserved mix based on actual MediaLive usage patterns before committing to reservations. [doc](https://aws.amazon.com/blogs/media/data-driven-approach-optimizing-on-demand-cost-of-aws-elemental-medialive/)
- **[idle channels]** Stop channels automatically when no input is detected instead of leaving them running, since a channel continues to incur cost as long as it's running even without active input or output. [doc](https://aws.amazon.com/blogs/media/automatically-stop-aws-elemental-medialive-channels-when-no-input-is-detected/)
- **[channel class choice]** Prefer a single standard channel over two independent single-pipeline channels when redundancy is required, since a standard channel costs less than running two identical single-pipeline channels in the same Region. [doc](https://aws.amazon.com/medialive/pricing/)
- **[reservation tracking]** Track reservation utilization monthly since unused reservation minutes don't roll over to the next month, and delete expired reservations that are no longer matched by running resources. [doc](https://docs.aws.amazon.com/medialive/latest/ug/reservations.html)

## ⚙️ Operational Excellence
- **[access requirements]** Formally document which downstream AWS services (S3, MediaPackage, Systems Manager Parameter Store, etc.) each MediaLive workflow needs before designing IAM roles and policies. [doc](https://docs.aws.amazon.com/medialive/latest/ug/complex-scenario-create-trusted-entity-role-step1.html)
- **[observability]** Centralize MediaLive CloudWatch metrics, channel alerts, and MediaPackage events into one monitoring view (CloudWatch dashboards/alarms plus SNS notifications) so operators aren't hunting across scattered logs during an incident. [doc](https://aws.amazon.com/blogs/media/gain-observability-of-live-streaming-workflows-with-aws-elemental-medialive-and-aws-elemental-mediapackage/)
- **[change auditing]** Use CloudTrail Lake or Event History queries to answer operational questions like who started or stopped a specific channel and when. [doc](https://docs.aws.amazon.com/medialive/latest/ug/logging-using-cloudtrail.html)
- **[source health]** Supplement MediaLive's built-in alerts with content-aware monitoring (e.g., Amazon Rekognition) to catch impairments like frozen or black frames that don't otherwise trigger an alert. [doc](https://aws.amazon.com/blogs/media/source-monitoring-for-aws-elemental-medialive-via-amazon-rekognition/)

<!-- meta: last_reviewed=2026-07-05; sources=24 -->
