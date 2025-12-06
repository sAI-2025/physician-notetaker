from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import json
from src.config import Config
from src.prompts.soap_prompts import SOAP_NOTE_PROMPT

class SOAPNoteChain:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=Config.TEMPERATURE
        )

    def build_chain(self):
        """Build SOAP note generation chain using LCEL"""
        chain = (
            SOAP_NOTE_PROMPT
            | self.llm
            | StrOutputParser()
        )
        return chain

    def process(self, conversation: str) -> dict:
        """Generate SOAP note from conversation"""
        chain = self.build_chain()
        result = chain.invoke({"conversation": conversation})

        try:
            soap_json = json.loads(result)
            return {
                "error": False,
                "data": soap_json
            }
        except json.JSONDecodeError:
            return {
                "error": False,
                "data": {
                    "raw_output": result,
                    "note": "Please review raw output"
                }
            }
