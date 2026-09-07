require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs' } });

let editorInstance = null;
require(['vs/editor/editor.main'], function () {
    editorInstance = monaco.editor.create(document.getElementById('editor'), {
        value: 'def hello():\n    print("Hello, AI!")',
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false }
    });
});

const outputEl = document.getElementById('output');
const loadingOverlay = document.getElementById('loadingOverlay');
const featureSelect = document.getElementById('featureSelect');
const targetLangInput = document.getElementById('targetLang');
const toastEl = document.getElementById('toast');

// ----- Toast notification -----
let toastTimeout = null;
function showToast(message = 'Copied!', duration = 2000) {
    if (toastTimeout) clearTimeout(toastTimeout);
    toastEl.textContent = message;
    toastEl.classList.remove('hidden');
    // Trigger reflow for animation restart
    void toastEl.offsetWidth;
    toastEl.classList.add('show');
    toastTimeout = setTimeout(() => {
        toastEl.classList.remove('show');
        setTimeout(() => { toastEl.classList.add('hidden'); }, 300);
    }, duration);
}

// Toggle target language input
featureSelect.addEventListener('change', function () {
    targetLangInput.style.display = (this.value === 'convert') ? 'inline-block' : 'none';
});

// Show/hide loading
function setLoading(active) {
    loadingOverlay.style.display = active ? 'flex' : 'none';
}

// Update output
function setOutput(text, isError = false) {
    outputEl.innerHTML = text || 'No result.';
    outputEl.style.color = isError ? '#fca5a5' : '#e4e6eb';
}

// ----- Copy helper with robust fallback -----
function copyToClipboard(text, buttonElement) {
    // If no text, show an error toast
    if (!text || text.trim() === '') {
        showToast('Nothing to copy!', 1500);
        return;
    }

    // Try using the Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
            .then(() => {
                showToast('Copied!');
                // Visual feedback on the button
                const orig = buttonElement.innerHTML;
                buttonElement.innerHTML = '<i class="fas fa-check" style="color: #34d399;"></i>';
                setTimeout(() => { buttonElement.innerHTML = orig; }, 1500);
            })
            .catch(() => {
                // Fallback to execCommand
                fallbackCopy(text, buttonElement);
            });
    } else {
        // Fallback for older browsers or insecure contexts
        fallbackCopy(text, buttonElement);
    }
}

function fallbackCopy(text, buttonElement) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        showToast('Copied!');
        const orig = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-check" style="color: #34d399;"></i>';
        setTimeout(() => { buttonElement.innerHTML = orig; }, 1500);
    } catch (e) {
        showToast('Failed to copy', 1500);
    }
    document.body.removeChild(textarea);
}

// Clear output
document.getElementById('clearOutputBtn').addEventListener('click', function () {
    outputEl.innerHTML = `<div class="output-placeholder">
                            <i class="fas fa-lightbulb"></i>
                            <p>Your AI response will appear here...</p>
                          </div>`;
    outputEl.style.color = '#6b7280';
});

// Copy Editor
document.getElementById('copyEditorBtn').addEventListener('click', function () {
    const code = editorInstance.getValue();
    copyToClipboard(code, this);
});

// Copy Output
document.getElementById('copyOutputBtn').addEventListener('click', function () {
    // Use innerText to get plain text (or textContent as fallback)
    const text = outputEl.innerText || outputEl.textContent || '';
    copyToClipboard(text, this);
});

// Execute main action
document.getElementById('actionBtn').addEventListener('click', function () {
    const code = editorInstance.getValue();
    const feature = featureSelect.value;
    let endpoint = '/api/' + feature;
    let payload = { code: code };

    if (feature === 'generate') {
        payload = { prompt: code, language: 'Python' };
        endpoint = '/api/generate';
    } else if (feature === 'convert') {
        const target = targetLangInput.value || 'JavaScript';
        payload = { code: code, target: target };
        endpoint = '/api/convert';
    }

    setLoading(true);
    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            setOutput('❌ Error: ' + data.error, true);
        } else {
            setOutput(data.result || 'No content returned.');
        }
    })
    .catch(err => {
        setOutput('❌ Network error: ' + err.message, true);
    })
    .finally(() => {
        setLoading(false);
    });
});

// Quality analysis
document.getElementById('analyzeQualityBtn').addEventListener('click', function () {
    const code = editorInstance.getValue();
    setLoading(true);
    fetch('/api/analyze-quality', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            setOutput('❌ Error: ' + data.error, true);
            return;
        }
        let issuesText = data.issues.length ? data.issues.join('\n') : 'No issues detected.';
        setOutput(`📊 Quality Score: ${data.score}/100\n🧠 Complexity: ${data.complexity}\n\nIssues:\n${issuesText}`);
    })
    .catch(err => setOutput('❌ Error: ' + err.message, true))
    .finally(() => setLoading(false));
});

// GitHub repo analysis
document.getElementById('analyzeRepoBtn').addEventListener('click', function () {
    const url = document.getElementById('githubUrl').value.trim();
    if (!url) {
        setOutput('⚠️ Please enter a GitHub repository URL.', true);
        return;
    }
    setLoading(true);
    fetch('/api/analyze-github', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            setOutput('❌ Error: ' + data.error, true);
        } else {
            setOutput(data.result || 'No analysis result.');
        }
    })
    .catch(err => setOutput('❌ Error: ' + err.message, true))
    .finally(() => setLoading(false));
});