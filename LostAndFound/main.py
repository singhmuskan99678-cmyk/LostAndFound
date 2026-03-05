from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import os
from database import get_db
from models import User, LostItem, FoundItem

app = FastAPI(title="Lost & Found System")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class UserCreate(BaseModel):
    name: str
    email: str
    mobile: str
    password: str

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = '''<!DOCTYPE html>
<html><head><title>Lost & Found</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;}
.container{background:rgba(255,255,255,0.95);padding:40px;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,0.1);max-width:400px;width:90%;text-align:center;}
h1{color:#333;margin-bottom:30px;background:linear-gradient(45deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5em;}
input{width:100%;padding:15px;margin:10px 0;border:1px solid #ddd;border-radius:10px;font-size:16px;box-sizing:border-box;}
button{width:100%;padding:15px;background:linear-gradient(45deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;font-size:16px;cursor:pointer;margin:10px 0;}
button:hover{transform:translateY(-2px);}.switch{margin-top:20px;}.switch a{color:#667eea;text-decoration:none;font-weight:bold;}</style></head>
<body><div class="container"><h1>🔍 Lost & Found</h1><form id="loginForm"><h3>Login</h3><input type="email" id="login_email" placeholder="Email" required><input type="password" id="login_password" placeholder="Password" required><button type="button" onclick="login()">Login</button></form>
<form id="signupForm" style="display:none;"><h3>Sign Up</h3><input type="text" id="signup_name" placeholder="Full Name" required><input type="email" id="signup_email" placeholder="Email" required><input type="tel" id="signup_mobile" placeholder="Mobile" required><input type="password" id="signup_password" placeholder="Password" required><button type="button" onclick="signup()">Sign Up</button></form>
<div class="switch"><a href="#" onclick="toggleForm()">Don't have account? Sign Up</a></div></div>
<script>function toggleForm(){document.getElementById('loginForm').style.display=document.getElementById('loginForm').style.display==='none'?'block':'none';document.getElementById('signupForm').style.display=document.getElementById('signupForm').style.display==='none'?'block':'none';}
async function login(){const email=document.getElementById('login_email').value;const password=document.getElementById('login_password').value;const response=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});const result=await response.json();if(response.ok){localStorage.setItem('token','logged-in');alert('Login successful!');window.location.href='/dashboard';}else{alert('Login failed!');}}
async function signup(){const data={name:document.getElementById('signup_name').value,email:document.getElementById('signup_email').value,mobile:document.getElementById('signup_mobile').value,password:document.getElementById('signup_password').value};const response=await fetch('/api/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const result=await response.json();alert(result.message||result.detail);}</script></body></html>'''
    return HTMLResponse(html_content)

