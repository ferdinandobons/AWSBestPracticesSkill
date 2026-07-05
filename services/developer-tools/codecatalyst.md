# Amazon CodeCatalyst — Best Practices

## Common scenarios
- Unified CI/CD (source, build, test, deploy) for teams building on AWS        → Security, Reliability, Operational Excellence
- Enforcing peer review and change quality gates before merge/deploy        → Security, Operational Excellence
- Granting CodeCatalyst workflows access to AWS accounts to provision resources        → Security
- Running cloud-based Dev Environments for day-to-day development        → Operational Excellence, Sustainability

## 🔒 Security
- **[account connections]** Create dedicated, least-privilege service roles instead of using the `CodeCatalystWorkflowDevelopmentRole-spaceName` role (which carries `AdministratorAccess`) outside of development accounts — scope permissions to only what workflows and projects actually need. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/ipa-iam-roles.html)
- **[IAM roles]** Configure the CodeCatalyst service role's trust policy with the `aws:SourceArn` condition key scoped to the specific space ID so only that space can assume the role. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/trust-model.html)
- **[secrets]** Store credentials, keys, and tokens as CodeCatalyst secrets and reference them in workflow YAML rather than embedding sensitive values directly in the workflow definition or repository. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/security-best-practices-for-actions.html)
- **[workflow actions]** Vet the trustworthiness, licensing terms, and source of third-party and GitHub Actions before using them in a workflow, since they can access secrets, source code, and compute time. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/security-best-practices-for-actions.html)
- **[sign-in]** Protect account credentials and enable multi-factor authentication (MFA) for AWS Builder ID sign-in to CodeCatalyst spaces. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/data-protection.html)
- **[free-form fields]** Avoid entering confidential or sensitive information (e.g., customer data) in tags, names, or free-form fields such as space, project, or deployment fleet names, since these may appear in URLs, billing, or diagnostic logs. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/data-protection.html)
- **[enterprise identity]** Manage space membership through IAM Identity Center federation (SSO) rather than individual AWS Builder ID invitations when you need centralized, auditable user and group lifecycle management. [doc](https://docs.aws.amazon.com/codecatalyst/latest/adminguide/setting-up-federation.html)
- **[roles]** Reserve the Space administrator role — which has full permissions in CodeCatalyst — for the few users who genuinely need to administer every aspect of a space; use Power user or Limited access roles for others. [doc](https://aws.amazon.com/blogs/devops/using-single-sign-on-sso-to-manage-project-teams-for-amazon-codecatalyst/)
- **[network access]** Ensure clients accessing CodeCatalyst APIs support TLS 1.2 (TLS 1.3 recommended) and cipher suites with perfect forward secrecy. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/infrastructure-security.html)
- **[supply chain]** Integrate SBOM generation and vulnerability scanning (e.g., Amazon Inspector Scan) into workflows to detect vulnerable dependencies before deployment. [doc](https://aws.amazon.com/blogs/devops/securing-your-software-supply-chain-with-amazon-codecatalyst-and-amazon-inspector/)

## 🛡️ Reliability
- **[pull requests]** Enforce pull request approval rules requiring at least one (or more) reviewer approvals before code can be merged, supporting separation of duties in the SDLC. [doc](https://aws.amazon.com/blogs/devops/best-practices-for-working-with-pull-requests-in-amazon-codecatalyst/)
- **[compute fleets]** Use on-demand fleets for variable workloads to get automatic scaling and fully managed provisioning, reducing the risk of capacity-related workflow failures. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/workflows-working-compute.html)
- **[DevSecOps]** Automate security testing (dependency/SCA checks, static analysis) directly in workflows rather than relying on manual, siloed reviews, so issues surface before deployment. [doc](https://aws.amazon.com/blogs/devops/enabling-devsecops-with-amazon-codecatalyst/)

## 💰 Cost Optimization
- **[compute fleets]** Prefer on-demand fleets (pay only for action run-time, machines destroyed after use) over provisioned fleets unless you need dedicated, always-available capacity, since provisioned fleets incur cost while idle. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/workflows-working-compute.html)
- **[compute sizing]** Select the smallest on-demand fleet size (e.g., `Linux.x86-64.Large` vs. larger instance types) that meets each workflow action's needs instead of defaulting to larger compute. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/workflows-assign-compute-resource.html)

## ⚙️ Operational Excellence
- **[auditing]** Enable AWS CloudTrail for the space's billing account to capture management events, and use connected-account trails to capture workflow-driven resource events for auditability. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/ipa-monitoring.html)
- **[event review]** Use `aws codecatalyst list-event-logs` (Space administrator role required) to review space activity such as user actions, timestamps, and source IP addresses. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/ipa-logs.html)
- **[dev environments]** Define project tools and dependencies in a devfile checked into the source repository so Dev Environments are reproducible and on-demand rather than manually configured per developer. [doc](https://aws.amazon.com/blogs/devops/managing-dev-environments-with-amazon-codecatalyst/)
- **[pull requests]** Use automated PR summaries and organized (nested) comment threads to reduce review time to merge while maintaining review quality. [doc](https://aws.amazon.com/blogs/devops/best-practices-for-working-with-pull-requests-in-amazon-codecatalyst/)
- **[continuity planning]** Since Amazon CodeCatalyst is closed to new customer sign-ups, review the official migration guidance to plan data export or transition for any new initiatives. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/migration.html)

## 🌱 Sustainability
- **[dev environments]** Configure a Dev Environment timeout (rather than "No timeout") so idle Dev Environments stop automatically, minimizing wasted compute instead of running continuously. [doc](https://docs.aws.amazon.com/codecatalyst/latest/userguide/devenvironment-stop.html)

<!-- meta: last_reviewed=2026-07-05; sources=17 -->
