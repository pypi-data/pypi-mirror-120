from typing import Dict

import stringcase
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneType

from django_graphene_crud_generator.crud_generator.contexts import BuildContext


class FederationNamesMixIn:
    """
    If you are developing a federation, the names within the federation needs to be unique.
    This namer enforces it. We assume the user has passed a parameters called "subgraph_name"
    during the init of the crud graphql generator
    """

    def subgraph_name(self, build_context: BuildContext) -> str:
        return build_context.params["subgraph_name"]

    def _read_single_query_name(self, build_context: BuildContext) -> str:
        return f"{stringcase.camelcase(self.subgraph_name(build_context))}ReadSingle{stringcase.pascalcase(build_context.django_type.__name__)}Item"

    def _read_all_query_name(self, build_context: BuildContext) -> str:
        return f"{stringcase.camelcase(self.subgraph_name(build_context))}ReadAll{stringcase.pascalcase(build_context.django_type.__name__)}Items"

    def _create_mutation_class_name(self, build_context: BuildContext) -> str:
        return f"{stringcase.camelcase(self.subgraph_name(build_context))}Create{stringcase.pascalcase(build_context.django_type.__name__)}Item"

    def _patch_mutation_return_value(self, build_context: BuildContext, d: Dict[str, TGrapheneType]) -> Dict[str, TGrapheneType]:
        result = dict()
        for k, v in d.items():
            result[f"{stringcase.camelcase(self.subgraph_name(build_context))}{stringcase.pascalcase(k)}"] = v
        return result
