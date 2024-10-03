from django.db import models
import uuid
from users.models import CustomUser,AppUsers
from django.core.exceptions import ValidationError

class Audience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(AppUsers, related_name="users")
    app = models.ForeignKey("company.App", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Project(models.Model):
    PROJECT_STATUS = (
        ('DFT', 'Draft'),
        ('UAP', 'Under Approval'),
        ('AP', 'Approved'),
        ('RUN', 'Running'),
        ('PAU', 'Paused'),
        ('CMT', 'Complete'),
    )
    
    PROJECT_TYPE = (
        ("QUZ", 'Quiz'),
        ('SRV', 'Survey'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    
    link = models.URLField(max_length=200)
    status = models.CharField(choices=PROJECT_STATUS, max_length=3)
    projectType = models.CharField(choices=PROJECT_TYPE, max_length=3)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='projects')
    
    app = models.ForeignKey('company.App',models.CASCADE,'projects')
    
    orderQuestion = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Questions(models.Model):
    QUESTION_TYPES = (
        ('SC', 'Single Choice'),
        ('MC', 'Multiple Choice'),
        ('NOPE', 'Numeric Open Ended'),
        ('OPE', 'Open Ended'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='questions', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=50,  choices=QUESTION_TYPES)
    orderMultiple = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.id}: {self.question_text}"
    
    def get_total_count(self):
        """
        Calculate the total count of all choices for this question.
        """
        return self.choices.aggregate(total=models.Sum('count'))['total'] or 0


class MultipleChoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='choices')
    choiceText = models.CharField(max_length=255)
    image = models.ImageField(upload_to='multiple', blank=True, null=True)
    is_correct = models.BooleanField(default=False) 
    count = models.IntegerField()

    def __str__(self):
        return self.choiceText
    
    
    def clean(self):
        if not self.choiceText and not self.image:
            raise ValidationError('At least one of "choiceText" or "image" must be provided.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(AppUsers, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    selected_choice = models.ForeignKey(MultipleChoice, on_delete=models.SET_NULL, blank=True, null=True)
    response = models.CharField(max_length=255, blank=True, null=True)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='answers', null=True)  # New field

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"Answer by {self.user.name} for {self.question.question_text}"

    @property
    def is_correct(self):
        if self.selected_choice and self.question.project.projectType == 'QUZ':
            return self.selected_choice.is_correct
        return None
