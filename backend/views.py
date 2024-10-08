from django.shortcuts import render
from .models import Property
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
# from django import messages
from .serializers import CustomUserSerializer, ChangeUserTypeSerializer,LoginSerializer,PropertySerializer,CartSerializer, CartItemSerializer
from rest_framework import status, generics, permissions
from .models import CustomUser, Property, Cart, CartItem
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from.filters import PropertyFilter

# Create your views here.
# def property_view(request):
#     properties = Property.objects.all()
#     context = {"properties":properties}
#     return render(request, "backend/index.html", context)
# migration from native django to the rest framework
# def register_view(request):
#     if request.method =="POST":
#         form  = UserCreationForm(request.Post)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             if User.objects.filter(username=username).exists():
#                 pass

class ChangeUserTypeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangeUserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({
                'message': 'login successful',
                user: {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            },  status=status.HTTP_201_CREATED,)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = PropertyFilter

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_objects(self):
        return Cart.objects.get(user=self.request.user)

class CartAddItemView(generics.CreateAPIView):
    serializer_class = CartSerializer

    def create_cart(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartUpdateItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer

    def get_item(self, slug):
        return CartItem.objects.get_or_create(slug=slug)
    
    def put(self, slug, request, *args, **kwargs):
        cart_item = self.get_object(slug)
        serializer = self.get_serializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CartDeleteItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





