from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models as django_models
from django.db.models.query_utils import DeferredAttribute


class RedisQuerySet(django_models.query.QuerySet):

    def update(self, **kwargs):
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        update_result = super().update(**kwargs)
        concrete_model = self.model
        id = concrete_model.id
        django_ids_to_update = [int(django_instance.id) for django_instance in self]
        data_to_update = redis_root.get(self.model, django_id__in=django_ids_to_update)
        redis_root.update(self.model, data_to_update, **kwargs)
        redis_root.set_pause(False)
        return self

    def create(self, **kwargs):
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        create_result = super().create(**kwargs)
        concrete_model = self.model._meta.concrete_model
        create_result = create_result
        id = create_result.id
        existing_fields = {}
        for field in create_result.__class__._meta.get_fields():
            try:
                field_name = field.name
                if field_name in ['id', 'pk']:
                    field_name = 'django_id'
                value = django_instance_field_to_redis_value(
                    redis_root,
                    create_result,
                    field,
                    redis_root.get_cache_conf(self.__class__)
                )
                if issubclass(value.__class__, django_models.Model):
                    field_name = field_name + '_id'
                    value = value.id
                existing_fields[field_name] = value
            except:
                pass
        existing_redis_instances = redis_root.get(self.model, create_result.id)
        if existing_redis_instances:
            redis_root.update(self.model, existing_redis_instances, **existing_fields)
        else:
            redis_root.create(self.model, **existing_fields)
        redis_root.set_pause(False)
        return create_result

    def delete(self):
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        list_self = list(self).copy()
        concrete_model = self.model._meta.concrete_model
        delete_result = super().delete()
        django_instance_ids_to_delete = [int(django_instance.id) for django_instance in list_self]
        print(django_instance_ids_to_delete)
        data_to_delete = redis_root.get(self.model, django_id__in=django_instance_ids_to_delete)
        print('data to delete: ', len(data_to_delete))
        redis_root.delete(self.model, data_to_delete)
        data_to_delete = redis_root.get(self.model, django_id__in=django_instance_ids_to_delete)
        print('after delete: ', len(data_to_delete))
        redis_root.set_pause(False)
        return list_self

class RedisUserObjectsManager(UserManager):
    def get_queryset(self):
        return RedisQuerySet(self.model)


class RedisObjectsManager(django_models.Manager):
    def get_queryset(self):
        return RedisQuerySet(self.model)


def get_redis_root():
    redis_root = getattr(settings, 'REDIS_ROOT', None)
    return redis_root


def django_instance_field_to_redis_value(
        redis_root,
        django_instance,
        django_field,
        cache_conf,
):

    save_related_models = cache_conf['save_related_models']
    django_field_value = getattr(django_instance, django_field.name)
    redis_value = django_field_value
    if isinstance(django_field_value, DeferredAttribute):
        django_field_value = django_field_value.__get__()
    if django_field.__class__ == django_models.ForeignKey:
        if django_field_value is None:
            redis_value = None
        else:
            django_foreign_key_instance = django_field_value
            if save_related_models:
                if django_foreign_key_instance:
                    django_instance_model = django_foreign_key_instance.__class__
                    redis_foreign_key_instance = get_or_create_redis_instance_from_django_instance(
                        redis_root,
                        django_foreign_key_instance,
                        cache_conf,
                    )
                    redis_value = redis_foreign_key_instance
                else:
                    redis_value = None
            else:
                redis_value = django_foreign_key_instance.id
    elif django_field.__class__ == django_models.ManyToManyField:
        django_many_to_many_instances = django_field_value.all()
        if save_related_models:
            if len(django_many_to_many_instances):
                django_instance_model = django_many_to_many_instances[0].__class__
                redis_value = [
                    get_or_create_redis_instance_from_django_instance(
                        redis_root,
                        django_many_to_many_instance,
                        cache_conf,
                    )
                    for django_many_to_many_instance in django_many_to_many_instances
                ]
            else:
                redis_value = []
        else:
            redis_value = [
                django_many_to_many_instance.id
                for django_many_to_many_instance in django_many_to_many_instances
            ]
    elif django_field.__class__.__name__.startswith('Image') or django_field.__class__.__name__.startswith('File'):
        try:
            redis_value = django_field_value.file.path
        except:
            redis_value = None
    return redis_value


