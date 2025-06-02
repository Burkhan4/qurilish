from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Term, Category
from .serializers import TermSerializer, CategorySerializer
from django.db.models import Q

@api_view(['GET', 'POST'])
def term_list(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        category_id = request.GET.get('category')
        order_by = request.GET.get('order_by', 'word')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        terms = Term.objects.all()

        if search:
            terms = terms.filter(
                Q(word__icontains=search) |
                Q(definition__icontains=search)
            )

        if category_id:
            terms = terms.filter(category_id=category_id)

        if order_by:
            terms = terms.order_by(order_by)

        total_count = terms.count()
        start = (page - 1) * page_size
        end = start + page_size
        terms_page = terms[start:end]

        if not terms_page:
            return Response({'message': 'So‘z topilmadi'}, status=404)

        serializer = TermSerializer(terms_page, many=True)
        return Response({
            'results': serializer.data,
            'total': total_count,
            'page': page,
            'page_size': page_size,
        })

    elif request.method == 'POST':
        serializer = TermSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def term_detail(request, pk):
    try:
        term = Term.objects.get(pk=pk)
    except Term.DoesNotExist:
        return Response({'message': 'So‘z topilmadi'}, status=404)

    if request.method == 'GET':
        serializer = TermSerializer(term)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = TermSerializer(term, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        term.delete()
        return Response({'message': 'So‘z o‘chirildi'}, status=204)


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
