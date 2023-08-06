from typing import Dict

from django_koldar_utils.graphql_toolsbox.graphql_types import TDjangoModelType, TGrapheneType, TGrapheneInputType


class BuildContext(object):

    def __init__(self, django_type: TDjangoModelType, graphene_type: TGrapheneType, graphene_input_type: TGrapheneInputType, params: Dict[str, any]):
        self.django_type = django_type
        self.graphene_type = graphene_type
        self.graphene_input_type = graphene_input_type

        self.create_parameters: Dict[str, TGrapheneType] = None
        self.read_single_parameters: Dict[str, TGrapheneType] = None
        self.read_all_parameters: Dict[str, TGrapheneType] = None
        self.update_parameters: Dict[str, TGrapheneType] = None
        self.delete_parameters: Dict[str, TGrapheneType] = None

        self.create_return_value: Dict[str, TGrapheneType] = None
        self.read_single_return_value: Dict[str, TGrapheneType] = None
        self.read_all_return_value: Dict[str, TGrapheneType] = None
        self.update_return_value: Dict[str, TGrapheneType] = None
        self.delete_return_value: Dict[str, TGrapheneType] = None
        
        self.params = params


class RuntimeContext(object):
    """
    Information available while running a graphql endpoint
    """

    def __init__(self, c: BuildContext, info, graphql_class, *args, **kwargs):
        self.build_context = c
        self.info = info
        self.graphql_class = graphql_class
        self.args = args
        self.kwargs = kwargs