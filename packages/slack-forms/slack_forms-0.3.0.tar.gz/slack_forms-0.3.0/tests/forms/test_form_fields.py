#!/usr/bin/env python

"""Tests for `slack_forms` package."""

import pytest  # type: ignore
from typing import Dict, Type
from slack_forms import forms


@pytest.fixture
def fields() -> Dict[str, forms.Field]:
    return {
        'button': forms.ButtonField('My Button'),
        'text': forms.TextField('My Text'),
        'checkbox': forms.CheckboxField('My Checkbox', ['check 1', 'check 2']),
        'radio_button': forms.RadioButtonField('My RadioButton', ['radio 1', 'radio 2']),
        'multi_select': forms.MultiSelectField('My MultiSelect', ['multi 1', 'multi 2']),
    }


@pytest.fixture
def test_form_class(fields) -> Type[forms.Form]:
    class TestForm(forms.Form):

        button = fields['button']
        text = fields['text']
        checkbox = fields['checkbox']
        radio_button = fields['radio_button']
        multi_select = fields['multi_select']
    return TestForm


@pytest.fixture
def test_form(test_form_class) -> forms.Form:
    return test_form_class()


def test_declared_fields(fields, test_form):
    assert test_form.declared_fields == fields
