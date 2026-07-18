# Bit: The Audio-Visual Laboratory Copilot 

Bit is an on-demand, multi-modal AI copilot designed to run in your environment. Built with a minimalist black-and-white graphical interface using Pygame, Bit acts as a pervasive assistant that analyzes your workstation state (screen captures and microphone input) in real-time using Gemini 2.5 Flash to deliver high-density, strategic engineering support.

---

Bit operates strictly via **Text-to-Speech (TTS)** 

**stateful, RAM-persistent chat session** that ensures a deep understanding of continuity without restating the context.


##  Tech Stack & Dependencies

The project is natively developed for **Linux** using Python 3 and leverages the following core components:

* **Core Engine:** `google-genai` (utilizing the `gemini-2.5-flash` model via persistent chat sessions)
* **Graphics & Physics:** `pygame` (for the audio-reactive visualizer and master loop)
* **Audio Input/Output:** `sounddevice` & `numpy` (for real-time mic streaming and waveform scaling)
* **Voice Engine:** Custom local TTS (`speaker_controller`)
* **Environment:** `python-dotenv` for API key management

---

##  Project Structure

```text
├── main.py                # Master control file, Pygame loop, and state management.
├── brain.py               # GenAI Client gateway, system instructions, and chat session.
├── audio_controller.py    # Microphone streaming, buffer handling, and WAV writer.
├── vision_controller.py   # Screen capture engine (X11 / Wayland compatibility wrapper).
├── speaker_controller.py  # local TTS execution subsystem.
└── delete_temp_files.py   # Cache cleaner for audio and visual binary leftovers.
