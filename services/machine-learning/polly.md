# Amazon Polly — Best Practices

## Common scenarios
- Converting text/SSML into lifelike speech for apps and IVR        → Performance Efficiency, Cost Optimization
- Building accessibility features (screen readers, read-aloud)        → Security, Reliability
- Generating long-form audio (audiobooks, news, e-learning)        → Reliability, Cost Optimization
- Voice-enabled chatbots and IoT devices        → Security, Operational Excellence

## 🔒 Security
- **[data protection]** Avoid putting sensitive identifying information (e.g. account numbers) into free-form text sent to Amazon Polly, since submitted content can be captured in diagnostic logs — protect customer data from unintended exposure. [doc](https://docs.aws.amazon.com/polly/latest/dg/data-protection.html)
- **[data protection]** Use SSL/TLS (1.2 or later) with cipher suites supporting perfect forward secrecy (DHE/ECDHE) for all calls to the Amazon Polly API — protects data in transit. [doc](https://docs.aws.amazon.com/polly/latest/dg/infrastructure-security.html)
- **[access control]** Sign every Amazon Polly request with IAM credentials or AWS STS temporary security credentials rather than long-lived static keys where possible — reduces the blast radius of leaked credentials. [doc](https://docs.aws.amazon.com/polly/latest/dg/infrastructure-security.html)
- **[access control]** Start from AWS managed policies and then define least-privilege customer managed policies scoped to the specific Amazon Polly actions and resources each workload needs. [doc](https://docs.aws.amazon.com/polly/latest/dg/security_iam_id-based-policy-examples.html)
- **[access control]** Add IAM policy conditions (e.g. requiring SSL, restricting by source service) to further constrain when Amazon Polly actions can be invoked. [doc](https://docs.aws.amazon.com/polly/latest/dg/security_iam_id-based-policy-examples.html)
- **[access control]** Validate identity-based policies with IAM Access Analyzer before attaching them, and require MFA for IAM/root users that can manage Amazon Polly resources. [doc](https://docs.aws.amazon.com/polly/latest/dg/security_iam_id-based-policy-examples.html)
- **[network security]** Use an interface VPC endpoint (AWS PrivateLink) for Amazon Polly when resources live in a VPC, so speech synthesis traffic never traverses the public internet. [doc](https://docs.aws.amazon.com/polly/latest/dg/using-polly-with-vpc-endpoints.html)
- **[responsible AI]** Implement content filtering and sensitive-content handling for input text, especially for regulated or public-facing applications, and add human review for high-risk or rights-impacting use cases. [doc](https://docs.aws.amazon.com/ai/responsible-ai/amazon-polly/overview.html)

## 🛡️ Reliability
- **[throttling]** Implement retries with exponential backoff and jitter for `SynthesizeSpeech` and other Polly API calls to smooth out usage spikes without compromising availability. [doc](https://docs.aws.amazon.com/polly/latest/dg/limits.html)
- **[throttling]** Track per-operation transaction-per-second quotas (they differ by voice engine: standard, neural, long-form, generative) and request quota increases proactively rather than after hitting `ThrottlingException`. [doc](https://docs.aws.amazon.com/polly/latest/dg/limits.html)
- **[long-running workloads]** Use the asynchronous `StartSpeechSynthesisTask` / `GetSpeechSynthesisTask` / `ListSpeechSynthesisTasks` APIs (with S3 output and optional SNS notification) for large text instead of forcing it through the real-time `SynthesizeSpeech` API. [doc](https://docs.aws.amazon.com/polly/latest/dg/longer-console.html)
- **[monitoring]** Watch Amazon Polly CloudWatch metrics and set alarms on throttling/error trends so capacity issues are caught before they affect end users. [doc](https://docs.aws.amazon.com/polly/latest/dg/cloud-watch.html)

## ⚡ Performance Efficiency
- **[voice selection]** Match the voice engine (generative, long-form, neural, standard) and voice/language to the use case, since latency, quality, and available regions differ by engine. [doc](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)
- **[input quality]** Ensure input text is well-structured, correctly punctuated, and contextually appropriate, and use SSML consistently to control pronunciation, pauses, rate, pitch, and emphasis — this avoids unnatural or incorrect speech output that would otherwise require re-synthesis. [doc](https://docs.aws.amazon.com/ai/responsible-ai/amazon-polly/overview.html)
- **[pronunciation]** Define custom pronunciation lexicons for domain-specific terms, acronyms, or names instead of relying on default pronunciation, reducing rework and manual QA. [doc](https://docs.aws.amazon.com/ai/responsible-ai/amazon-polly/overview.html)
- **[batching]** Parallelize synthesis of large documents by splitting text into paragraph/sentence chunks and processing them concurrently (e.g. with AWS Batch or Lambda), respecting the per-operation concurrency limits. [doc](https://docs.aws.amazon.com/polly/latest/dg/asynchronous.html)

## 💰 Cost Optimization
- **[caching]** Cache and replay previously generated speech output instead of re-synthesizing identical text, since Amazon Polly allows caching generated audio at no additional cost and you are billed only for text you synthesize. [doc](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)
- **[capacity planning]** Calculate your required transactions-per-second before requesting a quota increase — Amazon Polly provisions compute resources based on actual customer demand, so right-sizing requests keeps costs aligned with real usage. [doc](https://docs.aws.amazon.com/polly/latest/dg/limits.html)
- **[batch processing]** Use AWS Batch or asynchronous synthesis tasks for large-scale, non-interactive text-to-speech workloads (e.g. audiobooks) to process efficiently instead of over-provisioning for real-time peaks. [doc](https://docs.aws.amazon.com/polly/latest/dg/asynchronous.html)

## ⚙️ Operational Excellence
- **[logging]** Enable AWS CloudTrail to record Amazon Polly API activity (`SynthesizeSpeech`, `StartSpeechSynthesisTask`, lexicon operations, etc.), including caller identity and source IP, for auditing and troubleshooting. [doc](https://docs.aws.amazon.com/polly/latest/dg/logging-using-cloudtrail.html)
- **[monitoring]** Integrate Amazon CloudWatch with Amazon Polly to collect near real-time metrics on usage and errors, and use CloudWatch alarms to notify via SNS when thresholds are breached. [doc](https://docs.aws.amazon.com/polly/latest/dg/sec-logging.html)
- **[auditing]** When other AWS services (e.g. Amazon Lex) invoke Amazon Polly on your behalf via a service-linked role, review the corresponding CloudTrail entries to maintain transparency into those automated calls. [doc](https://aws.amazon.com/blogs/security/get-greater-transparency-into-actions-aws-services-perform-on-your-behalf-by-using-aws-cloudtrail/)

<!-- meta: last_reviewed=2026-07-05; sources=12 -->
