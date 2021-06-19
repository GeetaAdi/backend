from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import AttitudeSerializer, CpcqSerializer
from .serializers import EmpathySerializer
from .serializers import PolicySerializer
from .serializers import ProfessionalismSerializer
from .serializers import TeachingSerializer
from .serializers import ResponsesSerializer
from .serializers import PreSurveySerializer
from .serializers import PostSurveySerializer
from .serializers import FinalFeedbackSerializer
from .serializers import ProfileSerializer, CPCQResponsesSerializer, ScoresSerializer, PreSurveyQuestionsSerializer, PostSurveyQuestionsSerializer, StatusSerializer
from .models import Attitude, Profile, cpcq, CPCQResponses, Scores, PreSurveyQuestions, PostSurveyQuestions, Status
from .models import Empathy
from .models import Policy
from .models import Professionalism
from .models import Teaching
from .models import Responses
from .models import PreSurvey
from .models import PostSurvey
from .models import FinalFeedback
import random

# from djangocrud.api.serializers import UserSerializer



# from .models import Inquiry
from rest_framework import generics, permissions
from rest_framework.response import Response

from knox.models import AuthToken

from knox.auth import TokenAuthentication

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ScoreForm, RadioForm1, RadioForm2, RadioForm3, RadioForm4

from django.conf import settings
from django.core.mail import send_mail

def email(request):
    user_id = request.GET.get('user_id', '')
    print(user_id)
    user = User.objects.get(id = user_id)
    score = Scores.objects.get(username=user.username)
    if CPCQResponses.objects.filter(user = user).exists():
        stat = CPCQResponses.objects.filter(user = user)
        count = 0
        for each in stat:
            count = count + (len(each.scores) - 1)   
    if count >= 5:
        score.email_status = True
        score.save()
        s = Status.objects.get(username = user.username)
        s.scoresstatus = True
        s.save()
        # serializer_ = ScoresSerializer(score, data = {'email_status' : True}, partial=True)
        # if serializer_.is_valid():
        #     serializer_.save()    
        subject = 'CPCDP View Your Results'
        message = f"Hi {user.first_name.capitalize()}, thank you for your current engagement with the Cultural Proficiency Continuum Web-Based Dialogic Protocol: A Majority-Minority PreK-12 Schooling Context. Your reactions to vignettes have been reviewed and scored by your facilitator. You can now login and view your facilitator's comments and scores. Please login at https://cpcdp-vcu.cs.odu.edu/ to review your comments and scores."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect('http://127.0.0.1:7002/admin/api/scores/')
    else:
        return HttpResponseRedirect('http://127.0.0.1:7002/admin/api/scores/')

