#!/usr/bin/env python

"""Tests for `slack_forms` package."""

import pytest  # type: ignore


from slack_forms.forms.blocks import ButtonBlock


true = True
false = False


@pytest.fixture
def action_id():
    return "plain_text_input-button"


@pytest.fixture
def text():
    return "Click Me"


@pytest.fixture
def expected_value():
    return "click_me_123"


@pytest.fixture
def expected_block(action_id, text, expected_value):
    """
        Default input button from app.slack.com/block-kit-builder

        https://api.slack.com/reference/block-kit/block-elements#button
    """

    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text
        },
        "value": expected_value,
        "action_id": action_id
    }


@pytest.fixture
def block_state(expected_value):
    return {"value": expected_value}


def test_make_block(action_id, text, expected_value, expected_block):
    """ Validate ButtonBlock make_block """

    block = ButtonBlock().make_block(action_id=action_id, text=text, url=None, value=expected_value, style=None)
    assert block == expected_block


def test_value_from_state(expected_value, block_state):
    """ Validate ButtonBlock value_from_state """

    value = ButtonBlock().value_from_state(block_state)
    assert value == expected_value
