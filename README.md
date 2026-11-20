# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/salikamarlisa3-cell/global-edition-news-image-20261120-v2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/salikamarlisa3-cell/global-edition-news-image-20261120-v2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

An entry for the [news-image-20261120](https://make.fun/bounty/news-image-20261120)
bounty on make.fun: the whole of Friday 20 November 2026's world news in a
single 1024×1024 broadsheet poster.

## What is on the poster

- **56 numbered stories across 7 regions** — 8 per region, every one
  published or reported on 20 Nov 2026, each with its outlet tag on the page.
- **3 lead stories** — the Trump–Xi–Putin "peace declaration" signed in
  Shenzhen, the World Court's Myanmar genocide ruling (9–6), and
  Anthropic's record $81.3bn IPO (+17% on debut).
- **Dot-matrix world map** with 7 numbered region pins and a region key.
- **16 illustrated scenes** drawn from the day's stories.
- **UTC timeline** of six timed events, a **by-the-numbers** strip, and a
  **weather strip** (20 Nov highs, forecast issued 19 Nov) with the day's
  weather watches.
- **"Left out & why"** date-check box — the date rule and what it excluded.

## Regenerate

```sh
MAKEFUN_OUTPUT_DIR=. python3 main.py   # writes entry.png (1024x1024)
```

`main.py` (Python 3 + Pillow) draws the whole poster from the story data
baked into it — no network, no clock, no randomness; two runs produce a
byte-identical `entry.png`.

## Sources

Every story is listed with outlet, date and verification URL in
[SOURCES.md](SOURCES.md).

## License

MIT — see `LICENSE`.
