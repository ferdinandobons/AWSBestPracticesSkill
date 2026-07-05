# Amazon IVS — Best Practices

## Common scenarios
- Low-latency live streaming to a broad viewer audience        → Performance Efficiency, Cost Optimization
- Interactive, authenticated, or gated live-streaming experiences        → Security, Reliability
- Real-time multi-participant stages (co-streaming, watch parties)        → Performance Efficiency, Reliability
- Recording live streams for on-demand playback or moderation        → Reliability, Security

## 🔒 Security
- **[IAM policies]** Grant least privilege in identity-based policies and reserve `ivs:*` for admin roles only, not application roles — over-broad policies let application credentials create, modify, or delete channels and other billable resources. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-iam.html)
- **[IAM policies]** Require MFA and use policy conditions (source IP, date/time, `aws:SecureTransport`) on sensitive IVS API operations — this limits blast radius if credentials are compromised. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-iam.html)
- **[Stream keys]** Treat each channel's stream key as a secret and never embed it in client-distributed code — anyone holding the key can publish to the channel. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-ivs-alpha-readme.html)
- **[Playback authorization]** Enable playback authorization (private channels) and sign per-viewer JWTs with an uploaded ECDSA playback-key pair when streams must be restricted by channel or viewer — unauthorized playback requests are then rejected at the edge. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/private-channels.html)
- **[Playback authorization]** Because Amazon IVS does not rotate playback keys automatically and imported keys cannot be updated, plan for manual key replacement (import a new key pair and delete the old one) as your rotation mechanism. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/private-channels-create-key.html)
- **[Playback restriction]** Apply a playback restriction policy (allowed countries, allowed origins, and strict origin enforcement) to channels that must not serve arbitrary geographies or embedding sites. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/undesired-content.html)
- **[Ingest transport]** Use RTMPS (enabled by default) for stream ingest instead of plaintext RTMP unless you have a specific, verified need for insecure RTMP — RTMPS encrypts the contribution feed in transit. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-data-protection.html)
- **[Data protection]** Never place customer (end-user) identifying information in free-form IVS fields (channel names, metadata) — such fields can be surfaced in diagnostic logs and IVS does not encrypt live content end-to-end. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-data-protection.html)
- **[Resource authorization]** Use resource tags with `aws:ResourceTag`/`aws:RequestTag` condition keys in IAM policies to scope which principals can act on which channels — this supports team- or environment-level isolation without per-resource ARNs. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-iam.html)

## 🛡️ Reliability
- **[Service quotas]** Review and proactively request increases for concurrent-stream and concurrent-view quotas well before a large or high-profile streaming event — exceeding these thresholds causes stream rejection or viewer-facing failures. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/service-quotas.html)
- **[Ingest bitrate]** Keep encoder output safely under the channel type's ingest bitrate ceiling (do not target the maximum) since encoders routinely spike above their configured target and IVS disconnects streams that exceed the quota. [doc](https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/rt-rtmp-publishing.html)
- **[Recording redundancy]** Also record locally on the streaming device when using auto-record-to-S3 — network issues between the encoder and AWS can cause data loss in the cloud recording, and IVS prioritizes live delivery over recording fidelity. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/create-channel-auto-r2s3.html)
- **[Monitoring]** Monitor Stream Health metrics (video bitrate, frame rate, audio bitrate, starvation) in CloudWatch and alarm on unhealthy states to detect encoder or network degradation before viewers are impacted. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/stream-health.html)
- **[Incident response]** Subscribe to Amazon EventBridge stream-state events for real-time incident detection and consult the AWS Health Dashboard for regional IVS service health. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/security-incident-response.html)
- **[Encoder configuration]** Disable B-frames and keep RTMP streams carrying both audio and video tracks — streams with B-frames or a missing track are automatically disconnected by IVS. [doc](https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/rt-rtmp-publishing.html)

## ⚡ Performance Efficiency
- **[Encoder settings]** Set the IDR/keyframe interval to 1–2 seconds, use H.264 Main profile, and set CPU usage preset to `veryfast` with `zerolatency` tuning — these settings are what let IVS achieve sub-3-5-second glass-to-glass latency. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/streaming-config.html)
- **[Multitrack video]** Enable Multitrack Video on standard channels for broadcasters using compatible encoders (e.g., OBS Studio 30.2+) so the client sends multiple pre-encoded quality levels, giving viewers adaptive bitrate without added server-side transcoding latency. [doc](https://aws.amazon.com/blogs/media/multiple-video-quality-levels-and-lower-costs-with-amazon-ivs-multitrack-video/)
- **[Real-time stages]** For Web Broadcast SDK publishing, constrain `getUserMedia`/`getDisplayMedia` to the recommended resolution/frame-rate values and enable simulcast on Chromium browsers so the server can select the best rendition per participant's network conditions. [doc](https://docs.aws.amazon.com/ivs/latest/RealTimeUserGuide/web-publish-subscribe.html)
- **[Color/quality settings]** Use BT.709 color space for maximum playback compatibility across HDTVs and computer displays unless you have a verified need for another color space. [doc](https://docs.aws.amazon.com/ivs/latest/LowLatencyUserGuide/streaming-config.html)

## 💰 Cost Optimization
- **[Multitrack video]** Enable Multitrack Video on standard channels to shift ABR rendition generation to the broadcaster's device instead of server-side transcoding — this can cut live video input costs by up to ~75% compared to a standard channel without it. [doc](https://aws.amazon.com/blogs/media/multiple-video-quality-levels-and-lower-costs-with-amazon-ivs-multitrack-video/)
- **[Channel type selection]** Choose the channel type (basic, standard, or standard with multitrack) that matches actual quality and reach requirements — basic channels avoid transcoding costs for use cases that don't need adaptive bitrate output. [doc](https://aws.amazon.com/ivs/pricing/)
- **[Idle streams]** Stop publishing when a channel is not actively needed — all streams sent to IVS incur video input costs, metered per minute, even if no one is viewing. [doc](https://aws.amazon.com/ivs/pricing/)
- **[Recording]** Recognize that auto-record-to-S3 itself is not separately charged by IVS, but drives Amazon S3 storage, S3 API, and content-delivery costs — apply S3 lifecycle policies to recorded segments and thumbnails to control long-term storage spend. [doc](https://aws.amazon.com/blogs/machine-learning/moderate-your-amazon-ivs-live-stream-using-amazon-rekognition/)

## ⚙️ Operational Excellence
- **[Monitoring]** Build a CloudWatch dashboard combining IVS stream metrics and EventBridge stream-state events to track usage, state changes, and limit breaches across channels. [doc](https://aws.amazon.com/blogs/media/monitoring-amazon-ivs-with-a-cloudwatch-dashboard/)
- **[Quota tracking]** Track Service Quotas limit-breach metrics for concurrent viewers and concurrent streams, and request quota increases proactively ahead of anticipated growth or events. [doc](https://aws.amazon.com/blogs/media/monitoring-amazon-ivs-with-a-cloudwatch-dashboard/)
- **[Stream diagnostics]** Use `ListStreamSessions` with the `STARVING` health filter to proactively find unhealthy streams and correlate Stream Health data with playback-health data for a complete quality-of-experience picture. [doc](https://aws.amazon.com/blogs/media/using-analytics-to-improve-video-playback-quality-with-amazon-ivs/)
- **[Resource organization]** Tag IVS channels and related resources consistently to support cost allocation, access control, and operational filtering across environments and teams. [doc](https://docs.aws.amazon.com/securityhub/latest/userguide/ivs-controls.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
