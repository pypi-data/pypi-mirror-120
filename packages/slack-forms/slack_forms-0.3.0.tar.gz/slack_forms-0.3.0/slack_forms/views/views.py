import re
import uuid
import inspect
from typing import Callable, Type, Dict, Any, Iterable, Tuple, Optional
from slack_bolt import App
from ..forms.forms import Form
from ..logging.logging import getLogger


logger = getLogger(__name__)
true = True


class View:

    form_class: Type[Form] = Form
    callback_id: Optional[str] = None

    def __init__(self, app: App, initial: Dict[str, Any] = {}):
        self.app = app
        self.initial = initial
        if self.callback_id is None:
            self.callback_id = str(uuid.uuid4())

    def handle_view(self, ack, body, client, view):
        ack()
        logger.info(f'{self.callback_id} submitted')
        form = self.get_form(state=view['state'])
        self.form_valid(form)

    def get_form(self, **kwargs) -> Form:
        # form must be created so fields are bound for handler setup
        form = self.form_class(**kwargs)
        self.setup_view_handler()
        self.setup_action_handlers(form)
        return form

    def setup_view_handler(self):
        self.app.view(self.callback_id)(self.handle_view)

    def setup_action_handlers(self, form: Form):
        for action_id, action in self._action_handlers(form):
            self.app.action(action_id)(action)

    def _action_attrs(self, form: Form) -> Iterable[Tuple[str, Callable]]:
        """ returns iterable of (field_name, action_method) for qualifying methods """
        rule = re.compile('(?P<field_name>.+)_action$')
        for field_name_match, action in map(lambda attr: (rule.match(attr), getattr(self, attr)), dir(self)):
            if (
                field_name_match is not None and
                field_name_match.groups()[0] in form.declared_fields and
                inspect.ismethod(action)
            ):
                yield field_name_match.groups()[0], action

    def _action_handlers(self, form) -> Iterable[Tuple[str, Callable]]:
        """ returns iterable of (action_id, action_method) for qualifying methods """
        return ((form.declared_fields[field_name].action_id, action)
                for field_name, action in self._action_attrs(form))

    def render(self) -> Dict[str, Any]:
        pass

    def form_valid(self, form: Form):
        logger.info(f"default action for {self.__class__.__name__}.{form.__class__.__name__}")


class HomeView(View):

    def render(self) -> Dict[str, Any]:
        form = self.get_form(initial=self.initial)
        blocks = form.render()
        view = {
            "type": "home",
            "blocks": [{
                "type": "actions",
                "elements": blocks
            }]
        }
        return view


class ModalView(View):

    title_text = 'Modal'
    submit_text = 'Submit'
    close_text = 'Cancel'

    def render(self) -> Dict[str, Any]:
        form = self.get_form(initial=self.initial)
        blocks = form.render()
        view = {
            "type": "modal",
            "callback_id": self.callback_id,
            "title": {
                "type": "plain_text",
                "text": self.title_text,
                "emoji": true
            },
            "submit": {
                "type": "plain_text",
                "text": self.submit_text,
                "emoji": true
            },
            "close": {
                "type": "plain_text",
                "text": self.close_text,
                "emoji": true
            },
            "blocks": blocks,
        }
        return view
