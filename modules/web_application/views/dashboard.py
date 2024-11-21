from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from modules.web_application.models.models import db, ScrapedData, PromptLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    page_scraped = request.args.get('page_scraped', 1, type=int)

    page_prompts = request.args.get('page_prompts', 1, type=int)

    scraped_data_pagination = ScrapedData.query.filter_by(created_by_user_id=current_user.id).paginate(page=page_scraped, per_page=5)
    prompt_log_pagination = PromptLog.query.filter_by(created_by_user_id=current_user.id).paginate(page=page_prompts, per_page=5)
    # scraped_data_pagination = ScrapedData.query.filter_by(created_by_user_id=1).paginate(page=page_scraped, per_page=5)
    # prompt_log_pagination = PromptLog.query.filter_by(created_by_user_id=1).paginate(page=page_prompts, per_page=5)

    return render_template('dashboard.html', scraped_data_pagination=scraped_data_pagination, prompt_log_pagination=prompt_log_pagination)

@dashboard_bp.route('/scraped_data/delete/<int:id>', methods=['POST'])
@login_required
def delete_scraped_data(id):
    data = ScrapedData.query.get_or_404(id)
    if data.created_by_user_id != current_user.id:
    # if data.created_by_user_id != 1:
        flash("You are not authorized to delete this item.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    db.session.delete(data)
    db.session.commit()
    flash("Scraped data deleted successfully.", "success")
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/prompt_log/delete/<int:id>', methods=['POST'])
@login_required
def delete_prompt_log(id):
    log = PromptLog.query.get_or_404(id)
    if log.created_by_user_id != current_user.id:
    # if log.created_by_user_id != 1:
        flash("You are not authorized to delete this item.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    db.session.delete(log)
    db.session.commit()
    flash("Prompt log deleted successfully.", "success")
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/scraped_data/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_scraped_data(id):
    data = ScrapedData.query.get_or_404(id)
    if data.created_by_user_id != current_user.id:
    # if data.created_by_user_id != 1:
        flash("You are not authorized to edit this item.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        data.url = request.form['url']
        data.content = request.form['content']
        data.metadata = request.form['metadata']
        db.session.commit()
        flash("Scraped data updated successfully.", "success")
        return redirect(url_for('dashboard.dashboard'))
    return render_template('edit_scraped_data.html', data=data)

@dashboard_bp.route('/prompt_log/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prompt_log(id):
    log = PromptLog.query.get_or_404(id)
    if log.created_by_user_id != current_user.id:
    # if log.created_by_user_id != 1:
        flash("You are not authorized to edit this item.", "danger")
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        log.prompt_text = request.form['prompt_text']
        log.generated_output = request.form['generated_output']
        db.session.commit()
        flash("Prompt log updated successfully.", "success")
        return redirect(url_for('dashboard.dashboard'))
    return render_template('edit_prompt_log.html', log=log)
