# AWS Certificate Manager — Best Practices

## Common scenarios
- Provisioning TLS certificates for load balancers, CloudFront, and API Gateway        → Security, Reliability
- Automating certificate renewal to avoid expiry-driven outages        → Reliability, Operational Excellence
- Enforcing organizational PKI controls across many accounts/teams        → Security, Operational Excellence
- Managing certificates across regions and accounts at scale        → Reliability, Cost Optimization

## 🔒 Security
- **[Access control]** Use account-level separation to keep production certificates in separate accounts from testing and development certificates — limits blast radius if test environments are compromised or misconfigured. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Access control]** Restrict `kms:CreateGrant` by account or by specific certificate ARN using `kms:EncryptionContext` condition keys when account-level separation isn't feasible — limits which roles can sign or use a given certificate's private key. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[IAM]** Start from AWS managed policies and then author customer-managed policies scoped to least privilege for certificate request, export, and deletion actions. [doc](https://docs.aws.amazon.com/acm/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Use IAM condition keys to enforce organizational PKI controls, such as restricting the certificate types or validation methods users are allowed to request. [doc](https://aws.amazon.com/blogs/security/how-to-use-aws-certificate-manager-to-enforce-certificate-issuance-controls/)
- **[IAM]** Validate identity-based policies with IAM Access Analyzer to catch overly permissive statements before they're attached. [doc](https://docs.aws.amazon.com/acm/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Domain validation]** Prefer DNS validation over email validation when you can modify the domain's DNS records — it enables fully automated, indefinite renewal and removes dependence on WHOIS contact data or manual email approval. [doc](https://docs.aws.amazon.com/acm/latest/userguide/domain-ownership-validation.html)
- **[Trust configuration]** Include all Amazon root CAs (including the older Starfield Services Root CA - G2) in custom trust stores to maximize client compatibility with ACM-issued certificate chains. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Certificate pinning]** Avoid pinning applications directly to an ACM-managed certificate — ACM's managed renewal rotates the key pair, which can break pinned connections; if pinning is required, pin to the imported certificate or to the Amazon root CAs instead. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Auditing]** Turn on AWS CloudTrail before using ACM so you can retrieve a history of who called ACM APIs, from what source IP, and when. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Key management]** Use ACM as the managed service for storing, protecting, and rotating encryption keys and certificates with strict access control instead of building custom key/certificate handling. [doc](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/sec_protect_data_transit_key_cert_mgmt.html)

## 🛡️ Reliability
- **[Renewal automation]** Use DNS validation so ACM can renew certificates indefinitely without manual action, as long as the certificate stays in use and the CNAME record remains in place. [doc](https://docs.aws.amazon.com/acm/latest/userguide/dns-renewal-validation.html)
- **[Monitoring]** Subscribe to ACM Certificate Approaching Expiration, Renewal Action Required, and Expired events via Amazon EventBridge so PKI/security teams are notified before a certificate lapses. [doc](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-acm.html)
- **[Monitoring]** Route ACM Certificate Renewal Action Required events to the appropriate team (PKI, security, or app owners) since these indicate manual intervention is needed for renewal to succeed. [doc](https://aws.amazon.com/blogs/security/how-to-manage-certificate-lifecycles-using-acm-event-driven-workflows/)
- **[Exported certificates]** For certificates exported for use outside ACM-integrated services (EC2, on-premises, IoT), monitor DaysToExpiry via CloudWatch and automate redeployment of renewed certificates and keys. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-exportable-certificates.html)
- **[Exported certificates]** Begin using a renewed certificate immediately and test automated deployment processes for renewals to avoid serving an expiring certificate. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-exportable-certificates.html)
- **[Regional design]** Request or import a certificate in every AWS Region where it will be attached to a regional resource (such as an ALB) since ACM certificates cannot be copied or reused across regions; for CloudFront, certificates must be requested in US East (N. Virginia). [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- **[Multi-account/region]** Use AWS CloudFormation StackSets to standardize and repeat certificate request/validation across many accounts and regions rather than provisioning each manually. [doc](https://aws.amazon.com/blogs/security/how-to-deploy-public-acm-certificates-across-multiple-aws-accounts-and-regions-using-aws-cloudformation-stacksets/)

## ⚙️ Operational Excellence
- **[Infrastructure as code]** Provision ACM certificates for CloudFormation-managed resources (Elastic Load Balancing, CloudFront, API Gateway) through CloudFormation templates for repeatable, auditable deployment. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Event-driven operations]** Build event-driven workflows on ACM's EventBridge events (Approaching Expiration, Renewal Action Required, Expired, Available, Rotated, Revoked) to automate lifecycle notifications and remediation instead of manually tracking expiry dates. [doc](https://docs.aws.amazon.com/acm/latest/userguide/supported-events.html)
- **[Auditing]** Use AWS CloudTrail with ACM to identify which users/accounts invoked ACM APIs and correlate certificate issuance or deletion with source IP and time for operational investigations. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Change management]** Request a new certificate with the full revised domain list rather than trying to add or remove domain names on an existing certificate, since ACM certificates are immutable in that respect. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)

## 💰 Cost Optimization
- **[Quota management]** Use a single wildcard certificate (e.g. `*.service.example.com`) instead of issuing a separate certificate per ephemeral test environment to avoid exhausting your account's certificate quota. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)
- **[Quota management]** Track certificate counts against the default quota (2,500 concurrent certificates, 5,000 issued per year per region/account) and request a quota increase proactively instead of over-provisioning workarounds. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html)
- **[Validation method]** Avoid adding excessive domain names to email-validated certificates — each additional domain multiplies the manual validation-email workload; DNS validation avoids this recurring operational cost entirely. [doc](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html)

<!-- meta: last_reviewed=2026-07-05; sources=11 -->
