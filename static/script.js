function runPseudocode() {
    const pseudocode = document.getElementById('pseudocode-input').value;
    const language = document.getElementById('language-select').value;
    fetch('/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pseudocode, language }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Timeout or error occurred while generating code');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('output').textContent = data.output;
        document.getElementById('generated-code').textContent = data.code; // assuming `data.code` contains the generated code
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').textContent = 'Error: Code generation took too long or failed.';
        document.getElementById('generated-code').textContent = 'The code was too long to be generated within the time limit.';
    });
}

function toggleGeneratedCode() {
    const codeSection = document.getElementById('code-section');
    const toggleButton = document.getElementById('toggle-code-button');
    if (codeSection.classList.contains('hidden')) {
        codeSection.classList.remove('hidden');
        toggleButton.textContent = 'Hide Generated Code';
    } else {
        codeSection.classList.add('hidden');
        toggleButton.textContent = 'Show Generated Code';
    }
}

