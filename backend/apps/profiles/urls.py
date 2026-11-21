from django.urls import path
from .views import UserProfileView, SkillListView

urlpatterns = [
    path('', UserProfileView.as_view(), name='user-profile'),
    path('skills/', SkillListView.as_view(), name='skill-list'),
]
