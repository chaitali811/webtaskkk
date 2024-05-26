from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from .forms import AccountForm, DestinationForm
import requests





def home(request):
    return render(request, 'home.html')


# API Views
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class AccountDestinationsView(generics.ListAPIView):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return Destination.objects.filter(account__account_id=account_id)


class DataHandlerView(APIView):
    def post(self, request):
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        if not isinstance(data, dict):
            return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

        for destination in account.destinations.all():
            headers = destination.headers
            headers['Content-Type'] = 'application/json'

            if destination.http_method == 'GET':
                response = requests.get(destination.url, headers=headers, params=data)
            elif destination.http_method in ['POST', 'PUT']:
                response = requests.request(destination.http_method, destination.url, headers=headers, json=data)
            else:
                continue

        return Response({'status': 'Data sent to destinations'}, status=status.HTTP_200_OK)

# Template Views


# In your views.py
def account_list(request):
    accounts = Account.objects.all()
    for account in accounts:
        print(f"Account ID: {account.pk}, Account Name: {account.account_name}")
    return render(request, 'account_list.html', {'accounts': accounts})


def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account-list')
    else:
        form = AccountForm()
    return render(request, 'account_form.html', {'form': form})

def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account-list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'account_form.html', {'form': form})

def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account-list')
    return render(request, 'account_confirm_delete.html', {'account': account})

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination-list')
    else:
        form = DestinationForm()
    return render(request, 'destination_form.html', {'form': form})

def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination-list')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destination_form.html', {'form': form})

def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('destination-list')
    return render(request, 'destination_confirm_delete.html', {'destination': destination})
