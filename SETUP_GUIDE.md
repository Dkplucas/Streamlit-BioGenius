# 🚀 Complete Setup Guide

## Step-by-Step Installation & Configuration

### Part 1: Prerequisites

#### 1.1 Python Installation

- **Windows**: Download from https://www.python.org/downloads/

  - ✅ Check "Add Python to PATH" during installation
  - Verify: Open Command Prompt and run `python --version`
- **Linux/Mac**:

  ```bash
  # Debian/Ubuntu
  sudo apt-get install python3 python3-pip python3-venv

  # macOS (using Homebrew)
  brew install python3
  ```

  - Verify: `python3 --version`

#### 1.2 Get Openrouter API Key

1. Visit https://openrouter.ai/
2. Click **"Sign Up"** and create an account
3. Go to **Dashboard** → **API Keys**
4. Click **"Create New Key"**
5. Copy the API key (looks like: `sk_xxxxxxxxxxxxxxxxxx`)
6. **⚠️ Keep this secret! Never share it!**

---

### Part 2: Project Setup

#### 2.1 Navigate to Project

```bash
# Windows
cd f:\Database\Bioinformatics\APIs

# Linux/Mac
cd /path/to/Database/Bioinformatics/APIs
```

#### 2.2 Create Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `fastapi` - Backend framework
- `uvicorn` - ASGI server
- `streamlit` - Frontend framework
- `requests` - HTTP client
- `python-dotenv` - Environment variable loader
- `biopython` - Bioinformatics (optional)
- `pydantic` - Data validation

---

### Part 3: Environment Configuration

#### 3.1 Create `.env` File

**Option A: Manual (Windows)**

1. Open Notepad
2. Paste the following:

```
OPENROUTER_API_KEY=sk_your_actual_api_key_here
BACKEND_URL=http://localhost:8000
```

3. Replace `sk_your_actual_api_key_here` with your actual key
4. Save as `.env` in the project root directory
5. **Important**: Make sure there's no `.txt` extension!

**Option B: Using Command Line (Windows)**

```batch
copy .env.example .env
# Then edit .env with your API key
```

**Option C: Linux/Mac**

```bash
cp .env.example .env
nano .env  # or vim, code, etc.
# Edit and add your API key
```

#### 3.2 Verify Configuration

```bash
# Windows
type .env

# Linux/Mac
cat .env
```

Should output:

```
OPENROUTER_API_KEY=sk_xxxxxxxxxxxxxxxx
BACKEND_URL=http://localhost:8000
```

---

### Part 4: Running the Application

#### Option 1: Using the Run Script (Easiest)

**Windows (PowerShell):**

```powershell
# First, enable script execution if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the script
.\run.ps1
```

**Linux/Mac:**

```bash
chmod +x run.sh
./run.sh
```

#### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Start Backend:**

```bash
python backend/main.py
# or
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2 - Start Frontend:**

```bash
streamlit run frontend/app.py
```

You should see:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

The app will automatically open in your browser.

---

### Part 5: Verification

#### 5.1 Check Backend Health

Open your browser and visit:

```
http://localhost:8000/health
```

Expected response:

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

#### 5.2 Check API Documentation

Visit: `http://localhost:8000/docs`

This shows interactive API documentation where you can test endpoints.

#### 5.3 Test Frontend

Frontend should be open at: `http://localhost:8501`

- You should see the title "🧬 AI Bioinformatics Assistant"
- Sidebar should show file uploader
- Main chat interface should be visible

---

### Part 6: First Test

#### 6.1 Test Chat (No File Required)

1. In the chat input, type: `What is GC content?`
2. Click enter or send
3. Wait for response (might take 5-10 seconds)
4. You should see an AI response

#### 6.2 Test Sequence Analysis

1. In the sidebar, upload `examples/sample_sequences.fasta`
2. Click "Analyze Sequences"
3. Wait for analysis to complete
4. You should see results showing:
   - Number of sequences
   - Total length
   - GC content
   - Detailed sequence information

