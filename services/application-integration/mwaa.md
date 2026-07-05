# Amazon MWAA — Best Practices

## Common scenarios
- Orchestrating multi-step ETL/ELT data pipelines across AWS services (EMR, Glue, Redshift)        → Reliability, Operational Excellence
- Scheduling and monitoring DAG-based workflows at scale with autoscaled workers        → Performance Efficiency, Cost Optimization
- Running Apache Airflow in a private, regulated network without managing servers        → Security, Reliability
- Coordinating cross-account or cross-region data processing and ML pipelines        → Reliability, Operational Excellence

## 🔒 Security
- **[access control]** Grant least-privilege identity and execution role policies, scoping permissions to only the resources or actions users and the environment actually need. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/security-best-practices.html)
- **[audit logging]** Use AWS CloudTrail to monitor user activity in your account, including changes to environments and Airflow role/permission assignments. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/security-best-practices.html)
- **[S3 bucket policy]** Ensure the environment's Amazon S3 bucket policy and object ACLs grant permissions to the same users who need to run the corresponding DAGs in Airflow — keeps upload and execution permissions aligned. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/security-best-practices.html)
- **[bucket isolation]** Use the S3 bucket associated with an Amazon MWAA environment for that environment only — don't store unrelated objects in it or share it with another service. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/security-best-practices.html)
- **[network isolation]** Use private web server access mode so the Airflow UI is only reachable from within your VPC, avoiding the need for a NAT gateway path to the public internet. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-security.html)
- **[least-privilege networking]** Tighten security groups, network ACLs, and VPC endpoint policies around the Amazon MWAA environment to restrict traffic to only what schedulers and workers require. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-least-privilege-configuration-in-amazon-mwaa/)
- **[VPC endpoints]** Use interface VPC endpoints with restrictive endpoint policies for private routing to Amazon MWAA and dependent services instead of routing through the public internet. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-security.html)

## 🛡️ Reliability
- **[built-in HA]** Rely on the default Multi-AZ architecture — Amazon MWAA runs multiple schedulers, autoscaled workers, and a metadata database distributed across multiple Availability Zones — rather than building custom redundancy. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/disaster-recovery-resiliency.html)
- **[subnet design]** Deploy environments across two private subnets in two different Availability Zones to meet Amazon MWAA's Availability Zone failure tolerance requirement. [doc](https://aws.amazon.com/blogs/big-data/combine-aws-glue-and-amazon-mwaa-to-build-advanced-vpc-selection-and-failover-strategies/)
- **[DAG idempotency]** Design DAGs and tasks to be idempotent so every workflow run produces consistent results, including idempotent reads/writes to and from partitions. [doc](https://docs.aws.amazon.com/whitepapers/latest/aws-glue-best-practices-build-efficient-data-pipeline/building-an-operationally-excellent-data-pipeline.html)
- **[disaster recovery]** For Regional-outage resilience beyond the built-in Multi-AZ HA, implement a backup-and-restore or warm-standby multi-Region strategy for critical environments. [doc](https://aws.amazon.com/blogs/big-data/disaster-recovery-strategies-for-amazon-mwaa-part-2/)
- **[concurrency after scaling]** After changing environment class, manually update worker concurrency settings (e.g., `celery.worker_autoscale`) — Amazon MWAA does not automatically raise the per-worker concurrency default when you scale an existing environment. [doc](https://aws.amazon.com/blogs/big-data/a-guide-to-airflow-worker-pool-optimization-in-amazon-mwaa/)

## ⚡ Performance Efficiency
- **[environment sizing]** Right-size the environment class (mw1.small through mw1.2xlarge) based on CloudWatch CPU/memory utilization and observed task concurrency needs, rather than defaulting to a larger class. [doc](https://aws.amazon.com/blogs/big-data/optimize-cost-and-performance-for-amazon-mwaa/)
- **[scheduler tuning]** Tune scheduler parameters such as `scheduler.parsing_processes`/`dag_processor.parsing_processes` and `scheduler.scheduler_idle_sleep_time` based on observed DAG parse times and CPU usage, keeping parsing-process counts under the vCPU limit for the environment class. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-tuning.html)
- **[DAG folder scanning]** Increase `scheduler.dag_dir_list_interval`/`dag_processor.refresh_interval` and `min_file_process_interval` when you have a large number of DAG files, to reduce unnecessary scheduler CPU load from repeated parsing. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-tuning.html)
- **[bottleneck diagnosis]** Distinguish configuration-imposed throttles (`max_active_runs_per_dag`, DAG/task concurrency, pools) from true resource constraints before scaling infrastructure — adjusting configuration often resolves throughput issues without adding workers. [doc](https://aws.amazon.com/blogs/big-data/a-guide-to-airflow-worker-pool-optimization-in-amazon-mwaa/)
- **[workload analysis]** Analyze DAG schedules, task concurrency, and task runtimes using CloudWatch metrics and Airflow logs to identify long-running tasks and bottlenecks before choosing worker autoscaling limits. [doc](https://aws.amazon.com/blogs/big-data/optimize-cost-and-performance-for-amazon-mwaa/)

## 💰 Cost Optimization
- **[right-sizing]** Continuously monitor container, queue, and database utilization metrics in CloudWatch and adjust environment class and min/max workers to match actual workload demand instead of over-provisioning. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/accessing-metrics-cw-container-queue-db.html)
- **[autoscaling limits]** Set worker autoscaling minimum and maximum bounds based on measured concurrent task needs so idle capacity isn't paid for during low-activity periods. [doc](https://aws.amazon.com/blogs/big-data/optimize-cost-and-performance-for-amazon-mwaa/)
- **[configuration tuning]** Fine-tune Airflow configuration parameters (parallelism, logging verbosity, DAG code efficiency) as part of cost optimization, since inefficient configuration can drive unnecessary compute consumption. [doc](https://aws.amazon.com/blogs/big-data/optimize-cost-and-performance-for-amazon-mwaa/)

## ⚙️ Operational Excellence
- **[dependency management]** Manage Python dependencies through a versioned `requirements.txt` in the environment's S3 bucket, using `--constraint` files matched to your Airflow/Python version to keep installs reproducible. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-dependencies.html)
- **[private webserver dependencies]** Package dependencies into a `plugins.zip` when using a private web server (no PyPI internet access), and keep the packaged zip static until explicitly rebuilt. [doc](https://aws.amazon.com/blogs/big-data/amazon-mwaa-best-practices-for-managing-python-dependencies/)
- **[observability]** Monitor scheduler, worker, web server, queue, and database metrics (CPU, memory, connections, queue depth) in CloudWatch, and set alarms on key thresholds to catch capacity issues before they cause DAG failures. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/accessing-metrics-cw-container-queue-db.html)
- **[log retention]** Use the 15 months of retained CloudWatch metrics history to investigate recurring schedule failures and long-term capacity trends rather than relying only on recent data. [doc](https://docs.aws.amazon.com/mwaa/latest/userguide/accessing-metrics-cw-container-queue-db.html)
- **[least privilege at scale]** Separate execution and deployment IAM roles with narrowly scoped permissions, and periodically review them as environments and teams grow. [doc](https://aws.amazon.com/blogs/big-data/best-practices-for-least-privilege-configuration-in-amazon-mwaa/)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
