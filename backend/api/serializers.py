from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket, Reply

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status', 'created_by', 'created_at')


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description')

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Sarlavha bo'sh bo'lishi mumkin emas.")
        return value


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['open', 'in_progress', 'closed']:
            raise serializers.ValidationError("Noto'g'ri status kiritildi.")
        return value


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = ('id', 'ticket', 'body', 'author', 'created_at')


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('ticket', 'body')

    def validate_body(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Javob matni bo'sh bo'lishi mumkin emas.")
        return value

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket, Reply

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status', 'created_by', 'created_at')


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description')

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Sarlavha bo'sh bo'lishi mumkin emas.")
        return value


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['open', 'in_progress', 'closed']:
            raise serializers.ValidationError("Noto'g'ri status kiritildi.")
        return value


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = ('id', 'ticket', 'body', 'author', 'created_at')


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('ticket', 'body')

    def validate_body(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Javob matni bo'sh bo'lishi mumkin emas.")
        return value
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket, Reply

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status', 'created_by', 'created_at')


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description')

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Sarlavha bo'sh bo'lishi mumkin emas.")
        return value

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Tavsif bo'sh bo'lishi mumkin emas.")
        return value


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['open', 'in_progress', 'closed']:
            raise serializers.ValidationError("Noto'g'ri status kiritildi.")
        return value


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = ('id', 'ticket', 'body', 'author', 'created_at')


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('ticket', 'body')

    def validate_body(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Javob matni bo'sh bo'lishi mumkin emas.")
        return value