# AWS Elemental MediaConvert — Best Practices

## Common scenarios
- Video-on-demand (VOD) transcoding to ABR/HLS/DASH renditions        → Performance Efficiency, Cost Optimization
- Large-scale batch or archive transcoding pipelines        → Reliability, Cost Optimization
- Automated post-processing workflows triggered by job completion        → Operational Excellence, Reliability
- Delivering DRM-protected or encrypted output for OTT distribution        → Security

## 🔒 Security
- **[IAM]** Start from AWS managed policies and move toward least-privilege customer-managed policies scoped to specific MediaConvert actions and resources — reduces blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** When creating the MediaConvert service role, restrict it to only the specific Amazon S3 input and output bucket locations the job needs, rather than granting account-wide S3 access — limits what a compromised job role can reach. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/creating-the-iam-role-in-mediaconvert-configured.html)
- **[IAM]** Add IAM policy conditions such as requiring SSL/TLS transport or restricting by source ARN or account — narrows when and how MediaConvert actions can be invoked. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer before deploying them — catches overly permissive or non-functional statements before they reach production. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/security_iam_id-based-policy-examples.html)
- **[IAM]** Require multi-factor authentication (MFA) for IAM users or root account access used to manage MediaConvert resources — adds a second factor against credential compromise. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/security_iam_id-based-policy-examples.html)
- **[Confused deputy]** In the MediaConvert service role's trust policy, use the `aws:SourceArn` and `aws:SourceAccount` condition keys — prevents cross-service confused-deputy attacks by ensuring the role is only assumed on behalf of your own MediaConvert queues. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/cross-service-confused-deputy-prevention.html)
- **[Data protection]** Enable server-side encryption on output Amazon S3 destinations in the job settings — MediaConvert outputs are not encrypted by default. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/implementing-server-side-encryption.html)
- **[Data protection]** Use an AWS KMS customer-managed key for output encryption instead of the default S3-managed key — gives you control over key policies and auditability. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/implementing-server-side-encryption.html)
- **[Data protection]** If input or output S3 buckets use SSE-KMS default encryption, grant the MediaConvert service role only the specific `kms:Decrypt` (inputs) and `kms:GenerateDataKey` (outputs) permissions it needs — avoids broad KMS access. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/granting-permissions-for-mediaconvert-to-access-encrypted-s3-buckets.html)
- **[Compliance monitoring]** Continuously validate submitted job configurations against your required security posture (S3-only inputs, KMS encryption enabled, non-public output ACLs) — catches non-compliant jobs before they run. [doc](https://aws.amazon.com/blogs/media/how-to-perform-aws-elemental-mediaconvert-job-compliance-checks-using-amazon-cloudwatch/)

## 🛡️ Reliability
- **[Queue hopping]** Configure hop destinations on jobs or job templates to move a job to an alternate queue after a wait threshold — avoids indefinite delays when the original queue is backlogged. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/how-you-pay-for-reserved-queues.html)
- **[Reserved queues]** Design job templates and queue-hop targets with awareness that 8K output, Automated ABR, AV1, Dolby Vision, MV-HEVC spatial video, FrameFormer, and accelerated transcoding are unavailable on reserved queues — prevents jobs from failing when they land on a reserved queue. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/feature-limitations-with-reserved-queues.html)
- **[Job priority]** Set relative job priority within a queue — ensures time-sensitive jobs are processed ahead of lower-priority batch work when capacity is constrained. [doc](https://docs.aws.amazon.com/mediaconvert/latest/apireference/jobs.html)
- **[Monitoring]** Subscribe to MediaConvert EventBridge job-status events (`PROGRESSING`, `STATUS_UPDATE`, `COMPLETE`, `ERROR`, `NEW_WARNING`) — enables detection of failures or stalled jobs without polling. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/eventbridge_events.html)
- **[Monitoring]** Set up EventBridge rules with notifications specifically for failed (`ERROR`) jobs — lets operational teams respond quickly to transcoding failures. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/eventbridge_events.html)
- **[Idempotency]** Use a `clientRequestToken` on job creation requests — prevents duplicate job submission on retries. [doc](https://docs.aws.amazon.com/mediaconvert/latest/apireference/jobs.html)

## ⚡ Performance Efficiency
- **[Encoding settings]** Let MediaConvert automatically select recommended encoding settings (GOP structure, B-frames, adaptive quantization) unless you have specific delivery requirements — gives balanced quality and file size with less manual tuning. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/video-quality.html)
- **[Accelerated transcoding]** Use accelerated transcoding for long-duration or visually complex jobs on on-demand queues (or via queue hop from a reserved queue set to Preferred) — significantly reduces processing time. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/feature-limitations-with-reserved-queues.html)
- **[Packaging]** For HEVC and HDR/SDR ABR output stacks intended for OTT delivery, use fragmented MP4 (CMAF) output groups rather than MPEG-TS — required by the HLS authoring specification for HEVC video. [doc](https://aws.amazon.com/blogs/media/part-2-4k-hdr-vod-workflows-using-aws-elemental-mediaconvert-and-aws-elemental-server/)
- **[Quality monitoring]** Use MediaConvert Media Metrics with CloudWatch and EventBridge to track video/audio quality scores, black frames, and bitrate statistics — surfaces quality regressions in your encoding pipeline. [doc](https://aws.amazon.com/blogs/media/monitor-video-content-and-encoding-quality-with-media-metrics-in-aws-elemental-mediaconvert/)

## 💰 Cost Optimization
- **[Reserved queues]** For steady-state, predictable transcoding volume, purchase reserved transcode slots (RTS) instead of using on-demand pricing — steady usage on RTS can be substantially cheaper per minute than on-demand at high utilization. [doc](https://aws.amazon.com/blogs/media/reserved-pricing-in-aws-elemental-mediaconvert-part-1-intro-and-how-to-use-it/)
- **[Reserved queues]** Simulate a reserved queue before committing — reserved pricing requires a non-cancellable 12-month commitment and you pay for capacity whether or not it's used. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/working-with-reserved-queues.html)
- **[Queue hopping]** Combine a reserved queue with on-demand hop destinations so burst overflow runs on-demand while steady-state volume stays on reserved capacity — billing follows whichever queue actually runs the job. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/how-you-pay-for-reserved-queues.html)
- **[Accelerated transcoding]** Reserve accelerated transcoding for jobs that genuinely need faster turnaround on long or visually complex content rather than enabling it by default — outputs using this feature incur pro-tier pricing. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/feature-limitations-with-reserved-queues.html)

## ⚙️ Operational Excellence
- **[Automation]** Trigger post-processing (packaging, notifications, catalog updates) from MediaConvert `COMPLETE` EventBridge events using AWS Lambda — removes the need to manually poll job status. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/eventbridge_events.html)
- **[Observability]** Use `GetJob`/`ListJobs` or the console job list for status checks, and enable an AWS CloudTrail trail if you also need `SUBMITTED`-stage events — MediaConvert does not emit a `SUBMITTED` EventBridge event on its own. [doc](https://docs.aws.amazon.com/mediaconvert/latest/ug/how-mediaconvert-jobs-progress.html)
- **[Job templates]** Define job templates for recurring workflows, including acceleration settings, hop destinations, and priority — keeps job configuration consistent and auditable across your pipeline. [doc](https://docs.aws.amazon.com/boto3/latest/reference/services/mediaconvert/client/create_job_template.html)
- **[Migration]** When migrating from Amazon Elastic Transcoder, convert existing presets with the provided migration script and review built-in MediaConvert system presets and templates — avoids rebuilding settings from scratch. [doc](https://aws.amazon.com/blogs/media/migrating-workflows-from-elastic-transcoder-to-elemental-mediaconvert/)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
