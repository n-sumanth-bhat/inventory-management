from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .services import *
from .selectors import *
from utils.logging_utils import log_request


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        user = UserService.register_user(user_data)
        return Response(user, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        tokens = UserService.login_user(user_data)
        return Response(tokens, status=status.HTTP_200_OK)


class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        user = request.user.username
        try:
            item_data = request.data
            item = ItemService.create_item(item_data)
            log_request(user, "Create Item", "Success")
            return Response(item, status=status.HTTP_201_CREATED)
        except AlreadyExistsException:
            log_request(user, "Create Item", "Failed: Item already exists")
            return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log_request(user, "Create Item", f"Failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IndividualItemOperationView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, item_id):
        user = request.user.username
        try:
            item = ItemSelector.get_item(item_id)
            log_request(user, "Get an Item", "Success")
            return Response(item, status=status.HTTP_200_OK)
        except NotFoundException:
            log_request(user, "Get an Item", "Item not found")
            return Response({"error: Item doesn't exits"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_request(user, "Get an Item", f"Failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def put(request, item_id):
        user = request.user.username
        try:
            item_data = request.data
            item = ItemService.update_item(item_id, item_data)
            log_request(user, "Update an Item", "Success")
            return Response(item, status=status.HTTP_200_OK)
        except NotFoundException:
            log_request(user, "Update an Item", "Item not found")
            return Response({"error: Item doesn't exits"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_request(user, "Update an Item", f"Failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete(request, item_id):
        user = request.user.username
        try:
            result = ItemService.delete_item(item_id)
            log_request(user, "Delete an Item", "Success")
            return Response(result, status=status.HTTP_204_NO_CONTENT)
        except NotFoundException:
            log_request(user, "Delete an Item", "Item not found")
            return Response({"error: Item doesn't exits"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_request(user, "Delete an Item", f"Failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
