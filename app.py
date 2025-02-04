# ver - 1
import streamlit as st
from groq import Groq
import time
import json


# Initialize Groq client
api_key = st.secrets.get("API_KEY")
client = Groq(api_key=api_key)

def generate_index(topic):
    """Generate a comprehensive index for the topic"""
    prompt = f"""Generate a detailed and comprehensive index for studying {topic} in computer science. Include:
    1. All major concepts and their sub-topics
    2. Practical applications and examples
    3. Common problems and solutions
    4. Best practices and guidelines
    Use ## for main sections and nested bullets for subsections.
    Make sure to cover both theoretical and practical aspects."""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating index: {str(e)}")
        return None

def generate_notes_for_header(header, topic):
    """Generate detailed notes for a specific header"""
    prompt = f"""Create comprehensive educational notes for the topic "{header}" in the context of {topic}. Include:
    1. Detailed explanation of concepts
    2. Real-world examples and applications
    3. Code examples where applicable
    4. Common pitfalls and how to avoid them
    5. Best practices and tips
    6. Related concepts and their connections
    7. Practice problems or exercises
    
    Format the response in clear markdown with appropriate sections and highlighting of key concepts."""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating notes for {header}: {str(e)}")
        return None

def save_notes_to_markdown(topic, index_content, detailed_notes):
    """Save notes to a markdown file with enhanced formatting"""
    filename = f"{topic.lower().replace(' ', '_')}_notes.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write title and metadata
            f.write(f"# Complete Study Guide: {topic.title()}\n\n")
            f.write(f"*Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("---\n\n")
            
            # Write table of contents
            f.write("# Table of Contents\n\n")
            f.write(index_content + "\n\n")
            f.write("---\n\n")
            
            # Write detailed notes
            f.write("# Detailed Notes\n\n")
            for section, notes in detailed_notes.items():
                f.write(f"## {section}\n\n")
                f.write(notes + "\n\n")
                f.write("---\n\n")
            
            # Write footer
            f.write("\n\n## Additional Resources\n\n")
            f.write("- Practice exercises and problems can be found in the respective sections\n")
            f.write("- Refer to the official documentation for more detailed information\n")
            f.write("- Consider joining relevant online communities for discussions\n")
        
        return filename
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Noter - Helps You Note Study And Code", layout="wide")
    
    # Custom CSS for better formatting
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stMarkdown {
            font-size: 1.1rem;
        }
        h1 {
            color: #1E88E5;
        }
        h2 {
            color: #424242;
            margin-top: 2rem;
        }
        code {
            background-color: #f5f5f5;
            padding: 0.2rem;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # st.title("📚 Noter ノート")
    
    st.markdown("<h1 style='text-align: center; '>📚 Noter ノート</h1>", unsafe_allow_html=True)
    st.markdown("Generate comprehensive study notes for any computer science topic")
    
    # User input
    topic = st.text_input("Enter the topic you want to generate notes for (currently only works for computer science related topics)", 
                         help="Example: Data Structures, Machine Learning, Web Development")
    
    if st.button("🚀 Generate Comprehensive Notes") and topic:
        try:
            with st.spinner("🔍 Analyzing topic and generating index..."):
                index_content = generate_index(topic)
                if not index_content:
                    st.error("Failed to generate index. Please try again.")
                    return
                
                st.markdown("### 📑 Generated Index")
                st.markdown(index_content)
                
                headers = [header.strip() for header in index_content.split('##') if header.strip()]
                detailed_notes = {}
                
                # Progress bar for note generation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, header in enumerate(headers):
                    progress = (i + 1) / len(headers)
                    progress_bar.progress(progress)
                    status_text.text(f"Generating notes for: {header}")
                    
                    notes = generate_notes_for_header(header, topic)
                    if notes:
                        detailed_notes[header] = notes
                    time.sleep(1)  # Rate limiting
                
                if detailed_notes:
                    filename = save_notes_to_markdown(topic, index_content, detailed_notes)
                    if filename:
                        st.success(f"✅ Notes successfully generated and saved to {filename}")
                        st.balloons()
                        
                        # Display notes in an expander
                        with st.expander("📖 View Complete Notes", expanded=True):
                            for header, notes in detailed_notes.items():
                                st.markdown(f"## {header}")
                                st.markdown(notes)
                                st.markdown("---")
                        
                        # Download button
                        with open(filename, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label="📥 Download Notes",
                                data=f.read(),
                                file_name=filename,
                                mime="text/markdown"
                            )
                    else:
                        st.error("Failed to save notes to file.")
                else:
                    st.error("Failed to generate detailed notes.")
                
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()




# ___________________________________________________________________________________________________________________________________________________________________________________

#ver - 2

# import streamlit as st
# from groq import Groq
# import time
# import json

# # Initialize Groq client
# api_key = st.secrets.get("API_KEY")
# client = Groq(api_key=api_key)

# def generate_index(topic):
#     """Generate a comprehensive index for the topic"""
#     prompt = f"""Generate a detailed and comprehensive index for studying {topic} in computer science. Include:
#     1. All major concepts and their sub-topics
#     2. Practical applications and examples
#     3. Common problems and solutions
#     4. Best practices and guidelines
#     Use ## for main sections and nested bullets for subsections.
#     Make sure to cover both theoretical and practical aspects."""
    
#     try:
#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=2048,
#             top_p=1,
#             stream=False
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error generating index: {str(e)}")
#         return None

# def generate_notes_for_header(header, topic):
#     """Generate detailed notes for a specific header"""
#     prompt = f"""Create comprehensive educational notes for the topic "{header}" in the context of {topic}. Include:
#     1. Detailed explanation of concepts
#     2. Real-world examples and applications
#     3. Code examples where applicable
#     4. Common pitfalls and how to avoid them
#     5. Best practices and tips
#     6. Related concepts and their connections
#     7. Practice problems or exercises
    
#     Format the response in clear markdown with appropriate sections and highlighting of key concepts."""
    
#     try:
#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=4096,
#             top_p=1,
#             stream=False
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error generating notes for {header}: {str(e)}")
#         return None

# def save_notes_to_markdown(topic, index_content, detailed_notes):
#     """Save notes to a markdown file with enhanced formatting"""
#     filename = f"{topic.lower().replace(' ', '_')}_notes.md"
    
#     try:
#         with open(filename, 'w', encoding='utf-8') as f:
#             # Write title and metadata
#             f.write(f"# Complete Study Guide: {topic.title()}\n\n")
#             f.write(f"*Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
#             f.write("---\n\n")
            
#             # Write table of contents
#             f.write("# Table of Contents\n\n")
#             f.write(index_content + "\n\n")
#             f.write("---\n\n")
            
#             # Write detailed notes
#             f.write("# Detailed Notes\n\n")
#             for section, notes in detailed_notes.items():
#                 f.write(f"## {section}\n\n")
#                 f.write(notes + "\n\n")
#                 f.write("---\n\n")
            
#             # Write footer
#             f.write("\n\n## Additional Resources\n\n")
#             f.write("- Practice exercises and problems can be found in the respective sections\n")
#             f.write("- Refer to the official documentation for more detailed information\n")
#             f.write("- Consider joining relevant online communities for discussions\n")
        
#         return filename
#     except Exception as e:
#         st.error(f"Error saving file: {str(e)}")
#         return None

# def main():
#     st.set_page_config(page_title="noter.ai - Your AI Study Companion", page_icon="📚", layout="wide")
    
#     # Custom CSS for chat-like interface and modern design
#     st.markdown("""
#         <style>
#         .stApp {
#             background-color: #f4f4f4;
#             font-family: 'Inter', sans-serif;
#         }
#         .chat-container {
#             max-width: 800px;
#             margin: auto;
#             background-color: white;
#             border-radius: 12px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#             padding: 20px;
#         }
#         .chat-header {
#             background-color: #1E88E5;
#             color: white;
#             padding: 15px;
#             border-radius: 12px 12px 0 0;
#             text-align: center;
#         }
#         .chat-input {
#             margin-bottom: 20px;
#         }
#         .stTextInput > div > div > input {
#             border-radius: 20px;
#             padding: 10px 15px;
#             font-size: 16px;
#         }
#         .stButton > button {
#             background-color: #1E88E5;
#             color: white;
#             border-radius: 20px;
#             padding: 10px 20px;
#             font-weight: bold;
#         }
#         .stButton > button:hover {
#             background-color: #1565C0;
#         }
#         .message-box {
#             background-color: #f0f0f0;
#             border-radius: 10px;
#             padding: 15px;
#             margin-bottom: 15px;
#         }
#         .user-message {
#             background-color: #E3F2FD;
#             text-align: right;
#         }
#         .ai-message {
#             background-color: #F1F8E9;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     # Chat-like main container
#     st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#     st.markdown('<div class="chat-header"><h1>noter.ai 📚</h1><p>Your AI Study Companion</p></div>', unsafe_allow_html=True)
    
#     # Conversational welcome message
#     st.markdown('<div class="message-box ai-message">Hi there! I\'m noter.ai, your AI study buddy. What computer science topic would you like me to help you create comprehensive notes for?</div>', unsafe_allow_html=True)
    
#     # User input with chat-like styling
#     topic = st.text_input("Enter your topic", 
#                           help="Example: Data Structures, Machine Learning, Web Development", 
#                           key="topic_input", 
#                           label_visibility="collapsed")
    
#     # Generate notes button
#     if st.button("🚀 Generate Study Notes", key="generate_button"):
#         if topic:
#             # User message
#             st.markdown(f'<div class="message-box user-message">Topic: {topic}</div>', unsafe_allow_html=True)
            
#             try:
#                 with st.spinner("🧠 Generating your personalized study notes..."):
#                     # Generate index
#                     index_content = generate_index(topic)
#                     if not index_content:
#                         st.error("Oops! Failed to generate index. Let's try again.")
#                         return
                    
#                     # AI response message
#                     st.markdown('<div class="message-box ai-message">', unsafe_allow_html=True)
#                     st.markdown("### 📑 Study Notes Index")
#                     st.markdown(index_content)
#                     st.markdown('</div>', unsafe_allow_html=True)
                    
#                     headers = [header.strip() for header in index_content.split('##') if header.strip()]
#                     detailed_notes = {}
                    
#                     # Progress visualization
#                     progress_bar = st.progress(0)
#                     status_text = st.empty()
                    
#                     for i, header in enumerate(headers):
#                         progress = (i + 1) / len(headers)
#                         progress_bar.progress(progress)
#                         status_text.text(f"Generating notes for: {header}")
                        
#                         notes = generate_notes_for_header(header, topic)
#                         if notes:
#                             detailed_notes[header] = notes
#                         time.sleep(1)  # Rate limiting
                    
#                     if detailed_notes:
#                         filename = save_notes_to_markdown(topic, index_content, detailed_notes)
#                         if filename:
#                             # Final AI message
#                             st.markdown('<div class="message-box ai-message">', unsafe_allow_html=True)
#                             st.success(f"✅ Your comprehensive study notes for *{topic}* are ready!")
#                             st.markdown('</div>', unsafe_allow_html=True)
                            
#                             # Detailed notes expander
#                             with st.expander("📖 Expand Full Notes", expanded=False):
#                                 for header, notes in detailed_notes.items():
#                                     st.markdown(f"## {header}")
#                                     st.markdown(notes)
#                                     st.markdown("---")
                            
#                             # Download button
#                             with open(filename, 'r', encoding='utf-8') as f:
#                                 st.download_button(
#                                     label="📥 Download Full Notes",
#                                     data=f.read(),
#                                     file_name=filename,
#                                     mime="text/markdown"
#                                 )
#                         else:
#                             st.error("Sorry, I couldn't save the notes. Let's try again.")
#                     else:
#                         st.error("I had trouble generating detailed notes. Can we try a different topic?")
                    
#             except Exception as e:
#                 st.error(f"An unexpected hiccup occurred: {str(e)}")
#         else:
#             st.warning("Please enter a topic to generate notes!")
    
#     # Close the chat container
#     st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
