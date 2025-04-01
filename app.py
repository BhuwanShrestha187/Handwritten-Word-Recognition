from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
import sqlite3
import secrets
import uuid
import datetime
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from vision_api import extract_text
from translate_api import translate_text
from summarize_api import summarize_text
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["LOGS_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_logs")

# Create logs directory if it doesn't exist
if not os.path.exists(app.config["LOGS_FOLDER"]):
    os.makedirs(app.config["LOGS_FOLDER"])

# Function to log user activities
def log_user_activity(user_id, activity, details=None):
    """Log user activity to a file"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = os.path.join(app.config["LOGS_FOLDER"], f"{user_id}_log.txt")
        
        with open(log_file, "a") as f:
            log_entry = f"{timestamp} - {activity}"
            if details:
                log_entry += f" - {details}"
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error logging activity: {e}")

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = ""

# Google OAuth setup (placeholder)
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your Google Client ID
client = WebApplicationClient(GOOGLE_CLIENT_ID)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        if "files" not in request.files:
            return "No files uploaded!"

        files = request.files.getlist("files")
        results = []
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                extracted_text = extract_text(filepath)
                formatted_text = ' '.join(extracted_text.split()).replace('. ', '. ')
                results.append({"image": filename, "text": formatted_text})
                c.execute("INSERT INTO history (user_id, image, text) VALUES (?, ?, ?)",
                          (current_user.id, filename, formatted_text))
                
                # Log this activity
                log_user_activity(current_user.id, "OCR Performed", f"File: {filename}")
        conn.commit()
        conn.close()
        return render_template("result.html", results=results)
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
@login_required
def translate():
    text = request.form.get("text")
    target_lang = request.form.get("language")
    translated_text = translate_text(text, target_lang)
    
    # Log this activity
    log_user_activity(current_user.id, "Translation", f"Language: {target_lang}")
    
    return translated_text

@app.route("/summarize", methods=["POST"])
@login_required
def summarize():
    text = request.form["text"]
    summary = summarize_text(text)
    
    # Log this activity
    log_user_activity(current_user.id, "Summarization")
    
    return summary

@app.route("/download", methods=["POST"])
@login_required
def download():
    text = request.form["text"]
    filename = request.form["filename"]
    format = request.form["format"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.{format}")
    text = text.replace('<br>', '\n').replace('</p><p>', '\n').replace('<p>', '').replace('</p>', '\n')
    if format == "docx":
        doc = Document()
        doc.add_paragraph(text)
        doc.save(filepath)
    elif format == "pdf":
        pdf = SimpleDocTemplate(filepath, pagesize=letter)
        pdf.build([Paragraph(text)])
    else:  # txt
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(text)
    
    # Log this activity
    log_user_activity(current_user.id, "File Downloaded", f"Format: {format}, Filename: {filename}")
    
    return send_file(filepath, as_attachment=True)

@app.route("/feedback", methods=["POST"])
def feedback():
    # Get the form data
    name = request.json.get("name")
    email = request.json.get("email")
    message = request.json.get("message")
    
    success = True
    error_message = ""
    email_sent = False
    
    # Try to send email
    try:
        # Email credentials - Using secondary email to send to primary email
        secondary_email = "handwrittensender@gmail.com"  # Secondary email address
        secondary_app_password = "ymribhdrhrbsymls"  # App password without spaces (ymri bhdr hrbs ymls)
        recipient_email = "handwrittenocr448@gmail.com"  # Primary email that will receive
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = secondary_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Contact Form: Message from {name}"
        msg['Reply-To'] = email  # Set reply-to as the user's email
        
        # Email body
        body = f"""
        New message from contact form:
        
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server using SSL instead of STARTTLS
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            # Login with secondary email credentials
            server.login(secondary_email, secondary_app_password)
            server.send_message(msg)
            
            email_sent = True
            print(f"Email sent successfully from {secondary_email} to {recipient_email}")
            
        # Log this activity if user is logged in
        if current_user.is_authenticated:
            log_user_activity(current_user.id, "Contact Form Submitted", f"Email: {email}")
            
    except smtplib.SMTPAuthenticationError as auth_err:
        print(f"SMTP Authentication Error: {auth_err}")
        print("This means the app password or email is incorrect.")
        success = False
        error_message = "Failed to send your message. Authentication error."
        
    except smtplib.SMTPException as smtp_err:
        print(f"SMTP Error: {smtp_err}")
        print("This is a general SMTP error.")
        success = False
        error_message = "Failed to send your message. SMTP error."
        
    except ConnectionRefusedError as conn_err:
        print(f"Connection Refused: {conn_err}")
        print("This typically means a firewall or network issue is blocking the connection.")
        success = False
        error_message = "Failed to send your message. Connection refused."
        
    except TimeoutError as timeout_err:
        print(f"Connection Timeout: {timeout_err}")
        print("The connection to the Gmail server timed out.")
        success = False
        error_message = "Failed to send your message. Connection timeout."
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        success = False
        error_message = "Failed to send your message. Please try again later."
    
    return jsonify({
        "success": success, 
        "email_sent": email_sent,
        "message": "Thank you! Your message has been sent." if success else error_message
    })

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        
        # Check if the input matches either username or email
        c.execute("SELECT id FROM users WHERE (username=? OR gmail=?) AND password=?", 
                 (username_or_email, username_or_email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            login_user(User(user[0]))
            
            # Log this activity
            log_user_activity(user[0], "Login", f"IP: {request.remote_addr}")
            
            # Record this session
            session_id = uuid.uuid4().hex
            session['_id'] = session_id
            
            # Get IP address and user agent
            ip_address = request.remote_addr
            user_agent = request.user_agent.string
            
            # Create session record in database
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            
            # Create table if not exists
            c.execute('''CREATE TABLE IF NOT EXISTS user_sessions 
                      (id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT, 
                       ip_address TEXT, device_info TEXT, last_active DATETIME)''')
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert new session
            c.execute('''INSERT INTO user_sessions (user_id, session_id, ip_address, device_info, last_active) 
                       VALUES (?, ?, ?, ?, ?)''', 
                     (user[0], session_id, ip_address, user_agent, current_time))
            
            conn.commit()
            conn.close()
            
            return redirect(url_for("upload_file"))
        return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        gmail = request.form["gmail"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, gmail) VALUES (?, ?, ?)",
                  (username, password, gmail))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        # Log this activity
        log_user_activity(user_id, "Account Created", f"Username: {username}, Email: {gmail}")
        
        # Instead of logging in automatically, redirect to login page with success message
        flash("Account created successfully! Please login with your credentials.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    # Log this activity
    log_user_activity(current_user.id, "Logout", f"IP: {request.remote_addr}")
    
    # Remove session record from database
    session_id = session.get('_id')
    if session_id:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        
        # Delete this session
        c.execute("DELETE FROM user_sessions WHERE user_id=? AND session_id=?", 
                 (current_user.id, session_id))
        
        conn.commit()
        conn.close()
    
    logout_user()
    return redirect(url_for("login"))

@app.route("/history")
@login_required
def history():
    # Log this activity
    log_user_activity(current_user.id, "Viewed History")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT image, text, timestamp FROM history WHERE user_id=? ORDER BY timestamp DESC",
              (current_user.id,))
    records = c.fetchall()
    conn.close()
    return render_template("history.html", records=records)

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Log what's being changed
    changes = []
    if username:
        changes.append("username")
    if email:
        changes.append("email")
    if password:
        changes.append("password")
    
    log_user_activity(current_user.id, "Profile Update", f"Changed: {', '.join(changes)}")
    
    # Only update fields that were provided
    if username and email and password:
        c.execute("UPDATE users SET username=?, gmail=?, password=? WHERE id=?", 
                 (username, email, password, current_user.id))
    elif username and email:
        c.execute("UPDATE users SET username=?, gmail=? WHERE id=?", 
                 (username, email, current_user.id))
    elif username and password:
        c.execute("UPDATE users SET username=?, password=? WHERE id=?", 
                 (username, password, current_user.id))
    elif email and password:
        c.execute("UPDATE users SET gmail=?, password=? WHERE id=?", 
                 (email, password, current_user.id))
    elif username:
        c.execute("UPDATE users SET username=? WHERE id=?", 
                 (username, current_user.id))
    elif email:
        c.execute("UPDATE users SET gmail=? WHERE id=?", 
                 (email, current_user.id))
    elif password:
        c.execute("UPDATE users SET password=? WHERE id=?", 
                 (password, current_user.id))
    
    conn.commit()
    conn.close()
    
    # Flash a success message
    flash("Profile updated successfully", "success")
    return redirect(url_for("settings"))

@app.route("/toggle_2fa", methods=["POST"])
@login_required
def toggle_2fa():
    enabled = request.json.get("enabled", False)
    
    # Log this activity
    log_user_activity(current_user.id, "2FA Setting Changed", f"Enabled: {enabled}")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if we need to create a 2fa table
    c.execute('''CREATE TABLE IF NOT EXISTS user_2fa 
                (user_id INTEGER PRIMARY KEY, enabled INTEGER, secret TEXT)''')
    
    # Check if the user already has a 2FA record
    c.execute("SELECT * FROM user_2fa WHERE user_id=?", (current_user.id,))
    record = c.fetchone()
    
    if record:
        # Update existing record
        c.execute("UPDATE user_2fa SET enabled=? WHERE user_id=?", 
                 (1 if enabled else 0, current_user.id))
    else:
        # Create new record with a secret
        secret = secrets.token_hex(16)
        c.execute("INSERT INTO user_2fa (user_id, enabled, secret) VALUES (?, ?, ?)",
                 (current_user.id, 1 if enabled else 0, secret))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "enabled": enabled})

