# AWS Payment Cryptography — Best Practices

## Common scenarios
- Issuing and acquiring card payment key management (PIN, CVK, DUKPT, ARQC)        → Security, Reliability
- Migrating from on-premises payment HSMs to a managed cloud service        → Reliability, Operational Excellence
- Multi-region payment processing and transaction switching/routing        → Reliability, Performance Efficiency
- Auditing cryptographic key usage for PCI PIN, P2PE, DSS, and 3DS compliance        → Security, Operational Excellence

## 🔒 Security
- **[key attributes]** Rely on TR-31 key usage and mode-of-use enforcement instead of custom controls — the service cryptographically binds permitted operations to key material so a key encryption key cannot be reused for data decryption. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/security-best-practices.html)
- **[key sharing]** Limit sharing of symmetric key material (PIN encryption keys, key encryption keys) to at most one other entity, creating additional keys for additional partners — the service never exposes symmetric or asymmetric private key material in the clear. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/security-best-practices.html)
- **[key organization]** Use aliases and tags (for example bin=12345, use_case=acquiring) to associate keys with specific use cases or partners — this also enables access control separation between issuing and acquiring workloads. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/security-best-practices.html)
- **[access control]** Practice least-privileged IAM access — restrict who can create keys, run cryptographic operations, or perform sensitive actions like key import to specific service accounts rather than individual users. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/security_iam_id-based-policy-examples.html)
- **[access control]** Scope IAM policies to specific key ARNs and API operations — allow only the PIN generate/validate calls an acquirer actually needs instead of granting account-wide payment-cryptography access. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/security_iam_id-based-policy-examples.html)
- **[critical operations]** Enable Multi-party approval (MPA) for protected operations such as importing a root certificate — this requires multiple trusted individuals to approve before the action is carried out. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/mpa.html)
- **[shared responsibility]** Manage key material before import and after export, and correctly define key attributes at import/creation time — this remains your responsibility under the AWS shared responsibility model. [doc](https://aws.amazon.com/payment-cryptography/faqs/)

## 🛡️ Reliability
- **[key durability]** Design key lifecycle management (create, rotate, back up, recover, shred) around the service's built-in automated key management rather than custom scripts — a single key may need to remain usable with a terminal or chip card for years. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/cryptographic-details.designgoals.html)
- **[multi-region]** Use Multi-Region key replication for symmetric keys (3DES, AES, HMAC) to serve distributed applications and provide regional failover — note that replica keys are read-only and eventually consistent with the primary. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/keys-multi-region-replication.html)
- **[multi-region]** Reference the Primary Region key and its Replica Region keys by the same ARN in IAM policies — account for replica key count against your account-level AWS Payment Cryptography limits when planning capacity. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/keys-multi-region-replication.html)
- **[data residency]** Use independent AWS Regions to isolate key usage — this helps restrict data access geographically and meet data residency requirements. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/cryptographic-details.designgoals.html)

## ⚡ Performance Efficiency
- **[multi-region latency]** Add replication regions to keys used by applications distributed across regions — this provides lower-latency cryptographic operations closer to where transactions are processed. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_AddKeyReplicationRegions.html)
- **[elasticity]** Rely on the service's elastic, pay-as-you-go scaling instead of provisioning or reserving HSM capacity — throughput scales automatically with transaction volume. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/cryptographic-details.designgoals.html)

## 💰 Cost Optimization
- **[capacity planning]** Avoid over-provisioning by using the service's elastic scaling instead of sizing for peak on-premises HSM capacity — AWS Payment Cryptography scales out and in with demand. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/cryptographic-details.designgoals.html)

## ⚙️ Operational Excellence
- **[monitoring]** Use Amazon CloudWatch to track API usage against AWS Payment Cryptography quotas and set alarms — this notifies you before hitting service limits. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/monitoring.html)
- **[audit logging]** Enable AWS CloudTrail to capture control-plane and data-plane API calls — this lets you identify which users, accounts, source IPs, and keys were involved in each cryptographic operation for compliance reporting. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/monitoring-cloudtrail.html)
- **[log retention]** Archive CloudTrail and CloudWatch Logs data for AWS Payment Cryptography activity in durable storage — this supports PCI PIN, P2PE, and DSS compliance reviews over time. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/monitoring.html)
- **[change control]** Use Multi-party approval for sensitive control-plane actions and review the associated CloudTrail logging for MPA events — this strengthens your operational audit trail. [doc](https://docs.aws.amazon.com/payment-cryptography/latest/userguide/mpa.html)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
