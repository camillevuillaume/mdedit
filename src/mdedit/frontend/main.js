import EasyMDE from "easymde";
import "easymde/dist/easymde.min.css";
import "./style.css";


// Initialize the editor
const editor = new EasyMDE({
  element: document.getElementById("editor"),
  autosave: {
    enabled: true,
    uniqueId: "markdown-editor",
    delay: 1000,
  },
  spellChecker: false,
  toolbar: [
    "bold",
    "italic",
    "heading",
    "|",
    "quote",
    "unordered-list",
    "ordered-list",
    "|",
    "link",
    "image",
    "|",
    "preview",
    "side-by-side",
    "fullscreen",
    "|",
    "guide",
  ],
  placeholder: "Type your markdown here...",
});

console.log("EasyMDE initialized successfully!");

// Date picker functionality
let datePickerPopup = null;
let triggerPosition = null;
let dateKeydownHandler = null;

function createDatePicker() {
  const popup = document.createElement("div");
  popup.className = "date-picker-popup";
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

  datePickerPopup.style.display = "block";
  datePickerPopup.style.left = coords.left + "px";
  datePickerPopup.style.top = coords.bottom + "px";

  const dateInput = document.getElementById("date-input");
  dateInput.value = new Date().toISOString().split("T")[0];
  // Remove old event listeners if they exist
  if (dateKeydownHandler) {
    dateInput.removeEventListener("keydown", dateKeydownHandler);
  }

  // Create new handlers
  dateKeydownHandler = function(e) {
    if (e.key === "Enter") {
      insertDate(this.value);
    } else if (e.key === "Escape") {
      hideDatePicker();
    }
  };

  // Add event listeners
  dateInput.addEventListener("keydown", dateKeydownHandler);

  dateInput.focus();
}

function hideDatePicker() {
  if (datePickerPopup) {
    datePickerPopup.style.display = "none";
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

// Close date picker when clicking outside
document.addEventListener("click", function(e) {
  if (
    datePickerPopup &&
    datePickerPopup.style.display === "block" &&
    !datePickerPopup.contains(e.target) &&
    !e.target.classList.contains("CodeMirror")
  ) {
    const dateInput = document.getElementById("date-input");
    if (dateInput && dateInput.value) {
      insertDate(dateInput.value);
    }
    hideDatePicker();
  }
});

// Listen for change in editor
editor.codemirror.on("change", function(cm, change) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.mark_modified();
  }
  if (change.origin === "+input") {
    const cursor = cm.getCursor();
    const line = cm.getLine(cursor.line);
    const beforeCursor = line.substring(0, cursor.ch);

    if (beforeCursor.endsWith("/date")) {
      const coords = cm.cursorCoords(cursor, "page");
      triggerPosition = {
        start: { line: cursor.line, ch: cursor.ch - 5 },
        end: { line: cursor.line, ch: cursor.ch },
      };
      showDatePicker(coords);
    }
    else if (beforeCursor.endsWith("/complete")) {
      const triggerPos = {
        start: { line: cursor.line, ch: cursor.ch - 9 },
        end: { line: cursor.line, ch: cursor.ch },
      };
      const content = editor.value();
      completeText(content, triggerPos, cm);
    }
  }
});

// Function to call Python API for text completion
async function completeText(content, triggerPos, cm) {
  try {
    const completion = await window.pywebview.api.get_completion(content);
    if (completion) {
      cm.replaceRange(
        completion,
        triggerPos.start,
        triggerPos.end
      );
      cm.focus();
    }
  } catch (err) {
    console.error("Error during completion:", err);
  }
}

// Save to file functionality using PyWebView
document.getElementById("saveBtn").addEventListener("click", async () => {
  const content = editor.value();

  await window.pywebview.api.save_file(content).catch((err) => {
    console.error("Error:", err);
    alert("Error saving file");
  });
});

// Save as functionality using PyWebView
document.getElementById("saveAsBtn").addEventListener("click", async () => {
  const content = editor.value();

  await window.pywebview.api.save_file_as(content).catch((err) => {
    console.error("Error:", err);
    alert("Error saving file");
  });
});

// Open file functionality using PyWebView
document.getElementById("openBtn").addEventListener("click", async () => {
  await window.pywebview.api
    .open_file_dialog()
    .then((result) => {
      if (result.success) {
        editor.value(result.content);
      }
    })
    .catch((err) => {
      console.error("Error:", err);
      alert("Error opening file");
    });
});

document.getElementById("quitBtn").addEventListener("click", async () => {
  window.pywebview.api.quit_app();
});
