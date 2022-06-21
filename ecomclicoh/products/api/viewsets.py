from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from products.api.serializers import (
    ProductSerializer,
    OrderSerializer,
    OrderDetailSerializer,
)
from products.models import Product, OrderDetail, Order
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import requests


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = OrderSerializer.Meta.model.objects.all()


class OrderTotal(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        queryset = OrderDetail.objects.all()
        serializer = OrderDetailSerializer(queryset, many=True)

        total = OrderDetail.objects.select_related("product").aggregate(
            Sum("product__price")
        )["product__price__sum"]
        data = {
            "Total de las Ordenes": total,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = OrderDetail.objects.all()
        order_d = get_object_or_404(queryset, pk=pk)
        order_id = order_d.id
        total = (
            OrderDetail.objects.select_related("product")
            .filter(id=order_id)
            .aggregate(Sum("product__price"))["product__price__sum"]
        )

        data = {
            "Total de la Orden": total,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderTotalUsd(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        queryset = OrderDetail.objects.all()
        serializer = OrderDetailSerializer(queryset, many=True)

        total = OrderDetail.objects.select_related("product").aggregate(
            Sum("product__price")
        )["product__price__sum"]
        blue = self.get_total_usd(self)
        blue_uso = blue.split(",")
        blue_este = blue_uso[0]
        total_usd = total / float(blue_este)
        data = {"Total ordenes en USD": total_usd}
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = OrderDetail.objects.all()
        order_d = get_object_or_404(queryset, pk=pk)
        order_id = order_d.id
        total = (
            OrderDetail.objects.select_related("product")
            .filter(id=order_id)
            .aggregate(Sum("product__price"))["product__price__sum"]
        )
        blue = self.get_total_usd(self)
        blue_uso = blue.split(",")
        blue_este = blue_uso[0]
        total_usd = total / float(blue_este)
        data = {
            "Total de la Orden": total_usd,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def get_total_usd(request, self, params={}):
        reqUrl = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

        payload = ""
        if reqUrl:
            req = requests.request("GET", reqUrl, data=payload)
            blue = req.json()
            dolar = blue[1]["casa"]["venta"]
            return dolar


class OrderDetailViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = OrderDetailSerializer
    queryset = OrderDetailSerializer.Meta.model.objects.all()

    def create(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            cantidad = int(request.data["cuantity"])
            producto = Product.objects.get(id=request.data["product"])
            if cantidad > 0:
 
                if producto.stock > cantidad:
                    stocknuevo = producto.stock - cantidad
                    producto.stock = stocknuevo
                    nueva_orden = Order.objects.create()
                    producto.save()
                    serializer.save(order=nueva_orden)
                    return Response(
                        {"message": "Orden creada correctamente"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    raise serializers.ValidationError(
                        "No existe esa cantidad de stock del producto" + producto.name
                    )
            raise serializers.ValidationError(
                        "La cantidad del producto debe ser mayor a 0"
                    )        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        order_d = OrderDetail.objects.get(pk=pk)
        orden = order_d.order
        order = Order.objects.get(id=orden.id)
        cuantity = order_d.cuantity
        productos = order_d.product
        for producto in productos.all():
            producto.stock += cuantity
            producto.save()
        order.delete()
        order_d.delete()
        return Response(
            {"message": "Orden eliminada Correctamente!"}, status=status.HTTP_200_OK
        )