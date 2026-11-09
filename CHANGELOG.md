# Changelog

All notable changes to this project are recorded here, in the
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) format.

- The date on a section is the day the release PR was authored, not the release day. This departs
  from Keep a Changelog on purpose, because the entry is written before the release exists.
- An entry names no personal data (CLAUDE.md rule 4) and no `@`-mention, because GitHub renders a
  section as the release notes.
- The release workflow fails when a version's section is missing or empty.
- A release that needs a migration says so on its section's first line, which starts with the
  bold word Migration and a colon.

## Unreleased

- `generate-resume` now exits with status 1, after writing the documents, when a document's page
  count cannot be measured. It used to exit 0.
- Contributors can now run a driver session and parallel coder lanes in the shared dev container, as
  the readme's *Driver and lanes* section describes.
- Contributors can now work in the shared dev container, opened through the launcher, with dependencies
  installed by hand with `uv sync`. The local uv floor is now 0.13.6, the uv the dev image ships.
- The development environment, lock and build now run through uv. The wheel ships the same
  modules and package data, and `__version__` now reads the installed metadata. Contributors run
  `uv sync`.
- The page count no longer closes an open Word, a timed-out converter's process tree is killed
  (and so is the Word it started, when that Word can be identified), and a LibreOffice found
  only on PATH is used on Windows.

## [0.1.0] - 2026-11-05

The first tagged release of the packaged legacy generator.
