from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TransactionUpdateView, BudgetUpdateView, BudgetCreateView

urlpatterns = [
    path('', views.home, name='home'),

    path('manual', views.manual, name='manual'),
    path('transactions', views.transactions, name='transactions'),
    path('charts', views.charts, name='charts'),
    path('bill', views.bill, name='bill'),
    path('transaction/<int:pk>/update', TransactionUpdateView.as_view(), name='transaction-update'),
    path('profile/update', views.ProfileUpdate, name='profile-update'),

    path('predict', views.handlePredict, name='predict'),
    path('csv', views.csvUpload, name='csv'),

    path('profile', views.profile, name='profile'),
    path('budget', views.BudgetPage, name='budget'),
    path('budget/<int:pk>/update', BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/create', BudgetCreateView.as_view(), name='budget-create'),
    path('analysis', views.analysis, name='analysis'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