def scores(request):
    response_id = request.GET.get('response_id', '')
    user_id = request.GET.get('user_id', '')
    topic = request.GET.get('topic', '')
    value = request.GET.get('value', '')
    field = request.GET.get('field', '')
    num = {'A' : 'question1', 'B': 'question2', 'C': 'question3', 'D': 'question4', 'E': 'question5', 'F': 'question6'}
    if topic == 'Attitude':
        question = Attitude.objects.get(id = 1)
        if value[0:1] == 'A':
            question_final = question.question1
        if value[0:1] == 'B':
            question_final = question.question2
        if value[0:1] == 'C':
            question_final = question.question3
        if value[0:1] == 'D':
            question_final = question.question4
        if value[0:1] == 'E':
            question_final = question.question5
        if value[0:1] == 'F':
            question_final = question.question6
    elif topic == 'Empathy':
        question = Empathy.objects.get(id = 1)
        if value[0:1] == 'A':
            question_final = question.question1
        if value[0:1] == 'B':
            question_final = question.question2
        if value[0:1] == 'C':
            question_final = question.question3
        if value[0:1] == 'D':
            question_final = question.question4
        if value[0:1] == 'E':
            question_final = question.question5
        if value[0:1] == 'F':
            question_final = question.question6
    elif topic == 'Policy':
        question = Policy.objects.get(id = 1)
        if value[0:1] == 'A':
            question_final = question.question1
        if value[0:1] == 'B':
            question_final = question.question2
        if value[0:1] == 'C':
            question_final = question.question3
        if value[0:1] == 'D':
            question_final = question.question4
        if value[0:1] == 'E':
            question_final = question.question5
        if value[0:1] == 'F':
            question_final = question.question6
    elif topic == 'Professionalism':
        question = Professionalism.objects.get(id = 1)
        if value[0:1] == 'A':
            question_final = question.question1
        if value[0:1] == 'B':
            question_final = question.question2
        if value[0:1] == 'C':
            question_final = question.question3
        if value[0:1] == 'D':
            question_final = question.question4
        if value[0:1] == 'E':
            question_final = question.question5
        if value[0:1] == 'F':
            question_final = question.question6
    else:
        question = Teaching.objects.get(id = 1)
        if value[0:1] == 'A':
            question_final = question.question1
        if value[0:1] == 'B':
            question_final = question.question2
        if value[0:1] == 'C':
            question_final = question.question3
        if value[0:1] == 'D':
            question_final = question.question4
        if value[0:1] == 'E':
            question_final = question.question5
        if value[0:1] == 'F':
            question_final = question.question6

    final =  []
    queryset = CPCQResponses.objects.filter(response_id = response_id, user = user_id).exclude(culturalDestructivenessresponse__exact = '',
    culturalIncapacityresponse__exact = '', culturalBlindnessresponse__exact = '', culturalPreCompetenceresponse__exact = '', culturalCompetenceresponse__exact = '', culturalProficiencyresponse__exact = '')
    for obj in queryset:
        if obj.culturalDestructivenessresponse != '' and field == 'culturalDestructivenessresponse':
            final.append(obj.culturalDestructivenessresponse)
        if obj.culturalIncapacityresponse != '' and field == 'culturalIncapacityresponse':
            final.append(obj.culturalIncapacityresponse)
        if obj.culturalBlindnessresponse != '' and field == 'culturalBlindnessresponse':
            final.append(obj.culturalBlindnessresponse)
        if obj.culturalPreCompetenceresponse != '' and field == 'culturalPreCompetenceresponse':
            final.append(obj.culturalPreCompetenceresponse)
        if obj.culturalCompetenceresponse != '' and field == 'culturalCompetenceresponse':
            final.append(obj.culturalCompetenceresponse)
        if obj.culturalProficiencyresponse != '' and field == 'culturalProficiencyresponse':
            final.append(obj.culturalProficiencyresponse)
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        form1 = RadioForm1(request.POST)
        form2 = RadioForm2(request.POST)
        form3 = RadioForm3(request.POST)
        form4 = RadioForm4(request.POST)
        if form.is_valid() and form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            data = {}
            total_score = {}
            # score = form.cleaned_data['score']
            score1 = form1.cleaned_data['score1']
            score2 = form2.cleaned_data['score2']
            score3 = form3.cleaned_data['score3']
            score4 = form4.cleaned_data['score4']
            score = [int(score1), int(score2), int(score3), int(score4)]
            comment_1 = form.cleaned_data['Comments_For_Participant']
            comment_2 = form.cleaned_data['Comments_For_Facilitator']
            user = User.objects.get(id = user_id)
            if CPCQResponses.objects.filter(response_id = response_id).exists():
                stat = CPCQResponses.objects.get(response_id = response_id)
                if stat.scores == []:
                    data['scores'] = {'category':[field], value : score}        
                    data['status'] = True
                    data['comment1'] = {value : comment_1}
                    data['comment2'] = {value : comment_2}

                    serializer_ = CPCQResponsesSerializer(stat, data = data, partial=True)
                    if serializer_.is_valid():
                        serializer_.save()
                else:
                    keys = list(stat.scores.keys())                                      
                    if value not in keys and field not in stat.scores['category']:
                        stat.scores['category'].append(field)
                        stat.scores[value] = score
                    else:
                        index = stat.scores['category'].index(field)
                        stat.scores[keys[index + 1]] = score
                    serializer_ = CPCQResponsesSerializer(stat, data = stat.scores, partial=True)
                    if serializer_.is_valid():
                        serializer_.save()
                    stat.comment1[value] = comment_1
                    stat.comment2[value] = comment_2
                    serializer_ = CPCQResponsesSerializer(stat, data = stat.comment1, partial=True)
                    if serializer_.is_valid():
                        serializer_.save()
                    serializer_ = CPCQResponsesSerializer(stat, data = stat.comment2, partial=True)
                    if serializer_.is_valid():
                        serializer_.save()

            if Scores.objects.filter(username = user.username).exists():
                scores_ = Scores.objects.get(username = user.username)
                all_scores = CPCQResponses.objects.filter(user = user)
                avg = []
                for each in all_scores:
                    for each_ in each.scores:
                        if each_ != 'category':
                            avg.append(sum(each.scores[each_]) / len(each.scores[each_]))                
                total_score['totalScore'] = sum(avg) / len(avg)
                serializer = ScoresSerializer(scores_, data = total_score, partial=True)
                if serializer.is_valid():
                    serializer.save()
            else:
                if CPCQResponses.objects.filter(user = user).exists():
                    duration = 0
                    avg = []
                    duration_obj = CPCQResponses.objects.filter(user = user)
                    for each in duration_obj:
                        duration = duration + each.duration
                        for each_ in each.scores:
                            if each_ != 'category':
                                avg.append(sum(each.scores[each_]) / len(each.scores[each_]))
                Scores.objects.create(user = user, username=user.username, totalScore=sum(avg) / len(avg), duration = duration)            
            return HttpResponseRedirect('http://127.0.0.1:7002/admin/api/responses/')
    else:
        form = ScoreForm()
        rForms = {}
        r = [RadioForm1(), RadioForm2(), RadioForm3(), RadioForm4()]
        for k,v in final[0].items():
            rForms[k] = r[int(k[0])-1]
        print(rForms)
        # form1 = RadioForm()
        # form2 = RadioForm()
        # form3 = RadioForm()
        # form4 = RadioForm()
    return render(request, 'scores.html', {'form': form, 'rForm': rForms, 'final' : final, 'question_final': question_final })

