# CRUD Application

A full-featured CRUD (Create, Read, Update, Delete) application built with Python Flask, SQLAlchemy, and Bootstrap. This project demonstrates implementation of all CRUD operations with a focus on business logic rather than complex UI.

## Features

- **User Authentication**: Register, login, and logout functionality
- **CRUD Operations**: Create, read, update, and delete items
- **Search Functionality**: Search items by keywords and filter by category
- **More Menu**: Additional features including About and Contact pages
- **Responsive Design**: Works on desktop and mobile devices
- **Form Validation**: Client and server-side validation
- **Flash Messages**: User feedback for actions
- **Error Handling**: Custom 404 and 500 error pages

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default, configurable)
- **Authentication**: Flask-Login, Werkzeug security
- **Forms**: Flask-WTF, WTForms

## Project Structure

```
CURD - P/
├── app.py                 # Main application file
├── models.py              # Database models
├── forms.py               # Form definitions
├── requirements.txt       # Python dependencies
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Custom CSS
│   └── js/
│       └── script.js      # Custom JavaScript
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── item_form.html     # Create/Edit item form
    ├── item_detail.html   # Item details page
    ├── search.html        # Search page
    ├── my_items.html      # User's items page
    ├── about.html         # About page
    ├── contact.html       # Contact page
    ├── 404.html           # 404 error page
    └── 500.html           # 500 error page
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository or download the source code

2. Navigate to the project directory
   ```
   cd "CURD - P"
   ```

3. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   ```

4. Activate the virtual environment
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install dependencies
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URI=sqlite:///app.db
   ```

7. Run the application
   ```
   python app.py
   ```

8. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Register a new account or login with existing credentials
2. Browse items on the home page
3. Create new items using the "Add Item" button
4. View item details by clicking on an item
5. Edit or delete your own items
6. Search for items using the search page
7. Access additional features through the "More" menu

## Development

### Database Migrations

If you make changes to the database models, you can use Flask-Migrate to update the database schema:

```
flask db init    # Only needed once
flask db migrate -m "Migration message"
flask db upgrade
```

### Environment Variables

- `SECRET_KEY`: Used for session security (required)
- `DATABASE_URI`: Database connection string (defaults to SQLite)
- `DEBUG`: Set to `True` for development, `False` for production

## License

This project is open-source and available under the MIT License.