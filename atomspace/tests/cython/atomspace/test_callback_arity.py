import unittest

from opencog.utilities import set_default_atomspace, finalize_opencog
from opencog.type_constructors import *

import __main__


def return_concept(atom):
    return atom.atomspace.add_node(types.ConceptNode, "test")


__main__.return_concept = return_concept


class TestExecutionOutputLink(unittest.TestCase):

    def setUp(self):
        self.space = AtomSpace()
        set_default_atomspace(self.space)

    def tearDown(self):
        finalize_opencog()
        del self.space

    def test_correct_argcount(self):
        atom1 = ConceptNode("atom1")
        exec_link = ExecutionOutputLink(GroundedSchemaNode("py:return_concept"),
                                        ListLink(atom1))
        result = exec_link.execute()
        self.assertTrue(result.name == "test")

    def test_too_many_args(self):
        atom1 = ConceptNode("atom1")
        exec_link = ExecutionOutputLink(GroundedSchemaNode("py:return_concept"),
                                        ListLink(atom1, atom1))
        try:
           result = self.space.execute(exec_link)
           self.assertFalse("call should fail")
        except RuntimeError as e:
           self.assertTrue("but 2 were given" in str(e))

    def test_too_few_args(self):
        atom1 = ConceptNode("atom1")
        exec_link = ExecutionOutputLink(GroundedSchemaNode("py:return_concept"),
                                        ListLink())
        try:
           result = self.space.execute(exec_link)
           self.assertFalse("call should fail")
        except RuntimeError as e:
           self.assertTrue("missing 1 required positional argument" in str(e))

