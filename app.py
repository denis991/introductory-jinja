from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user = {
        "name": "Alice",
        "is_admin": True,
        "email": "alice@example.com",
        "join_date": "2024-01-15"
    }

    items = ["Apple", "Banana", "Cherry", "Orange", "Mango"]

    # Sample data for demonstrating Jinja features
    products = [
        {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
        {"name": "Book", "price": 19.99, "category": "Books", "in_stock": True},
        {"name": "Coffee Mug", "price": 12.50, "category": "Kitchen", "in_stock": False},
        {"name": "Headphones", "price": 89.99, "category": "Electronics", "in_stock": True},
        {"name": "Notebook", "price": 5.99, "category": "Office", "in_stock": True}
    ]

    categories = ["Electronics", "Books", "Kitchen", "Office"]

    return render_template("index.html",
                         user=user,
                         items=items,
                         products=products,
                         categories=categories)

@app.route("/about")
def about():
    team_members = [
        {"name": "Alice Johnson", "role": "Developer", "skills": ["Python", "Flask", "Jinja"]},
        {"name": "Bob Smith", "role": "Designer", "skills": ["CSS", "HTML", "UI/UX"]},
        {"name": "Carol Davis", "role": "Manager", "skills": ["Project Management", "Agile"]}
    ]

    project_stats = {
        "start_date": "2024-01-01",
        "version": "1.0.0",
        "features": ["Jinja Templates", "CSS Styling", "Flask Backend", "Responsive Design"]
    }

    return render_template("about.html",
                         team_members=team_members,
                         project_stats=project_stats)

@app.route("/products")
def products():
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True, "rating": 4.5},
        {"id": 2, "name": "Book", "price": 19.99, "category": "Books", "in_stock": True, "rating": 4.2},
        {"id": 3, "name": "Coffee Mug", "price": 12.50, "category": "Kitchen", "in_stock": False, "rating": 3.8},
        {"id": 4, "name": "Headphones", "price": 89.99, "category": "Electronics", "in_stock": True, "rating": 4.7},
        {"id": 5, "name": "Notebook", "price": 5.99, "category": "Office", "in_stock": True, "rating": 4.0},
        {"id": 6, "name": "Smartphone", "price": 699.99, "category": "Electronics", "in_stock": True, "rating": 4.6}
    ]

    return render_template("products.html", products=products)

if __name__ == "__main__":
    app.run(debug=True, port=5006)
