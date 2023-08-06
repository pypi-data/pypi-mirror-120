from typing import List, Dict

import stringcase

from django_koldar_utils.django_toolbox import django_helpers
from django_koldar_utils.graphql_toolsbox import error_codes
from django_koldar_utils.graphql_toolsbox.GraphQLAppError import GraphQLAppError
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.crud_generator.contexts import RuntimeContext, BuildContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TDjangoModelType, TGrapheneArgument


class CreateMutationViaSingleInputMixIn:

    def _get_fields_to_check(self, runtime_context: RuntimeContext) -> List[str]:
        return list(map(lambda x: x.name, django_helpers.get_unique_field_names(runtime_context.build_context.django_type)))

    def _create_mutation_input_parameter(self, build_context: BuildContext) -> str:
        """
        Name of the parameter in create mutation that defines the element to add
        """
        return stringcase.camelcase(build_context.django_type.__name__)

    def _create_mutation_parameters(self, build_context: BuildContext) -> Dict[str, TGrapheneArgument]:
        result = dict()
        param = self._create_mutation_parameters(build_context)
        result[param] = GraphQLHelper.argument_required_input(input_type=build_context.graphene_input_type)
        return result

    def _check_if_object_exists(self, django_type: TDjangoModelType, runtime_context: RuntimeContext) -> bool:
        input_name = self._create_mutation_input_parameter(runtime_context.build_context)
        input = runtime_context.kwargs[input_name]
        d = dict()
        for f in self._get_fields_to_check(runtime_context):
            d[f] = getattr(input, f)
        try:
            django_type._default_manager.get(**d)
            return True
        except:
            return False

    def _add_new_object_in_database(self, django_type: TDjangoModelType, runtime_context: RuntimeContext) -> any:
        """
        Adds a new object in the database. You are ensured that the object does not yet exist in the database

        :param django_type: type of the model to fetch
        :param info: graphql info value
        :param args: graphql args
        :param kwargs: graphql kwargs
        :return: anything you want. It should repersents the added row though
        """
        input_name = self._create_mutation_input_parameter(runtime_context.build_context)
        input_dict = runtime_context.kwargs[input_name]
        # create argumejnt and omits the None values
        create_args = {k: v for k, v in dict(input_dict).items() if v is not None}
        result = django_type._default_manager.create(**create_args)
        return result, create_args

    def _check_new_object_return_value(self, result: any, django_type: TDjangoModelType,
                                       runtime_context: RuntimeContext):
        value, create_args = result
        if value is None:
            raise GraphQLAppError(error_codes.CREATION_FAILED, object=django_type.__name__, values=create_args)