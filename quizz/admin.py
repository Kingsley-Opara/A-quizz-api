from django.contrib import admin
from .models import Quiz, MCQ, MCQSubmission, CodingProblems, TestCaseForCodingProblem, CodingSubmission

# Register your models here.
admin.site.register(Quiz)
admin.site.register(MCQ)
admin.site.register(MCQSubmission)
admin.site.register(CodingProblems)
admin.site.register(CodingSubmission)
admin.site.register(TestCaseForCodingProblem)
# admin.site.register(MCQSubmission)
