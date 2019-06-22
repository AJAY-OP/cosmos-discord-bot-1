from .actions import AutoModerationActions


class AutoModerationTrigger(object):

    def __init__(self, _document):
        self._document = _document
        self.__actions = AutoModerationActions()
        self.name = self._document["name"]
        self.actions = [getattr(self.__actions, _) for _ in self._document["actions"]]

    def __getattr__(self, item):
        try:
            return self._document[item]
        except KeyError:
            raise AttributeError

    async def dispatch(self, member):
        for action in self.actions:
            await action(member)


_base = AutoModerationTrigger