from django.db import models

# Create your models here.
class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=50)
    post = models.CharField((""), max_length=50)
    base_package = models.BigIntegerField((""))
    registered_date = models.DateField((""), auto_now=False, auto_now_add=False)

    
class Salary(models.Model):
    salary_id = models.AutoField(primary_key=True)
    salary_date = models.DateField(auto_now=False, auto_now_add=False)
    salary_for_month = models.IntegerField((""))
    emp_id = models.IntegerField((""))
    base_package = models.BigIntegerField(("")) 
    bonus_amount = models.IntegerField((""))
    deducted_amount = models.IntegerField((""))
    total_amount = models.IntegerField((""))
    status = models.CharField((""), max_length=50)
    
class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField((""))
    leave_date = models.DateField((""), auto_now=False, auto_now_add=False)
    requested_on = models.DateField((""), auto_now=False, auto_now_add=False)
    reason = models.CharField((""), max_length=50)
    status = models.IntegerField((""))
    
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField((""))
    employee_username = models.CharField(max_length=50)
    employee_password = models.CharField(max_length=50)
    
class Reduction(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField((""))
    deducted_amount = models.BigIntegerField((""))
    deducted_reason = models.CharField((""), max_length=50)
    leave_taken = models.DateField((""), auto_now=False, auto_now_add=False)
    reduction_for = models.IntegerField((""))
    
class OtherReduction(models.Model):
    emp_id = models.IntegerField((""))
    deducted_amount = models.BigIntegerField((""))
    deducted_reason = models.CharField((""), max_length=50)
    reduction_for = models.IntegerField((""))
    
class Bonus(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField((""))
    bonus_amount = models.BigIntegerField((""))
    reason = models.CharField((""), max_length=50)
    bonus_for = models.IntegerField((""))
    
class Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    username = models.CharField((""), max_length=50)
    password = models.CharField((""), max_length=50)
    
class LeaveStatus(models.Model):
    emp_id = models.IntegerField((""))
    sick_leave = models.IntegerField((""))
    casual_leave = models.IntegerField((""))
    half_day = models.IntegerField((""))
    paid_leave = models.IntegerField((""))
    status_upto = models.DateField((""), auto_now=False, auto_now_add=False)
    
class Approve(models.Model):
    status_name = models.CharField((""), max_length=50)

class Calender(models.Model):
    month_name = models.CharField((""), max_length=50)
    
class LeaveStatusMonth(models.Model):
    emp_id = models.IntegerField((""))
    sick_leave = models.IntegerField((""))
    casual_leave = models.IntegerField((""))
    half_day = models.IntegerField((""))
    paid_leave = models.IntegerField((""))
    status_upto = models.DateField((""), auto_now=False, auto_now_add=False)
    
class Halfday_leave(models.Model):
    emp_id = models.IntegerField((""))
    half_day = models.IntegerField((""))
    
class SalaryMonthwise(models.Model):
    salary_id = models.AutoField(primary_key=True)
    salary_date = models.DateField(auto_now=False, auto_now_add=False)
    salary_for_month = models.IntegerField((""))
    emp_id = models.IntegerField((""))
    base_package = models.BigIntegerField(("")) 
    bonus_amount = models.IntegerField((""))
    deducted_amount = models.IntegerField((""))
    total_amount = models.IntegerField((""))
    status = models.CharField((""), max_length=50)