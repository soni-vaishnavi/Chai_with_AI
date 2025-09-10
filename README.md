# ☕ ChaiWithAI Automation

ChaiWithAI is an automated system that fetches AI-generated content, processes it, and posts directly to your **Facebook Page** — all without manual work.  
Thanks to **GitHub Actions**, the script runs daily in the cloud, so you don’t need to keep your laptop on. 🚀  

---

## ✨ Features
- 🤖 Fetches daily content using **Gemini API**.  
- 🔍 Enhances and processes text/images using **Hugging Face API**.  
- 📢 Automatically posts generated content on **Facebook Page**.  
- ☁️ **Fully automated** with GitHub Actions (runs daily at a set time).  
- 🔑 Secure: All API keys are stored in **GitHub Secrets**, never exposed.  

---

## 📂 Project Structure
```bash
Chai_with_AI/
│── main.py              # Main automation script
│── main2.py             # Backup/testing script
│── learning.ipynb       # Notes/experiments (ignored by Git)
│── .env                 # Local API keys (not pushed to GitHub)
│── .gitignore           # Defines ignored files
│── images/              # Folder for generated images
│── prompts.txt          # Stores prompt templates
│── prompt_counter.txt   # Tracks prompt usage count
│── day_counter.txt      # Tracks daily run count
│── .github/workflows/   # Contains GitHub Actions workflow (main.yml)

✅ Example Run

At 11 AM IST every day, GitHub Actions starts the workflow.

It runs main.py.

The script generates AI content.

Posts it directly on your Facebook Page.