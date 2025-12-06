from langchain.prompts import PromptTemplate

SENTIMENT_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["conversation"],
    template="""You are a medical sentiment analysis expert. Analyze the patient's emotional state and intent.

**Conversation:**
{conversation}

**Task:**
Analyze ONLY the patient's statements (not the physician's) to determine:

1. **Sentiment Classification:**
   - Anxious: Patient expresses worry, fear, concern, or distress
   - Neutral: Patient shows calm, matter-of-fact responses without strong emotion
   - Reassured: Patient expresses relief, comfort, or confidence

2. **Intent Detection:**
   - "Seeking reassurance": Patient wants confirmation things will be okay
   - "Reporting symptoms": Patient describing medical issues
   - "Expressing concern": Patient worried about health outcomes
   - "Asking questions": Patient seeking information
   - "Acknowledging improvement": Patient noting positive progress

**Instructions:**
- Focus on patient dialogue only
- Choose the MOST DOMINANT sentiment if multiple are present
- List ALL applicable intents
- Base analysis on explicit statements, not assumptions

**Output Format (STRICT JSON):**
{{
  "Sentiment": "Anxious OR Neutral OR Reassured",
  "Intent": ["list of detected intents"],
  "Confidence": "High OR Medium OR Low",
  "Patient_Quotes": ["key quotes supporting the sentiment"]
}}

JSON Output:"""
)
