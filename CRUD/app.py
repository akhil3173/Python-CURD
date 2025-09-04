from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Import models and forms
from models import db, User, Item
from forms import LoginForm, RegisterForm, ItemForm

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# CRUD operations for items
@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Item created successfully!')
        return redirect(url_for('index'))
    return render_template('item_form.html', form=form, title='New Item')

@app.route('/item/<int:item_id>')
def view_item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('You do not have permission to edit this item')
        return redirect(url_for('index'))
    
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.price = form.price.data
        item.category = form.category.data
        item.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Item updated successfully!')
        return redirect(url_for('view_item', item_id=item.id))
    return render_template('item_form.html', form=form, title='Edit Item')

@app.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('You do not have permission to delete this item')
        return redirect(url_for('index'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!')
    return redirect(url_for('index'))

# More menu options
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    
    items = Item.query
    if query:
        items = items.filter(Item.title.contains(query) | Item.description.contains(query))
    if category and category != 'all':
        items = items.filter(Item.category == category)
    
    items = items.all()
    return render_template('search.html', items=items, query=query, category=category)

@app.route('/my_items')
@login_required
def my_items():
    items = Item.query.filter_by(user_id=current_user.id).all()
    return render_template('my_items.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)