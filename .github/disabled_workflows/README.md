# Disabled workflows (21 November 2026)

`cloud-run.yml` and `long-run.yml` ran ACL's studies on GitHub Actions. On 20 November 2026 GitHub disabled the
Mind Lab repository for using Actions as general compute (long simulation jobs). GitHub's terms allow Actions for
building, testing and publishing a repository's software, not for producing research data.

The creator decided (21 November 2026) to disable both here. GitHub only runs workflows in `.github/workflows/`, so these
files are kept for history and never run. Studies run on the creator's PC and on cloud machines the creator rents.
`tests.yml` (code tests), `diagnose.yml` (a short replay check) and `pages.yml` (the website) stay: they are normal use.
