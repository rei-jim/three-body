# Trisolaris

A gravitational n-body simulation of the Alpha Centauri triple-star system, inspired by Liu Cixin's *The Three-Body Problem*. Three suns in chaotic mutual orbit produce unpredictable Stable and Calamity Eras for the civilisation on the planet below.

![Windows 95 style simulation with CRT scanlines showing three orbiting stars and a planet trail](https://raw.githubusercontent.com/rei-jim/three-body/main/preview.png)

## Features

- Real-time n-body gravity integration (Euler, softened potential)
- Temperature-coded planet trail: orange = scorching · green = habitable · blue = frozen
- Era detection: Stable, Chaotic, Calamity (Scorching / Ice Age)
- Windows 95 + CRT aesthetic — scanlines, phosphor flicker, beveled buttons
- Adjustable simulation speed (1×–32×) and trail length
- Click any star to nudge it and trigger orbital chaos

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Hosted on [Streamlit Community Cloud](https://streamlit.io/cloud). Connect the repo, set `app.py` as the entry point, and deploy — no configuration needed.

## The physics

The three stars (α Cen A, α Cen B, Proxima Centauri) are initialised in a triangular configuration with approximate circular velocities. A lightweight planet orbits α Cen A with negligible mass. Each frame runs 20 sub-steps of the gravitational integrator at the chosen speed multiplier.

Era classification is based on the planet's distance to its nearest star:

| Distance | Condition |
|---|---|
| < 32 | Burning |
| 32 – 120 | Habitable |
| 120 – 200 | Cold |
| > 200 | Frozen |

A Stable Era is declared after the planet sustains habitable conditions long enough for civilisation to develop. Calamity Eras trigger when the planet spends extended time in burning or frozen territory.
