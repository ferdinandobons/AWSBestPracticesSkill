# AWS Elemental MediaStore — Best Practices

## Common scenarios
- Migrating an existing live-streaming MediaStore container before end of support        → Reliability, Operational Excellence
- Choosing a replacement origin (Amazon S3 vs. AWS Elemental MediaPackage) for a decommissioned container        → Reliability, Operational Excellence
- Retrieving persistent objects stored in MediaStore before the container becomes inaccessible        → Reliability, Operational Excellence

## 🛡️ Reliability
- **[Planning]** Treat November 13, 2025 as a hard cutover deadline — after this date MediaStore and all its capabilities stop working, so migrations must be validated and live well before then. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)
- **[Origin selection]** For simple live-streaming workflows, migrate to Amazon S3 as the origin; for workflows that need cross-Region failover, DRM, or specific low-latency packaging, migrate to AWS Elemental MediaPackage instead. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)
- **[Origin selection]** Use the documented origin comparison (scaling limits, latency, redundancy, pricing) to decide between Amazon S3 and MediaPackage rather than defaulting to a like-for-like replacement. [doc](https://aws.amazon.com/blogs/media/choosing-the-ideal-origin-for-live-media-entertainment-workflows/)
- **[Data retrieval]** If a container holds persistent objects (not just transient live-origination segments), use the MediaStore List and Get APIs to copy that data out to Amazon S3 or another store before the container becomes unreachable. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)
- **[Data retrieval]** Confirm whether objects are already being purged by encoder logic or a MediaStore Lifecycle Policy — workflows that only ever held transient live segments may have no data to migrate, simplifying the cutover. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)
- **[CDN cutover]** When repointing Amazon CloudFront from a MediaStore data endpoint to the new S3 or MediaPackage origin, update origin access control and container/bucket policies together so the CDN retains read access throughout the switch. [doc](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-mediastore.html)
- **[Escalation]** If you can't complete data retrieval before the end-of-support date, contact AWS Support proactively rather than waiting for the container to become inaccessible. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)

## ⚙️ Operational Excellence
- **[Dependency audit]** Inventory every workflow component that references MediaStore container/data endpoints — encoders (for example AWS Elemental MediaLive outputs), CDN origins, and playback applications — so no dependency is missed during migration. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)
- **[Cutover validation]** Test playback end-to-end against the new Amazon S3 or MediaPackage origin (including CDN caching behavior and access policies) before decommissioning the MediaStore container, rather than cutting over on faith. [doc](https://aws.amazon.com/blogs/media/choosing-the-ideal-origin-for-live-media-entertainment-workflows/)
- **[IaC and automation]** Update infrastructure-as-code, encoder configuration, and monitoring/alerting that targets MediaStore-specific resources (containers, lifecycle policies, CORS policies) so nothing continues to assume the service is available after cutover. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_mediastore.CfnContainer.html)
- **[Support]** Reach out to AWS Support with questions about your specific migration path or timeline rather than guessing at unsupported behavior as the end-of-support date approaches. [doc](https://aws.amazon.com/blogs/media/support-for-aws-elemental-mediastore-ending-soon/)

<!-- meta: last_reviewed=2026-07-05; sources=4 -->
