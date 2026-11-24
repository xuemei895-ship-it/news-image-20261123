# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/xuemei895-ship-it/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/xuemei895-ship-it/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page that sums up the world news of Monday
23 November 2026 in a single 1024×1024 image: the COP31 climate talks
collapse in Antalya leads, with five more top stories (Ukraine's drone
strike on Russian warships off Libya, Nvidia reinstating Jensen Huang,
Belgium's national strike grounding flights, the IRGC's claim that three
tankers hit mines in the Strait of Hormuz, and the Democrats reaching
258 House seats) plus a ticker of the day's other news.

## Run it

```sh
python3 main.py
```

The program copies `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It uses only the Python standard library:
no network, no randomness, no clock — two runs write identical bytes.

To regenerate the image from the stories, run `python3 generate.py`
(requires Pillow and the DejaVu fonts; it writes `assets/entry.png`).
Story sources are listed in `SOURCES.md`.

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards
