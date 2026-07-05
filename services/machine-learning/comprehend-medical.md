# Amazon Comprehend Medical — Best Practices

## Common scenarios
- Extracting medical entities and PHI from clinical notes, discharge summaries, and case notes        → Security, Reliability
- Linking detected conditions/medications to ICD-10-CM, RxNorm, or SNOMED CT ontology codes        → Reliability, Operational Excellence
- Running large-scale batch (asynchronous) analysis over clinical documents stored in Amazon S3        → Reliability, Performance Efficiency, Cost Optimization
- Redacting or de-identifying PHI before storing or sharing clinical text downstream        → Security

## 🔒 Security
- **[data in transit]** Require TLS 1.2 or later (TLS 1.3 recommended) with PFS cipher suites (DHE/ECDHE) for all client connections to the Comprehend Medical API — protects clinical text and PHI in transit. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/infrastructure-security.html)
- **[data at rest]** Supply a customer managed AWS KMS key (`KmsKey`) on every asynchronous `Start*Job` call to encrypt batch output files in S3 — without a key, output files are written in plain text. [doc](https://docs.aws.amazon.com/sdk-for-ruby/v3/api/Aws/ComprehendMedical/Types/StartPHIDetectionJobRequest.html)
- **[data at rest]** Scope any IAM policy that grants `kms:CreateGrant`/`kms:Decrypt`/`kms:GenerateDataKey` to the specific key ARN(s) used for Comprehend Medical jobs rather than granting access to all KMS keys. [doc](https://aws.amazon.com/blogs/machine-learning/enforce-vpc-rules-for-amazon-comprehend-jobs-and-cmk-encryption-for-custom-models/)
- **[network isolation]** Use an interface VPC endpoint (AWS PrivateLink) for Comprehend Medical so API traffic between your VPC and the service never traverses the public internet, and attach a restrictive endpoint policy scoped to the principals and actions that need it. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/comprehendmedical-vpcendpoints.html)
- **[IAM]** Grant only the specific Comprehend Medical actions each role needs (for example `DetectPHI`, `StartPHIDetectionJob`, `StartICD10CMInferenceJob`) rather than wildcard `comprehendmedical:*` permissions. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/security-iam-permissions.html)
- **[IAM]** Scope the batch job's data access role trust policy with `aws:SourceAccount` and `aws:SourceArn` conditions to prevent the confused-deputy problem when Comprehend Medical assumes the role to read/write your S3 buckets. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-batchapi.html)
- **[IAM]** Grant the data access role only `s3:GetObject`/`s3:ListBucket` on the input bucket and `s3:PutObject`/`s3:ListBucket` on the output bucket — avoid broad S3 permissions for the role Comprehend Medical assumes. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-batchapi.html)
- **[IAM]** Restrict `iam:PassRole` for the console's job-creation flow with a `iam:PassedToService` = `comprehendmedical.amazonaws.com` condition so users cannot pass arbitrary roles to the service. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/security-iam-permissions.html)
- **[sensitive data]** Never place confidential or sensitive information (such as patient identifiers) into tags or free-form name fields — this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/data-protection.html)
- **[account hygiene]** Protect AWS account credentials, require MFA, and set up individual least-privilege users through IAM or IAM Identity Center for anyone who can invoke Comprehend Medical. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/data-protection.html)
- **[compliance]** Treat Comprehend Medical as a HIPAA-eligible service and only process protected health information (PHI) after confirming your account and architecture meet your HIPAA compliance obligations, using AWS Artifact to review applicable audit reports. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/compliance-validation.html)
- **[auditability]** Enable AWS CloudTrail trails covering Comprehend Medical API events (including `Detect*`, `Start*Job`, and `Describe*Job` calls) to maintain an ongoing, queryable record of who accessed clinical data and when. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/logging-using-cloudtrail.html)

## 🛡️ Reliability
- **[clinical accuracy]** Identify an appropriate confidence-score threshold for your use case and require human review by trained medical professionals before any Comprehend Medical output is used in patient care decisions — the service is not a substitute for professional medical judgment. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/comprehendmedical-welcome.html)
- **[job design]** Use asynchronous batch jobs for large document sets (up to 10 GB per batch stored in S3) and synchronous detection APIs for smaller, latency-sensitive requests, matching each workload to the appropriate API. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-batchapi.html)
- **[quotas]** Design pipelines around the documented per-account limit of 10 active jobs per asynchronous API operation, and request quota increases through Service Quotas proactively for high-volume workloads. [doc](https://docs.aws.amazon.com/comprehend/latest/dg/guidelines-and-limits.html)
- **[job monitoring]** Poll `Describe*Job`/`List*Job` operations (or use CloudTrail/EventBridge events) to detect and react to failed or stopped batch jobs rather than assuming completion. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-batchapi.html)

## ⚡ Performance Efficiency
- **[job type selection]** Route large clinical document corpora to asynchronous batch APIs and reserve synchronous detection calls for real-time, low-latency needs, since batch jobs are optimized for throughput on bulk text. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-batchapi.html)
- **[ontology linking]** Use the purpose-built `InferICD10CM`, `InferRxNorm`, and `InferSNOMEDCT` operations to link entities directly to standardized codes instead of building custom post-processing logic to map free-text entities to ontologies. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/comprehendmedical-howitworks.html)

## 💰 Cost Optimization
- **[job type selection]** Batch documents into asynchronous jobs where real-time results aren't required, since minimum per-request character charges apply to every synchronous call regardless of actual document size. [doc](https://aws.amazon.com/comprehend/medical/pricing/)

## ⚙️ Operational Excellence
- **[monitoring]** Send Comprehend Medical API activity to an ongoing CloudTrail trail (not just Event History) so job creation, KMS configuration, and data access role usage remain auditable over time. [doc](https://docs.aws.amazon.com/comprehend-medical/latest/dev/logging-using-cloudtrail.html)
- **[event-driven automation]** Route Comprehend Medical CloudTrail events through EventBridge (`source: aws.comprehendmedical`) to trigger downstream automation, such as kicking off processing pipelines when a batch job completes. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-comprehendmedical.html)
- **[model lifecycle]** Track the `ModelVersion` recorded on each async job's properties so that downstream pipelines and reviewers can trace which model version produced a given set of clinical entity extractions. [doc](https://docs.aws.amazon.com/sdk-for-ruby/v3/api/Aws/ComprehendMedical/Types/ComprehendMedicalAsyncJobProperties.html)

<!-- meta: last_reviewed=2026-07-05; sources=15 -->
