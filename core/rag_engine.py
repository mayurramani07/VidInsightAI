import os
import re
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever
)


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


def get_rag_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert transcript assistant. Answer the user's question
based ONLY on the transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from transcript:
{context}"""
            ),
            ("human", "{question}"),
        ]
    )

def get_rerank_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a reranking assistant for a RAG system.

Your job is to select the most relevant transcript chunks for answering the user question.

Rules:
- Return ONLY chunk numbers.
- Return numbers separated by commas.
- Do not explain.
- Select chunks that directly help answer the question.
- For broad questions like "Which companies were mentioned?", select chunks containing entity names.
- If multiple chunks are useful, include multiple chunks.

Example output:
1, 3, 5"""
            ),
            (
                "human",
                """Question:
{question}

Transcript chunks:
{chunks}

Return the best chunk numbers:""",
            ),
        ]
    )

def parse_selected_indexes(output: str, max_index: int):
    numbers = re.findall(r"\d+", output)

    selected_indexes = []

    for num in numbers:
        index = int(num) - 1

        if 0 <= index < max_index and index not in selected_indexes:
            selected_indexes.append(index)

    return selected_indexes

def rerank_docs(question: str, docs: list, llm, top_n: int = 6):
    if not docs:
        return []

    chunks_text = ""

    for i, doc in enumerate(docs, start=1):
        chunks_text += f"\nChunk {i}:\n{doc.page_content}\n"

    rerank_prompt = get_rerank_prompt()

    rerank_chain = rerank_prompt | llm | StrOutputParser()

    result = rerank_chain.invoke(
        {
            "question": question,
            "chunks": chunks_text,
        }
    )

    selected_indexes = parse_selected_indexes(result, len(docs))

    if not selected_indexes:
        return docs[:top_n]

    selected_docs = [docs[i] for i in selected_indexes]

    return selected_docs[:top_n]

def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)

    retriever = get_retriever(vector_store, k=12)

    llm = get_llm()
    prompt = get_rag_prompt()

    def build_context(question: str):
        retrieved_docs = retriever.invoke(question)

        reranked_docs = rerank_docs(
            question=question,
            docs=retrieved_docs,
            llm=llm,
            top_n=6,
        )

        return format_docs(reranked_docs)

    rag_chain = (
        {
            "context": RunnableLambda(build_context),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

def load_rag_chain():
    vector_store = load_vector_store()

    retriever = get_retriever(vector_store, k=12)

    llm = get_llm()
    prompt = get_rag_prompt()

    def build_context(question: str):
        retrieved_docs = retriever.invoke(question)

        reranked_docs = rerank_docs(
            question=question,
            docs=retrieved_docs,
            llm=llm,
            top_n=6,
        )

        return format_docs(reranked_docs)

    rag_chain = (
        {
            "context": RunnableLambda(build_context),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

def ask_question(rag_chain, question: str) -> str:
    print(f"Question: {question}")

    answer = rag_chain.invoke(question)

    print(f"Answer: {answer}")

    return answer