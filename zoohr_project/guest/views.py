import datetime
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from guest.models import *

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Hi")
        adminlist = Admin.objects.filter(username=username,password=password)
        loginlist = Login.objects.filter(employee_username=username,employee_password=password)
        if adminlist.exists():
            request.session['username'] = username
            return JsonResponse({"admin":True})
        
        elif loginlist.exists():
            return JsonResponse({"employee":True})
        
        else:
            return JsonResponse({"fail":True})
        
@csrf_exempt        
def addemployee(request,id=0):
    if request.method == "POST":
        emp_name = request.POST.get('emp_name')
        emp_post = request.POST.get('emp_post')
        emp_pay = request.POST.get('emp_pay')
        emp_login = request.POST.get('emp_login')
        emp_pass = request.POST.get('emp_pass')
        date_now = datetime.date.today()
        next_year = date_now + datetime.timedelta(days=365)
        next_month = date_now + datetime.timedelta(days=31)
        employeelist = Employees()
        if Employees.objects.filter(employee_name = emp_name).exists():
            return JsonResponse({"fail":True}) 
        if Login.objects.filter(employee_username = emp_login).exists():
            return JsonResponse({"fail":True})
        else:
            employeelist.employee_name = emp_name
            employeelist.post = emp_post
            employeelist.base_package = emp_pay
            employeelist.registered_date = date_now
            employeelist.save()
            
            with connection.cursor() as cursor:
                sql_query = "SELECT (employee_id) FROM `guest_employees` ORDER BY employee_id DESC LIMIT 1"
                cursor.execute(sql_query)
                result = cursor.fetchone()
                
                
            employee_id = result[0]
            print(employee_id)
            loginlist = Login()
            loginlist.emp_id = employee_id
            loginlist.employee_username = emp_login
            loginlist.employee_password = emp_pass
            loginlist.save()
            
            
            
            leavestatuslist = LeaveStatus()
            leavestatuslist.emp_id = employee_id
            leavestatuslist.sick_leave = "6"
            leavestatuslist.casual_leave = "8"
            leavestatuslist.half_day = "16"
            leavestatuslist.paid_leave = "0"
            leavestatuslist.status_upto = next_year
            
            leavestatuslist.save()
            
            leavestatuslistformonth = LeaveStatusMonth()
            leavestatuslistformonth.emp_id = employee_id
            leavestatuslistformonth.sick_leave = "2"
            leavestatuslistformonth.casual_leave = "3"
            leavestatuslistformonth.half_day = "4"
            leavestatuslistformonth.paid_leave = "0"
            leavestatuslistformonth.status_upto = next_month
            leavestatuslistformonth.save()
            
            
            
            return JsonResponse({"success":True})
    
    elif request.method == "GET":
        employeelist = Employees.objects.all()
        data = [
            {
                'employee_name':item.employee_name,
                'employee_id':item.employee_id,
                'post':item.post,
                'basic_pay':item.base_package
            }
            for item in employeelist
        ]
        print(data)
        return JsonResponse(data,safe=False)
    
    elif request.method == "DELETE":
        employeelist = Employees.objects.get(employee_id=id)
        employeelist.delete()
        return JsonResponse({"sucess":True})
        
