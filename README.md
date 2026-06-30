<<<<<<< HEAD
# 🧬 AI Bioinformatics Assistant

An intelligent AI-powered chatbot for bioinformatics education and sequence analysis. Built with FastAPI, Streamlit, and Openrouter API.

## 🎯 Features

- **AI Chatbot**: Ask questions about bioinformatics concepts, get expert explanations
- **Sequence Analysis**: Upload and analyze FASTA/FASTQ files
- **GC Content Calculation**: Understand nucleotide composition
- **ORF Detection**: Find open reading frames in sequences
- **Chat History**: Maintain conversation context
- **Multi-file Support**: Analyze multiple sequences at once
- **Educational Focus**: Designed as a learning assistant for students

## 🖥️ Tech Stack

- **Frontend**: Streamlit (modern chat-style UI)
- **Backend**: FastAPI (REST API)
- **AI Model**: Openrouter API
- **Processing**: Python with optional Biopython
- **Format Support**: FASTA, FASTQ, FA, FNA, FQ

## 📋 Project Structure

```
.
├── README.md
├── requirements.txt
├── .env.example
├── frontend/
│   └── app.py                 # Streamlit UI
├── backend/
│   └── main.py                # FastAPI server
├── utils/
│   ├── __init__.py
│   ├── parser.py              # FASTA/FASTQ parser
│   ├── analysis.py            # Sequence analysis
│   └── ai_utils.py            # Openrouter API integration
└── examples/
    └── sample_sequences.fasta # Example file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Openrouter API key (get one at https://openrouter.ai/)

### Installation

1. **Clone/Navigate to the project**
```bash
cd f:\Database\Bioinformatics\APIs
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy .env.example to .env
copy .env.example .env

# Edit .env and add your Openrouter API key
# OPENROUTER_API_KEY=your_api_key_here
```

### Running the Application

**Option 1: Run both services locally**

**Terminal 1 - Start FastAPI Backend:**
```bash
python backend/main.py
# or
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```

The frontend will open at `http://localhost:8501`

**Option 2: Using PowerShell with concurrent execution**

```powershell
# Start both services in parallel
& python backend/main.py & streamlit run frontend/app.py
```

## 💡 Usage Guide

### 1. **Analyzing Sequences**
   - Upload FASTA or FASTQ files using the sidebar uploader
   - Click "Analyze Sequences" button
   - View results: sequence count, length, GC content, nucleotide composition
   - Optionally detect ORFs

### 2. **Asking Questions**
   - Type any bioinformatics question in the chat input
   - Examples:
     - "What is GC content?"
     - "Explain genome assembly"
     - "Analyze the uploaded sequence"
     - "What is CRISPR?"

### 3. **Using Context**
   - Upload sequences first, then ask about them
   - The AI will use sequence data to provide relevant explanations
   - Example: "Analyze the uploaded sequence" or "What does this GC content indicate?"

## 🔌 API Endpoints

### POST `/chat`
Chat with the AI bioinformatics expert

**Request:**
```json
{
  "query": "What is GC content?",
  "chat_history": [],
  "sequence_context": null
}
```

**Response:**
```json
{
  "response": "GC content is...",
  "error": false,
  "model": "openrouter/auto"
}
```

### POST `/analyze`
Analyze biological sequences

**Request:**
```json
{
  "content": ">sequence1\nATGC...",
  "file_format": "fasta",
  "detect_orfs": false
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "total_sequences": 1,
    "total_length": 300,
    "average_length": 300,
    "average_gc_content": 45.5,
    "sequences": [...]
  },
  "orfs": null
}
```

### GET `/health`
Health check and configuration status

**Response:**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "endpoints": {
    "chat": "/chat",
    "analyze": "/analyze",
    "health": "/health"
  }
}
```

## 📊 Example Analysis Output

When you analyze sequences, you'll see:

```
📊 Sequence Analysis Results
───────────────────────────
📄 sample_sequences.fasta

Sequences: 4
Total Length: 3,245 bp
Avg Length: 811.25 bp
Avg GC%: 47.32%

