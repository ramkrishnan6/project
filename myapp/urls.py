from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TransactionUpdateView, BudgetUpdateView, BudgetCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.logIn, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logOut, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('manual', views.manual, name='manual'),
    path('transactions', views.transactions, name='transactions'),
    path('charts', views.charts, name='charts'),
    path('bill', views.bill, name='bill'),
    path('transaction/<int:pk>/update', TransactionUpdateView.as_view(), name='transaction-update'),
    path('profile/update', views.ProfileUpdate, name='profile-update'),

    path('predict', views.handlePredict, name='predict'),
    path('csv', views.csvUpload, name='csv'),
    path('validate_username', views.validate_username),

    path('profile', views.profile, name='profile'),
    path('budget', views.BudgetPage, name='budget'),
    path('budget/<int:pk>/update', BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/create', BudgetCreateView.as_view(), name='budget-create'),

    path('analysis', views.analysis, name='analysis'),

    path('reset-password', auth_views.PasswordResetView.as_view(
        template_name='reset-password/reset_password.html'), name='reset_password'),
    path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(
        template_name='reset-password/reset_password_sent.html'), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reset-password/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset-password-done', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset-password/reset_password_done.html'), name='password_reset_complete')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
