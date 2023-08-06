from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.crud_generator.contexts import BuildContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument


class CrudGraphQLViaTokenGenerateMixIn:
    """
    Every graphql endpoint has an additioanl token parameter, used for authyentication
    """

    def _token_name(self, build_context: BuildContext) -> str:
        """
        name of the token required to authenticate
        """
        return "token"

    def _get_parameters_to_add_to_all_graphql(self, build_context: BuildContext) -> Dict[str, TGrapheneArgument]:
        result = dict()
        result[self._token_name(build_context)] = GraphQLHelper.argument_jwt_token()
        return result
