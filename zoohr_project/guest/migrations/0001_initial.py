# Generated by Django 5.0.7 on 2024-07-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminid', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, verbose_name='')),
                ('password', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('bonus_amount', models.BigIntegerField(verbose_name='')),
                ('reason', models.CharField(max_length=50, verbose_name='')),
                ('bonus_for', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Calender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('employee_id', models.IntegerField(primary_key=True, serialize=False)),
                ('employee_name', models.CharField(max_length=50)),
                ('post', models.CharField(max_length=50, verbose_name='')),
                ('base_package', models.BigIntegerField(verbose_name='')),
                ('registered_date', models.DateField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Halfday_leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('half_day', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('leave_id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('leave_date', models.DateField(verbose_name='')),
                ('requested_on', models.DateField(verbose_name='')),
                ('reason', models.CharField(max_length=50, verbose_name='')),
                ('status', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('sick_leave', models.IntegerField(verbose_name='')),
                ('casual_leave', models.IntegerField(verbose_name='')),
                ('half_day', models.IntegerField(verbose_name='')),
                ('paid_leave', models.IntegerField(verbose_name='')),
                ('status_upto', models.DateField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveStatusMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('sick_leave', models.IntegerField(verbose_name='')),
                ('casual_leave', models.IntegerField(verbose_name='')),
                ('half_day', models.IntegerField(verbose_name='')),
                ('paid_leave', models.IntegerField(verbose_name='')),
                ('status_upto', models.DateField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('login_id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('employee_username', models.CharField(max_length=50)),
                ('employee_password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OtherReduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('deducted_amount', models.BigIntegerField(verbose_name='')),
                ('deducted_reason', models.CharField(max_length=50, verbose_name='')),
                ('reduction_for', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('deducted_amount', models.BigIntegerField(verbose_name='')),
                ('deducted_reason', models.CharField(max_length=50, verbose_name='')),
                ('leave_taken', models.DateField(verbose_name='')),
                ('reduction_for', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('salary_id', models.IntegerField(primary_key=True, serialize=False)),
                ('salary_date', models.DateField()),
                ('salary_for_month', models.IntegerField(verbose_name='')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('base_package', models.BigIntegerField(verbose_name='')),
                ('bonus_amount', models.IntegerField(verbose_name='')),
                ('deducted_amount', models.IntegerField(verbose_name='')),
                ('total_amount', models.IntegerField(verbose_name='')),
                ('status', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='SalaryMonthwise',
            fields=[
                ('salary_id', models.IntegerField(primary_key=True, serialize=False)),
                ('salary_date', models.DateField()),
                ('salary_for_month', models.IntegerField(verbose_name='')),
                ('emp_id', models.IntegerField(verbose_name='')),
                ('base_package', models.BigIntegerField(verbose_name='')),
                ('bonus_amount', models.IntegerField(verbose_name='')),
                ('deducted_amount', models.IntegerField(verbose_name='')),
                ('total_amount', models.IntegerField(verbose_name='')),
                ('status', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
    ]
