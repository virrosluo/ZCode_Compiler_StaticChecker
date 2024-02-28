import unittest
from TestUtils import TestChecker
from AST import *


class CheckerSuite(unittest.TestCase):
    def test1(self):
        input = """func main(number b)
        begin
            string a[1,2] <- [["hello", "world"]]
            return a
        end
        """
        expect = "successful"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test2(self):
        input = """func main(number b)
        begin
            return c
        end
        """
        expect = "Undeclared Variable: c)"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test2(self):
        input = """
        func foo()

        func main(number b)
        begin
            return foo()
        end

        func foo()
        """
        expect = "function being redeclared"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test3(self):
        input = """
        number foo <- 10
        func foo()

        func main(number b)
        begin
            return foo()
        end

        func foo()
        """
        expect = "Declare the function name with the same identifier name"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test4(self):
        input = """
        number foo <- 10 + "string"

        func foo()
        func main(number b)
        begin
            return foo()
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(+, NumLit(10.0), StringLit(string)))"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test5(self):
        input = """
        func foo()
        begin
            return [1,2,3,4]
        end
        func main(number b)
        begin
            return foo() + 10
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(+, CallExpr(Id(foo), []), NumLit(10.0)))"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test6(self):
        input = """
        func foo()
        begin
            return true
        end
        func main()
        begin
            number i <- 0
            for i until foo() by foo()
            begin
                return false
            end
        end

        bool test <- main() and true
        """
        expect = "successful"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test7(self):
        input = """
        func foo()
        begin
            return 1
        end
        func main()
        begin
            number i <- 0
            for i until foo() by foo()
            begin
                return false
            end
        end

        bool test <- main() and true
        """
        expect = "Type Mismatch In Statement: For(Id(i), CallExpr(Id(foo), []), CallExpr(Id(foo), []), Block([Return(BooleanLit(False))]))"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test8(self):
        input = """func foo()
        begin
            return 1
        end
        
        func println(number i)
        begin
            return
        end

        func main()
        begin
            number i <- 0
            if (foo()) println(i)
            break
        end
        """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test9(self):
        input = """func foo()
        begin
            return 1
        end

        func main()
        begin
            foo()
        end
        """
        expect = "Type Mismatch In Expression: CallStmt(Id(foo), [])"
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test10(self):
        input = """func foo()
        begin
        end

        func main()
        begin
            number a<- foo()
        end
        """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo), [])"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test11(self):
        input = """func foo()
        begin
            return 1
        end

        func main()
        begin
            number a <- foo()
            number b <- a()
        end
        """
        expect = "Cannot call a non-function type id"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test12(self):
        input = """func foo()
        begin
            return [1,2,3,4]
        end

        func main()
        begin
            number a <- foo()[2] + 10
        end
        """
        expect = "successful"
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test13(self):
        input = """func foo()
        begin
            return [[1,2], [3], [4,5]]
        end

        func main()
        begin
            number a <- foo()[2] + 10
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(+, ArrayCell(CallExpr(Id(foo), []), [NumLit(2.0)]), NumLit(10.0)))"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test14(self):
        input = """func foo()
        begin
            return [[1,2], [3], [4,5]]
        end

        func main()
        begin
            number a <- foo()[2,3] + 10
        end
        """
        expect = "successful"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test15(self):
        input = """func foo()
        begin
            return [[1,2], [3], [4,5]]
        end

        func main()
        begin
            number b[1,1] <- [[1,2], [3], [4,5]]
            number a <- b[2] + 10
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(+, ArrayCell(Id(b), [NumLit(2.0)]), NumLit(10.0)))"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test16(self):
        input = """
        func main()
        begin
            number b[1] <- [[1,2], [3], [4,5]]
        end
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(b), ArrayType([1.0], NumberType), None, ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0)), ArrayLit(NumLit(3.0)), ArrayLit(NumLit(4.0), NumLit(5.0))))"
        self.assertTrue(TestChecker.test(input, expect, 416))