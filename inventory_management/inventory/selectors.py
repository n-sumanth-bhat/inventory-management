from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
from utils.custom_exceptions import NotFoundException

class ItemSelector:
    @staticmethod
    def get_item(item_id):
        cache_key = f"item_{item_id}"
        cached_item = cache.get(cache_key)
        if cached_item:
            return cached_item

        try:
            item = Item.objects.get(id=item_id)
            item_data = ItemSerializer(item).data
            cache.set(cache_key, item_data, timeout=3600)
            return item_data
        except Item.DoesNotExist:
            raise NotFoundException(error="Item not found", desc=f"Item with id {item_id} does not exist.")
