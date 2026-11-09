# Next steps

**Now:** Sprint S02, "Foundation and de-risk" (milestone 2), `implementing`. #88's PR 1 (#148),
#112, #113 and #115 are built and merged, so `RO-D20` is on `main`, the toolchain is uv, and the
review gate and the shared dev container are live.

**Just done:**
- #115's build, [PR #153](https://github.com/glunk-works/resume-orchestrator/pull/153), merged at
  `2957507`: the shared dev-App dev container, published as `glunk-admin[bot]` with two short-lived
  `wow-admin` tokens (the first head failed `verify / verify`, so a second token fixed the verifier pin).
  - Critic pass: none ran in the session that built it on the diff. The spec's own critic gate
    converged (8 rounds, spec mode). The fresh-session `glunk-review[bot]` review of record passed on
    head `3fbac3a`, with three non-blocking findings, filed as #154.
  - The `RO-D21` read-backs for both tokens read clean. The in-container checks also pass: the
    green gate, no capabilities, `NoNewPrivs`, a read-only `/run/wow`, and only the image's
    credential helper.
  - Deviation from the spec: the template's caller pinned the v1.5 verifier, which predates dev-App
    mode, so the PR pins v1.6 instead. Filed upstream as 603-Identity/devcontainers#502.
- By the maintainer's say-so, `verify / verify` is now in `main-required-checks` (done with the
  admin `gh`, not a token), and `allow_auto_merge` is on. The broker entry for this repo is in.

**Next:** task #156 — mirror `verify / verify` (integration 15368) into both ruleset blocks of
`.ai/project.yml`, per its approved spec. It needs a `spec-task:` comment first, which
`/way-of-working:spec-task 156` drafts as the dev App from the container, then the maintainer's
reaction. It is an ordinary PR: build it in the dev container as `glunk-dev[bot]`, not from a host
session. Assigned model: **sonnet** (coder). Then #155 (adopt lanes and the driver), then what
remains of #88. Until the mirror merges, the daily `ruleset-drift` run reports `verify / verify`
as unmirrored.

**HITL Gate: OPEN** — first anchor for milestone 2: the maintainer confirms the milestone, and a
spec for #156 is drafted and reacted to. The gate after that is the maintainer approving the #156 PR.

**Open for the owner (non-blocking):**
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
- Decide whether to delete or salvage the local branches `docs/sync-cursor-s02-b2-spec` and
  `fix/73-converter-safety`. Each tip has commits that no merged PR carries.
- The ruff version is pinned twice, in `pyproject.toml` and `.pre-commit-config.yaml`.
  Dependabot bumps each through a different ecosystem (#110), so a ruff bump arrives as two PRs:
  merge them together. A check that compares the pins is a possible follow-up. Check the first
  `pre-commit` Dependabot PR's title against `pr-title`'s length cap, and the first `docker` one's
  too: its default title is likely over the 72-character cap.
- Watch the first Dependabot `uv` run: it may write a newer `uv.lock` `revision` that fails the
  `UV_LOCKED` jobs, and a `uv_build` bump fails `check_uv_pin` until `UV_VERSION` is bumped to match.
  The local uv floor is now below CI's exact pin, and nothing compares them (#154).
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
- A workflow PR's build runs in a fresh host clone: the publish script added a `[branch]` tracking
  section to `.git/config` that the spec did not expect. Worth a line in the next spec's preflight.

**Pointers:**
- the plan: [docs/proposals/pipeline-plan.md](../docs/proposals/pipeline-plan.md)
- the decisions: [docs/decisions.md](../docs/decisions.md)
- the sprint plan: https://github.com/glunk-works/resume-orchestrator/milestone/2
