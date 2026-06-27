# Sales Insights Agent

**Author:** Niloofar Saghir

An AI agent that analyzes e-commerce sales data and generates business insights reports — with a human-in-the-loop approval step before any report is finalized.

Built for the **5-Day AI Agents Intensive Course** (Kaggle/Google), Capstone Project — **Agents for Business** track.

## What it does

Instead of manually pulling sales data, calculating trends, and writing up findings, this agent automates the process end-to-end while keeping a human in control of the final output:

1. **Query the data** — ask about top products, top customers, sales by country, or date-range performance
2. **Draft an insights report** — the agent pulls live numbers from the dataset and writes a structured report: trend summary, top performers (in tables), and recommended business actions
3. **Human review** — the draft is shown in full before anything is finalized; the human can approve or request changes
4. **Finalize** — once approved, the agent returns the completed report

This human-in-the-loop step matters in real business settings, where an unreviewed AI-generated number in a report sent to stakeholders can cause real damage. The agent removes the slow, mechanical work (data pulling, calculating, first-draft writing) so a human only needs to spend time on judgment.

## Tech stack

- **Google ADK (Agent Development Kit)** — agent framework and tool orchestration
- **Gemini API** — language model for reasoning and report generation
- **Google Antigravity** — AI-assisted IDE used to build and iterate on this project
- **Pandas** — data loading and analysis
- **Dataset**: [Online Retail Dataset](https://www.kaggle.com/datasets/carrie1/ecommerce-data) — ~540K UK e-commerce transactions

## Course concepts applied

- Agentic tool use / function calling
- Human-in-the-loop design for safe agent output
- Vibe coding with Google Antigravity + ADK

## Setup

1. Clone this repo
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Download `data.csv` from the [Online Retail Dataset](https://www.kaggle.com/datasets/carrie1/ecommerce-data) and place it in the project root
5. Run the agent:
   ```
   adk web sales_agent
   ```
6. Open the URL shown (typically `http://127.0.0.1:8000`), select `sales_agent`, and start chatting

## Example queries

- "What are the top 5 best-selling products?"
- "Which country generates the most revenue?"
- "Generate an insights report for January 2011"
- "Generate an insights report for the full year 2011"

## Notes

This is a capstone project for a learning course — built and debugged iteratively, including working through Gemini API rate limits and ADK's experimental tool-confirmation behavior, before settling on a simpler, reliable two-step draft → approve → finalize pattern for the human-in-the-loop flow.
