from typing import List

import stringcase

from django_graphene_crud_generator.crud_generator.contexts import BuildContext


class CanXPermissionsMixIn:
    """
    A mix in to support ICrudGraphQLGenerator implementations.

    This mixin configure the generator in such a way that it uses "can_X_Y" permissions,
    where X is either "create, view, update, delete" while Y is the snake case of a django model (e.g. foobar)
    """

    def _get_permissions_to_create(self, context: BuildContext) -> List[str]:
        return [f"add_{stringcase.snakecase(context.django_type.__name__)}"]

    def _get_permissions_to_read_single(self, context: BuildContext) -> List[str]:
        return [f"view_{stringcase.snakecase(context.django_type.__name__)}"]

    def _get_permissions_to_read_all(self, context: BuildContext) -> List[str]:
        return [f"view_{stringcase.snakecase(context.django_type.__name__)}"]

    def _get_permissions_to_update(self, context: BuildContext) -> List[str]:
        return [f"change_{stringcase.snakecase(context.django_type.__name__)}"]

    def _get_permissions_to_delete(self, context: BuildContext) -> List[str]:
        return [f"delete_{stringcase.snakecase(context.django_type.__name__)}"]