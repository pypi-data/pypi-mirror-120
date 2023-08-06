from typing import Callable, List, Dict, Any, Union, Optional
from yarl import URL
from slugify import slugify
from .exceptions import BindError
from .blocks import Block, ButtonBlock, PlainTextBlock, CheckboxBlock, RadioButtonBlock, MultiSelectBlock


class Field:

    block: Block
    action_handler: Callable

    def __init__(self, *, action_id: Optional[str] = None, block_id: Optional[str] = None):
        self._action_id = action_id
        self._block_id = block_id
        self.field_name: Optional[str] = None
        self._value: Optional[Union[str, List[str]]] = None
        self.is_bound = False

    def bind_name(self, field_name: str):
        """ Associate the form level field name with this instance """
        self.field_name = field_name
        self.field_name_slug = slugify(field_name)

    @property
    def block_id(self) -> str:
        if self.field_name is None:
            raise BindError(f"{self.__class__.__name__} used outside a Form class")
        return self._block_id or self.field_name_slug

    @property
    def action_id(self) -> str:
        if self.field_name is None:
            raise BindError(f"{self.__class__.__name__} used outside a Form class")
        return self._action_id or (self.field_name_slug + '-action')

    def bind_field(self, state_values: Dict[str, Any]) -> 'Field':
        try:
            self._value = self.block.value_from_state(state_values[self.block_id][self.action_id])
        except KeyError:
            raise BindError(f"{self.__class__.__name__} cannot find state for "
                            f"block {self.block_id} action {self.action_id}")
        self.is_bound = True
        return self

    @property
    def value(self) -> Optional[Union[str, List[str]]]:
        if not self.is_bound:
            raise BindError(f"{self.__class__.__name__} value is not bound; did you create the form with state?")
        return self._value

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        raise NotImplementedError


class ButtonField(Field):

    block = ButtonBlock()

    def __init__(
        self,
        text: str,
        *,
        url: Optional[str] = None,
        interaction_payload_value: Optional[str] = None,
        style: Optional[str] = None,
        **kwargs
    ):
        self.text = text
        self.url = URL(url or '')
        self.interaction_payload_value = interaction_payload_value
        self.style = style
        super().__init__(**kwargs)

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        return self.block.make_block(action_id=self.action_id,
                                     text=self.text,
                                     url=self.url,
                                     value=self.interaction_payload_value,
                                     style=self.style)


class TextField(Field):

    block = PlainTextBlock()

    def __init__(
        self,
        label: str,
        *,
        multiline: bool = False,
        optional: bool = False,
        initial: str = '',
        placeholder: Optional[str] = None,
        **kwargs
    ):
        self.label = label
        self.multiline = multiline
        self.optional = optional
        self.initial = initial
        self.placeholder = placeholder
        super().__init__(**kwargs)

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        if initial is None:
            initial = self.initial
        return self.block.make_block(action_id=self.action_id,
                                     block_id=self.block_id,
                                     optional=self.optional,
                                     label=self.label,
                                     multiline=self.multiline,
                                     bound_data=initial,
                                     placeholder=self.placeholder)


class CheckboxField(Field):

    block = CheckboxBlock()

    def __init__(
        self,
        label: str,
        options: List[str],
        *,
        optional: bool = False,
        initial: List[str] = [],
        **kwargs
    ):
        self.label = label
        self.options = options
        self.optional = optional
        self.initial = initial
        super().__init__(**kwargs)

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        if initial is None:
            initial = self.initial
        return self.block.make_block(action_id=self.action_id,
                                     block_id=self.block_id,
                                     optional=self.optional,
                                     label=self.label,
                                     options=self.options,
                                     bound_data=initial)


class RadioButtonField(Field):

    block = RadioButtonBlock()

    def __init__(
        self,
        label: str,
        options: List[str],
        *,
        optional: bool = False,
        initial: List[str] = [],
        **kwargs
    ):
        self.label = label
        self.options = options
        self.optional = optional
        self.initial = initial
        super().__init__(**kwargs)

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        if initial is None:
            initial = self.initial
        return self.block.make_block(action_id=self.action_id,
                                     block_id=self.block_id,
                                     optional=self.optional,
                                     label=self.label,
                                     options=self.options,
                                     bound_data=initial)


class MultiSelectField(Field):

    block = MultiSelectBlock()

    def __init__(
        self,
        label: str,
        options: List[str],
        *,
        optional: bool = False,
        initial: List[str] = [],
        placeholder: Optional[str] = None,
        **kwargs
    ):
        self.label = label
        self.options = options
        self.optional = optional
        self.initial = initial
        self.placeholder = placeholder
        super().__init__(**kwargs)

    def render(self, initial: Optional[Any] = None) -> Dict[str, Any]:
        if initial is None:
            initial = self.initial
        return self.block.make_block(action_id=self.action_id,
                                     block_id=self.block_id,
                                     optional=self.optional,
                                     label=self.label,
                                     options=self.options,
                                     bound_data=initial,
                                     placeholder=self.placeholder)
