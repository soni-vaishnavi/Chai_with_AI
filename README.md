☕ ChaiWithAI Automation

This project automatically fetches AI content, generates posts, and uploads them to Facebook using APIs. You don’t need to run it manually every day — it runs automatically in the cloud using GitHub Actions.

🚀 Features

Fetches daily content using Gemini API (AI text).

Uses Hugging Face API for AI-powered tasks.

Automatically posts content on Facebook Page.

Fully automated — no need to keep your laptop on.

Secure — API keys are stored in GitHub Secrets (not visible to anyone).

📂 Project Structure
chaiwithai/
│── main.py              # Main script (automation logic)
│── main2.py             # Backup/testing script
│── learning.ipynb       # Notes/experiments (ignored by git)
│── .env                 # Stores API keys (not uploaded to GitHub)
│── .gitignore           # Hides sensitive files from GitHub
│── images/              # Folder for generated images
│── prompts.txt          # Stores prompts used
│── prompt_counter.txt   # Tracks prompt usage
│── day_counter.txt      # Tracks day count

🔑 Secrets Setup

Since we don’t want to upload API keys publicly, we use GitHub Secrets.

Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret.

Add these one by one:

GEMINI_API_KEY

HF_ACCESS_TOKEN

FACEBOOK_ACCESS_TOKEN

FACEBOOK_PAGE_ID

⚙️ How It Works

Here’s the workflow:

flowchart TD
    A[Start GitHub Action ⏰] --> B[Run main.py]
    B --> C[Fetch content from Gemini API 🤖]
    C --> D[Process text/images with Hugging Face 🔍]
    D --> E[Generate final post ✍️]
    E --> F[Post to Facebook Page 📢]
    F --> G[Done ✅]


✅ Example Run

At 9 AM UTC every day, GitHub Actions starts the workflow.

It runs main.py.

The script generates AI content.

Posts it directly on your Facebook Page.