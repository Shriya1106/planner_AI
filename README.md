# 🎉 Festiva Planner AI

AI-powered event planning assistant with beautiful web interface.

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Generate Data
```powershell
python scripts/generate_data.py
```

### 3. Run Server
```powershell
python run.py
```

### 4. Open Browser
Visit: **http://localhost:8000**

---

## 🎯 Features

- 🤖 **AI Event Planner** - Generate complete event plans
- 💰 **Budget Optimizer** - ML-powered cost allocation
- 📚 **Knowledge Base** - Ask event planning questions
- 🏢 **Vendor Suggestions** - Smart recommendations
- 📅 **Timeline Generation** - Automated scheduling
- 🎨 **Beautiful UI** - Modern web interface

**Supported Events:** Weddings • Corporate • Birthdays • Conferences • Parties

---

## � Project Structure

```
festiva-planner-ai/
├── src/              # Source code
│   ├── agents/       # AI agents
│   ├── api/          # FastAPI app
│   ├── ml/           # ML models
│   ├── rag/          # Knowledge base
│   └── utils/        # Utilities
├── static/           # Web UI
├── scripts/          # Utility scripts
├── data/             # Generated data
├── run.py            # Start server
└── requirements.txt  # Dependencies
```

---

## 🎨 Using the Web Interface

1. **Plan Event** - Fill form and generate plan
2. **View Results** - Budget, timeline, vendors
3. **Ask Questions** - Query knowledge base
4. **Download Plan** - Save as JSON

---

## �️ Commands

| Command | Purpose |
|---------|---------|
| `python run.py` | Start server |
| `python scripts/generate_data.py` | Generate dataset |
| `python scripts/train_model.py` | Train ML model |
| `restart.bat` | Quick restart |

---

## 📊 API Endpoints

- `GET /` - Web UI
- `GET /docs` - API documentation
- `POST /api/v1/plan` - Create event plan
- `POST /api/v1/knowledge/query` - Query knowledge

---

## 🔧 Configuration

Copy `.env.example` to `.env` and configure (optional):
```env
API_PORT=8000
DEBUG=True
```

---

## � Support

- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

**Made with ❤️ for event planners**
