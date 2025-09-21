from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PRODUCTS = [
    {
        'id': 1,
        'name': 'Handmade Basket',
        'desc': 'Eco-friendly bamboo basket.',
        'img': 'https://th.bing.com/th/id/OIP.gr-6p2EdXE-l7eu23AM3gQHaKz?w=125&h=182&c=7&r=0&o=5&dpr=1.1&pid=1.7',
        'category': 'Home Decor',
        'owner': 'admin'
    },
    {
        'id': 2,
        'name': 'Clay Pot',
        'desc': 'Traditional handcrafted clay pot.',
        'img': 'https://i.etsystatic.com/52484195/r/il/5f26ff/6060935998/il_1080xN.6060935998_jf0f.jpg',
        'category': 'Kitchenware',
        'owner': 'admin'
    }
]
USERS = []

STYLE = '''
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
body {font-family:'Roboto',sans-serif;margin:0;background:#f5f5f5;color:#333;}
header {background:#8B4513;color:white;padding:20px;text-align:center;position:sticky;top:0;z-index:100;}
.container {max-width:950px;margin:20px auto;background:white;padding:20px;border-radius:12px;}
h2{text-align:center;color:#8B4513;margin-bottom:15px;}
input, textarea, select, button {width:100%;padding:10px;margin:5px 0;border-radius:6px;border:1px solid #ccc;font-size:1rem;}
button {background:#8B4513;color:white;font-weight:bold;cursor:pointer;transition:0.3s;}
button:hover {background:#A0522D;}
.product-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:15px;}
.card {border:1px solid #ddd;padding:10px;border-radius:10px;background:#fffaf0;transition:transform 0.2s;}
.card:hover {transform:scale(1.02);}
.card img {width:100%;height:180px;object-fit:cover;border-radius:8px;margin-bottom:8px;}
.product-actions {display:flex;justify-content:space-between;flex-wrap:wrap;}
nav {display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:15px;}
.input-group {
    position: relative;
    gap: 10px;
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    width: 100%;
}
input[type="text"], input[type="email"], input[type="password"] {
    padding-right: 2.5em;
    margin: 0;
    width: 100%;
    box-sizing: border-box;
    min-height: 40px;
}
.mic-btn {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    background: none;
    border: none;
    outline: none;
    font-size: 1.2em;
    cursor: pointer;
    color: #8B4513;
    padding: 0;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
form { margin-bottom: 0; }
.mic-btn.active { color: #FFD700; }
input[type="text"], input[type="email"], input[type="password"] {padding-right: 2.2em;}
.back-btn {
    background: #ccc;
    color: #333;
    font-weight: normal;
    margin-right: 12px;
    padding: 4px 12px;
    font-size: 0.92em;
    border-radius: 20px;
    position: absolute;
    left: 10px;
    top: 25px;
    width: auto;
    min-width: 38px;
    height: 28px;
    box-shadow: none;
}
.back-btn:hover {
    background: #bbb;
}
.nav-back-wrapper {
    position: relative;
    min-height: 38px;
    margin-bottom: 7px;
}
</style>
'''

INTRO = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Handmade Marketplace</title>
''' + STYLE + '''
</head>
<body>
<header>
<h1>AI Handmade Marketplace</h1>
<p>Fair Trade • Authentic • Local • AI Powered</p>
</header>
<div class="container" style="background: url('https://img.freepik.com/premium-photo/pottery-making-artisan-woman-cooking-crafts-person-village-woman-culture-india-indian-woman_569725-10656.jpg') center/cover no-repeat, white;
                             min-height: 320px; 
                             display: flex; 
                             flex-direction: column; 
                             align-items: center; 
                             justify-content: center; 
                             position: relative;">
  <div style="background:rgba(255,255,255,0.32);padding:24px 18px;border-radius:12px;box-shadow:0 1px 13px 0 #963c;">
    <h2 style="margin-bottom:18px;">Welcome to AI Handmade Marketplace</h2>
    <div style="display:flex; flex-direction:column; gap:12px;">
        <a href="{{ url_for('register') }}"><button>Register</button></a>
        <a href="{{ url_for('login') }}"><button>Login</button></a>
    </div>
  </div>
