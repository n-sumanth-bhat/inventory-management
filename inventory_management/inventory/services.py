from .models import Item
from .serializers import *
from utils.custom_exceptions import AlreadyExistsException, NotFoundException, ValidationException, AuthenticationFailed
from django.core.cache import cache
from django.db import transaction

class UserService:
    @staticmethod
    def register_user(data):
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return RegisterSerializer(user).data
        else:
            raise ValidationException(desc=serializer.errors)

    @staticmethod
    def login_user(data):
        serializer = LoginSerializer(data=data)
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials')

        if not user.check_password(data.get('password')):
            raise AuthenticationFailed('Invalid credentials')

        token = serializer.get_token(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }


class ItemService:
    @staticmethod
    @transaction.atomic
    def create_item(data):
        if Item.objects.filter(name=data.get('name')).exists():
            raise AlreadyExistsException(error="Item already exists", desc=f"An item with name {data.get('name')} already exists.")

        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            item = serializer.save()
            return ItemSerializer(item).data
        else:
            raise ValidationException(serializer.errors)

    @staticmethod
    @transaction.atomic
    def update_item(item_id, data):
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                item = serializer.save()
                cache.delete(f"item_{item_id}")  # Invalidate cache
                return ItemSerializer(item).data
            else:
                raise ValidationException(serializer.errors)
        except Item.DoesNotExist:
            raise NotFoundException(error="Item not found", desc=f"Item with id {item_id} does not exist.")

    @staticmethod
    @transaction.atomic
    def delete_item(item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f"item_{item_id}")  # Invalidate cache
            return {"message": "Item deleted successfully."}
        except Item.DoesNotExist:
            raise NotFoundException(error="Item not found", desc=f"Item with id {item_id} does not exist.")
