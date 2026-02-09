# Create your models here.
# hospital/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# This replaces the 'SignUp' and 'Login' tables using Django's built-in Auth
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('receptionist', 'Receptionist'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Doctor(models.Model):
    # Fields mapped from readadddoctor.jsp
    did = models.AutoField(primary_key=True)  # Auto-incrementing ID
    doctor_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    last_worked_hospital = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.doctor_name

class Patient(models.Model):
    # Fields mapped from readaddpatient.jsp ("addpatient" table)
    pid = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    address = models.TextField()
    consult_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
    problem = models.CharField(max_length=200)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    is_admitted = models.BooleanField(default=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    diagnosis = models.TextField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.patient_name} (PID: {self.pid})"

class Ward(models.Model):
    # Fields mapped from readaddward.jsp ("addward" table)
    wid = models.AutoField(primary_key=True)
    ward_name = models.CharField(max_length=50)
    ward_type = models.CharField(max_length=50) # e.g., Pediatrics
    ward_mode = models.CharField(max_length=50)
    total_beds = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=20) # AC/Non-AC

    def __str__(self):
        return self.ward_name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'On Leave'),
        ('half_day', 'Half Day'),
    ]
    
    # Fields mapped from readaddattendance.jsp
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date_of_attendance = models.DateField()
    incoming_time = models.TimeField(null=True, blank=True)
    outgoing_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    task_involved = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['staff', 'date_of_attendance']
        ordering = ['-date_of_attendance']
    
    def __str__(self):
        return f"{self.staff.username} - {self.date_of_attendance} ({self.status})"

class Bill(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partial'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]
    
    # Fields mapped from readbill.jsp
    bid = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    consult_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    diagnosis = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bill_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bills_created')
    
    def __str__(self):
        return f"Bill #{self.bid} - {self.patient.patient_name}"
    
    @property
    def tax_amount(self):
        """Calculate 18% GST"""
        return self.amount * Decimal('0.18')
    
    @property
    def total_amount(self):
        """Total including tax"""
        return self.amount + self.tax_amount
    
class Feedback(models.Model):
    # Fields mapped from readfeedback.jsp
    username = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.username} - {self.created_at.strftime('%Y-%m-%d')}"