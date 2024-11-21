import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, redirect, url_for, flash
from modules.web_application.forms.forms import ScrapeURLForm
from modules.web_application.models.models import db, ScrapedData
from flask_login import current_user, login_required

scrape_bp = Blueprint('scrape', __name__)

@scrape_bp.route('/scrape', methods=['GET', 'POST'])
@login_required
def scrape():
    form = ScrapeURLForm()
    if form.validate_on_submit():
        url = form.url.data
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            flash(f"Error fetching URL: {e}", "danger")
            return redirect(url_for('scrape.scrape'))

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else 'No title found'
        description = soup.find('meta', {'name': 'description'})
        description = description['content'] if description else 'No description found'
        
        content = soup.get_text()

        scraped_data = ScrapedData(
            url=url,
            content=content,
            metadata=f"Title: {title}, Description: {description}",
            created_by_user_id=current_user.id
            # created_by_user_id=1
        )
        db.session.add(scraped_data)
        db.session.commit()

        flash('Scraping successful', 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('scrape.html', form=form)
