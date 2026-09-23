import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search , scrape_url 
from dotenv import load_dotenv
import os

load_dotenv()




llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=1024,
)

#1st agent 
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""You are a web research search agent.

Your job is to search the web for the user's research topic.

IMPORTANT:
1. Always use the web_search tool.
2. Search for recent and reliable sources.
3. Preserve the URLs returned by the web_search tool.
4. Do not remove or rewrite the URLs.
5. Return the search results including TITLE, URL and CONTENT.
"""
    )
#2nd agent 

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are a research reader agent.

        Your job is to read search results and select
        the most relevant source.

        IMPORTANT:
        1. Identify the URL from the search results.
        2. Call the scrape_url tool using that URL.
        3. Never ask the user to provide a URL.
        4. Do not simply summarize the search results.
        5. Use the scraped content to produce a useful research summary.
        """
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()