@app.route("/toggle_analytics", methods=["POST"])
@login_required
def toggle_analytics():
    enabled = request.json.get("enabled", False)
    
    # Log this activity
    log_user_activity(current_user.id, "Analytics Setting Changed", f"Enabled: {enabled}")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if we need to create the table
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences 
                (user_id INTEGER PRIMARY KEY, analytics INTEGER, notifications INTEGER, language TEXT)''')
    
    # Check if the user already has preferences
    c.execute("SELECT * FROM user_preferences WHERE user_id=?", (current_user.id,))
    record = c.fetchone()
    
    if record:
        # Update existing preferences
        c.execute("UPDATE user_preferences SET analytics=? WHERE user_id=?", 
                 (1 if enabled else 0, current_user.id))
    else:
        # Create new preferences with default values
        c.execute("INSERT INTO user_preferences (user_id, analytics, notifications, language) VALUES (?, ?, ?, ?)",
                 (current_user.id, 1 if enabled else 0, 0, "en"))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "enabled": enabled})

@app.route("/toggle_notifications", methods=["POST"])
@login_required
def toggle_notifications():
    enabled = request.json.get("enabled", False)
    
    # Log this activity
    log_user_activity(current_user.id, "Notifications Setting Changed", f"Enabled: {enabled}")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if we need to create the table
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences 
                (user_id INTEGER PRIMARY KEY, analytics INTEGER, notifications INTEGER, language TEXT)''')
    
    # Check if the user already has preferences
    c.execute("SELECT * FROM user_preferences WHERE user_id=?", (current_user.id,))
    record = c.fetchone()
    
    if record:
        # Update existing preferences
        c.execute("UPDATE user_preferences SET notifications=? WHERE user_id=?", 
                 (1 if enabled else 0, current_user.id))
    else:
        # Create new preferences with default values
        c.execute("INSERT INTO user_preferences (user_id, analytics, notifications, language) VALUES (?, ?, ?, ?)",
                 (current_user.id, 0, 1 if enabled else 0, "en"))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "enabled": enabled})