📋 Detailed Sequence Info
- human_beta_globin: 146 bp, GC: 48.6%, AT: 51.4%
- mouse_beta_globin: 141 bp, GC: 47.5%, AT: 52.5%
- ecoli_dnaA: 1,290 bp, GC: 50.5%, AT: 49.5%
- salmonella_flagellin: 1,668 bp, GC: 45.2%, AT: 54.8%
```

## 🔧 Configuration

### Environment Variables

```bash
# Openrouter API key (required)
OPENROUTER_API_KEY=sk_xxxxxxxxxx

# Backend URL (optional, defaults to localhost:8000)
BACKEND_URL=http://localhost:8000
```

### File Formats Supported

| Format | Extensions | Description |
|--------|-----------|-------------|
| FASTA | .fasta, .fa, .fna | Sequence with headers starting with `>` |
| FASTQ | .fastq, .fq | Sequence with quality scores |
| Text | .txt | Plain text (auto-detect format) |

## 📚 Example Questions

### Concept Questions
- "What is GC content?"
- "Explain RNA-seq"
- "What is genome assembly?"
- "How does CRISPR work?"
- "What is BLAST?"

### Sequence Analysis
- "Analyze this sequence"
- "Why is this GC content high?"
- "What organism might have this composition?"
- "Explain these results"

### Learning
- "I'm learning bioinformatics, where should I start?"
- "What's the difference between DNA and RNA?"
- "Explain nucleotides"
- "What is a gene?"

## 🚨 Troubleshooting

### "Cannot connect to backend"
- Make sure FastAPI is running: `python backend/main.py`
- Check that port 8000 is not in use: `netstat -ano | findstr :8000`

### "API key not configured"
- Create `.env` file with `OPENROUTER_API_KEY=your_key`
- Restart the application
- Get an API key at https://openrouter.ai/

### "File format not recognized"
- Supported extensions: .fasta, .fa, .fna, .fastq, .fq, .txt
- Ensure file starts with `>` for FASTA or `@` for FASTQ

### "API request timed out"
- Check internet connection
- Verify Openrouter API key is valid
- Try again (might be a temporary issue)

## 📖 Sequence File Examples

### FASTA Format
```
>sequence_1 description here
ATGCGATCGATCGATCGATCG
ATGCGATCGATCGATCGATCG
>sequence_2 another description
GCTAGCTAGCTAGCTAGCTAG
```

### FASTQ Format
```
@sequence_1
ATGCGATCGATCGATCGATCG
+
IIIIIIIIIIIIIIIIIIII
@sequence_2
GCTAGCTAGCTAGCTAGCTAG
+
IIIIIIIIIIIIIIIIIIII
```

## 🧬 Bioinformatics Concepts

### GC Content
- **Formula**: (G + C) / Total Length × 100%
- **Significance**: 
  - Indicates organism type and genomic stability
  - High GC = thermostable, often in extreme environments
  - Low GC = found in AT-rich organisms

### Nucleotide Composition
- **A (Adenine)**: Purine, pairs with T
- **T (Thymine)**: Pyrimidine, pairs with A
- **G (Guanine)**: Purine, pairs with C
- **C (Cytosine)**: Pyrimidine, pairs with G

### ORF (Open Reading Frame)
- Sequence between start (ATG) and stop (TAA, TAG, TGA) codons
- Potential protein-coding region
- Multiple reading frames possible

## 🤝 Contributing

Found a bug or have a feature request? Please open an issue or submit a PR!

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the FAQ in the sidebar
- **API Docs**: Visit `http://localhost:8000/docs` when backend is running

## 📞 Contact

For more information about Openrouter API, visit: https://openrouter.ai/

---

**Version**: 1.0.0  
**Last Updated**: June 2026
=======
# Streamlit_-BioGenius
AI-Powered Bioinformatics Education &amp; Sequence Analysis Platform for assisting patients 
>>>>>>> 56d08dedb9139009293da91959b4654e33aa8c43
