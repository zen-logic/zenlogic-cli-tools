from core.handlers.base import BaseHandler


class NotFoundHandler(BaseHandler):

    def run(self):
        BaseHandler.run(self)
        self.not_found()


handler = NotFoundHandler
