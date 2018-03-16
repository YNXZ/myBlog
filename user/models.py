from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    nickname = models.CharField(max_length=64, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.IntegerField()
    perm_id = models.IntegerField()

    def verify_password(self, password):
        return check_password(password, self.password)

    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()

    @property
    def perms(self):
        perm_id_list = UserPermission.objects.filter(uid=self.id).only('perm_id')
        return Permission.objects.filter(id__in=perm_id_list).only('name')

    def has_perm(self, perm_name):
        try:
            perm_id = Permission.objects.get(name=perm_name).id
        except Permission.DoesNotExist as e:
            print(e)
            return
        return Permission.objects.exists(uid = self.id, perm_id=perm_id)

    def add_perm(self, perm_name):
        '''增加权限'''
        try:
            perm_id = Permission.objects.get(name=perm_name).id
        except Permission.DoesNotExist as e:
            print(e)
            return
        role, _ = UserPermission.objects.get_or_create(perm_id=perm_id, uid=self.id)
        return role

    def del_perm(self, perm_name):
        '''取消权限'''
        try:
            perm_id = Permission.objects.get(name=perm_name).id
            UserPermission.objects.get(uid=self.id, perm_id=perm_id).delete()
        except (Permission.DoesNotExist, UserPermission.DoesNotExist) as e:
            print(e)


class Permission(models.Model):
    '''权限'''
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    perm = models.IntegerField(default=0)


class UserPermission(models.Model):
    uid = models.IntegerField()
    perm_id = models.IntegerField()