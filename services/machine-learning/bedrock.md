# Amazon Bedrock — Best Practices

## Common scenarios
- Building generative AI chat/RAG applications with foundation models        → Security, Performance Efficiency, Cost Optimization
- Running agentic workflows with Bedrock Agents and Knowledge Bases        → Security, Reliability, Operational Excellence
- Batch document processing, summarization, and classification at scale        → Cost Optimization, Sustainability
- Enterprise deployments requiring governance, audit, and compliance        → Security, Operational Excellence

## 🔒 Security
- **[access control]** Grant least-privilege IAM permissions scoped to specific model ARNs and actions rather than broad `AmazonBedrockFullAccess` grants — reduces blast radius if credentials are compromised. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)
- **[agents]** Implement least-privilege access to Amazon Bedrock Agents resources and always use encrypted (`https://`) connections — helps prevent security incidents in agentic workflows. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/security-best-practice-agents.html)
- **[data protection]** Avoid including personally identifiable information (PII) in agent resource fields that don't support customer managed keys (for example action group or knowledge base names) — only fields supporting CMK encryption should carry sensitive data. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/security-best-practice-agents.html)
- **[guardrails]** Configure Amazon Bedrock Guardrails with content filters, denied topics, word filters, and PII redaction across every application, regardless of underlying model — provides a consistent responsible-AI safety layer. [doc](https://aws.amazon.com/blogs/publicsector/how-to-safeguard-healthcare-data-privacy-using-amazon-bedrock-guardrails/)
- **[guardrails]** Encrypt guardrails with a customer managed AWS KMS key instead of the default AWS managed key, and restrict who can view or modify guardrail configurations with least-privilege IAM — prevents unauthorized tampering with safety controls. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/gen-ai-sra.html)
- **[network]** Use AWS PrivateLink interface VPC endpoints to connect your VPC privately to Amazon Bedrock — removes the need for an internet gateway, NAT device, VPN, or Direct Connect and keeps traffic on the AWS network. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html)
- **[network]** Protect model customization, batch inference, and Knowledge Bases jobs by running them inside a VPC and monitoring traffic with VPC Flow Logs — limits data exposure to the internet. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html)
- **[transport]** Require TLS 1.2 (recommend TLS 1.3) with cipher suites supporting perfect forward secrecy, and sign every request with IAM credentials or AWS STS temporary credentials — Amazon Bedrock has no non-TLS endpoint. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/infrastructure-security.html)

## 🛡️ Reliability
- **[scaling]** Use cross-Region inference profiles to distribute traffic across multiple AWS Regions — increases aggregate throughput beyond single-Region quotas and reduces the likelihood of throttling during traffic bursts. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- **[scaling]** Update Service Control Policies and IAM policies to explicitly allow required Bedrock inference actions in every destination Region of your chosen inference profile — a blocked destination Region causes the whole request to fail even if other Regions are allowed. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
- **[capacity]** Purchase Provisioned Throughput for production workloads that need consistent, guaranteed throughput for base, fine-tuned, or continued pre-trained models beyond on-demand quota limits. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/scaling-throughput-best-practices.html)
- **[quotas]** Ramp up traffic gradually rather than sending large bursts immediately — on-demand throughput availability scales over time and not all requests within your quota are guaranteed to succeed during periods of high demand. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/scaling-throughput-best-practices.html)

## ⚡ Performance Efficiency
- **[model selection]** Use Amazon Bedrock Evaluations (automatic and human evaluation) to compare accuracy, robustness, toxicity, and use-case-specific metrics across candidate foundation models before committing to one — turns model choice into a measured decision rather than a guess. [doc](https://aws.amazon.com/blogs/aws/amazon-bedrock-model-evaluation-is-now-generally-available/)
- **[latency]** Enable prompt caching for workloads with long, repeated context (document Q&A, multi-turn conversations, coding assistants) — can cut response latency by up to 85% by skipping recomputation of previously seen input. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- **[throughput]** Use Geographic or Global cross-Region inference profiles to let Amazon Bedrock automatically route requests to the optimal Region, optimizing available resources and increasing model throughput for latency-tolerant use cases. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)

## 💰 Cost Optimization
- **[batch]** Move non-latency-sensitive workloads (bulk classification, embedding generation, content analysis) to batch inference — select foundation models are available at 50% of on-demand pricing. [doc](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- **[caching]** Apply prompt caching to stable, frequently reused context — cached tokens are billed at a reduced rate and can lower costs by up to 90% versus standard input token pricing. [doc](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- **[pricing model]** Match the inference option (on-demand, batch, or Provisioned Throughput) to the workload's latency and volume profile — Provisioned Throughput and Reserved capacity suit steady, predictable load while on-demand and batch suit variable or deferrable load. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/scaling-throughput-best-practices.html)

## ⚙️ Operational Excellence
- **[logging]** Enable AWS CloudTrail data events for Bedrock Agents and Knowledge Bases and forward logs to a centralized archive — Amazon Bedrock does not store user data by design, so CloudTrail is required to audit and analyze user activity. [doc](https://aws.amazon.com/blogs/mt/auditing-generative-ai-workloads-with-aws-cloudtrail/)
- **[monitoring]** Configure Amazon CloudWatch metrics and alarms for model invocation rates, response latencies, error rates, and token usage, and monitor Guardrails metrics to track content-filtering activations — surfaces service degradation and emerging policy-violation patterns. [doc](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/bedrock-integration.html)
- **[governance]** If you already use AWS Audit Manager, apply its AWS Generative AI Best Practices Framework to continuously monitor and evidence governance controls for Bedrock workloads against responsible-AI principles (safety, fairness, resilience, privacy, accuracy) — Audit Manager is in maintenance mode and closed to new customers as of April 2026, so net-new governance automation should use AWS Config conformance packs instead. [doc](https://docs.aws.amazon.com/audit-manager/latest/userguide/aws-generative-ai-best-practices.html)
- **[architecture review]** Apply the AWS Well-Architected Generative AI Lens to evaluate model selection, prompt engineering, model customization, and workload integration decisions against the six Well-Architected pillars. [doc](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html)

## 🌱 Sustainability
- **[batch processing]** Shift deferrable, large-volume inference (nightly content generation, bulk summarization) from real-time on-demand calls to batch inference — processes more work per compute unit and reduces the resource footprint of repeated ad hoc invocations. [doc](https://aws.amazon.com/blogs/machine-learning/automate-amazon-bedrock-batch-inference-building-a-scalable-and-efficient-pipeline/)
- **[caching]** Use prompt caching to avoid recomputing identical context across requests — reduces redundant model computation for repeated or multi-turn workloads. [doc](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)

<!-- meta: last_reviewed=2026-07-05; sources=19 -->
