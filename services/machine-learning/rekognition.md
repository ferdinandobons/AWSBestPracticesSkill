# Amazon Rekognition — Best Practices

## Common scenarios
- Face verification and identity onboarding        → Security, Reliability
- Content moderation for user-generated images/video        → Operational Excellence, Security
- Large-scale batch image/video analysis pipelines        → Performance Efficiency, Cost Optimization
- Streaming video analysis (e.g. camera feeds)        → Reliability, Performance Efficiency

## 🔒 Security
- **[access control]** Grant least-privilege IAM permissions and start from AWS managed policies before narrowing to customer-managed policies scoped to specific actions and resources — reduces blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html)
- **[access control]** Add IAM policy conditions (e.g. require SSL/TLS on requests) and validate policies with IAM Access Analyzer before attaching them — catches overly permissive or non-functional policies early. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html)
- **[authentication]** Use temporary credentials via IAM roles instead of long-term IAM user credentials, and require MFA for human users and the root account — limits exposure from leaked static keys. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html)
- **[data protection]** Enforce TLS 1.2 (prefer TLS 1.3) with cipher suites supporting perfect forward secrecy (DHE/ECDHE) for all API calls to Amazon Rekognition — protects data in transit. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/infrastructure-security.html)
- **[data protection]** Never place confidential or sensitive information (e.g. customer email addresses) into tags or free-form text fields such as name fields — this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html)
- **[data protection]** Enable AWS CloudTrail to log all Amazon Rekognition API and user activity for auditing and incident investigation. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html)
- **[network isolation]** Use an interface VPC endpoint (AWS PrivateLink) for Amazon Rekognition so traffic between your VPC and the service stays off the public internet. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/vpc.html)
- **[compliance]** Use FIPS endpoints when FIPS 140-3 validated cryptographic modules are required for CLI/API access. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html)

## 🛡️ Reliability
- **[resilience]** Design applications to rely on the multi-AZ resilience of the AWS Region rather than a single point of failure, and account for API quotas as part of failure-mode planning. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/disaster-recovery-resiliency.html)
- **[throughput]** Smooth spiky call patterns with a queueing/serverless architecture instead of bursting directly against TPS quotas — sustains maximum achievable throughput. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html)
- **[error handling]** Implement retries with exponential backoff and jitter for retryable errors (e.g. throttling, provisioned-throughput-exceeded) per the documented error codes. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/error-handling.html)
- **[capacity planning]** Calculate required TPS from peak concurrent calls and expected response window, review TPS utilization history, and request quota increases proactively before launch or before traffic spikes. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html)
- **[streaming video]** Note that each Kinesis Video input stream and Kinesis Data output stream can only be associated with a single Rekognition Video stream processor — architect stream processor allocation accordingly to avoid contention. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html)

## ⚡ Performance Efficiency
- **[input quality]** Follow documented recommendations for camera setup, image/video input quality, and facial comparison inputs to get optimal recognition accuracy and avoid unnecessary reprocessing. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/best-practices.html)
- **[latency]** Pass images as raw bytes (under 4 MB) for near-real-time processing (e.g. IP camera feeds); for larger or already-stored images, reference the Amazon S3 object instead, since S3-based analysis is generally faster than uploading bytes for larger images. [doc](https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/running-model.html)
- **[throughput]** Use a queueing/serverless architecture to smooth traffic and maximize achievable throughput within allotted TPS quotas. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/limits.html)
- **[multi-region]** For latency-sensitive, high-availability clients, deploy across multiple Regions and use Amazon Route 53 routing policies to steer traffic to the best-performing endpoint. [doc](https://aws.amazon.com/solutions/guidance/age-verification-on-aws/)

## 💰 Cost Optimization
- **[human review]** Use Amazon Augmented AI (A2I) with a confidence-score threshold or random sampling percentage to route only low-confidence predictions to human reviewers — balances accuracy against review cost. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/a2i-rekognition.html)
- **[architecture]** Favor serverless, pay-as-you-go architectures around Amazon Rekognition so compute and storage scale with actual demand instead of being over-provisioned. [doc](https://aws.amazon.com/solutions/guidance/age-verification-on-aws/)

## ⚙️ Operational Excellence
- **[monitoring]** Capture Amazon Rekognition API calls with AWS CloudTrail and application logs with Amazon CloudWatch to support troubleshooting and operational visibility. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html)
- **[human review]** Route content-moderation predictions below a confidence threshold to Amazon A2I human review workflows to catch and correct low-confidence model outputs in production. [doc](https://docs.aws.amazon.com/rekognition/latest/dg/a2i-rekognition.html)
- **[Face Liveness]** Keep Face Liveness SDKs updated, tune the liveness confidence threshold using representative real-world testing, and periodically sample selfie frames to monitor for quality drift over time. [doc](https://docs.aws.amazon.com/ai/responsible-ai/rekognition-face-liveness/overview.html)

<!-- meta: last_reviewed=2026-07-05; sources=12 -->
