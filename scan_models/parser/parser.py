from django.db.models import ManyToManyField, ManyToManyRel, Field, ManyToOneRel


class GeneralParser:
    field: Field

    @property
    def is_many(self):
        return (
            isinstance(self.field, ManyToManyField)
            or isinstance(self.field, ManyToManyRel)
            or isinstance(self.field, ManyToOneRel)
        )
