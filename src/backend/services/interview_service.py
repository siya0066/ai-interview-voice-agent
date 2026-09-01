from typing import Any

from backend.services.interview_manager import InterviewManager
from backend.services.interviewer import (
    evaluate_answer,
    generate_followup_question,
    generate_question,
)


class InterviewService:
    def __init__(self):
        self.manager = InterviewManager()

    def get_candidate_info(self) -> dict[str, str | None]:
        return self.manager.get_candidate_info()

    def get_interview_data(self) -> list[dict[str, Any]]:
        return self.manager.get_interview_data()

    def start_interview(self) -> str:
        candidate = self.manager.get_candidate_info()

        question = generate_question(
            role=candidate["role"] or "",
            experience=candidate["experience"] or "BEGINNER",
            previous_questions=self.manager.get_previous_questions(),
        )

        if not self.manager.add_asked_question(question):
            raise ValueError("Generated question was already asked.")

        return question

    def process_input(self, transcript: str) -> str | None:
        if self.manager.state == "ASK_NAME":
            return self.manager.process_name(transcript)

        if self.manager.state == "ASK_ROLE":
            return self.manager.process_role(transcript)

        if self.manager.state == "ASK_EXPERIENCE":
            return self.manager.process_experience(transcript)

        if self.manager.state == "READY_FOR_QUESTION":
            return self.start_interview()

        return None

    def submit_answer(self, answer: str) -> str:
        if not self.manager.current_question:
            return "There is no active interview question."

        question = self.manager.current_question

        evaluation = evaluate_answer(question=question, answer=answer)

        self.manager.record_answer(answer=answer, evaluation=evaluation)

        # Interview is complete
        if self.manager.has_finished_questions():
            self.manager.complete_interview()
            return "Interview completed."

        # Weak answer → follow-up
        if evaluation.get("score", 0) < 6 and self.manager.should_follow_up():
            self.manager.register_retry()

            follow_up = generate_followup_question(
                original_question=question,
                answer=answer,
            )

            if self.manager.add_asked_question(follow_up, is_follow_up=True):
                return follow_up

            self.manager.reset_retry()

        # Strong answer OR follow-up limit reached
        # → move to the next main question
        self.manager.reset_retry()
        return self.start_interview()
