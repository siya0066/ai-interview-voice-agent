# This file is responsible for:
##Managing interview states
##Extracting candidate information
##Keeping interview progress
##Tracking questions
##Preventing repeated questions
##Handling retries

import re
from typing import Any


class InterviewManager:
    MAX_QUESTION = 5
    MAX_RETRIES = 2

    def __init__(self):

        # Interview States
        self.state = "ASK_NAME"

        # Candidate Details
        self.candidate_name = None
        self.candidate_role = None
        self.candidate_experience = None

        # Question Management
        self.current_question = None
        self.question_count = 0
        self.max_questions = self.MAX_QUESTION
        self.retry_count = 0
        self.max_retries = self.MAX_RETRIES
        self.asked_questions = []

        # Answer Buffer
        self.current_answer = ""
        self.last_answer_time = 0

        # Interview Report
        self.interview_data: list[dict[str, Any]] = []

    # NAME
    def process_name(self, transcript: str) -> str | None:
        transcript = transcript.strip()

        if not transcript:
            return None

        match = re.search(r"my name is\s+([a-zA-Z]+)", transcript, re.IGNORECASE)

        if match:
            name = match.group(1).title()
        else:
            words = transcript.split()

            if len(words) == 1 and words[0].isalpha():
                name = words[0].title()
            else:
                return None

        self.candidate_name = name
        self.state = "ASK_ROLE"

        return f"Nice to meet you, {name}. What role are you applying for?"

    # ROLE
    def process_role(self, transcript: str) -> str | None:
        role = transcript.strip()

        if not role:
            return None

        patterns = [
            r"i am interviewing for the role of",
            r"i'm interviewing for the role of",
            r"interviewing for the role of",
            r"for the role of",
            r"i am applying for",
            r"i'm applying for",
            r"applying for",
            r"role of",
            r"role for",
            r"role of a",
            r"for a",
            r"for an",
        ]

        role = role.lower()

        for pattern in patterns:
            role = re.sub(pattern, "", role)

        role = role.replace(".", "").replace("?", "").strip()

        if not role:
            return None

        self.candidate_role = role.title()
        self.state = "ASK_EXPERIENCE"

        return (
            f"Great, you are interviewing for the role of "
            f"{self.candidate_role}. "
            f"How much experience do you have?"
        )

    # EXPERIENCE
    def process_experience(self, transcript: str) -> str:
        text = transcript.lower()

        years_match = re.search(r"(\d+)", text)

        if years_match:
            years = int(years_match.group(1))

            if years <= 1:
                experience = "BEGINNER"
            elif years <= 3:
                experience = "INTERMEDIATE"
            else:
                experience = "ADVANCED"
        elif any(
            word in text for word in ("fresher", "beginner", "student", "no experience")
        ):
            experience = "BEGINNER"

        elif any(word in text for word in ("intermediate", "junior")):
            experience = "INTERMEDIATE"

        elif any(word in text for word in ("advanced", "senior")):
            experience = "ADVANCED"

        else:
            experience = "BEGINNER"

        self.candidate_experience = experience
        self.state = "READY_FOR_QUESTION"

        return (
            f"Perfect. I've identified your experience level "
            f"as {experience}. Let's begin the interview."
        )

    # QUESTION MANAGEMENT
    def is_question_repeated(self, question: str) -> bool:
        normalized = self._normalize_question(question)

        return any(
            self._normalize_question(previous) == normalized
            for previous in self.asked_questions
        )

    def add_asked_question(self, question: str, is_follow_up: bool = False) -> bool:
        question = question.strip()

        if not question:
            return False

        if self.is_question_repeated(question):
            return False

        self.asked_questions.append(question)
        self.current_question = question

        if not is_follow_up:
            self.question_count += 1

        self.retry_count = 0
        self.current_answer = ""
        self.state = "WAITING_FOR_ANSWER"

        return True

    @staticmethod
    def _normalize_question(question: str) -> str:
        return re.sub(r"\s+", " ", question.lower().strip())

    # ANSWER MANAGEMENT
    def record_answer(
        self,
        answer: str,
        evaluation: dict[str, Any] | None = None,
        is_follow_up: bool = False,
    ) -> None:
        if not self.current_question:
            return

        self.current_answer = answer.strip()

        self.interview_data.append(
            {
                "question": self.current_question,
                "answer": self.current_answer,
                "evaluation": evaluation,
                "is_follow_up": is_follow_up,
            }
        )

        self.current_question = ""

    # FOLLOW-UP / RETRY MANAGEMENT
    def should_follow_up(self) -> bool:
        return self.retry_count < self.max_retries

    def register_retry(self) -> bool:
        if self.retry_count >= self.max_retries:
            return False

        self.retry_count += 1
        return True

    def reset_retry(self) -> None:
        self.retry_count = 0

    # INTERVIEW COMPLETION
    def has_finished_questions(self) -> bool:
        return self.question_count >= self.max_questions

    def is_complete(self) -> bool:
        return self.state == "COMPLETED"

    def complete_interview(self) -> None:
        self.state = "COMPLETED"

    # HELPERS
    def get_previous_questions(self) -> list[str]:
        return self.asked_questions.copy()

    def get_interview_data(self) -> list[dict[str, Any]]:
        return self.interview_data.copy()

    def get_candidate_info(self) -> dict[str, str | None]:
        return {
            "candidate_name": self.candidate_name,
            "role": self.candidate_role,
            "experience": self.candidate_experience,
        }
