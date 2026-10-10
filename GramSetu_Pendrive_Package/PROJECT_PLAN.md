# GramSetu AI (ग्रामसेतु AI) - Offline Rural AI Assistant
## 5-Day Fast-Track Build Plan & Project Specification

---

### Executive Summary
**GramSetu AI** is a fully offline, voice-first, multimodal generative AI mobile application tailored for rural communities and village populations with zero or intermittent internet connectivity. Powered by a fine-tuned/quantized **Qwen 2.5 (1.5B / 0.5B)** model running locally via an embedded inference engine (`llama.cpp` / MLC-LLM), it provides instant, trustworthy advice in local languages (Hindi, Hinglish, regional dialects) covering **Agriculture (Kisan Mitra)**, **Government Welfare Schemes (Sarkari Yojana)**, **Basic Healthcare & First Aid (Swasthya Salah)**, and **Daily Rural Empowerment**.

---

### Key Project Pillars & Naming Suggestions

| Project Name | Tagline | Target Persona |
| :--- | :--- | :--- |
| **GramSetu AI (ग्रामसेतु AI)** *(Recommended)* | *Bridging Villages with Offline Intelligence* | All-in-one rural assistant (Agri, Health, Schemes, Education) |
| **GaonSathi AI (गाँवसाथी AI)** | *Aapka Apna Offline Digital Salahkar* | Farmers, rural women, self-help groups (SHGs) |
| **KisanVani Qwen (किसानवाणी)** | *Voice-First Agricultural Advisory* | Farmers, crop management, mandi & weather guidance |
| **LokSeva Offline (लोकसेवा AI)** | *Decentralized Citizen Services & Scheme Navigator* | Panchayat leaders, village youth, scheme applicants |

---

### System Architecture & Technical Stack

```
+-------------------------------------------------------------------------------+
|                             FLUTTER MOBILE & WEB CLIENT                       |
|  +---------------------------+  +------------------------------------------+  |
|  |  Voice UI / Mic Input     |  |  Reasoning Dashboard & Chat Interface    |  |
|  |  (Bilingual Hi / En)      |  |  (🧠 Deep Think • 🎨 Image Studio • RAG) |  |
|  +-------------+-------------+  +--------------------+---------------------+  |
+----------------|-------------------------------------|------------------------+
                 | (Audio stream)                      | (Text query)
                 v                                     v
+--------------------------------+   +------------------------------------------+
|      OFFLINE SPEECH ENGINE     |   |     🧠 ADVANCED AI REASONING & ROUTER    |
| • Sherpa-ONNX / Whisper-tiny   |   | • 1. Context & Multi-Turn Understanding  |
| • On-device ASR (Hindi/Indian) |-->| • 2. Chain-of-Thought (CoT) Breakdown   |
+--------------------------------+   | • 3. Instruction Following & Adaptive Tone|
                                     +--------------------+---------------------+
                                                          |
                               +--------------------------+--------------------------+
                               |                                                     |
                               v                                                     v
+----------------------------------------------+   +---------------------------------------------+
|    💾 DYNAMIC MEMORY & CONVERSATIONAL LAYER  |   |        🛠️ AGENTIC TOOLS ECOSYSTEM           |
| • In-Context Working Memory (Sliding Buffer) |   | • AgriMath Resolver (Acre ⇄ Bigha / Gaj)    |
| • Semantic Long-Term Fact Store (LocalStorage|   | • Scientific Fertilizer & DAP/Urea Bags Calc|
| • User Profile & Preferences (Land/Crops/Loc)|   | • Verified Offline RAG Knowledge Base       |
| • Zero-Latency Dynamic Prompt Injection      |   | • 🎨 AI Visual Image Studio (Pollinations)  |
+----------------------------------------------+   +---------------------------------------------+
                               |                                                     |
                               +--------------------------+--------------------------+
                                                          |
                                                          | (Augmented Reasoning Prompt + Memory)
                                                          v
                                     +------------------------------------------+
                                     |         ON-DEVICE LLM INFERENCE          |
                                     | • Qwen 2.5 (1.5B-Instruct GGUF Q4_K_M)   |
                                     | • Embedded llama.cpp / Ollama Engine     |
                                     | • RAM Footprint: ~1.1 GB | ~15 tokens/s  |
                                     +--------------------+---------------------+
                                                          |
                                                          | (Streamed Output + <think> CoT)
                                                          v
                                     +------------------------------------------+
                                     |         OFFLINE AUDIO & DISPLAY          |
                                     | • Collapsible Thinking Accordion (<think>)|
                                     | • Android Native TTS (hi-IN / en-IN)     |
                                     | • Interactive Tool Pills & Image Cards   |
                                     +------------------------------------------+
```

---

### 4-Member Team Composition & Role Distribution

| Role | Title | Core Focus & Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | **Mobile Lead & UI/UX Architect** | Flutter UI/UX, Voice Audio Record/Play pipelines, Chat UX, state management (Riverpod/Bloc), category flows. |
| **Member 2** | **AI/ML & On-Device Engine Engineer** | Qwen 2.5 quantization (GGUF Q4_K_M), C++/NDK `llama.cpp` integration, STT/TTS offline bindings, memory & inference benchmarking. |
| **Member 3** | **Data & Knowledge Engineer (RAG)** | Rural dataset curation (PM-Kisan, Ayushman, Crop advisory), SQLite FTS5 database setup, Hindi/Hinglish prompt engineering, guardrails. |
| **Member 4** | **QA, Systems Integration & Release Lead** | Hardware testing across budget phones (4GB/6GB RAM), thermal/battery profiling, APK bundling, offline demo scenarios, pitch & documentation. |

