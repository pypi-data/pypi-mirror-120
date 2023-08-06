from typing import Dict

from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument

from django_graphene_crud_generator.crud_generator.contexts import BuildContext


class CrudGraphQLViaTokenGenerateMixIn:
    """
    Every graphql endpoint has an additioanl token parameter, used for authentication.
    Require the developer to pass "token_name" to params, the name of the token
    """

    def _token_name(self, build_context: BuildContext) -> str:
        """
        name of the token required to authenticate
        """
        return build_context.params["token_name"]

    def _get_parameters_to_add_to_all_graphql(self, build_context: BuildContext) -> Dict[str, TGrapheneArgument]:
        result = dict()
        result[self._token_name(build_context)] = GraphQLHelper.argument_jwt_token()
        return result
