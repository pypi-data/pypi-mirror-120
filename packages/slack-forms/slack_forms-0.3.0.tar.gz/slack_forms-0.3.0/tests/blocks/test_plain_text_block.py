#!/usr/bin/env python

"""Tests for `slack_forms` package."""

import pytest  # type: ignore
from slack_forms.forms.blocks import PlainTextBlock


true = True
false = False


@pytest.fixture
def action_id():
    return "plain_text_input-action"


@pytest.fixture
def block_id():
    return "plain_text_input-block"


@pytest.fixture
def optional():
    return True


@pytest.fixture
def label():
    return "Label"


@pytest.fixture
def placeholder():
    return "Add text"


@pytest.fixture
def expected_value():
    return "Here is some text"


@pytest.fixture
def expected_block(action_id, block_id, optional, label, placeholder):
    """
        Default input button from app.slack.com/block-kit-builder

        https://api.slack.com/reference/block-kit/block-elements#input
    """

    return {
        "type": "input",
        "block_id": block_id,
        "optional": optional,
        "element": {
            "type": "plain_text_input",
            "multiline": true,
            "action_id": action_id,
            "placeholder": {
                "type": "plain_text",
                "text": placeholder
            }
        },
        "label": {
            "type": "plain_text",
            "text": label,
            "emoji": true
        }
    }


@pytest.fixture
def block_state(expected_value):
    return {"value": expected_value}


def test_make_block(action_id, block_id, optional, label, placeholder, expected_block):
    """ Validate PlainTextBlock make_block """

    block = PlainTextBlock().make_block(
        action_id=action_id,
        block_id=block_id,
        optional=optional,
        label=label,
        multiline=True,
        bound_data=None,
        placeholder=placeholder
    )
    assert block == expected_block


def test_value_from_state(expected_value, block_state):
    """ Validate PlainTextBlock value_from_state """

    value = PlainTextBlock().value_from_state(block_state)
    assert value == expected_value
