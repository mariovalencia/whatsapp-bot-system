from rest_framework import serializers
from django.contrib.auth.models import User
from security.models import Role, Permission, UserProfile, RolePermission
from bot_management.models import Category, QuestionAnswer, AlternativeQuestion
from whatsapp_integration.models import WhatsAppSession, Contact, Conversation, Message

# Security Serializers
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'name', 'description']

class RolePermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='permission.name', read_only=True)
    code = serializers.CharField(source='permission.code', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['id', 'permission', 'name', 'code']

class RoleSerializer(serializers.ModelSerializer):
    permissions = RolePermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'permissions']

class UserProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'role_name', 'phone', 'is_active_agent', 'last_login_ip']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
            
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        # Actualizar usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        instance.save()
        
        # Actualizar perfil si existe
        if profile_data and hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
            
        return instance

# Bot Management Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'update_at']

class AlternativeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeQuestion
        fields = ['id', 'text']

class QuestionAnswerSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'category', 'category_name', 'question', 'answer', 
                  'keywords', 'priority', 'is_active', 'created_by', 
                  'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

class QuestionAnswerDetailSerializer(serializers.ModelSerializer):
    alternatives = AlternativeQuestionSerializer(many=True, required=False)
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'category', 'category_name', 'question', 'answer', 
                  'keywords', 'priority', 'is_active', 'created_by', 
                  'created_by_name', 'created_at', 'updated_at', 'alternatives']
        read_only_fields = ['created_by']
    
    def create(self, validated_data):
        alternatives_data = validated_data.pop('alternatives', [])
        question_answer = QuestionAnswer.objects.create(**validated_data)
        
        for alternative_data in alternatives_data:
            AlternativeQuestion.objects.create(question_answer=question_answer, **alternative_data)
            
        return question_answer
    
    def update(self, instance, validated_data):
        alternatives_data = validated_data.pop('alternatives', None)
        
        # Actualizar QA
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar alternativas si se proporcionaron
        if alternatives_data is not None:
            # Eliminar las existentes y crear nuevas
            instance.alternatives.all().delete()
            for alternative_data in alternatives_data:
                AlternativeQuestion.objects.create(question_answer=instance, **alternative_data)
                
        return instance

# WhatsApp Integration Serializers
class WhatsAppSessionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = WhatsAppSession
        fields = ['id', 'session_id', 'is_active', 'last_qr_code', 'qr_generated_at',
                  'connected_at', 'disconnected_at', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by', 'last_qr_code', 'qr_generated_at', 'connected_at', 'disconnected_at']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone', 'name', 'is_blocked', 'last_interaction', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sent_by_name = serializers.CharField(source='sent_by.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'message_id', 'content', 'type',
                  'sent_by', 'sent_by_name', 'is_from_bot', 'timestamp']
        read_only_fields = ['message_id']

class ConversationSerializer(serializers.ModelSerializer):
    contact_info = ContactSerializer(source='contact', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'contact', 'contact_info', 'started_at', 'ended_at',
                  'is_active', 'assigned_to', 'assigned_to_name', 'bot_mode', 'message_count']
    
    def get_message_count(self, obj):
        return obj.messages.count()