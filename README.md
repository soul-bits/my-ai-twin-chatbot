# my-ai-twin-chatbot

An open-source, customizable framework for creating a personal, RAG-style AI assistant using OpenAI's GPT models. It ingests professional documents, provides conversational answers, and integrates custom functions for data logging (Pushover notifications).

## Features

- 🤖 **AI-Powered Chat Interface**: Built with Gradio, providing an intuitive chat experience
- 📄 **Document Ingestion**: Automatically processes LinkedIn profile PDFs and summary text files
- 🔧 **Custom Function Tools**: Integrates with Pushover for logging user interactions and unanswered questions
- 💬 **Conversational AI**: Uses OpenAI's GPT-4o-mini model to answer questions about your professional background
- 📝 **User Engagement Tracking**: Automatically records user contact information and questions that couldn't be answered

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Pushover account (optional, for notifications)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd my-ai-twin-chatbot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-dotenv openai requests pypdf gradio
```

**For Jupyter Notebook users:** If you plan to use Jupyter, also install:
```bash
pip install jupyter ipykernel
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key (required)
   - `NAME`: The name that the AI will use to represent itself (optional)
   - `PUSHOVER_TOKEN`: Your Pushover application token (optional)
   - `PUSHOVER_USER`: Your Pushover user key (optional)

3. Create a `me/` directory in the project root and add your documents:
   - `me/linkedin.pdf`: Your LinkedIn profile exported as PDF
   - `me/summary.txt`: A text summary of your professional background

## Usage

1. Activate the virtual environment (if not already activated):
```bash
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

2. Run the application:
```bash
python3 app.py
```

**Important:** Use `python3` (not `python`) to ensure you're using the virtual environment's Python interpreter. The `python` command may be aliased to your system Python.

The Gradio interface will launch in your browser. You can interact with your AI twin chatbot, which will answer questions about your professional background, skills, and experience.

**Note:** Make sure the virtual environment (`myenv`) is activated before running the application.

### Using Jupyter Notebook

You can also run this application as a Jupyter notebook. The same dependencies are required:

1. Install Jupyter and ipykernel in your virtual environment:
```bash
source myenv/bin/activate
pip install jupyter ipykernel
```

2. Register the virtual environment as a Jupyter kernel:
```bash
python3 -m ipykernel install --user --name=myenv --display-name "Python (myenv)"
```

3. Launch Jupyter:
```bash
jupyter notebook
```

4. Open your `.ipynb` file and select the "Python (myenv)" kernel from the kernel menu.

**Important:** The dependencies from `requirements.txt` must be installed in the Python environment that your Jupyter kernel uses. If you're using the `myenv` virtual environment kernel, the dependencies are already installed. If you're using a different kernel, install the dependencies in that environment.

## How It Works

1. **Document Loading**: On startup, the app loads your LinkedIn PDF and summary text file
2. **System Prompt**: Creates a personalized system prompt that instructs the AI to act as you
3. **Chat Interface**: Users can ask questions through the Gradio chat interface
4. **Tool Integration**: The AI can use custom functions to:
   - Record user contact information when users want to get in touch
   - Log questions that couldn't be answered for later review
5. **Pushover Notifications**: When tools are called, notifications are sent via Pushover (if configured)

## Customization

### Changing the AI Persona

Edit the `name` variable in the `Me` class `__init__` method (line 80) to change who the AI represents.

### Modifying the System Prompt

Edit the `system_prompt()` method in the `Me` class to customize how the AI behaves and responds.

### Adding Custom Tools

You can add additional custom functions by:
1. Creating a function (e.g., `my_custom_function`)
2. Creating a JSON schema for the function
3. Adding it to the `tools` list
4. The function will be automatically callable by the AI

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `NAME` | No | The name that the AI will use to represent itself (defaults to empty if not set) |
| `PUSHOVER_TOKEN` | No | Pushover application token for notifications |
| `PUSHOVER_USER` | No | Pushover user key for notifications |

## File Structure

```
my-ai-twin-chatbot/
├── app.py              # Main application file
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment file
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── LICENSE             # License file
├── myenv/              # Virtual environment (created during setup)
└── me/                 # Your personal documents (create this)
    ├── linkedin.pdf    # LinkedIn profile PDF
    └── summary.txt     # Professional summary text
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