class ReportsView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        cpcq = CPCQResponses.objects.filter(user = user)
        d = {'series': [], 'category': [], 'pk': [], 'type': [], 'topic': [], 'scores': []}
        for each in cpcq:
            for each_ in each.scores:
                if each_ == 'category':
                    for i in range(len(each.scores[each_])):
                        var = each.scores[each_][i]
                        if var == 'culturalDestructivenessresponse':
                            d['type'].append(each.culturalDestructivenessresponse)
                        if var == 'culturalIncapacityresponse':
                            d['type'].append(each.culturalIncapacityresponse)
                        if var == 'culturalBlindnessresponse':
                            d['type'].append(each.culturalBlindnessresponse)
                        if var == 'culturalPreCompetenceresponse':
                            d['type'].append(each.culturalPreCompetenceresponse)
                        if var == 'culturalCompetenceresponse':
                            d['type'].append(each.culturalCompetenceresponse)
                        if var == 'culturalProficiencyresponse':
                            d['type'].append(each.culturalProficiencyresponse)
                # if each.id not in d['pk']:
                if each_ != 'category':
                    d['topic'].append(each.topic)
                    d['pk'].append(each.id)
                    d['series'].append({'name': each_, 'data': sum(each.scores[each_]) / len(each.scores[each_])})
                    d['category'].append(each_)
                    d['scores'].append(each.scores[each_])
        return Response(d)



class UserAPIView(generics.RetrieveAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)   
    
    def patch(self, request, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(id=request.data['id'])
        del request.data['id']
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttitudeViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Attitude.objects.all()
    serializer_class = AttitudeSerializer


class EmpathyViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Empathy.objects.all()
    serializer_class = EmpathySerializer


class PolicyViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class ProfessionalismViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Professionalism.objects.all()
    serializer_class = ProfessionalismSerializer


class TeachingViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Teaching.objects.all()
    serializer_class = TeachingSerializer

class PreSurveyQuestionsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = PreSurveyQuestions.objects.all()
    serializer_class = PreSurveyQuestionsSerializer

class PostSurveyQuestionsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = PostSurveyQuestions.objects.all()
    serializer_class = PostSurveyQuestionsSerializer


class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)    
    def patch(self, request, *args, **kwargs):
        params = self.request.query_params
        value = params.get('value', None)
        user = self.request.user
        username = User.objects.get(username = user).username
        if value == 'responsesstatus':
            s = Status.objects.get(username = user)
            s.responsesstatus = True
            s.save()     
        if value == 'cpcqstatus':
            s = Status.objects.get(username = user)
            s.cpcqstatus = True
            s.save() 
        if value == 'finalfeedbackstatus':
            s = Status.objects.get(username = user)
            s.finalfeedbackstatus = True
            s.save() 
        if value == 'postsurveystatus':
            s = Status.objects.get(username = user)
            s.postsurveystatus = True
            s.save()
        return Response({'success':1})  

class CpcqViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = cpcq.objects.all()
    serializer_class = CpcqSerializer
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)
    def perform_create(self, serializer):
        user = self.request.user
        username = User.objects.get(username = user).username
        serializer.save(user = user, username = username, status=True)

