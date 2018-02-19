#!/usr/bin/python
# -*- coding: utf-8 -*-

# For better print formatting
from __future__ import print_function

# Imports
import unittest


class Scop(object):
        """
        Represents a SCOP

        Attributes:
                - globl : Global SCOP properties
                - statements : List of Statement
                - extensions : Extensions properties
        """

        def __init__(self, globl=None, statements=None, extensions=None):
                self.globl = globl
                self.statements = statements
                self.extensions = extensions

        def get_global(self):
                return self.globl

        def get_statements(self):
                return self.statements

        def get_extensions(self):
                return self.extensions

        @staticmethod
        def read_os(f):
                # Store all file content
                with open(f, 'r') as f:
                        content = f.readlines()

                index = 0
                # Skip header
                while content[index] == '<OpenScop>\n' or content[index].startswith('# CLooG') or content[index] == '\n':
                        index = index + 1

                # Process global information
                from pycompss.util.translators.scop_types.scop.global_class import Global
                globl, index = Global.read_os(content, index)

                # Process statements
                from pycompss.util.translators.scop_types.scop.statement_class import Statement
                while content[index] == "\n" or content[index].startswith('#'):
                        index = index + 1
                num_statements = int(content[index])
                index = index + 1

                statements = []
                for _ in range(num_statements):
                        statement, index = Statement.read_os(content, index)
                        statements.append(statement)

                # Process extensions
                index = 108
                print("INIT EXTS WITH: " + str(content))
                print("INIT EXTS WITH: " + str(index))

                from pycompss.util.translators.scop_types.scop.extensions_class import Extensions
                extensions, index = Extensions.read_os(content, index)

                # Skip footer
                while index < len(content):
                        if content[index] != '\n' and content[index] != '</OpenScop>\n':
                                print("WARNING: Unexpected line at the end of the file: " + str(content[index]))
                        index = index + 1

                # Build scop
                scop = Scop(globl, statements, extensions)

                # Return structure
                return scop

        @staticmethod
        def read_py(f):
                pass

        def write_os(self, f):
                # Write header
                print("<OpenScop>", file=f)
                print("", file=f)

                # Print global
                if self.globl is not None:
                        self.globl.write_os(f)

                if self.statements is not None:
                        # Print number of statements
                        print("# Number of statements", file=f)
                        print(str(len(self.statements)), file=f)
                        print("", file=f)

                        # Print all statements
                        index = 1
                        for s in self.statements:
                                s.write_os(f, index)
                                index = index + 1

                # Print extensions
                if self.extensions is not None:
                        self.extensions.write_os(f)

                # Write footer
                print("</OpenScop>", file=f)
                print("", file=f)

        def write_py(self, f):
                pass


#
# UNIT TESTS
#

