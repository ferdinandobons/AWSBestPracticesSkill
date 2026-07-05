# AWS Network Firewall — Best Practices

## Common scenarios
- Filtering inbound/outbound VPC perimeter traffic at internet or NAT gateways        → Security, Reliability
- Blocking egress to known malware/botnet domains and IPs for compliance        → Security, Cost Optimization
- Inspecting traffic between subnets or tiers (segmentation) within a VPC        → Security, Performance Efficiency
- Centralizing firewall policy across many accounts and VPCs with Firewall Manager        → Operational Excellence, Security

## 🔒 Security
- **[traffic control layering]** Use a defense-in-depth approach that combines AWS Network Firewall with AWS WAF and VPC security groups, since Network Firewall covers stateful VPC-perimeter inspection while WAF handles Layer 7 HTTP protection. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-controls-by-caf-capability/infrastructure-controls.html)
- **[rule evaluation order]** Configure firewall policies and rule groups to use `STRICT_ORDER` rule evaluation so rules run in the exact sequence you define, rather than relying on the less predictable default action order. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html)
- **[managed rule adoption]** Use AWS managed domain/IP and threat-signature rule groups to block traffic to known malware, botnet, and low-reputation domains, and keep them updated as AWS refreshes the rule content. [doc](https://aws.amazon.com/blogs/security/keep-your-firewall-rules-up-to-date-with-network-firewall-features/)
- **[safe rule rollout]** Test new or modified managed and custom rule groups in alert mode (or in a staging environment) before switching them to drop/reject in production, to avoid blocking legitimate traffic. [doc](https://aws.amazon.com/blogs/awsforsap/securing-sap-with-aws-network-firewall-part-2-managed-rules/)
- **[centralized policy management]** Use AWS Firewall Manager to deploy and enforce consistent Network Firewall policies across AWS Organizations accounts and Regions so new accounts and resources are automatically protected. [doc](https://aws.amazon.com/blogs/awsforsap/securing-sap-with-aws-network-firewall-part-2-managed-rules/)
- **[TLS visibility]** Configure TLS inspection for encrypted traffic where you need Layer 7 visibility into HTTPS sessions, since domain filtering alone only inspects the TLS SNI field. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/firewall-logging.html)
- **[least-privilege IAM]** Grant IAM identities only the specific Network Firewall actions and resources they need, starting from AWS managed policies and narrowing to customer-managed least-privilege policies as usage patterns become clear. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/security_iam_id-based-policy-examples.html)
- **[policy validation]** Use IAM Access Analyzer to validate identity-based policies for Network Firewall so they grant only intended, functional permissions. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/security_iam_id-based-policy-examples.html)
- **[condition-based access]** Add IAM policy conditions (such as requiring SSL/TLS or restricting access to specific AWS services) to further scope who can manage Network Firewall resources. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/security_iam_id-based-policy-examples.html)

## 🛡️ Reliability
- **[multi-AZ deployment]** Deploy firewall endpoints in at least two Availability Zones for production workloads so a single AZ failure doesn't remove inspection coverage or create a single point of failure. [doc](https://docs.aws.amazon.com/securityhub/latest/userguide/networkfirewall-controls.html)
- **[dedicated firewall subnets]** Reserve firewall endpoint subnets exclusively for Network Firewall and don't place other resources in them, since an endpoint can't filter traffic to or from its own subnet. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/vpc-config-subnets.html)
- **[symmetric routing]** Ensure stateless rules and the policy's default action forward both request and response traffic to the stateful engine symmetrically, since asymmetric forwarding triggers the stream exception policy and can drop legitimate connections. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/troubleshooting-general-issues.html)
- **[stream exception policy]** Explicitly choose a stream exception policy (DROP, REJECT, or CONTINUE) that matches your availability requirements for traffic whose state is lost mid-stream, rather than relying on the default fail-closed behavior without review. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/stream-exception-policy.html)
- **[bandwidth planning]** Plan for the per-Availability-Zone bandwidth limit, which is shared across all VPC endpoints in that AZ, and split resources across additional subnets/endpoints if you need more throughput. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/vpc-config-subnets.html)

## ⚡ Performance Efficiency
- **[rule set sizing]** Keep the number of stateful rules and IPS signatures no larger than necessary, since rule count directly affects inspection latency and throughput. [doc](https://aws.amazon.com/blogs/awsforsap/securing-sap-with-aws-network-firewall-part-2-managed-rules/)
- **[selective inspection scope]** Scope traffic inspection to where it adds security value (for example, perimeter or cross-tier boundaries) and avoid inspecting latency-sensitive intra-application traffic that doesn't need it. [doc](https://aws.amazon.com/blogs/awsforsap/securing-sap-with-aws-network-firewall-part-2-managed-rules/)
- **[capacity validation]** Test your rule set against expected traffic volume before production cutover, since Network Firewall scales automatically but a single oversubscribed endpoint can still see degraded performance. [doc](https://aws.amazon.com/network-firewall/faqs/)
- **[latency troubleshooting]** Monitor `PacketsDropped`, `ReceivedPackets`, and `StreamExceptionPolicyPackets` CloudWatch metrics to identify oversubscribed endpoints or asymmetric-routing issues causing latency or packet loss. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/troubleshooting-general-issues.html)

## 💰 Cost Optimization
- **[log type selection]** Enable only the log types you need (flow vs. alert) since flow logs capture all traffic forwarded to the stateful engine while alert logs capture only rule matches, and each has different volume and cost profiles. [doc](https://aws.amazon.com/blogs/security/cost-considerations-and-common-options-for-aws-network-firewall-log-management/)
- **[log destination choice]** Choose your logging destination (CloudWatch Logs, S3, or Kinesis Data Firehose) based on query needs and retention cost, since vended log pricing and query costs vary by destination. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/firewall-logging-pricing.html)
- **[dashboard query limits]** Limit how often you refresh or adjust the time range on the firewall monitoring dashboard, since each update triggers a new query against your logging destinations and incurs additional charges. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/nwfw-using-dashboard.html)
- **[cross-AZ traffic]** Avoid routing traffic to a firewall endpoint in a different Availability Zone than the originating resource, since this incurs cross-zone data transfer charges. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html)

## ⚙️ Operational Excellence
- **[automated monitoring]** Automate Network Firewall monitoring using CloudWatch metrics/alarms, CloudWatch Logs, CloudTrail, and AWS Config rather than relying on manual checks. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/logging-monitoring.html)
- **[alert and flow logging]** Enable both alert and flow logs so you have stateful match details (drops, rejects, alerts) alongside traffic flow trends for troubleshooting and incident response. [doc](https://docs.aws.amazon.com/network-firewall/latest/developerguide/firewall-logging.html)
- **[compliance-as-code]** Use the AWS Config conformance pack for Network Firewall to continuously evaluate your firewalls against security best-practice rules. [doc](https://docs.aws.amazon.com/config/latest/developerguide/security-best-practices-for-Network-Firewall.html)
- **[multi-account governance]** Use AWS Firewall Manager to keep firewall rules consistently enforced as new accounts and resources are created in your organization. [doc](https://aws.amazon.com/blogs/awsforsap/securing-sap-with-aws-network-firewall-part-2-managed-rules/)

<!-- meta: last_reviewed=2026-07-05; sources=13 -->
