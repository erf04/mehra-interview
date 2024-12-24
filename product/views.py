from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from .models import Product
from . import serializers
from django.shortcuts import get_object_or_404
from .permissions import IsProductOwner
from drf_yasg.utils import swagger_auto_schema

class ProductView(APIView):
    permission_classes =[permissions.IsAuthenticated] # the user must be authenticated

    @swagger_auto_schema(operation_id="get_all_products", responses={200: serializers.ProductSerializer(many=True)})
    # get all products
    def get(self,request:Request):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products,many=True)
        return Response(serializer.data,status=200) 


    @swagger_auto_schema(
        operation_id="create_product",
        request_body=serializers.ProductCreationSerializer,
        responses={
            200: "Product created successfully",
            400: "bad request",
        }
    )
    # create a product 
    def post(self,request:Request):
        serializer = serializers.ProductCreationSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)



class SingleProductView(APIView):
 
    permission_classes =[permissions.IsAuthenticated,
                         IsProductOwner] # use my custom permission to check if 
                                         # the authenticated user is the owner of the product

    
    @swagger_auto_schema(operation_id="get_one_product", responses={200: serializers.ProductSerializer(many=False),404: "Product not found"})
    # get one product 
    def get(self,request:Request,id:int):
        product = get_object_or_404(Product,id=id) # if the object does not exist 404 will return in response
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data,status=200)

    @swagger_auto_schema(operation_id="update_product", request_body=serializers.ProductCreationSerializer, responses={200: "Product updated successfully", 400: "Bad request"})
    # update a product 
    def put(self,request:Request,id:int):
        product = get_object_or_404(Product,id=id)
        self.check_object_permissions(request=request,obj=product) # check if the authenticated user is the owner of the product
        serializer = serializers.ProductCreationSerializer(product, data=request.data,
                                                         context={'request': request}, partial=True) # partial update using the creation serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(operation_id="delete_product", responses={204: "Product deleted successfully", 404: "Product not found"})
    #delete a product 
    def delete(self,request:Request,id:int):
        product = get_object_or_404(Product,id=id)
        self.check_object_permissions(request=request, obj=product)
        product.delete()
        return Response({"message": "Product deleted successfully."}, status=204)
