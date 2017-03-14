# Copyright © 2016, 2017 CZ.NIC, z. s. p. o.
#
# This file is part of Yangson.
#
# Yangson is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Yangson is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with Yangson.  If not, see <http://www.gnu.org/licenses/>.

"""Exceptions used by the Yangson library.

This module defines the following exceptions:

* :exc:`BadSchemaNodeType`: A schema node is of a wrong type.
* :exc:`BadYangLibraryData`: Invalid YANG library data.
* :exc:`CyclicImports`: Imports of YANG modules form a cycle.
* :exc:`DefinitionNotFound`: Requested definition does not exist.
* :exc:`EndOfInput`: Unexpected end of input.
* :exc:`FeaturePrerequisiteError`: Pre-requisite feature isn't supported.
* :exc:`InstanceException`: Base class for exceptions related to operations
  on instance nodes.
* :exc:`InstanceValueError`: The instance value is incompatible with the called method.
* :exc:`InvalidArgument`: Invalid argument of a statement.
* :exc:`InvalidFeatureExpression`: Invalid if-feature expression.
* :exc:`InvalidKeyValue`: Invalid list key or leaf-list value.
* :exc:`InvalidLeafrefPath`: A leafref path is incorrect.
* :exc:`InvalidSchemaPath`: Invalid schema path
* :exc:`InvalidXPath`: An XPath expression is invalid.
* :exc:`MissingModule`: Abstract exception class – a module is missing.
* :exc:`ModuleNotFound`: A module not found.
* :exc:`ModuleNotImplemented`: A module is not implemented in the data model.
* :exc:`ModuleNotImported`: A module is not imported.
* :exc:`ModuleNotRegistered`: An imported module is not registered in YANG library.
* :exc:`MultipleImplementedRevisions`: A module has multiple implemented revisions.
* :exc:`NonexistentInstance`: Attempt to access an instance node that doesn't
  exist.
* :exc:`NonexistentSchemaNode`: A schema node doesn't exist.
* :exc:`NotSupported`: A given XPath 1.0 feature isn't (currently) supported.
* :exc:`ParserException`: Base class for parser exceptions.
* :exc:`RawDataError`: Abstract exception class for errors in raw data.
* :exc:`RawMemberError`: Object member in raw data doesn't exist in the schema.
* :exc:`RawTypeError`: Raw data value is of incorrect type.
* :exc:`SchemaError`: An instance violates a schema constraint.
* :exc:`SchemaNodeException`: Abstract exception class for schema node errors.
* :exc:`SemanticError`: An instance violates a semantic rule.
* :exc:`StatementNotFound`: Required statement does not exist.
* :exc:`UnexpectedInput`: Unexpected input.
* :exc:`UnknownPrefix`: Unknown namespace prefix.
* :exc:`ValidationError`: Abstract exception class for instance validation errors.
* :exc:`WrongArgument`: Statement argument is invalid.
* :exc:`XPathTypeError`: A subexpression is of a wrong type.
* :exc:`YangsonException`: Base class for all Yangson exceptions.
* :exc:`YangTypeError`: A scalar value is of incorrect type.
"""

from typing import Tuple
from .typealiases import *

class YangsonException(Exception):
    """Base class for all Yangson exceptions."""
    pass

class InvalidArgument(YangsonException):
    """The argument of a statement is invalid."""

    def __init__(self, stmt: "Statement"):
        self.statement = stmt

    def __str(self):
        return str(self.statement)

class InvalidKeyValue(YangsonException):
    """List key or leaf-list value is invalid."""

    def __init__(self, value: ScalarValue):
        self.value = value

    def __str(self):
        return str(self.value)

class InstanceException(YangsonException):
    """Abstract class for exceptions related to operations on instance nodes."""

    def __init__(self, path: JSONPointer):
        self.path = path

    def __str__(self):
        return "[" + self.path + "]"

class InstanceValueError(InstanceException):
    """The instance value is incompatible with the called method."""

    def __init__(self, path: JSONPointer, detail: str):
        super().__init__(path)
        self.detail = detail

    def __str__(self):
        return "{} {}".format(super().__str__(), self.detail)

class NonexistentInstance(InstanceException):
    """Attempt to access an instance node that doesn't exist."""

    def __init__(self, path: JSONPointer, detail: str):
        super().__init__(path)
        self.detail = detail

    def __str__(self):
        return "{} {}".format(super().__str__(), self.detail)

class ParserException(YangsonException):
    """Base class for parser exceptions."""

    def __init__(self, coord: Tuple[int, int]):
        self.coord = coord

    def __str__(self) -> str:
        """Print line and column number.
        """
        if "\n" in self.parser.input:
            return "line {0}, column {1}".format(*self.coord)
        return str(self.parser)

class EndOfInput(ParserException):
    """Unexpected end of input."""
    pass

class UnexpectedInput(ParserException):
    """Unexpected input."""

    def __init__(self, coord: Tuple[int, int], expected: str = None):
        super().__init__(coord)
        self.expected = expected

    def __str__(self) -> str:
        """Add info about expected input if available."""
        ex = "" if self.expected is None else ": expected " + self.expected
        return super().__str__() + ex

class InvalidFeatureExpression(ParserException):
    """Invalid **if-feature** expression."""
    pass

class InvalidXPath(ParserException):
    """Exception to be raised for an invalid XPath expression."""
    pass

