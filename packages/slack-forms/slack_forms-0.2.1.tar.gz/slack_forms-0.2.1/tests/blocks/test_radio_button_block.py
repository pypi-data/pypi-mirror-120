#!/usr/bin/env python

"""Tests for `slack_forms` package."""

import pytest  # type: ignore
from typing import List, Any
from slack_forms.forms.blocks import RadioButtonBlock


true = True
false = False


@pytest.fixture
def action_id() -> str:
    return "radio_buttons-action"


@pytest.fixture
def block_id() -> str:
    return "radio_buttons-block"


@pytest.fixture
def optional() -> bool:
    return True


@pytest.fixture
def label() -> str:
    return "Please select all restaurants you'd be willing to eat at:"


@pytest.fixture
def values() -> List[str]:
    return ["Gary Danko", "Chipotle", "Slack Cafe"]


@pytest.fixture
def initial_values(values) -> List[str]:
    return values[:1]


@pytest.fixture
def expected_block(action_id, block_id, optional, label, values, initial_values) -> Any:
    """
        Default input button from app.slack.com/block-kit-builder

        https://api.slack.com/reference/block-kit/block-elements#checkboxes
    """

    return {
        "type": "input",
        "block_id": block_id,
        "optional": optional,
        "element": {
            "type": "radio_buttons",
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": values[0],
                        "emoji": true
                    },
                    "value": values[0]
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": values[1],
                        "emoji": true
                    },
                    "value": values[1]
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": values[2],
                        "emoji": true
                    },
                    "value": values[2]
                }
            ],
            "initial_options": [
                {
                    'text': {
                        'type': 'plain_text',
                        'text': values[0]
                    },
                    'value': values[0]
                }
            ],
            "action_id": action_id
        },
        "label": {
            "type": "plain_text",
            "text": label,
            "emoji": true
        }
    }


@pytest.fixture
def block_state(initial_values) -> Any:
    return {"selected_option": {"value": initial_values[0]}}


def test_make_block(action_id, block_id, optional, label, values, initial_values, expected_block):
    """ Validate PlainTextBlock make_block """

    block = RadioButtonBlock().make_block(
        action_id=action_id,
        block_id=block_id,
        optional=optional,
        label=label,
        options=values,
        bound_data=initial_values
    )
    assert block == expected_block


def test_value_from_state(initial_values, block_state):
    """ Validate PlainTextBlock value_from_state """

    value = RadioButtonBlock().value_from_state(block_state)
    assert value == initial_values[0]
