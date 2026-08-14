#  VidInsight AI

> **Turn long-form videos and audio into searchable, structured knowledge.**

VidInsight AI is a full-stack AI platform that transforms **YouTube videos and local audio/video files** into transcripts, structured summaries, key decisions, action items, open questions, and a **transcript-grounded RAG chatbot**.

It combines audio preprocessing, multilingual speech-to-text, LLM-powered summarization, information extraction, semantic search, vector databases, and LLM reranking into a single end-to-end pipeline.

<p align="center">

** Video / Audio →  Transcript →  Insights →  Semantic Retrieval →  Grounded Q&A**

</p>

---

##  Features

###  Multi-Source Input

* Process **YouTube URLs**
* Process **local audio/video files**
* Automatically detect the input source
* Extract and prepare audio for transcription

###  Audio Processing

* YouTube audio extraction using `yt-dlp`
* Audio/video conversion using FFmpeg through `pydub`
* WAV conversion
* Mono-channel conversion
* 16 kHz sample-rate standardization
* 25-second audio chunking
* Temporary chunk generation and cleanup

###  Multilingual Transcription

Supports two transcription paths:

| Language | Provider         | Model                    |
| -------- | ---------------- | ------------------------ |
| English  | Groq Whisper API | `whisper-large-v3-turbo` |
| Hinglish | Sarvam AI        | `saaras:v2.5`            |

The transcription layer automatically routes the audio to the selected provider.

###  AI-Powered Summarization

Uses **Mistral Small** with a Map-Reduce style pipeline to process long transcripts.

Generates:

* Main discussion points
* Key decisions / conclusions
* Action items / next steps
* Important notes
* Deadlines and timelines when mentioned

###  Information Extraction

The system separately extracts:

* **Action Items**
* **Key Decisions**
* **Open Questions**
* **Unresolved Concerns**
* **Risks / Blockers**
* **Follow-ups**

The extraction prompts explicitly instruct the LLM not to invent information that is not present in the transcript.

###  Automatic Title Generation

Generates a short professional title from the transcript.

Constraints include:

* Maximum 8 words
* Professional tone
* No quotation marks
* No additional explanation

###  Transcript-Grounded RAG Chat

Ask natural-language questions about the processed content.

The RAG pipeline performs:

1. Transcript chunking
2. Embedding generation
3. ChromaDB storage
4. Semantic retrieval
5. LLM-based reranking
6. Context construction
7. Grounded answer generation

If the required information is not available in the retrieved transcript context, the system is instructed to explicitly say that it could not find the information.

###  Runtime Metrics

The backend tracks runtime information including:

* Videos processed
* API calls
* Groq Whisper calls
* Sarvam calls
* Chat queries
* Errors
* Total audio duration
* Whisper latency
* Sarvam latency
* Overall analysis latency

---

#  System Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │                      │
                         │ • YouTube URL        │
                         │ • Local Media        │
                         │ • Language Selection │
                         │ • Summary            │
                         │ • Insights           │
                         │ • RAG Chat           │
                         └──────────┬───────────┘
                                    │
                               HTTP / REST
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Input Processing   │
                         │                      │
                         │ YouTube → yt-dlp     │
                         │ Local File → pydub   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Audio Processing  │
                         │                      │
                         │ WAV                  │
                         │ Mono                 │
                         │ 16 kHz               │
                         │ 25-sec chunks        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Transcription     │
                         │                      │
                         │ English → Groq       │
                         │ Hinglish → Sarvam    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Complete Transcript  │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             Title Generation   Summarization   Information
                Mistral          Map-Reduce      Extraction
                    │               │                │
                    │               │         ┌──────┼──────┐
                    │               │         │      │      │
                    │               │         ▼      ▼      ▼
                    │               │      Actions Decisions Questions
                    │               │
                    │               ▼
                    │          Structured
                    │           Summary
                    │
                    └───────────────┐
                                    │
                                    ▼
                           ┌──────────────────┐
                           │   RAG Pipeline   │
                           └────────┬─────────┘
                                    │
                                    ▼
                            Transcript Chunks
                                    │
                                    ▼
                         Hugging Face Embeddings
                           all-MiniLM-L6-v2
                                    │
                                    ▼
                               ChromaDB
                                    │
                                    ▼
                         Semantic Retrieval (Top 12)
                                    │
                                    ▼
                         Mistral LLM Reranking
                              (Top 6)
                                    │
                                    ▼
                            Relevant Context
                                    │
                                    ▼
                              Mistral Small
                                    │
                                    ▼
                           Grounded Answer