</div>

</body>
</html>
'''

REGISTER = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Register</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
<h2>Register</h2>
<form method="post" autocomplete="off">
    <div class="input-group">
        <input type="text" id="name" name="name" placeholder="Your Name" required aria-label="Name">
        <button type="button" class="mic-btn" aria-label="Speak name" onclick="startRecording('name', this)" tabindex="-1" title="Record Name">🎤</button>
    </div>
    <div class="input-group">
        <input type="email" id="email" name="email" placeholder="Email" required aria-label="Email">
        <button type="button" class="mic-btn" aria-label="Speak email" onclick="startRecording('email', this)" tabindex="-1" title="Record Email">🎤</button>
    </div>
    <div class="input-group">
        <input type="password" id="password" name="password" placeholder="Password" required aria-label="Password">
        <button type="button" class="mic-btn" aria-label="Speak password" onclick="startRecording('password', this)" tabindex="-1" title="Record Password">🎤</button>
    </div>
    <button type="submit">Register</button>
</form>
<p id="voiceFeedback"></p>
<p style="color:red;">{{ message }}</p>
</div>
<script>
function startRecording(inputId, btn) {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.getElementById('voiceFeedback').innerText = "Sorry, your browser doesn't support Speech Recognition.";
        return;
    }
    if(window._recognition && window._recognition.active) {
        window._recognition.stop();
        return;
    }
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
    window._recognition = recognition;
    recognition.lang = 'en-US';
    recognition.onstart = function() {
        btn.classList.add('active');
        document.getElementById('voiceFeedback').innerText = "Listening... Please speak for " + inputId + ".";
        recognition.active = true;
    };
    recognition.onspeechend = function() {
        recognition.stop();
        btn.classList.remove('active');
        document.getElementById('voiceFeedback').innerText = "Processing...";
        recognition.active = false;
    };
    recognition.onerror = function(event) {
        btn.classList.remove('active');
        document.getElementById('voiceFeedback').innerText = "Sorry, couldn't capture voice. Try again.";
        recognition.active = false;
    };
    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        let input = document.getElementById(inputId);
        if (document.activeElement === input && typeof input.selectionStart === "number") {
            let start = input.selectionStart, end = input.selectionEnd;
            let text = input.value;
            input.value = text.slice(0, start) + transcript + text.slice(end);
            input.selectionStart = input.selectionEnd = start + transcript.length;
        } else {
            input.value = transcript;
    }
        document.getElementById('voiceFeedback').innerText = "Captured for " + inputId + ": " + transcript;
        btn.classList.remove('active');
        recognition.active = false;
    };
    recognition.start();
}
</script>
</body>
</html>
'''


# For navs with back button
NAV_BACK = '''
<div class="nav-back-wrapper">
    <a href="{{ url_for('dashboard') }}">
        <button class="back-btn">&larr; Back</button>
    </a>
</div>
'''

