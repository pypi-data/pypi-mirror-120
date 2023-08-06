import abc
from typing import Dict, Optional

from django.db import models

import stringcase
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_graphene_crud_generator.crud_generator.contexts import BuildContext, RuntimeContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType


class CreateMutationReturnAddedValueMixIn:
    """
    When calling the create operation, we will return the generated mutation
    """

    def _get_mutation_success_return_name(self, context: BuildContext) -> str:
        return stringcase.camelcase(context.django_type.__name__)

    def _get_mutation_success_ok_name(self, context: BuildContext) -> str:
        return "ok"

    def get_ok_flag_name(self, runtime_context: RuntimeContext):
        return list(
            filter(lambda x: self._get_mutation_success_ok_name(runtime_context.build_context).lower() in x.lower(),
                   runtime_context.build_context.create_return_value.keys()))[0]

    def get_return_flag_name(self, runtime_context: RuntimeContext):
        return list(
            filter(lambda x: self._get_mutation_success_return_name(runtime_context.build_context).lower() in x.lower(),
                   runtime_context.build_context.create_return_value.keys()))[0]

    def _create_mutation_return_value(self, context: BuildContext) -> Dict[str, TGrapheneReturnType]:
        result = dict()
        flag_name = self._get_mutation_success_ok_name(context)
        return_name = self._get_mutation_success_return_name(context)
        result[flag_name] = GraphQLHelper.return_ok()
        result[return_name] = GraphQLHelper.return_nullable(context.graphene_type)
        return result

    def _create_generate_mutation_instance_row_already_exists(self, mutation_class: type, item_in_db: Optional[models.Model],
                                                              runtime_context: RuntimeContext) -> any:
        flag_name = self.get_return_flag_name(runtime_context)
        ok_name = self.get_ok_flag_name(runtime_context)
        return mutation_class(**{flag_name: item_in_db, ok_name: False})

    def _create_generate_mutation_instance_row_added(self, mutation_class: type, result: any,
                                                     runtime_context: RuntimeContext) -> any:
        flag_name = self.get_return_flag_name(runtime_context)
        ok_name = self.get_ok_flag_name(runtime_context)
        return mutation_class(**{flag_name: result, ok_name: True})
