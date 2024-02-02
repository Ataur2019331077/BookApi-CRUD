from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class AddBook(APIView):
    def post(self, request):
        id = request.data.get("id")
        title = request.data.get("title")
        author = request.data.get("author")
        genre = request.data.get("genre")
        price = request.data.get("price")

        # Check if a book with the provided id already exists
        existing_book = Book.objects.filter(id=id).first()

        if existing_book:
            return Response({"message": f"Book with the provided id: {id} already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create a new book with the provided data
            new_book = Book.objects.create(title=title, author=author, genre=genre, price=price, id=id)
            serializer = BookSerializer(new_book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        search_field = request.query_params.get('search_field', None)
        value = request.query_params.get('value', None)
        sort_field = request.query_params.get('sort', 'id')
        order = request.query_params.get('order', 'asc')

        books = Book.objects.all()

        # Filtering based on query parameters
        if search_field and value:
            filter_kwargs = {f"{search_field}__icontains": value}
            books = books.filter(**filter_kwargs)

        # Sorting based on query parameters
        if sort_field:
            if order == 'DESC' or order == 'desc':
                sort_field = f"-{sort_field}"
            books = books.order_by(sort_field)

        if books.exists():
            serializer = BookSerializer(books, many=True)
            return Response({"books":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"books":[]}, status=status.HTTP_200_OK)
    


class GetBook(APIView):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"message": f"Book with the provided id: {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)



class SearchBook(APIView): 
    def get(self, request):
        search_field = request.query_params.get('search_field', None)
        value = request.query_params.get('value', None)
        sort_field = request.query_params.get('sort', 'id')
        order = request.query_params.get('order', 'asc')

        books = Book.objects.all()

        # Filtering based on query parameters
        if search_field and value:
            filter_kwargs = {f"{search_field}__icontains": value}
            books = books.filter(**filter_kwargs)
            for book in books:
                print(book.title)

        # Sorting based on query parameters
        if sort_field:
            if order == 'DESC' or order == 'desc':
                sort_field = f"-{sort_field}"
            books = books.order_by(sort_field)

        if books.exists():
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)

        

class UpdateBook(APIView):
    def put(self, request, id):
        title = request.data.get("title")
        author = request.data.get("author")
        genre = request.data.get("genre")
        price = request.data.get("price")

        try:
            existing_book = Book.objects.get(id=id)
            existing_book.title = title
            existing_book.author = author
            existing_book.genre = genre
            existing_book.price = price
            existing_book.save()

            serializer = BookSerializer(existing_book)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"message": f"Book with the provided id: {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)