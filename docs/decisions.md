# Decision log (`RO-D*`)

Each entry states the choice and the reason for it, and nothing about how it was reached. A
superseded entry stays in place, with a line naming the entry that replaces it. This repo is
public, so an entry never names an employer, a company applied to, or a personal detail
(`CLAUDE.md` rule 4). The maintainer's decisions below were reworded during the plan's critic
rounds for anonymity and precision. The maintainer's approval of plan task P0.0 confirms the
wording.

## RO-D1 — Deterministic actions in code; routing and judgment in agents

*Decided 2026-11-04 (maintainer). RO-D9 sets the runtime.* Anything that can
be checked, computed or rendered without judgment is a tested Python function: schema
validation, citation and claim-policy checks, AI-tell lint, page fitting, rendering and
naming. LLM roles handle what needs judgment: analysing a job, choosing evidence, writing,
judging support, deciding to interview, revise or escalate. Each role is a prompt plus input
and output schemas, and any provider can run it. **Why:** checks enforced in code hold
whichever model drafts, and the maintainer doesn't want to be locked into one provider.

## RO-D2 — The evidence ledger lives in a separate private repository

*Decided 2026-11-04 (maintainer). RO-D10 sets how changes are approved.* The
canonical career record is YAML in a private repository, created at plan task C2, and its
items carry stable IDs that are never reused. This repo stays public and holds only code,
schemas and synthetic `example_*` data. No LLM role writes the ledger. **Why:** each update
needs history, a diff and a rollback, and personal data has to stay out of a public repo.

## RO-D3 — Tiered claim policy

*Decided 2026-11-04 (maintainer).* Every factual claim cites evidence IDs, and three kinds are
allowed:

- **Restating** a cited fact.
- **Reframing** it in the job's vocabulary, through a broader-term mapping the ledger records.
- An **inference** ("managed a distributed team" → "led and developed engineers"). It is used
  only once the maintainer approves it, after which it's recorded in the ledger as an
  inference item with its basis IDs.

A **new fact** is blocked until the ledger has it. That means any metric, tool, certification,
framework, employer, title or date the cited evidence doesn't contain. **Why:** an
entailment-only rule makes the prose bland, and a permissive rule let a 2026-08 run claim a
compliance framework and a tool category that appear nowhere in the data.

## RO-D4 — Gap interviews run inline, capped

*Decided 2026-11-04 (maintainer).* When a job requirement has no evidence, the interviewer asks
about it before drafting. It asks one question at a time, about the **3–5 heaviest gaps**
only: 3 by default, raisable to 5 at the prompt. This entry is the single place that states
the cap. A skipped gap is counted in the gap
backlog. An answer the maintainer approves is committed to the ledger, and the same run uses
it (RO-D10). **Why:** the ledger records only a fraction of a long career (plan §1.2), and the
moment of applying is when the maintainer is most motivated to recall what the job asks about.

## RO-D5 — The Google Sheet is imported once, then mirrored read-only

*Decided 2026-11-04 (maintainer).* The Sheet is imported into the ledger once. From then on the
ledger is the only place edits are accepted. A deterministic export regenerates a read-only,
Sheet-shaped view so that Perplexity can still read it. Any change Perplexity suggests comes
back as a diff and is imported `unconfirmed`. **Why:** two places that accept edits drift
apart.

## RO-D6 — Import trust follows the last exports made before Perplexity's edits

*Decided 2026-11-04 (maintainer).* At import, a Sheet row identical to its row in that tab's
June 2026 export lands as `confirmed`. The June exports are the `experience.csv`,
`profile.csv` and `certifications.csv` the current pipeline builds from. A row that was added
or changed since then, or that belongs to a tab with no June export, lands as `unconfirmed`,
with `source: sheet-import-post-baseline`. It can be cited only after the maintainer reviews it
once. **Why:** Perplexity has edited the Sheet since those exports, and confirming every row
would turn anything it invented into ground truth that no later check can catch.

## RO-D7 — A final render cites only merged ledger evidence

*Proposed 2026-11-04 (Architect). Superseded by RO-D10 before adoption.* It made a GitHub
merge by the maintainer the approval gate for new evidence.

