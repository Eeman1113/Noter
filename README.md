# Noter : Making Notes Re-thought


Noter is a smart note-making app designed to help students and learners create comprehensive study materials effortlessly. Originally developed for my girlfriend while she was learning Java, Noter has evolved into a powerful tool for generating structured and detailed notes on any computer science topic.

---

## Features

- 📑 **Automated Study Guide Creation**: Generate a detailed index for any computer science topic.
- 📝 **Comprehensive Notes Generation**: Create structured, in-depth notes with explanations, examples, and best practices.
- 📂 **Markdown Export**: Save notes in a well-formatted Markdown file for easy sharing and reference.
- 🔍 **Real-World Applications**: Notes include real-life use cases and common pitfalls.
- 🚀 **Simple & Interactive UI**: Built with Streamlit for an intuitive and user-friendly experience.

---

## Getting Started

### Prerequisites
Ensure you have the following installed:

- Python 3.x
- Streamlit (`pip install streamlit`)
- `groq` library (`pip install groq`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Eeman1113/Noter.git
   cd noter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your API key in Streamlit secrets:
   ```bash
   mkdir -p ~/.streamlit
   echo "[secrets]\nAPI_KEY='your_api_key_here'" > ~/.streamlit/secrets.toml
   ```

---

## Usage

### Running the App
```bash
streamlit run app.py
```

### Generating Notes
1. Enter the topic (e.g., "Data Structures").
2. Click **"Generate Comprehensive Notes"**.
3. Wait for the structured index and notes to be generated.
4. View, download, or copy your notes in Markdown format.

---

## Roadmap
- [ ] Support for more subjects beyond computer science.
- [ ] Enhanced AI-generated diagrams and visual explanations.
- [ ] Collaboration features for shared note-taking.

---

## License
MIT License - Feel free to modify and contribute!

---

## Acknowledgments
- Inspired by the need for structured learning tools.
- Built with love ❤️ for better studying experiences!

---

## Repository
[GitHub Repository](https://github.com/Eeman1113/Noter)