```

---

#  End-to-End Workflow

```text
YouTube URL / Local Audio-Video
              │
              ▼
       Input Detection
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
   YouTube        Local File
       │             │
     yt-dlp       pydub
       │             │
       └──────┬──────┘
              ▼
        WAV Conversion
              │
              ▼
       Mono + 16 kHz
              │
              ▼
       25-sec Chunking
              │
              ▼
        Transcription
         ┌────┴─────┐
         │          │
         ▼          ▼
      English    Hinglish
         │          │
         ▼          ▼
       Groq       Sarvam
      Whisper       AI
         │          │
         └────┬─────┘
              ▼
      Complete Transcript
              │
      ┌───────┼────────┐
      │       │        │
      ▼       ▼        ▼
    Title   Summary  Extraction
      │       │        │
      │       │   ┌────┼─────┐
      │       │   ▼    ▼     ▼
      │       │ Actions Decisions Questions
      │       │
      │       ▼
      │   Map-Reduce
      │   Summarization
      │
      └────────┬─────────┐
               │         │
               ▼         ▼
             Result      RAG
                         │
                         ▼
                    Text Chunks
                         │
                         ▼
                     Embeddings
                         │
                         ▼
                      ChromaDB
                         │
                         ▼
                  Similarity Search
                       Top 12
                         │
                         ▼
                   LLM Reranking
                       Top 6
                         │
                         ▼
                   Mistral Small
                         │
                         ▼
                  Grounded Answer
```

---

#  Core Components

## 1. Input Processing

VidInsight AI accepts either a YouTube URL or a local media path.

The backend determines the input type before processing:

```text
HTTP/HTTPS URL
      │
      ▼
   yt-dlp
      │
      ▼
Audio

Local file
      │
      ▼
    pydub
      │
      ▼
Audio
```

The YouTube extraction layer uses `yt-dlp` and configures FFmpeg post-processing to obtain WAV audio.

---

#  2. Audio Preprocessing

The extracted or uploaded media is converted into a standardized audio representation.

```text
Input Media
    │
    ▼
Audio Extraction / Conversion
    │
    ▼
WAV
    │
    ▼
Mono
    │
    ▼
16 kHz
    │
    ▼
25-second Chunks
```

Standardizing the audio format provides a consistent input for downstream transcription APIs.

---

#  3. Audio Chunking

The current pipeline creates approximately **25-second audio chunks**.

```text
Long Audio
│
├── Chunk 1 → 25 sec
├── Chunk 2 → 25 sec
├── Chunk 3 → 25 sec
├── Chunk 4 → 25 sec
└── ...
```

The 25-second size is particularly important for the Sarvam synchronous STT-Translate path because the implementation explicitly uses this limit to stay below its short-duration input constraint.

Chunking also makes long-form transcription easier to control and retry.

---

#  4. Multilingual Transcription

## English → Groq Whisper

English audio chunks are sent to the Groq Whisper API.

```text
Audio Chunk
     │
     ▼
Groq Whisper
     │
     ▼
English Transcript
```

Default model:

```text
whisper-large-v3-turbo
```

The model can be configured using:

```env
GROQ_WHISPER_MODEL=whisper-large-v3-turbo
```

---

## Hinglish → Sarvam AI

Hinglish audio is routed through Sarvam's STT-Translate API.

```text
Hinglish Audio
      │
      ▼
Sarvam STT-Translate
      │
      ▼
English Transcript
```

Default model:

```text
saaras:v2.5
```

Configured using:

```env
SARVAM_STT_MODEL=saaras:v2.5
```

The current implementation sends the audio through Sarvam's speech-to-text-translate endpoint and disables diarization for this flow.

---

#  5. Retry and Rate-Limit Handling

External APIs can temporarily reject requests because of rate limits.

The Sarvam transcription path explicitly handles:

```text
HTTP 429 Too Many Requests
```

The retry flow is:

```text
API Request
     │
     ▼
Response
     │
 ┌───┴────┐
 │        │
 ▼        ▼
Success   429
 │        │
 ▼        ▼
Continue Retry
          │
          ▼
      Backoff
          │
          ▼
     Request Again
```

The current Sarvam implementation allows up to **5 attempts** and increases the waiting time between retries.

---

#  6. Transcript Generation

Every audio chunk produces a partial transcript.

```text
Chunk 1 → Transcript 1
Chunk 2 → Transcript 2
Chunk 3 → Transcript 3
...
Chunk N → Transcript N
```

The partial transcripts are concatenated into a single transcript:

```text
Transcript 1
     +
Transcript 2
     +
Transcript 3
     +
    ...
     ↓
