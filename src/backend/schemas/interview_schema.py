# These are your Pydantic schemas for request/response validation.

from datetime import datetime

from pydantic import BaseModel, Field


class EvaluationSchema(BaseModel):
    score: int = Field(..., ge=0, le=10)
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]


class InterviewQuestionSchema(BaseModel):
    question: str
    answer: str
    evaluations: EvaluationSchema


class FinalReportSchema(BaseModel):
    overall_score: float
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]
    recommendation: str


class InterviewReportSchema(BaseModel):
    candidate_name: str
    role: str
    experience: str
    interview_data: list[InterviewQuestionSchema]
    final_report: FinalReportSchema
    created_at: datetime = Field(default_factory=datetime.now)


# InterviewReportSchema
## validates data
##checks required fields
##ensures score is 0-10
##ensures lists are lists
