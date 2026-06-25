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
                """You are a professional transcript summarization assistant.

Summarize the given transcript chunk clearly and concisely.

The transcript may come from a meeting, podcast, YouTube video, interview, lecture, or discussion.

Focus on:
- Important discussion points
- Key conclusions or decisions, if any
- Action items or useful next steps, if any
- Deadlines or timelines, if mentioned
- Names, tools, products, companies, or technical terms if mentioned

Rules:
- Do not add anything that is not present in the transcript.
- Keep the summary short, clear, and useful."""
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
                """You are an expert transcript summarizer.

You will receive multiple partial summaries from a long transcript.

The transcript may come from a meeting, podcast, YouTube video, interview, lecture, or discussion.

Combine the partial summaries into one clean, professional final summary.

Output format:

## Summary
- Main points discussed

## Key Decisions / Conclusions
- Decisions or clear conclusions mentioned
- If none are present, write "None explicitly mentioned."

## Action Items / Next Steps
- Task:
  Owner:
  Deadline:
- If none are present, write "No action items found."

## Important Notes
- Any risks, blockers, follow-ups, context, or important observations

Rules:
- Use clear bullet points.
- Do not repeat the same point multiple times.
- Do not add information that is not present.
- If owner or deadline is not mentioned, write "Not mentioned.
"""
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
                """You are a professional title generator.

Generate a short, clear title based on the transcript.

The transcript may come from a meeting, podcast, YouTube video, interview, lecture, or discussion.

Rules:
- Maximum 8 words
- Professional tone
- No quotation marks
- No extra explanation
- Only return the title"""
            ),
            ("human", "Transcript:\n\n{text}"),
        ]
    )

    title_chain = title_prompt | llm | StrOutputParser()

    return title_chain.invoke({"text": transcript[:2000]})