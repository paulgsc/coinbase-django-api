from django.urls import path
from tradingbot.views.http.oauth import RequestCoinBaseExchangeTokenView, CreateCoinbaseAccessTokenView, GetCoinbaseBestBidAskView, CoinbaseRefreshAccessTokenView, GetCoinbaseActionsView

urlpatterns = [
    path('get/coinbase_actions/', GetCoinbaseActionsView.as_view()),
    path('get/exchange_token/', RequestCoinBaseExchangeTokenView.as_view(),
         name='get_exchange_token'),
    path('create/access_token/', CreateCoinbaseAccessTokenView.as_view(),
         name='create_access_token'),
    path('update/access_token/', CoinbaseRefreshAccessTokenView.as_view(),
         name='refresh_access_token'),

]