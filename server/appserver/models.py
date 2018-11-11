# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date

from django.db import models


class User(models.Model):
    last_active = models.DateField()
    password = models.CharField(db_column='pass', max_length=256)
    first_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    lang = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.first_name

    def get_children(self):
        user_children = UserChild.objects.filter(parent=self.id)
        child_ids = [user_child.child for user_child in user_children]
        return Child.objects.filter(pk__in=child_ids)

    def register_info(self):
        return {"parent_id": self.id, "name": self.first_name}

    def login_info(self):
        response = {"parent_id": self.id}
        children = self.get_children()
        children_info = [child.register_info() for child in children]
        response["children"] = children_info
        return response


class Child(models.Model):
    first_name = models.CharField(max_length=30)
    parent = models.IntegerField()
    #parent = models.ForeignKey(User, on_delete=models.CASCADE)
    last_active = models.DateField()
    birthday = models.DateField()
    sec_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'child'

    def __str__(self):
        return self.first_name

    def get_age(self):
        today = date.today()
        return (today.year - self.birthday.year)*12 + (today.month - self.birthday.month)

    def get_value_results(self, value):
        return Result.objects.filter(key_child=self.id, result_value=value)

    def get_results(self):
        return Result.objects.filter(key_child=self.id)

    def register_info(self):
        return {"child_id": self.id, "name": self.first_name}

    def get_parent(self):
        user_child = UserChild.objects.get(pk=self.id)
        return User.objects.get(pk=user_child.parent)





class UserChild(models.Model):
    parent = models.IntegerField()
    child = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_child'


class Exercise(models.Model):
    lang = models.CharField(max_length=3)
    ex = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercises'

    def __str__(self):
        response = "\nYou can try the following exercise: " + self.ex + \
                   "\nImage link: " + self.image_url + \
                   " , video link: " + self.video_url
        return response

    def get_milestone(self):
        milestonetest = MilestonesExercises.objects.get(exercise=self.id)
        return Milestone.objects.get(pk=milestonetest.milestone)


class Milestone(models.Model):
    target_age = models.IntegerField()
    lang = models.CharField(max_length=3)
    description = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'milestones'

    def __str__(self):
        return self.description

    def get_test(self):
        milestonetest = MilestonesTest.objects.get(milestone=self.id)
        if milestonetest.test is None:
            return None
        return Test.objects.get(pk=milestonetest.test)

    def get_exercise(self):
        milestonetest = MilestonesExercises.objects.get(milestone=self.id)
        return Exercise.objects.get(pk=milestonetest.exercise)


class Test(models.Model):
    lang = models.CharField(max_length=3)
    description = models.CharField(max_length=1000)
    follow_up_question = models.IntegerField(blank=True, null=True)
    back_question = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tests'

    def get_milestone(self):
        milestonetest = MilestonesTest.objects.get(test=self.id)
        return Milestone.objects.get(pk=milestonetest.milestone)


class MilestonesExercises(models.Model):
    milestone = models.IntegerField(blank=True, null=True)
    exercise = models.IntegerField(db_column='test', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'milestones_exercises'


class MilestonesTest(models.Model):
    milestone = models.IntegerField(blank=True, null=True)
    test = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'milestones_test'


class Result(models.Model):
    key_milestone = models.IntegerField()
    key_user = models.IntegerField()
    key_child = models.IntegerField()
    result_value = models.BooleanField()
    datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'results'

    def __str__(self):
        milestone = Milestone.objects.get(pk=self.key_milestone)
        if self.result_value:
            return "Your child can " + milestone.description
        else:
            return "Your child cannot " + milestone.description

    def get_milestone(self):
        return Milestone.objects.get(pk=self.key_milestone)