def getcount(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            sql_query = "SELECT COUNT(*) AS TOTAL FROM guest_employees"
            cursor.execute(sql_query)
            result = cursor.fetchone()
        total = result[0]
        print(total)
        return JsonResponse(total,safe=False)
        
def getdate(request):
    if request.method == "GET":
        date_now = datetime.date.today()
        print(date_now)
        return JsonResponse (date_now,safe=False)

@csrf_exempt    
def addbonus(request):
    if request.method == "POST":
        type = request.POST.get('type')
        emp_id = request.POST.get('employee_id')
        emp_amount = request.POST.get('emp_amount') 
        reason = request.POST.get('reason')
        with connection.cursor() as cursor:
            sql_query3 = "SELECT MONTH(CURRENT_DATE())"
            cursor.execute(sql_query3)
            result = cursor.fetchone()
            bonus_for = result[0]
        
        print(type)
        if type == '1':
            bonuslist = Bonus()
            
            bonuslist.emp_id = emp_id
            bonuslist.bonus_amount = emp_amount
            bonuslist.reason = reason
            salarylist = SalaryMonthwise.objects.filter(emp_id=emp_id,salary_for_month=bonus_for)
            if salarylist.exists():
                bonuslist.bonus_for = bonus_for + 1
            else:
                bonuslist.bonus_for = bonus_for
            bonuslist.save()
            return JsonResponse({"bonus":True})
        
        elif type == '2':
            reductionlist = OtherReduction()
            with connection.cursor() as cursor:
                sql_query3 = "SELECT MONTH(CURRENT_DATE())"
                cursor.execute(sql_query3)
                result = cursor.fetchone()
                reduction_for = result[0]
            reductionlist.emp_id = emp_id
            reductionlist.deducted_amount = emp_amount
            reductionlist.deducted_reason = reason
            salarylist = SalaryMonthwise.objects.filter(emp_id=emp_id,salary_for_month=reduction_for)
            if salarylist.exists():
                reductionlist.reduction_for = reduction_for + 1
            else:
                reductionlist.reduction_for = reduction_for
            reductionlist.save()
            return JsonResponse({"reduction":True})
        
    return JsonResponse({"fail":True})    
        
              
@csrf_exempt
def editform(request,id=0):
        if request.method == "GET":
            employeelist = Employees.objects.filter(employee_id=id)
            data = [
                {
                'employee_name':item.employee_name,
                'employee_id':item.employee_id,
                'post':item.post,
                'basic_pay':item.base_package,
                }
                for item in employeelist
            ]
            print(data)
            
            
            return JsonResponse(data,safe=False)
        
        elif request.method == "POST":
            employee_name = request.POST.get('emp_name')
            employee_post = request.POST.get('emp_post')
            employee_pay = request.POST.get('emp_pay')
            
            employeelist = Employees.objects.get(employee_id=id)
            employeelist.employee_name = employee_name
            employeelist.post = employee_post
            employeelist.base_package = employee_pay
            employeelist.save()
            
            return JsonResponse({"success":True})
 
@csrf_exempt       
def getemployee(request):
    if request.method == "POST":
         username = request.POST.get('username')
         password = request.POST.get('password')
         
         loginlist = Login.objects.get(employee_username = username,employee_password=password)
         emp_id = loginlist.emp_id
         logind = loginlist.login_id
         
         return JsonResponse({"emp_id":emp_id,"loginid":logind})
     
def getemployeebyid(request,id=0):
    if request.method == "GET":
       employeelist = Employees.objects.filter(employee_id=id) 
       data = [
            {
                'employee_name':item.employee_name,
                'employee_id':item.employee_id,
                'post':item.post,
                'basic_pay':item.base_package
            }
            for item in employeelist
        ]
    print(data)
    return JsonResponse(data,safe=False)

@csrf_exempt       
def submitleave(request):
    if request.method == "POST":
        date = request.POST.get('date')
        reason = request.POST.get('reason')
        emp_id = request.POST.get('emp_id')
        date_now = datetime.date.today()
        leavelist = Leave()
        
        leavelist.leave_date = date
        leavelist.reason = reason
        leavelist.emp_id = emp_id
        leavelist.requested_on = date_now
        leavelist.status = 2
        
        leavelist.save()
        
        return JsonResponse({"success":True})
    
    if request.method == "GET":
            sql_query ="SELECT * FROM `guest_leave` L INNER JOIN `guest_employees` e ON l.emp_id = e.employee_id inner join  `guest_approve` a ON l.status=a.id"
            result = Leave.objects.raw(sql_query)
            data = [
                {
                'leave_id':item.leave_id,
                'emp_name':item.employee_name,
                'leave_date':item.leave_date,
                'requested_on':item.requested_on,
                'reason':item.reason,
                'status':item.status_name,
                'emp_id':item.emp_id
                }
                for item in result
                
            ]
            
            return JsonResponse(data,safe=False)

def getleavestatusbyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_leave l inner join guest_approve a on l.status=a.id WHERE l.emp_id=%s"
        leavelist = Leave.objects.raw(sql_query,[id])
        data = [
                {
                'leave_id':item.leave_id,
                'leave_date':item.leave_date,
                'requested_on':item.requested_on,
                'reason':item.reason,
                'status':item.status_name
                }
                for item in leavelist
                
            ]
    return JsonResponse(data,safe=False)
        
@csrf_exempt        
def deleteleave(request,id=0):
    if request.method == "DELETE":
        leavelist = Leave.objects.filter(leave_id=id)
        leavelist.delete()
        
        return JsonResponse({"success":True})
    
def getcountofleavereq(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            sql_query = "SELECT COUNT(*) AS TOTAL FROM `guest_leave` WHERE status = '2'"
            cursor.execute(sql_query)
            result = cursor.fetchone()
            total = result[0]
            
            return JsonResponse(total,safe=False)
        
def approveleave(request,emp_id=0,leave_id=0):
    if request.method == "GET":
        print(emp_id)
        print(leave_id)
        leavelist = Leave.objects.get(leave_id=leave_id)
        leavelist.status = "1"
        leavetakendate = leavelist.leave_date
        leavelist.save()
        with connection.cursor() as cursor:
            sql_query3 = "SELECT MONTH(CURRENT_DATE())"
            cursor.execute(sql_query3)
            result = cursor.fetchone()
            reduction_for = result[0]
        leavestatuslist = LeaveStatus.objects.get(emp_id=emp_id)
        if leavelist.reason == "sick":
            print("sick")
            if leavestatuslist.sick_leave == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/30
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL SICK LEAVE TAKEN"
                reduction_list.reduction_for = reduction_for
                reduction_list.save()
                leavestatuslist.paid_leave += 1
                
            else:
                leavestatuslist.sick_leave -= 1
                
        elif leavelist.reason == "casual":
            if leavestatuslist.casual_leave == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/30
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL CASUAL LEAVE TAKEN"
                reduction_list.reduction_for = reduction_for
                reduction_list.save()
                leavestatuslist.paid_leave += 1
            else:
                    
                leavestatuslist.casual_leave -= 1
                
        elif leavelist.reason == "half-day":
            if leavestatuslist.half_day == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/60
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL HALF-DAY LEAVE TAKEN"
                reduction_list.reduction_for = reduction_for
                reduction_list.save()
                leavestatuslist.paid_leave += 1
            else:
                    
                leavestatuslist.half_day -= 1
            
        leavestatuslist.save()
        return JsonResponse({"success":True})
    
def generatesalary(request):
    if request.method == "GET":
        
        with connection.cursor() as cursor:
            sql_query = "SELECT (employee_id) FROM `guest_employees`"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            response  = []
            id_s = [emp_id[0] for emp_id in result]
            for id in id_s:
                data = {}
                employeelist = Employees.objects.get(employee_id=id)
                base_package = employeelist.base_package
                employee_name = employeelist.employee_name
                date_today = datetime.date.today()
                sql_query3 = "SELECT MONTH(CURRENT_DATE())"
                cursor.execute(sql_query3)
                result = cursor.fetchone()
                presentmonth = result[0]
                salarymonth = presentmonth - 1
                
                data["base_package"] = int(base_package)
                data["employee_name"] = employee_name
                data["date_today"] = date_today
                
                salaryformonth = SalaryMonthwise.objects.filter(emp_id=id,salary_for_month=salarymonth)
                if salaryformonth.exists():
                    if Salary.objects.filter(emp_id=id,salary_for_month=salarymonth).exists():
                        print("Hi")
                    else:    
                        salarylistmonth = SalaryMonthwise.objects.get(emp_id=id,salary_for_month=salarymonth)
                        credited_amount = salarylistmonth.base_package
                        month_bonus_amount = salarylistmonth.bonus_amount
                        month_deducted_amount = salarylistmonth.deducted_amount
                        
                        sql_query1 = f"SELECT SUM(bonus_amount) FROM guest_bonus WHERE emp_id = {id} and bonus_for = {salarymonth}"
                        cursor.execute(sql_query1)
                        result = cursor.fetchone()
                        bonus_amount = result[0]
                        if bonus_amount == None:
                            bonus_amount = 0 
                        
                        
                        
                        sql_query2 = f"SELECT SUM(deducted_amount) FROM guest_reduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
                        cursor.execute(sql_query2)
                        result = cursor.fetchone()
                        deducted_amount = result[0]
                        if deducted_amount == None:
                            deducted_amount = 0 
                        
                        sql_query4 = f"SELECT SUM(deducted_amount) FROM guest_otherreduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
                        cursor.execute(sql_query4)
                        result = cursor.fetchone()
                        otherdeducted_amount = result[0]
                        if otherdeducted_amount == None:
                            otherdeducted_amount = 0 
                        
                        total_deducted_amount = int(deducted_amount) + int(otherdeducted_amount)
                        
                        
                        total_amount = int(base_package) - int(total_deducted_amount) + int(bonus_amount)
                    
                        extra_bonus =  int(bonus_amount) - int(month_bonus_amount)
                        extra_deductions = int(total_deducted_amount) - int(month_deducted_amount)   
                        amount = int(base_package) - int(credited_amount)
                        credit_amount = int(amount) + int(extra_bonus) - int(extra_deductions)
                    
                        salarylist = Salary()
                        salarylist.salary_date = date_today
                        salarylist.base_package = int(base_package) - int(credited_amount)
                        salarylist.emp_id = id
                        salarylist.bonus_amount = int(bonus_amount) - int(month_bonus_amount)
                        salarylist.deducted_amount = int(total_deducted_amount) - int(month_deducted_amount)
                        salarylist.total_amount =  credit_amount
                        salarylist.status = 2
                        salarylist.salary_for_month = salarymonth
                        salarylist.save()
                    
                else:
                
                    sql_query1 = f"SELECT SUM(bonus_amount) FROM guest_bonus WHERE emp_id = {id} and bonus_for = {salarymonth}"
                    cursor.execute(sql_query1)
                    result = cursor.fetchone()
                    bonus_amount = result[0]
                    if bonus_amount == None:
                        bonus_amount = 0 
                    data["bonus_amount"] = int(bonus_amount)
                    
                    
                    sql_query2 = f"SELECT SUM(deducted_amount) FROM guest_reduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
                    cursor.execute(sql_query2)
                    result = cursor.fetchone()
                    deducted_amount = result[0]
                    if deducted_amount == None:
                        deducted_amount = 0 
                    
                    sql_query4 = f"SELECT SUM(deducted_amount) FROM guest_otherreduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
                    cursor.execute(sql_query4)
                    result = cursor.fetchone()
                    otherdeducted_amount = result[0]
                    if otherdeducted_amount == None:
                        otherdeducted_amount = 0 
                    
                    total_deducted_amount = int(deducted_amount) + int(otherdeducted_amount)
                    data["deducted_amount"] = int(total_deducted_amount)
                    
                    total_amount = int(base_package) - int(total_deducted_amount) + int(bonus_amount)
                    data["total_amount"] = int(total_amount)
                    
                    response.append(data)
                    
                    salarylist = Salary()
                        
                    if Salary.objects.filter(emp_id=id,salary_for_month=salarymonth).exists():
                        
                        print(id)
                        
                    else:
                        salarylist.salary_date = date_today
                        salarylist.base_package = int(base_package)
                        salarylist.emp_id = id
                        salarylist.bonus_amount = int(bonus_amount)
                        salarylist.deducted_amount = int(deducted_amount)
                        salarylist.total_amount = int(total_amount)
                        salarylist.status = 2
                        salarylist.salary_for_month = salarymonth
                        salarylist.save()
                    
                    
                    
                    
    return JsonResponse({"success":True})


def viewsalary(request):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_salary` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.status = 2"
        result = Salary.objects.raw(sql_query)
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)

def proceedsalary(request,id=0):
    if request.method == "GET":
        salarylist = Salary.objects.get(salary_id=id)
        salarylist.status = 1
        salarylist.save()
        emp_id = salarylist.emp_id
        print(emp_id)
        leavestatuslist = LeaveStatus.objects.get(emp_id=emp_id)
        
        leavestatuslist.paid_leave = 0
        
    return JsonResponse({"success":True})

def viewsalarygenerated(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_salary` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.status = 1"
        result = Salary.objects.raw(sql_query)
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)

def getsalarybyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_salary` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.emp_id=%s"
        result = Salary.objects.raw(sql_query,[id])
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)

def getleavebyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_leavestatus` WHERE emp_id = %s"
        result = LeaveStatus.objects.raw(sql_query,[id])
        data = [
            {
                'sick_leave':item.sick_leave,
                'casual_leave':item.casual_leave,
                'paid_leave':item.paid_leave,
                'half_day':item.half_day
            }
            for item in result
        ]
        return JsonResponse(data,safe=False)
    
@csrf_exempt    
def forgetpassword(request):
    if request.method == "POST":
        username = request.POST.get('username')
        
        
        if Login.objects.filter(employee_username=username).exists():
            
            return JsonResponse ({"success":True})
        else:
            
            return JsonResponse ({"fail":True})
        
@csrf_exempt
def changepassword(request):
    if request.method == "POST":
        id = request.POST.get('id')
        password = request.POST.get('password')
        
        loginobjects = Login.objects.get(employee_username=id)
        loginobjects.employee_password = password
        loginobjects.save()
        
        return JsonResponse({"success":True})
        
def generatesalaryforthismonth(request,id=0):
    if request.method == "GET":
        employeelist = Employees.objects.get(employee_id=id)
        base_package = employeelist.base_package
        
        with connection.cursor() as cursor:
            sql_query3 = "SELECT MONTH(CURRENT_DATE())"
            cursor.execute(sql_query3)
            result = cursor.fetchone()
            salarymonth = result[0]
            
            start_day = f'2024-0{salarymonth}-01'
            start_day = datetime.datetime.strptime(start_day,"%Y-%m-%d").date()
            date_today = datetime.date.today()
            working_days = (date_today-start_day).days
            salary_amount = (base_package/30)*working_days
            
                
            sql_query1 = f"SELECT SUM(bonus_amount) FROM guest_bonus WHERE emp_id = {id} and bonus_for = {salarymonth}"
            cursor.execute(sql_query1)
            result = cursor.fetchone()
            bonus_amount = result[0]
            if bonus_amount == None:
                bonus_amount = 0 
            
            
            
            sql_query2 = f"SELECT SUM(deducted_amount) FROM guest_reduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
            cursor.execute(sql_query2)
            result = cursor.fetchone()
            deducted_amount = result[0]
            if deducted_amount == None:
                deducted_amount = 0 
            
            sql_query4 = f"SELECT SUM(deducted_amount) FROM guest_otherreduction WHERE emp_id = {id} and reduction_for = {salarymonth}"
            cursor.execute(sql_query4)
            result = cursor.fetchone()
            otherdeducted_amount = result[0]
            if otherdeducted_amount == None:
                otherdeducted_amount = 0 
            
            total_deducted_amount = int(deducted_amount) + int(otherdeducted_amount)
           
            
            total_amount = round(salary_amount) - int(total_deducted_amount) + int(bonus_amount)
            
            
            
            
            salarylist = SalaryMonthwise()
                
            if SalaryMonthwise.objects.filter(emp_id=id,salary_for_month=salarymonth).exists():
                
                return JsonResponse({"exists":True})
                
            else:
                salarylist.salary_date = date_today
                salarylist.base_package = round(salary_amount)
                salarylist.emp_id = id
                salarylist.bonus_amount = int(bonus_amount)
                salarylist.deducted_amount = int(total_deducted_amount)
                salarylist.total_amount = int(total_amount)
                salarylist.status = 2
                salarylist.salary_for_month = salarymonth
                salarylist.save()
                
                
                    
                    
    return JsonResponse({"success":True})    

def viewsalaryforthismonth(request,id=0):
    if request.method == "GET":
        with connection.cursor() as cursor:
            sql_query1 = "SELECT MONTH(CURRENT_DATE())"
            cursor.execute(sql_query1)
            result = cursor.fetchone()
            this_month = result[0]
        sql_query = f"SELECT * FROM `guest_salarymonthwise` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.status = 2 and s.salary_for_month={this_month}"
        result = SalaryMonthwise.objects.raw(sql_query)
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)
        
        
def getbonusbyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_bonus` b INNER JOIN guest_calender c ON b.bonus_for = c.id WHERE b.emp_id =%s"
        result = Bonus.objects.raw(sql_query,[id])
        data = [
            {
                'bonus_amount':item.bonus_amount,
                'reason':item.reason,
                'month':item.month_name,
                'id':item.id
            }
            for item in result
        ]
        return JsonResponse(data,safe=False)
    
def getdeductionbyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_reduction r INNER JOIN guest_calender c ON r.reduction_for = c.id WHERE r.emp_id = %s"
        result = Reduction.objects.raw(sql_query,[id])
        data = [
            {
                'id':item.id,
                'deducted_amount':item.deducted_amount,
                'deducted_reason':item.deducted_reason,
                'leave_taken':item.leave_taken,
                'month':item.month_name
            }
            for item in result
        ]
        
        return JsonResponse(data,safe=False)
    
def getotherdeductionbyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_otherreduction r INNER JOIN guest_calender c ON r.reduction_for = c.id WHERE r.emp_id = %s"
        result = Reduction.objects.raw(sql_query,[id])
        data = [
            {   'id':item.id,
                'deducted_amount':item.deducted_amount,
                'deducted_reason':item.deducted_reason,
                'month':item.month_name
            }
            for item in result
        ]
        
        return JsonResponse(data,safe=False)
    
def getallbonus(request):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_bonus` b INNER JOIN guest_calender c ON b.bonus_for = c.id inner join guest_employees e on e.employee_id = b.emp_id"
        result = Bonus.objects.raw(sql_query)
        data = [
            {
                'employee_name':item.employee_name,
                'bonus_amount':item.bonus_amount,
                'reason':item.reason,
                'month':item.month_name,
                'id':item.id
            }
            for item in result
        ]
        return JsonResponse(data,safe=False)
    