def get_or_create_redis_instance_from_django_instance(
            redis_root,
            django_instance,
            cache_conf,
    ):
        django_fields = django_instance.__class__._meta.get_fields()
        django_instance_model = django_instance.__class__
        redis_root.wait_pause()
        redis_root.set_pause(True)
        redis_instance = redis_root.get(django_instance_model, django_id=django_instance.id)

        if not redis_instance:
            redis_dict = django_instance_to_redis_params(
                redis_root,
                django_instance,
                django_fields,
                cache_conf,
            )
            redis_instance = redis_root.create(
                django_model=django_instance_model,
                django_id=django_instance.id,
                **redis_dict
            )
        else:
            redis_instance = redis_instance[0]
        redis_root.set_pause(False)

        return redis_instance


def django_instance_to_redis_params(
        redis_root,
        django_instance,
        django_fields,
        cache_conf,
):
    redis_params = {}
    exclude_fields = cache_conf['exclude_fields']

    for i, django_field in enumerate(django_fields):
        if not django_field.__class__.__name__.endswith('Rel'):
            django_field_name = django_field.name
            allowed = True
            if exclude_fields:
                allowed = (django_field.name not in exclude_fields)
            if allowed:
                if django_field.name not in ['id', 'pk']:
                    redis_param = django_instance_field_to_redis_value(
                        redis_root,
                        django_instance,
                        django_field,
                        cache_conf,
                    )
                    if redis_param:
                        redis_params[django_field_name] = redis_param

    return redis_params


class DjangoRedisModel(django_models.Model):
    objects = RedisObjectsManager()

    def save(self, *args, **kwargs):
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        save_result = super().save(*args, **kwargs)
        existing_fields = {}
        for field in self.__class__._meta.get_fields():
            try:
                field_name = field.name
                if field_name in ['id', 'pk']:
                    field_name = 'django_id'
                existing_fields[field_name] = django_instance_field_to_redis_value(
                    redis_root,
                    self,
                    field,
                    redis_root.get_cache_conf(self.__class__)
                )
            except:
                pass
        redis_instance_qs = redis_root.get(self.__class__, django_id=self.id)
        if redis_instance_qs:
            redis_root.update(self.__class__, redis_instance_qs, **existing_fields)
        else:
            redis_root.create(self.__class__, redis_instance_qs, **existing_fields)
        redis_root.set_pause(False)
        return self

    def delete(self, *args, **kwargs):
        django_id = int(self.id)
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        delete_result = super().delete(*args, **kwargs)
        redis_root = get_redis_root()
        redis_instance_qs = redis_root.get(self.__class__, django_id=django_id)
        print('model pre delete: ', len(redis_instance_qs))
        if redis_instance_qs:
            print(self.__class__)
            redis_root.delete(self.__class__, redis_instance_qs)
            redis_instance_qs = redis_root.get(self.__class__, django_id=django_id)
            print('model post delete: ', len(redis_instance_qs))
        redis_root.set_pause(False)
        return self

    class Meta:
        abstract = True


class DjangoRedisUserModel(AbstractUser):
    objects = RedisUserObjectsManager()

    def save(self, *args, **kwargs):
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        save_result = super().save(*args, **kwargs)
        existing_fields = {}
        for field in self.__class__._meta.get_fields():
            try:
                field_name = field.name
                if field_name in ['id', 'pk']:
                    field_name = 'django_id'
                existing_fields[field_name] = django_instance_field_to_redis_value(
                    redis_root,
                    self,
                    field,
                    redis_root.get_cache_conf(self.__class__)
                )
            except:
                pass
        redis_instance_qs = redis_root.get(self.__class__, django_id=self.id)
        if redis_instance_qs:
            redis_root.update(self.__class__, redis_instance_qs, **existing_fields)
        else:
            redis_root.create(self.__class__, redis_instance_qs, **existing_fields)
        redis_root.set_pause(False)
        return self

    def delete(self, *args, **kwargs):
        django_id = int(self.id)
        redis_root = get_redis_root()
        redis_root.wait_pause()
        redis_root.set_pause(True)
        delete_result = super().delete(*args, **kwargs)
        redis_root = get_redis_root()
        redis_instance_qs = redis_root.get(self.__class__, django_id=django_id)
        print('model pre delete: ', len(redis_instance_qs))
        if redis_instance_qs:
            print(self.__class__)
            redis_root.delete(self.__class__, redis_instance_qs)
            redis_instance_qs = redis_root.get(self.__class__, django_id=django_id)
            print('model post delete: ', len(redis_instance_qs))
        redis_root.set_pause(False)
        return self

    class Meta:
        abstract = True
