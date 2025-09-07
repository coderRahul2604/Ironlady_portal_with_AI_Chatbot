from django.shortcuts import render

# Create your views here.

import os, json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import FAQ, ChatMessage

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

def chat_page(request):
    # pass top FAQs so the UI can show quick questions
    top_faqs = FAQ.objects.all()[:8]
    return render(request, 'chatbot/chat.html', {'faqs': top_faqs})

@require_POST
def ask(request):
    """
    Receives JSON: { "question": "..." }
    Returns JSON: { "answer": "...", "source": "faq" | "ai" | "notfound" }
    """
    data = json.loads(request.body.decode('utf-8'))
    question = data.get('question', '').strip()
    if not question:
        return JsonResponse({"answer":"Please type a question.","source":"error"})

    # 1) Try match against FAQ (simple fuzzy match: question text or keywords)
    q_lower = question.lower()
    faqs = FAQ.objects.all()
    for f in faqs:
        if f.keywords:
            kw_list = [k.strip().lower() for k in f.keywords.split(',')]
            if any(kw in q_lower for kw in kw_list):
                ChatMessage.objects.create(user_message=question, bot_response=f.answer)
                return JsonResponse({"answer": f.answer, "source": "faq"})
        if f.question.lower() in q_lower or q_lower in f.question.lower():
            ChatMessage.objects.create(user_message=question, bot_response=f.answer)
            return JsonResponse({"answer": f.answer, "source": "faq"})

    # 2) If OpenAI key configured, use it as fallback
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            prompt = f"You are Iron Lady helpdesk assistant. Answer concisely:\n\nQ: {question}\nA:"
            resp = openai.Completion.create(
                engine="text-davinci-003", prompt=prompt, max_tokens=300, temperature=0.3
            )
            answer = resp.choices[0].text.strip()
            ChatMessage.objects.create(user_message=question, bot_response=answer)
            return JsonResponse({"answer": answer, "source": "ai"})
        except Exception as e:
            # avoid exposing raw exceptions in production
            return JsonResponse({"answer": "Sorry — I couldn't reach AI service right now.", "source":"error"})
    # 3) No answer found
    return JsonResponse({"answer": "I couldn't find an exact answer. Try another question or contact support at careers@iamironlady.com", "source":"notfound"})