def getalldeductions(request):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_reduction r INNER JOIN guest_calender c ON r.reduction_for = c.id inner join guest_employees e on e.employee_id = r.emp_id"
        result = Reduction.objects.raw(sql_query)
        data = [
            {   'employee_name':item.employee_name,
                'deducted_amount':item.deducted_amount,
                'deducted_reason':item.deducted_reason,
                'leave_taken':item.leave_taken,
                'month':item.month_name,
                'id':item.id
                
            }
            for item in result
        ]
        
        return JsonResponse(data,safe=False)
    
def getallotherdeductions(request):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_otherreduction r INNER JOIN guest_calender c ON r.reduction_for = c.id inner join guest_employees e on e.employee_id = r.emp_id"
        result = Reduction.objects.raw(sql_query)
        data = [
            {   'id':item.id,
                'employee_name':item.employee_name,
                'deducted_amount':item.deducted_amount,
                'deducted_reason':item.deducted_reason,
                'month':item.month_name
            }
            for item in result
        ]
        
        return JsonResponse(data,safe=False)
    
def gethalfday(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `halfday_leave` WHERE emp_id=%s"
        result = Halfday_leave.objects.raw(sql_query,[id])
        data = [
            {
                'count':item.half_day
            }
            for item in result
        ]
        count = data[0]['count']
        if count == None:
            count = 0        
        return JsonResponse({"count":count})
    
def getstatusmonthbyid(request,id):
    if request.method == "GET":
        leave = LeaveStatusMonth.objects.filter(emp_id=id)
        data = [
            {
                'sickleave':item.sick_leave,
                'casual_leave':item.casual_leave,
                'paidleave':item.paid_leave,
                'halfday':item.half_day,
            }
            for item in leave
        ]
        
        return JsonResponse(data,safe=False)
    
def updatestatusinleavemonth(request,id=0):
    if request.method == "GET":
            date = datetime.date.today()
            leave = LeaveStatusMonth.objects.get(emp_id=id)
            print(leave.status_upto,date)
            if date > leave.status_upto:
                leave.casual_leave = '3'
                leave.sick_leave = '2'
                leave.half_day = '4'
                leave.paid_leave = '0'
                leave.status_upto += datetime.timedelta(days=31)
                leave.save()
                print("update")
                return JsonResponse({"success":True})
            else:
                return JsonResponse({"success":True})

def leavemonth(request,emp_id=0,leave_id=0):
    if request.method == "GET":
        print(emp_id)
        print(leave_id)
        leavelist = Leave.objects.get(leave_id=leave_id)
        leavetakendate = leavelist.leave_date
        with connection.cursor() as cursor:
            sql_query3 = "SELECT MONTH(CURRENT_DATE())"
            cursor.execute(sql_query3)
            result = cursor.fetchone()
            reduction_for = result[0]
        leavemonth = LeaveStatusMonth.objects.get(emp_id=emp_id)
        if leavelist.reason == "sick":
            if leavemonth.sick_leave == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/30
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL SICK LEAVE TAKEN"
                reduction_list.reduction_for = reduction_for
                reduction_list.save()
                leavemonth.paid_leave += 1
                
            else:
                leavemonth.sick_leave -= 1
                
        elif leavelist.reason == "casual":
            if leavemonth.casual_leave == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/30
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL CASUAL LEAVE TAKEN"
                reduction_list.save()
                leavemonth.paid_leave += 1
            else:
                    
                leavemonth.casual_leave -= 1
                
        elif leavelist.reason == "half-day":
            if leavemonth.half_day == 0:
                with connection.cursor() as cursor:
                    sql_query = "SELECT (base_package) FROM `guest_employees` WHERE employee_id=%s"
                    cursor.execute(sql_query,emp_id)
                    result = cursor.fetchone()
                    base_package = result[0]
                    base_package_perday = int(base_package)/60
                    
                reduction_list = Reduction()
                reduction_list.emp_id = emp_id
                reduction_list.leave_taken = leavetakendate
                reduction_list.deducted_amount = base_package_perday
                reduction_list.deducted_reason = "ADDITIONAL HALF-DAY LEAVE TAKEN"
                reduction_list.save()
                leavemonth.paid_leave += 1
            else:
                    
                leavemonth.half_day -= 1
            
        leavemonth.save()
        return JsonResponse({"success":True})
    
            

def deletesalary(request,id=0):
    if request.method == "GET":
        SalaryMonthwise.objects.get(salary_id = id).delete()
        return JsonResponse({"success":True})

def proceedsalaryformonth(request,id=0):
    if request.method == "GET":
        salarylist = SalaryMonthwise.objects.get(salary_id=id)
        salarylist.status = 1
        salarylist.save()
        
    return JsonResponse({"success":True})

def viewsalarymonth(request):
    if request.method == "GET":
        sql_query = f"SELECT * FROM `guest_salarymonthwise` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.status = 1"
        result = SalaryMonthwise.objects.raw(sql_query)
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)

def getsalarymonthbyid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_salarymonthwise` s INNER JOIN `guest_employees` e on s.emp_id = e.employee_id INNER JOIN `guest_approve` a on a.id = s.status INNER JOIN guest_calender c on c.id = s.salary_for_month WHERE s.emp_id=%s"
        result = Salary.objects.raw(sql_query,[id])
        data = [
            {
                'salary_id':item.salary_id,
                'salary_date':item.salary_date,
                'base_package':item.base_package,
                'bonus_amount':item.bonus_amount,
                'deducted_amount':item.deducted_amount,
                'total_amount':item.total_amount,
                'employee_name':item.employee_name,
                'status':item.status_name,
                'salary_month':item.month_name
                
            }
            for item in result
        ]
        
    return JsonResponse(data,safe=False)

def deletesalaryall(request,id=0):
    if request.method =="GET":
        salarylist = Salary.objects.get(salary_id = id)
        salarylist.delete()
        
        return JsonResponse({"success":True})