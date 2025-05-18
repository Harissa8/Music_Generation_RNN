# NN Music Generator 🎵
A narrow-AI RNN/LSTM system that composes brand-new music from scratch.

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%20|%203.10-orange?logo=python)](#)

NN (short for “Neural Notes” ) is a proof-of-concept generator that turns MIDI training data into fresh melodies, riffs and full-length pieces. It‘s deliberately **narrow AI**—it does one task well: generate music. No lyrics, no artwork—just tunes.


## Why NN?
* **Single-purpose, narrow AI.** Unlike “strong” or “general” AI, NN focuses only on music generation.  
* **Human-friendly.** The CLI lets composers seed a melody, set tempo/mood and get a playable MIDI in seconds.  
* **Open.** Built with TensorFlow/Keras; every layer, weight and training script lives in this repo.  
* **Extensible.** Swap in different datasets (classical, lofi, EDM) to steer the style.

---
![image](https://github.com/user-attachments/assets/caa6c2b7-a173-4ecc-8e06-9ddbad19a428)


## How It Works
| **Dataset** | Any folder of `.mid` files. A preprocessing script converts each track to sequences of note/velocity/duration tokens

| **Model** | 3-layer LSTM (embedding → 2 × LSTM → dense softmax). 

| **Training** | Optimizer = Adam

| **Generation** | Temperature-controlled softmax sampling

| **Output** | Generated token stream is converted back to a MIDI and optionally to .wav with FluidSynth.

