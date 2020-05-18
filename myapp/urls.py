from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TransactionUpdateView, BudgetUpdateView, BudgetCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('login', views.logIn),
    path('register', views.register),
    path('logout', views.logOut),

    path('dashboard', views.dashboard),
    path('manual', views.manual),
    path('transactions', views.transactions),
    path('charts', views.charts),
    path('bill', views.bill),
    path('transaction/<int:pk>/update', TransactionUpdateView.as_view(), name='transaction-update'),
    path('profile/update', views.ProfileUpdate, name='profile-update'),

    path('predict', views.handlePredict),
    path('csv', views.csvUpload),
    path('validate_username', views.validate_username),

    path('profile', views.profile),
    path('budget', views.BudgetPage),
    path('budget/<int:pk>/update', BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/create', BudgetCreateView.as_view(), name='budget-create'),

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
