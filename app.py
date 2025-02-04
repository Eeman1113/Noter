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
    topic = st.text_input("Enter the topic you want to generate notes for", 
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
