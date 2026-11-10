# Next steps

**Now:** Sprint S02, "Foundation and de-risk" (milestone 2), `implementing`. No lanes in flight.
The milestone's build order and **Lanes:** line say what is open and what each item waits on.

**Just done:**
- Driver session on **opus**. #155 and #88 were already closed with their outcome comments, so the
  old next action was moot. Removed the merged #174 and #176 lanes.
- `/way-of-working:plan-sprint`: placed #152, #150, #182, #187, #149 and #151 on S02, then #190 and
  #191 from the #188 and #189 reviews; closed #183 and #185 as duplicates of #182 and #187.
- Checked the backlog against the plugin: #152 and #171 wait on glunk-works/claude-workbench#1413
  and #1379, #149 on #1414 (filed upstream from a host session); all three carry `status/blocked`.
- #172 unblocked by #186 (dev image uv 0.13.7, confirmed on the host); its spec was redrafted and
  built: #188 (ef52aa9, `RO-D23`). #150 built: #189 (2ec3162). Both lanes cleaned up.
- No code was written in this session, so it had no critic pass of its own.

**Next:** in a driver session on **opus**: once the maintainer has reacted on #182, #187 and #190,
hand over one `wow-lane.ps1 -Spec N` line per issue with the full clone paths, review each posted
spec, then prep its lane. #152, #171, #191 and #149 stay blocked upstream; #151 is the maintainer's
manual check, its result relayed to claude-workbench#1414. This line carries no `task #N —` token
on purpose, so resume waits.

**HITL Gate: NONE OPEN** — next gate: the maintainer reacts on 182, 187 and 190 so their specs can be drafted

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

**Pointers:**
- the plan: [docs/proposals/pipeline-plan.md](../docs/proposals/pipeline-plan.md)
- the decisions: [docs/decisions.md](../docs/decisions.md)
- the sprint plan: https://github.com/glunk-works/resume-orchestrator/milestone/2
