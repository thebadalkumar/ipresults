from django.db import models

class Batch(models.Model):
    batch = models.IntegerField()

    def __str__(self):
        return str(self.batch)
    
    class Meta:
        verbose_name_plural = 'Batches'

class Institute(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    short = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    short = models.CharField(max_length=100, null=True, blank=True)
    # institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def __str__(self):
        return self.name   

class Result(models.Model):
    
    class Meta:
        abstract = True

    institution = models.ForeignKey(Institute, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    semester = models.JSONField(blank=True, default=dict)

    enrollment = models.CharField(max_length=11, primary_key = True)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.enrollment +" "+ self.name

class BCA(Result):
    
    class Meta:
        verbose_name_plural = 'BCA'

class MCA(Result):
    
    class Meta:
        verbose_name_plural = 'MCA'

class rsFiles(models.Model):
    courses = [
        ('BCA ' , 'BCA'),
        ('MCA' , 'MCA')]
    course = models.CharField(max_length=10, choices=courses, default='BCA')
    # migrated = models.BooleanField(default=False)
    regular_reappear = [
        ('REGULAR ' , 'REGULAR'),
        ('REAPPEAR' , 'REAPPEAR')]
    examination = models.CharField(max_length=8, choices=regular_reappear, default='Regular')
    # batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='result_pdfs/')

    def __str__(self):
        return str(self.course)
    
    class Meta:
        verbose_name_plural = 'Files'