@app.route("/update_language", methods=["POST"])
@login_required
def update_language():
    language = request.json.get("language", "en")
    
    # Log this activity
    log_user_activity(current_user.id, "Language Setting Changed", f"Language: {language}")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Check if we need to create the table
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences 
                (user_id INTEGER PRIMARY KEY, analytics INTEGER, notifications INTEGER, language TEXT)''')
    
    # Check if the user already has preferences
    c.execute("SELECT * FROM user_preferences WHERE user_id=?", (current_user.id,))
    record = c.fetchone()
    
    if record:
        # Update existing preferences
        c.execute("UPDATE user_preferences SET language=? WHERE user_id=?", 
                 (language, current_user.id))
    else:
        # Create new preferences with default values
        c.execute("INSERT INTO user_preferences (user_id, analytics, notifications, language) VALUES (?, ?, ?, ?)",
                 (current_user.id, 0, 0, language))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "language": language})

@app.route("/get_active_sessions", methods=["GET"])
@login_required
def get_active_sessions():
    # Log this activity
    log_user_activity(current_user.id, "Viewed Active Sessions")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Create sessions table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions 
                (id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT, 
                 ip_address TEXT, device_info TEXT, last_active DATETIME)''')
    
    # Get all active sessions for the user
    c.execute("SELECT id, session_id, ip_address, device_info, last_active FROM user_sessions WHERE user_id=?",
             (current_user.id,))
    sessions = c.fetchall()
    
    conn.close()
    
    session_list = []
    for s in sessions:
        session_list.append({
            "id": s[0],
            "session_id": s[1],
            "ip_address": s[2],
            "device_info": s[3],
            "last_active": s[4]
        })
    
    return jsonify({"success": True, "sessions": session_list})

