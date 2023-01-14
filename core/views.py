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
    """
    This view is used to consult the status
    Here we obtain a message where you can read aif the server 
    """
    def get(self, request):
        response = {'status': 'Server is running and OK'}
        return Response(response, status.HTTP_200_OK)
    

class ConsultView(APIView):
    """
    This view is used to consult a exchange currency
    It need for two data, the first data is base_currency where the specific the kind of currency we want to exchange,
    and the next data is quote_currency here we add the currency about you want to exchange
    """
    def post(self,request):
        # GET THE DAT OF THE REQUEST AND RETURN AN ERROR IF THE DATA IS NO COMPLETED
        try:
            base_currency = request.data['base_currency']
            quote_currency = request.data['quote_currency']
        except:
            response = {'message': 'all data is necesary for this request'} 
            return Response(response, status.HTTP_406_NOT_ACCEPTABLE)

        # GET THE LIST OF CURRENCY IN THE MODEL
        type_currency_list = []
        for _type in Currency.type_currency_list:    
            type_currency_list.append(_type[0])

        # CONVERT THE DATA TO UPPER CASE
        base_currency = base_currency.upper()
        quote_currency = quote_currency.upper()

        # IF ANY DATA IS NOT EN THE LIST OF CURRENCY WE RESPONDE AN ERROR
        if not base_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to base_currency'})

        if not quote_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to quote_currency'})
        
        actual_quote_currency = Currency.objects.get(type_currency=quote_currency)
        
        # GENERATE A LIST TO CONVERT DE BASE CURRENCY A DOLAR
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

        # CONVERT TO DOLLAR
        dollar_amount = 1 / value_dollar_list[base_currency]
        final_amount = dollar_amount * value_dollar_list[quote_currency]
        final_amount = round(final_amount,2)

        # GENERATING THE RESPONSE
        response = {
                'compra': final_amount,
                'venta': round(final_amount * 1.05,2),
                'disponible': actual_quote_currency.amount
                }
        return Response(response, status.HTTP_200_OK)


class CurrencyExchangeView(APIView):
    """
    This view is used to exchange a currency
    It need for three data, the first data is base_currency where the specific the kind of currency we want to exchange,
    the second data is quote_currency here we add the currency about you want to exchange
    and the final data is about the amount that you want to exchage
    """
    def post(self,request):
        # GET THE DAT OF THE REQUEST AND RETURN AN ERROR IF THE DATA IS NO COMPLETED
        try:
            base_currency = request.data['base_currency']
            quote_currency = request.data['quote_currency']
            amount = request.data['amount']
        except:
            response = {'message': 'all data is necesary for this request'} 
            return Response(response, status.HTTP_406_NOT_ACCEPTABLE)

        # GET THE LIST OF CURRENCY IN THE MODEL
        type_currency_list = []
        for _type in Currency.type_currency_list:    
            type_currency_list.append(_type[0])

        # CONVERT THE DATA TO UPPER CASE
        base_currency = base_currency.upper()
        quote_currency = quote_currency.upper()

        # IF ANY DATA IS NOT EN THE LIST OF CURRENCY WE RESPONDE AN ERROR
        if not base_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to base_currency'})

        if not quote_currency in type_currency_list:
            return Response({'message': 'please enter a valid data to quote_currency'})
        
        # GENERATE A LIST TO CONVERT DE BASE CURRENCY A DOLAR
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

        # CONVERT TO DOLAR
        dollar_amount = amount / value_dollar_list[base_currency]
        final_amount = dollar_amount * value_dollar_list[quote_currency]

        # GET THE AMOUNT TO BASE AND QUOTE CURRENCY
        actual_quote_currency = Currency.objects.get(type_currency=quote_currency)
        actual_base_currency = Currency.objects.get(type_currency=base_currency)

        # IF THE AMOUNT IS BETTER THAT THE AVAILABLE AMOUNT, WE RESPONDE A ERROR
        if final_amount > actual_quote_currency.amount:
            return Response({'message': 'the request is bigger than the available amount in the bank'})
        
        # SUBTRAIN THE AMOUNT TO THE QUOTE CURRENCY
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

        # ADD THE AMOUNT TO BASE CURRENCY
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

        # GENERATING THE RESPONSE
        response = {
                'amount_base': actual_base_currency.amount,
                'amount_quote': actual_quote_currency.amount
                }
        
        return Response(response, status.HTTP_200_OK)