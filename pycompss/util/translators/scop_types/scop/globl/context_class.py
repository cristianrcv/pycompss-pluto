#!/usr/bin/python
# -*- coding: utf-8 -*-

# For better print formatting
from __future__ import print_function

# Imports
import unittest
from enum import Enum


#
# CONTEXT TYPE ENUMERATION
#

class ContextType(Enum):
        UNDEFINED = -1
        CONTEXT = 2


#
# CONTEXT CLASS
#

class Context(object):
        """
        Represents a global context

        Attributes:
                - contextType : The context type (CONTEXT or UNDEFINED)
                - rows : Number of rows
                - columns : Number of columns
                - outputDims : Number of output dimensions
                - inputDims : Number of input dimensions
                - localDims : Number of local dimensions
                - params : Number of parameters
        """

        def __init__(self, contextType=ContextType.UNDEFINED, rows=-1, columns=-1, outputDims=-1, inputDims=-1, localDims=-1, params=-1):
                self.contextType = contextType
                self.rows = rows
                self.columns = columns
                self.outputDims = outputDims
                self.inputDims = inputDims
                self.localDims = localDims
                self.params = params

        def get_context_type(self):
                return self.contextType

        def get_rows(self):
                return self.rows

        def get_columns(self):
                return self.columns

        def get_output_dims(self):
                return self.outputDims

        def get_input_dims(self):
                return self.inputDims

        def get_local_dims(self):
                return self.localDims

        def get_params(self):
                return self.params

        @staticmethod
        def read_os(content, index):
                # Skip header and any annotation
                while content[index].startswith('#') or content[index] == '\n' or content[index] == 'CONTEXT\n':
                        index = index + 1

                # Process mandatory field: type rows columns outputDims inputDims localDims params
                line = content[index]
                index = index + 1

                fields = line.split()

                # Skip empty lines, and any annotation
                while index < len(content) and (content[index].startswith('#') or content[index] == '\n'):
                        index = index + 1

                # Build Context
                context = Context(ContextType.CONTEXT, *fields)

                # Return structure
                return context, index

        def write_os(self, f):
                # Print type
                print(self.contextType.name, file=f)

                # Print value attributes
                print(str(self.rows) + " " + str(self.columns) + " " + str(self.outputDims) + " " + str(self.inputDims) + " " + str(self.localDims) + " " + str(self.params), file=f)

                # Separator
                print("", file=f)


#
# UNIT TESTS
#

class TestContext(unittest.TestCase):

        def test_empty(self):
                context = Context()

                self.assertEqual(context.get_context_type().name, ContextType.UNDEFINED.name)
                self.assertEqual(context.get_rows(), -1)
                self.assertEqual(context.get_columns(), -1)
                self.assertEqual(context.get_output_dims(), -1)
                self.assertEqual(context.get_input_dims(), -1)
                self.assertEqual(context.get_local_dims(), -1)
                self.assertEqual(context.get_params(), -1)

        def test_full(self):
                contextType = ContextType.CONTEXT
                rows = 0
                cols = 5
                od = 0
                ind = 0
                ld = 0
                params = 3
                context = Context(contextType, rows, cols, od, ind, ld, params)

                self.assertEqual(context.get_context_type().name, contextType.name)
                self.assertEqual(context.get_rows(), rows)
                self.assertEqual(context.get_columns(), cols)
                self.assertEqual(context.get_output_dims(), od)
                self.assertEqual(context.get_input_dims(), ind)
                self.assertEqual(context.get_local_dims(), ld)
                self.assertEqual(context.get_params(), params)

        def test_write_os(self):
                contextType = ContextType.CONTEXT
                rows = 0
                cols = 5
                od = 0
                ind = 0
                ld = 0
                params = 3
                context = Context(contextType, rows, cols, od, ind, ld, params)

                try:
                        # Generate file
                        fileName = "context_test.out"
                        with open(fileName, 'w') as f:
                                context.write_os(f)

                        # Check file content
                        expected = "CONTEXT\n0 5 0 0 0 3\n\n"
                        with open(fileName, 'r') as f:
                                content = f.read()
                        self.assertEqual(content, expected)
                except Exception:
                        raise
                finally:
                        # Erase file
                        import os
                        os.remove(fileName)

        def test_read_os(self):
                # Store all file content
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                contextFile = dirPath + "/tests/context_test.expected.scop"
                with open(contextFile, 'r') as f:
                        content = f.readlines()

                # Read from file
                c, index = Context.read_os(content, 0)

                # Check index value
                self.assertEqual(index, len(content))

                # Check Context object content
                try:
                        # Write to file
                        outputFile = dirPath + "/tests/context_test.out.scop"
                        with open(outputFile, 'w') as f:
                                c.write_os(f)

                        # Check file content
                        with open(contextFile, 'r') as f:
                                expectedContent = f.read()
                        with open(outputFile, 'r') as f:
                                outputContent = f.read()
                        self.assertEqual(outputContent, expectedContent)
                except Exception:
                        raise
                finally:
                        # Remove test file
                        os.remove(outputFile)


#
# MAIN
#

if __name__ == '__main__':
        unittest.main()
