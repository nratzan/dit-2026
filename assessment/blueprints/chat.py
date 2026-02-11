from flask import Blueprint, render_template, request, jsonify, current_app
from llm.models import get_model_info

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/')
def chat_page():
    providers = current_app.llm_registry.get_available_providers()
    return render_template('chat.html', providers=providers)


@bp.route('/api/message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']
    provider_name = data.get('provider', 'auto')
    model_id = data.get('model')
    reasoning_value = data.get('reasoning')
    conversation_history = data.get('history', [])

    # Retrieve relevant context chunks
    chunks = current_app.search_engine.search(user_message, top_k=5)
    context = "\n\n---\n\n".join(
        f"[Source: {c.get('source_file','')}, Section: {c.get('section_title','')}]\n{c['text']}"
        for c in chunks
    )

    system_prompt = (
        "You are an expert on the Design in Tech Report 2026 E-P-I-A-S x SAE Framework "
        "by John Maeda for AI upskilling product designers. Answer questions based on the "
        "following framework content. Cite specific SAE levels and EPIAS stages when relevant. "
        "Be helpful and concrete in your advice.\n\n"
        f"FRAMEWORK CONTEXT:\n{context}"
    )

    # Build reasoning_config based on the model's parameter type
    reasoning_config = None
    if model_id and reasoning_value is not None:
        info = get_model_info(model_id)
        if info:
            param_type = info.get("reasoning_param")
            if param_type == "effort":
                reasoning_config = {"effort": reasoning_value}
            elif param_type == "thinking":
                reasoning_config = {"thinking": reasoning_value}
            elif param_type == "thinking_budget":
                reasoning_config = {"thinking_budget": reasoning_value}
            elif param_type == "thinking_level":
                reasoning_config = {"thinking_level": reasoning_value}

    provider = current_app.llm_registry.get_provider(provider_name)
    response = provider.generate(
        system_prompt=system_prompt,
        messages=conversation_history + [{"role": "user", "content": user_message}],
        model=model_id,
        reasoning_config=reasoning_config,
    )

    return jsonify({
        "response": response.text,
        "provider": response.provider,
        "model": response.model,
        "latency_ms": response.latency_ms,
        "sources": [{"file": c.get('source_file',''), "section": c.get('section_title','')} for c in chunks],
    })