@app.route("/terminate_session/<int:session_id>", methods=["POST"])
@login_required
def terminate_session(session_id):
    # Log this activity
    log_user_activity(current_user.id, "Terminated Session", f"Session ID: {session_id}")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Verify this session belongs to the current user before deleting
    c.execute("SELECT user_id FROM user_sessions WHERE id=?", (session_id,))
    session_record = c.fetchone()
    
    if session_record and int(session_record[0]) == current_user.id:
        c.execute("DELETE FROM user_sessions WHERE id=?", (session_id,))
        conn.commit()
        success = True
    else:
        success = False
    
    conn.close()
    
    return jsonify({"success": success})

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # Log this activity
    log_user_activity(current_user.id, "Viewed Settings Page")
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Get user info
    c.execute("SELECT username, gmail FROM users WHERE id=?", (current_user.id,))
    user = c.fetchone()
    
    # Get user preferences
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences 
                (user_id INTEGER PRIMARY KEY, analytics INTEGER, notifications INTEGER, language TEXT)''')
    
    c.execute("SELECT analytics, notifications, language FROM user_preferences WHERE user_id=?", 
             (current_user.id,))
    pref = c.fetchone()
    
    if not pref:
        # Create default preferences if none exist
        c.execute("INSERT INTO user_preferences (user_id, analytics, notifications, language) VALUES (?, ?, ?, ?)",
                 (current_user.id, 0, 0, "en"))
        conn.commit()
        analytics_enabled = False
        notifications_enabled = False
        language = "en"
    else:
        analytics_enabled = bool(pref[0])
        notifications_enabled = bool(pref[1])
        language = pref[2]
    
    # Get 2FA status
    c.execute('''CREATE TABLE IF NOT EXISTS user_2fa 
                (user_id INTEGER PRIMARY KEY, enabled INTEGER, secret TEXT)''')
    
    c.execute("SELECT enabled FROM user_2fa WHERE user_id=?", (current_user.id,))
    twofa = c.fetchone()
    twofa_enabled = bool(twofa[0]) if twofa else False
    
    # Record this session if necessary
    session_id = session.get('_id', uuid.uuid4().hex)
    session['_id'] = session_id
    
    # Get IP address and user agent
    ip_address = request.remote_addr
    user_agent = request.user_agent.string
    
    # Create or update session record
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions 
                (id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT, 
                 ip_address TEXT, device_info TEXT, last_active DATETIME)''')
    
    # Check if this session already exists
    c.execute("SELECT id FROM user_sessions WHERE user_id=? AND session_id=?", 
             (current_user.id, session_id))
    existing_session = c.fetchone()
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if existing_session:
        # Update last active time
        c.execute("UPDATE user_sessions SET last_active=? WHERE id=?", 
                 (current_time, existing_session[0]))
    else:
        # Create new session record
        c.execute('''INSERT INTO user_sessions (user_id, session_id, ip_address, device_info, last_active) 
                   VALUES (?, ?, ?, ?, ?)''', 
                 (current_user.id, session_id, ip_address, user_agent, current_time))
    
    conn.commit()
    conn.close()
    
    return render_template("settings.html", 
                          username=user[0], 
                          gmail=user[1],
                          twofa_enabled=twofa_enabled,
                          analytics_enabled=analytics_enabled,
                          notifications_enabled=notifications_enabled,
                          language=language)

