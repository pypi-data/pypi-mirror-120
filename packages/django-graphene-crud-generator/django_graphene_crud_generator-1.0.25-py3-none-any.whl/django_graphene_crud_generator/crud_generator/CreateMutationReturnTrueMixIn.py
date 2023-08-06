import abc
from typing import Dict

from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_graphene_crud_generator.crud_generator.contexts import BuildContext, RuntimeContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType


class CreateMutationReturnTrueMixIn:

    def _get_mutation_success_return_name(self, context: BuildContext) -> str:
        return "ok"

    def _create_mutation_return_value(self, context: BuildContext) -> Dict[str, TGrapheneReturnType]:
        result = dict()
        flag_name = self._get_mutation_success_return_name(context)
        result[flag_name] = GraphQLHelper.return_ok()
        return result

    def _create_generate_mutation_instance_row_already_exists(self, mutation_class: type,
                                                              runtime_context: RuntimeContext) -> any:
        flag_name = list(filter(lambda x: self._get_mutation_success_return_name(runtime_context.build_context) in x, runtime_context.build_context.create_return_value.values()))[0]
        return mutation_class(**{flag_name: False})

    def _create_generate_mutation_instance_row_added(self, mutation_class: type, result: any,
                                                     runtime_context: RuntimeContext) -> any:
        flag_name = list(filter(lambda x: self._get_mutation_success_return_name(runtime_context.build_context) in x, runtime_context.build_context.create_return_value.values()))[0]
        return mutation_class(**{flag_name: True})
