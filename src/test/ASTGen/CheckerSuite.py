import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
	def test0(self):
		input = """func test()
        begin
            string a[1,2] <- [["hello", "world"]]
            if (a[1,2] == "hello") return true
            else return false
        end
        func main()
        begin
            number s <- test()
        end
        """
		expect = """Type Mismatch In Statement: VarDecl(Id(s), NumberType, None, CallExpr(Id(test), []))"""
		self.assertTrue(TestChecker.test(input,expect,400))

