# Amazon File Cache — Best Practices

## Common scenarios
- High-speed caching layer in front of on-premises NFS file servers for cloud bursting        → Performance Efficiency, Reliability
- Unified, high-throughput view over multiple S3 buckets and/or on-premises NFS systems for compute-intensive workloads        → Performance Efficiency, Cost Optimization
- Temporary, high-performance storage for HPC, VFX/media rendering, and AI/ML training jobs run on EC2        → Performance Efficiency, Cost Optimization
- Bridging on-premises data repositories to AWS compute over Direct Connect or VPN        → Security, Reliability

## 🔒 Security
- **[Encryption at rest]** Rely on the automatic at-rest encryption enabled on every cache, and specify a customer-managed AWS KMS key at creation time when you need control over key policies instead of the AWS-owned key. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/encryption-at-rest.html)
- **[Encryption in transit]** Use EC2 client instance types that support automatic in-transit encryption to Amazon File Cache, and rely on HTTPS (TLS) for traffic between the cache and linked S3 data repositories. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/encryption.html)
- **[Encryption in transit]** For links to on-premises file servers, use a VPN to encrypt traffic between your VPC and your on-premises network, or use MACsec to encrypt traffic over AWS Direct Connect. — [doc](https://aws.amazon.com/filecache/faqs/)
- **[Network isolation]** Deploy caches inside a VPC and use security groups to control which clients and file servers can reach the cache. — [doc](https://aws.amazon.com/filecache/features/)
- **[Network security]** Scope security group inbound rules to only the required ports (TCP 988 and TCP 1018-1023) and only the specific security groups for your File Cache file servers and Lustre clients, rather than open CIDR ranges. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/limit-access-security-groups.html)
- **[Identity]** Apply least-privilege IAM identity-based policies for who can create, access, tag, and delete File Cache resources, starting from AWS managed policies and narrowing to customer-managed policies for your specific use cases. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/security_iam_id-based-policy-examples.html)
- **[Identity]** Use IAM conditions (for example, requiring SSL/TLS) and IAM Access Analyzer to validate that File Cache policies are both secure and functional. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/security_iam_id-based-policy-examples.html)
- **[Identity]** Require multi-factor authentication (MFA) for IAM principals that can manage File Cache resources. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/security_iam_id-based-policy-examples.html)
- **[Access control]** Use tag-based, resource-level IAM permissions to control which users and roles can create, tag, or untag File Cache resources. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/using-tags.html)
- **[Data protection]** Set up individual IAM users or IAM Identity Center identities instead of sharing root or broad credentials, and enforce TLS 1.2 or higher for all API communication with Amazon File Cache. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/data-protection.html)
- **[Traceability]** Turn on AWS CloudTrail to log and monitor Amazon File Cache API activity for security auditing. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/monitoring_overview.html)
- **[Sensitive data]** Never put confidential or sensitive information (such as customer email addresses) into tags or free-form name fields on File Cache resources, since this data can surface in billing or diagnostic logs. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/data-protection.html)

