from enum import StrEnum

from pydantic import BaseModel, Field


class ExperienceLevel(StrEnum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class InterviewCreateSchema(BaseModel):
    candidate_name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    experience: ExperienceLevel


class AnswerEvaluationSchema(BaseModel):
    score: float = Field(..., ge=0, le=10)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    feedback: str = ""


class InterviewQuestionSchema(BaseModel):
    question: str
    answer: str = ""
    evaluation: AnswerEvaluationSchema | None = None
    is_follow_up: bool = False


class FinalReportSchema(BaseModel):
    overall_score: float = Field(..., ge=0, le=10)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    recommendation: str


class InterviewReportSchema(BaseModel):
    candidate_name: str
    role: str
    experience: ExperienceLevel
    interview_data: list[InterviewQuestionSchema] = Field(default_factory=list)
    final_report: FinalReportSchema


# InterviewReportSchema
## validates data
##checks required fields
##ensures score is 0-10
##ensures lists are lists