class NotSupported(ParserException):
    """Exception to be raised for unimplemented XPath features."""

    def __init__(self, coord: Tuple[int, int], feature: str):
        super().__init__(coord)
        self.feature = feature

    def __str__(self) -> str:
        return super().str() + ": " + str(self.feature)

class MissingModule(YangsonException):
    """Abstract exception class – a module is missing."""

    def __init__(self, name: YangIdentifier, rev: str = ""):
        self.name = name
        self.rev = rev

    def __str__(self) -> str:
        if self.rev:
            return self.name + "@" + self.rev
        return self.name

class ModuleNotFound(MissingModule):
    """A module or submodule registered in YANG library is not found."""
    pass

class ModuleNotRegistered(MissingModule):
    """A module is not registered in YANG library."""
    pass

class ModuleNotImplemented(MissingModule):
    """A module is not implemented in the data model."""
    pass

class BadYangLibraryData(YangsonException):
    """Broken YANG library data."""

    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self) -> str:
        return self.reason

class InvalidSchemaPath(YangsonException):
    """Invalid schema or data path."""

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return self.path

class UnknownPrefix(YangsonException):
    """Unknown namespace prefix."""

    def __init__(self, prefix: YangIdentifier, mid: ModuleId):
        self.prefix = prefix
        self.mid = mid

    def __str__(self) -> str:
        return "prefix {} is not defined in {}".format(self.prefix, self.mid)

class ModuleNotImported(YangsonException):
    """Module is not imported."""

    def __init__(self, mod: YangIdentifier, mid: ModuleId):
        self.mod = mod
        self.mid = mid

    def __str__(self) -> str:
        return "{} not imported in {}".format(self.mod, self.mid)

class FeaturePrerequisiteError(YangsonException):
    """Pre-requisite feature is not supported."""

    def __init__(self, name: YangIdentifier, ns: YangIdentifier):
        self.name = name
        self.ns = ns

    def __str__(self) -> str:
        return "{}:{}".format(self.ns, self.name)

class MultipleImplementedRevisions(YangsonException):
    """A module has multiple implemented revisions."""

    def __init__(self, module: YangIdentifier):
        self.module = module

    def __str__(self) -> str:
        return self.module

class CyclicImports(YangsonException):
    """YANG modules are imported in a cyclic fashion."""
    pass

class SchemaNodeException(YangsonException):
    """Abstract exception class for schema node errors."""

    def __init__(self, qn: QualName):
        self.qn = qn

    def __str__(self) -> str:
        return str(self.qn)

class NonexistentSchemaNode(SchemaNodeException):
    """A schema node doesn't exist."""

    def __init__(self, qn: QualName, name: YangIdentifier,
                 ns: YangIdentifier = None):
        super().__init__(qn)
        self.qn = ("{}:".format(ns) if ns else "") + name

    def __str__(self) -> str:
        loc = ("under " + super().__str__() if self.schema_node.parent
                   else "top level")
        return "{} – {}".format(loc, self.qn)

class BadSchemaNodeType(SchemaNodeException):
    """A schema node is of a wrong type."""

    def __init__(self, qn: QualName, expected: str):
        super().__init__(qn)
        self.expected = expected

    def __str__(self) -> str:
        return super().__str__() + " is not a " + self.expected

class InvalidLeafrefPath(SchemaNodeException):
    """A leafref path is incorrect."""
    pass

class RawDataError(YangsonException):
    """Abstract exception class for errors in raw data."""

    def __init__(self, jptr: JSONPointer):
        self.jptr = jptr

    def __str__(self) -> JSONPointer:
        return self.jptr

class RawMemberError(RawDataError):
    """Object member in the raw value doesn't exist in the schema."""
    pass

class RawTypeError(RawDataError):
    """Raw value is of an incorrect type."""

    def __init__(self, jptr: JSONPointer, detail: str):
        super().__init__(jptr)
        self.detail = detail

    def __str__(self):
        return "[{}] {}".format(self.jptr, self.detail)

class ValidationError(YangsonException):
    """Abstract exception class for instance validation errors."""

    def __init__(self, path: JSONPointer, tag: str, message: str = None):
        self.path = path
        self.tag = tag
        self.message = message

    def __str__(self) -> str:
        msg = ": " + self.message if self.message else ""
        return "[{}]{}{}".format(self.path, self.tag, msg)

class SchemaError(ValidationError):
    """An instance violates a schema constraint."""
    pass

class SemanticError(ValidationError):
    """An instance violates a semantic rule."""
    pass

class YangTypeError(YangsonException):
    """A scalar value doesn't match its expected type."""
    pass

class StatementNotFound(YangsonException):
    """Required statement does not exist."""

    def __init__(self, parent: PrefName, kw: YangIdentifier):
        self.parent = parent
        self.keyword = kw

    def __str__(self) -> str:
        """Print the statement's keyword."""
        return "`{}' in `{}'".format(self.keyword, self.parent)

class DefinitionNotFound(YangsonException):
    """Requested definition does not exist."""

    def __init__(self, kw: YangIdentifier, name: YangIdentifier):
        self.keyword = kw
        self.name = name

    def __str__(self) -> str:
        return "{} {}".format(self.keyword, self.name)

class WrongArgument(YangsonException):
    """Statement argument is invalid."""

    def __init__(self, arg: str):
        self.arg = arg

    def __str__(self) -> str:
        return self.arg

class XPathTypeError(YangsonException):
    """The value of an XPath (sub)expression is of a wrong type."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value

from .statement import Statement
