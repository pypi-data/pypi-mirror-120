# Portions of this file are
#
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
#

from typing import List, Dict, Any, Optional, cast
from .exceptions import BindError
from .fields import Field


class DeclarativeFieldsMetaclass(type):
    """Collect Fields declared on the base classes."""
    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class and remove them from attrs.
        attrs['declared_fields'] = {
            key: attrs.pop(key) for key, value in list(attrs.items())
            if isinstance(value, Field)
        }

        new_class = super().__new__(mcs, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class


class BaseForm:

    base_fields: Dict[str, Field] = {}
    declared_fields: Dict[str, Field] = {}

    def __init__(self, *, initial: Dict[str, Any] = {}, state: Optional[Dict[str, str]] = None):
        self.initial = initial
        self.is_bound = state is not None
        self.state_values = state.get('values') if state is not None else None
        self._bound_fields_cache: Dict[str, Field] = {}
        for field_name, field in self.declared_fields.items():
            field.bind_name(field_name)

    def __getitem__(self, field_name):
        """ Bind a field's value from state """

        if not self.is_bound:
            raise BindError(f"{self.__class__.__name__} is not bound to state")
        try:
            return self._bound_fields_cache[field_name]
        except KeyError:
            pass
        try:
            field = self.declared_fields[field_name]
        except KeyError:
            raise KeyError(
                "Key '%s' not found in '%s'. Choices are: %s." % (
                    field_name,
                    self.__class__.__name__,
                    ', '.join(sorted(self.declared_fields)),
                )
            )
        bound_field = field.bind_field(self.state_values)
        self._bound_fields_cache[field_name] = bound_field
        return bound_field

    @property
    def data(self) -> Dict[str, Any]:
        return {field_name: self[field_name].value for field_name in self.declared_fields}

    def render(self, initial: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        #  See the convo at https://github.com/python/mypy/issues/9430 re: .get(cast(...))
        return [field.render(self.initial.get(cast(str, field.field_name))) for field in self.declared_fields.values()]


class Form(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    "A collection of Fields, plus their associated data."
