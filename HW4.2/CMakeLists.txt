cmake_minimum_required(VERSION 3.12)
project(untitled)

set(CMAKE_CXX_STANDARD 17)

add_executable(untitled ASTNode.h Comparision.h Function.h Grammar.cpp Grammar.h Main.cpp Parser.cpp Parser.h Scanner.cpp Scanner.h SymbolTable.h Token.cpp Token.h Util.cpp Util.h Variable.h)