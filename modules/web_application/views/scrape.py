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
    scraped_data = None
    
    if form.validate_on_submit():
        url = form.url.data
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            flash(f"Error fetching URL: {e}", "danger")
            return redirect(url_for('scrape.scrape'))

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Enhanced metadata extraction
        title = soup.title.string if soup.title else 'No title found'
        description_tag = soup.find('meta', {'name': 'description'})
        description = description_tag['content'] if description_tag else 'No description found'
        
        # Extract content
        content = soup.get_text(strip=True, separator=' ')
        
        # Truncate content if too long
        content = content[:10000] if len(content) > 10000 else content

        # Prepare metadata as a dictionary
        data_metadata = {
            'title': title,
            'description': description,
            'url': url,
            'content_length': len(content)
        }
        
        # Create ScrapedData entry
        scraped_data = ScrapedData(
            url=url,
            content=content,
            data_metadata=data_metadata,
            created_by_user_id=current_user.id
        )
        db.session.add(scraped_data)
        db.session.commit()

        flash('Scraping successful', 'success')
    
    return render_template('scrape.html', form=form, scraped_data=scraped_data)
