# 🎓 Vodenicharovi School

## 🧭 Project Overview

**"Vodenicharovi School"** is a web application developed using the Django Framework that serves as a platform for managing online courses. Its goal is to provide an intuitive and functional interface for both administrators and students — with capabilities for easy enrollment, management, and monitoring of the educational process.

---

## 🎯 Idea and Goals

The project aims to create a centralized system that:

- Provides easy registration and login for users.
- Offers a catalog of courses organized by subjects and teachers.
- Allows enrolling in and withdrawing from courses.
- Provides a personalized dashboard for each user.
- Facilitates content management for administrators.
- Ensures a responsive and user-friendly interface.

---

## ⚙️ How the Application Works

### 👤 Users and Profiles

- **Registration, Login/Logout** — complete authentication system.
- **Profiles** — automatically created upon registration via Django signals; includes additional info (phone, address, date of birth, profile photo).
- **Dashboard** — personalized page with profile and enrolled courses.
- **Edit Profile** — ability to update personal information.

### 📚 Course Management

- **Subjects** — categorization of courses.
- **Teachers** — bios and associated subjects.
- **Courses** — title, description, subject, teacher, price, dates, student limit.
- **CRUD Functionality** — create, read, update, and delete Subjects, Teachers, and Courses.
- **Detail Pages** — for each course, subject, and teacher.

### 📝 Enrollments

- **Enroll in Course** — available only to authenticated users.
- **Withdraw from Course** — accessible for students.
- **Enrollment List** — personalized view + admin control.
- **Enrollment Details** — view specific registration details.
- **Admin CRUD** — full management of enrollments.

### ➕ Additional Features

- 🔍 **Search and Filtering**
- 📄 **Pagination**
- 💬 **Message System (Django Messages Framework)**
- ⚠️ **Error Handling** (incl. 404, 500)
- 📱 **Responsive Design with Bootstrap**

---

## 🛠️ Technologies Used

| Component      | Technology                    |
|----------------|-------------------------------|
| Backend        | Django (Python)               |
| Database       | SQLite (default)              |
| Frontend       | HTML5, CSS3 (Bootstrap 5), JavaScript |
| Version Control| Git                           |

---

## 🚀 Installation and Running the Project

Follow the steps below to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/rvodenicharov/VodeniCharoviSchool.git
cd VodeniCharoviSchool

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Then open your web browser and go to:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧑‍💻 Author

Developed by **Rostislav Vodenicharov**
