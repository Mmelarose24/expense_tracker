from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, ExpenseForm, BudgetForm, ScheduleForm, CategoryForm
from .models import Expense, Budget, Schedule, Category, Notification
from django.db.models import Sum
from datetime import date, timedelta
from django.http import JsonResponse

def home(request):
    return render(request, 'expenses/home.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home') 

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Create default categories for the new user
            default_categories = [
                ('food', 10),
                ('transportation', 5),
                ('utilities', 15),
                ('rent', 30),
                ('entertainment', 10),
                ('savings', 20),
                ('other', 10),
            ]
            
            for name, percentage in default_categories:
                Category.objects.create(
                    name=name,
                    recommended_percentage=percentage,
                    user=user
                )
            
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'expenses/register.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Expenses data
    expenses = Expense.objects.filter(user=request.user, date__month=today.month).order_by('-date')
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # Budget data
    budgets = Budget.objects.filter(user=request.user)
    monthly_budget = budgets.filter(period='monthly').aggregate(total=Sum('amount'))['total'] or 0
    weekly_budget = budgets.filter(period='weekly').aggregate(total=Sum('amount'))['total'] or 0
    daily_budget = budgets.filter(period='daily').aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate remaining budget
    remaining_monthly = monthly_budget - total_expenses if monthly_budget else 0
    
    # Category breakdown
    category_data = []
    categories = Category.objects.filter(user=request.user)
    
    for category in categories:
        cat_expenses = expenses.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        if monthly_budget > 0:
            percentage = (cat_expenses / monthly_budget) * 100
        else:
            percentage = 0
        category_data.append({
            'name': category.name,
            'amount': cat_expenses,
            'percentage': round(percentage, 2),
    
        })
    
    # Notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    
    # Upcoming schedules
    upcoming_schedules = Schedule.objects.filter(
        user=request.user,
        start_date__gte=today
    ).order_by('start_date')[:5]
    
    context = {
        'expenses': expenses[:5],
        'total_expenses': total_expenses,
        'monthly_budget': monthly_budget,
        'remaining_monthly': remaining_monthly,
        'weekly_budget': weekly_budget,
        'daily_budget': daily_budget,
        'category_data': category_data,
        'notifications': notifications,
        'upcoming_schedules': upcoming_schedules,
    }
    
    return render(request, 'expenses/dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            # Check if expense exceeds budget
            category = expense.category
            if category:
                today = date.today()
                monthly_expenses = Expense.objects.filter(
                    user=request.user,
                    category=category,
                    date__month=today.month
                ).aggregate(total=Sum('amount'))['total'] or 0
                
                category_budget = Budget.objects.filter(
                    user=request.user,
                    category=category,
                    period='monthly'
                ).first()
                
                if category_budget and monthly_expenses > category_budget.amount * 0.8:
                    Notification.objects.create(
                        user=request.user,
                        notification_type='budget_limit',
                        trigger=f"Spending reached 80% of budget for {category.name}",
                        message=f"You've spent {monthly_expenses} out of {category_budget.amount} budget for {category.name} this month."
                    )
            
            messages.success(request, 'Expense added successfully!')
            return redirect('expenses_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expenses_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expenses_list.html', {'expenses': expenses})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenses_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expenses_list')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget added successfully!')
            return redirect('budgets_list')
    else:
        form = BudgetForm()
    return render(request, 'expenses/add_budget.html', {'form': form})

@login_required
def budgets_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'expenses/budgets_list.html', {'budgets': budgets})

@login_required
def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            messages.success(request, 'Schedule added successfully!')
            return redirect('schedules_list')
    else:
        form = ScheduleForm()
    return render(request, 'expenses/add_schedule.html', {'form': form})

@login_required
def schedules_list(request):
    schedules = Schedule.objects.filter(user=request.user)
    return render(request, 'expenses/schedules_list.html', {'schedules': schedules})

@login_required
def categories_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/categories_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/add_category.html', {'form': form})

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'expenses/notifications_list.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def reports(request):
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Monthly expenses
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__range=[start_of_month, end_of_month]
    ).order_by('date')
    
    # Category breakdown
    category_data = []
    categories = Category.objects.filter(user=request.user)
    
    for category in categories:
        cat_expenses = monthly_expenses.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
        category_data.append({
            'name': category.name,
            'amount': cat_expenses,
        })
    
    # Budget vs Actual
    budgets = Budget.objects.filter(user=request.user, period='monthly')
    budget_data = []
    
    for budget in budgets:
        actual = monthly_expenses.filter(category=budget.category).aggregate(total=Sum('amount'))['total'] or 0
        budget_data.append({
            'category': budget.category.name if budget.category else 'General',
            'budget': budget.amount,
            'actual': actual,
            'difference': budget.amount - actual
        })
    
    context = {
        'monthly_expenses': monthly_expenses,
        'category_data': category_data,
        'budget_data': budget_data,
    }
    
    return render(request, 'expenses/reports.html', context)