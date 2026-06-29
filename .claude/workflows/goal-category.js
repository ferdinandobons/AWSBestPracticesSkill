export const meta = {
  name: 'goal-category',
  description: 'Generate AWS best-practice files for one category (generate → verify, bounded retry)',
  phases: [
    { title: 'Generate', detail: 'one agent per service: research AWS docs, write the file' },
    { title: 'Verify', detail: 'one agent per file: confirm only-best-practices + sources' },
  ],
}

// args: { category, title, services: [ {name, slug, path, abspath, type, aws_service_code} ] }
const services = (args && args.services) || []
const categoryTitle = (args && args.title) || (args && args.category) || 'category'

const FILE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['path', 'status'],
  properties: {
    path: { type: 'string' },
    status: { type: 'string', enum: ['written', 'skipped', 'failed'] },
    pillars: { type: 'array', items: { type: 'string' } },
    sources: { type: 'integer' },
    note: { type: 'string' },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['onlyBestPractices', 'allSourced'],
  properties: {
    onlyBestPractices: { type: 'boolean' },
    allSourced: { type: 'boolean' },
    issues: { type: 'array', items: { type: 'string' } },
  },
}

function formatRules(isGeneral) {
  const sections = isGeneral
    ? `Use topic-based "## " sections (e.g. "## Root account", "## Organizations"). The 6-pillar structure is OPTIONAL for general docs.`
    : `Use ONLY these H2 sections, in this order, and include a pillar section ONLY if it has real practices:
- "## Common scenarios" (a short list mapping 2-4 typical use cases to relevant pillars, e.g. "- High traffic → Performance Efficiency, Cost Optimization")
- "## 🔒 Security"
- "## 🛡️ Reliability"
- "## ⚡ Performance Efficiency"
- "## 💰 Cost Optimization"
- "## ⚙️ Operational Excellence"
- "## 🌱 Sustainability"`
  return `Markdown format (English):
- First line: "# <Service name> — Best Practices"
${sections}
- Every best-practice bullet MUST be: "- **[context]** imperative practice — short rationale. [doc](OFFICIAL_AWS_URL)"
  where [context] is when it applies (e.g. [always], [production], [high traffic], [sensitive data], [multi-region]).
- "Common scenarios" bullets do NOT need a link; every other bullet MUST end with a Markdown link to an official AWS URL (docs.aws.amazon.com, aws.amazon.com, or wa.aws.amazon.com).
- Last line: "<!-- meta: last_reviewed=<TODAY>; sources=<count> -->"
HARD CONSTRAINT — ONLY BEST PRACTICES. Do NOT include: service descriptions / "what is X", pricing or cost figures, tutorials / getting-started, or extended code samples. Cost *optimization practices* are allowed; prices are not.`
}

function generatePrompt(svc, retry) {
  const isGeneral = svc.type === 'general'
  return `You are generating an AWS best-practices file. ${retry ? 'A previous attempt failed verification — be stricter this time.' : ''}

TARGET: ${svc.name}${isGeneral ? ' (cross-service GENERAL topic)' : ' (AWS service)'}
WRITE THE FILE TO (absolute path): ${svc.abspath}

STEP 1 — Research using the AWS Knowledge MCP. The tools are deferred: first call ToolSearch with query
"select:mcp__plugin_deploy-on-aws_awsknowledge__aws___search_documentation,mcp__plugin_deploy-on-aws_awsknowledge__aws___read_documentation"
to load them. Then search for best practices with queries like:
  "${svc.name} best practices", "${svc.name} security best practices", "${svc.name} Well-Architected", "${svc.name} reliability", "${svc.name} cost optimization".
Open the most relevant pages with read_documentation and extract concrete, actionable best practices with their source URLs.

STEP 2 — Write ${svc.abspath} using the Write tool. ${formatRules(isGeneral)}
Replace <TODAY> with the current date in YYYY-MM-DD form.

STEP 3 — Return the structured result: { path: "${svc.path}", status: "written" if you wrote a real file with at least 4 sourced best practices (else "skipped" with a note explaining why no published best practices exist), pillars: the list of pillar names you included (lowercase short forms: security, reliability, performance, cost, operations, sustainability) or [] for general docs, sources: the number of source links in the file, note: optional }.

Quality bar: prefer 6-15 high-signal, specific best practices over a long generic list. Every bullet must be a real AWS recommendation with a working official source link. Never invent URLs.`
}

function verifyPrompt(svc) {
  return `Adversarially verify the AWS best-practices file at ${svc.abspath} for "${svc.name}".
Read the file. Return a verdict:
- onlyBestPractices: false if it contains ANY service description/overview, pricing/cost figures, tutorial/getting-started, or extended code samples. Only best practices are allowed.
- allSourced: false if any non-"Common scenarios" bullet lacks a Markdown link to an official AWS URL (docs.aws.amazon.com / aws.amazon.com / wa.aws.amazon.com), or if any link looks invented/implausible.
- issues: list concrete problems found (empty if clean).
Be strict; default to false if uncertain.`
}

async function generateAndVerify(svc) {
  for (let attempt = 1; attempt <= 2; attempt++) {
    const file = await agent(generatePrompt(svc, attempt > 1), {
      label: `gen:${svc.slug}`,
      phase: 'Generate',
      schema: FILE_SCHEMA,
    })
    if (!file) continue
    if (file.status === 'skipped') {
      log(`skipped ${svc.slug}: ${file.note || 'no published best practices'}`)
      return { ...file, slug: svc.slug, category: args.category }
    }
    if (file.status !== 'written') continue
    const v = await agent(verifyPrompt(svc), {
      label: `verify:${svc.slug}`,
      phase: 'Verify',
      schema: VERDICT_SCHEMA,
    })
    if (v && v.onlyBestPractices && v.allSourced) {
      return { ...file, slug: svc.slug, category: args.category, verdict: v }
    }
    log(`retry ${svc.slug}: ${(v && v.issues && v.issues.join('; ')) || 'verification failed'}`)
  }
  return { path: svc.path, slug: svc.slug, category: args.category, status: 'failed' }
}

log(`Generating ${services.length} files for "${categoryTitle}"`)
const results = await parallel(services.map((svc) => () => generateAndVerify(svc)))
return { category: args.category, title: categoryTitle, results: results.filter(Boolean) }
