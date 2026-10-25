#!/usr/bin/env python3
"""Build docs/demo.gif from the real README screenshots plus HTML overlays.

Frames are rendered by headless Chrome (2x) from demo.html, then assembled with
ffmpeg palettegen/paletteuse. Usage: python3 docs/demo/build_demo.py
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(HERE, "..", "demo.gif")
EN_LEN, CN_LEN = 270, 104  # length of the typed drafts in demo.html (clamped by JS slice)

C1 = "Type a rough Chinese or English draft"
C2 = "One click: Spoken Script, Formal Writing and Notes"
C2b = "Chinese input works too, same two outputs"
C3 = "Every run is saved in History"
FPS = 10
tl = []  # (state, duration seconds)

def add(state, d=1 / FPS): tl.append((state, d))

done = dict(op=1, rev=1)
# Scene 1: English draft typed, generate, reveal
add(dict(step=1, cap=C1, en=dict(op=1, typed=0, rev=0)), 0.7)
n = 0
while n < EN_LEN:
    n += 9; add(dict(step=1, cap=C1, en=dict(op=1, typed=n, rev=0)))
add(dict(step=1, cap=C1, en=dict(op=1, typed=EN_LEN, rev=0)), 0.5)
for c in (0.3, 1.0):
    add(dict(step=2, cap=C2, en=dict(op=1, typed=EN_LEN, rev=0, click=c)))
for _ in range(7):
    add(dict(step=2, cap=C2, en=dict(op=1, typed=EN_LEN, boxfade=1, rev=0, spin=1)))
for i in range(1, 13):
    add(dict(step=2, cap=C2, en=dict(op=1, typed=EN_LEN, boxfade=1, rev=i / 12)))
add(dict(step=2, cap=C2, en=dict(op=1, rev=1)), 3.2)
# Crossfade to Chinese scene
for i in range(1, 4):
    a = i / 4
    add(dict(step=1, cap=C2b, en=dict(op=1 - a, rev=1), cn=dict(op=a, typed=0, rev=0)))
n = 0
while n < CN_LEN:
    n += 8; add(dict(step=1, cap=C2b, cn=dict(op=1, typed=n, rev=0)))
add(dict(step=1, cap=C2b, cn=dict(op=1, typed=CN_LEN, rev=0)), 0.4)
add(dict(step=2, cap=C2b, cn=dict(op=1, typed=CN_LEN, rev=0, click=1.0)))
for _ in range(4):
    add(dict(step=2, cap=C2b, cn=dict(op=1, typed=CN_LEN, boxfade=1, rev=0, spin=1)))
for i in range(1, 9):
    add(dict(step=2, cap=C2b, cn=dict(op=1, typed=CN_LEN, boxfade=1, rev=i / 8)))
add(dict(step=2, cap=C2b, cn=dict(op=1, rev=1)), 2.6)
# Crossfade to History
for i in range(1, 4):
    a = i / 4
    add(dict(step=3, cap=C3, cn=dict(op=1 - a, rev=1), hist=dict(op=a)))
add(dict(step=3, cap=C3, hist=dict(op=1, hl=1)), 3.5)

def shot(state, path):
    url = "file://" + os.path.join(HERE, "demo.html") + "#" + urllib.parse.quote(json.dumps(state))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1000,870", "--virtual-time-budget=400", f"--screenshot={path}", url],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    keep = os.environ.get("DEMO_FRAMES_DIR")  # optional: reuse rendered frames between runs
    tmp = keep or tempfile.mkdtemp(prefix="demo-frames-")
    os.makedirs(tmp, exist_ok=True)
    try:
        cache, lines = {}, []
        for st, d in tl:
            key = json.dumps(st, sort_keys=True)
            if key not in cache:
                p = os.path.join(tmp, "f" + hashlib.md5(key.encode()).hexdigest()[:12] + ".png")
                if not os.path.exists(p): shot(st, p)
                cache[key] = p
            lines.append((cache[key], d))
        lst = os.path.join(tmp, "list.txt")  # ffmpeg concat: last duration is honoured only if the file is repeated
        with open(lst, "w") as f:
            for i, (p, d) in enumerate(lines):
                if i == len(lines) - 1: d /= 2  # the repeated last file below repeats this duration
                f.write(f"file '{p}'\nduration {d:.3f}\n")
            f.write(f"file '{lines[-1][0]}'\n")  # concat needs a repeated last file to honour the final hold
        pal = os.path.join(tmp, "pal.png")
        vf = "fps=10,scale=960:-1:flags=lanczos"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", vf + ",palettegen=max_colors=128:stats_mode=diff", pal], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", pal, "-lavfi", vf + "[x];[x][1:v]paletteuse=dither=none:diff_mode=rectangle", OUT], check=True)
        if shutil.which("gifsicle"):
            subprocess.run(["gifsicle", "-O3", "-b", OUT], check=True, stderr=subprocess.DEVNULL)
        print("wrote", os.path.normpath(OUT), os.path.getsize(OUT) // 1024, "KB,", sum(d for _, d in tl), "s")
    finally:
        if not keep: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
