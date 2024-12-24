from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import User
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(
            operation_id="registration",
            request_body=RegisterSerializer,
            responses={200: "Registration successful", 400: "Registration failed"},
    )
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


