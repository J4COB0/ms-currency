from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Currency
from .serializer import CurrencySerializer, CurrencyCreateSerializer

class CurrencyListAPIView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyCreateAPIView(generics.CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyCreateSerializer

class CurrencyDestroyAPIView(generics.DestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyUpdateAPIView(generics.UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class StatusView(APIView):

    def get(self, request):
        response = {'status': 'Server is running and OK'}
        return Response(response, status.HTTP_200_OK)
    

class ConsultView(APIView):
    
    def post(self,request):
        try:
            base_currency = request.data['base_currency']
            quote_currency = request.data['quote_currency']
        except:
            response = {'message': 'all data is necesary for this request'} 
            return Response(response, status.HTTP_406_NOT_ACCEPTABLE)

        type_currency_list = []
        for _type in Currency.type_currency_list:    
            type_currency_list.append(_type[0])

        base_currency = base_currency.upper()
        quote_currency = quote_currency.upper()

        if not base_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to base_currency'})

        if not quote_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to quote_currency'})
        
        actual_quote_currency = Currency.objects.get(type_currency=quote_currency)
        
        value_dollar_list = {
            'EUR': 0.93,
            'USD': 1,
            'JPY': 132.41,
            'GBP': 0.82,
            'CHF': 0.92,
            'AUD': 1.45,
            'CAD': 1.34,
            'NZD': 1.57,
        }

        dollar_amount = 1 / value_dollar_list[base_currency]
        final_amount = dollar_amount * value_dollar_list[quote_currency]
        final_amount = round(final_amount,2)

        response = {
                'compra': final_amount,
                'venta': round(final_amount * 1.05,2),
                'disponible': actual_quote_currency.amount
                }
        return Response(response, status.HTTP_200_OK)


class CurrencyExchangeView(APIView):

    def post(self,request):
        try:
            base_currency = request.data['base_currency']
            quote_currency = request.data['quote_currency']
            amount = request.data['amount']
        except:
            response = {'message': 'all data is necesary for this request'} 
            return Response(response, status.HTTP_406_NOT_ACCEPTABLE)

        type_currency_list = []
        for _type in Currency.type_currency_list:    
            type_currency_list.append(_type[0])

        base_currency = base_currency.upper()
        quote_currency = quote_currency.upper()

        if not base_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to base_currency'})

        if not quote_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to quote_currency'})
        
        value_dollar_list = {
            'EUR': 0.93,
            'USD': 1,
            'JPY': 132.41,
            'GBP': 0.82,
            'CHF': 0.92,
            'AUD': 1.45,
            'CAD': 1.34,
            'NZD': 1.57,
        }

        dollar_amount = amount / value_dollar_list[base_currency]
        final_amount = dollar_amount * value_dollar_list[quote_currency]

        actual_quote_currency = Currency.objects.get(type_currency=quote_currency)
        actual_base_currency = Currency.objects.get(type_currency=base_currency)

        if final_amount > actual_quote_currency.amount:
            return Response({'message': 'the request is bigger than the available amount in the bank'})
        
        # Restar a la cantidad quote 
        available = True
        if final_amount == actual_quote_currency.amount:
            available = False

        data_quote = {
            'type_currency': actual_quote_currency.type_currency,
            'amount': round(actual_quote_currency.amount - final_amount,2),
            'available': available
        }

        serializer_quote = CurrencySerializer(actual_quote_currency, data=data_quote)
        
        if serializer_quote.is_valid():
            serializer_quote.save()

        # Añadir a la cantidad basek
        available = False
        if (actual_base_currency.amount + amount) > 0:
            available = True

        data_base = {
            'type_currency': actual_base_currency.type_currency,
            'amount': round(actual_base_currency.amount + amount,2),
            'available': available
        }

        serializer_base = CurrencySerializer(actual_base_currency, data=data_base)
        if serializer_base.is_valid():
            serializer_base.save()

        response = {
                'amount_base': serializer_base.data,
                'amount_quote': serializer_quote.data
                }
        
        return Response(response, status.HTTP_200_OK)