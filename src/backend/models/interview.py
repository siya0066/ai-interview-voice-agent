from datetime import UTC, datetime

from backend.schemas.interview_schema import InterviewReportSchema

# This is the model that converts the schema into a MongoDB document.

class Interview:
    def __init__(self, report: InterviewReportSchema):
        self.report = report

    def to_dict(self) -> dict:
        document = self.report.model_dump()
        document["created_at"] = datetime.now(UTC)

        return document


# Interview
##prepares data for MongoDB
##converts to dictionary
##future place for helper methods
