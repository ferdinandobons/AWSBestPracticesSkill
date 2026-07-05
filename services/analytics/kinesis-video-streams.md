# Amazon Kinesis Video Streams — Best Practices

## Common scenarios
- Ingesting live video/audio from cameras and IoT devices for cloud storage        → Security, Reliability
- Real-time and batch video analytics with ML frameworks (Rekognition, TensorFlow, OpenCV)        → Performance Efficiency, Cost Optimization
- Peer-to-peer WebRTC streaming for two-way media and interactive applications        → Security, Reliability
- Long-term video retention for compliance and surveillance use cases        → Cost Optimization, Operational Excellence

## 🔒 Security
- **[access control]** Grant producer applications only the minimum actions they need, such as `PutMedia`, `GetStreamingEndpoint`, and `DescribeStream` — avoid wildcard (`*`) permissions or unrelated actions like `GetMedia` — reduces the blast radius of a compromised credential. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/security-best-practices.html)
- **[authentication]** Use IAM roles to vend temporary credentials to producer and consumer applications instead of embedding long-term access keys in devices or client code — long-term credentials aren't automatically rotated and are costlier to recover from if leaked. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/security-best-practices.html)
- **[monitoring]** Enable AWS CloudTrail to record all Kinesis Video Streams API calls, including caller identity, source IP, and timestamp — provides the audit trail needed to detect and investigate unauthorized access. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/security-best-practices.html)
- **[encryption at rest]** Assign a customer managed AWS KMS key to streams that require independent key control and rotation, rather than relying solely on the default service key — server-side encryption is always on, but a customer managed key lets you manage rotation and access policy yourself. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-kms.html)
- **[encryption in transit]** Ensure producer and consumer clients support TLS 1.2+ with perfect-forward-secrecy cipher suites (DHE/ECDHE) and sign requests with IAM credentials or AWS STS temporary credentials — required for all API access to Kinesis Video Streams. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/infrastructure-security.html)
- **[WebRTC]** Apply the same least-privilege IAM permissions and CloudTrail monitoring practices to signaling channels and WebRTC-based streaming, not just archived-media APIs — WebRTC connections are a distinct credential and permission surface from PutMedia/GetMedia. [doc](https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/kvswebrtc-security-best-practices.html)

## 🛡️ Reliability
- **[data retention]** Set an explicit `DataRetentionInHours` value when creating a stream instead of leaving it at the default of 0 (no persistence) — without retention, consumers can only read the last few minutes held in the service host buffer, which is capped at 5 minutes or 200 MB. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/APIReference/API_CreateStream.html)
- **[ingestion resilience]** Configure encoders to emit key frames at intervals under 10 seconds (or set a matching max fragment duration) to avoid `MaxFragmentDurationReached` ingestion errors — long-GOP or key-frame-less encoding causes fragments to exceed the service's fragment duration quota. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/troubleshooting.html)
- **[throttling]** Design consumer read patterns (ListFragments, GetClip, GetHLSMediaPlaylist, GetMediaForFragmentList, etc.) around the per-stream fragment-metadata and fragment-media quotas, and handle `ClientLimitExceededException` with backoff — these quotas are shared across all archived-media APIs on a given stream. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/limits.html)
- **[live playback]** Size HLS/DASH playlist requests conservatively — a minimum of 3 and maximum of 10 fragments for live playback — to balance rebuffering risk against added latency, and remember only 10 active HLS/DASH sessions are supported per stream. [doc](https://docs.aws.amazon.com/sdk-for-ruby/v3/api/Aws/KinesisVideoArchivedMedia/Types/GetHLSStreamingSessionURLInput.html)

## ⚡ Performance Efficiency
- **[monitoring]** Track key CloudWatch metrics such as `PutMedia.FragmentIngestionLatency`, `PutMedia.FragmentPersistLatency`, `PutMedia.ActiveConnections`, and `PutMedia.ConnectionErrors` to detect ingestion bottlenecks and connection issues before they affect downstream consumers. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/monitoring-cloudwatch.html)
- **[playback tuning]** Choose the HLS/DASH fragment window based on your latency-vs-continuity needs — smaller playlist sizes reduce buffering latency, larger ones reduce the likelihood of rebuffering during playback. [doc](https://docs.aws.amazon.com/sdk-for-ruby/v3/api/Aws/KinesisVideoArchivedMedia/Types/GetHLSStreamingSessionURLInput.html)

## 💰 Cost Optimization
- **[storage tiering]** Move data that only needs infrequent, near-real-time access into the Kinesis Video Streams warm storage tier (built on S3 Standard-IA) instead of keeping it all in hot storage — warm tier can cut long-term storage cost significantly while preserving durability and availability, at the cost of a 30-day minimum retention commitment. [doc](https://aws.amazon.com/blogs/iot/optimize-long-term-video-storage-costs-with-amazon-kinesis-video-streams-warm-storage-tier/)
- **[retention sizing]** Set data retention to the minimum period your use case actually requires (compliance, review window, etc.) rather than retaining indefinitely by default — retention is billed per GB-month of stored data. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/limits.html)
- **[key management]** Use the default AWS-managed KMS key when independent key control isn't required — it has no key charge, whereas a customer managed key incurs both AWS KMS key costs and per-credential API usage costs each time producers/consumers rotate data keys. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-kms.html)

## ⚙️ Operational Excellence
- **[auditability]** Log Kinesis Video Streams API activity with CloudTrail as a standard part of stream operations so that stream creation, permission changes, and data access are traceable across producers and consumers. [doc](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/security-best-practices.html)
- **[observability]** Build CloudWatch dashboards/alarms on ingestion and retrieval success-rate metrics (e.g., `PutMedia.Success`, `GetHLSStreamingSessionURL.Success`, `GetMP4MediaFragment.Success`) to catch degraded stream health across large fleets of devices. [doc](https://aws.amazon.com/blogs/mt/understanding-amazon-kinesis-video-streams-behavior-using-amazon-cloudwatch-aggregated-metrics/)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
