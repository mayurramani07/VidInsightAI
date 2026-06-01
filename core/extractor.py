from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os 


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2
    )


def build_chain(system_prompt: str):
    llm = get_llm()

    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Text:\n\n{text}"),
        ])
        | llm
        | StrOutputParser()
    )


def extract_action_items(text: str) -> str:
    chain = build_chain(
        """
        You are an expert analyst for meetings, podcasts, YouTube videos, and long transcripts.

        Extract action items or useful next steps from the given text.

        Rules:
        - If the text already contains an "Action Items" section, extract those action items directly.
        - Include explicit action items if present.
        - Include practical suggestions only if the speaker clearly recommends doing them.
        - Do not convert general discussion topics into tasks.
        - Do not create research tasks unless the text clearly says someone should investigate, analyze, evaluate, or research something.
        - If owner is not mentioned, write Owner: Not mentioned.
        - If deadline is not mentioned, write Deadline: Not mentioned.
        - Do not invent facts.
        - Only say "No action items found" if the text contains no task, suggestion, recommendation, or follow-up.

        Format:
        1. Task:
           Owner:
           Deadline:
        """
    )

    return chain.invoke(text)


def extract_key_decisions(text: str) -> str:
    chain = build_chain(
        """
        You are an expert analyst for meetings, podcasts, YouTube videos, and long transcripts.

        Extract key decisions or confirmed conclusions from the given text.

        A key decision can be:
        - A decision made by people in the transcript
        - A confirmed business/product/pricing change mentioned in the discussion
        - A clear conclusion stated by the speaker

        Rules:
        - Do not invent decisions.
        - If no actual decision or confirmed conclusion exists, say exactly:
          No key decisions found.

        Format as a numbered list.
        """
    )

    return chain.invoke(text)


def extract_questions(text: str) -> str:
    chain = build_chain(
        """
        You are an expert analyst for meetings, podcasts, YouTube videos, and long transcripts.

        Extract open questions, unresolved concerns, or topics needing follow-up from the given text.

        Include:
        - Direct unanswered questions
        - Implied unresolved concerns
        - Risks that need further investigation
        - Business, technical, or pricing uncertainties

        Rules:
        - Do not invent unrelated questions.
        - If there are no open questions or unresolved concerns, say exactly:
          No open questions found.

        Format as a numbered list.
        """
    )

    return chain.invoke(text)