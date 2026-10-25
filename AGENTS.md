# Agent guide — Thought2English (repo: englearn)

A macOS SwiftUI app (menu bar + window) that turns Chinese or English notes into two English versions, Spoken Script and Formal Writing, using the user's own Gemini or DeepSeek API key. The product is named **Thought2English**; the SwiftPM package, executable and repo are named `englearn`.

## Layout

- `Sources/englearn/` — the whole app. `EnglearnApp.swift` (menu bar + window), `ComposeView`/`HistoryView`/`SettingsView`/`CompareView` (UI), `LLMService` with `GeminiClient` and `DeepSeekClient`, `PromptBuilder`, `OutputParser`, `DiffHighlighter`, `HistoryStore` (SQLite), `SpeechService` (system speech).
- `Package.swift` — SwiftPM, macOS 13+, single executable target, no dependencies.
- `scripts/package_app.sh` — release build plus `dist/Thought2English.app` (Info.plist written by the script). `scripts/build_icon.sh` builds `Assets/AppIcon.icns` from `Assets/IconSource.png`.
- `.github/workflows/ci.yml` — builds on push/PR to `main`. `release-homebrew.yml` — runs only on `v*` tags (or manually); see `RELEASING.md`.
- `PRIVACY.md` — what is stored and sent. Keep it accurate when you change storage or requests.

## Build and run

```sh
swift build                     # debug build
./scripts/package_app.sh        # what CI runs; ~30 s; creates dist/Thought2English.app
open dist/Thought2English.app
```

There is no automated test suite. Verify by building, and say what you did not run. Generating text needs a real API key, so do not claim end-to-end verification without one.

## Rules

- Never commit API keys or history databases. Keys live only in the user's app preferences at runtime; never log or print them.
- Do not call a model provider on the user's behalf without being asked, and never use someone else's key.
- Release only by pushing a `v*` tag, and only when the user asks. Do not create tags, releases or push on your own.
- Keep `PRIVACY.md` and both READMEs in sync when behavior changes.
- No personal data in the repo (names, local paths, real notes in screenshots).
