from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.summerize import generate_title, summarize_text
from core.transcriber import transcribe_all
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import built_rag_chain, ask_questions

load_dotenv()

def pipeline(source:str, language:str="english")->dict:
    print("starting AI Video Assistant")

    chunks=process_input(source)
    transcript=transcribe_all(chunks)
    print("raw transcription(first 300 characters) {transcript[:300]}")

    title= generate_title(transcript)

    summary= summarize_text(transcript)

    action_items=extract_action_items(transcript)

    key_decisions= extract_key_decisions(transcript)

    questions= extract_questions(transcript)

    rag_chain= built_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = pipeline(source, language)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_questions(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")