class CPCQResponsesView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    def get(self, request, *args, **kwargs):
        cpcq = CPCQResponses.objects.filter(user = self.request.user)
        user_dict = [dict(d) for d in CPCQResponsesSerializer(cpcq, many=True).data]
        return Response(user_dict)
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        user = self.request.user
        count = 0
        if CPCQResponses.objects.filter(response_id = data['response_id']).exists():
            stat = CPCQResponses.objects.get(response_id = data['response_id'])
            del data['response_id']
            data['duration'] = stat.duration + data['duration']
            serializer = CPCQResponsesSerializer(stat, data = data, partial=True)
            if serializer.is_valid():
                serializer.save()
        else:
            if 'culturalDestructivenessresponse' not in data:
                data['culturalDestructivenessresponse'] = ''
            if 'culturalIncapacityresponse' not in data:
                data['culturalIncapacityresponse'] = ''
            if 'culturalBlindnessresponse' not in data:
                data['culturalBlindnessresponse'] = ''
            if 'culturalPreCompetenceresponse' not in data:
                data['culturalPreCompetenceresponse'] = ''
            if 'culturalCompetenceresponse' not in data:
                data['culturalCompetenceresponse'] = ''
            if 'culturalProficiencyresponse' not in data:
                data['culturalProficiencyresponse'] = ''
            if 'duration' not in data:
                data['duration'] = 0
            CPCQResponses.objects.create(user = self.request.user, response_id = Responses.objects.get(id = data['response_id']), topic = data['topic'], culturalDestructivenessresponse = data['culturalDestructivenessresponse'], culturalIncapacityresponse = data['culturalIncapacityresponse'], culturalBlindnessresponse = data['culturalBlindnessresponse'], culturalPreCompetenceresponse = data['culturalPreCompetenceresponse'], culturalCompetenceresponse = data['culturalCompetenceresponse'], culturalProficiencyresponse = data['culturalProficiencyresponse'], duration = data['duration'])
        return Response({"success": 1})


class ResponsesViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Responses.objects.all().order_by('topic')
    serializer_class = ResponsesSerializer
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user) 

    def perform_create(self, serializer):
        user = self.request.user
        username = User.objects.get(username = user).username
        print(username)
        serializer.save(user = user, username = username, status=True)