@app.route("/about")
def about():
    # Only log if user is logged in
    if current_user.is_authenticated:
        log_user_activity(current_user.id, "Viewed About Page")
        
    team_members = [
        {"name": "Bhuwan Shrestha", "role": "Lead Developer", "image": "bhuwan_shrestha.jpg"},
        {"name": "Alen Varghese", "role": "UI/UX Designer", "image": "alen_varghese.jpg"},
        {"name": "Shubh Soni", "role": "Machine Learning Expert", "image": "shubh_soni.jpg"},
        {"name": "Dev Patel", "role": "Backend Engineer", "image": "dev_patel.jpg"}
    ]
    return render_template("about.html", team_members=team_members)

@app.route("/contact")
def contact():
    # Only log if user is logged in
    if current_user.is_authenticated:
        log_user_activity(current_user.id, "Viewed Contact Page")
        
    return render_template("contact.html")

@app.route("/references")
def references():
    # Only log if user is logged in
    if current_user.is_authenticated:
        log_user_activity(current_user.id, "Viewed References Page")
        
    return render_template("references.html")

@app.route("/download_activity_log")
@login_required
def download_activity_log():
    log_file = os.path.join(app.config["LOGS_FOLDER"], f"{current_user.id}_log.txt")
    
    # Log this activity
    log_user_activity(current_user.id, "Activity Log Downloaded")
    
    # Check if log file exists
    if os.path.exists(log_file):
        return send_file(log_file, as_attachment=True, 
                         download_name=f"activity_log_{current_user.id}.txt")
    else:
        # Create empty file with header if it doesn't exist
        with open(log_file, "w") as f:
            f.write(f"Activity log for user ID: {current_user.id}\n")
            f.write("==============================================\n\n")
        return send_file(log_file, as_attachment=True, 
                         download_name=f"activity_log_{current_user.id}.txt")

@app.route("/submit_rating", methods=["POST"])
@login_required
def submit_rating():
    # Get the rating data
    rating_data = request.json
    rating = rating_data.get("rating")
    comment = rating_data.get("comment", "")
    
    success = True
    error_message = ""
    email_sent = False
    
    # Get user information
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, gmail FROM users WHERE id=?", (current_user.id,))
    user = c.fetchone()
    conn.close()
    
    username = user[0] if user else "Unknown"
    user_email = user[1] if user else "Unknown"
    
    # Try to send email notification
    try:
        # Email credentials
        secondary_email = "handwrittensender@gmail.com"  # Secondary email address
        secondary_app_password = "ymribhdrhrbsymls"  # App password without spaces
        recipient_email = "handwrittenocr448@gmail.com"  # Primary email to receive notifications
        
        # Email body
        body = f"""
New rating submission:

Username: {username}
Email: {user_email}
Rating: {rating}/5 stars

Additional Comment:
{comment}
"""
        # Use yagmail to send the email
        try:
            import yagmail
            # Configure yagmail
            yag = yagmail.SMTP(secondary_email, secondary_app_password)
            # Send email
            yag.send(
                to=recipient_email,
                subject=f"Rating Notification: {username} rated {rating}/5 stars",
                contents=body,
                headers={'Reply-To': user_email}
            )
            email_sent = True
            print(f"Rating notification email sent successfully from {secondary_email} to {recipient_email}")
        except ImportError:
            print("Yagmail not available, falling back to smtplib")
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = secondary_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Rating Notification: {username} rated {rating}/5 stars"
            msg['Reply-To'] = user_email  # Set reply-to as the user's email
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
                # Login with secondary email credentials
                server.login(secondary_email, secondary_app_password)
                server.send_message(msg)
                
                email_sent = True
                print(f"Rating notification email sent successfully from {secondary_email} to {recipient_email}")
            
        # Log this activity
        log_user_activity(current_user.id, "Rating Submitted", f"Rating: {rating}/5 stars")
            
    except Exception as e:
        print(f"Error sending rating notification email: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        # Still return success even if email fails
    
    return jsonify({
        "success": success, 
        "email_sent": email_sent,
        "message": "Thank you for your rating!" if success else error_message
    })

if __name__ == "__main__":
    app.run(debug=True)