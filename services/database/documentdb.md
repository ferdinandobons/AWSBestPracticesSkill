# Amazon DocumentDB — Best Practices

## Common scenarios
- JSON document workloads migrated from self-managed MongoDB        → Reliability, Performance Efficiency
- Content management, catalog, and profile stores needing flexible schema        → Performance Efficiency, Cost Optimization
- High-availability operational databases requiring automatic failover        → Reliability
- Multi-tenant applications needing per-database access isolation        → Security

## 🔒 Security
- **[access control]** Enforce least privilege with role-based access control (RBAC) so each Amazon DocumentDB database user only has the permissions needed for their duties. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security_best_practices.html)
- **[IAM]** Assign an individual IAM account to each person who manages Amazon DocumentDB resources instead of the AWS account root user, and grant each user only the minimum permissions required. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security_best_practices.html)
- **[IAM]** Use IAM groups to manage permissions for multiple users consistently rather than assigning permissions to individuals one by one. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security_best_practices.html)
- **[credential rotation]** Regularly rotate IAM credentials and configure AWS Secrets Manager to automatically rotate the secrets used for Amazon DocumentDB authentication. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security_best_practices.html)
- **[encryption]** Use Transport Layer Security (TLS) to encrypt data in transit and AWS KMS to encrypt data at rest for every cluster. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security_best_practices.html)
- **[auditing]** Enable AWS CloudTrail to track control-plane API calls and enable Amazon DocumentDB auditing to CloudWatch Logs to capture DDL, DML, authentication, authorization, and user-management events. [doc](https://aws.amazon.com/blogs/gametech/game-developers-guide-to-amazon-documentdb-with-mongodb-compatibility-part-three-operation-best-practices/)
- **[least privilege]** Restrict sensitive management actions such as DeleteCluster, DeleteClusterSnapshot, and UpdateCluster to authorized IAM principals, and monitor them via CloudWatch and CloudTrail. [doc](https://aws.amazon.com/blogs/industries/financial-services-spotlight-featuring-amazon-documentdb/)

## 🛡️ Reliability
- **[cluster topology]** Deploy a cluster with two or more instances across two or more Availability Zones, and use three or more instances across three Availability Zones for production workloads. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[failover targets]** Provision one or more replicas as failover targets, using the same instance class as the primary and placing them in different Availability Zones, since promoting a replica is much faster than re-creating the primary. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/how-it-works.html)
- **[connectivity]** Connect using the cluster endpoint and in replica-set mode, and design applications to retry transient errors with exponential backoff, to minimize the impact of failover on your application. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[failover testing]** Periodically test failover for your cluster to understand how long the process takes for your specific use case. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[deletion protection]** Enable cluster deletion protection for production clusters or any cluster with valuable data, and take a final snapshot before deleting a cluster. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[backups]** Set your backup retention period to align with your recovery point objective, and use point-in-time recovery to protect against accidental writes or deletes. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/security.disaster-recovery-resiliency.html)
- **[engine version]** Explicitly specify the `--engine-version` for production clusters, especially those driven by scripting, automation, or CloudFormation, instead of relying on the default version. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[capacity monitoring]** Monitor memory, CPU, connections, and storage usage with CloudWatch, and scale up instances proactively before you approach capacity limits. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)

## ⚡ Performance Efficiency
- **[instance sizing]** Choose an instance type with enough RAM to fit your working set (data and indexes) in memory, since Amazon DocumentDB reserves one-third of instance RAM for its own services. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[cache monitoring]** Monitor the `BufferCacheHitRatio` CloudWatch metric per instance and scale up when it is lower than expected, to avoid costly repeated reads from the storage volume. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[read/write isolation]** Direct operational queries to the primary instance and analytic or scan-heavy queries to replica instances to isolate their buffer cache impact from each other. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[read scaling]** Choose a driver read preference such as `secondaryPreferred` to enable replica reads and free up the primary instance to do more work. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[indexing]** Create indexes before importing large datasets, and limit index creation to fields with high selectivity (duplicate values under roughly 1% of collection size) to keep index scans efficient. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[index count]** Keep the number of indexes per collection low (five or fewer as a guideline), since every additional index adds write latency and I/O on every insert, update, and delete. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[index hygiene]** Regularly identify missing indexes to improve slow queries and identify unused indexes to remove ones that only add overhead. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[TTL and change streams]** Deactivate TTL indexes and change streams when not actually used by your application, since both features add I/O on reads, inserts, updates, and deletes. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)

## 💰 Cost Optimization
- **[billing alerts]** Create billing alerts at 50 percent and 75 percent of your expected monthly bill to catch cost overruns early. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[dev/test sizing]** Use single-instance clusters for development and test environments when high availability is not required, since Amazon DocumentDB's separated storage/compute architecture keeps even single-instance clusters highly durable. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[pause non-prod clusters]** Stop clusters that are not in active use (such as dev/test clusters over a weekend) for up to seven days, since you are not charged for instance hours while stopped. [doc](https://aws.amazon.com/blogs/gametech/game-developers-guide-to-amazon-documentdb-with-mongodb-compatibility-part-three-operation-best-practices/)
- **[unused features]** Disable TTL indexes and change streams when they are enabled but not used by the application, to eliminate the additional I/O cost they incur. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[cost tracking]** Tag clusters and instances so you can track instance, storage, IOPS, and backup storage costs at a granular level using cost allocation tags. [doc](https://aws.amazon.com/blogs/gametech/game-developers-guide-to-amazon-documentdb-with-mongodb-compatibility-part-three-operation-best-practices/)
- **[data archival]** Archive infrequently accessed data out of the cluster to lower-cost storage such as Amazon S3 rather than keeping it in operational storage indefinitely. [doc](https://aws.amazon.com/blogs/gametech/game-developers-guide-to-amazon-documentdb-with-mongodb-compatibility-part-three-operation-best-practices/)
- **[scheduled scaling]** Schedule cluster scaling to match anticipated read traffic patterns so you avoid overprovisioning capacity that sits idle outside peak periods. [doc](https://aws.amazon.com/blogs/database/optimize-costs-with-scheduled-scaling-of-amazon-documentdb-for-read-workloads/)

## ⚙️ Operational Excellence
- **[service limits]** Operate within the documented Amazon DocumentDB quotas and limits, and monitor usage so you can act before hitting capacity or throttling boundaries. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[monitoring and alarms]** Set up Amazon CloudWatch alarms on memory, CPU, connections, and storage so you are notified automatically when usage patterns change or capacity is approached. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[query tuning]** Use CloudWatch performance metrics to evaluate instance usage, then tune slow-running queries based on the findings. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[parameter groups]** Manage engine configuration through cluster parameter groups so configuration changes are consistent, versioned, and repeatable across clusters. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[migrations]** Use the Amazon DocumentDB Index Tool to extract indexes from a source MongoDB instance or `mongodump` directory and recreate them before migrating data. [doc](https://docs.aws.amazon.com/documentdb/latest/devguide/best_practices.html)
- **[auditing]** Enable Amazon DocumentDB auditing to CloudWatch Logs and integrate with CloudTrail so database and API actions are tracked for operational and security review. [doc](https://aws.amazon.com/blogs/gametech/game-developers-guide-to-amazon-documentdb-with-mongodb-compatibility-part-three-operation-best-practices/)

<!-- meta: last_reviewed=2026-07-05; sources=7 -->
