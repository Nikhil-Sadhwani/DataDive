# Flask Web Application

This is a Flask web application that supports Google OAuth login, web scraping, and prompt generation.

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**:

   - Create a PostgreSQL database.
   - Update the `config.py` file with your PostgreSQL database URI.

5. **Run database migrations**:

   ```sh
   flask db upgrade
   ```

6. **Set up environment variables**:

   - Create a `.env` file in the root directory and add the following:
     ```
     SQLALCHEMY_DATABASE_URI=your_postgresql_database_uri
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     OPENAI_API_KEY=your_api_key
     ```

7. **Run the application**:
   ```sh
   flask run
   ```

## Usage Guide

### Running the Application

1. **Start the Flask development server**:

   ```sh
   flask run
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

### Features

- **Google OAuth Login**: Users can log in using their Google account.
- **Web Scraping**: Users can input a URL to scrape content and metadata from web pages.
- **Prompt Generation**: Users can enter a prompt to receive generated responses.

## API Documentation

### Endpoints

#### 1. **Google OAuth Login**

- **Endpoint**: `/authorize/google`
- **Method**: `GET`
- **Description**: Redirects users to Google for OAuth authentication and stores user information in the database.

#### 2. **Web Scraping**

- **Endpoint**: `/scrape`
- **Method**: `POST`
- **Description**: Scrapes content and metadata from the provided URL and stores it in the database.
- **Request Data**:
  ```json
  {
    "url": "https://example.com"
  }
  ```

#### 3. **Prompt Generation**

- **Endpoint**: `/prompt`
- **Method**: `POST`
- **Description**: Generates a response based on the provided prompt and stores it in the database.
- **Request Data**:
  ```json
  {
    "prompt": "What is the capital of France?"
  }
  ```

#### 4. **Dashboard**

- **Endpoint**: `/dashboard`
- **Method**: `GET`
- **Description**: Displays a dashboard with user’s scraped URLs and prompt logs.

#### 5. **Edit Scraped Data**

- **Endpoint**: `/scraped_data/edit/<int:id>`
- **Method**: `GET`, `POST`
- **Description**: Allows users to edit their scraped data.

#### 6. **Delete Scraped Data**

- **Endpoint**: `/scraped_data/delete/<int:id>`
- **Method**: `POST`
- **Description**: Allows users to delete their scraped data.

#### 7. **Edit Prompt Log**

- **Endpoint**: `/prompt_log/edit/<int:id>`
- **Method**: `GET`, `POST`
- **Description**: Allows users to edit their prompt logs.

#### 7. **Delete Prompt Log**

- **Endpoint**: `/prompt_log/delete/<int:id>`
- **Method**: `POST`
- **Description**: Allows users to delete their prompt logs.
