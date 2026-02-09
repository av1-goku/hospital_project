from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Doctor, Patient, Ward, Bill, Attendance, Feedback, UserProfile
from .forms import (UserRegistrationForm, LoginForm, DoctorForm, PatientForm, WardForm,
                   AttendanceForm, BillForm, FeedbackForm, SearchForm, DateRangeForm)
from datetime import datetime, timedelta

# ==================== Home & Authentication Views ====================

def index(request):
    """Homepage view"""
    return render(request, 'hospital/index.html')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = form.save()
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                mobile_no=form.cleaned_data['mobile_no']
            )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'hospital/auth/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'hospital/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def dashboard_view(request):
    """Dashboard view with statistics"""
    context = {
        'total_patients': Patient.objects.count(),
        'admitted_patients': Patient.objects.filter(is_admitted=True).count(),
        'total_doctors': Doctor.objects.count(),
        'total_revenue': Bill.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'recent_patients': Patient.objects.order_by('-admission_date')[:5],
        'recent_bills': Bill.objects.order_by('-bill_date')[:5],
    }
    return render(request, 'hospital/auth/dashboard.html', context)

@login_required
def change_password_view(request):
    """Password change view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'hospital/auth/change_password.html', {'form': form})

# ==================== Doctor Views ====================

@login_required
def add_doctor(request):
    """Add new doctor"""
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'hospital/doctor/add_doctor.html', {'form': form})

@login_required
def doctor_list(request):
    """List all doctors"""
    doctors = Doctor.objects.all().order_by('-did')
    return render(request, 'hospital/doctor/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_detail(request, did):
    """Doctor detail view"""
    doctor = get_object_or_404(Doctor, did=did)
    patients = doctor.patients.all()[:10]  # Recent 10 patients
    return render(request, 'hospital/doctor/doctor_detail.html', {
        'doctor': doctor,
        'patients': patients
    })

@login_required
def edit_doctor(request, did):
    """Edit doctor details"""
    doctor = get_object_or_404(Doctor, did=did)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', did=did)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor/edit_doctor.html', {'form': form, 'doctor': doctor})

@login_required
def delete_doctor(request, did):
    """Delete doctor"""
    doctor = get_object_or_404(Doctor, did=did)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully!')
    return redirect('doctor_list')

# ==================== Patient Views ====================

@login_required
def add_patient(request):
    """Admit new patient"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient admitted successfully!')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'hospital/patient/add_patient.html', {'form': form})

