# 1. AI & Database Setup
try:
    nlp = spacy.load("en_core_web_sm")
    print("--- AI ENGINE: ONLINE ---")
except:
    print("--- AI ERROR: Run 'python3 -m spacy download en_core_web_sm' ---")

def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_res TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("--- DATABASE INITIALIZED ---")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("message", "")
    
    # 2. AI Processing (Intent Recognition)
    doc = nlp(user_input)
    tokens = [token.lemma_.lower() for token in doc]
    print(f"Tokens: {tokens}") # See the 'brain' working in the terminal

    if "status" in tokens:
        response = "Industrial Status: All systems nominal. Database logging active."
    elif ("turn" in tokens or "activate" in tokens) and "on" in tokens:
        response = "Command Accepted: Activating hardware light."
    elif "hello" in tokens or "hi" in tokens:
        response = "Broadino System Online. Ready for commands."
    else:
        response = f"Analyzed: {user_input}. No hardware intent found."

    # 3. Log to Database (The 'Data Integrity' Requirement)
    try:
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_msg, bot_res) VALUES (?, ?)", (user_input, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

    return jsonify({"response": response})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