## RO-D8 — Tailoring runs locally; deterministic ledger chores run in GitHub Actions

*Decided 2026-11-04 (maintainer).* Every stage of a run executes on the maintainer's machine.
The LLM calls inside a run go wherever RO-D9 sends them. GitHub Actions in the private ledger
repo does only deterministic work that ledger changes trigger: validating every change, and
regenerating the read-only Sheet mirror. Driving a run from a GitHub issue or Action is not
planned. **Why:** a live interview needs a terminal, and jobs that a merge triggers belong next
to the merge.

## RO-D9 — Code drives a run; LLM roles run without tools

*Decided 2026-11-04 (maintainer). Partly superseded by RO-D17 for reviewer `support` mode.* `ro tailor` is a Python state machine. It runs every stage,
holds every human prompt, writes every artifact, and owns the only path that writes to the
ledger. Each LLM role is a single call that takes a prepared payload in and returns JSON out,
with **no tools**: no shell, no file access, no network. Roles still make the judgments, and
code carries them out and checks them. By default the call goes to headless Claude Code
(`claude -p`) on the maintainer's subscription, from an empty working directory. An API
adapter (Anthropic, Gemini, Bedrock, …) can run any role instead. Plan task B6 checks whether
`claude -p` can run tool-less on the subscription. If it can't, B6 records an entry choosing
the fallback. Claude Code remains the tool for developing and planning this repo. **Why:** an
LLM that reads an untrusted job req while holding a shell, file writes or `gh` can be steered
into acting. A role with no tools can only be steered into *writing* something, and every
claim it writes must still pass code checks that the req can't instruct. Req text reaches
those checks only as data, as a vocabulary source and as the `req_reference` allowlist. Code
extracts req vocabulary itself, so the req can add terms to what the checks enforce but can't
remove any.

## RO-D10 — Approvals happen at an interactive console and are committed directly

*Decided 2026-11-04 (maintainer).* New evidence is shown to the maintainer as a plain-English
card in `ro`'s terminal: interview answers, approved inferences, mined items, post-baseline
import rows. The maintainer confirms, edits or rejects each card. The same goes for the run's
other human choices: proceeding after triage, picking between variants, waiving a reviewer
finding. `ro` takes an approval only from an interactive console. It refuses pipes, the null
device, CI, `claude -p` and a Claude Code tool shell. End of input counts as a rejection, and
no prompt has a default. A process running as the maintainer can still reach a console,
directly or through a pseudo-terminal, and answer. The plan accepts that residual risk (plan
§5). Approved items are committed to the ledger by
`ro` and pushed. Git history is the record, and any item can be reverted. A final render
cites only items that are confirmed, with unchanged content, on the remote's current default
branch. **Why:** it keeps approval inside the maintainer's own flow at the terminal. Once no
run-time LLM holds a tool (RO-D9), the only way around it is a process the maintainer is
already running.

## RO-D11 — Sheet data moves by manual CSV export, never through the Sheets API

*Decided 2026-11-04 (maintainer).* The maintainer exports each tab by hand
(*File → Download → CSV*) for the one-time import. The read-only mirror (`RO-D5`) is published as
CSV files in a ledger workflow artifact, and the maintainer imports them into the Sheet whenever
Perplexity needs fresh data. Nothing in the system holds a Google credential. **Why:** the
import happens once, the mirror's only reader is Perplexity (whose credits are the problem
being solved), and an API path would add a credential and identity-federation setup for very
little gain. Revisit only if Perplexity remains in regular use after the engine ships.

## RO-D12 — Application tracking stays live in the Sheet

*Decided 2026-11-04 (maintainer).* Only the experience, skills, certification, education and
profile tabs are imported. The freeze and the mirror (`RO-D5`) apply to those tabs only. The
applications tab stays live in the Sheet, the maintainer goes on editing it there, and the
mirror never touches it. `ro`'s local runs index records which files went where. **Why:** an
applications log is activity, not evidence. It probably holds other people's contact details,
and it has no place in drafting payloads or ledger history.

## RO-D13 — Only providers on a no-training allowlist receive career data

