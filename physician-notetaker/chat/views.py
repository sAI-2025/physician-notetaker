import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from src.chains.ner_chain import MedicalNERChain
from src.chains.sentiment_chain import SentimentAnalysisChain
from src.chains.soap_chain import SOAPNoteChain


def analyze_medical_conversation(conversation):
    """
    Analyze medical conversation using three AI chains:
    1. NER Extraction (Symptoms, Treatment, Diagnosis, Prognosis)
    2. Sentiment & Intent Analysis
    3. SOAP Note Generation
    """

    # Initialize AI chains
    ner_chain = MedicalNERChain()
    sentiment_chain = SentimentAnalysisChain()
    soap_chain = SOAPNoteChain()

    # Process through all chains
    ner_result = ner_chain.process(conversation)
    sentiment_result = sentiment_chain.process(conversation)
    soap_result = soap_chain.process(conversation)

    # Build comprehensive result
    result = {
        "ner_extraction": {
            "status": "success" if not ner_result.get("error") else "error",
            "data": ner_result.get("data", {}),
            "message": ner_result.get("message", "")
        },
        "sentiment_analysis": {
            "status": "success" if not sentiment_result.get("error") else "error",
            "data": sentiment_result.get("data", {})
        },
        "soap_note": {
            "status": "success" if not soap_result.get("error") else "error",
            "data": soap_result.get("data", {})
        }
    }

    return result


def chat_view(request):
    """Render the main chat interface"""
    return render(request, 'chat/chat.html')


@csrf_exempt
def chat_api(request):
    """
    API endpoint to process medical conversations
    Accepts POST requests with conversation text
    Returns NER, Sentiment, and SOAP analysis
    """
    if request.method == "POST":
        try:
            # Parse request data
            data = json.loads(request.body)
            conversation = data.get("conversation", "")

            # Validate input
            if conversation.strip() == "":
                return HttpResponseBadRequest("Conversation text is empty.")

            # Analyze conversation
            print(f"\n🔍 Processing conversation ({len(conversation)} characters)...")
            analysis = analyze_medical_conversation(conversation)

            return JsonResponse({
                "success": True,
                "data": analysis
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON format"
            }, status=400)

        except Exception as e:
            print(f"❌ Error in chat_api: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": f"Processing error: {str(e)}"
            }, status=500)
    else:
        return HttpResponseBadRequest("Only POST method allowed.")


@csrf_exempt
def quick_analyze_api(request):
    """
    Quick analysis endpoint for specific analysis type
    Supports: ner, sentiment, soap
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            conversation = data.get("conversation", "")
            analysis_type = data.get("type", "all")

            if conversation.strip() == "":
                return HttpResponseBadRequest("Conversation text is empty.")

            result = {}

            if analysis_type in ["ner", "all"]:
                ner_chain = MedicalNERChain()
                result["ner"] = ner_chain.process(conversation)

            if analysis_type in ["sentiment", "all"]:
                sentiment_chain = SentimentAnalysisChain()
                result["sentiment"] = sentiment_chain.process(conversation)

            if analysis_type in ["soap", "all"]:
                soap_chain = SOAPNoteChain()
                result["soap"] = soap_chain.process(conversation)

            return JsonResponse({
                "success": True,
                "data": result
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)
    else:
        return HttpResponseBadRequest("Only POST method allowed.")
