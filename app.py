from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import subprocess
import tempfile
import os

# Create the Flask application
app = Flask(__name__)

# Configure your OpenAI API key
client = OpenAI(api_key='enter API key here',)

@app.route('/')
def index():
    return render_template('index.html')

def convert_pseudocode(pseudocode, language):
    data = request.json
    
    prompt = f"""
    Convert the following pseudocode to {language} code:
    
    Pseudocode:
    {pseudocode}
    
    Please ensure the output is syntactically correct and can be executed directly. Do not include any additional comments or explanations. Only provide the necessary code to perform the described operations.
    
    {language} code:
    """

    # Create a chat completion with the file content as the user's message
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-3.5-turbo",
    )

    # Extract and return the generated text from the API response
    return chat_completion.choices[0].message.content.strip()

def run_cpp_code(code):
    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp_cpp_file:
        temp_cpp_file.write(code.encode('utf-8'))
        temp_cpp_file.flush()
        temp_cpp_file_name = temp_cpp_file.name

    exe_file = temp_cpp_file_name.replace('.cpp', '.out')
    compile_process = subprocess.run(['g++', temp_cpp_file_name, '-o', exe_file], capture_output=True, text=True)
    
    if compile_process.returncode != 0:
        os.remove(temp_cpp_file_name)
        return compile_process.stderr

    run_process = subprocess.run([exe_file], capture_output=True, text=True)
    os.remove(temp_cpp_file_name)
    os.remove(exe_file)
    
    if run_process.returncode != 0:
        return run_process.stderr
    
    return run_process.stdout

@app.route('/run', methods=['POST'])
def run_pseudocode():
    data = request.get_json()
    pseudocode = data.get('pseudocode')
    language = data.get('language')
    code = convert_pseudocode(pseudocode, language)

    
    if language == 'python':
        # Save the generated code to a temporary file
        with open("temp_code.py", "w") as file:
            file.write(code)
        
        # Execute the Python code
        try:
            result = subprocess.run(
                ['python', 'temp_code.py'],
                capture_output=True,
                text=True,
                timeout=500
            )
            output = result.stdout
        except:
            output = "Error: Code generation took too long or failed."
            
        # Clean up the temporary file
        os.remove("temp_code.py")

    elif language == 'cpp':
        # Execute the C++ code
        output = run_cpp_code(code)

    return jsonify({'output': output, 'code': code})

if __name__ == '__main__':
    app.run(debug=True)