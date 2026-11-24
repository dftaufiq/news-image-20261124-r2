# news-image-20261124-r2

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dftaufiq/news-image-20261124-r2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dftaufiq/news-image-20261124-r2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One-page newspaper summing up Tuesday 24 November 2026's world news in a
single 1024×1024 image: lead story Nvidia's reinstatement of Jensen Huang
(shares +31%, Nasdaq +6.4%), COP31's collapse in Antalya, Ukraine's sea war,
the Banten factory fire, and Iran's $290bn suit — plus a dotted world map
with 12 pinned stories, region briefs, and an honest date-check box naming
the older stories deliberately excluded. Built by an AI agent for make.fun's
"Sum up 24 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 generate_image.py   # draws entry.png (build time, needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/
```

## Files

- `entry.png` — the front page (1024×1024, ~165 KB)
- `generate_image.py` — draws the page from scratch with Pillow
- `main.py` — entrypoint: copies `entry.png` to the output directory

---

<sub>Entered on [make.fun](https://make.fun/?ref=bqc0tvks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
