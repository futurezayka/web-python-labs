from typing import Generic, TypeVar

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def get_one(self, **kwargs) -> T | None:
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def exists(self, **kwargs) -> bool:
        return self.model.objects.filter(**kwargs).exists()

    def get_object_or_404(self, **kwargs) -> T:
        return get_object_or_404(self.model, **kwargs)

    def get_all(self) -> QuerySet[T]:
        return self.model.objects.all()

    def get_or_create(self, defaults: dict | None = None, **kwargs) -> tuple[T, bool]:
        return self.model.objects.get_or_create(defaults=defaults, **kwargs)

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def create_many(self, data_list: list[dict]) -> list[T]:
        instances = [self.model(**data) for data in data_list]
        return self.model.objects.bulk_create(instances)

    def update(self, values: dict, **kwargs) -> T:
        instance = self.get_one(**kwargs)
        if not instance:
            raise self.model.DoesNotExist(
                f"No {self.model.__name__} matches the given query."
            )
        for attr, value in values.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def update_or_create(
        self, defaults: dict | None = None, **kwargs
    ) -> tuple[T, bool]:
        return self.model.objects.update_or_create(defaults=defaults, **kwargs)

    def filter(self, **kwargs) -> QuerySet[T]:
        return self.model.objects.filter(**kwargs)

    def exclude(self, **kwargs) -> QuerySet[T]:
        return self.model.objects.exclude(**kwargs)

    def select_for_update(self) -> QuerySet[T]:
        return self.model.objects.select_for_update()

    def filter_one(self, **kwargs) -> T | None:
        return self.model.objects.filter(**kwargs).first()

    def delete(self, db_obj: T | None = None, **kwargs) -> bool:
        if db_obj:
            deleted_count, _ = db_obj.delete()
            return deleted_count > 0

        instances = self.filter(**kwargs)
        deleted_count, _ = instances.delete()
        return deleted_count > 0

    def select_related(self, *args) -> QuerySet[T]:
        return self.model.objects.select_related(*args)

    def prefetch_related(self, *args) -> QuerySet[T]:
        return self.model.objects.prefetch_related(*args)

    def bulk_create(self, objs: list[T]) -> list[T]:
        return self.model.objects.bulk_create(objs)

    def bulk_update(self, objs: list[T], fields: list[str] | None = None) -> None:
        return self.model.objects.bulk_update(objs, fields)

    def values_list(self, *fields, flat: bool = False, named: bool = False) -> QuerySet:
        return self.model.objects.values_list(*fields, flat=flat, named=named)

    def only(self, *args) -> QuerySet[T]:
        return self.model.objects.only(*args)

    def none(self):
        return self.model.objects.none()

    def count(self) -> int:
        return self.model.objects.count()

    def order_by(self, *fields) -> QuerySet[T]:
        """
        Orders the queryset by the given fields.
        Usage: repository.order_by("name") or repository.order_by("-created_at").
        """
        return self.model.objects.order_by(*fields)
