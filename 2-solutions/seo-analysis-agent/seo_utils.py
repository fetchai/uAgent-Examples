import os
from typing import Optional

import requests
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_CSE_ID = os.getenv("GOOGLE_SEARCH_CSE_ID")


def get_serp(keywords, count=4) -> Optional[list[str]]:
    query = " ".join(keywords)
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={GOOGLE_SEARCH_CSE_ID}&num={count}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
    except Exception:
        return None
    return [item["link"] for item in result.get("items", [])]


def extract_keywords(text, url):
    parser = CommaSeparatedListOutputParser()
    prompt_string = (
        f"Given the following text extracted from {url}, identify and list the "
        "three most relevant keywords as a Python list. Exclude brandname, the "
        "page title, or parts from the URL from the keywords. Return the "
        f"keywords as a comma-separated list.:\n\n{text}"
    )
    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
        template="{subject}.\n{format_instructions}",
        input_variables=["subject"],
        partial_variables={"format_instructions": format_instructions},
    )
    llm = OpenAI()
    chain = prompt | llm | parser
    response = chain.invoke({"subject": prompt_string})
    return response


def compare_websites(
    superior_page_content, inferior_page_content, keywords, superior_url, inferior_url
):
    prompt = f"""
    You are an SEO expert agent advising website owners how to improve their content.
    For this, you will compare a superior ranked website 'SUPERIOR' ({superior_url})
    with the website to be evaluated 'ORIGINAL' ({inferior_url})
    and summarize why the superior website ranks better for the given 'KEYWORDS'.
    You can include 1 or 2 concrete examples of what superior is doing better,
    or what inferior is not doing well.\n
    # SUPERIOR\n{superior_page_content[:20000]}\n
    # ORIGINAL\n{inferior_page_content[:20000]}\n
    # KEYWORDS\n{keywords}\n
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    comparison_result = llm.invoke(prompt)
    return comparison_result.content
