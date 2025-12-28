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
