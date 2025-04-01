/*
    Filename: script.js
    Author: Bhuwan Shrestha, Alen Varghese, Shubh Soni, and Dev Patel
    Date: 2025-04-01
    Project: Handwritten OCR | Capstone Project 2025
    Course: Systems Project
    Description: This is the main JavaScript file for the Handwritten OCR project.
*/

function copyToClipboard(textareaId) {
    const textarea = document.getElementById(textareaId);
    textarea.select();
    navigator.clipboard.writeText(textarea.value);
    alert("Text copied to clipboard!");
}

function translateText(textId, langSelectId, outputId) {
    let text = document.getElementById(textId).value;
    let targetLang = document.getElementById(langSelectId).value;

    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `text=${encodeURIComponent(text)}&language=${targetLang}`
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById(outputId).innerText = data;
        })
        .catch(error => console.error('Translation error:', error));
}



function summarizeText(textareaId) {
    const text = document.getElementById(textareaId).value;
    fetch('/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `text=${encodeURIComponent(text)}`
    })
        .then(response => response.text())
        .then(data => document.getElementById(`summary-${textareaId}`).innerText = data);
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");
    localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
}

document.addEventListener("DOMContentLoaded", () => {
    const theme = localStorage.getItem("theme") || "light";
    document.body.classList.add(`${theme}-mode`);
});