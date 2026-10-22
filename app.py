from flask import Flask, render_template, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("klink.db")

DEMO_BUSINESSES = [
    {"name": "Lindi's Kota Corner", "category": "Kota Shop", "area": "KwaMashu", "description": "Fresh kota combos made to order.", "price": "R", "rating": "New", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=900&q=80", "order_ahead": True, "address": "KwaMashu, Durban"},
    {"name": "Emaweni Shisanyama", "category": "Shisanyama", "area": "Umlazi", "description": "Braai favourites and a relaxed local atmosphere.", "price": "RR", "rating": "New", "image": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80", "order_ahead": True, "address": "Umlazi, Durban"},
    {"name": "Fresh Cut Barber Studio", "category": "Barbershop", "area": "Newlands East", "description": "Fades, trims and clean cuts.", "price": "R", "rating": "New", "image": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=80", "order_ahead": False, "address": "Newlands East, Durban"},
    {"name": "Thandi's Beauty Salon", "category": "Salon", "area": "KwaMashu", "description": "Hair styling, braids and beauty services.", "price": "RR", "rating": "New", "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80", "order_ahead": False, "address": "KwaMashu, Durban"},
    {"name": "Siyanda Butchery", "category": "Butchery", "area": "Inanda", "description": "Local meat cuts and braai packs.", "price": "RR", "rating": "New", "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=900&q=80", "order_ahead": False, "address": "Inanda, Durban"},
    {"name": "Corner Lounge", "category": "Tavern", "area": "KwaMashu", "description": "Find the venue, opening details and contact information.", "price": "RR", "rating": "New", "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=80", "order_ahead": False, "address": "KwaMashu, Durban"},
]

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                area TEXT NOT NULL,
                description TEXT,
                address TEXT,
                phone TEXT,
                opening_hours TEXT,
                menu_json TEXT,
                is_verified INTEGER DEFAULT 0,
                accepts_orders INTEGER DEFAULT 0
            )
        """)
        count = con.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
        if count == 0:
            con.executemany("""
                INSERT INTO businesses
                (name, category, area, description, address, accepts_orders)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (b["name"], b["category"], b["area"], b["description"], b["address"], int(b["order_ahead"]))
                for b in DEMO_BUSINESSES
            ])

@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    area = request.args.get("area", "All areas")
    businesses = DEMO_BUSINESSES
    if query:
        q = query.casefold()
        businesses = [b for b in businesses if q in " ".join([b["name"], b["category"], b["area"], b["description"]]).casefold()]
    if category != "All":
        businesses = [b for b in businesses if b["category"] == category]
    if area != "All areas":
        businesses = [b for b in businesses if b["area"] == area]
    categories = ["All", "Kota Shop", "Tavern", "Butchery", "Shisanyama", "Barbershop", "Salon"]
    areas = ["All areas", "KwaMashu", "Umlazi", "Inanda", "Newlands East"]
    return render_template("index.html", businesses=businesses, query=query, category=category, area=area,
                           categories=categories, areas=areas, total=len(DEMO_BUSINESSES))

@app.route("/business/<int:business_id>")
def business_detail(business_id):
    # Demo detail page uses the sample data until business records are fully database-driven.
    business = DEMO_BUSINESSES[business_id - 1] if 1 <= business_id <= len(DEMO_BUSINESSES) else None
    if business is None:
        return "Business not found", 404
    return render_template("business.html", business=business, business_id=business_id)

@app.route("/health")
def health():
    return {"status": "ok", "app": "K-Link"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
