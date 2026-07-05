# Sustainability — Best Practices

## Common scenarios
- Choosing an AWS Region for a new workload that balances latency, compliance, and carbon intensity        → Region Selection
- Right-sizing and scaling infrastructure so provisioned capacity tracks actual demand        → Alignment to Demand
- Refactoring application code and architecture to cut wasted compute and idle resources        → Software & Architecture Patterns
- Deciding how long to retain data, which storage tier to use, and when to delete it        → Data Management
- Picking instance types, accelerators, and managed services with the lowest environmental impact        → Hardware & Managed Services
- Building sustainability checks into CI/CD, testing, and organizational processes        → Process & Culture
- Measuring and reporting on the carbon footprint of AWS usage        → Measurement & Reporting

## Region Selection
- **[new workload placement]** Choose the AWS Region for a workload based on both business requirements (latency, data residency, cost) and sustainability goals, favoring Regions where it reduces the estimated carbon footprint. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/w2aac19c17b7b5.html)
- **[shared responsibility]** Treat sustainability as a shared responsibility: AWS is responsible for the sustainability *of* the cloud (efficient data centers, progress toward renewable energy), while you are responsible for sustainability *in* the cloud (how efficiently your workload uses the resources it consumes). [doc](https://aws.amazon.com/blogs/aws/sustainability-pillar-well-architected-framework/)

## Alignment to Demand
- **[dynamic scaling]** Scale workload infrastructure dynamically (auto scaling, serverless) so provisioned capacity continually matches real demand instead of being sized for peak or worst case. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html)
- **[SLA calibration]** Align service-level agreements (availability, durability, recovery targets) with actual business need rather than defaulting to maximum levels — over-specified SLAs force extra redundant resources that consume energy without adding business value. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html)
- **[decommission unused assets]** Stop the creation and maintenance of unused assets (orphaned volumes, snapshots, idle environments) so they don't continue consuming resources after they stop delivering value. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html)
- **[network-aware placement]** Optimize the geographic placement of workload components based on their networking requirements, positioning resources to minimize the network path between users, applications, and the data they consume. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html)
- **[demand flattening]** Implement buffering or throttling (queues, rate limiting) to flatten spiky demand curves so infrastructure can be sized closer to average load instead of peak load. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/alignment-to-demand.html)

## Software & Architecture Patterns
- **[async and scheduled work]** Optimize software and architecture for asynchronous and scheduled jobs so time-flexible work can run when it makes the best use of available capacity, rather than requiring constantly-on synchronous resources. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-03.html)
- **[retire dead weight]** Remove or refactor workload components that show low or no use — idle components still consume provisioned capacity and add sustainability impact without business benefit. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-03.html)
- **[code hotspot optimization]** Profile your workload and optimize the areas of code that consume the most time or resources, since a small number of hot paths typically dominate overall energy and resource use. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-03.html)
- **[minimize device impact]** Design software to minimize the impact on customer devices and equipment (for example, reducing processing or rendering load on client devices) so customers aren't driven toward unnecessary device upgrades. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-03.html)
- **[storage-pattern-fit architecture]** Use software patterns and architectures that best support your actual data access and storage patterns instead of a one-size-fits-all approach, so the underlying infrastructure isn't over-provisioned to handle mismatched access patterns. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-03.html)

