from django.urls import path
from .views import (
    WasteTypeListView, WasteTypeCreateView,
    WasteTypeUpdateView, WasteTypeDeleteView,
    LocationWasteListView, LocationWasteCreateView,
    LocationWasteUpdateView, LocationWasteDeleteView,
    ReviewListView, ReviewCreateView,
    ReviewUpdateView, ReviewDeleteView,
    LocationListView, LocationCreateView,
    LocationUpdateView, LocationDeleteView,
    stats_view, action_view
)
urlpatterns = [
    path('stats/',  stats_view,  name='stats'),
    path('action/', action_view, name='action'),

    path('locations/',           LocationListView.as_view(),   name='location-list'),
    path('locations/add/',       LocationCreateView.as_view(), name='location-add'),
    path('locations/<int:pk>/edit/',   LocationUpdateView.as_view(), name='location-edit'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),
    # WasteType
    path('waste-types/',        WasteTypeListView.as_view(),   name='wastetype-list'),
    path('waste-types/add/',    WasteTypeCreateView.as_view(), name='wastetype-add'),
    path('waste-types/<int:pk>/edit/',   WasteTypeUpdateView.as_view(), name='wastetype-edit'),
    path('waste-types/<int:pk>/delete/', WasteTypeDeleteView.as_view(), name='wastetype-delete'),

    # LocationWaste
    path('location-wastes/',        LocationWasteListView.as_view(),   name='locationwaste-list'),
    path('location-wastes/add/',    LocationWasteCreateView.as_view(), name='locationwaste-add'),
    path('location-wastes/<int:pk>/edit/',   LocationWasteUpdateView.as_view(), name='locationwaste-edit'),
    path('location-wastes/<int:pk>/delete/', LocationWasteDeleteView.as_view(), name='locationwaste-delete'),

    # Review
    path('reviews/',        ReviewListView.as_view(),   name='review-list'),
    path('reviews/add/',    ReviewCreateView.as_view(), name='review-add'),
    path('reviews/<int:pk>/edit/',   ReviewUpdateView.as_view(), name='review-edit'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]