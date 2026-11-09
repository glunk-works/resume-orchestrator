# Next steps

**Now:** Sprint S02, "Foundation and de-risk" (milestone 2), `implementing`. The first lane ran
end to end: #75 was built in a lane and merged as #166. #155 and #88 are the milestone's open issues.

**Just done:**
- Driver session on **opus**: `/way-of-working:resume` printed `Lanes: none`. #75 was moved from
  S07 into S02. Its spec was drafted by a `wow-lane.ps1 -Spec 75` session (critic gate: 3 rounds,
  converged) and approved. The lane, prepped with `lane.sh prep`, built #75 and shipped #166 as
  `glunk-dev[bot]`. The architect review passed with two non-blocking findings, now tracked in #167.
  The maintainer merged #166 (2c60b51), and `lane.sh done 75` cleaned up the lane.
- A driver retro and a feature audit of the plugin against this repo became the cutover feedback.
  It was relayed upstream through #169, which is closed and names the workbench issues.
  claude-workbench#1349 is closed.
- Filed #168 (pin line endings to LF across the repo; land it when no lane is in flight).
- No code was written in this session, so it had no critic pass of its own.

**Next:** close out #155 in a driver session on **opus**: post one comment recording the host steps
and the first lane run (#75, PR #166, feedback relayed via #169), close #155, then decide with the
maintainer what remains of #88. #88's approved spec reads `stale` and touches a workflow file, so a
lane cannot build it. This line carries no `task #N —` token on purpose, so resume waits.

**HITL Gate: NONE OPEN** — next gate: the maintainer confirms the #155 outcome comment and scopes what remains of #88

**Open for the owner (non-blocking):**
- Milestone descriptions are stale after #75's move: S07's Build order still lists #75, and S02's
  has neither #75 nor a *Lanes* line (`lane-groups.sh`). #167 and #168 have no milestone. All of
  this is a `/way-of-working:plan-sprint` pass, run when the maintainer schedules it.
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