*Decided 2026-11-04 (maintainer).* `ro` sends ledger, exemplar, interview or job-req content only
to a provider that its config marks as approved, and refuses any other. The approved providers
are:

- the Claude subscription, with the maintainer confirming that the account's training setting
  is off
- the Anthropic API
- AWS Bedrock
- Gemini, only on a billed key (until that is confirmed, A4 waits)
- Perplexity, only once its API terms are checked (E3)

Contact fields are never sent to any provider: code renders the header. This applies to the
legacy path as well as to `ro`: plan A2 strips the contact block from its payload, and its use
with real data waits until the provider's tier is confirmed. **Why:** a long career
history should not become training data or human-review material on a free tier.

## RO-D14 — LinkedIn positions are an excavation source and a consistency check

*Decided 2026-11-04 (maintainer).* A LinkedIn data export feeds excavation through its
Positions, Profile and Skills CSVs only. Connections, messages and recommendations are never
read, the archive is never copied into the ledger, and its contents are never sent to a
provider. Code reports, as warnings, every title or date mismatch between LinkedIn and the
ledger's roles. **Why:** the maintainer wrote the LinkedIn descriptions, so they are a
higher-trust source than generated resumes. Recruiters also compare a resume with LinkedIn,
so mismatches should be found first.

## RO-D15 — The ledger repository stays on the maintainer's personal account

*Decided 2026-11-04 (maintainer).* The private ledger repo is owned by the maintainer's personal
GitHub account, not the glunk-works org, and it stays there after this code repo moves (plan
F6). Its URL lives only in the maintainer's user config. **Why:** the org runs agent automation
and GitHub Apps. Keeping personal data outside the org keeps it out of that blast radius,
without an App audit every time an App is installed.

## RO-D16 — Every role stays dated; early roles are compressed, not hidden

*Decided 2026-11-04 (maintainer).* Every role appears with its real title and dates, grouped
under its employer, and certification years are shown. An empty section, such as Education
when there is no degree, is not rendered. Bullets go to roles inside a detail window, with a
per-role budget that shrinks the further back the role ended. Roles before the window default
to their title line alone, with at most one bullet each, used when it targets a requirement.
The window and taper numbers live in plan §3.9. They are configurable defaults, revisited once
real runs have been measured (plan E1). **Why:** applicant tracking systems compute years of experience from dated
entries. Undated "earlier career" lines would shorten long tenures and hide early roles that
add value. A wide window keeps foundational experience, while the taper keeps the resume
within two pages.
Hiding the timeline costs more than any age-bias benefit it might buy.

## RO-D17 — Reviewer `support` mode runs `--bare` with an API key

*Decided 2026-11-05 (maintainer).*
Reviewer `support` mode runs `claude -p --bare` with an API key, plus the same tool-less flags as
every other role (`--tools ""`, `--strict-mcp-config`, `--no-session-persistence`,
`--disable-slash-commands`, `--permission-mode dontAsk`). Every other role and mode keeps
RO-D9's default, headless Claude Code on the subscription. **Why:** on the subscription, `claude -p` loads `CLAUDE.md` files under the
§3.6 flags (user-level and parent-directory files both reached the model), and `--bare` is the
documented way to skip them. It accepts only an API key. The other roles may accept the
maintainer's `CLAUDE.md` as contamination (plan §3.6). `support` mode judges whether evidence
backs a claim, so it must see nothing but its payload. Nothing else moved: the spike showed
`claude -p` tool-less, with no transcript written and no hook firing under the flags. `--bare` itself was not run in B6:
D1 re-runs items 1, 4, 7 and 9 under it before relying on it. Tool-less
means zero tools, MCP servers, skills and slash commands in the init event, and only Claude Code's
built-in plugins, agents and output style; the plan's wording of zero in every category cannot be
met, because the built-ins are always listed. The maintainer accepted that reading, and D1's check
will assert it.

## RO-D18 — Releases are dispatched from `main`, never tagged by hand

