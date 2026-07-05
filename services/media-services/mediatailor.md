# AWS Elemental MediaTailor — Best Practices

## Common scenarios
- Server-side ad insertion (SSAI) for live and VOD streaming        → Reliability, Performance Efficiency
- Assembling virtual linear (FAST) channels from VOD/live sources        → Reliability, Cost Optimization
- Personalizing manifests and targeting ads per viewer session        → Security, Operational Excellence
- Delivering stitched content/ads at scale through a CDN        → Performance Efficiency, Cost Optimization

## 🔒 Security
- **[transport]** Require TLS 1.2 (prefer TLS 1.3) with PFS cipher suites (DHE/ECDHE) for all client and origin connections — MediaTailor only accepts HTTPS and rejects HTTP. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/infrastructure-security.html)
- **[access control]** Restrict MediaTailor resource-based policies by source IP address or scope access to specific VPC endpoints/VPCs — isolates network access to only trusted sources. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/infrastructure-security.html)
- **[IAM]** Grant least-privilege identity-based policies for MediaTailor actions instead of broad/administrator access — follow the documented policy best practices. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/security_iam_id-based-policy-examples.html)
- **[data protection]** Set up individual IAM users/roles with MFA rather than sharing account credentials, and enable AWS CloudTrail for API and user activity logging. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/data-protection.html)
- **[data protection]** Never place confidential or sensitive information (customer emails, credentials) in tags, free-form name fields, or origin/ADS URLs, since these can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/data-protection.html)
- **[origin auth]** Enable authentication (for example AWS Secrets Manager access token authentication) for custom origins so manifest and segment requests aren't served to unauthorized callers. [doc](https://aws.amazon.com/blogs/media/creating-virtual-linear-channels-using-aws-elemental-mediatailor/)
- **[CDN]** Enforce HTTPS-only viewer connections and configure geo-restriction, signed URLs/signed cookies, and IP allowlists for administrative CDN access. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-security-best-practices.html)
- **[CDN]** Enable CDN access logging and alerting on unusual traffic patterns, and periodically review security configuration for drift. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-security-best-practices.html)
- **[parameters]** Validate player/session parameters client-side, use configuration aliases to constrain allowed parameter values, and avoid passing sensitive data through parameters. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/parameter-troubleshooting.html)

## 🛡️ Reliability
- **[origins]** Configure redundant origin servers with automated failover between primary and backup origins so a single origin failure doesn't disrupt playback. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/plan-for-workflow.html)
- **[multi-Region]** Use Media Quality-Aware Resiliency (MQAR) with CloudFront to automatically route to the highest-quality-scoring origin across multiple Regions, particularly for live events requiring uninterrupted service. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/media-quality-resiliency.html)
- **[failover]** Implement configuration aliases for backup origins and ad servers so traffic can switch automatically during failover scenarios. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/configuration-aliases-overview.html)
- **[CDN caching]** Configure negative caching for error responses (4xx/5xx) at the CDN to avoid overwhelming the origin with repeated requests during a disruption. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-architecture-considerations.html)
- **[ad fallback]** Configure slate content to fill ad breaks when ads cannot be inserted, and set up backup ad sources or default ads for when primary ad sources fail. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/preventing-ad-skipping-best-practices.html)
- **[quotas]** Review MediaTailor channel assembly and API throttling quotas (channels per account, manifest requests per second, etc.) and request quota increases proactively for expected scale. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/quotas.html)
- **[monitoring]** Set CloudWatch alarms on `GetManifest.Age` to detect stale manifests, and use `Origin.Age` vs. `GetManifest.MediaTailorAge` to isolate whether the origin or MediaTailor is causing staleness. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/stale-manifest-diagnose.html)

## ⚡ Performance Efficiency
- **[CDN placement]** Place your CDN between viewers and MediaTailor (not between MediaTailor and the origin) so the CDN can cache segments while MediaTailor still personalizes manifests per viewer. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-architecture-considerations.html)
- **[cache behavior]** Create separate CDN cache behaviors per request type: no caching for manifests, longer TTLs for content and ad segments. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-architecture-considerations.html)
- **[Origin Shield]** Enable CloudFront Origin Shield in the Region closest to your MediaTailor origin to consolidate duplicate requests, improve cache hit ratio, and protect origin availability during traffic spikes. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cloudfront-performance-optimization.html)
- **[Origin Shield]** For global deployments, monitor Origin Shield cache hit ratios and consider multiple Origin Shield locations. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-advanced-optimization.html)
- **[capacity planning]** Size CDN and origin capacity based on channel count, bitrate, and expected concurrent viewer load, and account for predictable schedule-driven traffic patterns in channel assembly workloads. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/plan-for-workflow.html)
- **[testing]** Test ad insertion workflows across devices and network conditions before launch to catch performance issues early. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/preventing-ad-skipping-best-practices.html)

## 💰 Cost Optimization
- **[CDN]** Always front MediaTailor with a CDN such as CloudFront — it caches ad and content segments, reducing origin ad-delivery volume and lowering data-transfer costs. [doc](https://aws.amazon.com/mediatailor/pricing/)
- **[Origin Shield]** Use Origin Shield to reduce the number of redundant requests reaching the origin, which lowers origin compute/transfer costs in addition to improving reliability. [doc](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html)

## ⚙️ Operational Excellence
- **[monitoring]** Monitor CloudWatch metrics such as `Avail.FillRate`, `AdDecisionServer.FillRate` (target above 90%), `GetManifest.Latency`/`GetManifest.Errors`, and `AdDecisionServer.Latency`/`Errors`/`Timeouts` to track ad delivery and manifest health. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/cdn-monitoring.html)
- **[logging]** Use the `MediaTailor/AdDecisionServerInteraction` and `MediaTailor/ManifestService` CloudWatch Logs groups to correlate ad-request and manifest events, and review skipped-ad reasons when troubleshooting. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/monitoring.html)
- **[transcoding]** Monitor CloudWatch logs for transcoding efficiency/patterns that could cause ad skipping, and engage AWS Support if anomalies appear. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/preventing-ad-skipping-best-practices.html)
- **[monetization functions]** When using MediaTailor Monetization Functions, create CloudWatch dashboards on invocation/error/latency metrics and alarm on elevated error rates or hook execution time approaching the timeout budget. [doc](https://aws.amazon.com/blogs/media/customize-ad-workflows-with-aws-elemental-mediatailor-monetization-functions/)
- **[tagging]** Tag MediaTailor resources consistently to support cost allocation, access control, and operational tracking across configurations. [doc](https://docs.aws.amazon.com/mediatailor/latest/ug/monitoring.html)

<!-- meta: last_reviewed=2026-07-05; sources=20 -->
