# Emotion Synth

Turn mood prompts into music using a local LLM and real-time audio synthesis.

## What it does

This tool lets you describe a musical mood in natural language (e.g., "happy", "sad ambient", "glitchy alien rave"), and it uses a local LLM (via [Ollama](https://ollama.com)) to generate a list of musical notes and rhythms that match the mood. These are then played in real time using the [pyo](https://ajaxsoundstudio.com/software/pyo/) synthesis engine.

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) installed
- Audio system dependencies (macOS example):

## Setup

### 1. Install system audio libraries (macOS)

Make sure the following dependencies are installed via Homebrew:

```bash
brew install portaudio portmidi libsndfile liblo lame mpg123 flac opus libvorbis
```

If you're on Apple Silicon (M1/M2/M3), you may also need:
```
brew install tcl-tk
```

### 2. Create a Python virtual environment
```
python3 -m venv env
source env/bin/activate
```

### 3. Install Python dependencies
```
pip install -r requirements.txt
```

### 4. Install and start Ollama
```
brew install ollama
```

Start the Ollama server:

```
ollama serve
```

Download a compatible model (e.g., Mistral):

```
ollama pull mistral
```

### 5. Run the app
In a separate terminal tab (while ollama serve is running):

```
python main.py
```
When prompted, enter a mood or emotional prompt, for example:
```
Enter a musical mood or emotion: melancholic space lullaby
```

You’ll hear a generated sequence of tones based on your prompt.
