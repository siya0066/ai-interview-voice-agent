#This is the model that converts the schema into a MongoDB document.

from backend.schemas.interview_schema import InterviewReportSchema

class Interview:

    def __init__(
            self,
            report: InterviewReportSchema
    ):

        self.report = report

    def to_dict(self):
        return self.report.model_dump()

#Interview
##prepares data for MongoDB
##converts to dictionary
##future place for helper methods