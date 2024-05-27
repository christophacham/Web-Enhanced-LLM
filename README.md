# Web-Enhanced LLM

This project demonstrates how to set up and use a local language model (LLM) that can interact with the web. We will use the Mistral-7B-Instruct-v0.3-GGUF model and the EleutherAI GPT-J model. This guide will cover the installation of Rye for managing dependencies, configuring the project with PyCharm, downloading the LLM models, and testing the setup.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Downloading Models](#downloading-models)
4. [Project Setup](#project-setup)
5. [Configuring PyCharm](#configuring-pycharm)
6. [Running the Project](#running-the-project)
7. [Testing the Setup](#testing-the-setup)
8. [References](#references)

## Prerequisites

- Python 3.8 or higher
- Git
- Internet connection for downloading dependencies and models

## Installation

### Step 1: Install Rye

Rye is a tool for managing Python environments and dependencies.

```bash
curl -sSf https://install.rye-up.com | bash
```

### Step 2: Set Up Your Project

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Web-Enhanced-LLM.git
    cd Web-Enhanced-LLM
    ```

2. Initialize the project with Rye:

    ```bash
    rye init
    ```

3. Add necessary dependencies:

    ```bash
    rye add transformers flask requests beautifulsoup4
    ```

## Downloading Models

### Mistral-7B-Instruct-v0.3-GGUF

1. **Download the model** from the official source. Ensure you follow any provided instructions for downloading.

    ```bash
    # Example command (update with actual download link and instructions)
    wget https://path-to-mistral-model/mistral7B-Instruct-v0.3-GGUF.tar.gz
    tar -xzvf mistral7B-Instruct-v0.3-GGUF.tar.gz -C models/mistral7B
    ```

### EleutherAI GPT-J

1. **Download the model** from the Hugging Face Model Hub.

    ```bash
    git lfs install
    git clone https://huggingface.co/EleutherAI/gpt-j-6B
    ```

2. **Move the model files** to the appropriate directory:

    ```bash
    mv gpt-j-6B models/gpt-j
    ```

## Project Setup

1. **Create the project structure**:

    ```bash
    mkdir -p models/mistral7B
    mkdir -p models/gpt-j
    ```

2. **Update the Flask app** to load the downloaded models:

    ```python
    from flask import Flask, request, jsonify
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import requests
    from bs4 import BeautifulSoup

    app = Flask(__name__)

    # Load model and tokenizer
    model_name = "models/mistral7B"  # Update with actual path
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.json
        prompt = data.get("prompt", "")
        
        if "http" in prompt:
            url = prompt.split()[-1]
            web_content = get_web_content(url)
            if web_content:
                prompt = f"{prompt}\n\nExtracted web content:\n{web_content[:1000]}"
        
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=150)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": generated_text})

    def get_web_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def parse_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        return text

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

## Configuring PyCharm

1. **Open PyCharm** and select **Open** to open your project directory (`Web-Enhanced-LLM`).

2. **Configure the Project Interpreter**:
    - Go to `File` > `Settings` (or `PyCharm` > `Preferences` on macOS).
    - Navigate to `Project: Web-Enhanced-LLM` > `Python Interpreter`.
    - Click on the gear icon and select `Add...`.
    - Choose `Existing environment`.
    - Locate the Python interpreter managed by Rye. This is typically found under `~/.rye/tools/venv/bin/python`. Select this interpreter.

3. **Set Up a Run Configuration** for your Flask app:
    - Go to `Run` > `Edit Configurations...`.
    - Click the `+` icon to add a new configuration and select `Python`.
    - Name the configuration (e.g., `Run Flask App`).
    - Set the script path to the location of your `app.py` file.
    - Set the working directory to your project directory.
    - Ensure the Python interpreter is set to the one managed by Rye.

## Running the Project

1. **Run your Flask app** using the run configuration you set up:
    - Select the `Run Flask App` configuration from the top-right dropdown.
    - Click the green run button to start the Flask app.

2. **Test your Flask application**:
    - Use `curl` or a tool like Postman to send a POST request to your Flask app:

    ```bash
    curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Tell me about the latest news from https://example.com"}'
    ```

## Testing the Setup

1. **Test with a Real Existing Page**:
    - Choose a real existing page URL, for example, `https://www.bbc.com/news`.

    ```bash
    curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Tell me about the latest news from https://www.bbc.com/news"}'
    ```

    - The response should include a summary or relevant information extracted from the provided URL.

## References

- [Rye Installation Guide](https://rye-up.com/docs/installation)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/)

This README should guide you through the entire process of setting up, configuring, and running your Web-Enhanced LLM project. If you encounter any issues or have questions, please refer to the respective documentation or seek help from the community.
