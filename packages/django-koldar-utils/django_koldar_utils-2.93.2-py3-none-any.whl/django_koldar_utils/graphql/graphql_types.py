from typing import Union

import graphene

TDjangoModelType = type
"""
A type that extends models.Model
"""
TGrapheneType = type
"""
A type that extends graphene_toolbox.OPbjectType
"""
TGrapheneInputType = type
"""
A type that extends graphene_toolbox.ObjectInputType
"""

TGrapheneQuery = type
"""
A type that rerpesents a grpahql query
"""
TGrapheneMutation = type
"""
A type that rerpesents a grpahql mutation
"""

TGrapheneType = type
"""
A type that represent a graphene_toolbox type object (e.g., AuthorGraphqlType)
"""

TGrapheneReturnType = Union[graphene.Scalar, graphene.Field]
"""
A type that is put in graphene_toolbox.ObjectType and represents a query/mutation field
"""
TGrapheneArgument = Union[graphene.Scalar, graphene.InputObjectType, graphene.Argument]
"""
A type that is put in graphene_toolbox.ObjectType and represents a query/mutation argument
"""