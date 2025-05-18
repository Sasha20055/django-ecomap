from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Location, Review, WasteType, LocationWaste
from .serializers import UserSerializer, LocationSerializer, WasteTypeSerializer, LocationWasteSerializer, ReviewSerializer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from .forms  import WasteTypeForm, LocationWasteForm, ReviewForm, LocationForm
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['GET', 'OPTIONS'])
def stats_view(request):
    if request.method == 'OPTIONS':
        return Response({'status': 'ok'})
    q = request.query_params.get('queryType')
    if q == 'location_rating':
        data = Location.objects.all().annotate(average_rating=Avg('reviews__rating'))
        return Response([{'location': loc.name, 'average_rating': loc.average_rating or 0} for loc in data])
    elif q == 'location_count':
        return Response({'location_count': Location.objects.count()})
    elif q == 'user_count':
        return Response({'user_count': User.objects.count()})
    elif q == 'review_count':
        return Response({'review_count': Review.objects.count()})
    elif q == 'comments_by_location':
        data = Location.objects.all().annotate(comments=Count('reviews__comment'))
        return Response([{'location': loc.name, 'comments': loc.comments} for loc in data])
    elif q == 'all_locations':
        serializer = LocationSerializer(Location.objects.all(), many=True)
        return Response(serializer.data)
    else:
        return Response({'error': f'Invalid queryType: {q}'}, status=400)

@api_view(['POST'])
def action_view(request):
    action = request.data.get('action')
    if action == 'add_user':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'user_id': serializer.instance.id})
    elif action == 'add_location':
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loc = serializer.save(added_by=request.user)  # теперь request.user точно подходит!
        return Response({'success': True, 'location_id': loc.id})
    elif action == 'update_location':
        loc_id = request.data.get('id')
        if not loc_id:
            return Response({'error': 'Location id is required.'}, status=400)
        try:
            loc = Location.objects.get(pk=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found.'}, status=404)

        if loc.added_by_id != request.user.id and not request.user.is_staff:
            return Response({'error': 'Permission denied.'}, status=403)

        serializer = LocationSerializer(loc, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        loc = serializer.save()
        return Response({'success': True, 'location': serializer.data})


    elif action == 'delete_location':
        loc_id = request.data.get('id')
        if not loc_id:
            return Response({'error': 'Location id is required.'}, status=400)
        try:
            loc = Location.objects.get(pk=loc_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found.'}, status=404)

        if loc.added_by_id != request.user.id and not request.user.is_staff:
            return Response({'error': 'Permission denied.'}, status=403)

        loc.delete()
        return Response({'success': True})
    elif action == 'add_waste_type':
        serializer = WasteTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'waste_type_id': serializer.instance.id})
    elif action == 'add_review':
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'review_id': serializer.instance.id})
    else:
        return Response({'error': f'Invalid action: {action}'}, status=400)

# --- WasteType CRUD (только для админов) ---
class WasteTypeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WasteType
    template_name = 'api/wastetype_list.html'
    def test_func(self):
        return self.request.user.is_staff

class WasteTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = WasteType
    form_class = WasteTypeForm
    template_name = 'api/wastetype_form.html'
    success_url = reverse_lazy('wastetype-list')
    def test_func(self):
        return self.request.user.is_staff

class WasteTypeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WasteType
    form_class = WasteTypeForm
    template_name = 'api/wastetype_form.html'
    success_url = reverse_lazy('wastetype-list')
    def test_func(self):
        return self.request.user.is_staff

class WasteTypeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WasteType
    template_name = 'api/wastetype_confirm_delete.html'
    success_url = reverse_lazy('wastetype-list')
    def test_func(self):
        return self.request.user.is_staff

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'api/location_list.html'

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'api/location_form.html'
    success_url = reverse_lazy('location-list')
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class LocationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'api/location_form.html'
    success_url = reverse_lazy('location-list')
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.added_by or self.request.user.is_staff

class LocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Location
    template_name = 'api/location_confirm_delete.html'
    success_url = reverse_lazy('location-list')
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.added_by or self.request.user.is_staff
# --- LocationWaste CRUD (только для админов) ---
class LocationWasteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LocationWaste
    template_name = 'api/locationwaste_list.html'
    def test_func(self):
        return self.request.user.is_staff

class LocationWasteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LocationWaste
    form_class = LocationWasteForm
    template_name = 'api/locationwaste_form.html'
    success_url = reverse_lazy('locationwaste-list')
    def test_func(self):
        return self.request.user.is_staff

class LocationWasteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LocationWaste
    form_class = LocationWasteForm
    template_name = 'api/locationwaste_form.html'
    success_url = reverse_lazy('locationwaste-list')
    def test_func(self):
        return self.request.user.is_staff

class LocationWasteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LocationWaste
    template_name = 'api/locationwaste_confirm_delete.html'
    success_url = reverse_lazy('locationwaste-list')
    def test_func(self):
        return self.request.user.is_staff

# --- Review CRUD (опросы могут удалять/редактировать только авторы или админы) ---
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'api/review_list.html'
    def get_queryset(self):
        # обычный пользователь видит только свои; админ — все
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'api/review_form.html'
    success_url = reverse_lazy('review-list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'api/review_form.html'
    success_url = reverse_lazy('review-list')
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_staff

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'api/review_confirm_delete.html'
    success_url = reverse_lazy('review-list')
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_staff