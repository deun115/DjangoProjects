from rest_framework import serializers
from polls.models import Question
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner']

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'questions']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        #extra_kwargs = {'password': {'write_only':True}}