class ResponsesAllView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        details = Responses.objects.filter(user = user).order_by('topic')
        user_dict = [dict(d) for d in ResponsesSerializer(details, many=True).data]
        d = []
        count = 1
        for u in user_dict:
            final = {}
            final['id'] = u['id']
            final['topic'] = u['topic']
            options = u['culturalDestructiveness']
            result = int(options.split(". ")[1])
            result = abs(result - 1)
            if result >= 2:
                color = bool(random.getrandbits(1))
                if CPCQResponses.objects.filter(user = user, topic = u['topic']).exists():
                    stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first()
                else:
                    stat = None
                print(stat)
                if stat:                
                    if color and count < 6 and stat.culturalDestructivenessresponse == '':
                        final['1'] = [u['culturalDestructiveness'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalDestructivenessresponse != '':
                        final['1'] = [u['culturalDestructiveness'], 'greencolorbold']
                        count = count + 1
                    else:                    
                        final['1'] = [u['culturalDestructiveness'], 'bold']
                else:
                    if color and count < 6:
                        final['1'] = [u['culturalDestructiveness'], 'colorbold']
                        count = count + 1
                    else:                    
                        final['1'] = [u['culturalDestructiveness'], 'bold']
            else:
                final['1'] = [u['culturalDestructiveness'], 'nobold']
            
            options = u['culturalIncapacity']
            result = int(options.split(". ")[1])
            result = abs(result - 2)
            if result >= 2:
                color = bool(random.getrandbits(1))
                if CPCQResponses.objects.filter(user = user, topic = u['topic']).exists():
                    stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first()
                else:
                    stat = None  
                if stat:
                    if color and count < 6 and stat.culturalIncapacityresponse == '':
                        final['2'] = [u['culturalIncapacity'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalIncapacityresponse != '':
                        final['2'] = [u['culturalIncapacity'], 'greencolorbold']
                        count = count + 1
                    else:
                        final['2'] = [u['culturalIncapacity'], 'bold']
                else:
                    if color and count < 6:
                        final['2'] = [u['culturalIncapacity'], 'colorbold']
                        count = count + 1
                    else:
                        final['2'] = [u['culturalIncapacity'], 'bold']
            else:
                final['2'] = [u['culturalIncapacity'], 'nobold']
            
            options = u['culturalBlindness']
            result = int(options.split(". ")[1])
            result = abs(result - 3)
            if result >= 2:
                color = bool(random.getrandbits(1))
                if CPCQResponses.objects.filter(user = user, topic = u['topic']).exists():
                    stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first()
                else:
                    stat = None
                if stat:
                    if color and count < 6 and stat.culturalBlindnessresponse == '':
                        final['3'] = [u['culturalBlindness'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalBlindnessresponse != '':
                        final['3'] = [u['culturalBlindness'], 'greencolorbold']
                        count = count + 1               
                    else:
                        final['3'] = [u['culturalBlindness'], 'bold']
                else:
                    if color and count < 6:
                        final['3'] = [u['culturalBlindness'], 'colorbold']
                        count = count + 1
                    else:
                        final['3'] = [u['culturalBlindness'], 'bold']
            else:
                final['3'] = [u['culturalBlindness'], 'nobold']
            
            options = u['culturalPreCompetence']
            result = int(options.split(". ")[1])
            result = abs(result - 4)
            if result >= 2:
                color = bool(random.getrandbits(1))
                if CPCQResponses.objects.filter(user = user, topic = u['topic']).exists():
                    stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first()
                else:
                    stat = None
                if stat:
                    if color and count < 6 and stat.culturalPreCompetenceresponse == '':
                        final['4'] = [u['culturalPreCompetence'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalPreCompetenceresponse != '':
                        final['4'] = [u['culturalPreCompetence'], 'greencolorbold']
                        count = count + 1
                    else:
                        final['4'] = [u['culturalPreCompetence'], 'bold']
                else:
                    if color and count < 6:
                        final['4'] = [u['culturalPreCompetence'], 'colorbold']
                        count = count + 1
                    else:
                        final['4'] = [u['culturalPreCompetence'], 'bold']
            else:
                final['4'] = [u['culturalPreCompetence'], 'nobold']
            
            options = u['culturalCompetence']
            result = int(options.split(". ")[1])
            result = abs(result - 5)
            if result >= 2:
                color = bool(random.getrandbits(1))
                stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first() 
                if stat: 
                    if color and count < 6 and stat.culturalCompetenceresponse == '':
                        final['5'] = [u['culturalCompetence'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalCompetenceresponse != '':
                        final['5'] = [u['culturalCompetence'], 'greencolorbold']
                        count = count + 1
                    else:
                        final['5'] = [u['culturalCompetence'], 'bold']
                else:
                    if color and count < 6:
                        final['5'] = [u['culturalCompetence'], 'colorbold']
                        count = count + 1
                    else:
                        final['5'] = [u['culturalCompetence'], 'bold']
            else:
                final['5'] = [u['culturalCompetence'], 'nobold']
            
            options = u['culturalProficiency']
            result = int(options.split(". ")[1])
            result = abs(result - 6)
            if result >= 2:
                color = bool(random.getrandbits(1))
                if CPCQResponses.objects.filter(user = user, topic = u['topic']).exists():
                    stat = CPCQResponses.objects.filter(user = user, topic = u['topic']).first()
                else:
                    stat = None
                if stat:  
                    if color and count < 6 and stat.culturalProficiencyresponse == '':
                        final['6'] = [u['culturalProficiency'], 'colorbold']
                        count = count + 1
                    elif count < 6 and stat.culturalProficiencyresponse != '':
                        final['6'] = [u['culturalProficiency'], 'greencolorbold']
                        count = count + 1
                    else:
                        final['6'] = [u['culturalProficiency'], 'bold']
                else:
                    if color and count < 6:
                        final['6'] = [u['culturalProficiency'], 'colorbold']
                        count = count + 1
                    else:
                        final['6'] = [u['culturalProficiency'], 'bold']
            else:
                final['6'] = [u['culturalProficiency'], 'nobold']
            d.append(final)
        while count < 6:
            list = [0,1,2,3,4]
            num = random.choice(list)
            for k in d[num].keys():
                if k != 'topic' and k != 'id':
                    print(k)
                    if 'bold' in d[num][k]:
                        d[num][k] = [d[num][k][0], 'colorbold']
                        count = count + 1
                        break
        return Response(d)


class PreSurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = PreSurvey.objects.all()
    serializer_class = PreSurveySerializer

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user) 

    def perform_create(self, serializer):
        user = self.request.user
        username = User.objects.get(username = user).username
        Status.objects.create(user = user, username = username, presurveystatus=True)
        serializer.save(user = user, username = username, status=True)


class PostSurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = PostSurvey.objects.all()
    serializer_class = PostSurveySerializer
    def perform_create(self, serializer):
        user = self.request.user
        username = User.objects.get(username = user).username
        serializer.save(user = user, username = username, status=True) 

class FinalFeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = FinalFeedback.objects.all()
    serializer_class = FinalFeedbackSerializer
    def perform_create(self, serializer):
        user = self.request.user
        username = User.objects.get(username = user).username
        serializer.save(user = user, username = username, status=True) 

# class UsersLogViewSet(viewsets.ModelViewSet):
#     queryset = UsersLog.objects.all()
#     serializer_class = UsersLogSerializer