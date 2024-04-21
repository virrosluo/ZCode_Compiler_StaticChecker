import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):
    def test0(self):
        input = """func main(number b)
        begin
            string a[1,2] <- [["hello", "world"]]
            return a
        end
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test1(self):
        input = """func main(number b)
        begin
            return c
        end
        """
        expect = "Undeclared Identifier: c"
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
        expect = "Type Cannot Be Inferred: Return(CallExpr(Id(foo), []))"
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
        expect = "Type Cannot Be Inferred: Return(CallExpr(Id(foo), []))"
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
        expect = "Type Mismatch In Expression: BinaryOp(+, NumLit(10.0), StringLit(string))"
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
        expect = "Type Mismatch In Expression: BinaryOp(+, CallExpr(Id(foo), []), NumLit(10.0))"
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
        expect = "Type Mismatch In Statement: For(Id(i), CallExpr(Id(foo), []), CallExpr(Id(foo), []), Block([Return(BooleanLit(False))]))"
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
        expect = "Type Mismatch In Statement: If((CallExpr(Id(foo), []), CallStmt(Id(println), [Id(i)])), [], None)"
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
        expect = "Type Mismatch In Statement: CallStmt(Id(foo), [])"
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
        expect = "Undeclared Function: a"
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
        expect = ""
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
        expect = "Type Mismatch In Expression: ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0)), ArrayLit(NumLit(3.0)), ArrayLit(NumLit(4.0), NumLit(5.0)))"
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
        expect = "Type Mismatch In Expression: ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0)), ArrayLit(NumLit(3.0)), ArrayLit(NumLit(4.0), NumLit(5.0)))"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test15(self):
        input = """
        func main()
        begin
            number b[1,1] <- [[1,2], [3], [4,5]]
            number a <- b[2] + 10
        end
        """
        expect = "Type Mismatch In Expression: ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0)), ArrayLit(NumLit(3.0)), ArrayLit(NumLit(4.0), NumLit(5.0)))"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test16(self):
        input = """
        func main()
        begin
            number b[1] <- [[1,2], [3], [4,5]]
        end
        """
        expect = "Type Mismatch In Expression: ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0)), ArrayLit(NumLit(3.0)), ArrayLit(NumLit(4.0), NumLit(5.0)))"
        self.assertTrue(TestChecker.test(input, expect, 416))
        
    def test17(self):
        input = """
        func main()
        begin
            number y
            number x <- x + y
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 417))
        
    def test18(self):
        input = """
        func foo(number a)
        begin
            if (a = 1) 
                return 1
            else
                return 2
        end
        func main()
        begin
            foo(10)
        end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo), [NumLit(10.0)])"
        self.assertTrue(TestChecker.test(input, expect, 418))
        
    def test19(self):
        input = """
        func foo(number a)
        
        func foo(number a, number b)
        begin
            return "Hello World"
        end
        
        func main()
        begin
            foo()
        end
        """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 419))
        
    def test20(self):
        input = """
        number a
        
        func main()
        begin
            a()
        end
        """
        expect = "Undeclared Function: a"
        self.assertTrue(TestChecker.test(input, expect, 420))
    
    def test21(self):
        input = """
        func a(number b)
        
        func main()
        begin
            number b <- a(10) + 1
        end
        
        func a(number b)
        begin
            return "Hello World"
        end
        """
        expect = "Type Mismatch In Statement: Return(StringLit(Hello World))"
        self.assertTrue(TestChecker.test(input, expect, 421))
    
    def test22(self):
        input = """
        func a(number b)
        
        func main()
        begin
            number b <- a(10)
        end
        
        func a(number b)
        begin
            return "Hello World"
        end
        """
        expect = "Type Mismatch In Statement: Return(StringLit(Hello World))"
        self.assertTrue(TestChecker.test(input, expect, 422))
        
    def test23(self):
        input = """
        func a(number b)
        
        func a(number b)
        
        func a(number b)
        begin
            return 10
        end
        
        func main()
        begin
            number b <- a(10)
        end
        
        """
        expect = "Redeclared Function: a"
        self.assertTrue(TestChecker.test(input, expect, 423))
        
    def test24(self):
        input = """
        number a
        func a(number b)
        begin
            return 10
        end
        
        func main()
        begin
            number b <- a(10)
            number c <- a
        end
        
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 424))
    
    def test25(self):
        input = """
        dynamic c
        func a(number b)
        begin
            if (b = 1)
                return 2
            else
                return c
        end
        
        func main()
        begin
            number b <- a(10)
        end        
        """
        expect = "Type Cannot Be Inferred: Return(Id(c))"
        self.assertTrue(TestChecker.test(input, expect, 425))
        
    def test26(self):
        input = """        
        func main()
        begin
            dynamic a
            dynamic c
            for a until a >= 10 by c
            begin
                c <- "Hello World"
            end
        end        
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(c), StringLit(Hello World))"
        self.assertTrue(TestChecker.test(input, expect, 426))
        
    def test27(self):
        input = """        
        func main()
        begin
            dynamic a
            dynamic c
            string b <- "Hello World"
            for a until b >= 10 by c
            begin
            end
        end        
        """
        expect = "Type Mismatch In Expression: BinaryOp(>=, Id(b), NumLit(10.0))"
        self.assertTrue(TestChecker.test(input, expect, 427))
        
    def test28(self):
        input = """        
        func main()
        begin
            dynamic a
            dynamic c
            number b
            for a until b >= 10 by c
            begin
                a <- "String"
            end
        end        
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 428))
        
    def test29(self):
        input = """        
        func main()
        begin
            dynamic a
            dynamic c
            number b
            for a until b >= 10 by c
            begin
                string a <- "String"
            end
        end        
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 429))
        
    def test30(self):
        input = """
        func foo(number a, string b)
        begin
        end
        
        func main()
        begin
            dynamic a
            dynamic c
            foo(a, c)
            a <- 10
            c <- 10
        end        
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(c), NumLit(10.0))"
        self.assertTrue(TestChecker.test(input, expect, 430))
        
    def test31(self):
        input = """
        func foo(number a, string b)
        begin
        end
        
        func main()
        begin
            dynamic a
            dynamic c
            foo(a, c)
            a <- "String"
            c <- "String"
        end        
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 431))
        
    def test32(self):
        input = """
        func foo(number a, string b)
        begin
        end
        
        func t1()
        func t2()
        
        func main()
        begin
            foo(t1(), t2())
        end
        
        func t1()
            return "String"
            
        func t2()
            return "String"
        """
        expect = "Type Mismatch In Statement: Return(StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 432))
        
    def test33(self):
        input = """
        func foo(number a, string b)
        begin
        end
        
        func t1()
        func t2()
        
        func main()
        begin
            foo(t1(), t2())
        end
        
        func t1()
            return 10
            
        func t2()
            return 10
        """
        expect = "Type Mismatch In Statement: Return(NumLit(10.0))"
        self.assertTrue(TestChecker.test(input, expect, 433))
        
    def test34(self):
        input = """
        func foo(number a, string b)
        func t1()
        func t2()
        
        func main()
        begin
            number c <- foo(t1(), t2())
        end
        
        func t1()
            return 10
            
        func t2()
            return "String"
            
        func foo(number a, string b)
            return 10
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 434))
        
    def test35(self):
        input = """
        func foo(number a, string b)
        func t1()
        func t2()
        
        func main()
        begin
            number c <- foo(t1(), t2())
        end
        
        func t1()
            return 10
            
        func t2()
            return "String"
            
        func foo(number a, string b)
            return "String"
        """
        expect = "Type Mismatch In Statement: Return(StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 435))
        
    def test36(self):
        input = """
        number a[1,2] <- [[0,0]]
        func main()
        begin
            dynamic b
            number d
            number c <- a[b,d]
            b <- 10
            d <- "String"
        end
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(d), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 436))
        
    def test37(self):
        input = """
        number a[1,2] <- [[0,0]]
        func main()
        begin
            dynamic b <- a[0,1]
            b <- "String"
        end
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 437))
        
    def test38(self):
        input = """
        number a[1,2] <- [[0,0]]
        func main()
        begin
            dynamic b <- a[0,1]
            b <- 10
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 438))
        
    def test39(self):
        input = """
        func t1()
        func t2()
        number a[1,2] <- [[0,0]]
        func main()
        begin
            dynamic b <- a[t1(), t2()]
            b <- 10
        end
        
        func t1()
            return "t1"
        func t2()
            return "t2"
        """
        expect = "Type Mismatch In Statement: Return(StringLit(t1))"
        self.assertTrue(TestChecker.test(input, expect, 439))
        
    def test40(self):
        input = """
        func t1()
        func t2()
        number a[1,2] <- [[0,0]]
        func main()
        begin
            dynamic b <- a[t1(), t2()]
            b <- 10
        end
        
        func t1()
            return 1
        func t2()
            return "t2"
        """
        expect = "Type Mismatch In Statement: Return(StringLit(t2))"
        self.assertTrue(TestChecker.test(input, expect, 440))
        
    def test41(self):
        input = """
        number a[1,2]
        func main()
        begin
            dynamic b
            number d
            number c <- a[b,d]
            b <- "String"
            d <- "String"
        end
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 441))
        
    def test47(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            dynamic b <- [[0,0]]
            b <- "string"
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), StringLit(string))"
        self.assertTrue(TestChecker.test(input, expect, 447))
        
    def test42(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            b <- "string"
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), StringLit(string))"
        self.assertTrue(TestChecker.test(input, expect, 442))
        
    def test43(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            b <- [1,2,3]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), ArrayLit(NumLit(1.0), NumLit(2.0), NumLit(3.0)))"
        self.assertTrue(TestChecker.test(input, expect, 443))
        
    def test44(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            b <- [[1,2,3]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), ArrayLit(ArrayLit(NumLit(1.0), NumLit(2.0), NumLit(3.0))))"
        self.assertTrue(TestChecker.test(input, expect, 444))
        
    def test45(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            b <- [["hello", "world"]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b), ArrayLit(ArrayLit(StringLit(hello), StringLit(world))))"
        self.assertTrue(TestChecker.test(input, expect, 445))
        
    def test46(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            b <- [[1,2]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 446))
        
    def test48(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            if (b[0])
                dynamic c
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b), [NumLit(0.0)])"
        self.assertTrue(TestChecker.test(input, expect, 448))
        
    def test60(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            if (b[0,0,0])
                dynamic c
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b), [NumLit(0.0), NumLit(0.0), NumLit(0.0)])"
        self.assertTrue(TestChecker.test(input, expect, 460))
        
    def test61(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            if (b[0,0])
                dynamic c
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: If((ArrayCell(Id(b), [NumLit(0.0), NumLit(0.0)]), VarDecl(Id(c), None, dynamic, None)), [], None)"
        self.assertTrue(TestChecker.test(input, expect, 461))
        
    def test62(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            bool b[1,2] <- [[true, true]]
            if (b[0,0])
                dynamic c
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 462))
        
    def test49(self):
        input = """
        func t1()
        func t2()
        func main()
        begin
            number b[1,2] <- [[0,0]]
            if (b["hello",0])
                dynamic c
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b), [StringLit(hello), NumLit(0.0)])"
        self.assertTrue(TestChecker.test(input, expect, 449))
        
    def test50(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            number b[1,2] <- foo()
            dynamic c <- b[t1(), t2()]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 450))
        
    def test51(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            number b[1,2] <- foo()
            dynamic c <- b[t1(), t2()]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [1,2,3]
        """
        expect = "Type Mismatch In Statement: Return(ArrayLit(NumLit(1.0), NumLit(2.0), NumLit(3.0)))"
        self.assertTrue(TestChecker.test(input, expect, 451))
        
    def test52(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            number b[1,2] <- foo()
            dynamic c <- b[t1(), t2()]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [["String", "string"]]
        """
        expect = "Type Mismatch In Statement: Return(ArrayLit(ArrayLit(StringLit(String), StringLit(string))))"
        self.assertTrue(TestChecker.test(input, expect, 452))
        
    def test53(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            number b[1,2] <- foo()
            dynamic c <- b[t1(), t2()]
            c <- "String"
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(c), StringLit(String))"
        self.assertTrue(TestChecker.test(input, expect, 453))
        
    def test54(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            number b[1,2] <- foo()
            dynamic c <- b[t1(), t2()]
            c <- 5
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 454))
        
    def test55(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            dynamic c <- foo()[t1(), t2()]
            c <- "string"
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = "Type Cannot Be Inferred: VarDecl(Id(c), None, dynamic, ArrayCell(CallExpr(Id(foo), []), [CallExpr(Id(t1), []), CallExpr(Id(t2), [])]))"
        self.assertTrue(TestChecker.test(input, expect, 455))
        
    def test56(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            dynamic c <- foo()[t1(), t2()]
            c <- 5
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = "Type Cannot Be Inferred: VarDecl(Id(c), None, dynamic, ArrayCell(CallExpr(Id(foo), []), [CallExpr(Id(t1), []), CallExpr(Id(t2), [])]))"
        self.assertTrue(TestChecker.test(input, expect, 456))
        
    def test57(self):
        input = """
        func t1()
        func t2()
        func foo()
        func main()
        begin
            dynamic c
            c <- foo()
            c <- [["String", "string"]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        func foo()
            return [[1,2]]
        """
        expect = "Type Cannot Be Inferred: AssignStmt(Id(c), CallExpr(Id(foo), []))"
        self.assertTrue(TestChecker.test(input, expect, 457))
        
    def test58(self):
        input = """
        func t1()
        func t2()
        func foo()
            return [[1,2]]
        func main()
        begin
            dynamic c
            c <- foo()
            c <- [["String", "String"]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(c), ArrayLit(ArrayLit(StringLit(String), StringLit(String))))"
        self.assertTrue(TestChecker.test(input, expect, 458))
        
    def test59(self):
        input = """
        func t1()
        func t2()
        func foo()
            return [[1,2]]
        func main()
        begin
            dynamic c
            c <- foo()
            c <- [[1, 1]]
        end
        
        func t1()
            return 2
        func t2()
            return 2
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 459))
        
    def test63(self):
        input = """
        func main()
        begin
            number a[1,2] <- [1,2,3]
        end
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a), ArrayType([1.0, 2.0], NumberType), None, ArrayLit(NumLit(1.0), NumLit(2.0), NumLit(3.0)))"
        self.assertTrue(TestChecker.test(input, expect, 463))
        
    def test64(self):
        input = """
        func main()
        begin
            number a[1,2] <- [["String", "String"]]
        end
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a), ArrayType([1.0, 2.0], NumberType), None, ArrayLit(ArrayLit(StringLit(String), StringLit(String))))"
        self.assertTrue(TestChecker.test(input, expect, 464))
        
    def test65(self):
        input = """
        func main()
        begin
            number a[1,2] <- [[1,2]]
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 465))
        
    def test66(self):
            input = """
            func main()
                begin
                    dynamic num
                    bool arr <- num and (num > num)
                end
            """            
            expect = "Type Mismatch In Expression: BinaryOp(>, Id(num), Id(num))"
            self.assertTrue(TestChecker.test(input, expect, 466))

    def test67(self):
            input = """
            func main()
                begin
                    dynamic a
                    number b[1] <- [a]
                    a <- 10
                end
            """
            expect = ""
            self.assertTrue(TestChecker.test(input, expect, 467))
            
    def test68(self):
            input = """
            func main()
            begin
                dynamic a
                var b <- a
            end
            """
            expect = "Type Cannot Be Inferred: VarDecl(Id(b), None, var, Id(a))"
            self.assertTrue(TestChecker.test(input, expect, 468))
            
    def test69(self):
            input = """func test()
            begin
                dynamic a
                return a
            end 
            func main()
            begin
                test()
            end
            """
            expect = "Type Cannot Be Inferred: Return(Id(a))"
            self.assertTrue(TestChecker.test(input, expect, 469))
            
    def test70(self):
            input = """
            func main()
            begin
                dynamic c <- [1,2,3,4,5]
                number b[5] <- [1,2,3,4,5]
                dynamic d <- b
            end
            """
            expect = ""
            self.assertTrue(TestChecker.test(input, expect, 470))
            
    def test71(self):
        input = """
        func f(number x)
        
        func f(number y)
        begin
            return y
        end
        
        func main()
        begin
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 471))
        
    def test72(self):
        input = """
        number a
        
        func a()
        begin
            return
        end
        
        func main()
        begin
            a()
            number c <- a
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 472))
        
    def test73(self):
        input = """
        func foo()
        begin
            number a <- 10
            for a until a > 10 by 1
            begin
                number b <- 20
            end
            
            if (a = 1)
            begin
                number c <- 30
                return true
            end
            elif (a > 1)
                number e <- 20
            else
            begin
                number d <- 40
                return 1
            end
        end
        
        func main()
        begin
            bool a <- foo()
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 473))
        
    def test74(self):
        input = """
        func foo()
        begin
            number a <- 10
            for a until a > 10 by 1
            begin
                number b <- 20
            end
            
            if (a = 1)
            begin
                number c <- 30
            end
            elif (a > 1)
                number e <- 20
            else
            begin
                number d <- 40
            end
        end
        
        func main()
        begin
            bool a <- foo()
        end
        """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo), [])"
        self.assertTrue(TestChecker.test(input, expect, 474))
        
    def test75(self):
        input = """
        func foo()
        begin
            number a <- 10
            for a until a > 10 by 1
            begin
                number b <- 20
            end
            
            if (a = 1)
            begin
                number c <- 30
            end
            elif (a > 1)
                number e <- 20
            else
            begin
                number d <- 40
            end
        end
        
        func main()
        begin
            foo()
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 475))
        
    def test76(self):
        input = """
        number a
        
        func main()
        begin
            return 2
        end
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 476))
        
    def test77(self):
        input = """
        func a()
        begin
            return 1
        end
        
        func main()
        begin
            number b <- a
        end
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 477))
        
    def test78(self):
            input = """
    func main()
    begin
        number x
        begin
            number x <- (10 + x) * 2
        end
    end
    """
            expect = ""
            self.assertTrue(TestChecker.test(input, expect, 478))
            
    def test79(self):
        input = """
func foo() return 10
        
func main()
begin
    number x
    begin
        number a[3,3]
        number b <- a[foo() - 11, 3 < 4]
    end
end
"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(a), [BinaryOp(-, CallExpr(Id(foo), []), NumLit(11.0)), BinaryOp(<, NumLit(3.0), NumLit(4.0))])"
        self.assertTrue(TestChecker.test(input, expect, 479))
        
    def test80(self):
        input = """
        string a[2,2] <- [["string", "string1"],["hello","world"]]

        func main()
        begin
            dynamic i
            string arr <- "hello world"
            i <- arr[0,0]...arr[0,1]
        end
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(arr), [NumLit(0.0), NumLit(0.0)])"
        self.assertTrue(TestChecker.test(input, expect, 480))
        
    def test81(self):
        input = """
        func main()
        begin
        end
        func aaa(number a, bool b)
        begin
            number b
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 481))
        
    def test82(self):
        input = """
        func main()
        begin
            dynamic b
            number a[3] <- [b, "2", "three"]
        end
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a), ArrayType([3.0], NumberType), None, ArrayLit(Id(b), StringLit(2), StringLit(three)))"
        self.assertTrue(TestChecker.test(input, expect, 482))
        
    def test83(self):
            input = """
            func main()
                begin
                    dynamic a
                    number b[1] <- [a]
                    a <- "string"
                end
            """
            expect = "Type Mismatch In Statement: AssignStmt(Id(a), StringLit(string))"
            self.assertTrue(TestChecker.test(input, expect, 483))
            
    def test84(self):
        input = """
        func foo()
        func main()
        begin
            number a <- foo()
            return
        end
        
        func foo()
        begin
            dynamic a
            number b <- a + 1
            if (a < b)
                number c <- b
        end
        """
        
        expect = "Type Mismatch In Statement: None"
        self.assertTrue(TestChecker.test(input, expect, 484))
        
    def test85(self):
        input = """
        func test() 

        func main() begin
            bool a <- false and not (false and false)
        end
        """
        expect = "No Function Definition: test"
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test86(self):
        input = """
        func foo1(number a)
        begin
            return
        end
        func foo1(number a, number b)
        begin
            return
        end
        func main() begin 
            foo()
        end
        """
        expect = "Redeclared Function: foo1"
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test87(self):
        input = """
        func main() begin 
            number a
            for a until true by 1
            begin
                if (a > 10) break
                else continue
            end
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test88(self):
        input = """
        func sqr(number a)
            return a*a

        func sum(number arr[5])
        begin
            dynamic total <- 0
            dynamic a
            for a until a = 5 by 1
            begin
                total <- total + sqr(arr[a])
            end
            return total
        end

        func main() begin 
            writeBool(sum([1,2,3,4,5]) > 1000)
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test89(self):
        input = """
        func gcd(number a, number b)
        begin
            for b until b = 0 by 0
                a <- b
                b <- a % b
            return a
        end

        func main() begin 
            number a <- readNumber()
            number b <- readNumber()
            writeNumber(gcd(a,b))
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test90(self):
        input = """        
        func main() begin 
            string strArr[5] <- ["This", "Is", "A", "Hello", "World"]
            dynamic i
            string ans
            for i until i = 5 by 1
            begin
                ans <- ans + strArr[i]
            end
            writeString(ans)
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(+, Id(ans), ArrayCell(Id(strArr), [Id(i)]))"
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test91(self):
        input = """
        func foo(number a, bool b) begin
            return [[[1,2],[1,2],[1,2]]]
        end        

        func func1(number a, number b, number c)
        begin
            if (a + b = c)
                writeNumber(c)
            else writeNumber(a + b) 
        end

        func main() 
        begin
            number x <- 10
            number i <- 0
            for i until i > x by x-2
                if (i >= 1) break
                elif (x <= 1) continue
                elif (b[10,2+3] < foo(1,true)[1,2-2,3*4]) 
                    func1(1,2,3)
                else i <- i*10
        end
        """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test92(self):
        input = """
        func main(number a, number b) begin
            writeString("Hello World")
        end
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test93(self):
        input = """
        func main() begin
            number a[2, 3] <- [[1,2,3],[4,5,6]]
            for i until i >= 2 by 1 begin
                for j until j >= 3 by 1 begin
                    a[i, j] <- i + j
                end
            end
        end
        """
        expect = "Undeclared Identifier: i"
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test94(self):
        input = """
        number a
        func main() begin
            number b
            number arr[2] <- [a,b]
            writeNumber(arr[0])
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test95(self):
        input = """
        func foo(number a, number b)
        begin
            if (a > b) writeNumber(b-a)
            else writeNumber(a+b)
        end

        func main() begin
            number num1 <- readNumber()
            number num2 <- readNumber()
            foo(num1, num2)
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test96(self):
        input = """
        func foo(bool a, bool b, bool c)
        begin
            if (a and true) writeBool(a)
            elif (b or false) writeBool(b)
            elif (c and true) writeBool(c)
            else writeBool((a and b) and not c)
        end

        func main() begin
            bool a <- readBool()
            bool b <- readBool()
            bool c <- readBool()
            foo(a,b,c)
        end
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test97(self):
        input = """
        func foo(number a, number b, string c)
        begin
            rs <- ""
            for a until a = b by 1
            begin
                rs <- rs + c
            end
            return rs
        end

        func main() begin
            number a <- readNumber()
            number b <- readNumber()
            string c <- readString()
            writeString(foo(a,b,c))
        end
        """
        expect = "Undeclared Identifier: rs"
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test98(self):
        input = """
        func len(string a)
            return 10

        func merge(string arr[10])
        begin
            string ans <- ""
            dynamic i <- 0
            for i until i = 10 by 1
            begin
                ans <- ans...arr[i]
                if (len(ans) > 100)
                    break
            end
            return ans
        end

        func main() begin
            string arr[10]
            dynamic i <- 0
            for i until i = 10 by 1
                arr[i] <- readString()
            merge(arr)
        end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(merge), [Id(arr)])"
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test99(self):
        input = """
        func main() begin
            return "Hello World"
        end
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 499))
        
    def test100(self):
            input = """
    func main()
    begin
        dynamic a
        dynamic b
        number c[2] <- [3,4]
        number arr[2,2] <- [[a],c]
    end
    """
            expect = "Type Mismatch In Expression: ArrayLit(ArrayLit(Id(a)), Id(c))"
            self.assertTrue(TestChecker.test(input, expect, 500))