from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import json
from src.config import Config
from src.prompts.sentiment_prompts import SENTIMENT_ANALYSIS_PROMPT

class SentimentAnalysisChain:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=Config.TEMPERATURE
        )

    def build_chain(self):
        """Build sentiment analysis chain using LCEL"""
        chain = (
            SENTIMENT_ANALYSIS_PROMPT
            | self.llm
            | StrOutputParser()
        )
        return chain

    def process(self, conversation: str) -> dict:
        """Process conversation for sentiment analysis"""
        chain = self.build_chain()
        result = chain.invoke({"conversation": conversation})

        try:
            sentiment_json = json.loads(result)
            return {
                "error": False,
                "data": sentiment_json
            }
        except json.JSONDecodeError:
            return {
                "error": False,
                "data": {
                    "Sentiment": "Neutral",
                    "Intent": ["Unable to parse"],
                    "raw_output": result
                }
            }
