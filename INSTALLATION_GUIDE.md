# 🏰 EstateWise Intelligence - Installation Guide

Welcome to the official installation guide for **EstateWise Intelligence**, a premium real estate price prediction system. Follow the steps below to set up your environment and launch the application.

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed on your system:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **MySQL Server**: [Download MySQL](https://dev.mysql.com/downloads/installer/) (Workbench is recommended for database management).
3.  **Git** (Optional): To clone the repository.

---

## 🚀 Setup Instructions

### 1. Clone or Extract the Project
If you haven't already, clone the repository or extract the ZIP file to your desired directory.
```bash
git clone https://github.com/Kraaatoast21/house-predictor.git
cd ESTATEWISE
```

### 2. Configure the Database
EstateWise uses MySQL to store user data and prediction history.

1.  Open **MySQL Workbench**.
2.  Run the provided script: `database_setup.sql`. This will:
    *   Create the `estatewise_db` database.
    *   Initialize the `users` and `predictions` tables.
    *   Create a default admin account.
3.  **Update Credentials**: Open `src/config.py` and update the `DB_CONFIG` with your MySQL root password:
    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_PASSWORD_HERE', # Update this!
        'database': 'estatewise_db',
        'port': 3306
    }
    ```

### 3. Install Dependencies
Open your terminal/command prompt in the project root directory and run:
```bash
pip install -r requirements.txt
```
*This installs: CustomTkinter, MySQL-Connector, Pandas, Scikit-Learn, Joblib, and Numpy.*

---

## 🖥 Running the Application

To launch the EstateWise dashboard, execute:
```bash
python main.py
```

### 🔑 Default Credentials
*   **Username**: `admin`
*   **Password**: `admin123`

---

## 🛡 System Security
*   **Password Hashing**: All passwords are automatically hashed using SHA-256 upon first run or registration.
*   **Session Management**: The system includes a secure session termination feature.

---

## 📁 Project Structure
*   `main.py`: Application entry point.
*   `src/`: Core logic, UI components, and database handlers.
*   `models/`: Pre-trained machine learning models.
*   `data/`: Datasets used for model training.

---
*Created with ✨ by Antigravity*
