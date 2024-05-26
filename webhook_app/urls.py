from django.urls import path
from .views import (
    AccountListCreateView,
    AccountRetrieveUpdateDestroyView,
    DestinationListCreateView,
    DestinationRetrieveUpdateDestroyView,
    AccountDestinationsView,
    DataHandlerView,
    account_list,
    account_create,
    account_update,
    account_delete,
    destination_list,
    destination_create,
    destination_update,
    destination_delete, home


)

urlpatterns = [
    path('', home, name='home'),
    path('api/accounts/', AccountListCreateView.as_view(), name='account-list-create-api'),
    path('api/accounts/<uuid:pk>/', AccountRetrieveUpdateDestroyView.as_view(), name='account-detail-api'),
    path('api/destinations/', DestinationListCreateView.as_view(), name='destination-list-create-api'),
    path('api/destinations/<int:pk>/', DestinationRetrieveUpdateDestroyView.as_view(), name='destination-detail-api'),
    path('api/accounts/<uuid:account_id>/destinations/', AccountDestinationsView.as_view(), name='account-destinations-api'),
    path('api/server/incoming_data/', DataHandlerView.as_view(), name='data-handler-api'),
    path('accounts/', account_list, name='account-list'),
    path('accounts/create/', account_create, name='account-create'),
    path('accounts/update/<uuid:pk>/', account_update, name='account-update'),
    path('accounts/delete/<uuid:pk>/', account_delete, name='account-delete'),
    path('destinations/', destination_list, name='destination-list'),
    path('destinations/create/', destination_create, name='destination-create'),
    path('destinations/update/<int:pk>/', destination_update, name='destination-update'),
    path('destinations/delete/<int:pk>/', destination_delete, name='destination-delete'),
]
