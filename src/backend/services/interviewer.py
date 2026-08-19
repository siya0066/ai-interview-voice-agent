#Your entire project will use just four functions:
##generate_question(...)
##generate_followup_question(...)
##evaluate_answer(...)
##generate_final_report(...)
#This keeps all LLM-related code in one place.

import json
import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
)
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

#Generate Interview Question
def generate_question(
        role: str,
        experience: str,
        previous_questions: list[str]
):
    prompt = f"""
You are an experienced technical interviewer.

Candidate Role:
{role}

Experience Level:
{experience}

Previously Asked Questions:
{previous_questions}

IMPORTANT:
- Never repeat any question from the list above.
- Generate a completely different question.

Difficulty:

BEGINNER
- Very easy
- Basic concepts only

JUNIOR
- Easy to medium

MID
- Medium difficulty

SENIOR
- Medium to advanced

Rules:

- Ask ONLY ONE question.
- Conceptual question only.
- No coding.
- No DSA.
- No system design.
- No mathematical questions.
- Maximum 20 words.
- Return ONLY the question.
"""
    try:
        messages: list[ChatCompletionUserMessageParam] = [
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]

        response: ChatCompletion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Groq returned an empty response.")

        question = content.strip()
        if not question:
            return "Tell me about yourself."
        return question
    except Exception as e:
        print("QUESTION ERROR:", e)
        return "Tell me about yourself."

#Generate Follow-up Question
def generate_followup_question(
        original_question: str,
        answer: str
):
    prompt = f"""
    You are an interviewer.

Original Question:
{original_question}

Candidate Answer:
{answer}

The answer is incomplete.

Ask ONE short follow-up question
that helps the candidate explain
their answer better.

Rules:

- Friendly
- Under 15 words
- Return ONLY the question.
"""
    try:
        messages: list[ChatCompletionUserMessageParam] = [
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]

        response: ChatCompletion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Groq returned an empty response.")

        return content.strip()
    except Exception as e:
        print("FOLLOWUP ERROR:", e)
        return original_question

#Evaluate Candidate Answer
def evaluate_answer(
        question: str,
        answer: str
):
    prompt = f"""
    You are a senior interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer fairly.

Scoring Guide:

1-3
Incorrect or irrelevant.

4-5
Partially correct.

6-7
Correct but basic.

8-10
Strong answer.

Return ONLY JSON.

Format:

{{
    "score": number,
    "strengths": [],
    "weaknesses": [],
    "improvements": []
}}
"""
    try:
        messages: list[ChatCompletionUserMessageParam] = [
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]

        response: ChatCompletion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Groq returned an empty response.")

        text = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(text)
    except Exception as e:
        print("EVALUATION ERROR:", e)
        return {
            "score": 5,
            "strengths": [],
            "weaknesses": [],
            "improvements": []
        }

#Final Interview Report
def generate_final_report(
        interview_data
):
    prompt = f"""
    You are a senior technical interviewer.

Interview Data:

{interview_data}

Generate a JSON report.

Format:

{{
    "overall_score": number,
    "strengths": [],
    "weaknesses": [],
    "improvements": [],
    "recommendation": ""
}}
"""
    try:
        messages: list[ChatCompletionUserMessageParam] = [
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]

        response: ChatCompletion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Groq returned an empty response.")

        text = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(text)
    except Exception as e:
        print("FINAL REPORT ERROR:", e)
        return {
            "overall_score": 0,
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "recommendation":"Unable to generate report."
        }