*Decided 2026-11-05 (maintainer). Partly superseded by RO-D20 for the version source and the build residual.*
A release is cut by dispatching the `release` workflow from `main`, never by pushing a tag. The
tag is derived from the version in the package `__init__.py`, and it comes into existence only
when the draft release is published. Every `ci.yml` job re-runs at the release commit. The
`release` environment's main-only deployment branch policy, with the maintainer as required
reviewer, is the control, because the release App's key lives only there. The workflow's own
branch guard only fails fast. The release App is the only identity that creates `v` tags, and two
tag rulesets enforce it: `protected-release-tags` stops anyone moving or deleting a `v` tag, and
`release-tag-creation` lets only the App create one. A release carries three assets: the wheel
that CI's smoke step tested, CI's SBOM and a `SHA256SUMS` file. The SBOM describes CI's
development environment, not the wheel's runtime closure. The wheel also carries a build
provenance attestation, verified against the release workflow on `main`. The changelog section
for the version, followed by the commit subjects since the previous tag, is the release's notes. A published tag is never moved or reused, and a defect is
fixed by the next version. **Why:** installs pin a tag, so it must name a reviewed commit on
`main` and never change, and a hand-made tag can disagree with the code it names.

Residuals:
- The ruleset drift check reads the branch rules only, so the tag rulesets are not drift-checked.
- The wheel is built in a job that uses the pip cache and an unhashed build backend, so the
  attestation covers the built bytes, not a hermetic build.
- A process running as the maintainer can dispatch and approve a release, an instance of plan §5's
  accepted residual. The `CLAUDE.md` clause and the `gh workflow run` deny rules in
  `.claude/settings.json` are conventions against it, not controls.

## RO-D19 — The project is renamed resume-orchestrator

*Decided 2026-11-06 (maintainer).*
The project is renamed from resume-optimizer to resume-orchestrator: the GitHub repo, the
distribution, the import package (`resume_orchestrator`) and the application name. The initials
stay RO, so the `ro` CLI, the `RO_*` environment variables and the `RO-D*` IDs keep their meaning.
The rename lands in two parts, which may land in either order:
- **This code repo** is renamed together with its transfer to glunk-works (plan F6), so its URL
  changes once. The rename does not touch the private ledger repo, which stays on the
  maintainer's account (RO-D15).
- **The package, the distribution and the application name** are renamed in their own task, after
  the toolchain moves to uv, so the uv move and the package rename do not both rewrite
  `pyproject.toml` and the gate at once. The label namespace for labels the pipeline writes moves
  from `resume-optimizer/…` to `resume-orchestrator/…` with it.

The old names key stored state: the default ledger, runs and log directories (`APP_NAME`) and the
keyring service the provider keys are stored under (`SERVICE_NAME`). Where old state exists, the
renamed code never starts empty:
- **Directories:** each old directory is carried over, or the run refuses, naming the directory by
  its variable, never by its path.
- **Provider keys:** the credentials module stays a reader. A provider key still stored under the
  old service makes it refuse and name both service names, and the maintainer moves the entry with
  `python -m keyring set` and `del`.

The data-path check in `paths.py` recognises a checkout under either package name. So the old names
stay in `src/` only where old state is detected or carried over, or an old checkout is recognised.
Residual: a `resume-optimizer` distribution installed before the rename (its `generate-resume` and
`build-resume-state` entry points today) cannot recognise a renamed checkout, so it is upgraded
before a data path is pointed near one.
**Why:** "optimizer" reads as ATS keyword-tuning, a promise the legacy generator made and the
pipeline does not: every factual claim cites ledger evidence (RO-D3). "Orchestrator" names what
the plan builds, a run that code drives through gates and tool-less roles (RO-D1, RO-D9).

The glunk-works org already uses "orchestrator" for its development loop. The maintainer accepts
the reuse, because orchestration is a role many components can have. `CLAUDE.md`'s *Two
vocabularies* table keeps the product's run orchestration apart from the dev workflow's.

## RO-D20 — The toolchain moves from Hatch to uv

