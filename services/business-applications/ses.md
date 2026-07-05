# Amazon SES — Best Practices

## Common scenarios
- Transactional email (order confirmations, password resets)        → Reliability, Operational Excellence
- Marketing and bulk email campaigns        → Reliability, Cost Optimization
- Multi-tenant SaaS sending on behalf of customers        → Security, Reliability
- Inbound email processing and receipt handling        → Security, Operational Excellence

## 🔒 Security
- **[identity management]** Authenticate every sending domain with SPF, and sign outbound mail with DKIM (Easy DKIM or BYODKIM) — proves to receiving ISPs that your messages are legitimate and unmodified in transit. [doc](https://docs.aws.amazon.com/ses/latest/dg/configure-identities.html)
- **[compliance]** Configure DMARC on your sending domains in addition to SPF and DKIM — reduces the risk of spoofing and improves deliverability with ISPs that enforce DMARC policies. [doc](https://docs.aws.amazon.com/ses/latest/dg/configure-identities.html)
- **[access control]** Use IAM policies to restrict which users or roles can call SES actions, and constrain the "From", recipient, and "Return-Path" addresses they're allowed to use with condition keys such as `ses:FromAddress` — prevents unauthorized or unintended use of verified identities. [doc](https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html)
- **[cross-account access]** Use sending authorization policies (separate from IAM policies) when you need to let another account send on behalf of an identity you own — sending authorization is the only mechanism that grants cross-account use of a verified identity. [doc](https://aws.amazon.com/blogs/messaging-and-targeting/announcing-sending-authorization/)
- **[network isolation]** Connect to the SES SMTP or API endpoint through an interface VPC endpoint powered by AWS PrivateLink instead of the public internet — keeps traffic on the AWS network, removes the need for an internet gateway, and lets you enforce access with security groups and VPC flow logs. [doc](https://docs.aws.amazon.com/ses/latest/dg/send-email-set-up-vpc-endpoints.html)
- **[data in transit]** Set the TLS policy on your configuration sets to `REQUIRE` rather than relying on default opportunistic TLS — ensures messages are only delivered over an encrypted connection instead of silently falling back to plaintext. [doc](https://docs.aws.amazon.com/securityhub/latest/userguide/ses-controls.html)
- **[data at rest]** When receiving email into Amazon S3, enable SES/KMS encryption of stored messages — protects message content written to your bucket, since SES encrypts client-side before the object lands in S3. [doc](https://aws.amazon.com/ses/faqs/)
- **[governance]** Tag SES configuration sets and contact lists with meaningful keys (owner, environment, purpose) — supports ABAC authorization strategies and resource inventory, and avoids putting PII or sensitive data directly in tag values. [doc](https://docs.aws.amazon.com/securityhub/latest/userguide/ses-controls.html)
- **[multi-tenant]** Apply per-tenant reputation policies (Standard or Strict) and monitor tenant sending patterns before enforcing automated pauses — contains reputation damage from a single bad-acting tenant without disrupting well-behaved ones. [doc](https://docs.aws.amazon.com/ses/latest/dg/tenants.html)

## 🛡️ Reliability
- **[sender reputation]** Monitor account-level and per-configuration-set bounce and complaint rates via the SES reputation dashboard, and create CloudWatch alarms on `Reputation.BounceRate` and `Reputation.ComplaintRate` — gives early warning before SES pauses your sending ability. [doc](https://docs.aws.amazon.com/ses/latest/dg/monitor-sender-reputation.html)
- **[list hygiene]** Rely on the account-level (or configuration-set-level) suppression list so SES automatically stops sending to addresses with recent bounce or complaint history — protects reputation and avoids counting repeat failures against your bounce rate. [doc](https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html)
- **[list hygiene]** Implement double opt-in when collecting recipient addresses and validate address format/MX records at signup — reduces hard bounces caused by typos and prevents malicious sign-ups of addresses you don't control. [doc](https://docs.aws.amazon.com/ses/latest/dg/tips-and-best-practices.html)
- **[IP reputation]** Warm up new dedicated IP addresses gradually according to a predefined ramp-up plan (or use dedicated IPs (managed) for automatic, adaptive warm-up) — sudden volume spikes from an unrecognized IP cause ISPs to throttle or block delivery. [doc](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-warming.html)
- **[IP reputation]** Maintain a consistent, predictable sending pattern once an IP is warmed up, sending roughly 1,000 messages a day to each major ISP you care about — inconsistent volume erodes the reputation you built during warm-up. [doc](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip.html)
- **[event handling]** Route bounce, complaint, and delivery events to a configuration set event destination (SNS, CloudWatch, or Kinesis Data Firehose) and process them the same way you handle any other feedback loop — ensures your application reacts to delivery failures instead of silently losing track of them. [doc](https://aws.amazon.com/blogs/ses/introducing-sending-metrics/)
- **[domain separation]** Send different mail streams (marketing vs. transactional) from distinct subdomains — isolates reputation damage so a marketing campaign that trips a spam trap doesn't affect transactional deliverability. [doc](https://docs.aws.amazon.com/ses/latest/dg/tips-and-best-practices.html)

## ⚡ Performance Efficiency
- **[throughput]** Use dedicated IP pools tied to configuration sets when you need predictable, isolated sending capacity for specific mail streams — keeps high-volume or latency-sensitive sends from competing with other traffic on shared IPs. [doc](https://aws.amazon.com/ses/faqs/)
- **[connectivity]** Use a VPC interface endpoint for SES when sending from workloads inside a VPC — avoids the latency and operational overhead of routing through an internet gateway or NAT device. [doc](https://docs.aws.amazon.com/ses/latest/dg/send-email-set-up-vpc-endpoints.html)

## 💰 Cost Optimization
- **[sending strategy]** Use the SES shared IP pool for low or unpredictable volume instead of leasing dedicated IPs — dedicated IPs only pay off once you sustain enough steady volume to keep them warmed up. [doc](https://docs.aws.amazon.com/ses/latest/dg/managed-dedicated-sending.html)
- **[list hygiene]** Suppress and stop sending to chronically bouncing or complaining addresses rather than repeatedly attempting delivery — every send (including ones that bounce) counts toward your sending quota and can trigger unnecessary retries downstream. [doc](https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html)

## ⚙️ Operational Excellence
- **[monitoring]** Set up a CloudWatch alarm on reputation metrics backed by an SNS topic so the right people are notified automatically when bounce or complaint rates approach risky thresholds — enables proactive remediation before SES enforcement action. [doc](https://docs.aws.amazon.com/ses/latest/dg/reputationdashboard-cloudwatch-alarm.html)
- **[monitoring]** Review tenant-level or configuration-set-level sending metrics regularly, even absent active findings, to catch emerging reputation issues early — waiting for an enforcement notification means damage has already occurred. [doc](https://docs.aws.amazon.com/ses/latest/dg/tenants.html)
- **[incident response]** Educate internal teams or downstream tenants on email best practices (opt-in, content quality, unsubscribe handling) and react quickly to reputation findings by investigating root cause immediately — shortens time-to-resolution and limits blast radius of a reputation event. [doc](https://docs.aws.amazon.com/ses/latest/dg/tenants.html)
- **[identity hygiene]** Provide a clear, working way for recipients to unsubscribe or contact you, and avoid generic `no-reply@` addresses as your From/Reply-To — reduces complaint-driven enforcement actions such as sending pauses or review holds. [doc](https://docs.aws.amazon.com/ses/latest/dg/faqs-enforcement.html)

<!-- meta: last_reviewed=2026-07-05; sources=16 -->
