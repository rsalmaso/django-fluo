from django.core.exceptions import ValidationError
from django.db.models import enums

__all__ = ["Choices", "ChoicesMeta", "IntChoices", "StrChoices", "StrChoicesMeta"]


class ChoicesMeta(enums.ChoicesMeta):
    def __new__(metacls, classname, bases, classdict):
        # allow implicit value declaration
        new_values = {}
        for name in classdict._member_names:
            value = classdict[name]
            if not isinstance(value, (tuple, list)):
                new_values[name] = (name, value)
        classdict.update(new_values)
        return super().__new__(metacls, classname, bases, classdict)

    @property
    def display_names(cls):
        empty = [{"value": None, "display_name": cls.__empty__}] if hasattr(cls, "__empty__") else []
        return empty + [member.display_name for member in cls]

    @property
    def as_dict(cls):
        return dict(cls.choices)

    # Django-filter checks if choice is a callable to get the choices
    def __call__(cls, *args, **kwargs):
        # If called without arguments (it has no meaning for standard Enum, so we can add meaning):
        if not args and not kwargs:
            return cls.choices
        return super().__call__(*args, **kwargs)


class Choices(enums.Choices, metaclass=ChoicesMeta):
    """Class for creating enumerated choices."""

    @property
    def choice(self):
        return (self.value, self.label)

    @property
    def as_dict(self):
        return {self.value: self.label}

    @property
    def display_name(self):
        return {"value": self.value, "display_name": self.label}

    @classmethod
    def validate(cls, value):
        try:
            cls(value)
        except ValueError as exc:
            raise ValidationError(f"Invalid choice: {cls.__name__}.{value}") from exc


class IntChoices(int, Choices):
    """Integer based choices."""

    pass


class StrChoicesMeta(ChoicesMeta):
    @property
    def max_length(cls):
        return max([len(value) for value in cls.values])


class StrChoices(str, Choices, metaclass=StrChoicesMeta):
    """String based choices."""

    pass