*Decided 2026-11-07 (maintainer). Partly superseded by RO-D23 for the local uv floor.*
uv manages the project environment, the lock file (`uv.lock`, committed) and command running
(`uv run`), and `uv_build` replaces `hatchling` as the build backend. Hatch is no longer used. The
move lands in its own task, after which `RO-D19`'s package rename follows.
- **Version source:** the version is a static `version` in `pyproject.toml`, the single source. The
  package `__init__.py` stops being a version source. The release tag is derived from the version
  in `pyproject.toml`; the rest of `RO-D18`'s tag rules are unchanged.
- **uv's pin:** CI installs uv at an exact version, set in the workflow files as an `env:` value
  named `UV_VERSION`, never a repository or organization variable, which sits outside review. CI
  checks that every copy of it agrees with the `uv_build` pin in `[build-system]`.
  `required-version` in `pyproject.toml`'s uv settings is a floor for local use, not a pin. The
  local floor was lowered to 0.13.6, the uv the shared dev image shipped when #115 adopted it, so the
  container can run the project.
- **The interpreter:** every workflow job that installs the project or its dev dependencies gets
  Python from uv, not from `actions/setup-python`. That covers every job in `ci.yml`, the advisory
  3.15 job and the `test` job that builds and smoke-tests the wheel included. If uv cannot provide
  a 3.15 interpreter, that one job may keep `actions/setup-python` and point `UV_PYTHON` at it. A
  job that installs neither and only runs a standalone script may keep `actions/setup-python`: the
  `release` job in `release.yml`, which uses the wheel CI built, and the `pr-title` and
  `ruleset-drift` workflows.
- **Ruff:** its version follows this repo's own Dependabot pins, no longer the version the
  glunk-works repos use. The pins in `pyproject.toml` and `.pre-commit-config.yaml` stay equal, so
  their Dependabot PRs are merged together.

**Why:** the shared devcontainer base image in `603-Identity/devcontainers` names uv as the project
manager for every Python repo, reserves `/workspace/.venv` for the uv project environment, and
ships no Hatch, and this repo is due to adopt that devcontainer. Its glunk-works peers used Hatch
when this was decided, so this repo leads them until the workbench's Python conventions name a
tool.

Residual: the wheel is built in a job that uses uv's cache and a build backend pinned to an exact
version but not by hash, so the attestation covers the built bytes, not a hermetic build. This
replaces `RO-D18`'s second residual for the uv build.

## RO-D21 — The repo cuts over to declared identities and a fresh-session review gate

