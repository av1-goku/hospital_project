from django.contrib import admin
from .models import Doctor, Patient, Ward, Bill, Attendance, Feedback, UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'mobile_no', 'city']
    list_filter = ['role', 'gender']
    search_fields = ['user__username', 'user__email', 'mobile_no']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['did', 'doctor_name', 'qualification', 'experience', 'salary', 'gender']
    list_filter = ['gender', 'qualification']
    search_fields = ['doctor_name', 'qualification', 'last_worked_hospital']
    ordering = ['-did']
    
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pid', 'patient_name', 'age', 'gender', 'consult_doctor', 'is_admitted', 'admission_date']
    list_filter = ['is_admitted', 'gender', 'consult_doctor']
    search_fields = ['patient_name', 'mobile_number', 'email']
    ordering = ['-admission_date']
    date_hierarchy = 'admission_date'
    
    actions = ['mark_as_discharged']
    
    def mark_as_discharged(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_admitted=False, discharge_date=timezone.now())
        self.message_user(request, f'{queryset.count()} patients marked as discharged.')
    mark_as_discharged.short_description = 'Mark selected patients as discharged'

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['wid', 'ward_name', 'ward_type', 'total_beds', 'room_type', 'cost']
    list_filter = ['room_type', 'ward_type']
    search_fields = ['ward_name', 'ward_type']
    ordering = ['-wid']

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bid', 'patient', 'consult_doctor', 'amount', 'payment_status', 'payment_method', 'bill_date']
    list_filter = ['payment_status', 'payment_method', 'bill_date']
    search_fields = ['patient__patient_name', 'contact_number']
    ordering = ['-bill_date']
    date_hierarchy = 'bill_date'
    readonly_fields = ['bill_date', 'created_by']
    
    actions = ['mark_as_paid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status='paid')
        self.message_user(request, f'{queryset.count()} bills marked as paid.')
    mark_as_paid.short_description = 'Mark selected bills as paid'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date_of_attendance', 'status', 'incoming_time', 'outgoing_time']
    list_filter = ['status', 'date_of_attendance']
    search_fields = ['staff__username']
    ordering = ['-date_of_attendance']
    date_hierarchy = 'date_of_attendance'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']
    search_fields = ['username', 'email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
