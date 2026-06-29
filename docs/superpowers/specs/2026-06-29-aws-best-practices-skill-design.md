# AWSBestPracticesSkill — Design & Spec

**Data:** 2026-06-29
**Stato:** in revisione utente
**Autore:** sessione brainstorming Claude Code

---

## 1. Scopo e principio guida

Una skill per Claude e Codex che raccoglie **esclusivamente le best practice di ogni servizio AWS**.

L'utente che installa la skill deve poter accedere alle best practice di un servizio **in base al proprio caso d'uso**, e a nient'altro. La skill *è* la conoscenza: `SKILL.md` fa da mappa, il modello esplora le cartelle e apre solo i file che gli servono.

### Vincolo non negoziabile — "solo best practice"

I file servizio contengono **solo** best practice. Sono **vietati**:

- descrizioni del servizio ("cos'è", "a cosa serve", overview, introduzioni);
- pricing, listini, stime di costo (le *best practice* di cost optimization sono ammesse: "usa on-demand per carichi variabili" è una pratica, non un prezzo);
- tutorial, getting-started, how-to passo-passo, esempi di codice estesi;
- confronti commerciali, marketing, quote, SLA testuali.

Una voce di best practice valida = **cosa fare** (imperativo) + **quando si applica** (tag di contesto) + **perché** (razionale breve) + **fonte** (link al doc AWS ufficiale).

> Nota di confine: il vincolo "solo best practice" riguarda il **contenuto consumato** dall'utente (i file in `services/`). Il tooling di manutenzione (`MAINTENANCE.md`, `scripts/`, `README.md`, CI) serve al *manutentore* e vive nel repo senza far parte della conoscenza esposta.

---

## 2. Decisioni di design (riepilogo)

| Aspetto | Decisione |
|---|---|
| Copertura | Tutti i servizi AWS (200+), lista derivata dal catalogo ufficiale AWS |
| Fonte | Documentazione ufficiale AWS via MCP (AWS Knowledge + Well-Architected); ogni pratica con link |
| Raggruppamento | Per categoria AWS (~20 categorie), un file `.md` per servizio |
| Formato interno file | Pilastri Well-Architected come sezioni + tag `[quando si applica]` per ogni pratica + mini-indice "Scenari comuni" in cima |
| Struttura skill | `SKILL.md` router + `catalog.json` (sorgente di verità) + `services/<categoria>/<servizio>.md` + `_TEMPLATE.md` |
| Manutenzione | `MAINTENANCE.md` (procedura) + `scripts/check.py` (validatore/diff) |
| Compatibilità | `SKILL.md` con frontmatter YAML `name`/`description`: funziona su Claude e Codex |

---

## 3. Struttura del repository

```
AWSBestPracticesSkill/
├── SKILL.md                      # Router/indice. NON contiene best practice.
├── README.md                     # Scopo, install su Claude/Codex, struttura, link manutenzione
├── MAINTENANCE.md                # Procedura di aggiornamento + ricerca (vedi §8)
├── CHANGELOG.md                  # Storico versioni
├── catalog.json                  # Sorgente di verità: categoria → servizi → metadati
├── catalog.md                    # Indice umano, GENERATO da catalog.json (check.py --write-index)
├── _TEMPLATE.md                  # Template di un file servizio
├── scripts/
│   └── check.py                  # Validatore + diff-checker (stdlib, no deps)
├── .github/
│   └── workflows/
│       └── check.yml             # CI: esegue check.py sulle PR
├── docs/
│   └── superpowers/specs/        # Questo documento di design
└── services/
    ├── compute/
    │   ├── ec2.md
    │   ├── lambda.md
    │   └── ...
    ├── storage/
    ├── database/
    ├── networking-content-delivery/
    ├── security-identity-compliance/
    ├── management-governance/
    ├── application-integration/
    ├── analytics/
    ├── machine-learning/
    ├── containers/
    ├── developer-tools/
    ├── migration-transfer/
    ├── frontend-web-mobile/
    ├── iot/
    ├── media-services/
    ├── end-user-computing/
    ├── business-applications/
    ├── cloud-financial-management/
    └── ...
```

