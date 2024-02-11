import requests
import os
import secrets
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from tradingbot.models import CustomUser, CoinbaseAPIActions, CoinbaseSupportedScopes, UserCoinBaseAPIKeys



class GetCoinbaseActionsView(APIView):
    """
        Send the possible coinbase actions that user can grant and their permison details
    """

    def get(self, request):
        return Response(status=200)
        # instance = CoinbaseAPIActions.objects.all()
        # serializer = CoinbaseApiActionsSerializer(instance=instance, many=True)
        # return Response(data=serializer.data, status=200)


class RequestCoinBaseExchangeTokenView(APIView):
    """
    When redirecting a user to Coinbase to authorize access to your application,
    you'll need to construct the authorization URL
    with the correct parameters and scopes.
    """

    def get(self, request):
        # get authenticated user
        user = get_object_or_404(CustomUser, pk=request.user.id)

        # list of parameters you should always specify
        response_type = 'code'  # Required
        client_id = os.environ.get('COINBASE_CLIENT_ID')  # Required
        # Optional An unguessable random string. It is used to protect against cross-site request forgery attacks
        state = secrets.token_hex(32)

        # get scopes from db using the ids passed in request
        scope = self.get_scope_names_str(request=request)
        if not scope:
            # send 401 error if scopes not defined
            return Response(status=401)

        # because this initaites the oauth, we store important values in cache and not in db for now
        self.store_data_in_cache(request=request, state=state)

        url = 'https://www.coinbase.com/oauth/authorize'

        data = {
            'url': url,
            'params': {
                'response_type': response_type,
                'client_id': client_id,
                'redirect_uri': 'https://leafiproperties.com/coinbase/callback',
                'scope': scope,
                'state': state
            }
        }

        return Response(data=data, status=200)

    def get_scope_names_str(self, request):
        # Get the user granted scope ids from request
        scope_ids = request.data.get('scopeIds')

        # Retrieve the scope names for the given scope IDs
        scope_names = CoinbaseSupportedScopes.objects.filter(
            id__in=scope_ids).values_list('scope_name', flat=True)

        # Convert the queryset result to a comma-separated string
        scope_names_str = ','.join(scope_names)

        return scope_names or None

    def store_data_in_cache(self, request, **args):
        # Retrieve the 'state' parameter from args
        state = args.get('state')

        # Retrieve the action ids, and scope ids from request
        granted_scopes = {
            'action_ids': request.data.get('actionIds'),
            'scope_ids': request.data.get('scopeIds')
        }

       # Store the state param in cache for verification later.
        cache.set(
            key=f'coinbase_state_for_{request.user.email}', value=state, timeout=300)
        # Store the granted scopes temp in cache, will persist in db once outh is successful
        cache.set(
            key=f'coinbase_granted_scopes_for_{request.user.email}', value=granted_scopes, timeout=900)


class BaseCoinbaseAccessTokenView(APIView):

    client_id = os.environ.get('COINBASE_CLIENT_ID')
    client_secret = os.environ.get('COINBASE_CLIENT_SECRET')
    token_url = None
    params = None

    def post(self, request):
        return self.create_or_refresh_access_token(request=request)

    def create_or_refresh_access_token(self, request):
        try:
            # Make the POST request with data in the request body
            response = requests.post(
                self.token_url,
                data=self.params,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                token_data = response.json()

                # Create or update API keys
                self.create_or_update_coinbase_api_keys(
                    user=request.user, data=token_data)
            else:
                return Response(status=401)

            return Response(status=response.status_code)
        except Exception as e:
            return Response(status=500)

    def create_or_update_coinbase_api_keys(self, user, data):
        pass
        # data.update({'user': user.id})
        # user_has_coinbase_acct = hasattr(
        #     user, 'coinbase_oauth') and user.coinbase_oauth is not None

        # if user_has_coinbase_acct:
        #     instance = get_object_or_404(UserCoinBaseAPIKeys, user=user.id)
        #     serializer = CoinBaseAPIKeysCreateSerializer(
        #         data=data, instance=instance)
        # else:
        #     serializer = CoinBaseAPIKeysCreateSerializer(data=data)

        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     print('error: ', serializer.errors)
        #     raise Exception(serializer.errors)


class CreateCoinbaseAccessTokenView(BaseCoinbaseAccessTokenView):

    def post(self, request):
        # Get the exchange code token and redirect uri from request
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')
        # Define the URL for the access token exchange
        self.token_url = "https://api.coinbase.com/oauth/token"

        # Define the parameters required for the post request to coinbase
        self.params = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
        }
        return super().post(request)


class CoinbaseRefreshAccessTokenView(BaseCoinbaseAccessTokenView, APIView):

    def post(self, request):
        # Define the URL for the access token refresh
        self.token_url = "https://api.coinbase.com/oauth/token"

        # Retrieve the stored refresh token from db
        instance = get_object_or_404(UserCoinBaseAPIKeys, user=request.user.id)

        # Define the parameters required for the request
        self.params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": instance.refresh_token,
        }
        return super().post(request)


class GetCoinbaseBestBidAskView(APIView):

    def get(self, request):
        raise ValueError('mahomeboy')
        instance = get_object_or_404(UserCoinBaseAPIKeys, user=request.user.id)
        serializer = CoinBaseAPIKeysCreateSerializer(instance=instance)
        return Response(serializer.data, status=200)
