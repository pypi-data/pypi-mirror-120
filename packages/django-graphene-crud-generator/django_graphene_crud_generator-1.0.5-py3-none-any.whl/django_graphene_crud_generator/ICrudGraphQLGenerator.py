import abc
from typing import List, Tuple, Dict, Callable

import stringcase
from django.db.models import QuerySet

from django_koldar_utils.django_toolbox import django_helpers, auth_decorators, filters_helpers
from django_koldar_utils.graphql_toolsbox import error_codes
from django_koldar_utils.graphql_toolsbox.GraphQLAppError import GraphQLAppError
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.crud_generator.contexts import BuildContext, RuntimeContext
from django_koldar_utils.graphql_toolsbox.crud_operation_namers import ICrudOperationNamer, StandardCrudOperationNamer
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument, TGrapheneReturnType, TDjangoModelType, \
    TGrapheneType, TGrapheneInputType


class ICrudGraphQLGenerator(abc.ABC):

    def _activate_field_name(self, context: BuildContext) -> bool:
        """
        :return: Name of the field specifying whether or not a row is active
        """
        return "active"

    @abc.abstractmethod
    def _get_permissions_to_create(self, context: BuildContext) -> List[str]:
        pass

    @abc.abstractmethod
    def _get_permissions_to_read_single(self, context: BuildContext) -> List[str]:
        pass

    @abc.abstractmethod
    def _get_permissions_to_udpate(self, context: BuildContext) -> List[str]:
        pass

    @abc.abstractmethod
    def _get_permissions_to_delete(self, context: BuildContext) -> List[str]:
        pass

    def generate_graphql_crud_of(self,
                                 django_type: type, django_graphql_type: type, django_input_type: type,
                                 active_field_name: str = None,
                                 create_compare_fields: List[str] = None,
                                 permissions_required_create: List[str] = None,
                                 permissions_required_read: List[str] = None,
                                 permissions_required_update: List[str] = None,
                                 permissions_required_delete: List[str] = None,
                                 class_names: "ICrudOperationNamer" = None,
                                 generate_create: bool = True,
                                 generate_read_all: bool = True,
                                 generate_read_single: bool = True,
                                 generate_update: bool = True,
                                 generate_delete: bool = True,
                                 credentials: any = None,
                                 token_name: str = None
                                 ) -> Tuple[type, type, type, type, type]:
        """
        Generate a default create, update, delete operations. Delete actually just set the active field set to false.

        :param django_type: class deriving from models.Model
        :param django_graphql_type: class deriving from DjangoObjectType of graphene_toolbox package
        :param django_input_type: class deriving from DjangoInputObjectType from django_toolbox graphene_toolbox extras package
        :param active_field_name: name fo the active flag
        :param create_compare_fields: field used to check uniquness of the row when creating a new element. If missing, we will populate them with all the unique fields.
            Inactive rows are ignored
        :param permissions_required_create: permissions used to create elements. If None the mutation does not required authentication
        :param permissions_required_read: permissions used to read elements. If None the mutation does not required authentication
        :param permissions_required_update: permissions used to update elements. If None the mutation does not required authentication
        :param permissions_required_delete: permissions used to delete elements. If None the mutation does not required authentication
        :param class_names: instance representing a structure that supplies the name of the queries and mutation to create.
        :param generate_create: if true, we will generate the create mutation. Otherwise we will return None as the generated mutation class
        :param generate_read_all: if true, we will generate the read all mutation. Otherwise we will return None as the generated mutation class
        :param generate_read_single: if true, we will generate the read single mutatuion. Otherwise we will return None as the generated query class
        :param generate_update: if true, we will generate the update mutatuion. Otherwise we will return None as the generated query class
        :param generate_delete: if true, we will generate the delete mutatuion. Otherwise we will return None as the generated mutation class
        :param token_name: name of the token used to authenticate requests. if left missing, it is "token"
        :return: a tuple where each element is a class representing a mutation/query or None if the associated method "generate_" is set to False.
            - create mutation type
            - read all query type
            - update mutation type
            - delete mutation type
            - read single element query type
        """
        build_context = BuildContext(django_type, django_graphql_type, django_input_type)

        create = None
        read_single = None
        read_all = None
        update = None
        delete = None

        if class_names is None:
            class_names = StandardCrudOperationNamer()
        primary_key_name = django_helpers.get_name_of_primary_key(django_type)

        if generate_create:
            create = self._generate_mutation_create(
                build_context=build_context,
            )

        if generate_read_all:
            read_all = self._generate_mutation_read_all(
                build_context=build_context
            )

        if generate_read_single:
            read_all = self._generate_mutation_read_single(
                build_context=build_context
            )

        if generate_update:
            update = cls.generate_mutation_update_primitive_data(
                django_type=django_type,
                django_graphql_type=django_graphql_type,
                django_input_type=django_input_type,
                permissions_required=permissions_required_update,
                mutation_class_name=class_names.get_update_name(django_type),
                output_name=class_names.get_update_return_value_name(django_type),
                token_name=token_name,
            )

        if generate_delete:
            delete = cls.generate_mutation_mark_inactive(
                django_type=django_type,
                django_graphql_type=django_graphql_type,
                django_input_type=django_input_type,
                active_flag_name=active_field_name,
                permissions_required=permissions_required_delete,
                mutation_class_name=class_names.get_delete_name(django_type),
                output_name=class_names.get_delete_return_value_name(django_type),
                token_name=token_name,
            )
        return create, read_all, update, delete, read_single

    @abc.abstractmethod
    def _get_parameters_to_add_to_all_graphql(self, context: BuildContext) -> Dict[str, TGrapheneArgument]:
        """
        Set of graphql parameters that will be added to any graphql endpoint. If the argument is already present,
        we will override the previous parameter
        """
        pass

    # ######################################
    # READ SINGLE
    # ######################################

    @abc.abstractmethod
    def _read_single_query_name(self, build_context: BuildContext) -> str:
        """
        :return: the name of thwe type representing this query
        """
        pass
        return f"Get{stringcase.pascalcase(build_context.django_type.__name__)}Item"

    @abc.abstractmethod
    def _get_read_single_queryset_filter(self, queryset: QuerySet, runtime_context: RuntimeContext) -> QuerySet:
        """
        computes the result to show to the user when running the read single element query

        :param queryset: the set of all the elements of type django_type
        :param runtime_context: information know when running the graphql endpoint
        :return: result to output to the query
        """
        pass

    def _read_single_query_description(self, build_context: BuildContext) -> str:
        perms = self._get_permissions_to_read_single(build_context)
        return f"""Allows you to get a single element of {build_context.django_type.__name__} within the database.
        In order to run the query, you need the following permissions: {', '.join(perms)}
        """

    @abc.abstractmethod
    def _read_single_query_arguments(self, build_context: BuildContext) -> Dict[str, TGrapheneArgument]:
        """
        :return: arguments for the read single element query
        """
        pass

    def _read_single_body_decorator(self, build_context: BuildContext) -> Callable:
        """
        The decorator we use to decorate the actual read all query body. By default it is a no op operation

        :param build_context: information known at build time
        """

        def decorator(f):
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return decorator

    # ######################################
    # READ ALL
    # ######################################

    @abc.abstractmethod
    def _read_all_query_name(self, build_context: BuildContext) -> str:
        pass
        return f"GetAll{stringcase.pascalcase(build_context.django_type.__name__)}Items"

    @abc.abstractmethod
    def _get_read_all_queryset_filter(self, queryset: QuerySet, runtime_context: RuntimeContext) -> QuerySet:
        pass
        return queryset

    def _read_all_query_description(self, build_context: BuildContext) -> str:
        """
        :param build_context: information known at build time
        :return: the documentation attached to the read all query
        """
        perms = self._get_permissions_to_read_all(build_context)
        return f"""Allows you to get all the {build_context.django_type.__name__} within the database. In order to
        execute the query, you need to following permissions: {', '.join(perms)} 
        """

    @abc.abstractmethod
    def _read_all_query_arguments(self, build_context: BuildContext) -> Dict[str, TGrapheneArgument]:
        """
        :param build_context: information known at build time
        :return: arguments of the query read all elements
        """
        pass

    def _read_all_body_decorator(self, build_context: BuildContext) -> Callable:
        """
        The decorator we use to decorate the actual read all query body

        :param build_context: information known at build time
        """
        def decorator(f):
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return decorator

    @abc.abstractmethod
    def _get_permissions_to_read_all(self, context: BuildContext) -> List[str]:
        """
        :return: list of permissions required by the client in order to run the read all query
        """
        pass

    def _generate_mutation_read_all(self, build_context: BuildContext) -> type:
        arguments = self._read_all_query_arguments(build_context)
        arguments.update(self._get_parameters_to_add_to_all_graphql(build_context))

        result = GraphQLHelper.generate_query_from_queryset_filter(
            django_type=build_context.django_type,
            query_class_name=self._read_all_query_name(build_context),
            description=self._read_all_query_description(build_context),
            return_multipler="multi",
            queryset_filter=lambda queryset, query_type, info, args, kwargs: self._get_read_all_queryset_filter(queryset, RuntimeContext(build_context, info, query_type, args, kwargs)),
            arguments=arguments,
            return_type=build_context.graphene_type,
            body_decorator=self._read_all_body_decorator(build_context)
        )

        return result

    # ######################################
    # CREATE
    # ######################################

    def _create_mutation_description(self, context: BuildContext) -> str:
        """
        the description of the create mutation
        """
        perms = self._get_permissions_to_create(context)

        description = f"""Allows you to create a new instance of {context.django_type.__name__}. 
            If the object is already present we do nothing.
        """
        if len(perms) > 0:
            description += f"""Note that you need to authenticate your user in order to use this mutation.
                The permission your user is required to have are: {', '.join(perms)}. 
            """
        return description

    @abc.abstractmethod
    def _create_mutation_class_name(self, context: BuildContext) -> str:
        """
        mutation class name
        """
        pass

    @abc.abstractmethod
    def _create_mutation_parameters(self, context: BuildContext) -> Dict[str, TGrapheneArgument]:
        """
        create mutation graphql parameters
        """
        pass

    @abc.abstractmethod
    def _create_mutation_return_value(self, context: BuildContext) -> Dict[str, TGrapheneReturnType]:
        """
        create mutation graphql return values
        """
        pass

    @abc.abstractmethod
    def _check_if_object_exists(self, django_type: TDjangoModelType, runtime_context: RuntimeContext) -> bool:
        """
        Check if a particular element already exists in the database

        :param django_type: type of the model to fetch
        :param info: graphql info value
        :param args: graphql args
        :param kwargs: graphql kwargs
        :return: true if the object already exists in the database, false otherwise
        """
        pass

    @abc.abstractmethod
    def _add_new_object_in_database(self, django_type: TDjangoModelType, runtime_context: RuntimeContext) -> any:
        """
        Adds a new object in the database. You are ensured that the object does not yet exist in the database

        :param django_type: type of the model to fetch
        :param runtime_context: data availalbe to us while running the query
        :return: anything you want. It should repersents the added row though
        """
        pass

    @abc.abstractmethod
    def _check_new_object_return_value(self, result: any, django_type: TDjangoModelType, runtime_context: RuntimeContext):
        """
        Check if the output of _add_new_object_in_database represents a successful operation or not

        :param result: output of _add_new_object_in_database
        :param django_type: type of the model to fetch
        :param runtime_context: data availalbe to us while running the query
        """
        pass

    @abc.abstractmethod
    def _create_generate_mutation_instance_row_already_exists(self, mutation_class: type, runtime_context: RuntimeContext) -> any:
        """
        code used to create the instance of the create mutation class when the element to add is already
        present in the database

        :param mutation_class: type of the create mutation
        :return: instance of mutation_class
        """
        pass

    @abc.abstractmethod
    def _create_generate_mutation_instance_row_added(self, mutation_class: type, result: any, runtime_context: RuntimeContext) -> any:
        """
        code used to create the instance of the create mutation class when the element to add has
        been successfully added

        :param mutation_class: type of the create mutation
        :return: instance of mutation_class
        """
        pass

    def _create_mutation_decorate_body(self, build_context: BuildContext):
        """
        generate a decorator that will decorate the actual mutation body. graphql body function
        follows this signature:

        .. code-block::

            def body(mutation_class, info, *args, **kwargs) -> any:


        By default we will generate a noop decorator
        :param build_context: data available at buildtime
        """
        def result(f):
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return result

    def _generate_mutation_create(self, build_context: BuildContext) -> type:
        """
        Create a mutation that adds a new element in the database.
        We will generate a mutation that accepts a single input parameter. It checks if the input is not already present in the database and if not, it adds it.
        The returns the data added in the database.
        This method can already integrate graphene_jwt to authenticate and authorize users

        :param build_context: object containing data availalbe while genrating the graphql mutations and queries
        :return: class rerpesenting the mutation
        """

        mutation_class_name = self._create_mutation_class_name(build_context)
        description = self._create_mutation_description(build_context)
        mutation_arguments = self._create_mutation_parameters(build_context)
        mutation_arguments.update(self._get_parameters_to_add_to_all_graphql(build_context))
        mutation_return_value = self._create_mutation_return_value(build_context)

        @auth_decorators.graphql_ensure_user_has_permissions(perm=self._get_permissions_to_create(build_context))
        def body(mutation_class, info, *args, **kwargs) -> any:
            runtime_context = RuntimeContext(build_context, info, mutation_class, *args, **kwargs)
            exists = self._check_if_object_exists(build_context.django_type, runtime_context)
            if exists:
                return self._create_generate_mutation_instance_row_already_exists(mutation_class)
            # add the instance
            create_result = self._add_new_object_in_database(build_context.django_type, runtime_context)
            result = self._create_generate_mutation_instance_row_added(mutation_class, create_result, runtime_context)
            return result

        return GraphQLHelper.create_mutation(
            mutation_class_name=mutation_class_name,
            description=description,
            arguments=mutation_arguments,
            return_type=mutation_return_value,
            body=self._create_mutation_decorate_body(build_context)(body)
        )







