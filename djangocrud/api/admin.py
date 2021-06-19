import csv
from django.contrib import admin
from django.http.response import HttpResponse
from .models import Attitude
from .models import Empathy
from .models import Policy
from .models import Professionalism
from .models import Teaching
from .models import Responses
from .models import PreSurvey
from .models import PostSurvey
from .models import FinalFeedback
from .models import CPCQResponses, Scores, PostSurveyQuestions, PreSurveyQuestions
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.forms import TextInput


# from .models import Inquiry

class FlattenJsonWidget(TextInput):
    def render(self, name, value, attrs=None):
        if not value is None:
            parsed_val = ''
            for k, v in dict(value):
                parsed_val += " = ".join([k, v])
            value = parsed_val
        return super(FlattenJsonWidget, self).render(name, value, attrs)

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Excel"

class ResponseAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['username','topic','cultural_Destructiveness', 'cultural_Incapacity', 'cultural_Blindness', 'cultural_PreCompetence','cultural_Competence','cultural_Proficiency','description','duration']
    search_fields = ['username','topic']
    actions = ["export_as_csv"]
class PreSurveyAdmin(admin.ModelAdmin):
    list_display = ['username','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20','duration', 'consent']
    search_fields = ['username']

class PostSurveyAdmin(admin.ModelAdmin):
    list_display = ['username','q1','q2','q3','q4','q5','q6','q7','q8','q9','consent']
    search_fields = ['username']

class FinalFeedbackAdmin(admin.ModelAdmin):
    list_display = ['username','q1','q2','q3','q4','q5','q6','q7']
    search_fields = ['username']

class CPCQResponsesAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'culturalDestructivenessresponse','culturalIncapacityresponse','culturalBlindnessresponse','culturalPreCompetenceresponse','culturalCompetenceresponse','culturalProficiencyresponse','scores', 'comment1','comment2','duration']
    search_fields = ['user','topic']

class ScoresAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'totalScore', 'duration','email_send']
    search_fields = ['user','username']

class AttitudeAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6']

class EmpathyAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6']

class PolicyAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6']

class ProfessionalismAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6']

class TeachingAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6']

class PreSurveyQuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6','question7','question8','question9','question10','question11','question12','question13','question14','question15','question16','question17','question18','question19','question20', 'question21']

class PostSurveyQuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','question1','question2','question3','question4','question5','question6','question7','question8','question9', 'question10']

admin.site.register(Attitude, AttitudeAdmin)
admin.site.register(Empathy, EmpathyAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Professionalism, ProfessionalismAdmin)
admin.site.register(Teaching, TeachingAdmin)
admin.site.register(PreSurveyQuestions, PreSurveyQuestionsAdmin)
admin.site.register(PostSurveyQuestions, PostSurveyQuestionsAdmin)
admin.site.register(CPCQResponses, CPCQResponsesAdmin)
admin.site.register(Scores,ScoresAdmin)
# admin.site.register(UsersLog)

# admin.site.register(PreSurvey)
# admin.site.register(Inquiry)


admin.site.register(Responses,ResponseAdmin)
admin.site.register(PreSurvey,PreSurveyAdmin)
admin.site.register(PostSurvey,PostSurveyAdmin)
admin.site.register(FinalFeedback,FinalFeedbackAdmin)




