import os
from textwrap import dedent

import requests
from bs4 import BeautifulSoup
from crewai import Agent as CrewAgent
from crewai import Task
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError(
        "You need to provide an API key: https://platform.openai.com/api-keys"
    )

default_llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.1,
    model_name="gpt-4o-mini",
)


# models to llm response format
class GrammarMistake(BaseModel):
    error: str = Field(description="error/mistake in content")
    solution: str = Field(description="solution to that error")


class Mistakes(BaseModel):
    errors: list[GrammarMistake]


def scrape_website_text(url):
    """
    Scrapes the specified website and returns the text content.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, "html.parser")

        website_content = []

        for script in soup(["script", "style"]):
            script.decompose()

        def print_leaf_text(element):
            if not element.find_all():
                content = element.get_text(separator="\n").strip()
                if content:
                    website_content.append(content)
            else:
                for child in element.find_all(recursive=False):
                    print_leaf_text(child)

        print_leaf_text(soup)
        return website_content
    except Exception as e:
        print(f"Exception while scrapping {url}. error: {e}")
        raise


def find_content_grammar_mistakes(content):
    """
    get the scrapped content and return the grammar mistakes with suggested solution.
    """
    try:
        grammar_analyzer_agent = CrewAgent(
            role="Quality Assurance Editor",
            goal="""Identify and correct grammatical mistakes in provided content.
                Prioritize sentences first and then words. Provide all errors
                and suggested solutions in a key-value pair format, where the key
                is the wrong statement or word (error) and the value is its
                respective solution.
                """,
            backstory="""You are a meticulous Quality Assurance Editor with a sharp
                    eye for detail and a passion for linguistic precision. Your
                    expertise lies in reviewing, refining, and perfecting content
                    to ensure it adheres to the highest standards of grammar, style,
                    and coherence. You excel in identifying and correcting
                    grammatical errors, inconsistencies, and stylistic deviations
                    across various types of written material.""",
            llm=default_llm,
        )

        grammar_review_task = Task(
            description="""Grammar Mistakes finder and suggest solution to those mistakes.""",
            agent=grammar_analyzer_agent,
            expected_output=dedent(
                f"""
                    give me list of grammar mistakes available in given content(list of words/sentence): {content}
                    result should follow the below mentioned pydantic V1 model and make sure to not repeat a sentence or word:

                    class GrammarMistake(BaseModel):
                        error: str = Field(..., description="error/mistake in content")
                        solution: str = Field(..., description="solution to that error")
                    class Mistakes(BaseModel):
                        errors: list[GrammarMistake]
                    """
            ),
            output_json=Mistakes,
        )
        results = grammar_review_task.execute_sync()
        return results
    except Exception as e:
        print(f"Exception while finding grammar mistakes {e}")
        raise
