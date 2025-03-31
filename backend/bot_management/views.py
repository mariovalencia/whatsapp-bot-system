from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, QuestionAnswer, AlternativeQuestion
from .serializers import CategorySerializer, QuestionAnswerSerializer, AlternativeQuestionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar categorías
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar preguntas y respuestas
    """
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_alternative(self, request, pk=None):
        """
        Añadir pregunta alternativa a un QA existente
        """
        question_answer = self.get_object()
        serializer = AlternativeQuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(question_answer=question_answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def alternatives(self, request, pk=None):
        """
        Listar todas las preguntas alternativas de un QA
        """
        question_answer = self.get_object()
        alternatives = question_answer.alternatives.all()
        serializer = AlternativeQuestionSerializer(alternatives, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Filtrar preguntas por categoría
        """
        category_id = request.query_params.get('category', None)
        if category_id:
            questions = self.queryset.filter(category_id=category_id)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere un ID de categoría"}, status=status.HTTP_400_BAD_REQUEST)

class AlternativeQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar preguntas alternativas
    """
    queryset = AlternativeQuestion.objects.all()
    serializer_class = AlternativeQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
