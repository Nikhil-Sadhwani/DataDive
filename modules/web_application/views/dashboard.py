from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from modules.web_application.models.models import db, ScrapedData, PromptLog
from modules.web_application.forms.forms import ScrapedDataForm
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Pagination for scraped data
    page = request.args.get('page', 1, type=int)
    scraped_data_pagination = ScrapedData.query.filter_by(
        created_by_user_id=current_user.id
    ).order_by(
        ScrapedData.created_at.desc()
    ).paginate(
        page=page, 
        per_page=10  # Adjust as needed
    )

    # Pagination for prompt logs
    prompt_log_page = request.args.get('prompt_log_page', 1, type=int)
    prompt_logs_pagination = PromptLog.query.filter_by(
        created_by_user_id=current_user.id
    ).order_by(
        PromptLog.created_at.desc()
    ).paginate(
        page=prompt_log_page, 
        per_page=10  # Adjust as needed
    )

    return render_template(
        'dashboard.html', 
        scraped_data_pagination=scraped_data_pagination,
        prompt_logs_pagination=prompt_logs_pagination,
        total_prompt_logs=prompt_logs_pagination.total
    )

@dashboard_bp.route('/delete_scraped_data/<int:id>', methods=['GET'])
@login_required
def delete_scraped_data(id):
    """
    Delete a specific scraped data entry
    
    Args:
        id (int): ID of the scraped data to delete
    """
    try:
        # Find the specific scraped data entry
        scraped_data = ScrapedData.query.get_or_404(id)
        
        # Ensure the user can only delete their own data
        if scraped_data.created_by_user_id != current_user.id:
            flash('You do not have permission to delete this data.', 'danger')
            return redirect(url_for('dashboard.dashboard'))
        
        # Delete the entry
        db.session.delete(scraped_data)
        db.session.commit()
        
        # Success message
        flash('Scraped data successfully deleted.', 'success')
        
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash(f'Error deleting scraped data: {str(e)}', 'danger')
    
    # Redirect to dashboard
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/prompt_log/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_prompt_log(id):
    # Find the prompt log
    prompt_log = PromptLog.query.get_or_404(id)
    
    # Ensure the user can only delete their own prompt logs
    if prompt_log.created_by_user_id != current_user.id:
        flash('You are not authorized to delete this prompt log.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        # Delete the prompt log
        db.session.delete(prompt_log)
        db.session.commit()
        
        # Flash success message
        flash('Prompt log deleted successfully.', 'success')
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        flash(f'Error deleting prompt log: {str(e)}', 'danger')
    
    # Redirect to dashboard
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/edit_scraped_data/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_scraped_data(id):
    """
    Edit a specific scraped data entry
    
    Args:
        id (int): ID of the scraped data to edit
    """
    # Find the specific scraped data entry
    scraped_data = ScrapedData.query.get_or_404(id)
    
    # Ensure the user can only edit their own data
    if scraped_data.created_by_user_id != current_user.id:
        flash('You do not have permission to edit this data.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    # Convert metadata to string for form display if it's a dictionary
    metadata_display = (
        json.dumps(scraped_data.data_metadata, indent=2) 
        if isinstance(scraped_data.data_metadata, dict) 
        else scraped_data.data_metadata
    )
    
    # Create form with initial data
    form = ScrapedDataForm(
        url=scraped_data.url,
        content=scraped_data.content,
        metadata=metadata_display
    )
    
    # Handle form submission
    if form.validate_on_submit():
        try:
            # Update the scraped data entry
            scraped_data.url = form.url.data
            scraped_data.content = form.content.data
            
            # Try to parse metadata as JSON, fallback to original if invalid
            try:
                scraped_data.data_metadata = json.loads(form.metadata.data)
            except (json.JSONDecodeError, TypeError):
                # If parsing fails, keep the original metadata or set to None
                scraped_data.data_metadata = scraped_data.data_metadata
            
            db.session.commit()
            
            # Success message
            flash('Scraped data successfully updated.', 'success')
            return redirect(url_for('dashboard.dashboard'))
        
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            flash(f'Error updating scraped data: {str(e)}', 'danger')
    
    # Render the edit template
    return render_template(
        'edit_scraped_data.html', 
        form=form, 
        scraped_data=scraped_data
    )

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
