from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from .models import TrafficSource, ActiveAuthor, Designation, UserActivity
from .serializers import (
    TrafficSourceSerializer, ActiveAuthorSerializer,
    DesignationSerializer, UserActivitySerializer,
    UserSerializer, UserCreateSerializer
)

# ================== VIEWSETS (for CRUD) ==================
class TrafficSourceViewSet(viewsets.ModelViewSet):
    queryset = TrafficSource.objects.all()
    serializer_class = TrafficSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActiveAuthorViewSet(viewsets.ModelViewSet):
    queryset = ActiveAuthor.objects.all()
    serializer_class = ActiveAuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

# ================== CUSTOM API VIEWS (for dashboard) ==================
class TotalUsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_count = User.objects.count()
        last_week = datetime.now() - timedelta(days=7)
        prev_count = User.objects.filter(date_joined__lte=last_week).count()
        if prev_count:
            growth = ((total_count - prev_count) / prev_count) * 100
            growth_str = f"{growth:+.1f}%"
        else:
            growth_str = "+0%"
        return Response({'count': total_count, 'growth': growth_str})

class RecentUsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recent_users = User.objects.order_by('-date_joined')[:4]
        data = []
        for user in recent_users:
            data.append({
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'time': user.date_joined.strftime("%Y-%m-%d %H:%M")
            })
        return Response(data)

class TrafficSourcesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sources = TrafficSource.objects.all()
        labels = [s.source_name for s in sources]
        series = [s.visits for s in sources]
        return Response({'labels': labels, 'series': series})

class ActiveAuthorsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authors = ActiveAuthor.objects.order_by('-contribution_score')[:5]
        data = []
        for a in authors:
            data.append({
                'name': a.user.get_full_name() or a.user.username,
                'role': a.role,
                'progress': min(a.contribution_score, 100)
            })
        return Response(data)

class DesignationsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        designations = Designation.objects.all().order_by('-date')[:5]
        serializer = DesignationSerializer(designations, many=True)
        return Response(serializer.data)

class UserActivityStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Simplified mock data – replace with real aggregation
        data = {
            'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'active': [30, 40, 35, 50, 49, 60],
            'new': [20, 30, 25, 40, 39, 45]
        }
        return Response(data)

class SalesDistributionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            'labels': ['NYC', 'LDN', 'PAR', 'TOK', 'BER'],
            'series': [28, 22, 18, 17, 15],
            'growth': '+7.4%'
        }
        return Response(data)

class UsersListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        profile_data = {}
        # Collect all keys starting with 'profile.'
        for key in list(data.keys()):
            if key.startswith('profile.'):
                profile_key = key.replace('profile.', '', 1)
                profile_data[profile_key] = data.pop(key)
        if profile_data:
            data['profile'] = profile_data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)