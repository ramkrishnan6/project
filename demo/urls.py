from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TransactionUpdateView, BudgetUpdateView, BudgetCreateView

urlpatterns = [
    path('', views.home, name='home-demo'),
    path('options', views.options, name='options-demo'),
    path('phone', views.phone, name='phone-demo'),
    path('tablet', views.tablet, name='tablet-demo'),
    path('computer', views.computer, name='computer-demo'),

    path('manual', views.manual, name='manual-demo'),
    path('transactions', views.transactions, name='transactions-demo'),
    path('charts', views.charts, name='charts-demo'),
    path('bill', views.bill, name='bill-demo'),
    path('transaction/<int:pk>/update', TransactionUpdateView.as_view(), name='transaction-update-demo'),
    path('profile/update', views.ProfileUpdate, name='profile-update-demo'),

    path('predict', views.handlePredict, name='predict-demo'),
    path('csv', views.csvUpload, name='csv-demo'),

    path('profile', views.profile, name='profile-demo'),
    path('budget', views.BudgetPage, name='budget-demo'),
    path('budget/<int:pk>/update', BudgetUpdateView.as_view(), name='budget-update-demo'),
    path('budget/create', BudgetCreateView.as_view(), name='budget-create-demo'),
    path('analysis', views.analysis, name='analysis-demo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
