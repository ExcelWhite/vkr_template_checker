# vkr_template_checker

##📚 Academic PDF Verifier
This project is a comprehensive Python-based tool for automated verification of academic documents in PDF format, tailored for standards typically used in universities (e.g., ГОСТ). It inspects layout, structure, formatting, and semantic consistency.

##🔍 Features
✅ Page Number Check
Verifies that page numbers are present, sequential, and located correctly (usually at the bottom of each page).

📑 Table of Contents (TOC) Validation
Compares extracted TOC entries with actual document headings to identify missing or mismatched sections.

📖 Section Content Checks
Verifies whether specific sections like ВВЕДЕНИЕ, ЗАКЛЮЧЕНИЕ, and ПРИЛОЖЕНИЕ A start correctly with placeholder or expected content (e.g., the word "текст").

🧾 Reference List Validation
Checks for the presence of a properly formatted list under СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ. It validates numbering, structure, and ensures non-empty content.

🔡 Abbreviations Section Validation
Detects and evaluates entries under Список сокращений и условных обозначений using regex patterns to enforce the ABBR - Description format.

📊 Table Numbering Check
Ensures all tables follow correct hierarchical numbering like Таблица 1.1 – Title, based on the section they are in.

🧠 Technologies Used
Python 3.x

PyMuPDF (fitz) for PDF parsing

re for regex-based structure validation

Custom parsing logic for layout-aware verification
