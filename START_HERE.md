# ✨ START HERE - Festiva Planner AI

## 🎯 What You Have

A complete AI-powered event planning system with a beautiful web interface!

---

## 🚀 Quick Start (3 Steps)

### 1. Install
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate Data
```powershell
python scripts/generate_data.py
```

### 3. Run
```powershell
python run.py
```

**Then open:** http://localhost:8000

---

## 📁 Essential Files

```
festiva-planner-ai/
├── run.py              ← Start server (MAIN FILE)
├── restart.bat         ← Quick restart
├── requirements.txt    ← Dependencies
├── .env.example        ← Config template
├── README.md           ← Project info
├── HOW_TO_RUN.md       ← Detailed guide
│
├── src/                ← Source code
│   ├── agents/         ← AI agents
│   ├── api/            ← FastAPI app
│   ├── ml/             ← ML models
│   ├── rag/            ← Knowledge base
│   └── utils/          ← Utilities
│
├── static/             ← Web UI (HTML/CSS/JS)
├── scripts/            ← Utility scripts
├── data/               ← Generated data
└── venv/               ← Virtual environment
```

---

## 🎨 What You Can Do

1. **Plan Events** - Weddings, corporate, birthdays
2. **Get Budgets** - ML-powered cost allocation
3. **See Timelines** - Automated task scheduling
4. **Find Vendors** - Smart recommendations
5. **Ask Questions** - AI knowledge assistant

---

## 📖 Documentation

- **START_HERE.md** ← You are here!
- **HOW_TO_RUN.md** - Detailed instructions
- **README.md** - Project overview

---

## 🔥 Most Important Commands

```powershell
# Start server
python run.py

# Generate data (first time only)
python scripts/generate_data.py

# Train ML model (optional)
python scripts/train_model.py

# Quick restart
restart.bat
```

---

## 🌐 URLs

- **Main UI:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## ❓ Need Help?

1. Read **HOW_TO_RUN.md** for detailed steps
2. Check **README.md** for features
3. Visit http://localhost:8000/docs for API info

---

**🎉 That's all you need! Run `python run.py` and enjoy! 🎉**
