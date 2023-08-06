import abc
from typing import List, Dict, Callable

from django.db.models import QuerySet
from django_koldar_utils.django_toolbox import auth_decorators
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType, TGrapheneArgument

from django_graphene_crud_generator.ICrudGraphQLGenerator import ICrudGraphQLGenerator
from django_graphene_crud_generator.crud_generator.CanXPermissionsMixIn import CanXPermissionsMixIn
from django_graphene_crud_generator.crud_generator.CreateMutationReturnAddedValueMixIn import \
    CreateMutationReturnAddedValueMixIn
from django_graphene_crud_generator.crud_generator.CreateMutationReturnTrueMixIn import CreateMutationReturnTrueMixIn
from django_graphene_crud_generator.crud_generator.CreateMutationViaSingleInputMixIn import \
    CreateMutationViaSingleInputMixIn
from django_graphene_crud_generator.crud_generator.CrudGraphQLViaTokenGenerateMixIn import \
    CrudGraphQLViaTokenGenerateMixIn
from django_graphene_crud_generator.crud_generator.FederationNamesMixIn import FederationNamesMixIn
from django_graphene_crud_generator.crud_generator.ReadStandardMixIn import ReadStandardMixIn
from django_graphene_crud_generator.crud_generator.contexts import BuildContext, RuntimeContext


class AbstractFederatedCrudGenerator(
    CrudGraphQLViaTokenGenerateMixIn, CanXPermissionsMixIn, FederationNamesMixIn,
    CreateMutationViaSingleInputMixIn,
    ReadStandardMixIn,
    ICrudGraphQLGenerator, abc.ABC
):
    pass


class SimplifiedFederatedTokenBasedCrudGenerator(
    CreateMutationReturnTrueMixIn,
    AbstractFederatedCrudGenerator
    ):
    """
    Build CRUD operations that are designed to work within a graphql federation and accessed via an access token.
    When available, we will return simplieif output (e.g., when creating a new element we will not return the actual
    element, but just a flag
    """
    pass


class StandardFederatedTokenBasedCrudGenerator(
    CreateMutationReturnAddedValueMixIn,
    AbstractFederatedCrudGenerator
    ):
    """
    Build CRUD operations that are designed to work within a graphql federation and accessed via an access token.
    If you need to develop a graphql server, this is most likely the crud operation you want to use
    """
    pass