---

### 5-Day Daily Sprint Breakdown

#### **Day 1: System Blueprint, Quantization & Architecture Setup**
- **Member 1 (Mobile)**: Initialize Flutter project; configure design tokens (Rural warm palette: Green `#1B5E20`, Saffron `#E65100`, Clean Off-White); build main navigation shell and mock chat interface.
- **Member 2 (AI Engine)**: Download Qwen2.5-1.5B-Instruct & 0.5B-Instruct; run quantization scripts to produce GGUF (Q4_K_M, Q5_K_M); test llama.cpp CLI execution on Mac/Linux.
- **Member 3 (Data/RAG)**: Gather and clean rural knowledge assets: 30 Top Govt Schemes (eligibility, documents required, benefits) and 50 Agricultural crop/pest FAQs in structured JSON.
- **Member 4 (QA/Setup)**: Set up Antigravity task boards, Git repository, CI/CD for APK building, and baseline benchmark suite on test Android devices (4GB/6GB RAM).

#### **Day 2: Embedded LLM Integration & Offline Speech Pipeline**
- **Member 1 (Mobile)**: Implement Audio Recorder widget with wave animations and Android Native TTS integration for Hindi voice synthesis.
- **Member 2 (AI Engine)**: Cross-compile `llama.cpp` for Android (arm64-v8a via NDK) and create Dart FFI bindings or integrate `flutter_llama_cpp`; execute test inference inside Android emulator/device.
- **Member 3 (Data/RAG)**: Setup SQLite database with FTS5 table structure; index JSON dataset; write retrieval query logic (BM25 keyword search + metadata filtering).
- **Member 4 (QA/Setup)**: Profile memory usage and inference latency of Qwen 2.5 on target Android devices; document cold-start times and RAM consumption.

#### **Day 3: Context-Aware Offline RAG & Prompt Engineering**
- **Member 1 (Mobile)**: Connect Flutter chat state to the local inference bridge; implement streaming response token rendering.
- **Member 2 (AI Engine)**: Integrate Whisper-tiny / Sherpa-ONNX offline Speech-to-Text engine; enable voice-in to text-stream pipeline.
- **Member 3 (Data/RAG)**: Develop bilingual system prompts (Hindi/Hinglish/English) with strict rural guardrails (safety, simplicity, conversational tone); connect SQLite retrieval to prompt injection.
- **Member 4 (QA/Setup)**: Conduct test queries across 4 core domains (Agriculture, Health, Schemes, Education); log hallucination rates and adjust retrieval thresholds.

#### **Day 4: Domain Modules, Voice-First UX & Performance Tuning**
- **Member 1 (Mobile)**: Build dedicated domain portal cards: *Kisan Mitra* (Crop Doctor), *Yojana Sahayak* (Scheme Finder), *Swasthya Prathmik* (First Aid triage), *Shiksha Sathi* (Literacy/Math).
- **Member 2 (AI Engine)**: Optimize inference thread pool (4 CPU threads on ARM big.LITTLE), implement KV-cache reuse, and tune token generation limits for speed.
- **Member 3 (Data/RAG)**: Add offline bookmarking, scheme application checklist generator, and audio query pre-sets in Hindi.
- **Member 4 (QA/Setup)**: Perform thermal, battery, and memory leak stress testing (continuous 20-minute chat sessions); resolve crashes on 4GB RAM devices.

#### **Day 5: Polishing, Offline Field Validation, APK Packaging & Pitch**
- **Member 1 (Mobile)**: Final UI polish, haptic feedback, offline indicator badge, multilingual toggle button, and user onboarding walkthrough.
- **Member 2 (AI Engine)**: Package quantized model file (`qwen2.5-1.5b-instruct-q4_k_m.gguf` ~980MB or `0.5b` ~350MB) into APK asset bundle / single-click in-app unpacker.
- **Member 3 (Data/RAG)**: Verify knowledge accuracy across 100 sample rural queries; create a comprehensive demo script covering real village scenarios.
- **Member 4 (QA/Setup)**: Generate signed standalone release APK (`GramSetu_AI_v1.0.apk`); compile presentation pitch deck, executive flyer, and printable technical documentation.

---

### Hardware Requirements & Performance Targets

| Metric | Target Specification (Budget Android Device) |
| :--- | :--- |
| **Minimum Android OS** | Android 9.0 (Pie) / API Level 28+ (arm64-v8a) |
| **Minimum RAM** | 4 GB (Recommended: 6 GB or higher) |
| **Model Size (Storage)** | ~980 MB (Qwen 2.5 1.5B Q4_K_M) or ~380 MB (0.5B Q4_K_M) |
| **Inference Speed** | 12 - 18 tokens/sec on Snapdragon 680 / Helio G99 |
| **STT Voice Latency** | < 1.2 seconds for 5-second voice snippet (Sherpa-ONNX/Whisper) |
| **Battery Impact** | < 5% battery consumption per 30 minutes of continuous voice chat |
| **Internet Dependency** | **0.0% (100% Fully Air-Gapped & Offline)** |
