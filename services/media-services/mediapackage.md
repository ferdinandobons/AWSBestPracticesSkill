# AWS Elemental MediaPackage — Best Practices

## Common scenarios
- Just-in-time packaging of live streams into HLS, LL-HLS, DASH, and CMAF for multiple devices        → Performance Efficiency, Reliability
- Applying DRM (FairPlay, Widevine, PlayReady) and CDN authorization to protect premium content        → Security
- Building highly available live workflows with redundant encoder inputs and cross-Region failover        → Reliability
- Harvesting live streams into VOD assets and monitoring channel/endpoint health        → Operational Excellence, Cost Optimization

## 🔒 Security
- **[IAM]** Grant access with IAM users/roles and apply least-privilege permissions scoped to specific MediaPackage actions and resources, starting from AWS managed policies and narrowing with customer-managed policies. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Avoid wildcard characters in the `Principal` element of resource policies — explicitly list the users or groups allowed to access channels and origin endpoints instead. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/access-control-best-practices.html)
- **[IAM]** Make `Deny` statements as broad as possible and `Allow` statements as narrow as possible, and pair `Deny` with the `mediapackagev2:*` action as an opt-in pattern for least-privilege policies. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/access-control-best-practices.html)
- **[IAM]** Use IAM Access Analyzer to validate new and existing MediaPackage policies for secure, functional permissions, and require MFA for users who manage MediaPackage resources. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Use conditions in IAM policies (for example, requiring SSL) to further restrict which requests and services can invoke MediaPackage actions. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Content protection]** Apply CDN authorization so MediaPackage only fulfills playback requests carrying valid authorization headers from your CDN, preventing viewers from bypassing the CDN to hit the origin directly. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cdn-auth.html)
- **[Content protection]** Use UUID v4 format for CDN authorization secret values, and rotate secrets periodically while regularly testing the rotation procedure to ensure smooth transitions. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cdn-auth-best-practices.html)
- **[Content protection]** Reuse the same CDN authorization secret across multiple endpoints in the same Region/account where your security requirements allow it, to reduce management overhead. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cdn-auth-best-practices.html)
- **[Content protection]** Monitor for unusual patterns of CDN authorization failures and set CloudWatch alarms on them, since spikes can indicate attempted unauthorized access. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cdn-auth-best-practices.html)
- **[DRM]** Use SPEKE to integrate with a DRM key provider (FairPlay, Widevine, PlayReady) so encryption keys and licenses are supplied just-in-time during packaging rather than pre-encrypting source content. [doc](https://docs.aws.amazon.com/mediapackage/latest/ug/cfigs-hls-encryption.html)
- **[Data handling]** Don't put sensitive identifying information (such as customer account numbers) into free-form MediaPackage fields like harvest job IDs, since this data can be picked up in diagnostic logs or EventBridge events. [doc](https://docs.aws.amazon.com/mediapackage/latest/ug/hj-create.html)
- **[Authentication]** Sign requests to the MediaPackage API using AWS Signature Version 4 to ensure request integrity and authenticity. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/access-control-best-practices.html)

