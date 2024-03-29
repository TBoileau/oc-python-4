"""Imported modules/packages"""
from abc import ABC
from typing import Callable, Dict, Any, List

from lib.form.form import Form
from lib.input.input import Input
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.representation.header import Header
from lib.representation.representation import Representation
from lib.representation.representation_factory_interface import RepresentationFactoryInterface
from lib.router.router import RouterInterface
from lib.templating.templating import TemplatingInterface
from lib.workflow.workflow_interface import WorkflowInterface


class AbstractController(ABC):
    """
    Abstract controller
    """

    def __init__(
        self,
        templating: TemplatingInterface,
        router: RouterInterface,
        entity_manager: EntityManagerInterface,
        representation_factory: RepresentationFactoryInterface,
        workflow: WorkflowInterface,
    ):
        self.__templating: TemplatingInterface = templating
        self.__router: RouterInterface = router
        self._entity_manager: EntityManagerInterface = entity_manager
        self._representation_factory: RepresentationFactoryInterface = representation_factory
        self._workflow: WorkflowInterface = workflow

    def _list(
            self,
            headers: List[Header],
            data: List[Any],
            callback: Callable,
            backward: str,
            route: str=None,
            route_params: Callable=None,
            backward_params: List[Any]=None,
    ):
        representation: Representation = self._representation_factory.create(callback)
        for header in headers:
            representation.add_header(header)
        representation.set_data(data)

        representation.render()

        input_: Input = Input(
            label="Saisissez un identifier ou R pour retour : ",
            message="Veuillez un identifiant parmi la liste ou R.",
            validate=lambda str: str in ['R'] + ([] if route is None else representation.identifiers)
        )

        def redirect_to(identifier: str) -> Callable:
            return lambda: self.redirect(route, route_params(identifier))

        self._choice(
            input_,
            {
                **{'R': lambda: self.redirect(backward, [] if backward_params is None else backward_params)},
                **({} if route is None else dict(
                    zip(
                        representation.identifiers,
                        map(redirect_to, representation.identifiers)
                    )
                )),
            },
        )



    def render(self, view: str, data=None):
        """
        Render view

        :param input_:
        :param choices:
        :param view:
        :param data:
        :return:
        """
        print(self.__templating.render(view, data))

    def redirect(self, name: str, params: List[Any] = None):
        """
        Redirect to route

        :param name:
        :param params:
        :return:
        """
        if params is None:
            params = []
        print(
            """
_______________________________________________________________________________
        """
        )
        self.__router.generate(name, params)

    def _choice(self, input_: Input, choices: Dict[Any, Callable], view: str = None, data=None):
        """
        Render choice

        :param input_:
        :param choices:
        :param view:
        :param data:
        """
        if view is not None:
            if data is None:
                data = {}
            print(self.__templating.render(view, data))
        choices[input_.capture()]()

    def _form(self, form: Form, view: str, data=None) -> Any:
        """
        Render form

        :param form:
        :param view:
        :param data:
        :return:
        """
        print(self.__templating.render(view, data))
        form.handle()
