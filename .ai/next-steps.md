# Next steps

**Now:** Sprint S02, "Foundation and de-risk" (milestone 2), `implementing`. No lanes in flight.
#151 is the next build; its spec comment awaits the maintainer's reaction.

**Just done:**
- The maintainer ran #151's audit-log check on a throwaway repo and relayed the result to
  glunk-works/claude-workbench#1414 (2026-11-10).
- Architect session on **opus** drafted #151's spec and posted it as `glunk-dev[bot]` (a
  `spec-task:` comment). Its spec-mode critic pass (`architect`, `docs-consistency`): 2 rounds,
  converged. The maintainer chose the scoped `RO-D18` wording on a trust-boundary finding.
- No code was written in this session.

**Next:** task #151 — on **sonnet**, in a fresh session, once a maintainer has reacted to its
`spec-task:` comment: build it from that comment alone on branch
`docs/151-audit-log-default-branch`, run the green gate and `/way-of-working:critic-gate`
(`architect`, `security-critic`, `docs-consistency`, by rule), then `/way-of-working:ship` with
the trailers `Closes: #151` and `Decision: RO-D21`. Never merge. Still blocked: #149 on
glunk-works/claude-workbench#1414; #152 and #171 on claude-workbench#1413 and #1379; #191 waits
for the host workflow session that builds #152 and #171.

**HITL Gate: NONE OPEN** — next gate: the maintainer reacts to the spec comment on 151, then approves and merges the docs PR that builds it

**Open for the owner (non-blocking):**
- Tightenings #151's spec critics raised and the spec left out: in the new `RO-D18` residual,
  "the residual above" names the dispatch-and-approve bullet, where "another instance of plan
  §5's accepted residual, like the bullet above" is exact; ruleset deletion is caught by the
  read-back's by-id list, not its history; and a numeric width cap (99) with a runnable check.
- Neither #117 nor #118 owns the project's display title (`CLAUDE.md` and readme headings, the
  GitHub repo description). Pick an owner.
- `RO-D18` covers tags but not release assets: an account with write access can replace a
  published release's assets, and the trust root is now an org. Worth a residual line in `RO-D18`.
- `RO-D20`'s residual says the wheel is built "in a job that uses uv's cache", but every
  `setup-uv` step sets `enable-cache: false`. Correct the entry (it belongs to #112).
- The `RO-D21` read-back list names the auto-merge setting but not its intended value. Record
  `true` as the baseline, and that the maintainer changed `main-required-checks` by hand with the
  admin `gh`, which `RO-D21` says a host session does not do.
- After `RO-D17`, the plan header's "`RO-D1`..`RO-D16`" range and §3.8's subscription sentence are
  stale for `support` mode (the spec kept them unchanged). D1's spec should pick up three things:
  re-run B6 items 1, 4, 7 and 9 under `--bare`, pass the API key only to the `support` child, and
  create run directories under a parent only the user can write to.
- Still open from #100: a manual run of the `ruleset-drift` workflow, and its last two done-whens (a
  green run, and that a PR with a red `secrets / scan` cannot be merged).
- The Sheet CSV export in #34 (on S03), which blocks C3.
- The `depends_on` markers on #52, #53, #54 (S06) and #55 (S07) name issues in other milestones, so
  `plan-depends.sh` reads each as waiting on every earlier item. Worth its own backlog issue.
- The ruff version is pinned twice, in `pyproject.toml` and `.pre-commit-config.yaml`.
  Dependabot bumps each through a different ecosystem (#110), so a ruff bump arrives as two PRs:
  merge them together. A check that compares the pins is a possible follow-up. Check the first
  `pre-commit` Dependabot PR's title against `pr-title`'s length cap, and the first `docker` one's
  too: its default title is likely over the 72-character cap.
- Watch the first Dependabot `uv` run: it may write a newer `uv.lock` `revision` that fails the
  `UV_LOCKED` jobs, and a `uv_build` bump fails `check_uv_pin` until `UV_VERSION` and the local
  uv floor are both bumped to match (`RO-D23`). A floor bump needs a dev image whose uv meets it,
  and a `UV_VERSION` bump is a host workflow PR (`RO-D21`).
- Tightenings the critics raised on #113 and the build left out, as outside its spec: an explicit
  `checksum:` for `setup-uv`, requiring `[build-system].requires` to be exactly the one pin, a
  hashed install for the wheel smoke test, and a changelog note that the `dev` extra is gone.
- A decision entry in `docs/decisions.md` for the Betterleaks switch is optional.
- The `secrets / scan` pin stops other apps' statuses, but not a PR that adds or edits a workflow.
  Only the maintainer's merge covers that. A ruleset `workflows` rule would close it; check whether
  glunk-works' plan offers one now that the repo has moved.
- Nothing checks that the `ruleset` and `rulesets` blocks in `.ai/project.yml` agree with each
  other. Worth a backlog issue.
- The dev-container entry is the interim `devcontainer` CLI from PowerShell outside the checkout,
  until the launcher in glunk-works/claude-workbench#1276 ships. The checkout must be a fresh clone
  that no container has run on, and the CLI is never run from a shell holding secrets.
- B4 leaves some output unscrubbed, by design:
  - exception tracebacks
  - third-party text at WARNING and above
  - uncaught-exception stderr output

  The bug template warns about the first two. These tightenings from B4's critic pass were accepted:
  - no symlink check on the log file
  - a half-detached handler pair is not repaired
  - the docstring and template say "WARNING" where the filter passes WARNING and above
- Milestone 11's (T01's) description may still list #112, #113 and #115, which are now on S02.
- Raise naming uv in the claude-workbench Python conventions, so the glunk-works repos follow
  (T01's milestone description says this is outside this repo). Place
  glunk-works/claude-workbench#1349 in that repo's milestones.
- If `secrets / scan` fails with `couldn't find remote ref refs/pull/<N>/head`, the cause is
  GitHub, not a secret. GitHub created only the merge ref, and a re-run fails the same way.
  Pushing a commit to the branch creates the head ref (PR #107).
- The spec-mode cap of 4 fix-and-re-run rounds was hit on #113 and #115 (8 rounds). A spec for a
  multi-surface or host-procedure task may need splitting.
- Working-tree copies of `.ai/project.yml`, `CHANGELOG.md`, `CLAUDE.md` and `readme.md` read CRLF
  (index LF) after a branch switch in the dev container, which left the tree dirty; `git restore`
  cleared it. Cause not found.
- The dev container could not arm auto-merge on #159: the permission layer denied
  `gh pr merge --auto`. Arming it needs a permission rule for `gh pr merge` on this repo.
- Under this repo's installation token, resume's ruleset check reads both rulesets but not their
  bypass actors, so it prints inconclusive.
- A workflow PR's build runs in a fresh host clone: the publish script added a `[branch]` tracking
  section to `.git/config` that the spec did not expect. Worth a line in the next spec's preflight.
- `lane.sh prep` uses its `BRANCH` argument verbatim and does not add the issue number, so the
  driver must pass `<type>/<issue#>-<slug>` itself. Worth an upstream check in the plugin.

**Pointers:**
- the plan: [docs/proposals/pipeline-plan.md](../docs/proposals/pipeline-plan.md)
- the decisions: [docs/decisions.md](../docs/decisions.md)
- the sprint plan: https://github.com/glunk-works/resume-orchestrator/milestone/2
