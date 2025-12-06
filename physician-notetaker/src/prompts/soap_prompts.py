from langchain.prompts import PromptTemplate

SOAP_NOTE_PROMPT = PromptTemplate(
    input_variables=["conversation"],
    template="""You are an expert medical documentation specialist. Generate a structured SOAP note from this physician-patient conversation.

**SOAP Format:**
- **Subjective**: Patient's complaints, symptoms, history (what patient says)
- **Objective**: Physical examination findings, observations (what physician observes)
- **Assessment**: Diagnosis, medical interpretation
- **Plan**: Treatment recommendations, follow-up

**Conversation:**
{conversation}

**Instructions:**
- Extract ONLY information explicitly stated in the conversation
- Use professional medical terminology
- Be concise but comprehensive
- Organize chronologically within each section
- Include specific details (dates, numbers, durations)

**Output Format (STRICT JSON):**
{{
  "Subjective": {{
    "Chief_Complaint": "primary reason for visit",
    "History_of_Present_Illness": "detailed patient narrative",
    "Review_of_Systems": "additional symptoms or concerns"
  }},
  "Objective": {{
    "Physical_Exam": "examination findings",
    "Observations": "physician observations",
    "Vitals": "if mentioned"
  }},
  "Assessment": {{
    "Diagnosis": "confirmed diagnosis",
    "Severity": "condition severity",
    "Clinical_Impression": "physician's assessment"
  }},
  "Plan": {{
    "Treatment": "treatment given or recommended",
    "Medications": "if applicable",
    "Follow_Up": "follow-up instructions",
    "Prognosis": "expected outcome"
  }}
}}

JSON Output:"""
)
