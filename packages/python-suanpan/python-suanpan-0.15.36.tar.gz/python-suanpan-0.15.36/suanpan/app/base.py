# coding=utf-8
from __future__ import absolute_import, print_function

from unittest import mock

from suanpan import error
from suanpan.log import logger
from suanpan.objects import HasName
from suanpan.app import MessageHandler


class BaseApp(HasName):
    def __init__(self):
        self._handlerClass = None

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented!")

    def start(self, *args, **kwargs):  # pylint: disable=unused-argument
        logger.info(f"Suanpan component {self.name} start...")
        if self._handlerClass:
            try:
                handler = self._handlerClass()
                for arg in handler.inputs:
                    self.input(arg)
                for arg in handler.outputs:
                    self.output(arg)
                for arg in handler.params:
                    self.param(arg)

                handler.init_params(*args, **kwargs)
                self.beforeInit(handler.beforeInit)
                self.afterInit(handler.afterInit)
                self.beforeCall(handler.beforeCall)
                self.afterCall(handler.afterCall)

                self(handler.run)
                handler.initialize()
            except Exception as e:
                raise error.AppError(f"handler class {self._handlerClass} init failed: {e}")

    def use(self, handlerClass):
        if not issubclass(handlerClass, MessageHandler):
            raise error.AppError(f"can't use {handlerClass}")
        self._handlerClass = handlerClass

    @property
    def trigger(self):
        raise NotImplementedError(f"{self.name} not support trigger")

    def input(self, argument):
        raise NotImplementedError("Method not implemented!")

    def output(self, argument):
        raise NotImplementedError("Method not implemented!")

    def param(self, argument):
        raise NotImplementedError("Method not implemented!")

    def column(self, argument):
        raise NotImplementedError("Method not implemented!")

    def beforeInit(self, hook):
        raise NotImplementedError("Method not implemented!")

    def afterInit(self, hook):
        raise NotImplementedError("Method not implemented!")

    def beforeCall(self, hook):
        raise NotImplementedError("Method not implemented!")

    def afterCall(self, hook):
        raise NotImplementedError("Method not implemented!")

    def beforeExit(self, hook):
        raise NotImplementedError("Method not implemented!")

    def load(self, *args, **kwargs):
        raise NotImplementedError(f"{self.name} not support load")

    def save(self, *args, **kwargs):
        raise NotImplementedError(f"{self.name} not support save")

    def send(self, *args, **kwargs):
        raise NotImplementedError(f"{self.name} not support send")

    @property
    def args(self):
        raise NotImplementedError(f"{self.name} not support args")

    @property
    def vars(self):
        raise NotImplementedError(f"{self.name} not support args")

    def title(self, title):  # pylint: disable=unused-argument
        return self

    @property
    def modules(self):
        return mock.MagicMock()
