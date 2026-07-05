# Amazon VPC — Best Practices

## Common scenarios
- Isolating application tiers (web/app/data) across public and private subnets        → Security, Reliability
- Multi-AZ production workloads requiring highly available outbound internet access        → Reliability, Cost Optimization
- Private, low-latency access from workloads to AWS services (S3, DynamoDB, etc.)        → Security, Cost Optimization, Performance Efficiency
- Enterprise IP address planning across many VPCs and accounts        → Reliability, Operational Excellence

## 🔒 Security
- **[traffic control layering]** Use security groups as the primary, stateful mechanism for controlling access to instances, and add network ACLs as a stateless, subnet-level secondary control for defense-in-depth. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
- **[subnet exposure]** Place instances that don't need direct internet access in private subnets, and route their outbound traffic through a NAT gateway or bastion host instead of assigning public IPs. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
- **[route hygiene]** Configure subnet route tables with only the minimum routes needed for connectivity, avoiding routes that grant unnecessary access to other subnets or resources. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
- **[administrative access]** Avoid opening administrative ports (such as SSH/22 or RDP/3389) in security groups to broad IP ranges; use AWS Systems Manager Session Manager for remote access instead of exposing inbound management ports. [doc](https://aws.amazon.com/blogs/security/practical-steps-to-minimize-key-exposure-using-aws-security-services/)
- **[Availability Zone spread]** Create subnets in multiple Availability Zones when hosting an application in a VPC, since this is foundational to both security segmentation and fault tolerance. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[IAM access]** Manage access to VPC resources and APIs using IAM identity federation, users, and roles instead of long-lived shared credentials. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[traffic visibility]** Enable VPC Flow Logs to monitor IP traffic to and from a VPC, subnet, or network interface, and use the logs to detect anomalies or unintended access. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[unintended access detection]** Use Network Access Analyzer to identify unintended network access paths to sensitive resources in your VPCs. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[perimeter defense]** Use AWS Network Firewall to filter inbound and outbound traffic at the VPC perimeter for threats that security groups and NACLs don't cover. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[threat detection]** Enable Amazon GuardDuty, which analyzes VPC Flow Logs for your EC2 instances, to detect potential threats across your accounts and workloads. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- **[private AWS service access]** Use VPC endpoints (AWS PrivateLink) so traffic to supported AWS services stays on the Amazon network instead of traversing an internet gateway or NAT gateway. [doc](https://aws.amazon.com/privatelink/faqs/)
- **[endpoint access control]** Attach endpoint policies to VPC endpoints, combined with IAM identity-based policies, to restrict which principals and actions are allowed through the endpoint. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/streamline-access-to-most-used-aws-services-using-vpc-endpoints/)

## 🛡️ Reliability
- **[NAT gateway redundancy]** Deploy a NAT gateway in each Availability Zone that has private subnets needing outbound access, since NAT gateway high availability is confined to a single AZ. [doc](https://aws.amazon.com/blogs/architecture/one-to-many-evolving-vpc-design/)
- **[AZ-independent routing]** Route each private subnet to the NAT gateway in its own Availability Zone so that the loss of one AZ doesn't take down egress for workloads in other AZs. [doc](https://aws.amazon.com/blogs/mt/validating-and-improving-the-rto-and-rpo-using-aws-resilience-hub/)
- **[IP space planning]** Size VPC and subnet CIDR blocks to accommodate future growth and multi-AZ expansion, and leave unused CIDR space rather than allocating the minimum needed today. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_network_topology_ip_subnet_allocation.html)
- **[non-overlapping IP ranges]** Plan private IP ranges (per RFC 1918) so VPCs, on-premises networks, and other connected environments never overlap, avoiding routing conflicts when networks are peered or connected. [doc](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_network_topology_ip_subnet_allocation.html)
- **[centralized IPAM]** Use Amazon VPC IP Address Manager (IPAM) to organize, allocate, monitor, and audit IP address usage across many VPCs and accounts as your environment scales. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/aws-network-optimization-tips/)
- **[hybrid connectivity]** Use AWS Site-to-Site VPN or AWS Direct Connect for private, resilient connections between your VPCs and on-premises networks instead of routing that traffic over the public internet. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)

## ⚡ Performance Efficiency
- **[workload placement]** Choose the AWS Region, Local Zone, Outpost, or Wavelength zone for your VPC based on where your users are, and keep high-throughput, low-latency traffic flows inside the same VPC. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_networking_choose_workload_location_network_requirements.html)
- **[low-latency clustering]** Use EC2 placement groups (cluster) with enhanced networking (ENA) for workloads that need low latency and high throughput between instances in the same VPC. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_networking_choose_workload_location_network_requirements.html)
- **[edge acceleration]** Use edge services such as Amazon CloudFront and AWS Global Accelerator to cache content and route users over the AWS global network, reducing latency into your VPC-hosted workloads. [doc](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_networking_choose_workload_location_network_requirements.html)
- **[NAT gateway locality]** Keep resources in the same Availability Zone as the NAT gateway they use, or provision one NAT gateway per AZ, to avoid added cross-AZ latency and data transfer. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html)

## 💰 Cost Optimization
- **[NAT gateway vs. endpoints]** Replace NAT gateway usage with VPC gateway endpoints (no hourly or data-processing charge) for S3 and DynamoDB traffic, and interface endpoints for other supported AWS services when most NAT traffic targets AWS APIs. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html)
- **[NAT gateway right-sizing]** Use a single NAT gateway for non-production environments and one NAT gateway per Availability Zone only where production resiliency requires it, and monitor utilization to avoid over-provisioning. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html)
- **[cross-AZ data transfer]** Co-locate chatty resources within the same Availability Zone where possible, since inter-AZ traffic within a VPC incurs data transfer charges. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/designing-hyperscale-amazon-vpc-networks/)
- **[unused resource cleanup]** Regularly review and delete unused VPCs, subnets, security groups, NAT gateways, and other network resources to reduce both cost and unintended exposure. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-09.html)
- **[cost visibility]** Use AWS Cost Explorer to track NAT gateway and data-transfer costs and identify where switching to VPC endpoints or adjusting architecture would reduce spend. [doc](https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_data_transfer_implement_services.html)

## ⚙️ Operational Excellence
- **[network address planning]** Delegate administration of Amazon VPC IPAM to a central network account so IP assignment across the organization stays consistent and auditable. [doc](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-vpc-ip-address-manager-best-practices/)
- **[proactive IP alerts]** Configure CloudWatch alerts on IPAM metrics to catch conflicting or exhausted IP address ranges before they cause deployment failures. [doc](https://docs.aws.amazon.com/vpc/latest/ipam/cloudwatch-ipam.html)
- **[flow log analysis]** Send VPC Flow Logs to CloudWatch Logs or S3 and use CloudWatch Logs Insights or Athena queries to troubleshoot connectivity issues and understand traffic patterns. [doc](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html)
- **[reject-traffic alarms]** Create a CloudWatch alarm on a VPC Flow Logs metric filter for REJECT actions so you're notified of unauthorized or unexpectedly blocked traffic. [doc](https://docs.aws.amazon.com/vpc/latest/userguide/process-records-cwl.html)
- **[centralized dashboards]** Build CloudWatch dashboards that aggregate network metrics and flow log-derived data across Regions into a single operational view. [doc](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
