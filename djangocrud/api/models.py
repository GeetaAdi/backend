from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
import os
# from fields.JSONField import JSONField
# from django_mysql.models import JSONField
# from django_jsonfield_backport.models import JSONField

# models.JSONField = JSONField

class Attitude(models.Model):
    question1 = models.CharField(max_length = 1000)
    question2 = models.CharField(max_length = 1000)
    question3 = models.CharField(max_length = 1000)
    question4 = models.CharField(max_length = 1000)
    question5 = models.CharField(max_length = 1000)
    question6 = models.CharField(max_length = 1000)
    class Meta:
        verbose_name_plural = "Attitude"


class Empathy(models.Model):
    question1 = models.CharField(max_length = 1000)
    question2 = models.CharField(max_length = 1000)
    question3 = models.CharField(max_length = 1000)
    question4 = models.CharField(max_length = 1000)
    question5 = models.CharField(max_length = 1000)
    question6 = models.CharField(max_length = 1000)
    class Meta:
        verbose_name_plural = "Empathy"

class Policy(models.Model):
    question1 = models.CharField(max_length = 1000)
    question2 = models.CharField(max_length = 1000)
    question3 = models.CharField(max_length = 1000)
    question4 = models.CharField(max_length = 1000)
    question5 = models.CharField(max_length = 1000)
    question6 = models.CharField(max_length = 1000)
    class Meta:
        verbose_name_plural = "Policy"


class Professionalism(models.Model):
    question1 = models.CharField(max_length = 1000)
    question2 = models.CharField(max_length = 1000)
    question3 = models.CharField(max_length = 1000)
    question4 = models.CharField(max_length = 1000)
    question5 = models.CharField(max_length = 1000)
    question6 = models.CharField(max_length = 1000)
    class Meta:
        verbose_name_plural = "Professionalism"

class Teaching(models.Model):
    question1 = models.CharField(max_length = 1000)
    question2 = models.CharField(max_length = 1000)
    question3 = models.CharField(max_length = 1000)
    question4 = models.CharField(max_length = 1000)
    question5 = models.CharField(max_length = 1000)
    question6 = models.CharField(max_length = 1000)
    class Meta:
        verbose_name_plural = "Teaching"

