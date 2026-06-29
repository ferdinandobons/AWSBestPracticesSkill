export const meta = {
  name: 'goal',
  description: 'Recursively generate AWS best-practice files: one child workflow per category, run in parallel',
  phases: [
    { title: 'Generate', detail: 'one child workflow per category, each fans out per service' },
    { title: 'Verify', detail: 'each generated file is adversarially verified inside its category workflow' },
  ],
}

// args: { childScriptPath, categories: [ {category, title, services: [...]} ] }
const childScriptPath = args && args.childScriptPath
const categories = (args && args.categories) || []

if (!childScriptPath) {
  throw new Error('goal.js: args.childScriptPath is required (absolute path to goal-category.js)')
}

const total = categories.reduce((n, c) => n + (c.services ? c.services.length : 0), 0)
log(`/goal: ${categories.length} categories, ${total} files to generate (parallel child workflows)`)

// Recursive + parallel: each category is its own child workflow, all launched concurrently.
const out = await parallel(
  categories.map((g) => () =>
    workflow({ scriptPath: childScriptPath }, {
      category: g.category,
      title: g.title,
      services: g.services,
    })
  )
)

const flat = out.filter(Boolean).flatMap((c) => (c && c.results) || [])
const written = flat.filter((r) => r.status === 'written')
const skipped = flat.filter((r) => r.status === 'skipped')
const failed = flat.filter((r) => r.status === 'failed')
log(`/goal done: ${written.length} written, ${skipped.length} skipped, ${failed.length} failed`)

return {
  written: written.length,
  skipped: skipped.map((r) => ({ slug: r.slug, note: r.note })),
  failed: failed.map((r) => r.slug),
  results: flat,
}
