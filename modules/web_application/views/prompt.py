from flask import Blueprint, jsonify, render_template, redirect, url_for, flash
from modules.web_application.forms.forms import PromptForm
from modules.web_application.models.models import db, PromptLog
from flask_login import current_user, login_required
import os
from langchain_google_genai import ChatGoogleGenerativeAI

prompt_bp = Blueprint('prompt', __name__)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("OPENAI_API_KEY"),
)

@prompt_bp.route('/prompt', methods=['GET', 'POST'])
@login_required
def handle_prompt():
    form = PromptForm()
    if form.validate_on_submit():
        prompt_text = form.prompt_text.data

        if not prompt_text:
            return jsonify({"error": "Prompt text is required"}), 400

        messages = [
            (
                "system",
                "You are a helpful assistant that responds to user questions or statements.",
            ),
            ("human", prompt_text),
        ]
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        tokens_used = len(prompt_text.split()) + len(response.split())

        prompt_log = PromptLog(
            prompt_text=prompt_text,
            generated_output=response,
            created_by_user_id=current_user.id,
            # created_by_user_id=1,
            tokens_used=tokens_used
        )
        db.session.add(prompt_log)
        db.session.commit()

        flash('Resonse generated successful', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('prompt.html', form=form)