@login_required
def patient_list(request):
    """List all patients"""
    patients = Patient.objects.all().order_by('-admission_date')
    admitted_only = request.GET.get('admitted', False)
    if admitted_only:
        patients = patients.filter(is_admitted=True)
    return render(request, 'hospital/patient/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pid):
    """Patient detail view"""
    patient = get_object_or_404(Patient, pid=pid)
    bills = patient.bills.all()
    return render(request, 'hospital/patient/patient_detail.html', {
        'patient': patient,
        'bills': bills
    })

@login_required
def edit_patient(request, pid):
    """Edit patient details"""
    patient = get_object_or_404(Patient, pid=pid)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details updated successfully!')
            return redirect('patient_detail', pid=pid)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient/edit_patient.html', {'form': form, 'patient': patient})

@login_required
def discharge_patient(request, pid):
    """Discharge patient"""
    patient = get_object_or_404(Patient, pid=pid)
    if request.method == 'POST':
        patient.is_admitted = False
        patient.discharge_date = datetime.now()
        patient.save()
        messages.success(request, f'Patient {patient.patient_name} discharged successfully!')
        return redirect('patient_list')
    return render(request, 'hospital/patient/discharge_patient.html', {'patient': patient})

# ==================== Ward Views ====================

@login_required
def add_ward(request):
    """Add new ward"""
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward added successfully!')
            return redirect('ward_list')
    else:
        form = WardForm()
    return render(request, 'hospital/ward/add_ward.html', {'form': form})

@login_required
def ward_list(request):
    """List all wards"""
    wards = Ward.objects.all().order_by('-wid')
    return render(request, 'hospital/ward/ward_list.html', {'wards': wards})

@login_required
def ward_detail(request, wid):
    """Ward detail view"""
    ward = get_object_or_404(Ward, wid=wid)
    return render(request, 'hospital/ward/ward_detail.html', {'ward': ward})

# ==================== Bill Views ====================

@login_required
def generate_bill(request, patient_id):
    """Generate bill for patient"""
    patient = get_object_or_404(Patient, pid=patient_id)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.created_by = request.user
            bill.save()
            messages.success(request, f'Bill generated successfully for {patient.patient_name}!')
            return redirect('bill_detail', bill_id=bill.bid)
    else:
        form = BillForm(initial={
            'patient': patient,
            'consult_doctor': patient.consult_doctor,
            'diagnosis': patient.diagnosis,
            'contact_number': patient.mobile_number,
            'amount': patient.fee
        })
    return render(request, 'hospital/bill/generate_bill.html', {'form': form, 'patient': patient})

@login_required
def bill_list(request):
    """List all bills"""
    bills = Bill.objects.all().order_by('-bill_date')
    
    # Filter by payment status
    status = request.GET.get('status')
    if status:
        bills = bills.filter(payment_status=status)
    
    return render(request, 'hospital/bill/bill_list.html', {'bills': bills})

@login_required
def bill_detail(request, bill_id):
    """Bill detail view (for printing)"""
    bill = get_object_or_404(Bill, bid=bill_id)
    return render(request, 'hospital/bill/bill_detail.html', {'bill': bill})

@login_required
def update_bill_payment(request, bill_id):
    """Update bill payment status"""
    bill = get_object_or_404(Bill, bid=bill_id)
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        payment_method = request.POST.get('payment_method')
        bill.payment_status = payment_status
        bill.payment_method = payment_method
        bill.save()
        messages.success(request, 'Payment status updated successfully!')
        return redirect('bill_detail', bill_id=bill_id)

# ==================== Search Views ====================

@login_required
def search_patients(request):
    """Search patients"""
    form = SearchForm(request.GET or None)
    patients = None
    
    if form.is_valid() and form.cleaned_data['query']:
        query = form.cleaned_data['query']
        patients = Patient.objects.filter(
            Q(patient_name__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(email__icontains=query) |
            Q(pid__icontains=query)
        ).order_by('-admission_date')
    
    return render(request, 'hospital/patient/search_patients.html', {
        'form': form,
        'patients': patients
    })

@login_required
def search_doctors(request):
    """Search doctors"""
    form = SearchForm(request.GET or None)
    doctors = None
    
    if form.is_valid() and form.cleaned_data['query']:
        query = form.cleaned_data['query']
        doctors = Doctor.objects.filter(
            Q(doctor_name__icontains=query) |
            Q(qualification__icontains=query) |
            Q(did__icontains=query)
        )
    
    return render(request, 'hospital/doctor/search_doctors.html', {
        'form': form,
        'doctors': doctors
    })

@login_required
def search_bills(request):
    """Search bills"""
    form = SearchForm(request.GET or None)
    bills = None
    
    if form.is_valid() and form.cleaned_data['query']:
        query = form.cleaned_data['query']
        bills = Bill.objects.filter(
            Q(patient__patient_name__icontains=query) |
            Q(bid__icontains=query)
        ).order_by('-bill_date')
    
    return render(request, 'hospital/bill/search_bills.html', {
        'form': form,
        'bills': bills
    })

# ==================== Attendance Views ====================

@login_required
def mark_attendance(request):
    """Mark staff attendance"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'hospital/attendance/mark_attendance.html', {'form': form})

@login_required
def attendance_list(request):
    """List all attendance records"""
    attendances = Attendance.objects.all().order_by('-date_of_attendance')[:50]
    return render(request, 'hospital/attendance/attendance_list.html', {'attendances': attendances})

# ==================== Feedback Views ====================

def feedback_form(request):
    """Feedback form (public)"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, 'hospital/feedback/feedback_form.html', {'form': form})

@login_required
def feedback_list(request):
    """List all feedback (admin only)"""
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'hospital/feedback/feedback_list.html', {'feedbacks': feedbacks})

# ==================== Report Views ====================

@login_required
def admission_report(request):
    """Admission/Discharge report"""
    form = DateRangeForm(request.GET or None)
    admissions = Patient.objects.all()
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if start_date:
            admissions = admissions.filter(admission_date__gte=start_date)
        if end_date:
            admissions = admissions.filter(admission_date__lte=end_date)
    
    stats = {
        'total_admissions': admissions.count(),
        'currently_admitted': admissions.filter(is_admitted=True).count(),
        'discharged': admissions.filter(is_admitted=False).count(),
        'by_doctor': admissions.values('consult_doctor__doctor_name').annotate(count=Count('pid')).order_by('-count')
    }
    
    return render(request, 'hospital/reports/admission_report.html', {
        'form': form,
        'admissions': admissions.order_by('-admission_date')[:50],
        'stats': stats
    })

@login_required
def revenue_report(request):
    """Revenue report"""
    form = DateRangeForm(request.GET or None)
    bills = Bill.objects.all()
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if start_date:
            bills = bills.filter(bill_date__gte=start_date)
        if end_date:
            bills = bills.filter(bill_date__lte=end_date)
    
    stats = {
        'total_revenue': bills.aggregate(Sum('amount'))['amount__sum'] or 0,
        'paid_amount': bills.filter(payment_status='paid').aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_amount': bills.filter(payment_status='pending').aggregate(Sum('amount'))['amount__sum'] or 0,
        'by_payment_method': bills.values('payment_method').annotate(total=Sum('amount')).order_by('-total'),
        'by_doctor': bills.values('consult_doctor__doctor_name').annotate(total=Sum('amount')).order_by('-total')
    }
    
    return render(request, 'hospital/reports/revenue_report.html', {
        'form': form,
        'bills': bills.order_by('-bill_date')[:50],
        'stats': stats
    })

@login_required
def attendance_report(request):
    """Attendance report"""
    form = DateRangeForm(request.GET or None)
    attendances = Attendance.objects.all()
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if start_date:
            attendances = attendances.filter(date_of_attendance__gte=start_date)
        if end_date:
            attendances = attendances.filter(date_of_attendance__lte=end_date)
    
    stats = {
        'total_records': attendances.count(),
        'present_count': attendances.filter(status='present').count(),
        'absent_count': attendances.filter(status='absent').count(),
        'leave_count': attendances.filter(status='leave').count(),
        'by_staff': attendances.values('staff__username').annotate(count=Count('id')).order_by('-count')
    }
    
    return render(request, 'hospital/reports/attendance_report.html', {
        'form': form,
        'attendances': attendances.order_by('-date_of_attendance')[:50],
        'stats': stats
    })