## 🛡️ Reliability
- **[Input redundancy]** Send two encoder streams to a channel's separate ingest URLs/domains so MediaPackage can automatically fail over to the passive stream if the active one stops, without interrupting playback. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/what-is-flow-ir.html)
- **[Input redundancy]** When using an HLS output group from MediaLive, set the input loss action to pause output rather than sending filler/black frames — otherwise MediaPackage cannot detect missing segments and can't trigger failover. [doc](https://docs.aws.amazon.com/mediapackage/latest/ug/what-is-flow-ir.html)
- **[Input redundancy]** Use the endpoint time-delay feature to reduce viewer-facing buffering during input switches when using short output segments, understanding this adds end-to-end latency. [doc](https://docs.aws.amazon.com/mediapackage/latest/ug/what-is-flow-ir.html)
- **[Quality-aware resiliency]** Enable "input switch based on MQCS" so MediaPackage selects the ingest pipeline with the best media-quality confidence scores instead of only the most complete/lowest-latency one, improving output quality during partial degradation. [doc](https://aws.amazon.com/blogs/media/improve-your-viewers-live-streaming-experience-with-media-quality-aware-resiliency/)
- **[Cross-Region failover]** Deploy symmetric MediaPackage Live v2 origins in multiple AWS Regions and let your CDN fail over between them transparently, since single-Region failover configurations don't protect against a full Regional outage. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cross-region-failover.html)
- **[Endpoint error handling]** Enable stale-manifest, incomplete-manifest, and slate-input failover conditions on the primary origin endpoint but disable them on the backup, so the backup endpoint remains available to the CDN as a fallback. [doc](https://aws.amazon.com/blogs/media/build-a-resilient-cross-region-live-streaming-architecture-on-aws/)
- **[Monitoring]** Watch CloudWatch metrics and MediaPackage Input Notification events to detect input switches and endpoint failovers so operations teams can respond to underlying encoder or network issues. [doc](https://aws.amazon.com/blogs/media/part1-how-to-set-up-a-resilient-end-to-end-live-workflow/)

## ⚡ Performance Efficiency
- **[Format selection]** Choose low-latency HLS (LL-HLS) over standard HLS when sub-10-second latency matters — standard HLS typically runs 18-30 seconds while LL-HLS can reach 3-5 seconds, at the cost of requiring LL-HLS-aware players. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/hls-overview.html)
- **[Delivery]** Front MediaPackage origin endpoints with a CDN such as Amazon CloudFront so cached responses absorb repeat viewer requests instead of hitting the origin for every playback session. [doc](https://aws.amazon.com/mediapackage/features/)
- **[Manifest freshness]** Use the MediaPackage manifest-update response headers (last sequence, last part, last updated) to detect and troubleshoot stale-manifest issues affecting playback performance. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/monitoring-manifest-last-updated.html)

## 💰 Cost Optimization
- **[Delivery]** Use Amazon CloudFront (or another CDN) in front of MediaPackage so cached content reduces the volume of video originated and packaged directly from MediaPackage, lowering origination costs. [doc](https://aws.amazon.com/mediapackage/pricing/)
- **[VOD storage]** Use MediaPackage VOD packaging so only a single adaptive-bitrate asset needs to be stored in S3, and multiple output formats/DRM policies are generated just-in-time rather than duplicating pre-packaged variants. [doc](https://aws.amazon.com/mediapackage/pricing/)
- **[CDN authorization]** Reuse CDN authorization secrets across endpoints in the same Region/account where appropriate, to reduce Secrets Manager and operational overhead. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/cdn-auth-best-practices.html)

## ⚙️ Operational Excellence
- **[Monitoring]** Use Amazon CloudWatch metrics (via the MediaPackage console, CloudWatch console, or CLI) to track bandwidth, request counts, and response times, and set alarms on thresholds that matter to your workflow. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/monitoring-cloudwatch.html)
- **[Auditing]** Enable AWS CloudTrail to capture MediaPackage API calls, letting you identify which users/accounts made changes, from which source IP, and when. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/monitoring.html)
- **[Event-driven ops]** Use EventBridge (CloudWatch Events) rules on MediaPackage events, such as input-switch notifications, to automate operational responses instead of manual polling. [doc](https://aws.amazon.com/blogs/media/part1-how-to-set-up-a-resilient-end-to-end-live-workflow/)
- **[Access logging]** Enable MediaPackage access logs on channels for detailed request records, useful for security and access audits. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/monitoring.html)
- **[Visibility]** Use the Live Video Workflow Monitor to discover, visualize, and monitor the resources associated with a live stream, and configure metric alarm/notification templates to alert on issues across the workflow. [doc](https://aws.amazon.com/mediapackage/features/)
- **[Live-to-VOD]** Use harvest jobs to extract live-to-VOD assets for a specific timeframe, keeping in mind a harvest job runs once and its record can't be modified or deleted afterward. [doc](https://docs.aws.amazon.com/mediapackage/latest/userguide/live-to-vod.html)

<!-- meta: last_reviewed=2026-07-05; sources=19 -->
