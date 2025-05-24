# Advanced SQL Injection Scanner

A Python-based SQL Injection scanner to identify potential vulnerabilities in web applications.  
Tested on platforms like **DVWA** and custom login forms, this tool helps detect weak query handling practices.

---

## 🔍 Features

- 🧠 Scans web pages for SQL Injection vulnerabilities
- 📥 Injects over **100+ advanced SQLi payloads**
- 🎯 Supports both GET and POST requests
- 🧪 Tamper with query logic to reveal flaws
- 🔐 Designed for ethical testing and learning

---

## 🛠 Technologies Used

- Python 3
- `requests` for HTTP communication
- `re` for response pattern matching
- `tkinter` (if GUI is added)
- Custom payload list

---

## 🚀 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/chinnu75/SQL_Scanner.git
   cd SQL_Scanner
   ```

2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the scanner:
   ```bash
   python SQL_Scanner.py
   ```

4. Enter a vulnerable URL (e.g., from DVWA) and follow the prompts.

---

## 📁 File Structure

```
SQL_Scanner/
├── SQL_Scanner.py       # Main Python scanner script
├── payloads.txt         # (Optional) SQLi payload list
├── README.md            # Project documentation
└── LICENSE              # MIT License
```

---

## ⚠️ Disclaimer

> This tool is intended for **educational and authorized testing** only.  
> Do **not** use it on websites you don’t own or have permission to test.

---

## 👨‍💻 Author

**Kasturi Bharadwaj**  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/bharadwaj-kasturi-451a031a9)

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