Complete Transcript
```

This complete transcript becomes the source for:

* Title generation
* Summarization
* Action-item extraction
* Decision extraction
* Question extraction
* RAG indexing

---

#  7. Map-Reduce Summarization

Long transcripts are not sent to the LLM in one large request.

Instead, VidInsight AI uses a Map-Reduce style workflow.

## Map Stage

The transcript is split using:

```python
RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200
)
```

Each chunk is independently summarized by Mistral Small.

```text
                 Complete Transcript
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Chunk 1     Chunk 2     Chunk 3
             │           │           │
             ▼           ▼           ▼
          Mistral      Mistral     Mistral
             │           │           │
             ▼           ▼           ▼
        Summary 1    Summary 2    Summary 3
```

## Reduce Stage

The partial summaries are combined and sent to Mistral again.

```text
Summary 1
Summary 2
Summary 3
   ...
    │
    ▼
Mistral Small
    │
    ▼
Final Structured Summary
```

The final output is organized into:

```text
## Summary

## Key Decisions / Conclusions

## Action Items / Next Steps

## Important Notes
```

The prompts instruct the model to avoid adding information that is not supported by the transcript.

---

#  8. Structured Information Extraction

The application runs dedicated extraction chains over the transcript.

### Action Items

Extracts tasks and, when available:

```text
Task
Owner
Deadline
```

If an owner or deadline is not present, the system reports it as not mentioned instead of inventing a value.

### Key Decisions

Extracts:

* Decisions made during the discussion
* Confirmed conclusions
* Confirmed business/product/pricing changes

### Open Questions

Identifies:

* Unanswered questions
* Unresolved concerns
* Risks requiring investigation
* Technical uncertainties
* Business or pricing uncertainties
* Follow-up topics

---

#  9. Automatic Title Generation

VidInsight AI generates a short title directly from the transcript.

The title-generation prompt enforces:

* Maximum 8 words
* Professional tone
* No quotation marks
* No additional explanation

Example:

```text
Transcript:
Discussion about AI deployment, infrastructure,
and project planning.

Generated Title:
AI Deployment and Project Planning
```

---

#  10. RAG-Based Question Answering

The RAG system allows users to ask questions about the processed transcript.

The pipeline is:

```text
User Question
     │
     ▼
Semantic Retrieval
     │
     ▼
12 Candidate Chunks
     │
     ▼
Mistral Reranking
     │
     ▼
Up to 6 Relevant Chunks
     │
     ▼
Context Construction
     │
     ▼
Mistral Small
     │
     ▼
Grounded Answer
```

---

#  11. RAG Text Chunking

The transcript is independently chunked for retrieval.

Current configuration:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

This is intentionally smaller than the summarization chunks because retrieval benefits from more focused pieces of context.

```text
Transcript
│
├── Chunk 1
├── Chunk 2
├── Chunk 3
├── Chunk 4
└── ...
```

The overlap helps preserve contextual continuity between adjacent chunks.

---

#  12. Embeddings

Each RAG chunk is converted into a vector representation using:

```text
all-MiniLM-L6-v2
```

The implementation uses Hugging Face / Sentence Transformers embeddings.

```text
Transcript Chunk
      │
      ▼
all-MiniLM-L6-v2
      │
      ▼
Embedding Vector
```

These vectors allow semantic comparison between the user's question and transcript content.

---

#  13. ChromaDB Vector Store

The generated embeddings are stored in ChromaDB.

```text
Transcript Chunk
      │
      ▼
Embedding
      │
      ▼
ChromaDB
```

The current vector store configuration uses:

```text
Collection: meeting_transcript
Directory: vector_db
Embedding: all-MiniLM-L6-v2
```

The vector store is rebuilt for the newly processed transcript.

---

#  14. Semantic Retrieval

When a user asks a question, the system first performs similarity-based retrieval.

The current configuration retrieves:

```text
Top K = 12
```

Example:

```text
Question:
"What was the project deadline?"

        │
        ▼

Question Embedding

        │
        ▼

ChromaDB Similarity Search

        │
        ▼

12 Candidate Transcript Chunks
```

Semantic retrieval allows the system to find conceptually relevant content even when the exact words used in the question do not appear in the transcript.

---

#  15. LLM-Based Reranking

The 12 retrieved chunks are passed to a Mistral-based reranking step.

```text
12 Retrieved Chunks
        │
        ▼
Mistral Small
        │
        ▼
Relevant Chunk Selection
        │
        ▼
