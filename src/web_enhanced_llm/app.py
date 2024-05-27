import requests  # Add this import statement
from bs4 import BeautifulSoup  # Add this import statement
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

# Load model and tokenizer
model_name = "mistral7B-Instruct-v0.3-GGUF"  # Replace with the actual path or model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    # Process the prompt (for example, to handle URLs or specific instructions)
    if "http" in prompt:  # Simple check to see if a URL is included
        url = prompt.split()[-1]
        web_content = get_web_content(url)
        if web_content:
            prompt = f"{prompt}\n\nExtracted web content:\n{web_content[:1000]}"  # Limit content length

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=150)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": generated_text})


# Add the web interaction functions here or import them
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
