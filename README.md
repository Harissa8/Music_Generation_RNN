# NN Music Generator 🎵
A narrow-AI RNN/LSTM system that composes brand-new music from scratch.

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%20|%203.10-orange?logo=python)](#)

NN (short for “Neural Notes” *and* the future first name of the project’s creator’s daughter) is a proof-of-concept generator that turns MIDI training data into fresh melodies, riffs and full-length pieces. It‘s deliberately **narrow AI**—it does one task well: generate music. No lyrics, no artwork—just tunes.

---

## Table of Contents
1. [Why NN?](#why-nn)
2. [How It Works](#how-it-works)
3. [Quick Start](#quick-start)
4. [Training From Scratch](#training-from-scratch)
5. [Testing & Evaluation](#testing--evaluation)
6. [Roadmap](#roadmap)
7. [Contributing](#contributing)
8. [License](#license)

---

## Why NN?
* **Single-purpose, narrow AI.** Unlike “strong” or “general” AI, NN focuses only on music generation.  
* **Human-friendly.** The CLI lets composers seed a melody, set tempo/mood and get a playable MIDI in seconds.  
* **Open.** Built with TensorFlow/Keras; every layer, weight and training script lives in this repo.  
* **Extensible.** Swap in different datasets (classical, lofi, EDM) to steer the style.

---

## How It Works

| Stage | Details |
|-------|---------|
| **Dataset** | Any folder of `.mid` files. A preprocessing script converts each track to sequences of note/velocity/duration tokens. |
| **Model** | 3-layer LSTM (embedding → 2 × LSTM → dense softmax). |
| **Training** | Optimizer = Adam; default LR = 1e-3; teacher forcing ratio = 0.9. |
| **Generation** | Temperature-controlled softmax sampling plus nucleus (top-p) filtering. |
| **Output** | Generated token stream is converted back to a MIDI and optionally to .wav with FluidSynth. |

---

## Quick Start
```bash
git clone https://github.com/<your-org>/<repo>.git
cd <repo>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate an 8-bar clip conditioned on a primer melody
python nn_generate.py \
    --primer midi/primer.mid \
    --length 32 \
    --temperature 0.95 \
    --out samples/out.mid