Le categorie rispecchiano la tassonomia ufficiale AWS. La lista esatta dei servizi viene consolidata in `catalog.json` durante la build, partendo da `get_pricing_service_codes` (MCP pricing) + la classificazione per categoria dei doc AWS.

---

## 4. `catalog.json` — sorgente di verità

È il file machine-readable da cui dipendono lo script e l'indice umano. Schema:

```json
{
  "version": "0.1.0",
  "generated": "2026-06-29",
  "categories": {
    "database": {
      "title": "Database",
      "services": [
        {
          "name": "Amazon DynamoDB",
          "slug": "dynamodb",
          "path": "services/database/dynamodb.md",
          "aws_service_code": "AmazonDynamoDB",
          "pillars": ["security", "reliability", "performance", "cost", "operations"],
          "last_reviewed": "2026-06-29",
          "sources": 7
        }
      ]
    }
  }
}
```

- `slug`/`path` legano l'entry al file.
- `aws_service_code` permette il confronto con il catalogo AWS (rilevare nuovi servizi).
- `last_reviewed` abilita il controllo di freschezza.
- `pillars` elenca solo i pilastri effettivamente presenti nel file.
- `sources` = numero di link alla fonte (sanity check di copertura).

`catalog.md` e l'indice in `SKILL.md` sono **generati** da qui con `check.py --write-index`, così non divergono mai.

---

## 5. `_TEMPLATE.md` — formato di un file servizio

````markdown
# <Nome servizio> — Best Practices

> Solo best practice. Ogni voce: **cosa fare** · `[quando si applica]` · perché · [fonte](url).

## Scenari comuni
- <caso d'uso tipico>      → <Pilastri rilevanti>
- <caso d'uso tipico>      → <Pilastri rilevanti>

## 🔒 Security
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

## 🛡️ Reliability
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

## ⚡ Performance Efficiency
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

## 💰 Cost Optimization
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

## ⚙️ Operational Excellence
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

## 🌱 Sustainability
- **[<contesto>]** <pratica imperativa> — <perché>. [doc](<url AWS>)

<!-- meta: last_reviewed=YYYY-MM-DD; sources=AWS Well-Architected + service docs -->
````

Regole:
- Si includono **solo i pilastri con best practice reali** per quel servizio (niente sezioni vuote).
- Tag di contesto in minuscolo tra parentesi quadre: `[sempre]`, `[produzione]`, `[alto traffico]`, `[dati sensibili]`, `[multi-region]`, `[carico variabile]`, ecc.
- Ogni bullet deve avere **un link alla fonte**.
- Niente H2 diversi da "Scenari comuni" + i 6 pilastri (lo script lo verifica per impedire info extra).

---

## 6. `SKILL.md` — il router

Frontmatter + istruzioni di navigazione, **zero best practice**:

```markdown
---
name: aws-best-practices
description: >
  Use when the user needs AWS best practices for any AWS service based on their
  use case — security, reliability, performance, cost, operations, sustainability.
  Trigger on "best practice <servizio AWS>", "come configurare bene <servizio>",
  "is my <servizio> setup correct", "AWS Well-Architected for <servizio>".
  Contains ONLY best practices, nothing else about the services.
---

# AWS Best Practices

## Cosa contiene / cosa NON contiene
- ✅ Solo best practice per servizio, organizzate per pilastro Well-Architected, con fonte.
- ❌ Niente descrizioni servizio, pricing, tutorial, how-to.

## Come usarla
1. Dal caso d'uso dell'utente, identifica il **servizio** e il **pilastro/preoccupazione**.
2. Apri `catalog.md` (o l'indice qui sotto) e trova il path del servizio.
3. Apri `services/<categoria>/<servizio>.md`.
4. Leggi "Scenari comuni" per mappare il caso d'uso, poi la/le sezione/i pilastro rilevanti.
5. Cita le best practice con il loro link alla fonte ufficiale.

## Indice servizi
<!-- BEGIN:INDEX (generato da scripts/check.py --write-index) -->
... categorie → servizi → path ...
<!-- END:INDEX -->
```

