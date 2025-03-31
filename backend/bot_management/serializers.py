from rest_framework import serializers
from .models import Category, QuestionAnswer, AlternativeQuestion

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Category
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'update_at']
        read_only_fields = ['id', 'created_at', 'update_at']

class AlternativeQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AlternativeQuestion
    """
    class Meta:
        model = AlternativeQuestion
        fields = ['id', 'question_answer', 'text']
        read_only_fields = ['id']
        extra_kwargs = {
            'question_answer': {'required': False}
        }

class QuestionAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo QuestionAnswer
    """
    alternatives = AlternativeQuestionSerializer(many=True, read_only=True)
    created_by_username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = QuestionAnswer
        fields = [
            'id', 'category', 'category_name', 'question', 'answer', 
            'keywords', 'priority', 'is_active', 'created_by', 
            'created_by_username', 'created_at', 'updated_at', 'alternatives'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_created_by_username(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None
    
    def get_category_name(self, obj):
        return obj.category.name