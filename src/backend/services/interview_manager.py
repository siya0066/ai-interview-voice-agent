#This file is responsible for:
##Managing interview states
##Extracting candidate information
##Keeping interview progress
##Tracking questions
##Preventing repeated questions
##Handling retries

import re
class InterviewManager:
    def __init__(self):

        # Interview States
        self.state = "ASK_NAME"

        #Candidate Details
        self.candidate_name = None
        self.candidate_role = None
        self.candidate_experience = None

        #Question Management
        self.current_question = None
        self.question_count = 0
        self.max_questions = 5
        self.retry_count = 0
        self.max_retries = 2
        self.asked_questions = []

        #Answer Buffer
        self.current_answer = ""
        self.last_answer_time = 0

        #Interview Report
        self.interview_data = []

    #NAME
    def process_name(self, transcript: str):
        transcript = transcript.strip()
        match = re.search(
            r"(?:my name is)\s+([a-zA-Z]+)", transcript, re.IGNORECASE
        )
        if match:
            name = match.group(1).title()
        else:
            words=transcript.split()
            if len(words) == 1:
                name = words[0].title()
            else:
                return None
        self.candidate_name = name
        self.state = "ASK_ROLE"

        return(
            f"Nice to meet you {name}."
            f"What role are you applying for?"
        )

    #ROLE
    def process_role(self, transcript: str):
        role = transcript.lower()
        patterns=[
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
            r"for an"
        ]
        for pattern in patterns:
            role = re.sub(pattern, "", role)
        role = role.replace(".", "")
        role = role.replace("?", "")
        role = role.strip().title()

        self.candidate_role = role
        self.state = "ASK_EXPERIENCE"

        return(
            f"Great, you are interviewing for the role of"
            f"{role}."
            f"How much experience do you have?"
        )

    #EXPERIENCE
    def process_experience(self, transcript: str):
        text = transcript.lower()
        years = re.findall(r"(\d+)", text)
        experience = "BEGINNER"
        if years:
            years = int(years[0])
            if years <= 1:
                experience = "BEGINNER"
            elif years <= 3:
                experience = "JUNIOR"
            elif years <= 5:
                experience = "MID"
            else:
                experience = "SENIOR"
        else:
            if "fresher" in text:
                experience = "BEGINNER"
            elif "beginner" in text:
                experience = "BEGINNER"
            elif "junior" in text:
                experience = "JUNIOR"
            elif "mid" in text:
                experience = "MID"
            elif "senior" in text:
                experience = "SENIOR"

        self.candidate_experience = experience
        self.state = "WAITING_FOR_ANSWER"

        return(
            f"Perfect. I've identified your experience level"
            f"as {experience}. Let's begin the interview."
        )