DASHBOARD = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Dashboard</title>
''' + STYLE + '''
<style>
.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
}
.dashboard-header {
  text-align: center;
  margin-bottom: 12px;
}
.dashboard-nav-row {
  display: flex;
  justify-content: center;
  gap: 18px;
  margin: 24px 0 28px 0;
  flex-wrap: wrap;
}
.carousel-outer {
  width: 340px;
  height: 180px;
  overflow: hidden;
  position: relative;
  margin-bottom: 34px;
  border-radius: 20px;
  background: #e0e0e0;
  box-shadow: 0 2px 16px #8B451326;
  display: flex;
  align-items: center;
  justify-content: center;
}
.carousel-img {
  width: 340px;
  height: 180px;
  object-fit: cover;
  position: absolute;
  left: 0; top: 0;
  opacity: 0;
  transition: opacity 0.8s;
  border-radius: 20px;
}
.carousel-img.active {
  opacity: 1;
  z-index: 2;
}
.about-section {
  margin-top: 22px;
  padding: 30px 28px;
  background: #fffbe8;
  border-radius: 13px;
  box-shadow: 0 2px 13px #f6deba22;
  max-width: 620px;
  color: #60350A;
}
.about-section h3 {
  margin-top: 0;
  color: #8B4513;
  font-weight: bold;
}
@media (max-width: 900px) {
  .carousel-outer { width: 98vw; height: 36vw; min-height:120px; max-width: 96vw; }
  .carousel-img { width: 98vw; height: 36vw; min-height:120px; max-width:96vw;}
  .about-section { padding:16px 10px; }
}
</style>
</head>
<body>
<header>
<h1>AI Handmade Marketplace</h1>
</header>
<div class="dashboard-container">
  <div class="dashboard-header">
    <p>Welcome, <strong>{{ current_user }}</strong></p>
  </div>
  <div class="dashboard-nav-row">
    <a href="{{ url_for('explore') }}"><button>Explore Products</button></a>
    <a href="{{ url_for('sell') }}"><button>Sell Product</button></a>
    <a href="{{ url_for('my_products') }}"><button>My Products</button></a>
    <a href="{{ url_for('cart') }}"><button>My Cart</button></a>
    <a href="{{ url_for('logout') }}"><button>Logout</button></a>
  </div>
  <div class="carousel-outer">
    <img src="https://th.bing.com/th/id/OIP.HtUs2JVUBvwnWOv6vIQMSwHaEO?w=298&h=180&c=7&r=0&o=5&dpr=1.1&pid=1.7" class="carousel-img active"/>
    <img src="https://img.freepik.com/premium-photo/exquisite-handmade-crafts-local-artisan-marke_1022456-145149.jpg" class="carousel-img"/>
    <img src="https://static.vecteezy.com/system/resources/previews/025/431/017/non_2x/artisan-crafts-ai-generated-free-photo.jpg" class="carousel-img"/>
  </div>
  <div class="about-section">
    <h3>About Artisans</h3>
    <p>
      Artisans form the foundation of our community, demonstrating exceptional skill, creativity, and a commitment to quality in every piece they create. By supporting our platform, you empower local talent, preserve cultural traditions, and invest in genuine craftsmanship. Every product is a testament to artistry and dedication—thank you for supporting and valuing the work of artisans.
    </p>
  </div>
</div>
<script>
// Simple one-at-a-time carousel
const images = document.querySelectorAll('.carousel-img');
let idx = 0;
setInterval(()=> {
  images[idx].classList.remove('active');
  idx = (idx+1)%images.length;
  images[idx].classList.add('active');
}, 2800);
</script>
</body>
</html>
'''

EXPLORE = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Explore Products</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
''' + NAV_BACK + '''
<h2>Explore Products</h2>
<form method="post" style="margin-bottom:15px;">
    <input type="text" name="search" placeholder="Search..." value="">
    <button type="submit">Search</button>
</form>
<div class="product-grid">
{% for p in products %}
<div class="card">
    <img src="{{ p.img }}">
    <h3>{{ p.name }}</h3>
    <p>{{ p.desc }}</p>
    <small>Category: {{ p.category }}</small>
    <div class="product-actions">
        <a href="{{ url_for('add_to_cart', pid=p.id) }}"><button>Add to Cart</button></a>
    </div>
</div>
{% endfor %}
{% if not products %}
<p>No products found.</p>
{% endif %}
</div>
</div>
</body>
</html>
'''

CART = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Cart</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
''' + NAV_BACK + '''
<h2>My Cart</h2>
<div class="product-grid">
{% for p in products %}
<div class="card">
    <img src="{{ p.img }}">
    <h3>{{ p.name }}</h3>
    <p>{{ p.desc }}</p>
