from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda

import os


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )

    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a professional meeting notes assistant. Summarize the given transcript chunk clearly and concisely.

                Focus on:
                - Important discussion points
                - Decisions made
                - Action items
                - Deadlines or timelines
                - Names, tools, products, or technical terms if mentioned
               Do not add anything that is not present in the transcript.
               Keep the summary short and useful. """
            ),
            ("human", "Transcript chunk:\n\n{text}"),
        ]
    )

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [
        map_chain.invoke({"text": chunk})
        for chunk in chunks
    ]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert meeting summarizer. You will receive multiple partial summaries from a long meeting transcript. 
                Combine them into one clean, professional final meeting summary.
                Output format: 
                ## Meeting Summary
                - Main points discussed
                ## Key Decisions
                - Decisions made during the meeting
                ## Action Items
                - Task
                - Owner, if mentioned
                - Deadline, if mentioned

                ## Important Notes
                - Any risks, blockers, follow-ups, or extra context

                Rules:
                - Use clear bullet points.
                - Do not repeat the same point multiple times.
                - Do not add information that is not present.
                - If owner or deadline is not mentioned, write "Not mentioned"."""
            ),
            ("human", "Partial summaries:\n\n{text}"),
        ]
    )

    combined_chain = (
        RunnableLambda(lambda x: {"text": x})
        | combined_prompt
        | llm
        | StrOutputParser()
    )

    return combined_chain.invoke(combined)


def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a professional meeting title generator. Generate a short, clear meeting title based on the transcript.
                Rules:
                - Maximum 8 words
                - Professional tone
                - No quotation marks
                - No extra explanation
                - Only return the title"""
            ),
            ("human", "Meeting transcript:\n\n{text}"),
        ]
    )

    title_chain = title_prompt | llm | StrOutputParser()

    return title_chain.invoke({"text": transcript[:2000]})