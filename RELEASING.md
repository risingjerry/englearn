# Releasing (maintainers)

Pushing a version tag builds the app, publishes a GitHub Release, and updates the Homebrew cask.

```bash
git tag v0.2.0
git push origin v0.2.0
```

[`release-homebrew.yml`](.github/workflows/release-homebrew.yml) runs on tags matching `v*` (and manually via *Run workflow*, which derives a version from the run number). It:

1. builds `Thought2English.app` with `scripts/package_app.sh` on a macOS runner,
2. zips it and computes the `sha256`,
3. creates a GitHub Release for the tag with the zip attached,
4. updates the cask in `risingjerry/homebrew-thought2english` (version / sha256 / url).

Ordinary pushes to `main` only run [CI](.github/workflows/ci.yml); they do not publish anything.

## One manual setup step: a secret

In the `englearn` repo → Settings → Secrets and variables → Actions, add `HOMEBREW_TAP_TOKEN`: a GitHub token (fine-grained is fine) with Contents read/write on `risingjerry/homebrew-thought2english`. Without it the release still succeeds and the cask update is skipped.

After a release, users get it with:

```bash
brew upgrade --cask thought2english
```
