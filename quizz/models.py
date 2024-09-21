from typing import Any
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from multiselectfield import MultiSelectField
from django.utils import timezone 

# Create your models here.


User = settings.AUTH_USER_MODEL

def get_options(option_a, option_b, option_c, option_d):
    options_ = (
        (option_a, option_a),
        (option_b, option_b),
        (option_c, option_c),
        (option_d, option_d),
    )
    options = options_
    return options



class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = (
        ('MCQ', 'Multiple Choice Questions'),
        ('Coding Task', 'Coding Task'),
    )
    question_type = MultiSelectField(choices=type, max_choices = 1, max_length=1000)
    question = models.TextField()
    option_a = models.CharField(max_length=1000, null=True, blank=True)
    option_b = models.CharField(max_length=1000, null=True, blank=True)
    option_c = models.CharField(max_length=1000, null=True, blank=True)
    option_d = models.CharField(max_length=1000, null=True, blank=True)
    coding_task_description = models.TextField(null=True, blank=True)
    languages = (
        ('python', 'python'),
        ('javascript', 'javascript'),
        ('java', 'java'),
    )
    language = models.CharField(max_length=255, choices=languages, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

    def __str__(self):
        return self.question
    


class MCQ(models.Model):
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    option_a = models.CharField(max_length=1000, null=True, blank=True)
    option_b = models.CharField(max_length=1000, null=True, blank=True)
    option_c = models.CharField(max_length=1000, null=True, blank=True)
    option_d = models.CharField(max_length=1000, null=True, blank=True)
    options = (
        (option_a, option_a),
        (option_b, option_b),
        (option_c, option_c),
        (option_d, option_d),

    )
    created_at = models.DateField(auto_now_add=True)
    answer = models.CharField(max_length=1000, null=True, blank=True, choices=options)


    

    def __str__(self):
        return self.question.question
    


class MCQSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mcq = models.ForeignKey(MCQ, on_delete=models.DO_NOTHING)
    options = (
        
        ('Option A', 'Option A'),
        ('Option B', 'Option B'),
        ('Option C', 'Option C'),
        ('Option D', 'Option D'),

        
    )
    user_answer = models.CharField(max_length=350, choices=options, null=True, blank=True, help_text='answer')
    submitted_at = models.DateTimeField(auto_now=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Submission for {self.mcq.question}'


class CodingProblems(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=True, null=True)
    sample_input = models.TextField()
    sample_output = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    
class TestCaseForCodingProblem(models.Model):
    problem = models.ForeignKey(CodingProblems, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self) -> str:
        return super().__str__()

class CodingSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(CodingProblems, on_delete=models.CASCADE)
    submitted_code = models.TextField()
    result = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(auto_now=True) 


def save_obj(instance, save = True):
    if save:
        instance.save()
    return instance





def postsave_signal_Quiz(sender, instance, created, *args, **kwargs):
    if created:    
        type = list(instance.question_type)
        option_a = ''
        option_b = ''
        option_c = ''
        option_d = ''

        if 'MCQ' in type:
            if instance.option_a:
                option_a = instance.option_a
            if instance.option_b:
                option_b = instance.option_b
            if instance.option_c:
                option_c = instance.option_c
            if instance.option_d:
                option_d = instance.option_d
            options = get_options(option_a, option_b, option_c, option_d)
            MCQ._meta.get_field('answer').choices = options
            obj = MCQ.objects.create(question = instance, option_a= option_a, option_b = option_b, option_c = option_c, option_d = option_d)
            obj.save()   
        if 'Coding Task' in type:
            pass

       
   

  
def postsave_MCQ_Questions(sender, instance, created, *args, **kwargs):
    if created:
        option_a = instance.option_a
        option_b = instance.option_b
        option_c = instance.option_c
        option_d = instance.option_d
        options = get_options(option_a, option_b, option_c, option_d)
        MCQSubmission._meta.get_field('user_answer').choices = options
        obj = MCQSubmission.objects.create(mcq = instance)
        obj.save()
        

    if not created:
        print('good')
        print(instance.answer)

def postsave_MCQSubmission(sender, instance, *args, **kwargs):

    option_a = instance.mcq.option_a
    option_b = instance.mcq.option_b
    option_c = instance.mcq.option_c
    option_d = instance.mcq.option_d

    answer = instance.mcq.answer
    user_answer = instance.user_answer
    if answer and user_answer:
        if answer == user_answer:
            instance.is_correct = True
            options = get_options(option_a, option_b, option_c, option_d)
            instance._meta.get_field('user_answer').choices = options
            save_obj(instance, save=False)


pre_save.connect(postsave_MCQSubmission, sender=MCQSubmission)
post_save.connect(postsave_signal_Quiz, sender=Quiz)
post_save.connect(postsave_MCQ_Questions, sender=MCQ)

    

 




# def post_save_MCQ(sender, instance, created, *args, **kwargs):
#     option_a = instance.option_a
#     option_b = instance.option_b
#     option_c = instance.option_c
#     option_d = instance.option_d
#     if created:
#         obj = MCQSubmission.objects.create(mcq = instance)
#         obj.save()
#         if option_a is None:
#             instance.option_a = 'Option A'
#             # instance.save()
#             save_obj(instance, save=True)
#         if option_b is None:
#             instance.option_b = 'Option B'
#             save_obj(instance, save=True)
#         if option_c is None:
#             instance.option_c = 'Option c'
#             save_obj(instance, save=True)
#         if option_d is None:
#             instance.option_d = 'Option D'
#             save_obj(instance, save=True)
#     # save_obj(instance, save=True)

# post_save.connect(post_save_MCQ, sender=MCQ)



# def update_presaveoptions_forAnswer(sender, instance, created, *args, **kwargs):
#     option_a = instance.mcq.option_a
#     option_b = instance.mcq.option_b
#     option_c = instance.mcq.option_c
#     option_d = instance.mcq.option_d
#     if created:
#         instance.option_a = option_a
#         instance.option_b = option_b
#         instance.option_c = option_c
#         instance.option_d = option_d
#         save_obj(instance=instance, save=True)

#         if instance.mcq.answer == instance.picked_answer:
#             instance.picked_answer = True
#             save_obj(instance=instance, save=True)










