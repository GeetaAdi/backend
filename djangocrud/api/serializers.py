from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Attitude, cpcq, CPCQResponses, Scores
from .models import Empathy
from .models import Policy
from .models import Professionalism
from .models import Teaching
from .models import Responses
from .models import PreSurvey
from .models import PostSurvey
from .models import FinalFeedback
from .models import  Profile, PreSurveyQuestions, PostSurveyQuestions, Status



# from .models import Inquiry


User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','last_name')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            first_name = validated_data['first_name'],
            last_name =validated_data['last_name']
        )
        user_ = User.objects.get(username = user)
        Profile.objects.create(user = user_)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ProfileSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    preSurveydate = serializers.SerializerMethodField()
    responsesdate = serializers.SerializerMethodField()
    cpcqdate = serializers.SerializerMethodField()
    scoredate = serializers.SerializerMethodField()
    postSurveydate = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id','user','photo_profile','location','gender','date','status')
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['first_name'] = UserSerializer(instance.user).data['first_name']
        rep['last_name'] = UserSerializer(instance.user).data['last_name']
        rep['email'] = UserSerializer(instance.user).data['email']
        return rep

    def get_location(self, obj):
        if PreSurvey.objects.filter(user = obj.user).exists():
            last = PreSurvey.objects.filter(username = obj.user).last()
            if last is not None:
                return last.q4
            else:
                return None

    def get_gender(self, obj):
        if PreSurvey.objects.filter(user = obj.user).exists():
            last = PreSurvey.objects.filter(username = obj.user).last()
            if last is not None:
                return last.q8
            else:
                return None

    def get_preSurveydate(self, obj):
        if PreSurvey.objects.filter(user = obj.user).exists():
            last = PreSurvey.objects.filter(username = obj.user).last()
            if last is not None:
                return last.created
            else:
                return None

    def get_responsesdate(self, obj):
        if Responses.objects.filter(user = obj.user).exists():
            last = Responses.objects.filter(username = obj.user).last()
            if last is not None:
                return last.created
            else:
                return None

    def get_cpcqdate(self, obj):
        if cpcq.objects.filter(user = obj.user).exists():
            last = cpcq.objects.filter(username = obj.user).last()
            if last is not None:
                return last.created
            else:
                return None

    def get_scoredate(self, obj):
        if Scores.objects.filter(user = obj.user).exists():
            last = Scores.objects.filter(username = obj.user).last()
            if last is not None:
                return last.created
            else:
                return None

    def get_postSurveydate(self, obj):
        if PostSurvey.objects.filter(user = obj.user).exists():
            last = PostSurvey.objects.filter(username = obj.user).last()
            if last is not None:
                return last.created
            else:
                return None

    def get_status(self, obj):
        if cpcq.objects.filter(user = obj.user).exists() and FinalFeedback.objects.filter(user = obj.user).exists():
            last = cpcq.objects.filter(username = obj.user).last()
            if last is not None:
                return [last.status, last.status, last.status, last.status, False, False]
            else:
                return None
        elif PreSurvey.objects.filter(user = obj.user).exists():
            last = PreSurvey.objects.filter(username = obj.user).last()
            if last is not None:
                return [last.status, False, False, False, False, False]
            else:
                return None
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password', 'email']

#         def create(self, validated_data):
#             print("nihaarika123")
#             user = User.objects.create_user(**validated_data)
#             return user


class AttitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attitude
        fields = '__all__'


class EmpathySerializer(serializers.ModelSerializer):
    class Meta:
        model = Empathy
        fields = '__all__'



class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'



class ProfessionalismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professionalism
        fields = '__all__'



class TeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teaching
        fields = '__all__'


class CpcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = cpcq
        fields = '__all__'

class CPCQResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPCQResponses
        fields = '__all__'

class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = '__all__'

class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        fields = '__all__'
        # fields = ['user','username','topic','culturalDestructiveness', 'culturalIncapacity', 'culturalBlindness', 'culturalPreCompetence','culturalCompetence','culturalProficiency']
        # list_display = ['user','username','topic','culturalDestructiveness', 'culturalIncapacity', 'culturalBlindness', 'culturalPreCompetence','culturalCompetence','culturalProficiency']

class PreSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreSurvey
        fields = '__all__'
        # fields = ['user','username','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20']
        # list_display = ['user','username','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20']

class PreSurveyQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreSurveyQuestions
        # fields = '__all__'
        fields = ['question1','question2','question3','question4','question5','question6','question7','question8','question9','question10','question11','question12','question13','question14','question15','question16','question17','question18','question19','question20', 'question21']


class PostSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSurvey
        fields = '__all__'
        # fields = ['user','username','question1','question2','question3','question4','question5','question6','question7','question8','question9']
        # list_display = ['user','username','q1','q2','q3','q4','q5','q6','q7','q8','q9']

class PostSurveyQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSurveyQuestions
        # fields = '__all__'
        fields = ['question1','question2','question3','question4','question5','question6','question7','question8','question9', 'question10', 'question11']


class FinalFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalFeedback
        fields = '__all__'
        # fields = ['user','username','q1','q2','q3','q4','q5','q6','q7']
        # list_display = ['user','username','q1','q2','q3','q4','q5','q6','q7']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
