# Hospital Management System

A comprehensive Django-based Hospital Management System with PostgreSQL database, modernizing the original Java/MySQL implementation.

## 🏥 Overview

This system provides complete hospital management functionality including patient admission/discharge, doctor management, billing, attendance tracking, and comprehensive reporting.

## ✨ Features

- 🔐 **Authentication & Authorization** - Role-based access (Admin, Doctor, Staff, Receptionist)
- 👨‍⚕️ **Doctor Management** - Complete CRUD operations for doctor records
- 🏥 **Patient Management** - Admission, discharge, and medical records
- 💰 **Billing System** - Automated billing with tax calculation (18% GST)
- 🛏️ **Ward Management** - Room and bed allocation
- 📊 **Reports** - Admission, revenue, and attendance reports
- 🔍 **Search** - Multi-field search for patients, doctors, and bills
- 📅 **Attendance** - Staff attendance tracking
- 💬 **Feedback** - Public feedback system
- ⚙️ **Admin Panel** - Comprehensive Django admin with custom actions

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip and virtualenv

### Installation

1. **Clone the repository** (if applicable)
```bash
cd /home/cdapatna/avi/hospital_project
```

2. **Activate virtual environment**
```bash
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install django psycopg2-binary
```

4. **Configure database**
Edit `hospital_project/settings.py` with your PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## 👥 User Roles

| Role | Access Level | Capabilities |
|------|-------------|--------------|
| **Admin** | Full access | All operations + reports + user management |
| **Doctor** | Limited | View patients, generate bills, reports |
| **Receptionist** | Patient focus | Admit/discharge patients, billing |
| **Staff** | Basic | View information, mark attendance |

## 📚 Usage

### Register a New User
1. Navigate to `/register/`
2. Fill in user details and select role
3. Submit registration
4. Login with credentials

### Admit a Patient
1. Navigate to Patients > Admit New Patient
2. Fill in patient details
3. Select consulting doctor
4. Submit admission

### Generate a Bill
1. Go to patient detail page
2. Click "Generate Bill"
3. Fill in billing details
4. Amount is automatically calculated with 18% GST
5. Select payment method and status
6. Generate and print bill

### View Reports
1. Navigate to Reports menu
2. Select report type (Admission/Revenue/Attendance)
3. Optional: Filter by date range
4. View statistics and detailed records

## 🗂️ Project Structure

```
hospital_project/
├── hospital/                    # Main Django app
│   ├── static/hospital/        # CSS, JS, images
│   ├── templates/hospital/     # HTML templates
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Django forms
│   ├── admin.py                # Admin configuration
│   └── urls.py                 # URL routing
├── hospital_project/           # Project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URL config
│   └── wsgi.py                # WSGI config
├── manage.py                   # Django management script
└── venv/                       # Virtual environment
```

## 🔧 Technology Stack

- **Backend**: Django 6.0.1
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Language**: Python 3.12

## 📊 Database Models

- **UserProfile** - Extended user with role and personal info
- **Doctor** - Doctor information and credentials
- **Patient** - Patient records and medical history
- **Ward** - Hospital ward and bed management
- **Bill** - Billing and payment tracking
- **Attendance** - Staff attendance records
- **Feedback** - User feedback

## 🔒 Security Features

- CSRF protection
- Password hashing
- SQL injection protection (ORM)
- Session management
- Login required decorators
- Role-based access control

## 📝 API Endpoints

### Authentication
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /logout/` - User logout
- `GET /dashboard/` - User dashboard

### Doctors
- `GET /doctors/` - List doctors
- `POST /doctors/add/` - Add doctor
- `GET /doctors/<id>/` - Doctor details
- `PUT /doctors/<id>/edit/` - Edit doctor
- `DELETE /doctors/<id>/delete/` - Delete doctor

### Patients
- `GET /patients/` - List patients
- `POST /patients/add/` - Admit patient
- `GET /patients/<id>/` - Patient details
- `POST /patients/<id>/discharge/` - Discharge patient
- `GET /patients/search/` - Search patients

### Bills
- `GET /bills/` - List bills
- `POST /bills/generate/<patient_id>/` - Generate bill
- `GET /bills/<id>/` - Bill details

### Reports
- `GET /reports/admissions/` - Admission report
- `GET /reports/revenue/` - Revenue report
- `GET /reports/attendance/` - Attendance report

## 🎨 UI Features

- Responsive design (mobile-friendly)
- Modern Bootstrap 5 interface
- Professional hospital-themed colors
- Interactive data tables
- Status badges
- Print-friendly bill layout
- Smooth animations

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

Check for issues:
```bash
python manage.py check
```

## 📦 Dependencies

- Django 6.0.1
- psycopg2-binary 2.9.11
- asgiref 3.11.0
- sqlparse 0.5.5

## 🔄 Development Workflow

1. Activate virtual environment
2. Make changes to code
3. Run migrations if models changed
4. Test changes locally
5. Commit changes

## 🚀 Deployment (Production)

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Use environment variables for secrets
4. Set up Gunicorn or uWSGI
5. Configure Nginx reverse proxy
6. Use PostgreSQL in production
7. Collect static files: `python manage.py collectstatic`
8. Set up SSL certificate

## 📄 License

[Your License Here]

## 👨‍💻 Authors

- Original Java/MySQL version: INDRA MOHAN
- Django/PostgreSQL version: [Your Name]

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome
- PostgreSQL Community

## 📞 Support

For issues and questions:
- Check the walkthrough.md for detailed documentation
- Review the implementation_plan.md for technical details
- Contact system administrator

---

**Built with ❤️ using Django & PostgreSQL**