#### 6.3 Test Context-Aware Chat

1. After analyzing sequences, ask: `Analyze the uploaded sequence`
2. The AI should reference the sequence data in its response

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Run `pip install -r requirements.txt` again

### "Port 8000 already in use"

**Windows:**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Linux/Mac:**

```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### "OPENROUTER_API_KEY not configured"

**Solution**:

1. Check `.env` file exists in project root
2. Verify API key is not empty
3. Restart backend (changes to .env require restart)

### "Cannot connect to backend" (Streamlit error)

**Solution**:

1. Make sure backend is running: `http://localhost:8000/health`
2. Check firewall isn't blocking port 8000
3. Try restarting both services

### "API Key Error" or "401 Unauthorized"

**Solution**:

1. Verify API key is correct (copy-paste from Openrouter)
2. Check it starts with `sk_`
3. Make sure it's not expired (check Openrouter dashboard)
4. Try creating a new key

### "Request timed out"

**Solution**:

1. Check internet connection
2. Check Openrouter API status
3. Try a simpler question
4. Wait a few seconds and retry

### Script won't run (Permission denied)

**Linux/Mac:**

```bash
chmod +x run.sh
./run.sh
```

**Windows (PowerShell):**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\run.ps1
```

---

## 📊 Folder Structure After Setup

```
APIs/
├── README.md                    # Main documentation
├── SETUP_GUIDE.md              # This file
├── requirements.txt            # Python dependencies
├── .env                        # ✅ Create this with your API key
├── .env.example               # Example template
├── run.ps1                    # Windows startup script
├── run.sh                     # Linux/Mac startup script
├── frontend/
│   └── app.py                # Streamlit UI
├── backend/
│   └── main.py               # FastAPI server
├── utils/
│   ├── __init__.py
│   ├── parser.py             # FASTA/FASTQ parsing
│   ├── analysis.py           # Sequence analysis
│   └── ai_utils.py           # Openrouter API
└── examples/
    └── sample_sequences.fasta # Test data
```

---

## 🎯 Quick Reference

### Starting Services

```bash
# Option 1: Automatic (Windows)
.\run.ps1

# Option 2: Automatic (Linux/Mac)
./run.sh

# Option 3: Manual Backend
python backend/main.py

# Option 4: Manual Frontend (different terminal)
streamlit run frontend/app.py
```

### Important URLs

| Service  | URL                          | Purpose              |
| -------- | ---------------------------- | -------------------- |
| Frontend | http://localhost:8501        | Web UI               |
| Backend  | http://localhost:8000        | API                  |
| API Docs | http://localhost:8000/docs   | Interactive API docs |
| Health   | http://localhost:8000/health | Status check         |

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=sk_your_key_here

# Optional
BACKEND_URL=http://localhost:8000  # Frontend connects to this
```

### Deactivate Virtual Environment

When done, deactivate the virtual environment:

```bash
# Windows
deactivate

# Linux/Mac
deactivate
```

---

## 🎓 Next Steps

1. ✅ Test with sample FASTA file
2. ✅ Try uploading your own sequence files
3. ✅ Experiment with different questions
4. ✅ Check API documentation at `/docs`
5. ✅ Explore modifying the system prompt in `ai_utils.py`

---

## 📞 Getting Help

1. **Backend not starting**: Check `python backend/main.py` output
2. **Frontend error**: Check `streamlit run frontend/app.py` output
3. **API error**: Visit `http://localhost:8000/health` to check status
4. **File upload error**: Ensure file format is FASTA or FASTQ
5. **Slow responses**: Check internet connection and API quota

---

## ✨ You're All Set!

You're ready to use the AI Bioinformatics Assistant!

- Upload sequences and ask questions
- Explore bioinformatics concepts
- Use it as a learning tool
- Customize prompts and behavior

Happy analyzing! 🧬
