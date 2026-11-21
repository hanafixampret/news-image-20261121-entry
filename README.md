# news-image-20261121-entry

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/hanafixampret/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/hanafixampret/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that sums up 21 November 2026's world news in one image.

`draw_news.py` draws a 1024×1024 newspaper front page — the world court's
genocide ruling on Myanmar, Russia's missile barrage on Ukraine, Anthropic's
9% fall a day after its record IPO, and 26 more stories, with the day's big
numbers and a date line that names Saturday 21 November 2026 — as
`entry.png` with PIL, no network. `main.ts` copies it to the output
directory.

## Run it

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=hnbaye7d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