*Decided 2026-11-07 (maintainer).*
`.ai/project.yml` declares `identities` as a map, and a PR that touches `code_paths` cannot merge
until the reviewer App posts a fresh-session review that passes on its current head. Every PR into
`main` also needs the code owner's approval. The cutover follows the plugin's
`reference/cutover.md` at `v0.30.0`, and task F7 in the plan carries it (issue #88).
- **Identities and the gate:** `maintainer` is `Seuss27`; the Apps are `glunk-dev[bot]` (the dev
  App, `commit_route: api`), `glunk-review[bot]` (the reviewer) and `glunk-loop[bot]`, which the
  loop never uses here but which readers now refuse as an author. The gate is
  `architect-review`, triggered on `code_paths`. `CLAUDE.md` joins `code_paths`, because it
  changes agent behaviour as much as `.claude/` does. `agents.diff_rule` stays: it selects critics
  for the pre-PR pass and covers `docs/` and other paths outside `code_paths`.
- **Two rulesets:** `main-required-checks` keeps the status checks, all pinned to GitHub Actions
  (15368), and `architect-review` is added to it. The maintainer added it to
  `main-required-checks` themselves, by hand, with a `gh` login that holds admin rights on the
  repo, not through any Claude Code session, by 2026-11-09. `main-code-owner-approval` holds the
  code owner's approval, with no bypass actor: code-owner review, stale reviews dismissed on push, and
  last-push approval. `.github/scripts/check_ruleset.py` accepts an entry with no status checks.
- **Who opens and who approves:** the only code owner is `Seuss27`, and GitHub does not let an
  author approve their own PR, and the approval ruleset's last-push rule refuses an approval from
  whoever pushed last. So `Seuss27` opens no PR after the cutover. `glunk-dev[bot]` opens every ordinary PR and
  Dependabot its own. `glunk-admin[bot]` opens every other PR that adds, edits or deletes a
  workflow file. `Seuss27` approves and merges.
- **App commits:** the dev App publishes through the REST git data API with the plugin's
  `api-commit.sh`, so each commit is authored and committed by the App and signed by GitHub, and no
  `git push` from a container is needed. `main` does not require signed commits.
- **Workflow PRs:** the dev App has no Workflows permission, and `api-commit.sh` refuses
  `.github/workflows/`. A workflow PR is built by a host session in a fresh clone made for that
  build and published with a short-lived `wow-admin` token holding `contents`, `pull_requests` and
  `workflows` write. No dev or review container runs while that token is live. Every other
  dev-workflow session runs in a dev container.
- **Ordinary PRs wait:** between the cutover merge and the dev App's installation (below), no
  dev-workflow identity may open an ordinary PR: `Seuss27` is barred, and `glunk-admin[bot]` opens
  workflow PRs only. Dependabot keeps opening its own, which wait for the check to be required
  and for the review the Consequences below describe. #115 is itself a workflow PR, so it is the
  first dev-workflow PR after the cutover.
- **Order:** the second GitHub account's write access is removed before the cutover PR merges. The dev
  App is installed, and the repo added to the token broker, only after the check is required and
  #115's PR has merged. That is later than `reference/cutover.md` requires, and it means no
  `glunk-dev` session can touch the cutover PR. The reviewer App is installed on this repo before
  the cutover PR merges, and the dev App's registration holds no Workflows and no Administration
  permission.
- **The gate job takes no checkout:** it holds `statuses: write`, so it checks out no ref and
  runs no local action or repo script. That goes further than `reference/cutover.md`, which names
  those only as a limit of the integration pin.
- **The `release` environment:** it admits only `main` and requires `Seuss27`'s review
  (`RO-D18`). The cutover also requires that `Seuss27` is the only required reviewer and that
  admins cannot bypass it. GitHub's default lets admins bypass, so the cutover changed this
  setting: `can_admins_bypass` was turned off on 2026-11-07, before the cutover PR was published.

Consequences:
- Readers trust by id, not by `author_association`.
- A spec comment, including one already posted on another open task, is used only after a
  maintainer's reaction after its last edit.
- Under a map the builder never reads a task issue's body, as the plugin's `coder` agent says.
- The review is posted by the host launcher as `glunk-review[bot]`. The launcher runs no Claude
  Code session on the host; the review runs in its container.
- `glunk-admin[bot]` is not declared in `identities`, so a review of a `glunk-admin` PR takes
  the plugin's untrusted path, with no local execution.
- Every Dependabot PR touches `code_paths`, so it needs a passing `glunk-review[bot]` review on
  its head too.
- A fork PR cannot pass the gate.

Residuals:
- A host session can reach more than `Seuss27`'s credential: the host's identity directory also
  holds the reviewer and dev Apps' keys, a Claude credential and the installed identity tools. A
  misbehaving host session could open a PR as `glunk-admin`, mint a `glunk-review` token and post
  a passing review, then approve and merge as `Seuss27`. It could also replace `wow-admin` to
  catch its passphrase. What bounds this is the rule that a host session never approves, merges or
  changes settings, and the maintainer's check that their own approval is a PR's only one. This is
  the plan §5 residual, and it narrows to workflow PRs once other sessions run in containers.
- While a `glunk-admin` token is live, it can push to or delete any branch but `main` and create
  tags other than the `v` tags `RO-D18` reserves. It can create, edit or delete releases on any
  tag, release assets included, and push a branch workflow that declares any write permission a
  job can request for itself: `statuses`, `contents`, `id-token` and `actions` among them. That
  workflow could post the `architect-review` context, push as `github-actions[bot]`, mint OIDC
  tokens and attestations under this repo, or use `actions` write as the Actions point below
  describes. The code
  owner's approval bounds only what merges. A short-lived token, revoked after use, with no dev or
  review container running meanwhile, bounds the rest, with two exceptions. A workflow PR's own
  workflows run on `pull_request`, so it can post `architect-review` (for instance from a job of
  that name with no permissions), and the edited workflow keeps posting after the token is revoked.
  On a PR that adds or edits a workflow, `architect-review` is therefore not evidence of a review:
  before approving, the maintainer confirms the `glunk-review[bot]` review on the head. The other
  exception is a branch the token pushed: a workflow on it keeps firing on later pushes, and on a
  PR opened from it, so those branches are deleted, or checked for stray workflows, before any dev
  container runs again.
- The `glunk-admin` installation itself holds Administration, Environments and Actions write. Only
  the `--perms` passed to `wow-admin` keeps them off a minted token. No Claude Code session, on
  the host or in a container, mints a token with any of the three: only the maintainer does,
  outside any session, and such a token falls under the key-rotation bullet below. That is a rule,
  not a technical control: the installation still holds the permissions.
  - With Administration a token could change or delete any ruleset, or add a bypass actor to it.
    On the branch rulesets that defeats the required check and the code owner's approval. On the
    two tag rulesets of `RO-D18`, with `contents` write as well, it lets a token move, delete or
    create `v` tags. It could change or delete the `release` environment, whose reviewers, admin
    bypass and main-only branch policy `RO-D18` and this entry's `release` bullet rely on. It could
    invite a collaborator, grant a team access, add a deploy key or register a self-hosted runner:
    write paths that outlive the token. It could rename, transfer, delete or make private the
    repo, and turn off secret scanning's push protection. The daily `ruleset-drift` workflow sees
    none of the environment, write-path or tag-ruleset changes, and little of the branch-ruleset
    ones (the drift residual below).
    A read at one moment cannot show a ruleset, `main` or a `v` tag that was changed and put back,
    and an environment has no history endpoint (the release-environment rule below). So after each
    token the maintainer reads back what Administration can change, including:
    - the four rulesets by name and id (`main-required-checks`, `main-code-owner-approval`, and
      `RO-D18`'s `protected-release-tags` and `release-tag-creation`), with each one's enforcement,
      target, branch or tag conditions, rules and bypass actors. All four must still be listed, and
      any other that `GET repos/glunk-works/resume-orchestrator/rulesets` lists is a finding;
    - evidence that nothing was changed and put back. Each ruleset's change history
      (`GET repos/glunk-works/resume-orchestrator/rulesets/<id>/history`) has no entry from the
      token's life. Both branch rulesets target the default branch, so a default-branch change
      leaves no ruleset history, and a matching head for `main` proves nothing by itself: the
      activity for `refs/heads/main` (`GET repos/glunk-works/resume-orchestrator/activity?ref=...`)
      shows only the maintainer's approved merges, the default branch was not changed during the
      token's life (the web UI's audit log; the REST endpoint is unavailable on this plan), no `v`
      tag was added that the maintainer did not release, and every `v` tag is still at its release
      commit;
    - the `release` environment's protection, the default branch, and the repo's name, owner and
      visibility;
    - the workflows, compared in both directions (`GET repos/glunk-works/resume-orchestrator/actions/workflows`)
      against the workflow files tracked under `.github/workflows/` on `main` (read with
      `GET repos/glunk-works/resume-orchestrator/contents/.github/workflows?ref=main`):
      - every tracked workflow file appears in the listing with state `active`; one missing or not
        `active` (a disabled daily `ruleset-drift`, for example) is a finding;
      - every listed workflow whose `path` is not a tracked file on `main` is a finding, except
        two expected kinds: Dependabot's two dynamic entries (`path`
        `dynamic/dependabot/dependabot-updates` and `dynamic/dependabot/update-graph`; any other
        `dynamic/` entry is a finding), and the
        files that a workflow PR published with that token adds, if there is one;
      - the listing cannot show a branch's edit to a workflow at a path already on `main`, because
        the path is the same. The rule above, that the token's pushed branches are deleted or
        checked for stray workflows, covers that. Nor can a point-in-time listing show a workflow
        that was disabled and put back;
    - the repo's Actions settings (the default `GITHUB_TOKEN` permissions, whether Actions may
      create or approve a PR, the allowed-actions policy and SHA pinning, and the fork-PR approval
      policy), the auto-merge setting (`allow_auto_merge` is `true`, written as the baseline the
      read-back compares against, not as a claim about the live setting) and secret scanning's
      push protection;
    - the repo's write paths: collaborators with their permission levels, pending invitations,
      teams, deploy keys, self-hosted runners (expect none) and App installations.
  - With Environments it could change that environment's secrets or variables, which `release.yml`
    reads.
  - A change to the `release` environment's reviewers, branch policy or admin bypass needs
    Administration. It can be put back, and no endpoint the read-back calls shows what changed,
    though the web UI's audit log may. A branch workflow with `environment: release` could read
    the release App key meanwhile. So, as a rule (the maintainer confirmed it as policy on
    2026-11-09), a token minted with Administration, Environments or Actions is treated as exposing
    that key: the key is rotated (the old key is
    deleted, because a new one does not revoke it, and installation tokens already minted stay
    valid for up to an hour), and the runs, deployments and releases since the mint are reviewed,
    with the release App's `v` tag and branch activity. Actions counts although a token with it
    cannot read the key (a dispatch of `release.yml` still waits on the `release` environment's
    review): it can delete workflow runs and their logs, part of the record that review of runs,
    deployments and releases reads. A token minted with `--perms` for `contents`,
    `pull_requests` and `workflows` write, as the cutover PR's token was, holds none of the three.
    It can reach the same deletions (the Actions point below), and this entry leaves open
    whether such a token should trigger rotation too.
  - With Actions it could dispatch `release.yml`, still gated by that environment's review,
    disable the daily `ruleset-drift` workflow, or delete workflow runs, logs and artifacts, which
    are evidence of what a token did. A branch workflow pushed by any token with `workflows` write
    can request `actions` write for its own job, so these are reachable without the Actions
    permission on the token. Such a job cannot request Administration or Environments.