L'indice tra i marker è generato dallo script.

---

## 7. `README.md` (GitHub) — outline

- Titolo + una riga di scopo (solo best practice AWS).
- **Cosa contiene / cosa NON contiene** (lo stesso paletto).
- **Installazione** su Claude Code (path skill / plugin) e su Codex.
- Struttura del repo (albero sintetico).
- Come si naviga (link a `catalog.md`).
- **Manutenzione**: rimando a `MAINTENANCE.md` e a `scripts/check.py`.
- Stato copertura (N servizi, ultima revisione).
- Licenza.

Il README è parte della superficie di release: va sincronizzato a ogni cambio di comandi/struttura (regole di release globali).

---

## 8. `MAINTENANCE.md` — bozza completa (procedura di aggiornamento + ricerca)

> Questo blocco diventa il file `MAINTENANCE.md` nel repo.

````markdown
# Manutenzione di AWSBestPracticesSkill

Questa skill contiene **solo best practice AWS**. Ogni aggiornamento deve preservare
questo vincolo: niente descrizioni servizio, pricing, tutorial.

## 1. Quando aggiornare (trigger)
- **Periodico**: revisione completa ogni 3-6 mesi.
- **Nuovo servizio AWS**: quando AWS annuncia/GA un nuovo servizio.
- **Cambio best practice**: AWS aggiorna Well-Architected o le pagine "best practices"
  di un servizio.
- **Link rotti**: segnalati da `scripts/check.py --check-links`.
- **Freschezza**: file con `last_reviewed` più vecchio di 180 giorni.

## 2. Procedura di ricerca (rigenerazione dei contenuti)
Da eseguire in una sessione Claude Code o Codex con i tool MCP AWS attivi.

### 2.1 Aggiorna il catalogo dei servizi
1. Recupera l'elenco autorevole dei servizi: tool MCP `get_pricing_service_codes`.
2. Confronta con `catalog.json`:
   ```bash
   # dump dei service code AWS, uno per riga, in /tmp/aws_codes.txt
   python scripts/check.py --aws-codes /tmp/aws_codes.txt
   ```
   Lo script segnala i servizi **nuovi** (in AWS, non nel catalogo) e quelli **scomparsi**.
3. Aggiungi le entry mancanti in `catalog.json` (categoria, slug, path, aws_service_code).

### 2.2 Estrai le best practice da fonte ufficiale (per servizio)
Per ogni servizio da (ri)generare, con il MCP **AWS Knowledge**:
1. `search_documentation` con query del tipo: `"<servizio> best practices"`,
   `"<servizio> security best practices"`, `"<servizio> Well-Architected"`.
2. `read_documentation` sulle pagine rilevanti (best practices, security, operational
   guidance, resilience, cost optimization). Usa `retrieve_skill` se restituisce
   guidance strutturata.
3. Estrai **solo best practice**. Per ognuna annota: pratica (imperativo),
   `[quando si applica]`, razionale breve, URL della fonte.
4. Scarta tutto ciò che è descrizione/pricing/tutorial.

