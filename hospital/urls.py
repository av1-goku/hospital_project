# hospital/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ==================== Home & Auth ====================
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('change-password/', views.change_password_view, name='password_change'),
    
    # ==================== Doctor URLs ====================
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/<int:did>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:did>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:did>/delete/', views.delete_doctor, name='delete_doctor'),
    path('doctors/search/', views.search_doctors, name='search_doctors'),
    
    # ==================== Patient URLs ====================
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:pid>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pid>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:pid>/discharge/', views.discharge_patient, name='discharge_patient'),
    path('patients/search/', views.search_patients, name='search_patients'),
    
    # ==================== Ward URLs ====================
    path('wards/', views.ward_list, name='ward_list'),
    path('wards/add/', views.add_ward, name='add_ward'),
    path('wards/<int:wid>/', views.ward_detail, name='ward_detail'),
    
    # ==================== Bill URLs ====================
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/generate/<int:patient_id>/', views.generate_bill, name='generate_bill'),
    path('bills/<int:bill_id>/', views.bill_detail, name='bill_detail'),
    path('bills/<int:bill_id>/update-payment/', views.update_bill_payment, name='update_bill_payment'),
    path('bills/search/', views.search_bills, name='search_bills'),
    
    # ==================== Attendance URLs ====================
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    
    # ==================== Feedback URLs ====================
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('feedback/list/', views.feedback_list, name='feedback_list'),
    
    # ==================== Report URLs ====================
    path('reports/admissions/', views.admission_report, name='admission_report'),
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/attendance/', views.attendance_report, name='attendance_report'),
]