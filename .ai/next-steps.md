# Next steps

**Now:** Sprint S02, "Foundation and de-risk" (milestone 2), `implementing`. #88's PR 1 (#148),
#112, #113, #115 and #156 are built and merged, so `RO-D20` is on `main`, the toolchain is uv, the
review gate and the shared dev container are live, and `.ai/project.yml` mirrors `main`'s ruleset.

**Just done:**
- #155's spec is posted as `glunk-dev[bot]` (comment 6741619016), and the maintainer has reacted to it.
  - Critic pass (spec mode: `architect`, `security-critic`, `docs-consistency`): 3 rounds,
    converged; all on their frontmatter models, no second-opinion round.
  - The spec departs from the issue in four ways: coder lanes only (the pinned plugin has no
    spec lanes); a `CLAUDE.md` deviations row for the release PR's non-append `CHANGELOG.md`
    edit; no `wow-driver.ps1` parameters or record path (it defers to the tool's help); and the
    workflow-PR step stops the dev container, as `RO-D21` requires.
  - The PR does not close #155: four of its done-whens run after the merge, as host steps.

**Next:** task #155 — build #155 (adopt lanes and the driver) from its approved spec comment, in a
fresh session on **sonnet** (coder), which the finder locates. Open the PR as `glunk-dev[bot]` with
"Part of #155" and no `Closes:` trailer, after the critic pass. Then what remains of #88.

**HITL Gate: NONE OPEN** — next gate: the code owner approves the #155 PR after its architect-review gate

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
- The #155 spec's last critic round left three optional tightenings out of the posted text: make
  its "stop the dev container" done-when a grep, make "start them again" name what restarts, and
  defer the container-stop scope to `RO-D21`. The builder may take them.
- After #155 merges: update the host Reference clone, then the post-merge steps its PR body
  lists, recorded in one comment on #155 before it is closed.
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
