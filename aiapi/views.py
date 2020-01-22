from rest_framework import status, generics
from rest_framework.response import Response
from aiapi.utility.chatbot import final_response
from rest_framework.views import APIView


class ChatBotAPIView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        input_data = request.data.get('text')
        response = final_response(input_data)
        #ChatBotLog.objects.create(
        #	input_data=input_data,
        #	reply=str(response)
        #	)
        return Response({'success': True, 'data': str(response)}, status=status.HTTP_200_OK)