from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# JWT maxfiy kalitini sozlash
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"
jwt = JWTManager(app)

# Ma'lumotlar bazasi o'rnida ishlatiladigan vaqtinchalik xotira (In-memory DB)
users_db = {}  # { username: password_hash }
products_db = [
    {"id": 1, "title": "Noutbuk", "price": 1200.0},
    {"id": 2, "title": "Smartfon", "price": 800.0},
    {"id": 3, "title": "Quloqchin", "price": 150.0}
]
carts_db = {}  # { username: [ {product_id, quantity}, ... ] }


# 1. Ro'yxatdan o'tish (Register)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username va password kiritilishi shart"}), 400

    if username in users_db:
        return jsonify({"message": "Bu foydalanuvchi nomi band"}), 400

    # Parolni xavfsiz heshlash
    users_db[username] = generate_password_hash(password)
    carts_db[username] = []  # Yangi foydalanuvchiga bo'sh savat yaratish

    return jsonify({"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"}), 201


# 2. Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_hash = users_db.get(username)

    if not user_hash or not check_password_hash(user_hash, password):
        return jsonify({"message": "Username yoki parol noto'g'ri"}), 401

    # JWT token yaratish
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


# 3. Mahsulotlar ro'yxatini olish (Ochiq endpoint)
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({"products": products_db}), 200


# 4. Savatga mahsulot qo'shish (Faqat token bilan)
@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    # Tokendan foydalanuvchi shaxsini aniqlash
    current_user = get_jwt_identity()
    data = request.get_json()

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({"message": "product_id ko'rsatilishi kerak"}), 400

    # Mahsulot mavjudligini tekshirish
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        return jsonify({"message": "Mahsulot topilmadi"}), 404

    # Savatga qo'shish
    user_cart = carts_db.setdefault(current_user, [])
    user_cart.append({
        "product_id": product_id,
        "title": product["title"],
        "price": product["price"],
        "quantity": quantity
    })

    return jsonify({
        "message": "Mahsulot savatga qo'shildi",
        "cart": user_cart
    }), 200


if __name__ == '__main__':
    app.run(debug=True)