# Demo GIF

`../demo.gif` is built from the real screenshots in `Assets/screenshots/` plus HTML overlays (typed draft, click highlight, result wipe, captions). The Spoken Script, Formal Writing, Notes and History content all come from the screenshots; the typed draft text is the draft shown in them.

Rebuild (macOS, needs Google Chrome, ffmpeg and gifsicle):

```sh
python3 docs/demo/build_demo.py
```

Set `DEMO_FRAMES_DIR=/some/dir` to cache rendered frames between runs.