Up to 6 Chunks
```

The reranker is instructed to return only the chunk numbers that are directly useful for answering the question.

This reduces irrelevant context before final answer generation.

---

#  16. Grounded Answer Generation

The final answer is generated only from the selected transcript context.

Example:

```text
Question:
What was the project deadline?

Retrieved Context:
"The team agreed to complete the project by Friday."

Answer:
The project deadline was Friday.
```

The RAG system explicitly instructs the LLM:

```text
Answer based ONLY on the transcript context.
```

If the information cannot be found:

```text
I could not find this information in the transcript.
```

This helps reduce unsupported answers and keeps responses grounded in the processed content.

---

#  17. Runtime Metrics

The backend contains an in-memory metrics collector.

Tracked counters include:

```text
videos_processed
api_calls
whisper_calls
sarvam_calls
chat_queries
errors
total_audio_seconds
```

Timing metrics include:

```text
whisper_latency
sarvam_latency
analyze_latency
```

Metrics are exposed through:

```http
GET /api/metrics
```

Example:

```json
{
  "counters": {
    "videos_processed": 1,
    "api_calls": 1,
    "whisper_calls": 37,
    "sarvam_calls": 0,
    "chat_queries": 2,
    "errors": 0,
    "total_audio_seconds": 925
  },
  "avg_timings": {
    "whisper_latency": 2.98,
    "analyze_latency": 172.95
  },
  "live": {
    "videos_processed": 1,
    "api_calls": 1,
    "chat_queries": 2,
    "errors": 0,
    "total_audio_seconds": 925
  }
}
```

> **Note:** Metrics are currently stored in memory and reset when the backend process restarts.

---

#  Development Testing

During development, the pipeline was tested with long-form audio/video content.

### Example Test

```text
Video Duration: 15 min 25 sec
Audio Duration: 925 sec
Whisper Calls: 37
```

This is consistent with the approximate 25-second chunking strategy:

```text
925 / 25 ≈ 37 chunks
```

Another test case:

```text
Video Duration: ~27 minutes
Audio Duration: ~1650 sec
Whisper Calls: 66
```

Actual processing time and API calls can vary depending on:

* Audio duration
* Chunking configuration
* API response time
* Network conditions
* API rate limits
* Retry attempts

---

#  Tech Stack

## Frontend

* React 19
* Vite
* Tailwind CSS
* Axios
* Framer Motion
* Lucide React
* React Router

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Python-dotenv

## LLM / AI

* Mistral AI
* LangChain
* Groq Whisper API
* Sarvam AI

## RAG

* LangChain Text Splitters
* Sentence Transformers
* Hugging Face Embeddings
* `all-MiniLM-L6-v2`
* ChromaDB
* Semantic Retrieval
* LLM-based Reranking

## Audio / Media

* FFmpeg
* pydub
* yt-dlp

---

#  Project Structure

```text
VidInsightAI/
│
├── Frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   ├── audio_processor.py
│   └── metrics.py
│
├── api_server.py
├── main.py
├── requirements.txt
├── apt.txt
├── test.py
├── .python-version
└── .gitignore
```

---

# ⚙️ Installation

## Prerequisites

Make sure you have:

* Python 3.9+
* Node.js
* npm
* FFmpeg
* Git

You will also need API credentials for:

* Groq
* Mistral AI
* Sarvam AI

---

#  Backend Setup

Clone the repository:

```bash
git clone https://github.com/mayurramani07/VidInsightAI.git
cd VidInsightAI
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_WHISPER_MODEL=whisper-large-v3-turbo

MISTRAL_API_KEY=your_mistral_api_key

SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=saaras:v2.5
```

The current Sarvam endpoint is configured in the backend as:

```text
https://api.sarvam.ai/speech-to-text-translate
```

> Never commit `.env` files or API keys to GitHub.

---

# ▶ Run the Backend

Start the FastAPI server:

```bash
uvicorn api_server:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

---

#  Frontend Setup

Open another terminal:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The Vite development server will provide the frontend URL in the terminal.

For a production build:

```bash
npm run build
```

---

#  API Reference

## Health Check

```http
GET /
```

Returns:

```json
{
  "message": "VidInsight AI backend is running"
}
```

---

## Analyze Video / Audio

```http
POST /api/analyze
```

Request:

```json
{
  "source": "https://youtube.com/watch?v=VIDEO_ID",
  "language": "english"
}
```

Supported language values:

```text
english
hinglish
```

The endpoint executes:

```text
Input
 ↓
Audio Processing
 ↓
Transcription
 ↓
Transcript Generation
 ↓
Title Generation
 ↓
Summarization
 ↓
Action Item Extraction
 ↓
Decision Extraction
 ↓
Question Extraction
 ↓
RAG Index Construction
 ↓
Response
```

