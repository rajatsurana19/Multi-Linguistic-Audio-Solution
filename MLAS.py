import streamlit as st
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS
import speech_recognition as sr
import time
import os
import tempfile
import logging
import base64
import uuid
import traceback
from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient
import bcrypt
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("_name_")

# Set page configuration
st.set_page_config(page_title="Multi Linguistic Audio Solution", layout="wide")


# Custom CSS for a modern and clean look
def load_css():
    st.markdown("""
    <style>
    /* Header and Footer Styling */
    .header {
        background-color: #1E90FF;
        padding: 20px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        background-color: #1E90FF;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 16px;
        border-radius: 10px;
        margin-top: 20px;
    }
    /* Button Styling */
    .stButton>button {
        background-color: #FF4500;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        width: 100%;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6347;
        color: #1E90FF;  /* Light blue text on hover */
    }
    /* Sidebar Button Styling */
    .sidebar-button {
        background-color: #1E90FF;
        color: white;
        margin-bottom: 10px;
    }
    .sidebar-button:hover {
        background-color: #4169E1;
    }
    /* File Uploader Styling */
    .stFileUploader>div>div>div {
        background-color: #F0F8FF;
        border-radius: 5px;
        padding: 10px;
    }
    /* Text Area Styling */
    .stTextArea>div>div>textarea {
        background-color: #F0F8FF;
        color: #2b2d42;
        border-radius: 5px;
        padding: 10px;
    }
    /* Select Box Styling */
    .stSelectbox>div>div>div {
        background-color: #F0F8FF;
        color: #2b2d42;
        border-radius: 5px;
    }
    .stSelectbox>div>div>div:hover {
        color: #1E90FF;  
    }
    /* Progress Bar Styling */
    .stProgress>div>div>div>div {
        background-color: #FF4500;
    }
    /* Tooltip Styling - Improved for better visibility */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-weight: bold;
    }
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    /* Add better text contrast for options */
    .option-text {
        color: #1E90FF;
        font-weight: 500;
    }
    .option-text:hover {
        color: #1E90FF;
        font-weight: 600;
    }
 
    /* Improve visibility of translated text */
    .translated-text {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1E90FF;
        margin: 10px 0;
    }
    /* Feedback Form Styling */
    .feedback-form {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1E90FF;
        margin: 20px 0;
    }
    .feedback-form h3 {
        color: #1E90FF;
        margin-bottom: 15px;
    }
    .feedback-submit {
        background-color: #4CAF50 !important;
        margin-top: 15px !important;
    }
    /* Card Styling */
    .card {
        background-color: #ff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        cursor: pointer;
    }
    .card h3 {
        color: #1E90FF;
    }
    .card p {
        color: #333;
    }
    /* Activity Card Styling */
    .activity-card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin: 8px 0;
        transition: transform 0.2s, box-shadow 0.2s;
        border-left: 3px solid #1E90FF;
    }
    .activity-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        cursor: pointer;
        background-color: #f9f9f9;
    }
    /* Quick Actions Button */
    .quick-action-button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 8px 16px;
        margin: 5px;
        border: none;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.3s;
    }
    .quick-action-button:hover {
        background-color: #4169E1;
        cursor: pointer;
    }
    /* Login/Register Container */
    .auth-container {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 25px;
        margin: 20px auto;
        max-width: 500px;
    }
    .tab-content {
        padding-top: 20px;
    }
    /* Form Fields */
    .stTextInput>div>div>input {
        background-color: #F0F8FF;
        color: #2b2d42;
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #ddd;
    }
    .stTextInput>div>div>input:focus {
        border-color: #1E90FF;
        box-shadow: 0 0 0 2px rgba(30, 144, 255, 0.2);
    }
    /* Status Messages */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    /* Spinner */
    .stSpinner {
        text-align: center;
        padding: 20px;
    }
    /* Image placeholders */
    .placeholder-image {
        width: 100%;
        height: 200px;
        background-color: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #666;
        font-weight: bold;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

# Define language
LANGUAGE_TO_CODE = {
    "Hindi": "hi",
    "Marathi": "mr",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-TW",
    "Russian": "ru",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Italian": "it"
}

# Setup caching
@st.cache_resource
def get_db_connection():
    try:
        client = MongoClient("mongodb+srv://multilinguisticaudiosolution:v4noloVAiktXpOmf@multilinguisticaudiosol.uyguf.mongodb.net/?retryWrites=true&w=majority&appName=MultiLinguisticAudioSolution")
        db = client["MultiLinguisticAudioSolution"]
        return db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

# Initialize database collections
def init_db():
    try:
        db = get_db_connection()
        if db is None:
            st.error("Could not connect to database. Please check your connection.")
            return
            
        if "users" not in db.list_collection_names():
            db.create_collection("users")
        if "feedback" not in db.list_collection_names():
            db.create_collection("feedback")
        if "recent_activity" not in db.list_collection_names():
            db.create_collection("recent_activity")
        if "output_files" not in db.list_collection_names():
            db.create_collection("output_files")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        st.error("Could not initialize database. Please check your connection.")

# User registration
def register_user(username, email, password):
    if not username or not email or not password:
        return False, "All fields are required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
        
    db = get_db_connection()
    if db is None:
        return False, "Database connection error"
        
    users = db["users"]
    try:
        # Check if user already exists
        existing_user = users.find_one({"email": email})
        if existing_user:
            return False, "Email already registered"
            
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.now()
        }
        users.insert_one(user)
        return True, "Registration successful!"
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return False, f"Registration error: {str(e)}"
    
# Define constants for login attempts
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW = timedelta(minutes=5)

def check_login_attempts(email):
    """
    Check if the user has exceeded the maximum number of login attempts.
    """
    db = get_db_connection()
    if db is None:
        return False
    
    login_attempts = db["login_attempts"]
    
    # Count the number of failed attempts within the time window
    count = login_attempts.count_documents({
        "email": email,
        "success": False,
        "timestamp": {"$gt": datetime.now() - LOGIN_ATTEMPT_WINDOW}
    })
    
    # If the count exceeds the maximum attempts, return False
    if count >= MAX_LOGIN_ATTEMPTS:
        return False
    return True

def record_login_attempt(email, success):
    db = get_db_connection()
    if db is None:
        return
    
    login_attempts = db["login_attempts"]
    login_attempts.insert_one({
        "email": email,
        "success": success,
        "timestamp": datetime.now()
    })

# User login
def login_user(email, password):
    if not email or not password:
        return None, "Email and password are required"
    
    if not check_login_attempts(email):
        return None, "Too many login attempts. Please try again later."
    
    db = get_db_connection()
    if db is None:
        return None, "Database connection error"
        
    users = db["users"]
    try:
        user = users.find_one({"email": email})
        
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                record_login_attempt(email, True)
                st.session_state.user = user  # Store user in session state
                return user, "Login successful"
            else:
                record_login_attempt(email, False)
                return None, "Invalid password"
        else:
            return None, "Email not found"
    except Exception as e:
        logger.error(f"Login error: {e}")
        return None, f"Login error: {str(e)}"


def check_login():
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to access this feature.")
        return False
    return True

# Add this at the top of your file with other constants
LAST_CLEANUP_KEY = "last_cleanup_run"

def cleanup_old_files():
    """
    Cleans up old files and database records older than 30 days.
    Runs maximum once per day using a file-based timestamp.
    """
    try:
        # File to store last cleanup timestamp
        LAST_CLEANUP_FILE = "last_cleanup.txt"
        
        # Check when we last ran cleanup
        last_run = None
        if os.path.exists(LAST_CLEANUP_FILE):
            try:
                with open(LAST_CLEANUP_FILE, "r") as f:
                    last_run_str = f.read().strip()
                    if last_run_str:
                        last_run = datetime.fromisoformat(last_run_str)
            except (ValueError, IOError) as e:
                logger.warning(f"Could not read last cleanup time: {e}")
        
        # Only proceed if it's been more than 1 day since last run
        if last_run and (datetime.now() - last_run) < timedelta(days=1):
            logger.debug("Cleanup skipped - ran recently")
            return
            
        now = datetime.now()
        cutoff = now - timedelta(days=30)
        deleted_files_count = 0
        deleted_db_records = 0
        
        logger.info(f"Starting cleanup for files older than {cutoff.date()}")
        
        # 1. Clean permanent_outputs directory
        if os.path.exists("permanent_outputs"):
            for filename in os.listdir("permanent_outputs"):
                filepath = os.path.join("permanent_outputs", filename)
                try:
                    if os.path.isfile(filepath):
                        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                        if file_time < cutoff:
                            os.remove(filepath)
                            deleted_files_count += 1
                            logger.debug(f"Deleted file: {filename}")
                except Exception as e:
                    logger.error(f"Error deleting {filename}: {e}")
        
        # 2. Clean MongoDB records
        db = get_db_connection()
        if db is not None:
            try:
                output_files = db["output_files"]
                recent_activity = db["recent_activity"]
                
                # Find and delete old files
                old_files = output_files.find({"timestamp": {"$lt": cutoff}})
                for file in old_files:
                    try:
                        if "file_path" in file and os.path.exists(file["file_path"]):
                            os.remove(file["file_path"])
                            logger.debug(f"Deleted file: {file['file_path']}")
                    except Exception as e:
                        logger.error(f"Error deleting file {file.get('file_path', 'unknown')}: {e}")
                
                # Delete the records
                files_result = output_files.delete_many({"timestamp": {"$lt": cutoff}})
                activity_result = recent_activity.delete_many({"timestamp": {"$lt": cutoff}})
                deleted_db_records = files_result.deleted_count + activity_result.deleted_count
                
            except Exception as e:
                logger.error(f"Database cleanup error: {e}")
        
        # Update last run time
        try:
            with open(LAST_CLEANUP_FILE, "w") as f:
                f.write(now.isoformat())
        except IOError as e:
            logger.error(f"Could not save cleanup timestamp: {e}")
        
        # Log summary
        if deleted_files_count > 0 or deleted_db_records > 0:
            logger.info(
                f"Cleanup completed. "
                f"Deleted {deleted_files_count} files and {deleted_db_records} database records."
            )
        else:
            logger.info("No old records found for cleanup")
            
    except Exception as e:
        logger.error(f"Critical error during cleanup: {e}")
        raise  # Re-raise if you want the error to be visible


# Get user activity
def get_user_activity(user_id, limit=10):
    try:
        db = get_db_connection()
        if db is None:
            return []
            
        activities = list(db["recent_activity"].find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit))
        
        return activities
    except Exception as e:
        logger.error(f"Error retrieving user activity: {e}")
        return []

# Get user files
def get_user_files(user_id, file_type=None, limit=20):
    try:
        db = get_db_connection()
        if db is None:
            return []
            
        query = {"user_id": user_id}
        if file_type:
            query["file_type"] = file_type
            
        files = list(db["output_files"].find(query).sort("created_at", -1).limit(limit))
        
        return files
    except Exception as e:
        logger.error(f"Error retrieving user files: {e}")
        return []


def get_download_link(file_path, link_text="Download"):
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return "File not available"
            
        with open(file_path, "rb") as f:
            file_data = f.read()
        b64_data = base64.b64encode(file_data).decode()
        filename = os.path.basename(file_path)
        mime_type = "application/octet-stream"
        if file_path.lower().endswith(".mp3"):
            mime_type = "audio/mpeg"
        elif file_path.lower().endswith(".txt"):
            mime_type = "text/plain"
        elif file_path.lower().endswith(".pdf"):
            mime_type = "application/pdf"
            
        return f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}" class="quick-action-button">{link_text}</a>'
    except Exception as e:
        logger.error(f"Error creating download link: {e}")
        return "Error creating download link"


def create_permanent_copy(temp_file_path, file_type):
    try:
        os.makedirs("permanent_outputs", exist_ok=True)
        filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_type}"
        permanent_path = os.path.join("permanent_outputs", filename)
        with open(temp_file_path, "rb") as temp_file:
            with open(permanent_path, "wb") as perm_file:
                perm_file.write(temp_file.read())
        return permanent_path
    except Exception as e:
        logger.error(f"Error creating permanent copy: {e}")
        return None

@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_recent_activity(_user_id):
    db = get_db_connection()
    if db is None:
        return []
        
    recent_activity = db["recent_activity"]
    try:
        return list(recent_activity.find({"user_id": _user_id}).sort("timestamp", -1))
    except Exception as e:
        logger.error(f"Error getting recent activity: {e}")
        return []
    
def save_feedback_to_db(user_id, rating, comments, feature):
    db = get_db_connection()
    if db is None:
        return False
        
    feedback = db["feedback"]
    try:
        feedback.insert_one({
            "user_id": user_id,
            "rating": rating,
            "comments": comments,
            "feature": feature,
            "timestamp": datetime.now()
        })
        return True
    except Exception as e:
        logger.error(f"Feedback save error: {e}")
        return False
    
def save_recent_activity(user_id, file_name, file_type, output_path=None):
    db = get_db_connection()
    if db is None:
        return None
        
    recent_activity = db["recent_activity"]
    try:
        activity = {
            "user_id": user_id,
            "file_name": file_name,
            "file_type": file_type,
            "output_path": output_path,
            "timestamp": datetime.now()
        }
        activity_id = recent_activity.insert_one(activity).inserted_id
        
        if output_path:
            output_files = db["output_files"]
            output_files.insert_one({
                "user_id": user_id,
                "activity_id": activity_id,
                "file_path": output_path,
                "file_type": file_type,
                "timestamp": datetime.now()
            })
        
        return activity_id
    except Exception as e:
        logger.error(f"Activity save error: {e}")
        return None

def show_feedback_form(feature_name):
    st.markdown('<div class="feedback-form">', unsafe_allow_html=True)
    st.subheader("We value your feedback!")
    st.write("Please take a moment to let us know how we're doing.")
    
    rating = st.radio(
        "How would you rate the quality of the conversion?",
        options=["Excellent", "Good", "Average", "Poor", "Very Poor"],
        horizontal=True,
        key=f"rating_{feature_name}"
    )
    
    comments = st.text_area(
        "Any additional comments or suggestions?",
        key=f"comments_{feature_name}"
    )
    
    if st.button("Submit Feedback", key=f"submit_{feature_name}", type="primary"):
        if 'user' in st.session_state and st.session_state.user:
            if save_feedback_to_db(
                user_id=st.session_state.user["_id"],  
                rating=rating,                     
                comments=comments,                 
                feature=feature_name               
            ):
                st.success("Thank you for your feedback! We appreciate your input.")
            else:
                st.error("Failed to submit feedback. Please try again.")
        else:
            st.warning("Please log in to submit feedback.")
    
    st.markdown('</div>', unsafe_allow_html=True)



# Module History Page
def module_history_page():
    if not check_login():
        return
    st.header("Module History")
    
    user_id = st.session_state.user["_id"]
    activities = get_user_activity(user_id)
    
    if not activities:
        st.info("No recent activities found.")
        return
    
    for activity in activities:
        with st.expander(f"{activity['file_name']} - {activity['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
            st.write(f"Type: {activity['file_type']}")
            if activity.get("output_path"):
                st.markdown(get_download_link(activity["output_path"], "Download Output"), unsafe_allow_html=True)
            else:
                st.info("No output file available for this activity.")

# Dashboard Page
def dashboard_page():
    if not check_login():
        return
    st.header("Dashboard")
    
    user_id = st.session_state.user["_id"]
    activities = get_user_activity(user_id)
    
    if not activities:
        st.info("No recent activities found.")
        return
    
    # Display statistics
    st.subheader("Usage Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Files Processed", len(activities))
    
    with col2:
        st.metric("Most Used Feature", max(set([a["file_type"] for a in activities]), key=[a["file_type"] for a in activities].count))
    
    with col3:
        st.metric("Last Activity", activities[0]["timestamp"].strftime('%Y-%m-%d %H:%M'))
    
    # Display activity chart
    st.subheader("Activity Over Time")
    activity_df = pd.DataFrame(activities)
    activity_df["date"] = activity_df["timestamp"].dt.date
    activity_count = activity_df.groupby("date").size().reset_index(name="count")
    st.line_chart(activity_count.set_index("date"))

import streamlit as st

def header():
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center; /* Vertically centers the items */
            justify-content: space-between; /* Positions text and menu at opposite ends */
            background-color: #1E90FF; /* Sets the background color to blue */
            padding: 10px 20px;
            border-radius: 5px;
            color: white; /* Makes the text color readable against the blue background */
        }

        .header-text {
            flex-grow: 1;
            text-align: center; /* Centers the text within the available space */
            color: #ffffff; /* Sets the text color to orange */
        }

        .hamburger-menu {
            cursor: pointer;
            font-size: 20px; /* Increases the size of the hamburger icon */
            background: none;
            border: none;
            color: white; /* Matches the menu color with the text */
        }

        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown-content {
            display: none; /* Initially hidden */
            position: absolute;
            right: 0;
            background-color: #FF4500; /* Sets menu background color to orange */
            min-width: 120px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
            flex-direction: column; /* Ensures items are stacked vertically */
        }

        .dropdown:hover .dropdown-content {
            display: flex; /* Makes the dropdown content visible on hover */
        }

        .dropdown-content a {
            display: flex; /* Aligns the content using flexbox */
            align-items: center; /* Vertically centers the logo and text */
            justify-content: center; /* Horizontally centers the logo and text */
            color: white; /* Makes text readable against the orange background */
            padding: 8px 12px;
            text-decoration: none;
            font-size: 15px; /* Sets font size */
            min-height: 40px; /* Sets a minimum height for each dropdown item */
        }

        .dropdown-content a:hover {
            background-color: #FFA07A; /* A lighter shade of orange for hover effect */
        }

        .icon {
            margin-right: 8px; /* Adds spacing between the logo and the text */
            width: 20px;
            height: 20px;
        }
        </style>

        <div class="header">
            <div class="header-text">Multi Linguistic Audio Solution</div>
            <div class="dropdown">
                <button class="hamburger-menu">☰</button>
                <div class="dropdown-content">
                    <a href="https://github.com/rajatsurana19" target="_blank">
                        <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons/icons/github.svg" class="icon"> &nbsp;GitHub &nbsp;
                    </a>
                    <a href="https://linkedin.com/in/rajat-surana" target="_blank">
                        <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons/icons/linkedin.svg" class="icon"> LinkedIn
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )




@st.cache_data(ttl=3600)  # Cache translations for 1 hour
def translate_text(text, target_lang, source_lang="auto", max_retries=3):
    """
    Translate text using GoogleTranslator with retry logic.
    """
    for attempt in range(int(max_retries)):  # Ensure max_retries is an integer
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)
            return translated_text, None
        except Exception as e:
            logger.error(f"Translation attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Wait before retrying
    return None, f"Translation failed after {max_retries} attempts"

# Function to convert PDF to audio (enhanced with progress tracking)
def convert_pdf_to_audio(pdf_path, lang_code, max_retries=3):
    try:
        # Read PDF content
        reader = PdfReader(pdf_path)
        text = ""
        
        # Initialize progress bar
        progress_bar = st.progress(0)
        total_pages = len(reader.pages)
        
        # Extract text from each page with progress updates
        for i, page in enumerate(reader.pages):
            text += page.extract_text() + "\n"
            progress_bar.progress((i + 1) / (total_pages + 2))  # +2 for translation and audio steps
        
        # Translate the text if necessary (English is default for most PDFs)
        if lang_code != "en":
            st.text("Translating PDF content...")
            translated_text, error = translate_text(text, lang_code)
            if error:
                return None, error
            text = translated_text
        
        progress_bar.progress((total_pages + 1) / (total_pages + 2))
        
        # Convert text to speech
        st.text("Converting to speech...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_path = temp_audio.name
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(temp_path)
            
        progress_bar.progress(1.0)
        time.sleep(0.5)  # Small delay to show completed progress
        progress_bar.empty()  # Remove progress bar
        
        return temp_path, None
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"PDF to Audio error: {e}\n{error_traceback}")
        return None, f"Error processing PDF: {e}"

# Function to convert text to speech
def text_to_speech(text, lang_code, max_retries=3):
    for attempt in range(max_retries):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                temp_path = temp_audio.name
                tts = gTTS(text=text, lang=lang_code, slow=False)
                tts.save(temp_path)
            return temp_path, None
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"Text to Speech error on attempt {attempt+1}: {e}\n{error_traceback}")
            if attempt == max_retries - 1:
                return None, f"Error generating speech after {max_retries} attempts: {e}"
            


def home_page():
    st.header("Welcome to Multi Linguistic Audio Solution")
    
    # Display user-specific content if logged in
    if 'user' in st.session_state and st.session_state.user:
        st.subheader(f"Welcome back, {st.session_state.user['username']}!")
    
    # Quick action buttons
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Audio to Text", key="quick_audio_text"):
            st.session_state.current_page = "Audio to Text"
            st.rerun()
            
    with col2:
        if st.button("PDF to Audio", key="quick_pdf_audio"):
            st.session_state.current_page = "PDF to Audio"
            st.rerun()
            
    with col3:
        if st.button("Text to Speech", key="quick_text_speech"):
            st.session_state.current_page = "Text to Speech"
            st.rerun()
            
    with col4:
        if st.button("Translation", key="quick_translation"):
            st.session_state.current_page = "Translation"
            st.rerun()
    
    # General information cards
    st.markdown("""
        <div class="card">
            <h3>About the Application</h3>
            <p>This application provides a suite of tools for multi-linguistic audio and text processing. You can convert audio to text, PDFs to audio, text to speech, and translate text into multiple languages.</p>
        </div>
        <div class="card">
            <h3>How to Use</h3>
            <p>1. Select the desired functionality from the sidebar.</p>
            <p>2. Upload files or enter text as required.</p>
            <p>3. Select language options.</p>
            <p>4. Click the action button to process your request.</p>
        </div>
        <div class="card">
            <h3>Supported Features</h3>
            <p>- Audio to Text Conversion</p>
            <p>- PDF to Audio Conversion</p>
            <p>- Text-to-Speech Conversion</p>
            <p>- Text Translation</p>
        </div>
    """, unsafe_allow_html=True)

def login_register_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.header("User Authentication")
    
    if 'user' in st.session_state and st.session_state.user:
        st.subheader(f"Welcome, {st.session_state.user['username']}!")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.current_page = "Home"
            st.rerun()
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", key="login_button"):
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    with st.spinner("Logging in..."):
                        user, message = login_user(email, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.current_page = "Home"
                            st.success("Login successful!")
                            time.sleep(1)  # Brief pause to show success message
                            st.rerun()
                        else:
                            st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Register")
            username = st.text_input("Username", key="register_username")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            
            if st.button("Register", key="register_button"):
                with st.spinner("Creating account..."):
                    success, message = register_user(username, email, password)
                    if success:
                        st.success(message)
                        time.sleep(2)
                        st.rerun()
                        
                    else:
                        st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def help_faq_page():
    st.header("Help & FAQs")
    
    # Display FAQs using expandable sections
    with st.expander("What file formats are supported?"):
        st.write("""
        - Audio to Text: WAV files
        - PDF to Audio: PDF files
        - Text-to-Speech: Plain text input
        - Translation: Plain text input
        """)
    
    with st.expander("How large can my files be?"):
        st.write("""
        We recommend keeping files under 10MB for optimal performance.
        - Audio files: Maximum 10MB
        - PDF files: Maximum 10MB or 50 pages
        """)
    
    with st.expander("Why do I need to create an account?"):
        st.write("""
        Creating an account allows you to:
        - Save your conversion history
        - Download your past conversions
        - Track your usage
        - Provide feedback to help us improve
        
        Your data is kept secure and private.
        """)
    
    with st.expander("What languages are supported?"):
        st.write("""
        We currently support the following languages:
        - Hindi
        - English
        - Spanish
        - French
        - German
        - Japanese
        - Chinese
        - Russian
        - Arabic
        - Portuguese
        - Italian
        - Marathi
        
        More languages may be added in future updates.
        """)
    
    with st.expander("How accurate is the audio transcription?"):
        st.write("""
        Our audio transcription uses Google's Speech Recognition API, which has high accuracy for clear audio.
        Factors that may affect accuracy include:
        - Background noise
        - Speaker accent
        - Audio quality
        - Multiple speakers
        
        For best results, use clear audio recordings in quiet environments.
        """)
    
    with st.expander("How can I report issues or suggest features?"):
        st.write("""
        We welcome your feedback! You can:
        1. Use the feedback forms available on each feature page
        2. Email us at multilinguisticaudiosolution@gmail.com
        3. Visit our GitHub repository to create an issue
        """)

# Audio to Text Page - Improved
def audio_to_text_page():
    if not check_login():
        return
    st.header("Audio to Text Conversion")
    
    # Add file size warning
    st.warning("""
    **Privacy Notice:** 
    - Files are automatically deleted after 30 days for your privacy
    - Maximum file size: 2MB
    - Supported format: WAV
    """)
    
    # File uploader for audio
    audio_file = st.file_uploader(
        "Upload a WAV file (max 2MB)", 
        type=["wav"], 
        label_visibility="visible"
    )
    
    if audio_file:
        if audio_file.size > 2 * 1024 * 1024:
            st.error("File size exceeds 2MB limit. Please upload a smaller file.")
            return
        
        st.audio(audio_file, format='audio/wav')
        
        if st.button("Convert to Text", key="convert_audio_button"):
            with st.spinner("Processing audio..."):
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                    temp_audio.write(audio_file.getbuffer())
                    temp_audio_path = temp_audio.name
                                    
                # Process the audio file
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(temp_audio_path) as source:
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data)
                    
                    st.subheader("Transcription Result:")
                    st.markdown(f'<div class="translated-text">{text}</div>', unsafe_allow_html=True)
                    
                    # Save text to file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as temp_text:
                        temp_text.write(text)
                        temp_text_path = temp_text.name
                    
                    # Create permanent copy of the output text file
                    permanent_text_path = create_permanent_copy(temp_text_path, 'txt')
                    
                    if permanent_text_path:
                        # Save recent activity with output path
                        activity_id = save_recent_activity(
                            st.session_state.user["_id"], 
                            audio_file.name, 
                            "Audio", 
                            permanent_text_path
                        )
                        
                        # Provide download link
                        st.markdown(get_download_link(permanent_text_path, "Download Transcription Text"), unsafe_allow_html=True)
                        
                        # Clean up temporary text file
                        os.unlink(temp_text_path)
                    else:
                        st.error("Failed to save transcription file.")
                        
                except sr.UnknownValueError:
                    st.error("Speech Recognition could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech Recognition service: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"Audio to text error: {e}\n{traceback.format_exc()}")
                finally:
                    # Clean up temporary file
                    os.unlink(temp_audio_path)
    
    # Always show feedback form
    show_feedback_form("audio_to_text")

# PDF to Audio Page - Improved
def pdf_to_audio_page():
    if not check_login():
        return
    st.header("PDF to Audio Conversion")
    
    # Add file size warning
    st.warning("""
    **Privacy Notice:** 
    - Files are automatically deleted after 30 days for your privacy
    - Maximum file size: 10MB
    - Supported format: PDF
    """)
    
    # File uploader for PDF
    pdf_file = st.file_uploader(
        "Upload a PDF file (max 10MB)", 
        type=["pdf"], 
        label_visibility="visible"
    )
    
    if pdf_file:
        if pdf_file.size > 10 * 1024 * 1024:
            st.error("File size exceeds 10MB limit. Please upload a smaller file.")
            return
        
        target_lang = st.selectbox(
            "Select target language for audio:", 
            list(LANGUAGE_TO_CODE.keys()),
            index=list(LANGUAGE_TO_CODE.keys()).index("English"),
            key="pdf_lang",
            label_visibility="visible"
        )
        
        if st.button("Convert to Audio", key="convert_pdf_button"):
            with st.spinner("Processing PDF..."):
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                    temp_pdf.write(pdf_file.getbuffer())
                    temp_pdf_path = temp_pdf.name
                
                # Process the PDF file
                audio_path, error = convert_pdf_to_audio(temp_pdf_path, LANGUAGE_TO_CODE[target_lang])
                
                # Clean up PDF temp file
                os.unlink(temp_pdf_path)
                
                if audio_path:
                    st.success(f"PDF successfully converted to {target_lang} audio!")
                    st.subheader("Audio Output:")
                    st.audio(audio_path, format='audio/mp3')
                    
                    # Create permanent copy of the output audio file
                    permanent_audio_path = create_permanent_copy(audio_path, 'mp3')
                    
                    if permanent_audio_path:
                        # Save recent activity with output path
                        activity_id = save_recent_activity(
                            st.session_state.user["_id"], 
                            pdf_file.name, 
                            "PDF", 
                            permanent_audio_path
                        )
                        
                        # Add download link
                        st.markdown(get_download_link(permanent_audio_path, "Download Audio File"), unsafe_allow_html=True)
                        
                        # Clean up temporary audio file
                        os.unlink(audio_path)
                    else:
                        st.error("Failed to save audio file.")
                else:
                    st.error(f"Error: {error}")
    
    # Always show feedback form
    show_feedback_form("pdf_to_audio")

# Text-to-Speech Page - Improved (Continued)
def text_to_speech_page():
    if not check_login():
        return
    st.header("Text to Speech Conversion")
    
    # Text input area with a label to avoid the warning
    input_text = st.text_area(
        "Enter the text you want to convert to speech:",
        height=200,
        label_visibility="visible",
        key="tts_input_text"
    )
    
    target_lang = st.selectbox(
        "Select target language:", 
        list(LANGUAGE_TO_CODE.keys()),
        index=list(LANGUAGE_TO_CODE.keys()).index("English"),
        key="tts_lang",
        label_visibility="visible"
    )
    
    if st.button("Generate Speech", key="generate_speech_button"):
        if input_text:
            with st.spinner("Translating and generating audio..."):
                # Translate the text to the target language
                translated_text, error = translate_text(input_text, LANGUAGE_TO_CODE[target_lang])
                
                if translated_text:
                    # Show translated text
                    st.subheader("Translated Text:")
                    st.markdown(f'<div class="translated-text">{translated_text}</div>', unsafe_allow_html=True)
                    
                    # Convert translated text to speech
                    audio_path, error = text_to_speech(translated_text, LANGUAGE_TO_CODE[target_lang])
                    
                    if audio_path:
                        st.success(f"Text successfully converted to {target_lang} audio!")
                        st.subheader("Audio Output:")
                        st.audio(audio_path, format='audio/mp3')
                        
                        # Create permanent copy of the output audio file
                        permanent_audio_path = create_permanent_copy(audio_path, 'mp3')
                        
                        if permanent_audio_path:
                            # Save recent activity with output path
                            activity_id = save_recent_activity(
                                st.session_state.user["_id"], 
                                "Text to Speech", 
                                "Text", 
                                permanent_audio_path
                            )
                            
                            # Add download link
                            st.markdown(get_download_link(permanent_audio_path, "Download Audio File"), unsafe_allow_html=True)
                            
                            # Clean up temporary audio file
                            os.unlink(audio_path)
                        else:
                            st.error("Failed to save audio file.")
                    else:
                        st.error(f"Error: {error}")
                else:
                    st.error(f"Translation error: {error}")
        else:
            st.warning("Please enter some text to convert.")
    
    # Always show feedback form
    show_feedback_form("text_to_speech")

# Translation Page - Improved
def translation_page():
    if not check_login():
        return
    st.header("Text Translation")
    
    # Text input area with a label to avoid the warning
    input_text = st.text_area(
        "Enter the text you want to translate:",
        height=200,
        label_visibility="visible",
        key="translation_input_text"
    )
    
    source_lang = st.selectbox(
        "Select source language:", 
        list(LANGUAGE_TO_CODE.keys()),
        index=list(LANGUAGE_TO_CODE.keys()).index("English"),
        key="source_lang",
        label_visibility="visible"
    )
    
    target_lang = st.selectbox(
        "Select target language:", 
        list(LANGUAGE_TO_CODE.keys()),
        index=list(LANGUAGE_TO_CODE.keys()).index("Hindi"),
        key="target_lang",
        label_visibility="visible"
    )
    
    if st.button("Translate", key="translate_button"):
        if input_text:
            with st.spinner("Translating text..."):
                translated_text, error = translate_text(input_text, LANGUAGE_TO_CODE[target_lang], LANGUAGE_TO_CODE[source_lang])
                
                if translated_text:
                    st.success("Translation successful!")
                    st.subheader("Translated Text:")
                    st.markdown(f'<div class="translated-text">{translated_text}</div>', unsafe_allow_html=True)
                    
                    # Save recent activity
                    save_recent_activity(
                        st.session_state.user["_id"], 
                        "Text Translation", 
                        "Text"
                    )
                else:
                    st.error(f"Translation error: {error}")
        else:
            st.warning("Please enter some text to translate.")
    
    # Always show feedback form
    show_feedback_form("translation")


# Main Application Logic
def main():
    load_css()
    header()
    
    cleanup_old_files()
    # Initialize database
    init_db()
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home", key="sidebar_home"):
        st.session_state.current_page = "Home"
    if st.sidebar.button("Audio to Text", key="sidebar_audio_text"):
        st.session_state.current_page = "Audio to Text"
    if st.sidebar.button("PDF to Audio", key="sidebar_pdf_audio"):
        st.session_state.current_page = "PDF to Audio"
    if st.sidebar.button("Text to Speech", key="sidebar_text_speech"):
        st.session_state.current_page = "Text to Speech"
    if st.sidebar.button("Translation", key="sidebar_translation"):
        st.session_state.current_page = "Translation"
    if st.sidebar.button("FAQ", key="sidebar_FAQ"):
        st.session_state.current_page = "FAQ"
    if st.sidebar.button("Module History", key="sidebar_module_history"):
        st.session_state.current_page = "Module History"
    if st.sidebar.button("Dashboard", key="sidebar_dashboard"):
        st.session_state.current_page = "Dashboard"
    if st.sidebar.button("Login / Register", key="sidebar_login_register"):
        st.session_state.current_page = "Login / Register"
    
    # Page Routing
    if st.session_state.current_page == "Home":
        home_page()
    elif st.session_state.current_page == "FAQ":
        help_faq_page()
    elif st.session_state.current_page == "Audio to Text":
        audio_to_text_page()
    elif st.session_state.current_page == "PDF to Audio":
        pdf_to_audio_page()
    elif st.session_state.current_page == "Text to Speech":
        text_to_speech_page()
    elif st.session_state.current_page == "Translation":
        translation_page()
    elif st.session_state.current_page == "Login / Register":
        login_register_page()
    elif st.session_state.current_page == "Module History":
        module_history_page()
    elif st.session_state.current_page == "Dashboard":
        dashboard_page()
    
    # Footer
    st.markdown('<div class="footer">Multi Linguistic Audio Solution © 2025</div>', unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
