# 🎓 Veriden – Smart Digital Attendance System

> **Say goodbye to proxy attendance. Say hello to accountability.**

Veriden is a **smart, secure digital attendance system** built to ensure genuine student participation during lectures. It combines **time-bound verification**, **focus tracking**, and **teacher-controlled reporting** to reduce proxy attendance while keeping the system fair and practical.

This project is designed as an **academic-ready, demo-friendly web application** with clean logic, clear workflows, and explainable design decisions.

---

## ✨ Why Veriden?

Traditional attendance systems fail because they:

* Rely on trust alone
* Are easy to manipulate
* Provide no behavioral insights

**Veriden fixes this** by adding verification, monitoring, and transparency — without overcomplicating things.

---

## 🚀 Key Features

### 👩‍🏫 Teacher Module

* Create lectures with **unique, time-sensitive codes**
* View **lecture-wise attendance reports**
* Identify **focus issues** during submissions
* Full control over attendance interpretation

### 👨‍🎓 Student Module

* Secure login-based attendance submission
* Enter lecture ID + verification code
* Focus tracking during submission
* Immediate feedback on attendance status

### 🛡️ Anti-Proxy Measures

* Time-bound lecture codes
* Focus/blur detection during submission
* Attendance flagged (not auto-penalized) for fairness

---

## 🧠 Smart Design Choices

* **Blur detection does NOT auto-mark absent**
  → Instead, it flags submissions for teacher review to avoid false penalties.

* **Attendance reports are lecture-specific**
  → Teachers only see data related to their own lectures.

* **Simple refresh-based updates**
  → Reliable, explainable, and exam-safe.

---

## 🧱 Tech Stack

| Layer      | Technology              |
| ---------- | ----------------------- |
| Backend    | Flask (Python)          |
| Frontend   | HTML, CSS               |
| Database   | MySQL                   |
| Auth       | Session-based login     |
| Deployment | Render (structure demo) |

---

## 📁 Project Structure

```
Veriden_mini_project/
│
├── app.py
├── db.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── student_submission.html
│   ├── submission_result.html
│   └── attendance_report.html

```

---

## 📊 Attendance Report Workflow

1. Teacher selects a **Lecture ID**
2. Attendance data is fetched from the database
3. Refreshing the page shows updated records

Simple. Transparent. Reliable.

---

## ⚙️ Setup Instructions (Local)

```bash
pip install -r requirements.txt
python app.py
```

Make sure MySQL is running and the database schema is set up correctly.

---

## 🔮 Future Enhancements

* Cloud database integration (Supabase / PostgreSQL)
* Real-time attendance updates
* Admin analytics dashboard
* Mobile-friendly UI

---

## 🎯 Academic Note

This project is implemented with a focus on **clarity, correctness, and explainability**, making it suitable for:

* College submissions
* Viva discussions
* Resume projects

---

## 👤 Author

**Poorvi Parashar**
B.Tech CSE Student

---

⭐ If you like this project, give it a star — it helps more than you think!
