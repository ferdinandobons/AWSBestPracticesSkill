# AWS Amplify — Best Practices

## Common scenarios
- Hosting and CI/CD for static sites and SSR frameworks (Next.js, Nuxt) from a Git repo        → Reliability, Operational Excellence, Performance Efficiency
- Full-stack apps needing auth, data, and storage backends provisioned alongside the frontend        → Security, Operational Excellence
- Previewing feature branches and pull requests before merging to production        → Reliability, Operational Excellence
- Serving global end users with low-latency static and dynamic content        → Performance Efficiency, Cost Optimization

## 🔒 Security
- **[IAM]** Grant Amplify console/CLI users least-privilege identity-based policies scoped to specific apps and actions, starting from AWS managed policies and narrowing to customer-managed policies as needs firm up. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Add IAM policy conditions (e.g. require SSL, restrict by source service) to further scope who can call Amplify management APIs beyond what resource-level permissions alone provide. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/security_iam_id-based-policy-examples.html)
- **[IAM]** Validate custom IAM policies with IAM Access Analyzer before attaching them, to catch overly permissive statements affecting Amplify resources. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/security_iam_id-based-policy-examples.html)
- **[Access control]** Password-protect (basic auth) feature or staging branches that host unreleased functionality so only authorized testers can reach them; Amplify throttles repeated failed auth attempts automatically. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/access-control.html)
- **[Access control]** Prefer WAF Web ACL integration over relying solely on branch passwords when you need IP allow/deny lists, geo-restriction, or bot/exploit protection for a hosted app. [doc](https://aws.amazon.com/blogs/mobile/aws-amplify-hosting-adds-web-application-firewall-protection-public-preview/)
- **[Access control]** Disable or restrict the default `amplifyapp.com` domain once a custom domain is attached, to stop search engines and bots from indexing or probing the default URL. [doc](https://aws.amazon.com/blogs/mobile/aws-amplify-hosting-adds-web-application-firewall-protection-public-preview/)
- **[Secrets]** Use the Amplify console Secrets management feature (Gen 2) or Systems Manager Parameter Store-backed environment secrets (Gen 1) for sensitive values — never store API keys, tokens, or credentials as plain environment variables. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html)
- **[Cookies]** When setting sensitive cookies on the shared `amplifyapp.com` domain, use the `__Host-` cookie prefix to harden against cross-site request forgery, since that domain is on the Public Suffix List. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/security-best-practices.html)
- **[Transport security]** Ensure clients calling Amplify APIs support TLS 1.2 at minimum (TLS 1.3 recommended) with PFS cipher suites (DHE/ECDHE). [doc](https://docs.aws.amazon.com/amplify/latest/userguide/infrastructure-security.html)
- **[Data protection]** Never place sensitive identifying information (account numbers, credentials) into free-form Amplify console/API fields, since such input can be captured in diagnostic logs. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/data-protection.html)
- **[Data protection]** Set up individual IAM identities with MFA rather than sharing root or broad credentials across a team managing Amplify apps. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/data-protection.html)

## 🛡️ Reliability
- **[Deployments]** Enable pull-request previews so changes deploy to an ephemeral URL and backend environment for testing before merging into a production or integration branch. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-amplify-alpha-readme.html)
- **[Deployments]** Gate production merges behind a reviewed pull-request workflow (e.g. `main` → `prod`) so backend and frontend changes are validated in staging before reaching production. [doc](https://aws.amazon.com/blogs/mobile/enable-sign-in-with-apple-on-your-app-with-aws-amplify/)
- **[Deployments]** Rely on Amplify's automatic cache invalidation on every deployment so stale assets aren't served after a rollout, and account for this when planning deploy timing. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/caching.html)
- **[SSR apps]** Redeploy (trigger a fresh build) after changing access-control settings on a server-side-rendered app, since SSR apps require a new build for access control changes to take effect. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/access-control.html)

## ⚡ Performance Efficiency
- **[Caching]** Rely on Amplify's CloudFront-backed default cache configuration (up to one-year TTL for static assets) rather than customizing cache behavior unless you have a specific requirement. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/caching.html)
- **[Caching]** Set an explicit `Cache-Control` `s-maxage` custom header when you need finer control over how long content stays at the CDN edge versus the default. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/Using-headers-to-control-cache-duration.html)
- **[Caching]** Exclude cookies from the cache key (`AMPLIFY_MANAGED_NO_COOKIES`) when your app doesn't vary responses by cookie, to improve cache hit ratio. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-amplify-alpha-readme.html)
- **[Monorepos]** Let Amplify auto-detect npm/Yarn/pnpm workspace or Nx monorepo build settings, and check in a shared `amplify.yml` at the repo root so all branches use consistent, centrally-managed build configuration. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/monorepo-configuration.html)
- **[Global delivery]** Serve apps through Amplify Hosting's CloudFront-backed global edge network so end-user requests are served from the nearest of 600+ points of presence. [doc](https://aws.amazon.com/amplify/hosting/)

## 💰 Cost Optimization
- **[Build configuration]** Tune build instance size and custom build image only when default build performance is insufficient, to avoid paying for oversized build compute on every commit. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings-configuration.html)
- **[Caching]** Maximize CDN cache hit ratio (longer TTLs for static content) to reduce origin fetches and data transfer costs on repeat requests. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/caching.html)
- **[Environments]** Tear down ephemeral pull-request preview backend environments promptly (Amplify does this automatically when the PR closes) rather than leaving unused backend resources provisioned. [doc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-amplify-alpha-readme.html)

## ⚙️ Operational Excellence
- **[CI/CD]** Use Git-based CI/CD (auto-build on commit) plus incoming webhooks only where a build must be triggered without a repository commit, keeping deployment history tied to source control by default. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings-configuration.html)
- **[CI/CD]** Set up build notifications so the team learns promptly about build successes and failures instead of discovering them after the fact. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings-configuration.html)
- **[Environments]** Clone a staging backend environment to create an isolated production backend, and connect a dedicated `prod` branch to it, instead of pointing multiple environments at the same backend stack. [doc](https://aws.amazon.com/blogs/mobile/enable-sign-in-with-apple-on-your-app-with-aws-amplify/)
- **[Secrets]** Centralize environment-specific secrets in Amplify's console-based secret management (Gen 2), scoped to specific branches, instead of duplicating values across environments. [doc](https://aws.amazon.com/blogs/mobile/team-workflows-amplify/)
- **[Monitoring]** Use Amplify's CloudWatch metrics (traffic, errors, latency, data transfer) and access logs to track hosted-app health, and CloudTrail logging to audit who made API-level changes to your apps. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/access-logs.html)
- **[Monitoring]** Create a multi-Region CloudTrail trail to Amazon S3 to retain an ongoing, queryable record of Amplify API activity beyond the default Event history retention window. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/logging-using-cloudtrail.html)
- **[Monitoring]** Route Amplify-related events to EventBridge when you need to trigger automated responses (e.g. notifications, remediation Lambdas) rather than polling CloudWatch or CloudTrail manually. [doc](https://docs.aws.amazon.com/amplify/latest/userguide/monitoring-overview.html)

<!-- meta: last_reviewed=2026-07-05; sources=18 -->
