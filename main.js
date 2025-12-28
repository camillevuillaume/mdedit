import EasyMDE from 'easymde';
import 'easymde/dist/easymde.min.css';
import './style.css';

// Initialize the editor
const editor = new EasyMDE({
    element: document.getElementById('editor'),
    autosave: {
        enabled: true,
        uniqueId: 'markdown-editor',
        delay: 1000,
    },
    spellChecker: false,
    toolbar: [
        'bold',
        'italic',
        'heading',
        '|',
        'quote',
        'unordered-list',
        'ordered-list',
        '|',
        'link',
        'image',
        '|',
        'preview',
        'side-by-side',
        'fullscreen',
        '|',
        'guide'
    ],
    placeholder: 'Type your markdown here...',
});

console.log('EasyMDE initialized successfully!');

// Date picker functionality
let datePickerPopup = null;
let triggerPosition = null;

function createDatePicker() {
    const popup = document.createElement('div');
    popup.className = 'date-picker-popup';
    popup.innerHTML = `
        <input type="date" id="date-input" class="date-input" />
    `;
    document.body.appendChild(popup);
    return popup;
}

function showDatePicker(coords) {
    if (!datePickerPopup) {
        datePickerPopup = createDatePicker();
    }
    
    datePickerPopup.style.display = 'block';
    datePickerPopup.style.left = coords.left + 'px';
    datePickerPopup.style.top = coords.bottom + 'px';
    
    const dateInput = document.getElementById('date-input');
    dateInput.value = new Date().toISOString().split('T')[0];
    dateInput.focus();
    
    // Handle date selection
    dateInput.addEventListener('change', function() {
        insertDate(this.value);
    });
    
    // Handle Enter key
    dateInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            insertDate(this.value);
        } else if (e.key === 'Escape') {
            hideDatePicker();
        }
    });
}

function hideDatePicker() {
    if (datePickerPopup) {
        datePickerPopup.style.display = 'none';
    }
}

function insertDate(dateValue) {
    if (triggerPosition) {
        const doc = editor.codemirror.getDoc();
        doc.replaceRange(dateValue, triggerPosition.start, triggerPosition.end);
        editor.codemirror.focus();
    }
    hideDatePicker();
}

// Listen for /date trigger
editor.codemirror.on('change', function(cm, change) {
    if (change.origin === '+input') {
        const cursor = cm.getCursor();
        const line = cm.getLine(cursor.line);
        const beforeCursor = line.substring(0, cursor.ch);
        
        if (beforeCursor.endsWith('/date')) {
            const coords = cm.cursorCoords(cursor, 'page');
            triggerPosition = {
                start: { line: cursor.line, ch: cursor.ch - 5 },
                end: { line: cursor.line, ch: cursor.ch }
            };
            showDatePicker(coords);
        }
    }
});

// Close date picker when clicking outside
document.addEventListener('click', function(e) {
    if (datePickerPopup && !datePickerPopup.contains(e.target) && 
        !e.target.classList.contains('CodeMirror')) {
        hideDatePicker();
    }
});

// Save to file functionality using PyWebView
document.getElementById('saveBtn').addEventListener('click', async () => {
    const content = editor.value();
    
    // Wait for pywebview API to be ready
    await window.pywebview.api.save_file(content)
        .catch(err => {
            console.error('Error:', err);
            alert('Error saving file');
        });
});


// Open file functionality using PyWebView
document.getElementById('openBtn').addEventListener('click', async () => {
    // Wait for pywebview API to be ready
    await window.pywebview.api.open_file_dialog()
        .then(result => {
            if (result.success) {
                // Update the editor with the opened file content
                editor.value(result.content);
                // alert('File opened successfully!');
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert('Error opening file');
        });
});
