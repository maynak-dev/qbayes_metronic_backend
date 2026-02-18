from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    TrafficSourceViewSet, ActiveAuthorViewSet,
    DesignationViewSet, UserActivityViewSet,
    TotalUsersAPIView, RecentUsersAPIView, TrafficSourcesAPIView,
    ActiveAuthorsAPIView, DesignationsAPIView, UserActivityStatsAPIView,
    UsersListAPIView, SalesDistributionAPIView
)

router = DefaultRouter()
router.register(r'traffic-sources', TrafficSourceViewSet, basename='trafficsource')
router.register(r'active-authors', ActiveAuthorViewSet, basename='activeauthor')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'user-activities', UserActivityViewSet, basename='useractivity')

urlpatterns = [
    # Include all CRUD endpoints from the router
    path('', include(router.urls)),

    # Custom dashboard endpoints
    path('users/count/', TotalUsersAPIView.as_view(), name='users-count'),
    path('users/recent/', RecentUsersAPIView.as_view(), name='recent-users'),
    path('traffic-sources/', TrafficSourcesAPIView.as_view(), name='traffic-sources'),
    path('active-authors/', ActiveAuthorsAPIView.as_view(), name='active-authors'),
    path('designations/', DesignationsAPIView.as_view(), name='designations'),
    path('user-activity/', UserActivityStatsAPIView.as_view(), name='user-activity'),
    path('sales-distribution/', SalesDistributionAPIView.as_view(), name='sales-distribution'),
    path('users/', UsersListAPIView.as_view(), name='users-list'),
]