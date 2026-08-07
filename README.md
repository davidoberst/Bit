# Bit (v2.0.1): The Audio-Visual Laboratory Copilot

<img src="Bit_logo.png" alt="Bit Logo" width="200">
Bit is an on-demand, multi-modal AI copilot designed to run in your environment. Built for the terminal with a minimalist interface, Bit acts as a pervasive assistant that can analyze your workstation state (screen captures and microphone input) in real-time using Gemini 2.5 Flash, or operate in a lightweight, screen-free command mode to execute real actions on your system through structured tool calling.

---

Bit operates strictly via **Text-to-Speech (TTS)**, powered by a fully local synthesis engine (Piper), and listens through a **stateful, RAM-persistent chat session** that ensures a deep understanding of continuity without restating the context.

---

## Modes of Assistance

Bit runs in one of two selectable modes, switched live from the terminal:

* **Bit Vision** — Combines computer vision and real-time voice recognition. Bit analyzes your screen alongside your spoken input to resolve questions about on-screen content and provide immediate contextual assistance, without needing to explain every detail manually.

* **Bit Command** — Designed for fast, lightweight interaction. Bit focuses exclusively on answering questions, casual conversation, and processing voice instructions to execute real system actions: creating and deleting files or folders, and managing tasks, without ever processing your screen.

---

## Tool Calling & System Actions

In Command mode, Bit doesn't just talk about actions, it executes them through Gemini's native function calling, backed by a sandboxed action layer (`sys_actions.py`):

* Every filesystem action (`create_folder`, `create_file`, `delete_file`, `delete_folder`) is resolved and validated against a fixed workspace root before touching disk, preventing any path traversal outside the permitted directory.
* Bit never fabricates a confirmation. If an action isn't backed by a real tool result, it says so instead of inventing success.
* Compound requests ("create a folder with a file inside") are handled through chained function calls in a single conversational turn.

---

## Tech Stack & Dependencies

The project is natively developed for **Linux** using Python 3 and leverages the following core components:

* **Core Engine:** `google-genai` (utilizing the `gemini-2.5-flash` model via persistent chat sessions, with native function calling for Command mode)
* **Speech-to-Text:** `faster-whisper` (local, CPU-optimized transcription)
* **Voice Engine:** Piper TTS (fully local, low-latency speech synthesis)
* **Audio Input/Output:** `sounddevice` & `numpy` (for real-time mic streaming and waveform capture)
* **Vision Capture:** `xfce4-screenshooter` / `spectacle` (auto-detected per desktop environment, Vision mode only)
* **System Actions:** sandboxed filesystem operations via `os` and `shutil`, exposed to Gemini as declared tools
* **Environment:** `python-dotenv` for API key management

---
