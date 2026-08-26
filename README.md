# 🎙️ AI Video Assistant

An end-to-end video processing pipeline powered by **LangChain**, **RAG (Retrieval-Augmented Generation)**, **Sarvam AI**, and **Whisper**. The system transcribes audio/video media (supporting English, multilingual, and Hinglish audio), produces structured summaries, extracts unresolved action items, and features an interactive Q&A assistant grounded in the meeting transcript via a **Streamlit** dashboard[cite: 1, 2].

---

## 🚀 Features[cite: 1]

* **Multi-Engine Transcription Pipeline**:
  * **Sarvam AI**: High-accuracy transcription tailored for Hinglish and Indian language contexts[cite: 1].
  * **Whisper**: Robust transcription for general English and global multilingual speech[cite: 1].
  * **Audio Chunking**: Automatically processes long-duration recordings in sequential audio chunks[cite: 1].
* **Automated Meeting Intelligence**:
  * **Map-Reduce Summarization**: Synthesizes lengthy transcripts into concise, structured executive summaries[cite: 1].
  * **Action Items & Decision Extraction**: Automatically extracts action items, key decisions, and open follow-up questions[cite: 1, 2].
* **Interactive Transcript RAG Engine**:
  * Dense vector retrieval with **Hugging Face BGE Embeddings** (`BAAI/bge-small-en-v1.5`)[cite: 1].
  * Multi-hardware execution support across CPU, NVIDIA GPU (`cuda`), and Intel Arc (`xpu`).
  * Strict context-grounded Q&A prompt design to eliminate hallucinations[cite: 1, 2].
* **Streamlit Web UI & Pre-Loaded Demo**:
  * Clean UI with categorized tabs for Summary, Details, Transcript, and Chat[cite: 1, 2].
  * Includes a **Pre-Loaded Sample Demo Mode** to preview UI and RAG features without requiring API keys[cite: 2].
  * Sidebar **Bring Your Own Key (BYOK)** support for Mistral and Sarvam AI APIs[cite: 2].

---

## 🛠️ Tech Stack & Architecture[cite: 1]

* **Language & Runtime**: Python 3.10+, PyTorch[cite: 1]
* **LLM Orchestration**: LangChain, LCEL (LangChain Expression Language)[cite: 1]
* **Models**: Mistral AI (LLM), Sarvam AI STT, Whisper STT[cite: 1]
* **Vector Store & Embeddings**: Hugging Face BGE Embeddings, ChromaDB[cite: 1]
* **Frontend**: Streamlit[cite: 1]