@app.post("/api/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.email == user.email) | (User.mobile == user.mobile)).first()
    if existing: raise HTTPException(status_code=400, detail="User already exists!")
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(name=user.name, email=user.email, mobile=user.mobile, password=hashed_pw)
    db.add(db_user); db.commit(); db.refresh(db_user)
    return {"message": "Signup successful! Please login."}

@app.post("/api/login")
async def login(user_data: dict, db: Session = Depends(get_db)):
    email = user_data.get("email"); password = user_data.get("password")
    if not email or not password: raise HTTPException(status_code=400, detail="Email and password required!")
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    user = db.query(User).filter(User.email == email, User.password == hashed_pw).first()
    if not user: raise HTTPException(status_code=400, detail="Invalid credentials!")
    return {"token": "fake-jwt-token", "user_id": user.id, "name": user.name}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return HTMLResponse('''<!DOCTYPE html>
<html><head><title>Dashboard</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);margin:0;padding:20px;min-height:100vh;}
.container{max-width:1200px;margin:0 auto;background:white;border-radius:20px;padding:30px;box-shadow:0 20px 40px rgba(0,0,0,0.1);position:relative;}
h1{text-align:center;color:#333;background:linear-gradient(45deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.5em;margin-bottom:40px;}
.options{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin:30px 0;}
.card{background:#f8f9fa;padding:30px;border-radius:15px;text-align:center;cursor:pointer;transition:all 0.3s;border:3px solid transparent;}
.card:hover{transform:translateY(-5px);box-shadow:0 15px 30px rgba(0,0,0,0.2);border-color:#667eea;}
.card h3{color:#333;margin-bottom:10px;font-size:1.5em;}
.logout{position:absolute;top:20px;right:20px;background:#ff6b6b;color:white;padding:10px 20px;border-radius:20px;text-decoration:none;}
form{background:#f8f9fa;padding:25px;border-radius:15px;margin:20px 0;display:none;}
input,textarea,select{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:8px;box-sizing:border-box;}
button{background:linear-gradient(45deg,#667eea,#764ba2);color:white;padding:15px;border:none;border-radius:25px;cursor:pointer;font-size:16px;width:100%;margin-top:10px;}
.delete-btn{background:#ff4757!important;width:auto!important;padding:8px 16px!important;font-size:14px!important;margin:5px;}
#historyList{padding:20px;}
.history-item{background:white;margin:10px 0;padding:20px;border-radius:10px;box-shadow:0 5px 15px rgba(0,0,0,0.1);border-left:5px solid #667eea;display:flex;align-items:flex-start;}
.history-img{width:80px;height:80px;object-fit:cover;border-radius:8px;margin-right:15px;border:2px solid #667eea;}
.history-content{flex:1;}
.history-item h4{margin:0 0 10px 0;color:#333;}
.history-item p{margin:5px 0;font-size:14px;}
.history-actions{text-align:right;}</style></head>
<body><div class="container">
<a href="/" class="logout" onclick="localStorage.removeItem('token')">Logout</a><h1>📱 Dashboard</h1>
<div class="options">
<div class="card" onclick="showForm('lost')"><h3>🚫 Report Lost</h3><p>Report lost item</p></div>
<div class="card" onclick="showForm('found')"><h3>✅ Report Found</h3><p>Report found item</p></div>
<div class="card" onclick="showHistory()"><h3>📋 History</h3><p>View history</p></div></div>

<form id="lostForm"><h3>🚫 Report Lost Item</h3>
<input type="text" id="lost_title" placeholder="Item name *" required>
<select id="lost_category" onchange="toggleOther('lost')"><option value="">Select Category *</option><option value="Electronics">Electronics</option><option value="Documents">Documents</option><option value="Stationary">Stationary</option><option value="Clothing">Clothing</option><option value="Books">Books</option><option value="other">Other...</option></select>
<input type="text" id="lost_category_other" placeholder="Enter other category..." style="display:none;">
<input type="text" id="lost_location" placeholder="Location *" required>
<textarea id="lost_desc" placeholder="Description"></textarea>
<input type="tel" id="lost_contact" placeholder="Contact *" required>
<input type="file" id="lost_image" accept="image/*">
<button onclick="submitLost()">🚫 Submit Lost</button></form>

<form id="foundForm"><h3>✅ Report Found Item</h3>
<input type="text" id="found_title" placeholder="Item name *" required>
<select id="found_category" onchange="toggleOther('found')"><option value="">Select Category *</option><option value="Electronics">Electronics</option><option value="Documents">Documents</option><option value="Stationary">Stationary</option><option value="Clothing">Clothing</option><option value="Books">Books</option><option value="other">Other...</option></select>
<input type="text" id="found_category_other" placeholder="Enter other category..." style="display:none;">
<input type="text" id="found_location" placeholder="Location *" required>
<textarea id="found_desc" placeholder="Description"></textarea>
<input type="tel" id="found_contact" placeholder="Contact *" required>
<input type="file" id="found_image" accept="image/*">
<button onclick="submitFound()">✅ Submit Found</button></form>

<div id="history" style="display:none;"><h3>📋 Your History</h3><div id="historyList">Click History to load...</div></div></div>

<script>let historyData=JSON.parse(localStorage.getItem('historyData'))||[];
function toggleOther(type){const sel=document.getElementById(type+'_category'),other=document.getElementById(type+'_category_other');other.style.display=sel.value==='other'?'block':'none';other.required=sel.value==='other';}
function showForm(t){document.querySelectorAll('form,#history').forEach(el=>el.style.display='none');document.getElementById(t+'Form').style.display='block';}
function showHistory(){document.querySelectorAll('form,#history').forEach(el=>el.style.display='none');document.getElementById('history').style.display='block';loadHistory();}
function submitLost(){
const catSel=document.getElementById('lost_category'),catOther=document.getElementById('lost_category_other'),category=catSel.value==='other'?catOther.value:catSel.value;
const item={id:Date.now(),title:document.getElementById('lost_title').value,category,location:document.getElementById('lost_location').value,desc:document.getElementById('lost_desc').value,contact:document.getElementById('lost_contact').value,type:'lost',image:document.getElementById('lost_image').files[0]?URL.createObjectURL(document.getElementById('lost_image').files[0]):'https://via.placeholder.com/80?text=No+Image',date:new Date().toLocaleDateString('en-GB')};
if(!item.title||!item.location||!item.contact||!item.category){alert('Fill all required fields!');return;}
historyData.unshift(item);localStorage.setItem('historyData',JSON.stringify(historyData));alert('✅ Lost item added!');document.getElementById('lostForm').reset();toggleOther('lost');showHistory();}
function submitFound(){
const catSel=document.getElementById('found_category'),catOther=document.getElementById('found_category_other'),category=catSel.value==='other'?catOther.value:catSel.value;
const item={id:Date.now(),title:document.getElementById('found_title').value,category,location:document.getElementById('found_location').value,desc:document.getElementById('found_desc').value,contact:document.getElementById('found_contact').value,type:'found',image:document.getElementById('found_image').files[0]?URL.createObjectURL(document.getElementById('found_image').files[0]):'https://via.placeholder.com/80?text=No+Image',date:new Date().toLocaleDateString('en-GB')};
if(!item.title||!item.location||!item.contact||!item.category){alert('Fill all required fields!');return;}
historyData.unshift(item);localStorage.setItem('historyData',JSON.stringify(historyData));alert('✅ Found item added!');document.getElementById('foundForm').reset();toggleOther('found');showHistory();}
function deleteItem(id){if(confirm('Delete this item?')){historyData=historyData.filter(item=>item.id!=id);localStorage.setItem('historyData',JSON.stringify(historyData));loadHistory();}}
function loadHistory(){const list=document.getElementById('historyList');if(historyData.length===0){list.innerHTML='<p>No history found. Add some items!</p>';return;}
list.innerHTML=historyData.map(item=>`<div class="history-item"><img src="${item.image}" alt="${item.title}" onerror="this.src='https://via.placeholder.com/80?text=No+Image'" class="history-img"><div class="history-content"><h4>${item.title}</h4><p><strong>${item.type.toUpperCase()}</strong> • ${item.category} • ${item.location} • ${item.date}</p><p>${item.desc||'No description'}</p><p><strong>Contact:</strong> ${item.contact}</p></div><div class="history-actions"><button class="delete-btn" onclick="deleteItem(${item.id})">🗑️ Delete</button></div></div>`).join('');}</script></body></html>''')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
