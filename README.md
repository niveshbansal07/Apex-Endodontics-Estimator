# 🦷 Endodontic Cost Estimator Tool (Python + EmailJS)

This is a self-contained cost estimation tool built using **Python (Flask)** and **EmailJS**. It does **not require a backend email server** and can be hosted independently or integrated into an existing website.

---

## 💻 What This Tool Does

- Patients select treatment and tooth type.
- Must accept 4 consent points.
- See cost estimate on screen.
- If patient selects “Yes, I’d like to be contacted,” they can enter optional details.
- Email is sent directly to: `info@apexendopllc.com` using EmailJS.
- Admin Panel (Password: `admin123`) to update prices without touching code.

---

## 🔐 How to Use the Admin Panel

1. Click on Admin Login on top right.
2. Enter admin DoctorId: `DoctorEC`
3. Enter admin Password: `apexsecure2024`
3. Update prices.
4. Click **Update** and the cost calculator updates instantly.

---

## 🧪 How to Run This Tool

### 1. Install Python & Flask
```bash
pip install flask


*Deploy the Python app on:

1.Render
2.PythonAnywhere
3.Railway

Embed the tool inside your website using an iframe where you want this tool in your website:

<iframe src="https://your-cost-tool-hosted-link.com" width="100%" height="600"></iframe>