Response contains:

```json
{
  "title": "...",
  "transcript": "...",
  "summary": "...",
  "action_items": "...",
  "key_decisions": "...",
  "open_questions": "...",
  "processing_time": 0.0
}
```

---

## Chat With Transcript

```http
POST /api/chat
```

Request:

```json
{
  "question": "What were the main action items discussed?"
}
```

Response:

```json
{
  "answer": "..."
}
```

The transcript must be analyzed first. Otherwise the API returns an error indicating that a video needs to be analyzed before asking questions.

---

## Runtime Metrics

```http
GET /api/metrics
```

Returns counters, average timings, and live runtime statistics.

---

#  Security

API credentials are loaded through environment variables.

Never expose API keys in:

* Frontend source code
* GitHub repositories
* Public configuration files
* Screenshots
* README examples
* Client-side JavaScript

Use environment variables and placeholders instead.

---

#  Current Limitations

* Processing depends on external transcription and LLM APIs.
* API rate limits can increase processing time.
* Long videos require multiple transcription requests.
* Sarvam transcription is processed in short audio segments.
* Metrics are stored in memory and reset when the backend restarts.
* The current RAG state is stored in memory for the actively processed transcript.
* The vector store is rebuilt when a new transcript is processed.
* The current RAG implementation does not provide timestamp-level citations.
* The system is currently designed as a development/prototype application rather than a distributed production platform.
* Network availability and third-party API availability can affect processing.

---

#  Future Improvements

Potential improvements include:

* [ ] Parallel transcription
* [ ] Background job processing
* [ ] Redis-based caching
* [ ] Persistent multi-user sessions
* [ ] Timestamp-aware retrieval
* [ ] Timestamp-based citations
* [ ] Speaker diarization
* [ ] Speaker-aware summaries
* [ ] Retrieval evaluation
* [ ] Answer groundedness evaluation
* [ ] Citation accuracy evaluation
* [ ] PDF / DOCX export
* [ ] Real-time transcription
* [ ] User authentication
* [ ] Multi-user support
* [ ] Production observability
* [ ] Docker-based deployment
* [ ] Cloud-native deployment

---

#  Engineering Concepts Demonstrated

VidInsight AI demonstrates practical implementation of:

* Full-stack AI application development
* REST API design with FastAPI
* React frontend development
* Audio preprocessing
* YouTube audio extraction
* Speech-to-text integration
* Multilingual transcription
* API rate-limit handling
* Retry mechanisms
* LLM integration
* Prompt engineering
* Map-Reduce summarization
* Structured information extraction
* Text chunking
* Dense embeddings
* Vector databases
* Semantic retrieval
* Retrieval-Augmented Generation
* LLM-based reranking
* Grounded answer generation
* Runtime metrics
* Frontend / backend integration

---

#  Why VidInsight AI?

Long-form videos, podcasts, lectures, interviews, and meetings contain valuable information, but manually watching or searching through hours of content is inefficient.

VidInsight AI transforms that unstructured content into searchable knowledge:

```text
                Video / Audio
                     │
                     ▼
                 Transcript
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Summary    Decisions   Actions
          │          │          │
          └──────────┼──────────┘
                     ▼
               Open Questions
                     │
                     ▼
              Semantic Knowledge
                     │
                     ▼
                RAG Retrieval
                     │
                     ▼
              Grounded Q&A
```

Instead of watching an entire video to find one piece of information, users can simply ask a question and retrieve the relevant information from the transcript.

---

#  Example Use Cases

VidInsight AI can be used for:

### 🎙️ Meetings

Extract:

* Decisions
* Action items
* Owners
* Deadlines
* Open questions

###  Lectures

Generate:

* Summaries
* Important concepts
* Searchable transcripts
* Question answering

###  Podcasts

Extract:

* Main topics
* Important statements
* Key takeaways
* Searchable knowledge

###  Interviews

Identify:

* Topics discussed
* Important answers
* Technical concepts
* Follow-up questions

###  YouTube Videos

Convert long-form videos into:

```text
Transcript
   ↓
Summary
   ↓
Insights
   ↓
Searchable Knowledge
   ↓
Interactive Q&A
```

---

#  Author

## Mayur Ramani

**AI / ML Engineer | Generative AI | Full-Stack AI**

GitHub:
https://github.com/mayurramani07

Project:
https://github.com/mayurramani07/VidInsightAI

---

#  Support

If you find **VidInsight AI** useful, consider giving the repository a ⭐ on GitHub.

Contributions, feedback, and suggestions are welcome.
