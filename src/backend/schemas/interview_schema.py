#These are your Pydantic schemas for request/response validation.

from pydantic import BaseModel,Field
from typing import List
from datetime import datetime

class EvaluationSchema(BaseModel):
    score: int = Field(..., ge=0, le=10)
    strengths: List [str]
    weaknesses: List [str]
    improvements: List [str]

class InterviewQuestionSchema(BaseModel):
    question: str
    answer: str
    evaluations: EvaluationSchema

class FinalReportSchema(BaseModel):
    overall_score: float
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]
    recommendation: str

class InterviewReportSchema(BaseModel):
    candidate_name: str
    role: str
    experience: str
    interview_data: List[InterviewQuestionSchema]
    final_report: FinalReportSchema
    created_at: datetime= Field(default_factory=datetime.now)

#InterviewReportSchema
## validates data
##checks required fields
##ensures score is 0-10
##ensures lists are lists