### 2.3 Scrivi il file con il template
1. Parti da `_TEMPLATE.md`.
2. Compila "Scenari comuni" (2-4 casi d'uso → pilastri) e i pilastri che hanno pratiche reali.
3. Aggiorna il footer `<!-- meta: last_reviewed=... -->` e `last_reviewed`/`sources`
   nell'entry di `catalog.json`.

### 2.4 Scala: generazione di massa
Per molti servizi insieme, usa un **Workflow** con fan-out: un agente per servizio (o per
batch), stesso schema/template, ognuno interroga l'MCP e scrive il file. Poi verifica.

## 3. Aggiungere un nuovo servizio
1. Aggiungi l'entry in `catalog.json`.
2. Crea `services/<categoria>/<slug>.md` da `_TEMPLATE.md`.
3. Esegui la ricerca (§2.2-2.3).
4. Rigenera gli indici: `python scripts/check.py --write-index`.
5. Valida: `python scripts/check.py`.

## 4. Aggiornare un servizio esistente (flusso diff/review)
1. Rigenera il contenuto in una cartella di staging, es. `_staging/services/...`.
2. Confronta con la versione committata:
   ```bash
   python scripts/check.py --baseline _staging
   ```
   Lo script mostra il diff (pratiche aggiunte/rimosse/modificate) per ogni file.
3. Rivedi il diff, sostituisci i file, aggiorna `last_reviewed`.
4. Valida e committa.

## 5. Validazione prima del commit (gate)
```bash
python scripts/check.py                 # coverage + conformità + freschezza
python scripts/check.py --check-links   # valida i link (rete)
```
Tutto verde **prima** di bumpare la versione (allineato alle regole di release).

## 6. Versioning e release
- Bump `version` in `catalog.json` + voce in `CHANGELOG.md`.
- Sincronizza `README.md` (conteggio servizi, struttura, comandi).
- Tag annotato `vX.Y.Z` **solo** quando il lavoro è stabile e i check sono verdi.
- Mai force-push di un tag già rilasciato: in caso, patch di follow-up.

## 7. CI
`.github/workflows/check.yml` esegue `python scripts/check.py` su ogni PR.
````

---

## 9. `scripts/check.py` — validatore + diff-checker (bozza completa)

Pure stdlib (Python 3.8+), nessuna dipendenza. Esce con codice ≠ 0 in caso di errori (gate CI).

```python
#!/usr/bin/env python3
"""check.py — validatore e diff-checker per AWSBestPracticesSkill.

Solo stdlib. Comandi:
  python scripts/check.py                 # coverage + conformità + freschezza
  python scripts/check.py --check-links   # valida anche i link (richiede rete)
  python scripts/check.py --baseline DIR  # diff dei file servizio vs DIR (staging)
  python scripts/check.py --aws-codes F   # confronta catalogo vs service code AWS (uno/riga)
  python scripts/check.py --write-index   # rigenera catalog.md e l'indice in SKILL.md
  python scripts/check.py --max-age-days N # soglia freschezza (default 180)
  python scripts/check.py --json          # output in JSON
Exit code != 0 se ci sono errori.
"""
from __future__ import annotations
import argparse, json, re, sys, difflib, datetime, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
SERVICES = ROOT / "services"
PILLARS = {"Security", "Reliability", "Performance Efficiency",
           "Cost Optimization", "Operational Excellence", "Sustainability"}
ALLOWED_H2 = {"Scenari comuni"} | PILLARS
URL_RE = re.compile(r"\]\((https?://[^)]+)\)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
BULLET_RE = re.compile(r"^\s*-\s+\S")

class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []
    def err(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)
    def note(self, m): self.info.append(m)
    def ok(self): return not self.errors

def load_catalog() -> dict:
    if not CATALOG.exists():
        sys.exit(f"catalog.json non trovato in {CATALOG}")
    return json.loads(CATALOG.read_text(encoding="utf-8"))

def iter_entries(cat: dict):
    for ckey, c in cat.get("categories", {}).items():
        for s in c.get("services", []):
            yield ckey, s

def strip_emoji_h2(h2: str) -> str:
    # rimuove eventuali emoji/prefissi: "🔒 Security" -> "Security"
    return re.sub(r"^[^\w]+", "", h2).strip()

def check_coverage(cat: dict, rep: Report):
    declared = set()
    for _, s in iter_entries(cat):
        declared.add(s["path"])
        if not (ROOT / s["path"]).exists():
            rep.err(f"[coverage] file mancante per {s['name']}: {s['path']}")
    on_disk = {str(p.relative_to(ROOT)) for p in SERVICES.rglob("*.md")}
    for orphan in sorted(on_disk - declared):
        rep.warn(f"[coverage] file non nel catalogo: {orphan}")

def check_conformance(path: Path, rep: Report):
    text = path.read_text(encoding="utf-8")
    if not H1_RE.search(text):
        rep.err(f"[conformance] {path.name}: manca il titolo H1")
    h2s = [strip_emoji_h2(h) for h in H2_RE.findall(text)]
    if "Scenari comuni" not in h2s:
        rep.warn(f"[conformance] {path.name}: manca la sezione 'Scenari comuni'")
    if not (set(h2s) & PILLARS):
        rep.err(f"[conformance] {path.name}: nessuna sezione pilastro valida")
    for h in h2s:
        if h not in ALLOWED_H2:
            rep.warn(f"[conformance] {path.name}: sezione non ammessa '{h}' "
                     f"(possibile info extra oltre alle best practice)")
    # ogni bullet sotto un pilastro deve avere un link
    in_pillar = False
    for line in text.splitlines():
        m = H2_RE.match(line)
        if m:
            in_pillar = strip_emoji_h2(m.group(1)) in PILLARS
            continue
        if in_pillar and BULLET_RE.match(line) and "](http" not in line:
            rep.warn(f"[conformance] {path.name}: bullet senza fonte → {line.strip()[:70]}")

def check_freshness(cat: dict, max_age: int, rep: Report):
    today = datetime.date.today()
    for _, s in iter_entries(cat):
        lr = s.get("last_reviewed")
        if not lr:
            rep.warn(f"[freshness] {s['name']}: manca last_reviewed")
            continue
        age = (today - datetime.date.fromisoformat(lr)).days
        if age > max_age:
            rep.warn(f"[freshness] {s['name']}: {age}g dall'ultima revisione (>{max_age})")

def collect_urls(cat: dict) -> dict[str, list[str]]:
    urls = {}
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            urls[s["path"]] = URL_RE.findall(p.read_text(encoding="utf-8"))
    return urls

def check_links(cat: dict, rep: Report):
    seen = {u for lst in collect_urls(cat).values() for u in lst}
    def probe(u):
        req = urllib.request.Request(u, method="HEAD",
                                     headers={"User-Agent": "awsbp-check"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return u, r.status
        except urllib.error.HTTPError as e:
            return u, e.code
        except Exception as e:
            return u, str(e)
    with ThreadPoolExecutor(max_workers=8) as ex:
        for u, status in ex.map(probe, sorted(seen)):
            if status != 200:
                rep.warn(f"[links] {status} → {u}")
    rep.note(f"[links] controllati {len(seen)} URL")

def compare_aws_codes(cat: dict, codes_file: str, rep: Report):
    aws = {l.strip() for l in Path(codes_file).read_text().splitlines() if l.strip()}
    have = {s.get("aws_service_code") for _, s in iter_entries(cat) if s.get("aws_service_code")}
    for new in sorted(aws - have):
        rep.note(f"[aws] servizio AWS non ancora coperto: {new}")
    for gone in sorted(have - aws):
        rep.warn(f"[aws] in catalogo ma assente dal listino AWS: {gone}")

def diff_baseline(cat: dict, baseline: str, rep: Report):
    base = Path(baseline)
    for _, s in iter_entries(cat):
        cur = ROOT / s["path"]
        old = base / s["path"]
        if not old.exists():
            rep.note(f"[diff] nuovo: {s['path']}")
            continue
        a = old.read_text(encoding="utf-8").splitlines(keepends=True)
        b = cur.read_text(encoding="utf-8").splitlines(keepends=True)
        d = list(difflib.unified_diff(a, b, fromfile=f"baseline/{s['path']}",
                                      tofile=s["path"]))
        if d:
            added = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
            removed = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
            rep.note(f"[diff] {s['path']}: +{added} -{removed}")
            sys.stdout.writelines(d)

def write_index(cat: dict, rep: Report):
    lines = ["# Catalogo servizi\n", "\n",
             f"Generato da scripts/check.py — {cat.get('generated','')}\n", "\n"]
    for ckey, c in cat.get("categories", {}).items():
        lines.append(f"## {c.get('title', ckey)}\n")
        for s in sorted(c.get("services", []), key=lambda x: x["name"]):
            lines.append(f"- [{s['name']}]({s['path']})\n")
        lines.append("\n")
    (ROOT / "catalog.md").write_text("".join(lines), encoding="utf-8")
    rep.note("[index] catalog.md rigenerato")
    # aggiorna l'indice tra i marker in SKILL.md
    skill = ROOT / "SKILL.md"
    if skill.exists():
        txt = skill.read_text(encoding="utf-8")
        block = "".join(lines[4:])  # senza l'intestazione del file
        new = re.sub(r"(<!-- BEGIN:INDEX.*?-->).*?(<!-- END:INDEX -->)",
                     rf"\1\n{block}\2", txt, flags=re.S)
        skill.write_text(new, encoding="utf-8")
        rep.note("[index] SKILL.md aggiornato")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--baseline")
    ap.add_argument("--aws-codes")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--max-age-days", type=int, default=180)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cat = load_catalog()
    rep = Report()

    if args.write_index:
        write_index(cat, rep)
    check_coverage(cat, rep)
    for _, s in iter_entries(cat):
        p = ROOT / s["path"]
        if p.exists():
            check_conformance(p, rep)
    check_freshness(cat, args.max_age_days, rep)
    if args.check_links:
        check_links(cat, rep)
    if args.aws_codes:
        compare_aws_codes(cat, args.aws_codes, rep)
    if args.baseline:
        diff_baseline(cat, args.baseline, rep)

    if args.json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings,
                          "info": rep.info}, ensure_ascii=False, indent=2))
    else:
        for m in rep.info:     print("· ", m)
        for m in rep.warnings: print("⚠ ", m)
        for m in rep.errors:   print("✗ ", m)
        print(f"\n{len(rep.errors)} errori, {len(rep.warnings)} warning.")
    sys.exit(0 if rep.ok() else 1)

if __name__ == "__main__":
    main()
```

Controlli implementati:
- **coverage** — ogni entry del catalogo ha un file; segnala file orfani non catalogati.
- **conformance** — H1 presente, "Scenari comuni" presente, almeno un pilastro valido, nessun H2 non ammesso (blocca info extra), ogni bullet di pilastro ha una fonte.
- **freshness** — segnala `last_reviewed` mancante o oltre la soglia.
- **links** (`--check-links`) — HTTP check di tutti gli URL.
- **aws-codes** (`--aws-codes`) — confronto col listino AWS per scoprire servizi nuovi/scomparsi.
- **baseline** (`--baseline`) — diff staging vs committato per la review.
- **write-index** (`--write-index`) — rigenera `catalog.md` e l'indice in `SKILL.md`.

---

## 10. Piano di build (fasi)

- **Fase A — Scheletro & validazione formato**
  Repo, `SKILL.md`, `catalog.json` (con le categorie e un primo set di servizi), `_TEMPLATE.md`, `scripts/check.py`, `MAINTENANCE.md`, `README.md`. Più **3-4 servizi esemplari** (S3, EC2, Lambda, IAM/DynamoDB) estratti dai doc ufficiali via MCP, per validare il formato con l'utente prima della generazione di massa. `check.py` verde.

- **Fase B — Generazione di massa**
  Workflow con fan-out: un agente per servizio (o batch), interroga AWS Knowledge MCP, estrae solo best practice, scrive il file da template, aggiorna `catalog.json`. Verifica di qualità (conformità + link + un controllo adversariale "è davvero solo best practice?").

- **Fase C — Pubblicazione**
  `check.py --write-index`, `check.py --check-links` verdi, README sincronizzato, repo GitHub `AWSBestPracticesSkill`, push. Tag/release solo quando stabile.

---

## 11. Verifica e qualità

- `python scripts/check.py` (coverage + conformità + freschezza) verde.
- `--check-links` verde (o warning noti documentati).
- Controllo a campione che i file contengano **solo** best practice (no descrizioni/pricing/tutorial).
- Ogni best practice ha una fonte AWS ufficiale.

---

## 12. Non-goal (esplicito)

- Non è una guida introduttiva ad AWS, né documentazione generale.
- Non fornisce pricing, stime di costo, tutorial o codice di esempio esteso.
- Non copre best practice di terze parti o multi-cloud: **solo AWS**.

---

## 13. Decisioni risolte

1. **Raggruppamento per categoria**: confermato.
2. **Lingua dei contenuti dei file servizio**: **inglese** (standard tecnico AWS, più riusabile, miglior triggering anche su prompt in inglese). La conversazione con l'utente resta in italiano.
3. **Soglia di freschezza** di default: 180 giorni.

---

## 14. Addendum (richiesta utente, 2026-06-29)

### 14.1 Documenti generali (`general/`)
Oltre ai file per servizio, una cartella `general/` con best practice **cross-service** non legate a un singolo servizio:
- `general/well-architected.md` — principi generali dei 6 pilastri
- `general/security-baseline.md` — baseline sicurezza account (root MFA, IAM, CloudTrail, GuardDuty org-wide)
- `general/multi-account-organizations.md` — landing zone, Control Tower, OU, SCP
- `general/cost-governance.md` — tagging per costo, Budgets, Cost Explorer, Savings Plans
- `general/networking-baseline.md` — design VPC, multi-AZ, minima esposizione
- `general/reliability-dr.md` — backup/DR, RTO/RPO, multi-region
- `general/observability.md` — logging/metriche/tracing baseline
- `general/tagging-strategy.md` — convenzioni di tagging
- `general/sustainability.md` — pratiche di sostenibilità generali

Modellati nel catalogo come categoria `general` con `type: "general"`.

### 14.2 Campo `type` nel catalogo
Ogni entry ha `type: "service" | "general"` (default `service`). `check.py` applica le regole dei pilastri solo a `type=service`; per `type=general` richiede H1 + ≥1 sezione + ogni bullet con fonte + `last_reviewed`. Restano vietate descrizioni/pricing/tutorial.

### 14.3 Comando `/goal` (generazione ricorsiva e parallela)
File `.claude/commands/goal.md` nel repo (tool del manutentore, non parte della skill consumata). Su `/goal [categoria|--stale|--all]`:
1. Il modello esegue `python3 scripts/check.py --json` per la work-list (file mancanti; con `--stale` anche oltre soglia freschezza).
2. Lancia un **Workflow padre** che per categoria avvia un **workflow figlio in parallelo**: `parallel(categorie.map(c => () => workflow({scriptPath: '.claude/workflows/goal-category.js'}, {category, services})))`.
3. Ogni figlio esegue `pipeline(services, generate, verify)`: `generate` interroga l'AWS Knowledge MCP, estrae solo best practice e **scrive il file** dal template; `verify` rigetta descrizioni/pricing/tutorial e conferma le fonti. Loop-until-dry sui falliti.
4. Al ritorno il modello aggiorna `catalog.json` e lancia `python3 scripts/check.py`.

Vincoli Workflow: gli script JS non accedono al filesystem → la work-list passa via `args`; gli agenti (subagent completi) scrivono i file. Nesting di un solo livello (padre→figlio-categoria; il figlio usa agenti, non altri workflow). Update di `catalog.json` centralizzato dopo il ritorno per evitare race.
```
