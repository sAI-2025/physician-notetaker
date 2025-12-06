from langchain.prompts import PromptTemplate

# Chain 1: Medical Conversation Validator
MEDICAL_VALIDATOR_PROMPT = PromptTemplate(
    input_variables=["conversation"],
    template="""You are a medical conversation validator.

Determine if the following conversation is related to medical/healthcare topics.

Conversation:
{conversation}

Respond with ONLY one word: "MEDICAL" or "NON_MEDICAL"

Response:"""
)

# Chain 2: NER Extraction - STRICT JSON OUTPUT
NER_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["conversation"],
    template="""You are a medical NER extraction system. Extract entities and return ONLY valid JSON.

**Extract these entities from the conversation:**
- Symptoms: Physical complaints, pain, discomfort
- Treatment: Medications, therapies, procedures
- Diagnosis: Medical conditions identified
- Prognosis: Recovery predictions, future outcomes

**Conversation:**
{conversation}

**CRITICAL INSTRUCTIONS:**
- Return ONLY the JSON object, NO explanatory text
- NO markdown code blocks, NO "```
- Start your response with {{ and end with }}
- If no entity found, use empty array []

**Example Output Format:**
{{
  "Symptoms": ["neck pain", "back pain"],
  "Treatment": ["physiotherapy"],
  "Diagnosis": ["whiplash injury"],
  "Prognosis": ["full recovery expected"]
}}

Now extract from the conversation above. Return ONLY the JSON:"""
)

# Chain 3: Validator & Corrector - STRICT JSON OUTPUT
NER_VALIDATOR_PROMPT = PromptTemplate(
    input_variables=["conversation", "extracted_data"],
    template="""You are a medical data validator. Verify extracted NER data and return corrected JSON.

**Original Conversation:**
{conversation}

**Extracted Data to Validate:**
{extracted_data}

**Your Task:**
1. Verify all entities exist in the conversation
2. Remove any hallucinated information
3. Add any missing entities
4. Return corrected JSON

**CRITICAL INSTRUCTIONS:**
- Return ONLY the JSON object, NO explanatory text
- NO markdown, NO "```json" tags, NO commentary
- Start with {{ and end with }}
- Use exact medical terms from conversation

**Required JSON Format:**
{{
  "Symptoms": ["list"],
  "Treatment": ["list"],
  "Diagnosis": ["list"],
  "Prognosis": ["list"]
}}

Return ONLY the corrected JSON now:"""
)
