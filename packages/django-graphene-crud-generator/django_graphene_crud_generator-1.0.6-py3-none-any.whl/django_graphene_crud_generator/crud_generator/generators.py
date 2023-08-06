from typing import List, Dict

from django.db.models import QuerySet
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType, TGrapheneArgument

from django_graphene_crud_generator.ICrudGraphQLGenerator import ICrudGraphQLGenerator
from django_graphene_crud_generator.crud_generator.CanXPermissionsMixIn import CanXPermissionsMixIn
from django_graphene_crud_generator.crud_generator.CreateMutationReturnTrueMixIn import CreateMutationReturnTrueMixIn
from django_graphene_crud_generator.crud_generator.CreateMutationViaSingleInputMixIn import \
    CreateMutationViaSingleInputMixIn
from django_graphene_crud_generator.crud_generator.CrudGraphQLViaTokenGenerateMixIn import \
    CrudGraphQLViaTokenGenerateMixIn
from django_graphene_crud_generator.crud_generator.FederationNamesMixIn import FederationNamesMixIn
from django_graphene_crud_generator.crud_generator.ReadStandardMixIn import ReadStandardMixIn
from django_graphene_crud_generator.crud_generator.contexts import BuildContext, RuntimeContext


class AbstractFederatedTokenBasedCrudGenerator(
    CrudGraphQLViaTokenGenerateMixIn, CanXPermissionsMixIn, FederationNamesMixIn,
    CreateMutationViaSingleInputMixIn, CreateMutationReturnTrueMixIn,
    ReadStandardMixIn, ICrudGraphQLGenerator):
    """
    Build CRUD operations that are designed to work within a graphql federation and accessed via an access token
    """
    pass