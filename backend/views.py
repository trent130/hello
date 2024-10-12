from .models import Property
from .serializers import CustomUserSerializer, ChangeUserTypeSerializer,LoginSerializer,PropertySerializer,CartSerializer, CartItemSerializer, ClientSerializer
from .serializers import OwnerSerializer, NotificationSerializer, TransactionSerializer, PaymentSerializer, OrderSerializer, OrderItemSerializer,AgentSerializer
from rest_framework import status, generics, permissions
from .models import CustomUser, Property, Cart, CartItem, Client, Agent, Owner,  Order, OrderItem #Notification, Transaction, Payment,
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from.filters import PropertyFilter

class ChangeUserTypeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangeUserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =CustomUserSerializer
    permission_classes = [permissions.AllowAny]

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
    filter_backends = (DjangoFilterBackend)
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

class CheckoutView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_class = [permissions.IsAuthenticated]
    
    # I have not implimented the checkout class well i will revisit at a later date so no url for you yet
    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'details': 'no items in cart found'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(user=request.user)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                property=cart_item.property,
                quantity=cart_item.quantity,
            )
        
        #remove the items from cart after creating an order
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartDeleteItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AgentProfileView(generics.GenericAPIView):
    queryset = Agent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgentSerializer

    def get_objects(self):
        return self.request.user.agent

class ClientProfileView(generics.GenericAPIView):
    queryset = Client.objects.all()
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    def get_objects(self):
        return self.request.user.customer
    
class OwnerProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_objects(self):
        return self.request.user.owner

class OrderView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.get(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    permission_class = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
class CancelOrderView(generics.DestroyAPIView):
    permission_class =[permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def cancel_order(self):
        order =Order.objects.filter(user=self.request.user)
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemListView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return OrderItem.objects.filter(slug=slug, order__user=self.request.user)
    
class OrderItemDetailView(generics.RetrieveAPIView):
    permission_class = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    class get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


