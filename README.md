# CyberGuard Input Interceptor (V1 to V2 Evolution)

An intermediate, security-focused Django backend utility acting as an application architecture shield. It intercepts incoming form string payloads, scans them for malicious structural manipulation vectors (such as SQL Injection scripts and Cross-Site Scripting tags), blocks dangerous operations at the front door, and writes network footprints into a dedicated database audit trail.

📈 System Architectural Evolution

🟩 Version 1.0: View-Level Security Gate
In the initial development cycle, the validation and threat parsing logic were constructed directly inside specific application views using functional python loops.
* **Mechanism:** Intercept traffic page-by-page inside `views.py` using explicit conditional checks on incoming `request.POST` string variables.
* **Limitation:** Repetitive architecture. If the application expands to 50 separate forms, the check logic must be copied across all 50 views, creating unoptimized code and potential security holes.

🟨 Version 2.0 (Current): Global Middleware Shield & Network Tracking
The system architecture was upgraded to decouple security scanning from individual page logic entirely. The filter now operates as a central gateway layer sitting in front of the entire infrastructure, handing the heavy lifting to a specialized scanning module.
* **Global Interception:** Implemented a Custom Django Middleware class registered globally inside the core pipeline framework of `settings.py`. It evaluates every single web request entering the web server before it ever hits a URL path, view function, or database mapping.
* **Decoupled Threat Analyzer Engine:** Security logic is pulled completely out of views and middleware into an isolated `security_engine.py` component using pre-compiled Regular Expressions (RegEx), ensuring blazing-fast execution.
* **Advanced Metadata Parsing:** Incorporates deep network packet inspection utilizing the hidden `request.META` dictionary.
* **Hacker IP Logging:** Extracts the user's real-world network identification signature (`HTTP_X_FORWARDED_FOR` or `REMOTE_ADDR`), automatically tracking and logging the attacker's IP footprint right next to their malicious script string inside the database tables.

🗄️ Database Schema Design (models.py)

The relational database architecture is built across two separate tracking models designed using proper Python object structures:

1. **user_input Table:**
   * `text` (TextField): Stores clean, validated frontend string submissions.
   * `is_safe` (BooleanField, default=True): System validation flag tracking structural safety.
   * `created_at` (DateTimeField): Precision server timestamp of the ingestion event.

2. **sec_audit_log Table (The Threat Vault):**
   * `attempted_payload` (TextField): Isolates the raw malicious script or attack query character text safely without execution.
   * `flagged_keywords` (CharField): Captures the specific threat classifications and matched signatures that triggered the system alarm.
   * `timestamp` (DateTimeField): Records the exact millisecond the entry layer was blocked.
   * `ip_address` (GenericIPAddressField): Logs the active IP address network footprint of the source client machine.

⚙️ Core Threat Analysis Engine
The scanning layer bypasses basic string matching by utilizing high-performance Regex compilation structures, sanitizing whitespaces to intercept complex obfuscation patterns:
* **XSS Vector Matching:** Mitigation layer tracking `<script>` tags, javascript event execution triggers, and inline event hooks (`onerror`, `onload`).
* **SQLi Logic Matching:** Structural block protecting backend relational tables from True-Condition SQL Injections (such as variations of `1=1` or structural comment identifiers `--`, `#`, `/*`).

💻 Tech Stack & Engineering Focus
* **Framework:** Django 5.x / Python 3.x
* **Database Interface:** Django Object-Relational Mapping (ORM) & SQLite
* **Core Concepts Practiced:** Class-Based Middleware design, Decoupled Security Utility Separation, HTTP network header metadata parsing, multi-relational database logging, operational threat mitigation routing.
