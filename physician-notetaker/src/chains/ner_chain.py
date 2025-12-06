from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import json
from src.config import Config
from src.prompts.ner_prompts import (
    MEDICAL_VALIDATOR_PROMPT,
    NER_EXTRACTION_PROMPT,
    NER_VALIDATOR_PROMPT
)

class MedicalNERChain:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=Config.TEMPERATURE
        )

    def build_chain(self):
        """Build sequential chain for NER extraction with validation using LCEL"""

        # Chain 1: Validate if conversation is medical
        validator_chain = (
            MEDICAL_VALIDATOR_PROMPT
            | self.llm
            | StrOutputParser()
        )

        # Chain 2: Extract NER entities
        extraction_chain = (
            NER_EXTRACTION_PROMPT
            | self.llm
            | StrOutputParser()
        )

        # Chain 3: Validate and correct extracted entities
        # This chain needs both conversation and extracted_entities
        def prepare_validator_input(data):
            """Prepare input for validator chain"""
            return {
                "conversation": data["conversation"],
                "extracted_data": data["extracted_entities"]
            }

        correction_chain = (
            RunnableLambda(prepare_validator_input)
            | NER_VALIDATOR_PROMPT
            | self.llm
            | StrOutputParser()
        )

        # Build complete pipeline
        def complete_pipeline(inputs):
            conversation = inputs["conversation"]

            # Step 1: Validate medical conversation
            validation_result = validator_chain.invoke({"conversation": conversation})

            # Step 2: Extract entities if medical
            if "NON_MEDICAL" in validation_result:
                return {
                    "validation_result": validation_result,
                    "extracted_entities": None,
                    "final_entities": None
                }

            extracted_entities = extraction_chain.invoke({"conversation": conversation})

            # Step 3: Validate and correct
            final_entities = correction_chain.invoke({
                "conversation": conversation,
                "extracted_entities": extracted_entities
            })

            return {
                "validation_result": validation_result,
                "extracted_entities": extracted_entities,
                "final_entities": final_entities
            }

        return RunnableLambda(complete_pipeline)

    def process(self, conversation: str) -> dict:
        """Process conversation through NER pipeline"""
        chain = self.build_chain()
        result = chain.invoke({"conversation": conversation})

        # Check if medical conversation
        if result["validation_result"] and "NON_MEDICAL" in result["validation_result"]:
            return {
                "error": True,
                "message": "Sorry, I can only process medical conversations. I'm designed to extract medical information like symptoms, treatments, diagnoses, and prognosis from healthcare-related discussions."
            }

        # Parse final JSON output
        try:
            final_json = json.loads(result["final_entities"])
            return {
                "error": False,
                "data": final_json,
                "raw_extraction": result["extracted_entities"],
                "validation_status": "MEDICAL"
            }
        except (json.JSONDecodeError, TypeError):
            # Fallback parsing
            return {
                "error": False,
                "data": self._parse_fallback(result["final_entities"]),
                "raw_extraction": result["extracted_entities"],
                "validation_status": "MEDICAL"
            }

    def _parse_fallback(self, text: str) -> dict:
        """Fallback parser if JSON parsing fails"""
        if text is None:
            return {
                "Symptoms": [],
                "Treatment": [],
                "Diagnosis": [],
                "Prognosis": []
            }
        return {
            "Symptoms": [],
            "Treatment": [],
            "Diagnosis": [],
            "Prognosis": [],
            "raw_text": text
        }
