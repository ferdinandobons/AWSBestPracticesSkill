# Amazon Cognito — Best Practices

## Common scenarios
- Customer-facing sign-up/sign-in for web and mobile apps        → Security, Reliability
- Issuing temporary AWS credentials to authenticated/guest users        → Security, Cost Optimization
- Federating enterprise or social identity providers (SAML/OIDC)        → Security, Operational Excellence
- Machine-to-machine and agentic AI authentication        → Security, Reliability

## 🔒 Security
- **[Network protection]** Attach AWS WAF web ACLs to user pool endpoints and managed login to filter unwanted network- and application-layer traffic before it reaches Cognito. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Public sign-up]** Disable self-service sign-up and use admin-only user creation when your app doesn't need public registration, and enable "prevent user existence errors" on app clients to stop username/email enumeration. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Client secrets]** Only enable app client secrets for confidential server-side or M2M clients, and store the secret in AWS Secrets Manager or encrypted storage — never embed it in public clients. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Authentication method]** Prefer passwordless authentication with WebAuthn passkeys; if passwords are required, use the Secure Remote Password (SRP) flow together with MFA. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Credentials handling]** Never store ID or access tokens, passwords, or AWS credentials in local storage, and revoke refresh tokens on sign-out or when a session should no longer persist. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[PKCE]** Generate a new random PKCE code verifier for every authorization-code request and never expose it to users, to prevent authorization-code interception attacks. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Admin least privilege]** Scope IAM policies for user pool administration to only the specific `cognito-idp:Admin*` actions each principal needs, since permissions apply pool-wide across all app clients. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Multi-tenancy]** Use one user pool per tenant when your security model requires separation of administrative responsibilities between tenants. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Identity providers]** Only enable social identity providers on an app client once you intend to allow public sign-in, since enterprise SAML/OIDC providers are more tightly controlled than open social IdPs. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[OAuth scopes]** Configure app clients to request only the minimum OAuth scopes needed, since scopes like `aws.cognito.signin.user.admin` and `openid`/`profile`/`email`/`phone` control what profile data and self-service operations are exposed. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Input handling]** Perform client-side validation of user-submitted attribute values and map only secure, predictable IdP attributes into user pool attributes. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)
- **[Threat protection]** Turn on threat protection (compromised-credential detection and adaptive/risk-based authentication) to block or challenge sign-ins that show signs of credential stuffing or anomalous location/device activity. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-threat-protection.html)
- **[SMS abuse]** Guard against SMS pumping and sign-up fraud by monitoring SMS usage and applying the available anti-fraud controls for account verification. — [doc](https://aws.amazon.com/blogs/security/reduce-risks-of-user-sign-up-fraud-and-sms-pumping-with-amazon-cognito-user-pools/)
- **[Identity pool trust policy]** Require both `cognito-identity.amazonaws.com:aud` and `cognito-identity.amazonaws.com:amr` conditions on every IAM role trust policy that federates with an identity pool. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools-security-best-practices.html)
- **[Identity pool permissions]** Grant least-privilege, resource-scoped IAM permissions to authenticated and unauthenticated roles rather than broad access. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools-security-best-practices.html)
- **[Guest access]** Leave unauthenticated guest access disabled by default; if required, restrict the unauthenticated role's permissions tightly since anyone who knows the identity pool ID can request guest credentials. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools-security-best-practices.html)
- **[Identity pool auth flow]** Use the enhanced (simplified) authentication flow by default so role selection is governed by centralized identity pool logic rather than app-side logic. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools-security-best-practices.html)
- **[Transport security]** Require clients to use TLS 1.2 (recommended TLS 1.3) with forward-secrecy cipher suites when calling Cognito APIs. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/infrastructure-security.html)

## 🛡️ Reliability
- **[Multi-Region]** Enable multi-Region replication (MRR) for user pools so registered users can continue authenticating from a secondary Region during a primary-Region disruption. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-multi-region.html)
- **[Quota monitoring]** Monitor Cognito API category utilization against Service Quotas and configure CloudWatch alarms at multiple thresholds (e.g., 50/70/90 percent) so legitimate traffic isn't unexpectedly throttled. — [doc](https://aws.amazon.com/blogs/security/protect-public-clients-for-amazon-cognito-by-using-an-amazon-cloudfront-proxy/)
- **[Data resilience]** Plan for regional data protection and back up critical user profile/group data given Cognito's Region- and Availability Zone-based resilience model. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/disaster-recovery-resiliency.html)

## ⚡ Performance Efficiency
- **[Rate quotas]** Design authentication flows around the lowest per-category API rate quota in the chain (e.g., UserAuthentication, UserCreation categories), since a multi-call flow is limited by its most restrictive operation. — [doc](https://aws.amazon.com/blogs/security/implement-step-up-authentication-with-amazon-cognito-part-1-solution-overview/)
- **[Quota increases]** Request quota increases proactively for adjustable rate limits (e.g., UserAuthentication, UserCreation, identity providers per pool) ahead of expected traffic growth. — [doc](https://docs.aws.amazon.com/general/latest/gr/cognito.html)

## 💰 Cost Optimization
- **[SMS/fraud costs]** Configure fraud protections for sign-up and password-reset flows since SMS pumping and unwanted sign-up activity can directly inflate your AWS bill. — [doc](https://aws.amazon.com/blogs/security/reduce-risks-of-user-sign-up-fraud-and-sms-pumping-with-amazon-cognito-user-pools/)
- **[Network filtering]** Use AWS WAF web ACLs in front of Cognito endpoints to drop unwanted automated traffic before it consumes authentication capacity and cost. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-security-best-practices.html)

## ⚙️ Operational Excellence
- **[Auditing]** Enable AWS CloudTrail for Cognito to capture console and API activity, and route the trail to CloudWatch Logs so you can use Logs Insights to search for errors or unusual activity. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/logging-using-cloudtrail.html)
- **[Alerting]** Create CloudWatch alarms on specific CloudTrail events (for example, identity pool configuration changes) to catch unintended or unauthorized changes quickly. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/logging-using-cloudtrail.html)
- **[Deletion protection]** Enable user pool deletion protection to require additional confirmation before a pool can be deleted, guarding against accidental removal by automated systems. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/managing-security.html)
- **[Policy validation]** Validate IAM policies for Cognito with IAM Access Analyzer to check for secure, functional least-privilege permissions before deployment. — [doc](https://docs.aws.amazon.com/cognito/latest/developerguide/security_iam_id-based-policy-examples.html)

<!-- meta: last_reviewed=2026-07-05; sources=9 -->
