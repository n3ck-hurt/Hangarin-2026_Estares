from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from .models import ArmoryCategory, Supplier, Weapon, Client, Transaction, IntelligenceNote

@method_decorator(login_not_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Dashboard Statistics for Ares Arms
        context['total_revenue'] = Transaction.objects.filter(status='Completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_deals'] = Transaction.objects.count()
        context['pending_approvals'] = Transaction.objects.filter(status='Pending').count()
        context['active_weapons'] = Weapon.objects.filter(is_active=True).count()
        
        # Additional metrics
        context['total_clients'] = Client.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        
        # Recent transactions
        context['recent_transactions'] = Transaction.objects.all()[:5]
        
        return context

class WeaponListView(ListView):
    model = Weapon
    template_name = 'tasks/task_list.html' # Will rename later or keep for now
    context_object_name = 'weapons'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Weapon.objects.all().select_related('category', 'supplier')
        
        # Search Functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(model_number__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Filter by category if provided
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Sorting
        sort_by = self.request.GET.get('sort_by')
        allowed_sort_fields = {
            'name': 'name',
            '-name': '-name',
            'price': 'unit_price',
            '-price': '-unit_price',
            'stock': 'stock_quantity',
            '-stock': '-stock_quantity',
        }
        ordering = allowed_sort_fields.get(sort_by, '-created_at')
        return queryset.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArmoryCategory.objects.all()
        context['current_sort'] = self.request.GET.get('sort_by', '-created_at')
        context['current_query'] = self.request.GET.get('q', '')
        return context

class TransactionListView(ListView):
    model = Transaction
    template_name = 'tasks/member_list.html' # Reusing member list template structure
    context_object_name = 'transactions'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Transaction.objects.all().select_related('client', 'weapon')
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(client__name__icontains=query) |
                Q(weapon__name__icontains=query) |
                Q(status__icontains=query)
            )
            
        # Sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'date':
            queryset = queryset.order_by('-deal_date')
        elif sort_by == 'price':
            queryset = queryset.order_by('-total_price')
        else:
            queryset = queryset.order_by('-deal_date')
            
        return queryset

class ClientListView(ListView):
    model = Client
    template_name = 'tasks/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = Client.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(region__icontains=query)
            )
        return queryset

class SupplierListView(ListView):
    model = Supplier
    template_name = 'tasks/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Supplier.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(country__icontains=query)
            )
        return queryset

class WeaponDetailView(DetailView):
    model = Weapon
    template_name = 'tasks/task_detail.html'
    context_object_name = 'weapon'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_deals'] = self.object.transactions.all()[:5]
        return context