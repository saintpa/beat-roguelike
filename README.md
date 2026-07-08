# 🎵 Beat Roguelike

A live performance sampler built with **Python, PySide6 and Pygame**.

The project started as an experiment to learn desktop application architecture, audio programming and game development. It is gradually evolving into the music engine that will power my future roguelike rhythm game.

---

# Current Features

- 🎹 18 playable pads
- 🎧 Load individual samples
- 📦 Load complete kits using JSON
- ⌨️ Keyboard driven workflow
- 🔁 Natural loop mode
- 🎼 BPM synchronized loop mode
- ⏱ Adjustable BPM
- 🎵 Built-in metronome
- 🔴 Multi-slot loop recorder
- ▶ Loop playback
- ⏹ Loop stop events
- 💡 Visual pad progress indicator

---

# Controls

## Pads

### Melody

Q W E

A S D

Z X C

### Drums

I O P

K L ;

, . /

---

## Mouse

Left Click
Play pad

Right Click
Load sample

---

## Keyboard

Shift + Pad

Stop pad immediately

Option (Alt) + Pad

Natural looping

Option + Shift + Pad

BPM synchronized looping

]

Enter BPM input mode

-

Decrease BPM

=

Increase BPM

`

Choose loop slot

1-9

Play / Stop loop slot

Shift + 1-9

Emergency kill loop slot

---

# Kit Format

Example:

```json
{
    "Q": "sounds/kick.wav",
    "W": "sounds/snare.wav",
    "E": "sounds/hihat.wav"
}
```

---

# Installation

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/beat-roguelike.git
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

macOS/Linux

```bash
source .venv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

# Project Structure

```
audio/
    audio_engine.py

systems/
    bpm_manager.py
    kit_manager.py
    loop_manager.py

ui/
    pad_button.py
    sampler_window.py

sounds/

main.py
```

---

# Roadmap

## Loop Station

- Multiple loop slots
- Quantized launch
- Scene switching

## Sampler

- Waveform display
- Sample trimming
- Slice mode
- Choke groups
- FX rack

## Live Performance

- MPC inspired workflow
- DJ style performance tools
- MIDI support

## Game Integration

The sampler is not the final product.

It is being developed as the core music engine for a future roguelike rhythm game where players will collect new samples, instruments and effects during each run.

---

# Technologies

- Python
- PySide6
- pygame
- JSON

---

# Why this project?

Instead of cloning an existing drum pad application, I wanted to build an audio engine that could eventually become part of a game.

The project has become an opportunity to learn software architecture, event-driven programming, desktop UI development and audio systems while gradually implementing ideas inspired by devices such as the Akai MPC and live performance samplers.