## Data Management
- **[classification policy]** Implement a data classification policy so you understand the value and required durability/performance of each dataset, which is the basis for choosing an appropriately efficient storage approach. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[access-pattern storage fit]** Use storage technologies and configurations that match the actual data access and storage patterns of the workload rather than defaulting to the highest-performance tier for all data. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[lifecycle policies]** Use lifecycle policies to automatically transition datasets to more efficient, less performant storage tiers as their access frequency and business value decline over time. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[elastic storage]** Use elasticity and automation to expand (and shrink) block storage or file systems in line with actual usage, instead of statically over-provisioning capacity. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[delete redundant data]** Remove unneeded or redundant data — duplicate copies, stale exports, and obsolete datasets consume storage and the energy to maintain it with no offsetting value. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[shared storage]** Use shared file systems or shared storage to access common data across multiple consumers instead of duplicating the same dataset for each consumer. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[minimize data movement]** Minimize data movement across networks by processing data close to where it's stored and by choosing architectures that avoid unnecessary transfers between Regions, Availability Zones, or services. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)
- **[selective backup]** Back up data only when it is difficult or costly to recreate, and align backup frequency and retention to actual recovery requirements rather than backing up everything indefinitely. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-04.html)

## Hardware & Managed Services
- **[minimum hardware footprint]** Use the minimum amount of hardware needed to meet workload requirements, and update deployed components as needs change rather than leaving excess capacity provisioned indefinitely. [doc](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/sus-hardware-patterns.html)
- **[efficient instance types]** Continually monitor and adopt newer instance types with the least sustainability impact, including instance families purpose-built for workloads like machine learning training/inference and video transcoding, as energy efficiency improves generation over generation. [doc](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/sus-hardware-patterns.html)
- **[prefer managed services]** Prefer managed services over self-managed infrastructure — managed services shift responsibility for maintaining high average utilization and hardware efficiency to AWS, spreading the sustainability impact across all tenants of the service. [doc](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/sus-hardware-patterns.html)
- **[GPU/accelerator efficiency]** Optimize your use of GPUs and other hardware-based compute accelerators by running them only for the time actually needed and decommissioning them automatically when idle, since these accelerators are a significant source of power consumption. [doc](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/sus-hardware-patterns.html)

## Process & Culture
- **[cascade sustainability goals]** Communicate and cascade sustainability goals across the organization so development, test, and operations teams factor environmental impact into everyday decisions, not just architecture reviews. [doc](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/process-and-culture.html)
- **[rapid, low-cost testing]** Adopt development and deployment practices that can rapidly test, validate, and introduce sustainability improvements, accounting for the cost of testing against the expected future benefit of each improvement. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-development-deployment-patterns.html)
- **[stay current]** Keep operating systems, libraries, and applications up to date, since newer versions often improve workload efficiency and add better instrumentation for measuring sustainability impact. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-development-deployment-patterns.html)
- **[ephemeral build/test environments]** Increase utilization of build and test environments by using automation and infrastructure as code to bring them up only when needed (for example, scheduled to match working hours) and take them down otherwise, using Spot Instances, burstable instance types, or hibernation where suitable. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-development-deployment-patterns.html)
- **[managed device farms]** Use managed device farms for testing rather than maintaining a private device lab — this spreads the sustainability impact of hardware manufacturing across tenants and gives access to older device types without forcing unnecessary customer device upgrades. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-development-deployment-patterns.html)

## Measurement & Reporting
- **[track carbon footprint]** Use the AWS Customer Carbon Footprint Tool to measure, track, and forecast the carbon emissions (Scope 1 and Scope 2) associated with your AWS usage, broken down by month, service, and geography. [doc](https://aws.amazon.com/blogs/aws/new-customer-carbon-footprint-tool/)
- **[regional emissions detail]** Review carbon emissions broken out by AWS Region to understand how usage in different Regions contributes to your overall footprint, and use that detail to inform targeted reduction strategies. [doc](https://docs.aws.amazon.com/ccft/latest/releasenotes/what-is-ccftrn.html)
- **[export for analysis at scale]** Configure automated Carbon Data Exports to Amazon S3 (CSV or Parquet, account- and Region-level detail) so sustainability and finance teams can analyze emissions with existing BI and reporting tooling instead of manual data pulls. [doc](https://docs.aws.amazon.com/ccft/latest/releasenotes/what-is-ccftrn.html)

<!-- meta: last_reviewed=2026-07-05; sources=10 -->
