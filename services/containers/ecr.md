# Amazon ECR — Best Practices

## Common scenarios
- Storing and versioning container images for ECS/EKS/Fargate workloads        → Security, Reliability, Cost Optimization
- Scanning images for vulnerabilities before deployment        → Security, Operational Excellence
- Caching and mirroring public/upstream images to avoid pull-rate limits        → Reliability, Performance Efficiency
- Distributing images across accounts and Regions for multi-account or DR architectures        → Reliability, Security

## 🔒 Security
- **[encryption]** Use customer-managed AWS KMS keys instead of the default SSE-S3 encryption for repositories that need granular key control and auditability — the KMS key must reside in the same Region as the repository. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ecr.html)
- **[encryption]** Do not revoke the grants Amazon ECR creates by default on a repository's KMS key — doing so breaks the ability to push, encrypt, or decrypt images. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ecr.html)
- **[network]** Restrict registry/repository access to specific VPCs or VPC endpoints and require encrypted transport, isolating network access to only the resources that need it. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/ecr.html)
- **[network]** Use Amazon ECR interface VPC endpoints (AWS PrivateLink) so pushes and pulls stay on the AWS network without requiring an internet gateway or NAT device. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)
- **[network]** Attach VPC endpoint policies to control exactly which Amazon ECR actions and repositories are reachable through each endpoint. [doc](https://aws.amazon.com/blogs/containers/using-vpc-endpoint-policies-to-control-amazon-ecr-access/)
- **[iam]** Start from AWS managed policies and then author customer-managed policies that grant only the least-privilege permissions each user or workload role actually needs. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)
- **[iam]** Add IAM policy conditions (for example, requiring SSL/TLS or restricting to specific source services) to further scope down access to Amazon ECR actions and resources. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)
- **[iam]** Validate identity-based and repository policies with IAM Access Analyzer before applying them, to catch overly permissive statements. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)
- **[access-control]** Use resource-based repository policies to scope push/pull access by AWS account, IAM principal, or service principal rather than granting broad account-wide access. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/set-repository-policy.html)
- **[access-control]** For cross-account image sharing or cross-account replication, grant the minimum required actions (such as `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer`, or `ecr:ReplicateImage`) in a registry or repository policy rather than full access. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions-create-replication.html)
- **[image-integrity]** Enable image tag immutability on repositories so a pushed tag cannot be silently overwritten, ensuring deployed tags reliably reference the same image content. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html)
- **[scanning]** Turn on Amazon ECR enhanced scanning (Amazon Inspector integration) for continuous, automated scanning of OS and language-package vulnerabilities, not just scan-on-push. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced.html)
- **[scanning]** Configure scan filters to target production repositories for continuous scanning, and re-push older images after enabling enhanced scanning so they become eligible for scanning. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced.html)
- **[data-protection]** Set up individual IAM users/roles with least-privilege permissions and require MFA rather than sharing or using root credentials to manage repositories. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/data-protection.html)
- **[data-protection]** Avoid putting confidential or sensitive information in repository names, image tags, or other free-form fields, since this data can surface in billing or diagnostic logs. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/data-protection.html)
- **[transport]** Require TLS 1.2 (and prefer TLS 1.3) with cipher suites that support perfect forward secrecy for all clients communicating with the Amazon ECR API. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/infrastructure-security.html)

## 🛡️ Reliability
- **[replication]** Configure cross-Region (and, where needed, cross-account) private image replication so images remain available if a Region is impaired and to support multi-Region deployments. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html)
- **[replication]** Create replication rules before pulling through a pull-through cache so newly cached images are automatically propagated to the target Regions. [doc](https://aws.amazon.com/blogs/containers/announcing-pull-through-cache-for-registry-k8s-io-in-amazon-elastic-container-registry/)
- **[availability]** Use pull-through cache repositories to source images from public upstream registries, avoiding upstream throttling/rate limits that can cause build and deployment failures. [doc](https://aws.amazon.com/blogs/aws/announcing-pull-through-cache-repositories-for-amazon-elastic-container-registry/)
- **[lifecycle-safety]** When applying lifecycle policies, keep good CI/CD hygiene and set expiry rules that account for release cadence — purging an image still referenced by a long-running deployment causes image-pull errors. [doc](https://docs.aws.amazon.com/eks/latest/best-practices/image-security.html)
- **[lifecycle-safety]** Always run the lifecycle policy preview to confirm exactly which images will expire before applying a policy to a repository. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)

## ⚡ Performance Efficiency
- **[caching]** Use pull-through cache repositories for public-registry images to get Amazon ECR's higher download performance and availability instead of pulling directly from the public internet each time. [doc](https://aws.amazon.com/blogs/aws/announcing-pull-through-cache-repositories-for-amazon-elastic-container-registry/)
- **[network]** Use a VPC endpoint for Amazon ECR so tasks (for example, Fargate tasks) can pull private images without requiring a public IP address or traversing the internet, reducing latency and failure points. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-and-push-docker-images-to-amazon-ecr-using-github-actions-and-terraform.html)

## 💰 Cost Optimization
- **[lifecycle-policies]** Configure at least one lifecycle policy per repository to automatically expire old or unused images, lowering storage costs and keeping repositories organized. [doc](https://docs.aws.amazon.com/awssupport/latest/user/cost-optimization-checks.html)
- **[lifecycle-policies]** Define rules that filter by image age, image count, tag prefix, or tagged/untagged status (for example, expire untagged images after 90 days, staging images after 180 days) to match retention needs to actual usage. [doc](https://aws.amazon.com/blogs/compute/clean-up-your-container-images-with-amazon-ecr-lifecycle-policies/)
- **[storage-cleanup]** Regularly purge unneeded or obsolete image versions, since Amazon ECR does not track whether an image is currently in use — verify usage (for example via the AWS CLI) before enacting aggressive cleanup rules. [doc](https://aws.amazon.com/blogs/containers/optimize-your-container-workloads-for-sustainability/)

## ⚙️ Operational Excellence
- **[logging]** Enable AWS CloudTrail for Amazon ECR to capture all API calls, encryption-setting actions, and lifecycle-policy actions, giving you an audit trail of who pushed, pulled, or modified images and when. [doc](https://docs.aws.amazon.com/AmazonECR/latest/userguide/logging-using-cloudtrail.html)
- **[automation]** Route Amazon ECR CloudTrail events through Amazon EventBridge to automate responses, such as triggering repository creation or vulnerability-remediation workflows on specific API events. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-ecr.html)
- **[monitoring]** Use Amazon Inspector's deployment-footprint insights (last-used date, number of ECS tasks/EKS pods using an image) to prioritize vulnerability remediation on images that are actually in active use. [doc](https://aws.amazon.com/inspector/features/)

## 🌱 Sustainability
- **[storage-efficiency]** Apply lifecycle policies to purge unneeded image versions and reduce the storage footprint of container registries, especially for high-velocity projects producing many images per day. [doc](https://aws.amazon.com/blogs/containers/optimize-your-container-workloads-for-sustainability/)

<!-- meta: last_reviewed=2026-07-05; sources=22 -->
