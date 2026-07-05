# Amazon CodeGuru — Best Practices

## Common scenarios
- Automating code quality and security review on pull requests and repository branches        → Security, Operational Excellence
- Detecting hardcoded secrets and OWASP Top 10-style vulnerabilities in Java/Python code        → Security
- Continuously profiling production applications to cut CPU cost and latency        → Performance Efficiency, Cost Optimization, Sustainability
- Planning migration away from CodeGuru Reviewer now that it is in maintenance mode        → Operational Excellence, Reliability

## 🔒 Security
- **[data protection]** Create your own AWS KMS key for repository associations and code reviews instead of the AWS-owned default key when you need control over key policy and rotation — data at rest and in transit is encrypted by default, but a customer-managed key adds auditability. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/data-protection.html)
- **[network access]** Use an interface VPC endpoint (AWS PrivateLink) for CodeGuru Reviewer API calls, especially for programmatic access — traffic stays on the Amazon network instead of traversing the public internet (note: VPC endpoint policies are not supported, so full access is allowed through the endpoint). [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/vpc-interface-endpoints.html)
- **[IAM]** Grant only the specific CodeGuru Reviewer API actions each persona needs using the AWS managed policies (`AmazonCodeGuruReviewerFullAccess`, `AmazonCodeGuruReviewerReadOnlyAccess`, `AmazonCodeGuruReviewerServiceRolePolicy`) or scoped customer-managed policies — avoids granting developers administrator-level access. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/auth-and-access-control-iam-identity-based-access-control.html)
- **[CI/CD workflow]** Leave the auto-created `codeguru-reviewer-*` S3 bucket's assigned permissions unchanged — it already carries the minimum IAM permissions required for CodeGuru Reviewer to perform code security analysis. [doc](https://docs.aws.amazon.com/whitepapers/latest/security-overview-of-amazon-codeguru-reviewer/amazon-s3-bucket-protection-in-the-security-and-ci-workflow.html)
- **[secrets detection]** Run CodeGuru Reviewer's Secrets Detector across Java/Python code, configuration, and documentation files — it uses ML to flag hardcoded passwords, API keys, and tokens and recommends securing them with AWS Secrets Manager. [doc](https://aws.amazon.com/blogs/aws/codeguru-reviewer-secrets-detector-identify-hardcoded-secrets/)
- **[code review]** Combine CodeGuru Reviewer's automated security detectors (OWASP Top 10, AWS API security, crypto library misuse, input validation, log injection) with traditional peer review — a combination of code review processes catches more issues before production than either alone. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/create-code-reviews.html)
- **[profiler credentials]** Scope IAM permissions for the CodeGuru Profiler agent to only `codeguru-profiler:ConfigureAgent` and `codeguru-profiler:PostAgentProfile` on the specific profiling group ARN — limits what a compromised application role could do. [doc](https://aws.amazon.com/blogs/machine-learning/optimizing-application-performance-with-amazon-codeguru-profiler/)
- **[auditing]** Create a CloudTrail trail to capture CodeGuru Reviewer API events (e.g., `AssociateRepository`, `PutRecommendationFeedback`) — gives an ongoing, cross-Region audit record beyond the default Event history retention. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/logging-using-cloudtrail.html)

## 🛡️ Reliability
- **[code quality]** Integrate CodeGuru into your pipeline to automatically identify potential code and security issues via program analysis and machine learning — surfaces defects before they reach production. [doc](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/ops_dev_integ_code_quality.html)
- **[code reviews]** Require automated code reviews (CodeGuru Reviewer or an equivalent) as a standard SDLC gate alongside human review — automated tools catch errors, inconsistencies, and security flaws that manual review alone can miss. [doc](https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/sec_appsec_manual_code_reviews.html)
- **[migration planning]** Plan migration of code-review workflows to an alternative service for any new repositories or initiatives — as of November 7, 2025 you can no longer create new repository associations in CodeGuru Reviewer, though existing associations continue to function. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/codeguru-reviewer-availability-change.html)

## ⚡ Performance Efficiency
- **[profiler adoption]** Continuously profile live, latency-sensitive applications with the CodeGuru Profiler agent instead of relying only on point-in-time load testing — its low-overhead, always-on sampling surfaces the most CPU/latency-expensive lines of code. [doc](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/what-is-codeguru-profiler.html)
- **[anomaly response]** Configure Amazon SNS notification channels on a profiling group — CodeGuru Profiler sends a notification the moment it detects a method-level latency or CPU anomaly, enabling faster investigation of regressions. [doc](https://aws.amazon.com/codeguru/profiler/features/)
- **[recommendation triage]** Prioritize fixing the specific expensive lines of code, concurrency issues, and resource leaks that CodeGuru Reviewer and Profiler flag over broad, unguided refactors — recommendations are tied to measured CPU/latency impact. [doc](https://aws.amazon.com/codeguru/profiler/faqs/)

## 💰 Cost Optimization
- **[profiler-driven tuning]** Act on CodeGuru Profiler's recommendations to fix CPU-intensive lines of code — reducing CPU utilization directly lowers the compute infrastructure cost of the profiled application. [doc](https://aws.amazon.com/codeguru/profiler/features/)
- **[reviewer scope]** Exclude test, generated, and vendored directories from analysis with an `aws-codeguru-reviewer.yml` suppression file — reduces the amount of code analyzed and the associated CodeGuru Reviewer cost. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/recommendation-suppression.html)

## ⚙️ Operational Excellence
- **[workflow integration]** Run CodeGuru Reviewer as an automated step in CI/CD (e.g., GitHub Actions) triggered on push, pull, or a schedule — surfaces code quality and security recommendations in the CodeGuru console or GitHub Security tab continuously instead of only at manual review time. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/repository-analysis-vs-pull-request.html)
- **[feedback loop]** Rate CodeGuru Reviewer recommendations as helpful or not in the console or as pull request comments — this feedback is used to improve recommendation precision over time. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/recommendations.html)
- **[profiler onboarding]** Create a dedicated profiling group per application and grant its runtime execution role permission to submit profiles — keeps profiling data organized and access-scoped. [doc](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up.html)
- **[continuity planning]** Review AWS's guidance on alternative code-analysis services before starting new projects that would have depended on CodeGuru Reviewer — the service no longer accepts new repository associations. [doc](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/codeguru-reviewer-availability-change.html)

## 🌱 Sustainability
- **[carbon-aware tuning]** Use CodeGuru Profiler's recommendations to reduce CPU-intensive code paths — lowers the compute resources, and the associated emissions, needed to run a workload at the same throughput. [doc](https://aws.amazon.com/blogs/devops/reducing-your-organizations-carbon-footprint-with-codeguru-profiler/)

<!-- meta: last_reviewed=2026-07-05; sources=19 -->
