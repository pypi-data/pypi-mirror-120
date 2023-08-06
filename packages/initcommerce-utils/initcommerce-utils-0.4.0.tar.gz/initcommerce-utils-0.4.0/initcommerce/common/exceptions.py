from graphql import GraphQLError

import abc


class InitCommerceBaseException(GraphQLError, metaclass=abc.ABCMeta):
    path = ""
    locations = ""
    original_error = None

    def __init__(self):  # avoid errors for non-initializing positional arg
        pass

    @property
    @abc.abstractmethod
    def code(self):
        pass

    @property
    def extensions(self):
        return dict(
            code=self.code,
        )