## 🛡️ Reliability
- **[High availability]** Design for the cache's built-in resilience — unavailable file servers are automatically replaced within minutes and failed disks are automatically and transparently replaced, with client requests transparently retrying in the meantime. — [doc](https://aws.amazon.com/filecache/faqs/)
- **[Data durability]** Treat the cache as temporary, high-performance storage, not a system of record — export changed data and metadata back to your linked S3 or NFS data repository using HSM commands so results survive independent of the cache's lifecycle. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/export-changed-data.html)
- **[Data durability]** Before deleting a cache, verify no files are left "dirty" or unarchived and export any pending changes to the data repository first, since deleted cache data cannot be recovered. — [doc](https://aws.amazon.com/blogs/media/accelerate-thinkbox-deadline-by-bursting-to-the-cloud-with-amazon-file-cache/)
- **[Data repository lifecycle]** Do not delete an Amazon S3 bucket that is linked to a cache until all caches linked to it have been deleted, to avoid orphaned or broken data repository associations. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/overview-data-repo.html)
- **[Connectivity]** For cloud-bursting architectures linking to on-premises file servers, use AWS Direct Connect for the most reliable and highest-throughput connection between your data center and the cache. — [doc](https://aws.amazon.com/filecache/faqs/)

## ⚡ Performance Efficiency
- **[I/O sizing]** Use larger average I/O sizes where possible, since each file operation incurs a client-cache round trip and overhead is amortized better over larger requests. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/performance.html)
- **[Write mode]** Enable asynchronous writes for lower write latency, understanding the tradeoff in cross-instance consistency versus synchronous writes. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/performance.html)
- **[Compute sizing]** Choose EC2 instance types with enough memory and compute capacity for read/write-intensive workloads; Amazon File Cache performance does not depend on using EBS-optimized instances. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/performance.html)
- **[Client tuning]** For large client instances, apply the recommended Lustre client tuning (adjust `lru_max_age` on high-memory instances and `ptlrpcd`/`ksocklnd` settings on high-core-count instances) to sustain optimal throughput. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/performance.html)
- **[Data loading]** Use lazy load (the default) for most workloads so processing can start immediately, and use preloading instead only when your workload is sensitive to first-byte latency. — [doc](https://aws.amazon.com/filecache/faqs/)
- **[Data loading]** When listing large DRA directory hierarchies, use a recursive `ls` to populate metadata for all data repository associations in one pass rather than triggering lazy load per subdirectory. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/mdll-lazy-load.html)
- **[Throughput planning]** Remember that cache throughput capacity is shared between client I/O and data movement to/from linked repositories, so size the cache to cover both concurrently for workloads that actively load data while serving clients. — [doc](https://aws.amazon.com/filecache/faqs/)
- **[Monitoring]** Track CloudWatch front-end I/O, backend I/O, and cache utilization metrics (for example `DataReadBytes` and `FreeDataStorageCapacity` sums) to understand throughput and free capacity trends. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/performance.html)

## 💰 Cost Optimization
- **[Ephemeral usage]** Provision the cache only for the duration of the burst workload and delete it afterward instead of leaving it running idle, since File Cache is billed for provisioned storage capacity over time. — [doc](https://aws.amazon.com/filecache/pricing/)
- **[Automatic eviction]** Rely on automatic cache eviction (enabled by default) to release less recently used files as the cache fills, avoiding the need to over-provision storage capacity for peak working-set size. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/cache-eviction.html)
- **[Right-sizing]** Size cache storage capacity to your active working dataset rather than your total repository size, since throughput scales with (and is billed by) provisioned storage capacity. — [doc](https://aws.amazon.com/filecache/faqs/)
- **[Data transfer]** Be mindful that data transferred out of Amazon File Cache to another AWS Region is charged at inter-Region rates, and design workload placement to minimize unnecessary cross-Region movement. — [doc](https://aws.amazon.com/filecache/pricing/)

## ⚙️ Operational Excellence
- **[Monitoring]** Use Amazon CloudWatch (namespace `AWS/FSx`) to monitor cache health and performance in near real time, and build alarms with Amazon SNS notifications on key metrics. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/monitoring_overview.html)
- **[Logging]** Enable AWS CloudTrail logging for Amazon File Cache API calls and send logs to CloudWatch Logs for real-time monitoring and retention. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/monitoring_overview.html)
- **[Resource organization]** Tag Amazon File Cache resources consistently at creation to support cost allocation, access control, and reporting across your environment. — [doc](https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/tag-resources.html)
- **[Cleanup procedure]** Follow a defined shutdown procedure — confirm all data is archived/exported via HSM commands, delete the cache, then remove cache references from client bootstrap scripts and workflow orchestration tools — to avoid stale configuration or data loss. — [doc](https://aws.amazon.com/blogs/media/accelerate-thinkbox-deadline-by-bursting-to-the-cloud-with-amazon-file-cache/)

<!-- meta: last_reviewed=2026-07-05; sources=17 -->