class cpcq(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    choices = models.CharField(max_length = 3999, blank=True, null=True, default='')
    class Meta:
        verbose_name_plural = "CPCQ"

class CPCQResponses(models.Model):
    response_id = models.ForeignKey('Responses', on_delete=models.CASCADE, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    topic = models.CharField(max_length = 20,blank=True, null=True, default='')
    culturalDestructivenessresponse = models.JSONField(blank=True, null=True, default='')
    culturalIncapacityresponse = models.JSONField(blank=True, null=True, default='')
    culturalBlindnessresponse = models.JSONField(blank=True, null=True, default='')
    culturalPreCompetenceresponse = models.JSONField(blank=True, null=True, default='')
    culturalCompetenceresponse = models.JSONField(blank=True, null=True, default='')
    culturalProficiencyresponse = models.JSONField(blank=True, null=True, default='')
    duration  = models.FloatField(blank=True, null=True, default=0)
    status = models.BooleanField(default=False)
    scores = models.JSONField(default = list)
    comment1 = models.JSONField(default = list)
    comment2 = models.JSONField(default = list)

    class Meta:
        verbose_name_plural = "CPCQResponses"
        ordering = ['topic']

class Responses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    topic = models.CharField(max_length = 20)
    culturalDestructiveness = models.CharField(max_length=5)
    culturalIncapacity = models.CharField(max_length=5)
    culturalBlindness = models.CharField(max_length=5)
    culturalPreCompetence = models.CharField(max_length=5)
    culturalCompetence = models.CharField(max_length=5)
    culturalProficiency = models.CharField(max_length=5)
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    duration  = models.FloatField(blank=True, null=True, default=0)
    # scores = models.JSONField(default = list)
    # comment1 = models.CharField(max_length=1000, blank=True, null=True, default='')
    # comment2 = models.CharField(max_length=1000, blank=True, null=True, default='')

    def cultural_Destructiveness(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic) + '&value=' + str(self.culturalDestructiveness)+ '&field=culturalDestructivenessresponse'
        result = int(self.culturalDestructiveness.split(". ")[1])
        result = abs(result - 1)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalDestructivenessresponse == "":
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalDestructiveness)
                else:
                    if r.status == True and 'culturalDestructivenessresponse' in r.scores['category']:                        
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalDestructiveness + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalDestructivenessresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalDestructiveness + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalDestructiveness)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalDestructiveness)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalDestructiveness)

    cultural_Destructiveness.allow_tags = True

    def cultural_Incapacity(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic)+ '&value=' + str(self.culturalIncapacity)+ '&field=culturalIncapacityresponse'
        result = int(self.culturalIncapacity.split(". ")[1])
        result = abs(result - 2)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalIncapacityresponse == "":
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalIncapacity)
                else:                    
                    if r.status == True and 'culturalIncapacityresponse' in r.scores['category']:
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalIncapacity + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalIncapacityresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalIncapacity + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalIncapacity)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalIncapacity)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalIncapacity)

    cultural_Incapacity.allow_tags = True

    def cultural_Blindness(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic)+ '&value=' + str(self.culturalBlindness)+ '&field=culturalBlindnessresponse'
        result = int(self.culturalBlindness.split(". ")[1])
        result = abs(result - 3)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalBlindnessresponse == "":
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalBlindness)
                else:                    
                    if r.status == True and 'culturalBlindnessresponse' in r.scores['category']:
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalBlindness + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalBlindnessresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalBlindness + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalBlindness)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalBlindness)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalBlindness)

    cultural_Blindness.allow_tags = True

    def cultural_PreCompetence(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic)+ '&value=' + str(self.culturalPreCompetence)+ '&field=culturalPreCompetenceresponse'
        result = int(self.culturalPreCompetence.split(". ")[1])
        result = abs(result - 4)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalPreCompetenceresponse == "":                    
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalPreCompetence)
                else:                    
                    if r.status == True and 'culturalPreCompetenceresponse' in r.scores['category']:
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalPreCompetence + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalPreCompetenceresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalPreCompetence + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalPreCompetence)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalPreCompetence)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalPreCompetence)

    cultural_PreCompetence.allow_tags = True

    def cultural_Competence(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic)+ '&value=' + str(self.culturalCompetence)+ '&field=culturalCompetenceresponse'
        result = int(self.culturalCompetence.split(". ")[1])
        result = abs(result - 5)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalCompetenceresponse == "":
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalCompetence)
                else:                    
                    if r.status == True and 'culturalCompetenceresponse' in r.scores['category']:
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalCompetence + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalCompetenceresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalCompetence + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalCompetence)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalCompetence)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalCompetence)

    cultural_Competence.allow_tags = True

    def cultural_Proficiency(self):
        url = 'http://cpcdp.tedoratech.com/api/scores/?response_id=' + str(self.id) + '&user_id=' + str(self.user.id) + '&topic=' + str(self.topic)+ '&value=' + str(self.culturalProficiency)+ '&field=culturalProficiencyresponse'
        # url = (
        #     reverse("admin:api_cpcqresponses_changelist")
        #     + "?"
        #     + urlencode({"responses__id": f"{self.id}"})
        # )
        result = int(self.culturalProficiency.split(". ")[1])
        result = abs(result - 6)
        if result >= 2:
            if CPCQResponses.objects.filter(response_id = self.id).exists():
                r = CPCQResponses.objects.get(response_id = self.id)
                if r.culturalProficiencyresponse == "":
                    return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalProficiency)
                else:                    
                    if r.status == True and 'culturalProficiencyresponse' in r.scores['category']:
                        if len(list(r.scores.keys())) == 2:
                            res = list(r.scores.keys())[1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalProficiency + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                        else:
                            index = r.scores['category'].index('culturalProficiencyresponse')
                            res = list(r.scores.keys())[index + 1]
                            return format_html('<a href="{}"><span style="color: #008000; font-weight: bold;">{}</span></a>', url, self.culturalProficiency + ' Scores: ' + str(r.scores[res])[1:-1] + ' Total: ' + str(sum(r.scores[res])/len(r.scores[res])))
                    else:
                        return format_html('<a href="{}"><span style="color: #cc0033; font-weight: bold;">{}</span></a>', url, self.culturalProficiency)
            else:
                return format_html('<a href="{}"><span style="color: #000; font-weight: bold;">{}</span></a>', url, self.culturalProficiency)
        else:
            return format_html('<span style="color: #000;">{0}</span>', self.culturalProficiency)

    cultural_Proficiency.allow_tags = True

    class Meta:
        verbose_name_plural = "Responses"
        ordering = ['created']

class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    totalScore = models.FloatField(blank=True, null=True, default=0)
    duration  = models.FloatField(blank=True, null=True, default=0)
    comments = models.CharField(max_length=1000, blank=True, null=True, default='')
    # email = models.CharField(max_length=1000, blank=True, null=True, default='')
    email_status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Scores"
    def email_send(self):
        print(self.user.id)
        url = 'http://cpcdp.tedoratech.com/api/email/?user_id=' + str(self.user.id)
        # return format_html('<form action="{}" method="post"><input type="submit" value="Send Email To User"></form>', url)
        # if self.email_status == b'\x00':
        if self.email_status ==False:
            return format_html("""<button onclick='location.href="{}"' type="button">Send Email To User</button>""", url)
            # return format_html('<a href="{}"><span style="color: #FFFFFF; background-color:#008000;">Send Email To User</span></a></a>', url)
        else:
            return format_html('<a href="{}"><span style="color: #FFFFFF; background-color:#cc0033;">Sent</span></a></a>', url)

class PreSurveyQuestions(models.Model):
    question1 = models.CharField(max_length=500, blank=True, null=True, default='')
    question2 = models.CharField(max_length=500, blank=True, null=True, default='')
    question3 = models.CharField(max_length=500, blank=True, null=True, default='')
    question4 = models.CharField(max_length=500, blank=True, null=True, default='')
    question5 = models.CharField(max_length=500, blank=True, null=True, default='')
    question6 = models.CharField(max_length=500, blank=True, null=True, default='')
    question7 = models.CharField(max_length=500, blank=True, null=True, default='')
    question8 = models.CharField(max_length=500, blank=True, null=True, default='')
    question9 = models.CharField(max_length=500, blank=True, null=True, default='')
    question10 = models.CharField(max_length=500, blank=True, null=True, default='')
    question11 = models.CharField(max_length=500, blank=True, null=True, default='')
    question12 = models.CharField(max_length=500, blank=True, null=True, default='')
    question13 = models.CharField(max_length=500, blank=True, null=True, default='')
    question14 = models.CharField(max_length=500, blank=True, null=True, default='')
    question15 = models.CharField(max_length=500, blank=True, null=True, default='')
    question16 = models.CharField(max_length=500, blank=True, null=True, default='')
    question17 = models.CharField(max_length=500, blank=True, null=True, default='')
    question18 = models.CharField(max_length=500, blank=True, null=True, default='')
    question19 = models.CharField(max_length=500, blank=True, null=True, default='')
    question20 = models.CharField(max_length=500, blank=True, null=True, default='')
    question21 = models.CharField(max_length=500, blank=True, null=True, default='')
    class Meta:
        verbose_name_plural = "Pre Survey Questions"

class PostSurveyQuestions(models.Model):
    question1 = models.CharField(max_length=500, blank=True, null=True, default='')
    question2 = models.CharField(max_length=500, blank=True, null=True, default='')
    question3 = models.CharField(max_length=500, blank=True, null=True, default='')
    question4 = models.CharField(max_length=500, blank=True, null=True, default='')
    question5 = models.CharField(max_length=500, blank=True, null=True, default='')
    question6 = models.CharField(max_length=500, blank=True, null=True, default='')
    question7 = models.CharField(max_length=500, blank=True, null=True, default='')
    question8 = models.CharField(max_length=500, blank=True, null=True, default='')
    question9 = models.CharField(max_length=500, blank=True, null=True, default='')
    question10 = models.CharField(max_length=500, blank=True, null=True, default='')
    class Meta:
        verbose_name_plural = "Post Survey Questions"

class PreSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    q1 = models.CharField(max_length=500)
    q2 = models.CharField(max_length=500)
    q3 = models.CharField(max_length=500)
    q4 = models.CharField(max_length=500)
    q5 = models.CharField(max_length=500)
    q6 = models.CharField(max_length=500)
    q7 = models.JSONField(default=list)
    q8 = models.CharField(max_length=500)
    q9 = models.CharField(max_length=500)
    q10 = models.CharField(max_length=500)
    q11 = models.CharField(max_length=500)
    q12 = models.CharField(max_length=500)
    q13 = models.CharField(max_length=500)
    q14 = models.CharField(max_length=500)
    q15 = models.CharField(max_length=500)
    q16 = models.CharField(max_length=500)
    q17 = models.CharField(max_length=500)
    q18 = models.CharField(max_length=500)
    q19 = models.CharField(max_length=500)
    q20 = models.CharField(max_length=500, blank=True, null=True, default='')
    q21 = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)
    duration  = models.FloatField(blank=True, null=True, default=0)
    class Meta:
        verbose_name_plural = "PreSurvey"
class PostSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    q1 = models.CharField(max_length=500)
    q2 = models.CharField(max_length=500)
    q3 = models.CharField(max_length=500)
    q4 = models.CharField(max_length=500)
    q5 = models.CharField(max_length=500)
    q6 = models.CharField(max_length=500)
    q7 = models.CharField(max_length=500)
    q8 = models.CharField(max_length=500, blank=True, null=True, default='')
    q9 = models.JSONField(default=list)
    q10 = models.CharField(max_length=500, blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "PostSurvey"

class FinalFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    q1 = models.CharField(max_length=500)
    q2 = models.CharField(max_length=500)
    q3 = models.CharField(max_length=500)
    q4 = models.CharField(max_length=500)
    q5 = models.CharField(max_length=500)
    q6 = models.CharField(max_length=500)
    q7 = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "FinalFeedback"

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    photo_profile = models.CharField(max_length=1000, blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=50, blank=True, null=True, default='')
    presurveystatus = models.BooleanField(default=False)
    responsesstatus = models.BooleanField(default=False)
    cpcqstatus = models.BooleanField(default=False)
    finalfeedbackstatus = models.BooleanField(default=False)
    scoresstatus = models.BooleanField(default=False)
    postsurveystatus = models.BooleanField(default=False)

# class UsersLog(models.Model):
#     username = models.CharField(max_length = 100)
#     password = models.CharField(max_length = 100)
#     email = models.CharField(max_length = 100)
#     created = models.DateTimeField(auto_now_add=True)





# class Inquiry(models.Model):
#     username = models.CharField(max_length = 100)
#     q1 = models.CharField(max_length=500)
#     q2 = models.CharField(max_length=500)
#     q3 = models.CharField(max_length=500)
#     q4 = models.CharField(max_length=500)
#     q5 = models.CharField(max_length=500)
#     q6 = models.CharField(max_length=500)