- No automated check reads the `pull_request` rule's parameters or who a ruleset's bypass actors
  are; only the manual read-back by id does.
  Run by a repo admin, `ruleset-drift.sh` reports, per ruleset, the missing types and checks,
  whether a `pull_request` rule applies, and the bypass-actor count. Run by anyone else, it reports
  every entry as inconclusive, or as missing when it cannot find the name. So
  `/way-of-working:resume` running as `glunk-dev` gets no ruleset signal. The daily `ruleset-drift`
  workflow sees only rule types, checks and their pins, pooled across rulesets, so any other
  change to a ruleset goes unseen by it. Because the approval ruleset's rule types are all carried
  by `main-required-checks` too, that includes anything that stops the approval ruleset applying to
  `main`: its deletion, a move off `active` enforcement or a change to its target.
- `docs/` and the other rule-4 paths outside `code_paths` rest on the approval and the critic pass
  alone.

## RO-D22 — A run fails when a page count cannot be measured

*Decided 2026-11-09 (maintainer).*
When a document's page count cannot be measured, `generate-resume` exits with status 1 after it
has written every document and printed every report. It does not set those documents aside or
rename them, because they were not refused. A refused document takes precedence: when one
document is refused and another is unmeasured, the run exits as it does for a refused document.
D5's render stage also fails the run when a page count cannot be measured, and D5 decides its
file naming and handling. This extends plan §3.9's rule that render fails loudly when neither
converter works to every failed count. **Why:** a zero exit reports a finished run although a
document's page count was not produced, so its length limit could not be checked.

## RO-D23 — The local uv floor equals CI's pinned uv

*Decided 2026-11-10 (maintainer).*
The `required-version` floor under `[tool.uv]` in `pyproject.toml` must be exactly `>=` followed by
the uv version CI pins (`UV_VERSION`), which is also the `uv_build` pin. `check_uv_pin.py` enforces
it in CI, and refuses a `uv.toml` beside `pyproject.toml`, which uv reads in place of `[tool.uv]`.
Every `UV_VERSION` bump now also raises the floor, so it needs a dev image whose uv meets it. No
automated check ties the dev image's uv to the floor, because CI checks only its own uv, so the
code owner confirms the image's uv before approving a change to the floor or to the image's FROM
line. This supersedes the part of `RO-D20` that set the floor below CI's pin.
**Why:** a local uv older than CI's can write a lock or a build that CI's uv would not.
