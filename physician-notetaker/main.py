import json
from src.chains.ner_chain import MedicalNERChain
from src.chains.sentiment_chain import SentimentAnalysisChain
from src.chains.soap_chain import SOAPNoteChain

def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def main():
    # Sample conversation
    conversation = """
    Physician: Good morning, Ms. Jones. How are you feeling today?

    Patient: Good morning, doctor. I'm doing better, but I still have some discomfort now and then.

    Physician: I understand you were in a car accident last September. Can you walk me through what happened?

    Patient: Yes, it was on September 1st, around 12:30 in the afternoon. I was driving from Cheadle Hulme to Manchester when I had to stop in traffic. Out of nowhere, another car hit me from behind, which pushed my car into the one in front.

    Physician: That sounds like a strong impact. Were you wearing your seatbelt?

    Patient: Yes, I always do.

    Physician: What did you feel immediately after the accident?

    Patient: At first, I was just shocked. But then I realized I had hit my head on the steering wheel, and I could feel pain in my neck and back almost right away.

    Physician: Did you seek medical attention at that time?

    Patient: Yes, I went to Moss Bank Accident and Emergency. They checked me over and said it was a whiplash injury, but they didn't do any X-rays. They just gave me some advice and sent me home.

    Physician: How did things progress after that?

    Patient: The first four weeks were rough. My neck and back pain were really bad—I had trouble sleeping and had to take painkillers regularly. It started improving after that, but I had to go through ten sessions of physiotherapy to help with the stiffness and discomfort.

    Physician: That makes sense. Are you still experiencing pain now?

    Patient: It's not constant, but I do get occasional backaches. It's nothing like before, though.

    Physician: That's good to hear. Have you noticed any other effects, like anxiety while driving or difficulty concentrating?

    Patient: No, nothing like that. I don't feel nervous driving, and I haven't had any emotional issues from the accident.

    Physician: And how has this impacted your daily life? Work, hobbies, anything like that?

    Patient: I had to take a week off work, but after that, I was back to my usual routine. It hasn't really stopped me from doing anything.

    Physician: That's encouraging. Let's go ahead and do a physical examination to check your mobility and any lingering pain.

    [Physical Examination Conducted]

    Physician: Everything looks good. Your neck and back have a full range of movement, and there's no tenderness or signs of lasting damage. Your muscles and spine seem to be in good condition.

    Patient: That's a relief!

    Physician: Yes, your recovery so far has been quite positive. Given your progress, I'd expect you to make a full recovery within six months of the accident. There are no signs of long-term damage or degeneration.

    Patient: That's great to hear. So, I don't need to worry about this affecting me in the future?

    Physician: That's right. I don't foresee any long-term impact on your work or daily life. If anything changes or you experience worsening symptoms, you can always come back for a follow-up. But at this point, you're on track for a full recovery.

    Patient: Thank you, doctor. I appreciate it.

    Physician: You're very welcome, Ms. Jones. Take care, and don't hesitate to reach out if you need anything.
    """

    print("\n🩺 PHYSICIAN NOTETAKER - AI Medical Transcription System")
    print("="*60)

    # Problem 1: Medical NER with Sequential Chains
    print_section("PROBLEM 1: Medical NER Extraction")
    ner_chain = MedicalNERChain()
    ner_result = ner_chain.process(conversation)

    if ner_result["error"]:
        print(f"\n❌ {ner_result['message']}")
    else:
        print("\n✅ Medical Conversation Validated")
        print("\n📋 Extracted Entities (JSON):")
        print(json.dumps(ner_result["data"], indent=2))

    # Problem 2: Sentiment & Intent Analysis
    print_section("PROBLEM 2: Sentiment & Intent Analysis")
    sentiment_chain = SentimentAnalysisChain()
    sentiment_result = sentiment_chain.process(conversation)

    if not sentiment_result["error"]:
        print("\n😊 Sentiment Analysis (JSON):")
        print(json.dumps(sentiment_result["data"], indent=2))

    # Problem 3: SOAP Note Generation
    print_section("PROBLEM 3: SOAP Note Generation")
    soap_chain = SOAPNoteChain()
    soap_result = soap_chain.process(conversation)

    if not soap_result["error"]:
        print("\n📝 SOAP Note (JSON):")
        print(json.dumps(soap_result["data"], indent=2))

    # Save results to file
    print_section("Saving Results")
    output = {
        "ner_extraction": ner_result,
        "sentiment_analysis": sentiment_result,
        "soap_note": soap_result
    }

    with open("output_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n✅ All results saved to 'output_results.json'")
    print("\n" + "="*60)
    print("Processing Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