</div>
{% endfor %}
{% if not products %}
<p>Cart empty</p>
{% endif %}
</div>
</div>
</body>
</html>
'''

SELL = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Sell Product</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
''' + NAV_BACK + '''
<h2>Sell Your Product</h2>
<form method="post" enctype="multipart/form-data">
    <input type="text" name="pname" placeholder="Product Name" required>
    <input type="text" name="pcat" placeholder="Category" required>
    <textarea name="pdesc" placeholder="Description" required></textarea>
    <input type="file" name="pfile" accept="image/*" required>
    <button type="submit">Add Product</button>
</form>
<p style="color:red;">{{ message }}</p>
</div>
</body>
</html>
'''

MY_PRODUCTS = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>My Products</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
''' + NAV_BACK + '''
<h2>My Products</h2>
<div class="product-grid">
{% for p in products %}
<div class="card">
    <img src="{{ p.img }}">
    <h3>{{ p.name }}</h3>
    <p>{{ p.desc }}</p>
</div>
{% endfor %}
{% if not products %}
<p>No products</p>
{% endif %}
</div>
</div>
</body>
</html>
'''

LOGIN = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Login</title>
''' + STYLE + '''
</head>
<body>
<header><h1>AI Handmade Marketplace</h1></header>
<div class="container">
<h2>Login</h2>
<form method="post">
    <input type="email" name="email" placeholder="Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>
<p style="color:red;">{{ message }}</p>
</div>
</body>
</html>
'''

@app.route('/')
def intro():
    return render_template_string(INTRO)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        if not name or not email or not password:
            message = "Fill all fields"
        elif any(u['email'] == email for u in USERS):
            message = "Email already registered"
        else:
            USERS.append({'name': name, 'email': email, 'password': password})
            message = "Registered! Login now."
            return redirect(url_for('login'))
    return render_template_string(REGISTER, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        user = next((u for u in USERS if u['email'] == email and u['password'] == password), None)
        if user:
            session['current_user'] = user['name']
            session['cart'] = []
            return redirect(url_for('dashboard'))
        else:
            message = "Invalid credentials!"
    return render_template_string(LOGIN, message=message)

@app.route('/dashboard')
def dashboard():
    if 'current_user' not in session:
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD, current_user=session['current_user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('intro'))

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    query = request.form.get("search", "").lower() if request.method == "POST" else ""
    if query:
        products = [p for p in PRODUCTS if query in p['name'].lower()]
    else:
        products = PRODUCTS
    return render_template_string(EXPLORE, products=products)

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'cart' not in session:
        session['cart'] = []
    if pid not in session['cart']:
        session['cart'].append(pid)
        flash("Added to cart")
    else:
        flash("Already in cart")
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    cart_products = [p for p in PRODUCTS if p['id'] in session['cart']]
    return render_template_string(CART, products=cart_products)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    message = ''
    if request.method == 'POST':
        name = request.form["pname"]
        cat = request.form["pcat"]
        desc = request.form["pdesc"]
        file = request.files.get("pfile")
        if not name or not cat or not desc or not file:
            message = "Fill all fields and upload image"
        else:
            data = file.read()
            img_data = "data:image/jpeg;base64," + base64.b64encode(data).decode()
            new_id = max([p["id"] for p in PRODUCTS], default=0) + 1
            PRODUCTS.append({'id': new_id, 'name': name, 'desc': desc, 'img': img_data,
                             'category': cat, 'owner': session.get('current_user', 'admin')})
            message = "Product added!"
            return redirect(url_for('dashboard'))
    return render_template_string(SELL, message=message)

@app.route('/my_products')
def my_products():
    owner = session.get('current_user', None)
    my_prods = [p for p in PRODUCTS if p['owner'] == owner]
    return render_template_string(MY_PRODUCTS, products=my_prods)

if __name__ == "__main__":
    app.run(debug=True)