class TestScop(unittest.TestCase):

        # Helper method for unit tests
        @staticmethod
        def generate_empty_scop():
                from pycompss.util.translators.scop_types.scop.global_class import Global
                from pycompss.util.translators.scop_types.scop.statement_class import Statement
                from pycompss.util.translators.scop_types.scop.extensions_class import Extensions

                # Generate global
                g = Global()

                # Generate statements
                s1 = Statement()
                statements = [s1]

                # Generate extensions
                e = Extensions()

                # Generate SCOP
                scop = Scop(g, statements, e)

                return scop

        # Helper method for unit tests
        @staticmethod
        def generate_full_scop():
                from pycompss.util.translators.scop_types.scop.global_class import Global
                from pycompss.util.translators.scop_types.scop.statement_class import Statement
                from pycompss.util.translators.scop_types.scop.extensions_class import Extensions

                # Generate global
                from pycompss.util.translators.scop_types.scop.globl.context_class import Context, ContextType
                from pycompss.util.translators.scop_types.scop.globl.parameters_class import Parameters
                from pycompss.util.translators.scop_types.scop.globl.parameters.parameter_class import Parameter
                context = Context(ContextType.CONTEXT, 0, 5, 0, 0, 0, 3)
                params = Parameters([Parameter("strings", ["mSize", "kSize", "nSize"])])
                g = Global("C", context, params)

                # Generate statements
                from pycompss.util.translators.scop_types.scop.statement.relation_class import Relation, RelationType
                from pycompss.util.translators.scop_types.scop.statement.statement_extension_class import StatementExtension
                s1_domain = Relation(RelationType.DOMAIN, 9, 8, 3, 0, 0, 3, [[1, 1], [1, -1]])
                s1_scattering = Relation(RelationType.SCATTERING, 7, 15, 7, 3, 0, 3, [[0, -1], [0, 0]])
                s1_a1 = Relation(RelationType.READ, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s1_a2 = Relation(RelationType.WRITE, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s1_a3 = Relation(RelationType.MAY_WRITE, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s1_access = [s1_a1, s1_a2, s1_a3]
                s1_ext1 = StatementExtension(["i", "j", "k"], "c[i][j] += a[i][k]*b[k][j];")
                s1_extensions = [s1_ext1]
                s1 = Statement(s1_domain, s1_scattering, s1_access, s1_extensions)

                s2_domain = Relation(RelationType.DOMAIN, 9, 8, 3, 0, 0, 3, [[1, 1], [1, -1]])
                s2_scattering = Relation(RelationType.SCATTERING, 7, 15, 7, 3, 0, 3, [[0, -1], [0, 0]])
                s2_a1 = Relation(RelationType.READ, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s2_a2 = Relation(RelationType.WRITE, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s2_a3 = Relation(RelationType.MAY_WRITE, 3, 11, 3, 3, 0, 3, [[0, -1], [0, 0]])
                s2_access = [s2_a1, s2_a2, s2_a3]
                s2_ext1 = StatementExtension(["i", "j", "k"], "c[i][j] += a[i][k]*b[k][j];")
                s2_extensions = [s2_ext1]
                s2 = Statement(s2_domain, s2_scattering, s2_access, s2_extensions)

                statements = [s1, s2]

                # Generate extensions
                from pycompss.util.translators.scop_types.scop.extensions.arrays_class import Arrays
                from pycompss.util.translators.scop_types.scop.extensions.coordinates_class import Coordinates
                from pycompss.util.translators.scop_types.scop.extensions.scatnames_class import Scatnames
                scatnames = Scatnames(["b0", "i", "b1", "j", "b2", "k", "b3"])
                arrays = Arrays(["i", "mSize", "j", "kSize", "k", "nSize", "c", "a", "b"])
                coordinates = Coordinates("example2_src_matmul.cc", 72, 0, 80, 0, 8)
                e = Extensions(scatnames, arrays, coordinates)

                # Generate SCOP
                scop = Scop(g, statements, e)

                return scop

        def test_empty(self):
                scop = Scop()

                self.assertEqual(scop.get_global(), None)
                self.assertEqual(scop.get_statements(), None)
                self.assertEqual(scop.get_extensions(), None)

        def test_full(self):
                from pycompss.util.translators.scop_types.scop.global_class import Global
                from pycompss.util.translators.scop_types.scop.statement_class import Statement
                from pycompss.util.translators.scop_types.scop.extensions_class import Extensions

                from pycompss.util.translators.scop_types.scop.globl.context_class import Context, ContextType
                from pycompss.util.translators.scop_types.scop.globl.parameters_class import Parameters
                from pycompss.util.translators.scop_types.scop.globl.parameters.parameter_class import Parameter
                g = Global("C", Context(ContextType.CONTEXT, 0, 5, 0, 0, 0, 3), Parameters([Parameter("strings", ["mSize", "kSize", "nSize"])]))
                s1 = Statement()
                s2 = Statement()
                statements = [s1, s2]
                e = Extensions()

                scop = Scop(g, statements, e)

                self.assertEqual(scop.get_global(), g)
                self.assertEqual(scop.get_statements(), statements)
                self.assertEqual(scop.get_extensions(), e)

        def test_write_os_empty(self):
                # Generate empty SCOP
                scop = TestScop.generate_empty_scop()

                # Generate file
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                outputFile = dirPath + "/tests/test1.out.scop"
                expectedFile = dirPath + "/tests/empty.scop"
                with open(outputFile, 'w') as f:
                        scop.write_os(f)

                # Check file content
                with open(expectedFile, 'r') as f:
                        expectedContent = f.read()
                with open(outputFile, 'r') as f:
                        outputContent = f.read()
                self.assertEqual(outputContent, expectedContent)

                # Erase file
                os.remove(outputFile)

        def test_write_os_full(self):
                # Generate full SCOP
                scop = TestScop.generate_full_scop()

                # Generate file
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                outputFile = dirPath + "/tests/test2.out.scop"
                expectedFile = dirPath + "/tests/full.scop"
                with open(outputFile, 'w') as f:
                        scop.write_os(f)

                # Check file content
                with open(expectedFile, 'r') as f:
                        expectedContent = f.read()
                with open(outputFile, 'r') as f:
                        outputContent = f.read()
                self.assertEqual(outputContent, expectedContent)

                # Erase file
                os.remove(outputFile)

        def ttest_read_os_empty(self):
                # Read from OpenScop
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                inputFile = dirPath + "/tests/empty.scop"
                scop = Scop.read_os(inputFile)

                # Build expected content
                scopExp = TestScop.generate_empty_scop()

                # Check loaded content
                self.assertEqual(scop, scopExp)

        def ttest_read_os_full(self):
                # Read from OpenScop
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                inputFile = dirPath + "/tests/full.scop"
                scop = Scop.read_os(inputFile)

                # Build expected content
                scopExp = TestScop.generate_full_scop()

                # Check loaded content
                self.assertEqual(scop, scopExp)

        def ttest_write_py_empty(self):
                # Read from OpenScop
                import os
                dirPath = os.path.dirname(os.path.realpath(__file__))
                inputFile = dirPath + "/tests/empty.scop"
                outputFile = dirPath + "/tests/test7.out.python"
                expectedFile = dirPath + "/tests/empty.python"

                scop = Scop.read_os(inputFile)

                # Generate Python file
                scop.write_py(outputFile)

                # Check file content
                with open(expectedFile, 'r') as f:
                        expectedContent = f.read()
                with open(outputFile, 'r') as f:
                        outputContent = f.read()
                self.assertEqual(outputContent, expectedContent)

                # Erase file
                os.remove(outputFile)


#
# MAIN
#

if __name__ == '__main__':
        unittest.main()
