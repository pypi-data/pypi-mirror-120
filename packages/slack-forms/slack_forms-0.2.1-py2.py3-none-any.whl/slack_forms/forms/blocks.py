from typing import List, Dict, Any, Callable, Union, Optional
from yarl import URL

true = True


class Block:

    make_block: Callable[..., Dict[str, Any]]
    value_from_state: Callable[..., Union[str, List[str]]]


class ButtonBlock(Block):

    def make_block(
        self,
        *,
        action_id: str,
        text: str,
        url: Optional[URL],
        value: Optional[str],
        style: Optional[str]
    ) -> Dict[str, Any]:
        block = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text
            },
            "action_id": action_id
        }
        if url:
            block['url'] = str(url)
        if value:
            block['value'] = value
        if style and style in ('default', 'primary', 'danger',):
            block['style'] = style
        return block

    def value_from_state(self, block_state: Dict[str, Any]) -> str:
        return block_state['value']


class PlainTextBlock(Block):

    def make_block(
        self,
        *,
        action_id: str,
        block_id: str,
        optional: bool,
        label: str,
        multiline: bool,
        bound_data: str,
        placeholder: Optional[str]
    ) -> Dict[str, Any]:
        block: Dict[str, Any] = {
            "type": "input",
            "optional": optional,
            "block_id": block_id,
            "element": {
                "type": "plain_text_input",
                "multiline": multiline,
                "action_id": action_id,
                "placeholder": {
                    "type": "plain_text",
                    "text": placeholder if placeholder is not None else "Enter text"
                }
            },
            "label": {
                "type": "plain_text",
                "text": label,
                "emoji": true
            }
        }
        if bound_data:
            block["element"]["initial_value"] = bound_data
        return block

    def value_from_state(self, block_state: Dict[str, Any]) -> str:
        return '' if block_state['value'] is None else block_state['value']


class CheckboxBlock(Block):

    def make_block(
        self,
        *,
        action_id: str,
        block_id: str,
        optional: bool,
        label: str,
        options: List[str],
        bound_data: List[str]
    ) -> Dict[str, Any]:
        block: Dict[str, Any] = {
            "type": "input",
            "optional": optional,
            "block_id": block_id,
            "element": {
                "type": "checkboxes",
                "options": [self._make_option(value, value) for value in options],
                "action_id": action_id
            },
            "label": {
                "type": "plain_text",
                "text": label,
                "emoji": true
            }
        }
        if bound_data:
            block["element"]["initial_options"] = [self._make_initial_options(value, value) for value in bound_data]

        return block

    def _make_option(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": true
            },
            "value": value
        }

    def _make_initial_options(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text
            },
            "value": value,
        }

    def value_from_state(self, block_state: Dict[str, Any]) -> List[str]:
        return [option['value'] for option in block_state['selected_options']]


class RadioButtonBlock(Block):

    def make_block(
        self,
        *,
        action_id: str,
        block_id: str,
        optional: bool,
        label: str,
        options:
        List[str],
        bound_data: List[str]
    ) -> Dict[str, Any]:
        block: Dict[str, Any] = {
            "type": "input",
            "optional": optional,
            "block_id": block_id,
            "element": {
                "type": "radio_buttons",
                "options": [self._make_option(value, value) for value in options],
                "action_id": action_id
            },
            "label": {
                "type": "plain_text",
                "text": label,
                "emoji": true
            }
        }
        if bound_data:
            block["element"]["initial_options"] = [self._make_initial_options(value, value) for value in bound_data]

        return block

    def _make_option(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": true
            },
            "value": value
        }

    def _make_initial_options(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text
            },
            "value": value,
        }

    def value_from_state(self, block_state: Dict[str, Any]) -> str:
        return block_state['selected_option']['value'] if block_state['selected_option'] is not None else None


class MultiSelectBlock(Block):

    def make_block(
        self,
        *,
        action_id: str,
        block_id: str,
        optional: bool,
        label: str,
        options: List[str],
        bound_data: List[str],
        placeholder: Optional[str]
    ) -> Dict[str, Any]:
        block: Dict[str, Any] = {
            "type": "input",
            "optional": optional,
            "block_id": block_id,
            "element": {
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": placeholder if placeholder is not None else "Select items",
                    "emoji": true
                },
                "options": [self._make_option(value, value) for value in options],
                "action_id": action_id
            },
            "label": {
                "type": "plain_text",
                "text": label,
                "emoji": true
            }
        }
        if bound_data:
            block["element"]["initial_options"] = [self._make_initial_options(value, value) for value in bound_data]

        return block

    def _make_option(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": true
            },
            "value": value
        }

    def _make_initial_options(self, value: str, text: str) -> Dict[str, Any]:
        return {
            "text": {
                "type": "plain_text",
                "text": text
            },
            "value": value,
        }

    def value_from_state(self, block_state: Dict[str, Any]) -> List[str]:
        return [option['value'] for option in block_state['selected_options']]
