from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser,Payment,Property,CartItem,Cart,PropertyFeature, Order, OrderItem, Agent, Image, Client, Owner, Transaction, Notification

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'first_name', 'email', 'last_name']

        def create(self, **validated_data):
            user = CustomUser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

class ChangeUserTypeSerializer(serializers.ModelSerializer):
    new_user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ['new_user_type']
    
    def update(self, instance, validated_data):
        new_user_type = validated_data['new_user_type']
        instance.apply_for_type_change(new_user_type)
        return instance

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get['email']
        password = data.get['password']

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise serializers.ValueError('invalid email or password')

        data['user'] = user
        return data
    
class PropertyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ['feature_name', 'feature_value']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'image_alt']

class OwnerSerializer(serializers.ModelSerializer):
    property_details = serializers.SerializerMethodField()
    property = serializers.PrimaryKeyRelatedField(read_only=True, source='property.id')
    user = serializers.StringRelatedField()

    class Meta:
        model = Owner
        fields = ['id', 'property', 'user', 'property_details', 'phone_number' ]

class PropertySerializer(serializers.ModelSerializer):
    features = PropertyFeaturesSerializer(many=True, required=False)
    owners = OwnerSerializer(many=True, read_only=True, source='owned_properties')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property 
        fields = ['slug', 'title', 'description', 'price', 'image', 'city', 'address', 'listed_at', 'updated_at', 'features']
    
    def create(self,request, **validated_data):
        features_data = validated_data.pop('features', [])
        images_data = validated_data.pop('images', [])

        property_instance = Property.objects.create(**validated_data)

        for feature_data in features_data:
            Property_Features.objects.create(property=property_instance, **feature_data)
        
        for image_data in images_data:
            Image.objects.create(property=property_instance, **image_data)

        return property_instance

    def update(self, instance, **validated_data):
        features_data = validated_data.pop('features', [])
        images_data = validated_data.pop('images', [])

        instance.title = validated_data.get('name', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        
        instance.features.all().delete()
        for feature_data in features_data:
            Property_Features.objects.create(property=instance, **feature_data)

        instance.images.all().delete()
        for image_data in images_data:
            Image.objects.create(property=instance, **image_data)

        return instance

class TransactionSerializer(serializers.ModelSerializer):
    payment_details = serializers.SerializerMethodField()
    payment = serializers.PrimaryKeyRelatedField(read_only=True, source='payment.id')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date_paid', 'transaction_desc', 'payment_details', 'payment']

    def get_payment_details(self, obj):
        return PaymentSerializer(obj.payment).data

class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, source='transactions', read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'price', 'user', 'transaction_type', 'updated_at', 'description', 'added_at', 'transactions']

class CartItemSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source="property.title", read_only=True)
    slug = serializers.SlugField()

    class Meta:
        model = CartItem
        fields = ['slug', 'property_name', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    slug =serializers.SlugField()
   
    class Meta:
        model = Cart
        fields = ['slug', 'total_price', 'items', 'user']
    
    def get_total_price(self, obj):
        total = sum(item.quantity * item.property.price for item in obj.items.all())
        return total

class OrderItemSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    property_name = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['slug', 'quantity', 'property_name']

class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(source="order_items" ,many=True, read_only=True)
    slug = serializers.SlugField()
    user = CustomUserSerializer(source="order", read_only=True)

    class Meta:
        model = Order
        fields = ['slug', 'user', 'created_at', 'updated_at']

class AgentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source='CustomUser.username', read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone_number', 'dob', 'listings', 'is_available']

class ClientSerializer(serializers.ModelSerializer):
    tenant = CustomUserSerializer(source='CustomUser.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'tenant', 'phone_number', 'has_paid']

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'received_at', 'is_read']