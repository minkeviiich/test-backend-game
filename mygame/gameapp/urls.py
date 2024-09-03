from django.urls import path
from .views import daily_login, export_to_csv, export_to_html

urlpatterns = [
    path('daily-login/<int:player_id>/', daily_login, name='daily_login'),
    path('export-to-html/', export_to_html, name='export_to_html'),
    path('export-to-csv/', export_to_csv, name='export_to_csv'),
]
