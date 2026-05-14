# 🚀 How to Run Festiva Planner AI

## Simple 4-Step Guide

### Step 1: Install
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Generate Data
```powershell
python scripts/generate_data.py
```

### Step 3: Start Server
```powershell
python run.py
```

### Step 4: Open Browser
```
http://localhost:8000
```

---

## 🎯 That's It!

You'll see a beautiful web interface where you can:
- Plan events (weddings, corporate, birthdays)
- Get budget breakdowns
- See timelines and vendor suggestions
- Ask event planning questions

---

## 🔄 Restart Server

**Option 1:** Double-click `restart.bat`

**Option 2:** 
```powershell
# Stop with Ctrl+C, then:
python run.py
```

---

## 🛑 Stop Server

Press `Ctrl + C` in the terminal

---

## 📍 Important URLs

- **Main UI:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## ❓ Troubleshooting

**Port already in use?**
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Module not found?**
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

---

**That's all you need to know!** 🎉
