"""
GermanLeap - Lea AI Tutor Frontend
A Streamlit-based interface for the German language learning AI tutor.
"""
import streamlit as st
from services.api_client import api_client

# Page configuration
st.set_page_config(
    page_title="GermanLeap - Lea AI Tutor",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1E3A5F;
        --secondary-color: #FFD700;
        --accent-color: #DD0000;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2E5A8F 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    .user-message {
        background-color: #E3F2FD;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #F5F5F5;
        margin-right: 2rem;
        border-left: 4px solid #1E3A5F;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Teaching mode buttons */
    .stButton > button {
        width: 100%;
    }
    
    /* Level badge */
    .level-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .level-A1 { background-color: #C8E6C9; color: #2E7D32; }
    .level-A2 { background-color: #B3E5FC; color: #0277BD; }
    .level-B1 { background-color: #FFE0B2; color: #EF6C00; }
    .level-B2 { background-color: #E1BEE7; color: #7B1FA2; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "student_profile" not in st.session_state:
        st.session_state.student_profile = None
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "teaching_mode" not in st.session_state:
        st.session_state.teaching_mode = None
    if "page" not in st.session_state:
        st.session_state.page = "auth"
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"  # 'login' or 'signup'


def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🇩🇪 GermanLeap - Lea AI Tutor</h1>
        <p>Your personal AI companion for mastering German</p>
    </div>
    """, unsafe_allow_html=True)


def render_auth_page():
    """Render the authentication page with login/signup options."""
    st.markdown("## Welcome to GermanLeap! 👋")
    st.markdown("""
    I'm **Lea**, your AI-powered German language tutor. I'm here to help you:
    
    - 📚 **Learn German** from A1 to B2 level
    - 📝 **Prepare for exams** (Goethe, Telc)
    - 💼 **Practice interviews** for German jobs
    - 🌍 **Navigate your journey** to Germany (Ausbildung, Nursing, etc.)
    """)
    
    st.markdown("---")
    
    # Toggle between Login and Signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True, 
                     type="primary" if st.session_state.auth_mode == "login" else "secondary"):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True,
                     type="primary" if st.session_state.auth_mode == "signup" else "secondary"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.auth_mode == "login":
        render_login_form()
    else:
        render_signup_form()


def render_login_form():
    """Render the login form."""
    st.markdown("### 🔑 Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email *", placeholder="e.g., priya@example.com")
        password = st.text_input("Password *", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("🔓 Login", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please fill in both email and password.")
            else:
                try:
                    with st.spinner("Logging in..."):
                        response = api_client.login(email=email, password=password)
                        st.session_state.student_profile = response["profile"]
                        st.session_state.page = "chat"
                        st.success("Login successful! 🎉")
                        st.rerun()
                except ConnectionError as e:
                    st.error(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
    
    st.markdown("---")
    st.markdown("Don't have an account? Click **Sign Up** above to create one.")


def render_signup_form():
    """Render the signup form."""
    st.markdown("### 📝 Create Your Account")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name *", placeholder="e.g., Priya Sharma")
            email = st.text_input("Email *", placeholder="e.g., priya@example.com")
            password = st.text_input("Password *", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
        
        with col2:
            current_level = st.selectbox(
                "Current German Level *",
                options=["A1", "A2", "B1", "B2"],
                help="Select your current German proficiency level"
            )
            goals = st.multiselect(
                "Learning Goals",
                options=[
                    "Basic communication",
                    "Grammar improvement",
                    "Vocabulary building",
                    "Speaking fluency",
                    "Exam preparation",
                    "Job interview preparation",
                    "Career in Germany"
                ],
                help="Select all that apply"
            )
            target_exam = st.selectbox(
                "Target Exam (optional)",
                options=["None", "Goethe A1", "Goethe A2", "Goethe B1", "Goethe B2", "Telc A1", "Telc A2", "Telc B1", "Telc B2"],
                help="If you're preparing for an exam"
            )
            career_interest = st.selectbox(
                "Career Interest (optional)",
                options=["None", "Ausbildung", "Nursing", "IT/Tech", "Engineering", "Healthcare", "Hospitality", "Other"],
                help="Your career goal in Germany"
            )
        
        submitted = st.form_submit_button("🚀 Create Account & Start Learning", use_container_width=True)
        
        if submitted:
            if not name or not email or not password:
                st.error("Please fill in all required fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                try:
                    with st.spinner("Creating your account..."):
                        response = api_client.signup(
                            name=name,
                            email=email,
                            password=password,
                            current_level=current_level,
                            goals=goals,
                            target_exam=target_exam if target_exam != "None" else None,
                            career_interest=career_interest if career_interest != "None" else None
                        )
                        st.session_state.student_profile = response["profile"]
                        st.session_state.page = "chat"
                        st.success("Account created successfully! 🎉")
                        st.rerun()
                except ConnectionError as e:
                    st.error(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
    
    st.markdown("---")
    st.markdown("Already have an account? Click **Login** above to sign in.")


def render_sidebar():
    """Render the sidebar with profile info and teaching modes."""
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        
        profile = st.session_state.student_profile
        if profile:
            st.markdown(f"**{profile['name']}**")
            level = profile['current_level']
            st.markdown(f"<span class='level-badge level-{level}'>{level}</span>", unsafe_allow_html=True)
            
            if profile.get('target_exam'):
                st.markdown(f"🎯 Target: {profile['target_exam']}")
            if profile.get('career_interest'):
                st.markdown(f"💼 Career: {profile['career_interest']}")
        
        st.markdown("---")
        st.markdown("### 📚 Teaching Mode")
        
        modes = {
            None: ("💬 Free Chat", "Open conversation with Lea"),
            "grammar_practice": ("📖 Grammar Practice", "Structured grammar lessons"),
            "vocabulary_building": ("📝 Vocabulary", "Learn new words in context"),
            "speaking_practice": ("🗣️ Speaking Practice", "Conversation practice"),
            "exam_preparation": ("📋 Exam Prep", "Goethe/Telc style questions"),
            "interview_coaching": ("💼 Interview Coaching", "Job interview practice"),
            "career_guidance": ("🌍 Career Guidance", "Advice for Germany journey")
        }
        
        for mode_key, (mode_label, mode_desc) in modes.items():
            is_selected = st.session_state.teaching_mode == mode_key
            if st.button(
                mode_label,
                key=f"mode_{mode_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                help=mode_desc
            ):
                st.session_state.teaching_mode = mode_key
                st.rerun()
        
        st.markdown("---")
        
        # New chat button
        if st.button("🔄 Start New Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.session_id = None
            st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.student_profile = None
            st.session_state.chat_messages = []
            st.session_state.session_id = None
            st.session_state.page = "welcome"
            st.rerun()


def render_chat_page():
    """Render the main chat interface."""
    render_sidebar()
    
    # Chat header with current mode
    mode_names = {
        None: "Free Chat",
        "grammar_practice": "Grammar Practice",
        "vocabulary_building": "Vocabulary Building",
        "speaking_practice": "Speaking Practice",
        "exam_preparation": "Exam Preparation",
        "interview_coaching": "Interview Coaching",
        "career_guidance": "Career Guidance"
    }
    current_mode = mode_names.get(st.session_state.teaching_mode, "Free Chat")
    
    st.markdown(f"### 💬 Chat with Lea - {current_mode}")
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        # Welcome message if no messages yet
        if not st.session_state.chat_messages:
            profile = st.session_state.student_profile
            welcome_text = f"""
            Hallo {profile['name']}! 👋
            
            I'm Lea, your German language tutor. I see you're at the **{profile['current_level']}** level.
            
            How can I help you today? You can:
            - Ask me grammar questions
            - Practice vocabulary
            - Have a conversation in German
            - Prepare for exams
            - Practice job interviews
            
            Just type your message below, or select a teaching mode from the sidebar!
            """
            with st.chat_message("assistant", avatar="🧑‍🏫"):
                st.markdown(welcome_text)
        
        # Display message history
        for msg in st.session_state.chat_messages:
            role = msg["role"]
            content = msg["content"]
            avatar = "👤" if role == "user" else "🧑‍🏫"
            with st.chat_message(role, avatar=avatar):
                st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Type your message to Lea..."):
        # Add user message to history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get response from Lea
        with st.chat_message("assistant", avatar="🧑‍🏫"):
            with st.spinner("Lea is thinking..."):
                try:
                    response = api_client.send_message(
                        student_id=st.session_state.student_profile["student_id"],
                        message=prompt,
                        session_id=st.session_state.session_id,
                        teaching_mode=st.session_state.teaching_mode
                    )
                    
                    # Update session ID
                    st.session_state.session_id = response["session_id"]
                    
                    # Display and store response
                    assistant_message = response["message"]
                    st.markdown(assistant_message)
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                except ConnectionError as e:
                    st.error(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def check_backend_connection():
    """Check if the backend is reachable."""
    try:
        api_client.health_check()
        return True
    except Exception:
        return False


def main():
    """Main application entry point."""
    init_session_state()
    render_header()
    
    # Check backend connection
    if not check_backend_connection():
        st.warning("""
        ⚠️ **Cannot connect to the backend server.**
        
        Please make sure the backend is running:
        ```bash
        cd backend
        python main.py
        ```
        
        The backend should be running at `http://localhost:8000`
        """)
        st.stop()
    
    # Route to appropriate page
    if st.session_state.student_profile is None:
        render_auth_page()
    else:
        render_chat_page()


if __name__ == "__main__":
    main()
