# Amazon Textract — Best Practices

## Common scenarios
- Extracting text, forms, and tables from scanned documents        → Performance Efficiency, Reliability
- Processing large multi-page PDFs (invoices, mortgages, claims)        → Reliability, Cost Optimization
- Automated document pipelines invoked from Lambda/S3 events        → Operational Excellence, Security
- Handling sensitive documents (financial, healthcare, ID) at scale        → Security, Cost Optimization

## 🔒 Security
- **[access control]** Start from AWS managed policies (e.g. `AmazonTextractFullAccess`) and narrow to customer-managed, least-privilege policies scoped to specific actions and resources as you productionize — reduces blast radius of compromised credentials. [doc](https://docs.aws.amazon.com/textract/latest/dg/security_iam_id-based-policy-examples.html)
- **[access control]** Add IAM policy conditions (e.g. require SSL, restrict by source) and validate policies with IAM Access Analyzer before attaching them — catches overly permissive or non-functional policies early. [doc](https://docs.aws.amazon.com/textract/latest/dg/security_iam_id-based-policy-examples.html)
- **[authentication]** Require MFA for IAM users and the root account, and use IAM Identity Center or IAM roles instead of long-lived credentials — limits exposure from leaked static keys. [doc](https://docs.aws.amazon.com/textract/latest/dg/data-protection.html)
- **[data protection]** Enforce TLS 1.2 (prefer TLS 1.3) with cipher suites supporting perfect forward secrecy (DHE/ECDHE) for all API calls to Amazon Textract — protects data in transit. [doc](https://docs.aws.amazon.com/textract/latest/dg/infrastructure-security.html)
- **[data protection]** Never put confidential or sensitive information (e.g. customer email addresses) into free-form text fields — this data can be picked up by diagnostic logs. [doc](https://docs.aws.amazon.com/textract/latest/dg/data-protection.html)
- **[data protection]** Encrypt asynchronous job output with an AWS KMS customer-managed key (via the `KmsKeyId` parameter) when routing results to your own S3 bucket, instead of relying only on default SSE-S3 — gives you an auditable key-usage trail and revocable access. [doc](https://docs.aws.amazon.com/textract/latest/dg/encryption.html)
- **[data protection]** Enable AWS CloudTrail to log Amazon Textract API calls (e.g. `DetectDocumentText`, `AnalyzeDocument`, `StartDocumentAnalysis`) for auditing and incident investigation. [doc](https://docs.aws.amazon.com/textract/latest/dg/security.html)
- **[network isolation]** Use an interface VPC endpoint (AWS PrivateLink) for Amazon Textract so control-plane traffic between your VPC and the service does not traverse the public internet. [doc](https://docs.aws.amazon.com/textract/latest/dg/vpc-interface-endpoints.html)
- **[network isolation]** Apply a restrictive VPC endpoint policy that limits the endpoint to only the specific Textract APIs a workload needs (e.g. only `DetectDocumentText`) as an additional least-privilege layer beyond IAM. [doc](https://aws.amazon.com/blogs/machine-learning/using-amazon-textract-with-aws-privatelink/)
- **[confused deputy]** When granting Amazon Textract a service role to publish to your Amazon SNS topic or read from S3, use the `aws:SourceArn` (and `aws:SourceAccount` where the ARN lacks an account ID) condition keys in the trust/resource policy — prevents cross-service impersonation. [doc](https://docs.aws.amazon.com/textract/latest/dg/cross-service-confused-deputy-prevention.html)
- **[compliance]** Use FIPS endpoints when FIPS 140-2 validated cryptographic modules are required for CLI/API access. [doc](https://docs.aws.amazon.com/textract/latest/dg/data-protection.html)

## 🛡️ Reliability
- **[error handling]** Configure automatic retries (a retry count of 5 is recommended) with exponential backoff and jitter on the Textract client to handle throttling (`ProvisionedThroughputExceededException`) and dropped connections. [doc](https://docs.aws.amazon.com/textract/latest/dg/handling-errors.html)
- **[throughput]** Smooth spiky call patterns with a queueing or serverless architecture instead of bursting directly against TPS quotas — sustains maximum achievable throughput. [doc](https://docs.aws.amazon.com/textract/latest/dg/limits-quotas-explained.html)
- **[capacity planning]** Estimate optimal quota values with the Textract Service Quota Calculator and request quota increases proactively before launch or traffic spikes. [doc](https://docs.aws.amazon.com/textract/latest/dg/limits-quotas-explained.html)
- **[async processing]** Use the asynchronous APIs (`StartDocumentTextDetection`/`StartDocumentAnalysis` with Amazon SNS + Amazon SQS notification) for multi-page PDFs/TIFFs so large documents don't block application threads or hit synchronous timeouts. [doc](https://docs.aws.amazon.com/textract/latest/dg/api-async.html)
- **[resilience]** Design applications around the multi-Availability-Zone resilience of the Region and account for API quotas as part of failure-mode planning; note that cross-Region transfer of Textract data is restricted under GDPR, which affects DR architecture choices. [doc](https://docs.aws.amazon.com/textract/latest/dg/disaster-recovery-resiliency.html)

## ⚡ Performance Efficiency
- **[input quality]** Provide as high a quality scan/image as possible (at least 150 DPI) and avoid downsampling or converting documents that are already in a supported format (PDF, JPG, PNG) — directly improves extraction accuracy and avoids reprocessing. [doc](https://aws.amazon.com/textract/faqs/)
- **[input quality]** For table extraction, ensure tables are visually separated from surrounding content and text is upright rather than rotated — improves table-structure detection reliability. [doc](https://aws.amazon.com/textract/faqs/)
- **[throughput]** Use a queueing/serverless architecture to smooth traffic and maximize achievable throughput within allotted TPS quotas. [doc](https://docs.aws.amazon.com/textract/latest/dg/limits-quotas-explained.html)
- **[async processing]** Prefer asynchronous operations for large, multi-page documents so your application can continue other work while Textract processes the job in the background. [doc](https://docs.aws.amazon.com/textract/latest/dg/async.html)
- **[custom queries]** When training Custom Queries adapters, use representative layout/image variation in samples, a minimum of five samples per query level, and consistent annotation conventions — produces more accurate extraction for business-specific document formats. [doc](https://docs.aws.amazon.com/textract/latest/dg/best-practices-adapters.html)

## 💰 Cost Optimization
- **[API selection]** Call only the specific feature types you need (e.g. Tables, Forms, Queries, Signatures) on `AnalyzeDocument` rather than requesting all features by default — avoids paying for analysis you don't use. [doc](https://aws.amazon.com/textract/pricing/)
- **[capacity planning]** Monitor quota utilization trends via the Service Quotas console CloudWatch integration and set alarms on utilization thresholds to catch runaway usage before it drives unplanned cost. [doc](https://aws.amazon.com/blogs/machine-learning/introducing-self-service-quota-management-and-higher-default-service-quotas-for-amazon-textract/)
- **[evaluation]** Use the Bulk Document Uploader for evaluating Textract against a representative document sample before committing to a specific feature set or architecture at production scale — avoids paying for a poorly-fitted approach. [doc](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-textract-bulk-document-uploader-for-enhanced-evaluation-and-analysis/)

## ⚙️ Operational Excellence
- **[monitoring]** Monitor `ThrottledCount`, `UserErrorCount`, `ResponseTime`, and `SuccessfulRequestCount` CloudWatch metrics (overall or per-operation via the Operation dimension) to detect throttling, errors, and latency issues. [doc](https://docs.aws.amazon.com/textract/latest/dg/textract-monitoring.html)
- **[monitoring]** Enable AWS CloudTrail logging for Textract API calls to support troubleshooting, auditing, and operational visibility into the document-processing lifecycle. [doc](https://aws.amazon.com/textract/faqs/)
- **[architecture]** Build asynchronous pipelines using the documented SNS/SQS notification-channel pattern (or Lambda triggers) to decouple document submission from result retrieval and simplify operational monitoring of job state. [doc](https://docs.aws.amazon.com/textract/latest/dg/api-async-roles.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
