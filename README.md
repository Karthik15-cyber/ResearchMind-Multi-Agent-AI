# ResearchMind: Multi-Agent AI Research System

ResearchMind takes any research topic and produces a structured, source-cited report. It chains two tool-calling agents and two LLM chains: one searches the web, one reads the best source in depth, one writes the report, and one critiques it.

**Live demo:** [ADD_STREAMLIT_LINK_HERE](ADD_STREAMLIT_LINK_HERE)

![ResearchMind screenshot](screenshot.png)

---

## How It Works

```
Topic → Search Agent → Reader Agent → Writer Chain → Critic Chain → Report + Feedback
```

| Stage | Type | What it does |
|---|---|---|
| 1. Search Agent | Tool-calling agent | Uses the Tavily search tool to find the top 3 recent sources (title, URL, snippet) |
| 2. Reader Agent | Tool-calling agent | Picks the most relevant URL and scrapes it with BeautifulSoup for deeper content |
| 3. Writer Chain | LLM chain | Combines search results and scraped content into a report with an introduction, key findings, conclusion, and sources |
| 4. Critic Chain | LLM chain | Scores the report out of 10 and lists strengths, areas to improve, and a one-line verdict |

All stages run on **GPT-OSS-120B served through Groq**, orchestrated with **LangChain**.

The two agents decide for themselves when and how to call their tools. The writer and critic are fixed prompt chains, since their inputs are already known.

---

## Features

- End-to-end research from a single topic input
- Live web search (Tavily) and page scraping (BeautifulSoup) for up-to-date information
- Structured reports that list every source URL used
- Automatic quality review with a score and specific improvement points
- Streamlit interface with pipeline progress, expandable raw agent outputs, and Markdown report download
- Command-line version (`pipeline.py`) for running without the UI

---

## Tech Stack

- **Python**
- **LangChain**: agents, prompt templates, output parsers
- **Groq**: fast LLM inference (GPT-OSS-120B)
- **Tavily**: web search API built for LLM agents
- **BeautifulSoup + Requests**: web scraping
- **Streamlit**: web interface

---

## Project Structure

```
ResearchMind/
├── agents.py          # LLM setup, search and reader agents, writer and critic chains
├── tools.py           # web_search (Tavily) and scrape_url (BeautifulSoup) tools
├── pipeline.py        # Command-line version of the full pipeline
├── app.py             # Streamlit web app
├── requirements.txt   # Python dependencies
├── .env.example       # Template for the required API keys
└── README.md
```

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/Karthik15-cyber/ResearchMind.git
cd ResearchMind
```

**2. Create a virtual environment and install dependencies**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

**3. Add your API keys**

Copy `.env.example` to `.env` and fill in your keys:

```
GROQ_API_KEY=your-groq-key
TAVILY_API_KEY=your-tavily-key
```

Both services offer free tiers: [Groq](https://console.groq.com/keys) and [Tavily](https://app.tavily.com).

**4. Run the app**

```bash
streamlit run app.py
```

Or run the command-line version:

```bash
python pipeline.py
```

---

## Example Topics

- LLM agents in 2025
- CRISPR gene editing
- Fusion energy progress

---

## Limitations

- The reader agent scrapes only one source per run, and keeps the first 1,500 characters, so depth depends on that page.
- Some websites block scraping or load content with JavaScript, which returns little usable text.
- The critic's feedback is shown to the user but not yet used to improve the report.

## Future Improvements

- Feed the critic's feedback back to the writer for an automatic revision round
- Scrape and combine multiple sources instead of one
- Add error handling and retries for API and scraping failures
- Measure report quality across many topics (for example, average critic score)

---

## Author

**Kondrapu Karthik**
GitHub: [Karthik15-cyber](https://github.com/Karthik15-cyber) · LinkedIn: [karthik-kondrapu](https://www.linkedin.com/in/karthik-kondrapu/)
