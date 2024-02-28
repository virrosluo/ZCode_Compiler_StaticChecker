# Generated from main/zcode/parser/ZCode.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from lexererr import *



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\67")
        buf.write("\u01ab\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3")
        buf.write("\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b")
        buf.write("\3\b\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13")
        buf.write("\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write("\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3")
        buf.write("\20\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21")
        buf.write("\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\23\5\23\u00db\n\23\3\24\3\24\3\24\3\25\3\25\3")
        buf.write("\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\32")
        buf.write("\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\36")
        buf.write("\3\36\3\36\3\37\3\37\3 \3 \3 \3!\3!\3\"\3\"\3\"\3#\3#")
        buf.write("\3#\3#\3$\3$\3$\3%\6%\u010c\n%\r%\16%\u010d\3%\7%\u0111")
        buf.write("\n%\f%\16%\u0114\13%\3&\3&\3\'\3\'\3(\3(\3)\3)\3*\3*\3")
        buf.write("+\3+\3+\3+\3+\3+\5+\u0126\n+\3+\3+\5+\u012a\n+\3,\6,\u012d")
        buf.write("\n,\r,\16,\u012e\3-\3-\7-\u0133\n-\f-\16-\u0136\13-\3")
        buf.write(".\3.\5.\u013a\n.\3.\6.\u013d\n.\r.\16.\u013e\3/\3/\3/")
        buf.write("\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61\3\61\3\61\3\62")
        buf.write("\3\62\3\62\3\63\6\63\u0153\n\63\r\63\16\63\u0154\3\63")
        buf.write("\3\63\3\64\3\64\3\64\3\64\7\64\u015d\n\64\f\64\16\64\u0160")
        buf.write("\13\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\65\5\65\u016a")
        buf.write("\n\65\7\65\u016c\n\65\f\65\16\65\u016f\13\65\3\65\3\65")
        buf.write("\3\66\3\66\3\66\3\66\3\66\3\66\5\66\u0179\n\66\7\66\u017b")
        buf.write("\n\66\f\66\16\66\u017e\13\66\3\66\3\66\3\66\3\67\3\67")
        buf.write("\3\67\3\67\3\67\3\67\5\67\u0189\n\67\7\67\u018b\n\67\f")
        buf.write("\67\16\67\u018e\13\67\3\67\3\67\3\67\5\67\u0193\n\67\3")
        buf.write("\67\3\67\38\38\38\38\58\u019b\n8\38\38\78\u019f\n8\f8")
        buf.write("\168\u01a2\138\38\38\38\38\38\39\39\39\4\u018c\u01a0\2")
        buf.write(":\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31")
        buf.write("\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O")
        buf.write(")Q*S+U,W\2Y\2[\2]-_.a/c\60e\61g\62i\63k\64m\65o\66q\67")
        buf.write("\3\2\r\5\2C\\aac|\6\2\62;C\\aac|\3\2\62;\3\2\60\60\4\2")
        buf.write("GGgg\4\2--//\5\2\n\13\16\16\"\"\4\2\f\f\17\17\7\2\f\f")
        buf.write("\17\17$$))^^\t\2))^^ddhhppttvv\3\2$$\2\u01c4\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2")
        buf.write("9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2")
        buf.write("\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3")
        buf.write("\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o")
        buf.write("\3\2\2\2\2q\3\2\2\2\3s\3\2\2\2\5z\3\2\2\2\7\177\3\2\2")
        buf.write("\2\t\u0086\3\2\2\2\13\u008d\3\2\2\2\r\u0091\3\2\2\2\17")
        buf.write("\u0099\3\2\2\2\21\u009e\3\2\2\2\23\u00a2\3\2\2\2\25\u00a8")
        buf.write("\3\2\2\2\27\u00ab\3\2\2\2\31\u00b1\3\2\2\2\33\u00ba\3")
        buf.write("\2\2\2\35\u00bd\3\2\2\2\37\u00c2\3\2\2\2!\u00c7\3\2\2")
        buf.write("\2#\u00cd\3\2\2\2%\u00da\3\2\2\2\'\u00dc\3\2\2\2)\u00df")
        buf.write("\3\2\2\2+\u00e1\3\2\2\2-\u00e3\3\2\2\2/\u00e5\3\2\2\2")
        buf.write("\61\u00e7\3\2\2\2\63\u00e9\3\2\2\2\65\u00ed\3\2\2\2\67")
        buf.write("\u00f1\3\2\2\29\u00f4\3\2\2\2;\u00f6\3\2\2\2=\u00f9\3")
        buf.write("\2\2\2?\u00fb\3\2\2\2A\u00fe\3\2\2\2C\u0100\3\2\2\2E\u0103")
        buf.write("\3\2\2\2G\u0107\3\2\2\2I\u010b\3\2\2\2K\u0115\3\2\2\2")
        buf.write("M\u0117\3\2\2\2O\u0119\3\2\2\2Q\u011b\3\2\2\2S\u011d\3")
        buf.write("\2\2\2U\u0129\3\2\2\2W\u012c\3\2\2\2Y\u0130\3\2\2\2[\u0137")
        buf.write("\3\2\2\2]\u0140\3\2\2\2_\u0146\3\2\2\2a\u0149\3\2\2\2")
        buf.write("c\u014e\3\2\2\2e\u0152\3\2\2\2g\u0158\3\2\2\2i\u0163\3")
        buf.write("\2\2\2k\u0172\3\2\2\2m\u0182\3\2\2\2o\u0196\3\2\2\2q\u01a8")
        buf.write("\3\2\2\2st\7p\2\2tu\7w\2\2uv\7o\2\2vw\7d\2\2wx\7g\2\2")
        buf.write("xy\7t\2\2y\4\3\2\2\2z{\7d\2\2{|\7q\2\2|}\7q\2\2}~\7n\2")
        buf.write("\2~\6\3\2\2\2\177\u0080\7u\2\2\u0080\u0081\7v\2\2\u0081")
        buf.write("\u0082\7t\2\2\u0082\u0083\7k\2\2\u0083\u0084\7p\2\2\u0084")
        buf.write("\u0085\7i\2\2\u0085\b\3\2\2\2\u0086\u0087\7t\2\2\u0087")
        buf.write("\u0088\7g\2\2\u0088\u0089\7v\2\2\u0089\u008a\7w\2\2\u008a")
        buf.write("\u008b\7t\2\2\u008b\u008c\7p\2\2\u008c\n\3\2\2\2\u008d")
        buf.write("\u008e\7x\2\2\u008e\u008f\7c\2\2\u008f\u0090\7t\2\2\u0090")
        buf.write("\f\3\2\2\2\u0091\u0092\7f\2\2\u0092\u0093\7{\2\2\u0093")
        buf.write("\u0094\7p\2\2\u0094\u0095\7c\2\2\u0095\u0096\7o\2\2\u0096")
        buf.write("\u0097\7k\2\2\u0097\u0098\7e\2\2\u0098\16\3\2\2\2\u0099")
        buf.write("\u009a\7h\2\2\u009a\u009b\7w\2\2\u009b\u009c\7p\2\2\u009c")
        buf.write("\u009d\7e\2\2\u009d\20\3\2\2\2\u009e\u009f\7h\2\2\u009f")
        buf.write("\u00a0\7q\2\2\u00a0\u00a1\7t\2\2\u00a1\22\3\2\2\2\u00a2")
        buf.write("\u00a3\7w\2\2\u00a3\u00a4\7p\2\2\u00a4\u00a5\7v\2\2\u00a5")
        buf.write("\u00a6\7k\2\2\u00a6\u00a7\7n\2\2\u00a7\24\3\2\2\2\u00a8")
        buf.write("\u00a9\7d\2\2\u00a9\u00aa\7{\2\2\u00aa\26\3\2\2\2\u00ab")
        buf.write("\u00ac\7d\2\2\u00ac\u00ad\7t\2\2\u00ad\u00ae\7g\2\2\u00ae")
        buf.write("\u00af\7c\2\2\u00af\u00b0\7m\2\2\u00b0\30\3\2\2\2\u00b1")
        buf.write("\u00b2\7e\2\2\u00b2\u00b3\7q\2\2\u00b3\u00b4\7p\2\2\u00b4")
        buf.write("\u00b5\7v\2\2\u00b5\u00b6\7k\2\2\u00b6\u00b7\7p\2\2\u00b7")
        buf.write("\u00b8\7w\2\2\u00b8\u00b9\7g\2\2\u00b9\32\3\2\2\2\u00ba")
        buf.write("\u00bb\7k\2\2\u00bb\u00bc\7h\2\2\u00bc\34\3\2\2\2\u00bd")
        buf.write("\u00be\7g\2\2\u00be\u00bf\7n\2\2\u00bf\u00c0\7u\2\2\u00c0")
        buf.write("\u00c1\7g\2\2\u00c1\36\3\2\2\2\u00c2\u00c3\7g\2\2\u00c3")
        buf.write("\u00c4\7n\2\2\u00c4\u00c5\7k\2\2\u00c5\u00c6\7h\2\2\u00c6")
        buf.write(" \3\2\2\2\u00c7\u00c8\7d\2\2\u00c8\u00c9\7g\2\2\u00c9")
        buf.write("\u00ca\7i\2\2\u00ca\u00cb\7k\2\2\u00cb\u00cc\7p\2\2\u00cc")
        buf.write("\"\3\2\2\2\u00cd\u00ce\7g\2\2\u00ce\u00cf\7p\2\2\u00cf")
        buf.write("\u00d0\7f\2\2\u00d0$\3\2\2\2\u00d1\u00d2\7v\2\2\u00d2")
        buf.write("\u00d3\7t\2\2\u00d3\u00d4\7w\2\2\u00d4\u00db\7g\2\2\u00d5")
        buf.write("\u00d6\7h\2\2\u00d6\u00d7\7c\2\2\u00d7\u00d8\7n\2\2\u00d8")
        buf.write("\u00d9\7u\2\2\u00d9\u00db\7g\2\2\u00da\u00d1\3\2\2\2\u00da")
        buf.write("\u00d5\3\2\2\2\u00db&\3\2\2\2\u00dc\u00dd\7>\2\2\u00dd")
        buf.write("\u00de\7/\2\2\u00de(\3\2\2\2\u00df\u00e0\7-\2\2\u00e0")
        buf.write("*\3\2\2\2\u00e1\u00e2\7/\2\2\u00e2,\3\2\2\2\u00e3\u00e4")
        buf.write("\7,\2\2\u00e4.\3\2\2\2\u00e5\u00e6\7\61\2\2\u00e6\60\3")
        buf.write("\2\2\2\u00e7\u00e8\7\'\2\2\u00e8\62\3\2\2\2\u00e9\u00ea")
        buf.write("\7p\2\2\u00ea\u00eb\7q\2\2\u00eb\u00ec\7v\2\2\u00ec\64")
        buf.write("\3\2\2\2\u00ed\u00ee\7c\2\2\u00ee\u00ef\7p\2\2\u00ef\u00f0")
        buf.write("\7f\2\2\u00f0\66\3\2\2\2\u00f1\u00f2\7q\2\2\u00f2\u00f3")
        buf.write("\7t\2\2\u00f38\3\2\2\2\u00f4\u00f5\7?\2\2\u00f5:\3\2\2")
        buf.write("\2\u00f6\u00f7\7#\2\2\u00f7\u00f8\7?\2\2\u00f8<\3\2\2")
        buf.write("\2\u00f9\u00fa\7>\2\2\u00fa>\3\2\2\2\u00fb\u00fc\7>\2")
        buf.write("\2\u00fc\u00fd\7?\2\2\u00fd@\3\2\2\2\u00fe\u00ff\7@\2")
        buf.write("\2\u00ffB\3\2\2\2\u0100\u0101\7@\2\2\u0101\u0102\7?\2")
        buf.write("\2\u0102D\3\2\2\2\u0103\u0104\7\60\2\2\u0104\u0105\7\60")
        buf.write("\2\2\u0105\u0106\7\60\2\2\u0106F\3\2\2\2\u0107\u0108\7")
        buf.write("?\2\2\u0108\u0109\7?\2\2\u0109H\3\2\2\2\u010a\u010c\t")
        buf.write("\2\2\2\u010b\u010a\3\2\2\2\u010c\u010d\3\2\2\2\u010d\u010b")
        buf.write("\3\2\2\2\u010d\u010e\3\2\2\2\u010e\u0112\3\2\2\2\u010f")
        buf.write("\u0111\t\3\2\2\u0110\u010f\3\2\2\2\u0111\u0114\3\2\2\2")
        buf.write("\u0112\u0110\3\2\2\2\u0112\u0113\3\2\2\2\u0113J\3\2\2")
        buf.write("\2\u0114\u0112\3\2\2\2\u0115\u0116\7*\2\2\u0116L\3\2\2")
        buf.write("\2\u0117\u0118\7+\2\2\u0118N\3\2\2\2\u0119\u011a\7]\2")
        buf.write("\2\u011aP\3\2\2\2\u011b\u011c\7_\2\2\u011cR\3\2\2\2\u011d")
        buf.write("\u011e\7.\2\2\u011eT\3\2\2\2\u011f\u012a\5W,\2\u0120\u0121")
        buf.write("\5W,\2\u0121\u0122\5Y-\2\u0122\u012a\3\2\2\2\u0123\u0125")
        buf.write("\5W,\2\u0124\u0126\5Y-\2\u0125\u0124\3\2\2\2\u0125\u0126")
        buf.write("\3\2\2\2\u0126\u0127\3\2\2\2\u0127\u0128\5[.\2\u0128\u012a")
        buf.write("\3\2\2\2\u0129\u011f\3\2\2\2\u0129\u0120\3\2\2\2\u0129")
        buf.write("\u0123\3\2\2\2\u012aV\3\2\2\2\u012b\u012d\t\4\2\2\u012c")
        buf.write("\u012b\3\2\2\2\u012d\u012e\3\2\2\2\u012e\u012c\3\2\2\2")
        buf.write("\u012e\u012f\3\2\2\2\u012fX\3\2\2\2\u0130\u0134\t\5\2")
        buf.write("\2\u0131\u0133\t\4\2\2\u0132\u0131\3\2\2\2\u0133\u0136")
        buf.write("\3\2\2\2\u0134\u0132\3\2\2\2\u0134\u0135\3\2\2\2\u0135")
        buf.write("Z\3\2\2\2\u0136\u0134\3\2\2\2\u0137\u0139\t\6\2\2\u0138")
        buf.write("\u013a\t\7\2\2\u0139\u0138\3\2\2\2\u0139\u013a\3\2\2\2")
        buf.write("\u013a\u013c\3\2\2\2\u013b\u013d\t\4\2\2\u013c\u013b\3")
        buf.write("\2\2\2\u013d\u013e\3\2\2\2\u013e\u013c\3\2\2\2\u013e\u013f")
        buf.write("\3\2\2\2\u013f\\\3\2\2\2\u0140\u0141\7\17\2\2\u0141\u0142")
        buf.write("\7\17\2\2\u0142\u0143\7\f\2\2\u0143\u0144\3\2\2\2\u0144")
        buf.write("\u0145\b/\2\2\u0145^\3\2\2\2\u0146\u0147\7\17\2\2\u0147")
        buf.write("\u0148\b\60\3\2\u0148`\3\2\2\2\u0149\u014a\7\17\2\2\u014a")
        buf.write("\u014b\7\f\2\2\u014b\u014c\3\2\2\2\u014c\u014d\b\61\4")
        buf.write("\2\u014db\3\2\2\2\u014e\u014f\7\f\2\2\u014f\u0150\b\62")
        buf.write("\5\2\u0150d\3\2\2\2\u0151\u0153\t\b\2\2\u0152\u0151\3")
        buf.write("\2\2\2\u0153\u0154\3\2\2\2\u0154\u0152\3\2\2\2\u0154\u0155")
        buf.write("\3\2\2\2\u0155\u0156\3\2\2\2\u0156\u0157\b\63\6\2\u0157")
        buf.write("f\3\2\2\2\u0158\u0159\7%\2\2\u0159\u015a\7%\2\2\u015a")
        buf.write("\u015e\3\2\2\2\u015b\u015d\n\t\2\2\u015c\u015b\3\2\2\2")
        buf.write("\u015d\u0160\3\2\2\2\u015e\u015c\3\2\2\2\u015e\u015f\3")
        buf.write("\2\2\2\u015f\u0161\3\2\2\2\u0160\u015e\3\2\2\2\u0161\u0162")
        buf.write("\b\64\6\2\u0162h\3\2\2\2\u0163\u016d\7$\2\2\u0164\u016c")
        buf.write("\n\n\2\2\u0165\u0166\7^\2\2\u0166\u016c\t\13\2\2\u0167")
        buf.write("\u0169\7)\2\2\u0168\u016a\t\f\2\2\u0169\u0168\3\2\2\2")
        buf.write("\u0169\u016a\3\2\2\2\u016a\u016c\3\2\2\2\u016b\u0164\3")
        buf.write("\2\2\2\u016b\u0165\3\2\2\2\u016b\u0167\3\2\2\2\u016c\u016f")
        buf.write("\3\2\2\2\u016d\u016b\3\2\2\2\u016d\u016e\3\2\2\2\u016e")
        buf.write("\u0170\3\2\2\2\u016f\u016d\3\2\2\2\u0170\u0171\b\65\7")
        buf.write("\2\u0171j\3\2\2\2\u0172\u017c\7$\2\2\u0173\u017b\n\n\2")
        buf.write("\2\u0174\u0175\7^\2\2\u0175\u017b\t\13\2\2\u0176\u0178")
        buf.write("\7)\2\2\u0177\u0179\t\f\2\2\u0178\u0177\3\2\2\2\u0178")
        buf.write("\u0179\3\2\2\2\u0179\u017b\3\2\2\2\u017a\u0173\3\2\2\2")
        buf.write("\u017a\u0174\3\2\2\2\u017a\u0176\3\2\2\2\u017b\u017e\3")
        buf.write("\2\2\2\u017c\u017a\3\2\2\2\u017c\u017d\3\2\2\2\u017d\u017f")
        buf.write("\3\2\2\2\u017e\u017c\3\2\2\2\u017f\u0180\7$\2\2\u0180")
        buf.write("\u0181\b\66\b\2\u0181l\3\2\2\2\u0182\u018c\7$\2\2\u0183")
        buf.write("\u018b\n\n\2\2\u0184\u0185\7^\2\2\u0185\u018b\t\13\2\2")
        buf.write("\u0186\u0188\7)\2\2\u0187\u0189\t\f\2\2\u0188\u0187\3")
        buf.write("\2\2\2\u0188\u0189\3\2\2\2\u0189\u018b\3\2\2\2\u018a\u0183")
        buf.write("\3\2\2\2\u018a\u0184\3\2\2\2\u018a\u0186\3\2\2\2\u018b")
        buf.write("\u018e\3\2\2\2\u018c\u018d\3\2\2\2\u018c\u018a\3\2\2\2")
        buf.write("\u018d\u0192\3\2\2\2\u018e\u018c\3\2\2\2\u018f\u0190\7")
        buf.write("\17\2\2\u0190\u0193\7\f\2\2\u0191\u0193\t\t\2\2\u0192")
        buf.write("\u018f\3\2\2\2\u0192\u0191\3\2\2\2\u0193\u0194\3\2\2\2")
        buf.write("\u0194\u0195\b\67\t\2\u0195n\3\2\2\2\u0196\u01a0\7$\2")
        buf.write("\2\u0197\u019f\n\n\2\2\u0198\u019a\7)\2\2\u0199\u019b")
        buf.write("\t\f\2\2\u019a\u0199\3\2\2\2\u019a\u019b\3\2\2\2\u019b")
        buf.write("\u019f\3\2\2\2\u019c\u019d\7^\2\2\u019d\u019f\t\13\2\2")
        buf.write("\u019e\u0197\3\2\2\2\u019e\u0198\3\2\2\2\u019e\u019c\3")
        buf.write("\2\2\2\u019f\u01a2\3\2\2\2\u01a0\u01a1\3\2\2\2\u01a0\u019e")
        buf.write("\3\2\2\2\u01a1\u01a3\3\2\2\2\u01a2\u01a0\3\2\2\2\u01a3")
        buf.write("\u01a4\7^\2\2\u01a4\u01a5\n\13\2\2\u01a5\u01a6\3\2\2\2")
        buf.write("\u01a6\u01a7\b8\n\2\u01a7p\3\2\2\2\u01a8\u01a9\13\2\2")
        buf.write("\2\u01a9\u01aa\b9\13\2\u01aar\3\2\2\2\33\2\u00da\u010d")
        buf.write("\u0112\u0125\u0129\u012e\u0134\u0139\u013e\u0154\u015e")
        buf.write("\u0169\u016b\u016d\u0178\u017a\u017c\u0188\u018a\u018c")
        buf.write("\u0192\u019a\u019e\u01a0\f\3/\2\3\60\3\3\61\4\3\62\5\b")
        buf.write("\2\2\3\65\6\3\66\7\3\67\b\38\t\39\n")
        return buf.getvalue()


class ZCodeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    NUM_KEYWORD = 1
    BOOL_KEYWORD = 2
    STRING_KEYWORD = 3
    RETURN_KEYWORD = 4
    VAR_KEYWORD = 5
    DYNAMIC_KEYWORD = 6
    FUNC_KEYWORD = 7
    FOR_KEYWORD = 8
    UNTIL_KEYWORD = 9
    BY_KEYWORD = 10
    BREAK_KEYWORD = 11
    CONTINUE_KEYWORD = 12
    IF_KEYWORD = 13
    ELSE_KEYWORD = 14
    ELIF_KEYWORD = 15
    BEGIN_KEYWORD = 16
    END_KEYWORD = 17
    BOOL_LIT = 18
    ASSIGN_OP = 19
    ADD_OP = 20
    SUB_OP = 21
    MUL_OP = 22
    DIV_OP = 23
    MOD_OP = 24
    NOT_OP = 25
    AND_OP = 26
    OR_OP = 27
    EQUAL_OP = 28
    INEQUAL_OP = 29
    LESS_OP = 30
    LESSEQUAL_OP = 31
    LARGE_OP = 32
    LARGEEQUAL_OP = 33
    CONCAT_OP = 34
    EQUAL_STR_OP = 35
    ID = 36
    LEFT_PARENTHESIS = 37
    RIGHT_PARENTHESIS = 38
    LEFT_BRACKET = 39
    RIGHT_BRACKET = 40
    SEPARATOR_KEYWORD = 41
    REAL_LIT = 42
    NL1 = 43
    NL2 = 44
    NL3 = 45
    NL4 = 46
    WS = 47
    COMMENT_LINE = 48
    UNCLOSE_STRING = 49
    STRING_LIT = 50
    NEWLINE_STRING = 51
    ILLEGAL_ESCAPE = 52
    ERROR_TOKEN = 53

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'number'", "'bool'", "'string'", "'return'", "'var'", "'dynamic'", 
            "'func'", "'for'", "'until'", "'by'", "'break'", "'continue'", 
            "'if'", "'else'", "'elif'", "'begin'", "'end'", "'<-'", "'+'", 
            "'-'", "'*'", "'/'", "'%'", "'not'", "'and'", "'or'", "'='", 
            "'!='", "'<'", "'<='", "'>'", "'>='", "'...'", "'=='", "'('", 
            "')'", "'['", "']'", "','", "'\r\r\n'", "'\r'", "'\r\n'", "'\n'" ]

    symbolicNames = [ "<INVALID>",
            "NUM_KEYWORD", "BOOL_KEYWORD", "STRING_KEYWORD", "RETURN_KEYWORD", 
            "VAR_KEYWORD", "DYNAMIC_KEYWORD", "FUNC_KEYWORD", "FOR_KEYWORD", 
            "UNTIL_KEYWORD", "BY_KEYWORD", "BREAK_KEYWORD", "CONTINUE_KEYWORD", 
            "IF_KEYWORD", "ELSE_KEYWORD", "ELIF_KEYWORD", "BEGIN_KEYWORD", 
            "END_KEYWORD", "BOOL_LIT", "ASSIGN_OP", "ADD_OP", "SUB_OP", 
            "MUL_OP", "DIV_OP", "MOD_OP", "NOT_OP", "AND_OP", "OR_OP", "EQUAL_OP", 
            "INEQUAL_OP", "LESS_OP", "LESSEQUAL_OP", "LARGE_OP", "LARGEEQUAL_OP", 
            "CONCAT_OP", "EQUAL_STR_OP", "ID", "LEFT_PARENTHESIS", "RIGHT_PARENTHESIS", 
            "LEFT_BRACKET", "RIGHT_BRACKET", "SEPARATOR_KEYWORD", "REAL_LIT", 
            "NL1", "NL2", "NL3", "NL4", "WS", "COMMENT_LINE", "UNCLOSE_STRING", 
            "STRING_LIT", "NEWLINE_STRING", "ILLEGAL_ESCAPE", "ERROR_TOKEN" ]

    ruleNames = [ "NUM_KEYWORD", "BOOL_KEYWORD", "STRING_KEYWORD", "RETURN_KEYWORD", 
                  "VAR_KEYWORD", "DYNAMIC_KEYWORD", "FUNC_KEYWORD", "FOR_KEYWORD", 
                  "UNTIL_KEYWORD", "BY_KEYWORD", "BREAK_KEYWORD", "CONTINUE_KEYWORD", 
                  "IF_KEYWORD", "ELSE_KEYWORD", "ELIF_KEYWORD", "BEGIN_KEYWORD", 
                  "END_KEYWORD", "BOOL_LIT", "ASSIGN_OP", "ADD_OP", "SUB_OP", 
                  "MUL_OP", "DIV_OP", "MOD_OP", "NOT_OP", "AND_OP", "OR_OP", 
                  "EQUAL_OP", "INEQUAL_OP", "LESS_OP", "LESSEQUAL_OP", "LARGE_OP", 
                  "LARGEEQUAL_OP", "CONCAT_OP", "EQUAL_STR_OP", "ID", "LEFT_PARENTHESIS", 
                  "RIGHT_PARENTHESIS", "LEFT_BRACKET", "RIGHT_BRACKET", 
                  "SEPARATOR_KEYWORD", "REAL_LIT", "INTPART", "DECPART", 
                  "EXPPART", "NL1", "NL2", "NL3", "NL4", "WS", "COMMENT_LINE", 
                  "UNCLOSE_STRING", "STRING_LIT", "NEWLINE_STRING", "ILLEGAL_ESCAPE", 
                  "ERROR_TOKEN" ]

    grammarFileName = "ZCode.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[45] = self.NL1_action 
            actions[46] = self.NL2_action 
            actions[47] = self.NL3_action 
            actions[48] = self.NL4_action 
            actions[51] = self.UNCLOSE_STRING_action 
            actions[52] = self.STRING_LIT_action 
            actions[53] = self.NEWLINE_STRING_action 
            actions[54] = self.ILLEGAL_ESCAPE_action 
            actions[55] = self.ERROR_TOKEN_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NL1_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
            self.text = "\n"
     

    def NL2_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.text = "\n"
     

    def NL3_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.text = "\n"
     

    def NL4_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.text = "\n"
     

    def UNCLOSE_STRING_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            raise UncloseString(self.text[1:])
     

    def STRING_LIT_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.text = self.text[1:-1]
     

    def NEWLINE_STRING_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            raise UncloseString(self.text[1:].replace('\r', '').replace('\n',''))
     

    def ILLEGAL_ESCAPE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 7:
            raise IllegalEscape(self.text[1:])
     

    def ERROR_TOKEN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 8:
            raise ErrorToken(self.text)
     


