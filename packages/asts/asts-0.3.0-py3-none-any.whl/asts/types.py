from .asts import AST

class TerminalSymbol(AST):
    pass

class CAST(AST):
    pass

class CNewline(CAST, TerminalSymbol, AST):
    pass

class CLogicalNot(CAST, TerminalSymbol, AST):
    pass

class CNotEqual(CAST, TerminalSymbol, AST):
    pass

class CDoubleQuote(CAST, TerminalSymbol, AST):
    pass

class CMacroDefine(CAST, TerminalSymbol, AST):
    pass

class CMacroElif(CAST, TerminalSymbol, AST):
    pass

class CMacroElse(CAST, TerminalSymbol, AST):
    pass

class CMacroEndIf(CAST, TerminalSymbol, AST):
    pass

class CMacroIf(CAST, TerminalSymbol, AST):
    pass

class CMacroIfDefined(CAST, TerminalSymbol, AST):
    pass

class CMacroIfNotDefined(CAST, TerminalSymbol, AST):
    pass

class CMacroInclude(CAST, TerminalSymbol, AST):
    pass

class CModulo(CAST, TerminalSymbol, AST):
    pass

class CModuleAssign(CAST, TerminalSymbol, AST):
    pass

class CBitwiseAnd(CAST, TerminalSymbol, AST):
    pass

class CLogicalAnd(CAST, TerminalSymbol, AST):
    pass

class CBitwiseAndAssign(CAST, TerminalSymbol, AST):
    pass

class CSingleQuote(CAST, TerminalSymbol, AST):
    pass

class COpenParenthesis(CAST, TerminalSymbol, AST):
    pass

class CCloseParenthesis(CAST, TerminalSymbol, AST):
    pass

class CMultiply(CAST, TerminalSymbol, AST):
    pass

class CMultiplyAssign(CAST, TerminalSymbol, AST):
    pass

class CAdd(CAST, TerminalSymbol, AST):
    pass

class CIncrement(CAST, TerminalSymbol, AST):
    pass

class CAddAssign(CAST, TerminalSymbol, AST):
    pass

class CComma(CAST, TerminalSymbol, AST):
    pass

class CSubtract(CAST, TerminalSymbol, AST):
    pass

class CDecrement(CAST, TerminalSymbol, AST):
    pass

class CAttributeSubtract(CAST, TerminalSymbol, AST):
    pass

class CBased(CAST, TerminalSymbol, AST):
    pass

class CCdecl(CAST, TerminalSymbol, AST):
    pass

class CClrcall(CAST, TerminalSymbol, AST):
    pass

class CDeclspec(CAST, TerminalSymbol, AST):
    pass

class CFastcall(CAST, TerminalSymbol, AST):
    pass

class CStdcall(CAST, TerminalSymbol, AST):
    pass

class CThiscall(CAST, TerminalSymbol, AST):
    pass

class CUnderscoreUnaligned(CAST, TerminalSymbol, AST):
    pass

class CVectorcall(CAST, TerminalSymbol, AST):
    pass

class CSubtractAssign(CAST, TerminalSymbol, AST):
    pass

class CArrow(CAST, TerminalSymbol, AST):
    pass

class CAbstractDeclarator(CAST, AST):
    pass

class CAtomic(CAST, TerminalSymbol, AST):
    pass

class CDeclarator(CAST, AST):
    pass

class ExpressionAST(AST):
    pass

class CExpression(CAST, ExpressionAST, AST):
    pass

class CFieldDeclarator(CAST, AST):
    pass

class StatementAST(AST):
    pass

class CStatement(CAST, StatementAST, AST):
    pass

class CTypeDeclarator(CAST, AST):
    pass

class CTypeSpecifier(CAST, AST):
    pass

class CUnaligned(CAST, TerminalSymbol, AST):
    pass

class CDot(CAST, TerminalSymbol, AST):
    pass

class CEllipsis(CAST, TerminalSymbol, AST):
    pass

class CDivide(CAST, TerminalSymbol, AST):
    pass

class CDivideAssign(CAST, TerminalSymbol, AST):
    pass

class CColon(CAST, TerminalSymbol, AST):
    pass

class CSemicolon(CAST, TerminalSymbol, AST):
    pass

class CLessThan(CAST, TerminalSymbol, AST):
    pass

class CBitshiftLeft(CAST, TerminalSymbol, AST):
    pass

class CBitshiftLeftAssign(CAST, TerminalSymbol, AST):
    pass

class CLessThanOrEqual(CAST, TerminalSymbol, AST):
    pass

class CAssign(CAST, TerminalSymbol, AST):
    pass

class CEqual(CAST, TerminalSymbol, AST):
    pass

class CGreaterThan(CAST, TerminalSymbol, AST):
    pass

class CGreaterThanOrEqual(CAST, TerminalSymbol, AST):
    pass

class CBitshiftRight(CAST, TerminalSymbol, AST):
    pass

class CBitshiftRightAssign(CAST, TerminalSymbol, AST):
    pass

class CQuestion(CAST, TerminalSymbol, AST):
    pass

class CAbstractArrayDeclarator(CAbstractDeclarator, AST):
    pass

class CAbstractFunctionDeclarator(CAbstractDeclarator, AST):
    pass

class CAbstractParenthesizedDeclarator(CAbstractDeclarator, AST):
    pass

class CAbstractPointerDeclarator(CAbstractDeclarator, AST):
    pass

class CXXArgumentList(AST):
    pass

class CArgumentList(CAST, CXXArgumentList, AST):
    pass

class CArgumentList0(CArgumentList, AST):
    pass

class CArgumentList1(CArgumentList, AST):
    pass

class CXXArrayDeclarator(AST):
    pass

class CArrayDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXArrayDeclarator, AST):
    pass

class CArrayDeclarator0(CArrayDeclarator, AST):
    pass

class CArrayDeclarator1(CArrayDeclarator, AST):
    pass

class VariableDeclarationAST(AST):
    pass

class CXXAssignmentExpression(AST):
    pass

class CAssignmentExpression(CExpression, CXXAssignmentExpression, VariableDeclarationAST, AST):
    pass

class CAttributeSpecifier(CAST, AST):
    pass

class CAuto(CAST, TerminalSymbol, AST):
    pass

class BinaryAST(ExpressionAST, AST):
    pass

class CXXBinaryExpression(AST):
    pass

class CBinaryExpression(CExpression, CXXBinaryExpression, BinaryAST, AST):
    pass

class CBitfieldClause(CAST, AST):
    pass

class CBreak(CAST, TerminalSymbol, AST):
    pass

class CXXBreakStatement(AST):
    pass

class CBreakStatement(CStatement, CXXBreakStatement, AST):
    pass

class CallAST(ExpressionAST, AST):
    pass

class CXXCallExpression(AST):
    pass

class CCallExpression(CExpression, CXXCallExpression, CallAST, AST):
    pass

class CCallExpression0(CCallExpression, AST):
    pass

class CCallExpression1(CCallExpression, AST):
    pass

class CCase(CAST, TerminalSymbol, AST):
    pass

class ControlFlowAST(AST):
    pass

class CXXCaseStatement(AST):
    pass

class CCaseStatement(CStatement, CXXCaseStatement, ControlFlowAST, AST):
    pass

class CCaseStatement0(CCaseStatement, AST):
    pass

class CCaseStatement1(CCaseStatement, AST):
    pass

class CCastExpression(CExpression, AST):
    pass

class CXXCharLiteral(AST):
    pass

class CCharLiteral(CExpression, CXXCharLiteral, AST):
    pass

class CCommaExpression(CAST, AST):
    pass

class CommentAST(AST):
    pass

class CXXComment(AST):
    pass

class CComment(CAST, CXXComment, CommentAST, AST):
    pass

class CCompoundLiteralExpression(CExpression, AST):
    pass

class CompoundAST(AST):
    pass

class CXXCompoundStatement(AST):
    pass

class CCompoundStatement(CStatement, CXXCompoundStatement, CompoundAST, AST):
    pass

class CConcatenatedString(CExpression, AST):
    pass

class CConditionalExpression(CExpression, AST):
    pass

class CConst(CAST, TerminalSymbol, AST):
    pass

class CContinue(CAST, TerminalSymbol, AST):
    pass

class CXXContinueStatement(AST):
    pass

class CContinueStatement(CStatement, CXXContinueStatement, AST):
    pass

class CXXDeclaration(AST):
    pass

class CDeclaration(CAST, CXXDeclaration, StatementAST, AST):
    pass

class CDeclarationList(CAST, AST):
    pass

class CDefault(CAST, TerminalSymbol, AST):
    pass

class CDefined(CAST, TerminalSymbol, AST):
    pass

class CDo(CAST, TerminalSymbol, AST):
    pass

class LoopAST(ControlFlowAST, AST):
    pass

class CXXDoStatement(AST):
    pass

class CDoStatement(CStatement, CXXDoStatement, LoopAST, AST):
    pass

class CElse(CAST, TerminalSymbol, AST):
    pass

class CEnum(CAST, TerminalSymbol, AST):
    pass

class DefinitionAST(AST):
    pass

class CXXEnumSpecifier(AST):
    pass

class CEnumSpecifier(CTypeSpecifier, CXXEnumSpecifier, DefinitionAST, AST):
    pass

class CEnumSpecifier0(CEnumSpecifier, AST):
    pass

class CEnumSpecifier1(CEnumSpecifier, AST):
    pass

class CXXEnumerator(AST):
    pass

class CEnumerator(CAST, CXXEnumerator, AST):
    pass

class CEnumerator0(CEnumerator, AST):
    pass

class CEnumerator1(CEnumerator, AST):
    pass

class CEnumeratorList(CAST, AST):
    pass

class CEnumeratorList0(CEnumeratorList, AST):
    pass

class CEnumeratorList1(CEnumeratorList, AST):
    pass

class CEnumeratorList2(CEnumeratorList, AST):
    pass

class CEnumeratorList3(CEnumeratorList, AST):
    pass

class ParseErrorAST(AST):
    pass

class CXXError(AST):
    pass

class CError(CAST, CXXError, ParseErrorAST, AST):
    pass

class CEscapeSequence(CAST, AST):
    pass

class ExpressionStatementAST(AST):
    pass

class CXXExpressionStatement(AST):
    pass

class CExpressionStatement(CStatement, CXXExpressionStatement, ExpressionStatementAST, AST):
    pass

class CExpressionStatement0(CExpressionStatement, AST):
    pass

class CExpressionStatement1(CExpressionStatement, AST):
    pass

class CExtern(CAST, TerminalSymbol, AST):
    pass

class LiteralAST(AST):
    pass

class BooleanAST(LiteralAST, AST):
    pass

class BooleanFalseAST(BooleanAST, AST):
    pass

class CFalse(CExpression, BooleanFalseAST, AST):
    pass

class CXXFieldDeclaration(AST):
    pass

class CFieldDeclaration(CAST, CXXFieldDeclaration, DefinitionAST, AST):
    pass

class CFieldDeclaration0(CFieldDeclaration, AST):
    pass

class CFieldDeclaration1(CFieldDeclaration, AST):
    pass

class CFieldDeclaration2(CFieldDeclaration, AST):
    pass

class CFieldDeclaration3(CFieldDeclaration, AST):
    pass

class CFieldDeclarationList(CAST, AST):
    pass

class CFieldDesignator(CAST, AST):
    pass

class FieldAST(AST):
    pass

class CXXFieldExpression(AST):
    pass

class CFieldExpression(CExpression, CXXFieldExpression, FieldAST, AST):
    pass

class CXXFieldIdentifier(AST):
    pass

class CFieldIdentifier(CFieldDeclarator, CXXFieldIdentifier, AST):
    pass

class CFor(CAST, TerminalSymbol, AST):
    pass

class CXXForStatement(AST):
    pass

class CForStatement(CStatement, CXXForStatement, LoopAST, AST):
    pass

class CForStatement0(CForStatement, AST):
    pass

class CForStatement1(CForStatement, AST):
    pass

class CForStatement2(CForStatement, AST):
    pass

class CForStatement3(CForStatement, AST):
    pass

class CXXFunctionDeclarator(AST):
    pass

class CFunctionDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXFunctionDeclarator, AST):
    pass

class CFunctionDeclarator0(CFunctionDeclarator, AST):
    pass

class CFunctionDeclarator1(CFunctionDeclarator, AST):
    pass

class FunctionAST(AST):
    pass

class CXXFunctionDefinition(AST):
    pass

class CFunctionDefinition(CAST, CXXFunctionDefinition, FunctionAST, StatementAST, AST):
    pass

class CFunctionDefinition0(CFunctionDefinition, AST):
    pass

class CFunctionDefinition1(CFunctionDefinition, AST):
    pass

class CGoto(CAST, TerminalSymbol, AST):
    pass

class GotoAST(StatementAST, AST):
    pass

class CGotoStatement(CStatement, GotoAST, AST):
    pass

class IdentifierAST(AST):
    pass

class CXXIdentifier(AST):
    pass

class CIdentifier(CDeclarator, CExpression, CXXIdentifier, IdentifierAST, AST):
    pass

class CIf(CAST, TerminalSymbol, AST):
    pass

class ConditionalAST(AST):
    pass

class IfAST(ControlFlowAST, ConditionalAST, AST):
    pass

class CXXIfStatement(AST):
    pass

class CIfStatement(CStatement, CXXIfStatement, IfAST, AST):
    pass

class CIfStatement0(CIfStatement, AST):
    pass

class CIfStatement1(CIfStatement, AST):
    pass

class CXXInitDeclarator(AST):
    pass

class CInitDeclarator(CAST, CXXInitDeclarator, VariableDeclarationAST, AST):
    pass

class CInitializerList(CAST, AST):
    pass

class CInitializerList0(CInitializerList, AST):
    pass

class CInitializerList1(CInitializerList, AST):
    pass

class CInitializerList2(CInitializerList, AST):
    pass

class CInitializerList3(CInitializerList, AST):
    pass

class CXXInitializerPair(AST):
    pass

class CInitializerPair(CAST, CXXInitializerPair, AST):
    pass

class CInline(CAST, TerminalSymbol, AST):
    pass

class TextFragment(AST):
    pass

class InnerWhitespace(TextFragment, AST):
    pass

class CInnerWhitespace(CAST, InnerWhitespace, AST):
    pass

class CWcharDoubleQuote(CAST, TerminalSymbol, AST):
    pass

class CWcharSingleQuote(CAST, TerminalSymbol, AST):
    pass

class CLabeledStatement(CStatement, AST):
    pass

class CLabeledStatement0(CLabeledStatement, AST):
    pass

class CLabeledStatement1(CLabeledStatement, AST):
    pass

class CLinkageSpecification(CAST, AST):
    pass

class CLong(CAST, TerminalSymbol, AST):
    pass

class CMacroTypeSpecifier(CTypeSpecifier, AST):
    pass

class CMsBasedModifier(CAST, AST):
    pass

class CMsCallModifier(CAST, AST):
    pass

class CMsDeclspecModifier(CAST, AST):
    pass

class CMsPointerModifier(CAST, AST):
    pass

class CMsRestrictModifier(CAST, AST):
    pass

class CMsSignedPtrModifier(CAST, AST):
    pass

class CMsUnalignedPtrModifier(CAST, AST):
    pass

class CMsUnsignedPtrModifier(CAST, AST):
    pass

class CNull(CExpression, AST):
    pass

class NumberAST(LiteralAST, AST):
    pass

class CXXNumberLiteral(AST):
    pass

class CNumberLiteral(CExpression, CXXNumberLiteral, NumberAST, AST):
    pass

class CXXParameterDeclaration(AST):
    pass

class CParameterDeclaration(CAST, CXXParameterDeclaration, AST):
    pass

class CParameterDeclaration0(CParameterDeclaration, AST):
    pass

class CParameterDeclaration1(CParameterDeclaration, AST):
    pass

class CParameterList(CAST, AST):
    pass

class CParameterList0(CParameterList, AST):
    pass

class CParameterList1(CParameterList, AST):
    pass

class CXXParenthesizedDeclarator(AST):
    pass

class CParenthesizedDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXParenthesizedDeclarator, AST):
    pass

class CParenthesizedDeclarator0(CParenthesizedDeclarator, AST):
    pass

class CParenthesizedDeclarator1(CParenthesizedDeclarator, AST):
    pass

class ParenthesizedExpressionAST(AST):
    pass

class CXXParenthesizedExpression(AST):
    pass

class CParenthesizedExpression(CExpression, CXXParenthesizedExpression, ParenthesizedExpressionAST, AST):
    pass

class CParenthesizedExpression0(CParenthesizedExpression, AST):
    pass

class CParenthesizedExpression1(CParenthesizedExpression, AST):
    pass

class CXXPointerDeclarator(AST):
    pass

class CPointerDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXPointerDeclarator, AST):
    pass

class CPointerDeclarator0(CPointerDeclarator, AST):
    pass

class CPointerDeclarator1(CPointerDeclarator, AST):
    pass

class CXXPointerExpression(AST):
    pass

class CPointerExpression(CExpression, CXXPointerExpression, AST):
    pass

class CXXPreprocArg(AST):
    pass

class CPreprocArg(CAST, CXXPreprocArg, AST):
    pass

class CPreprocCall(CAST, AST):
    pass

class CXXPreprocDef(AST):
    pass

class CPreprocDef(CAST, CXXPreprocDef, DefinitionAST, AST):
    pass

class CPreprocDefined(CAST, AST):
    pass

class CPreprocDefined0(CPreprocDefined, AST):
    pass

class CPreprocDefined1(CPreprocDefined, AST):
    pass

class CPreprocDirective(CAST, AST):
    pass

class CXXPreprocElif(AST):
    pass

class CPreprocElif(CAST, CXXPreprocElif, AST):
    pass

class CPreprocElif0(CPreprocElif, AST):
    pass

class CPreprocElif1(CPreprocElif, AST):
    pass

class CXXPreprocElse(AST):
    pass

class CPreprocElse(CAST, CXXPreprocElse, AST):
    pass

class CPreprocElse0(CPreprocElse, AST):
    pass

class CPreprocElse1(CPreprocElse, AST):
    pass

class CXXPreprocFunctionDef(AST):
    pass

class CPreprocFunctionDef(CAST, CXXPreprocFunctionDef, DefinitionAST, AST):
    pass

class CPreprocIf(CAST, AST):
    pass

class CPreprocIf0(CPreprocIf, AST):
    pass

class CPreprocIf1(CPreprocIf, AST):
    pass

class CPreprocIfdef(CAST, AST):
    pass

class CPreprocIfdef0(CPreprocIfdef, AST):
    pass

class CPreprocIfdef1(CPreprocIfdef, AST):
    pass

class CXXPreprocInclude(AST):
    pass

class CPreprocInclude(CAST, CXXPreprocInclude, AST):
    pass

class CXXPreprocParams(AST):
    pass

class CPreprocParams(CAST, CXXPreprocParams, AST):
    pass

class CPreprocParams0(CPreprocParams, AST):
    pass

class CPreprocParams1(CPreprocParams, AST):
    pass

class CPreprocParams2(CPreprocParams, AST):
    pass

class CXXPrimitiveType(AST):
    pass

class CPrimitiveType(CTypeSpecifier, CXXPrimitiveType, AST):
    pass

class CRegister(CAST, TerminalSymbol, AST):
    pass

class CRestrict(CAST, TerminalSymbol, AST):
    pass

class CReturn(CAST, TerminalSymbol, AST):
    pass

class ReturnAST(StatementAST, AST):
    pass

class CXXReturnStatement(AST):
    pass

class CReturnStatement(CStatement, CXXReturnStatement, ReturnAST, AST):
    pass

class CReturnStatement0(CReturnStatement, AST):
    pass

class CReturnStatement1(CReturnStatement, AST):
    pass

class CShort(CAST, TerminalSymbol, AST):
    pass

class CSigned(CAST, TerminalSymbol, AST):
    pass

class CSizedTypeSpecifier(CTypeSpecifier, AST):
    pass

class CSizeof(CAST, TerminalSymbol, AST):
    pass

class CSizeofExpression(CExpression, AST):
    pass

class CSizeofExpression0(CSizeofExpression, AST):
    pass

class CSizeofExpression1(CSizeofExpression, AST):
    pass

class SourceTextFragment(AST):
    pass

class CSourceTextFragment(CAST, SourceTextFragment, AST):
    pass

class CStatementIdentifier(CAST, AST):
    pass

class CStatic(CAST, TerminalSymbol, AST):
    pass

class CStorageClassSpecifier(CAST, AST):
    pass

class StringAST(LiteralAST, AST):
    pass

class CXXStringLiteral(AST):
    pass

class CStringLiteral(CExpression, CXXStringLiteral, StringAST, AST):
    pass

class CStruct(CAST, TerminalSymbol, AST):
    pass

class CXXStructSpecifier(AST):
    pass

class CStructSpecifier(CTypeSpecifier, CXXStructSpecifier, DefinitionAST, AST):
    pass

class CStructSpecifier0(CStructSpecifier, AST):
    pass

class CStructSpecifier1(CStructSpecifier, AST):
    pass

class CStructSpecifier2(CStructSpecifier, AST):
    pass

class CStructSpecifier3(CStructSpecifier, AST):
    pass

class CStructSpecifier4(CStructSpecifier, AST):
    pass

class CStructSpecifier5(CStructSpecifier, AST):
    pass

class CSubscriptDesignator(CAST, AST):
    pass

class SubscriptAST(AST):
    pass

class CXXSubscriptExpression(AST):
    pass

class CSubscriptExpression(CExpression, CXXSubscriptExpression, SubscriptAST, AST):
    pass

class CSwitch(CAST, TerminalSymbol, AST):
    pass

class CXXSwitchStatement(AST):
    pass

class CSwitchStatement(CStatement, CXXSwitchStatement, ControlFlowAST, AST):
    pass

class CSystemLibString(CAST, AST):
    pass

class RootAST(AST):
    pass

class CTranslationUnit(CAST, RootAST, AST):
    pass

class BooleanTrueAST(BooleanAST, AST):
    pass

class CTrue(CExpression, BooleanTrueAST, AST):
    pass

class CXXTypeDefinition(AST):
    pass

class CXXTypeIdentifier(AST):
    pass

class CTypeDefinition(CAST, CXXTypeIdentifier, CXXTypeDefinition, DefinitionAST, AST):
    pass

class CTypeDescriptor(CAST, AST):
    pass

class CTypeIdentifier(CTypeDeclarator, CTypeSpecifier, AST):
    pass

class CTypeQualifier(CAST, AST):
    pass

class CTypedef(CAST, TerminalSymbol, AST):
    pass

class CUnicodeDoubleQuote(CAST, TerminalSymbol, AST):
    pass

class CUnsignedTerminalDoubleQuote(CAST, TerminalSymbol, AST):
    pass

class CUnicodeSingleQuote(CAST, TerminalSymbol, AST):
    pass

class CUnsignedTerminalSingleQuote(CAST, TerminalSymbol, AST):
    pass

class CUnsigned8bitTerminalDoubleQuote(CAST, TerminalSymbol, AST):
    pass

class CUnsigned8bitTerminalSingleQuote(CAST, TerminalSymbol, AST):
    pass

class UnaryAST(ExpressionAST, AST):
    pass

class CXXUnaryExpression(AST):
    pass

class CUnaryExpression(CExpression, CXXUnaryExpression, UnaryAST, AST):
    pass

class CUnion(CAST, TerminalSymbol, AST):
    pass

class CXXUnionSpecifier(AST):
    pass

class CUnionSpecifier(CTypeSpecifier, CXXUnionSpecifier, DefinitionAST, AST):
    pass

class CUnionSpecifier0(CUnionSpecifier, AST):
    pass

class CUnionSpecifier1(CUnionSpecifier, AST):
    pass

class CUnionSpecifier2(CUnionSpecifier, AST):
    pass

class CUnionSpecifier3(CUnionSpecifier, AST):
    pass

class CUnsigned(CAST, TerminalSymbol, AST):
    pass

class CXXUpdateExpression(AST):
    pass

class CUpdateExpression(CExpression, CXXUpdateExpression, AST):
    pass

class CUpdateExpressionPostfix(CUpdateExpression, AST):
    pass

class CUpdateExpressionPrefix(CUpdateExpression, AST):
    pass

class CVariadicDeclaration(CParameterDeclaration, CIdentifier, AST):
    pass

class CVolatile(CAST, TerminalSymbol, AST):
    pass

class CWhile(CAST, TerminalSymbol, AST):
    pass

class WhileAST(ControlFlowAST, ConditionalAST, AST):
    pass

class CXXWhileStatement(AST):
    pass

class CWhileStatement(CStatement, CXXWhileStatement, LoopAST, WhileAST, AST):
    pass

class COpenBracket(CAST, TerminalSymbol, AST):
    pass

class CCloseBracket(CAST, TerminalSymbol, AST):
    pass

class CBitwiseXor(CAST, TerminalSymbol, AST):
    pass

class CBitwiseXorAssign(CAST, TerminalSymbol, AST):
    pass

class COpenBrace(CAST, TerminalSymbol, AST):
    pass

class CBitwiseOr(CAST, TerminalSymbol, AST):
    pass

class CBitwiseOrAssign(CAST, TerminalSymbol, AST):
    pass

class CLogicalOr(CAST, TerminalSymbol, AST):
    pass

class CCloseBrace(CAST, TerminalSymbol, AST):
    pass

class CBitwiseNot(CAST, TerminalSymbol, AST):
    pass

class CPPAST(AST):
    pass

class CPPNewline(CPPAST, TerminalSymbol, AST):
    pass

class CPPLogicalNot(CPPAST, TerminalSymbol, AST):
    pass

class CPPNotEqual(CPPAST, TerminalSymbol, AST):
    pass

class CPPDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroDefine(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroElif(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroElse(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroEndIf(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroIf(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroIfDefined(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroIfNotDefined(CPPAST, TerminalSymbol, AST):
    pass

class CPPMacroInclude(CPPAST, TerminalSymbol, AST):
    pass

class CPPModulo(CPPAST, TerminalSymbol, AST):
    pass

class CPPModuleAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseAnd(CPPAST, TerminalSymbol, AST):
    pass

class CPPLogicalAnd(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseAndAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPSingleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPOpenParenthesis(CPPAST, TerminalSymbol, AST):
    pass

class CPPCloseParenthesis(CPPAST, TerminalSymbol, AST):
    pass

class CPPMultiply(CPPAST, TerminalSymbol, AST):
    pass

class CPPMultiplyAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPAdd(CPPAST, TerminalSymbol, AST):
    pass

class CPPIncrement(CPPAST, TerminalSymbol, AST):
    pass

class CPPAddAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPComma(CPPAST, TerminalSymbol, AST):
    pass

class CPPSubtract(CPPAST, TerminalSymbol, AST):
    pass

class CPPDecrement(CPPAST, TerminalSymbol, AST):
    pass

class CPPAttributeSubtract(CPPAST, TerminalSymbol, AST):
    pass

class CPPBased(CPPAST, TerminalSymbol, AST):
    pass

class CPPCdecl(CPPAST, TerminalSymbol, AST):
    pass

class CPPClrcall(CPPAST, TerminalSymbol, AST):
    pass

class CPPDeclspec(CPPAST, TerminalSymbol, AST):
    pass

class CPPFastcall(CPPAST, TerminalSymbol, AST):
    pass

class CPPStdcall(CPPAST, TerminalSymbol, AST):
    pass

class CPPThiscall(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnderscoreUnaligned(CPPAST, TerminalSymbol, AST):
    pass

class CPPVectorcall(CPPAST, TerminalSymbol, AST):
    pass

class CPPSubtractAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPArrow(CPPAST, TerminalSymbol, AST):
    pass

class CPPAbstractDeclarator(CPPAST, AST):
    pass

class CPPAtomic(CPPAST, TerminalSymbol, AST):
    pass

class CPPDeclarator(CPPAST, AST):
    pass

class CPPExpression(CPPAST, AST):
    pass

class CPPFieldDeclarator(CPPAST, AST):
    pass

class CPPStatement(CPPAST, StatementAST, AST):
    pass

class CPPTypeDeclarator(CPPAST, AST):
    pass

class CPPTypeSpecifier(CPPAST, AST):
    pass

class CPPUnaligned(CPPAST, TerminalSymbol, AST):
    pass

class CPPDot(CPPAST, TerminalSymbol, AST):
    pass

class CPPEllipsis(CPPAST, TerminalSymbol, AST):
    pass

class CPPDivide(CPPAST, TerminalSymbol, AST):
    pass

class CPPDivideAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPColon(CPPAST, TerminalSymbol, AST):
    pass

class CPPScopeResolution(CPPAST, TerminalSymbol, AST):
    pass

class CPPSemicolon(CPPAST, TerminalSymbol, AST):
    pass

class CPPLessThan(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitshiftLeft(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitshiftLeftAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPLessThanOrEqual(CPPAST, TerminalSymbol, AST):
    pass

class CPPAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPEqual(CPPAST, TerminalSymbol, AST):
    pass

class CPPGreaterThan(CPPAST, TerminalSymbol, AST):
    pass

class CPPGreaterThanOrEqual(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitshiftRight(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitshiftRightAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPQuestion(CPPAST, TerminalSymbol, AST):
    pass

class CPPAbstractArrayDeclarator(CPPAbstractDeclarator, AST):
    pass

class CPPAbstractFunctionDeclarator(CPPAbstractDeclarator, AST):
    pass

class CPPAbstractFunctionDeclarator0(CPPAbstractFunctionDeclarator, AST):
    pass

class CPPAbstractFunctionDeclarator1(CPPAbstractFunctionDeclarator, AST):
    pass

class CPPAbstractParenthesizedDeclarator(CPPAbstractDeclarator, AST):
    pass

class CPPAbstractPointerDeclarator(CPPAbstractDeclarator, AST):
    pass

class CPPAbstractReferenceDeclarator(CPPAbstractDeclarator, AST):
    pass

class CPPAbstractReferenceDeclarator0(CPPAbstractReferenceDeclarator, AST):
    pass

class CPPAbstractReferenceDeclarator1(CPPAbstractReferenceDeclarator, AST):
    pass

class CPPAccessSpecifier(CPPAST, AST):
    pass

class CPPAliasDeclaration(CPPAST, AST):
    pass

class CPPArgumentList(CPPAST, CXXArgumentList, AST):
    pass

class CPPArgumentList0(CPPArgumentList, AST):
    pass

class CPPArgumentList1(CPPArgumentList, AST):
    pass

class CPPArrayDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXArrayDeclarator, AST):
    pass

class CPPArrayDeclarator0(CPPArrayDeclarator, AST):
    pass

class CPPArrayDeclarator1(CPPArrayDeclarator, AST):
    pass

class CPPAssignmentExpression(CPPExpression, CXXAssignmentExpression, VariableDeclarationAST, AST):
    pass

class CPPAttribute(CPPAST, AST):
    pass

class CPPAttributeSpecifier(CPPAST, AST):
    pass

class CPPAuto(CPPTypeSpecifier, AST):
    pass

class CPPBaseClassClause(CPPAST, AST):
    pass

class CPPBaseClassClause0(CPPBaseClassClause, AST):
    pass

class CPPBaseClassClause1(CPPBaseClassClause, AST):
    pass

class CPPBaseClassClause2(CPPBaseClassClause, AST):
    pass

class CPPBaseClassClause3(CPPBaseClassClause, AST):
    pass

class CPPBinaryExpression(CPPExpression, CXXBinaryExpression, BinaryAST, AST):
    pass

class CPPBitfieldClause(CPPAST, AST):
    pass

class CPPBreak(CPPAST, TerminalSymbol, AST):
    pass

class CPPBreakStatement(CPPStatement, CXXBreakStatement, AST):
    pass

class CPPCallExpression(CPPExpression, CXXCallExpression, CallAST, AST):
    pass

class CPPCallExpression0(CPPCallExpression, AST):
    pass

class CPPCallExpression1(CPPCallExpression, AST):
    pass

class CPPCase(CPPAST, TerminalSymbol, AST):
    pass

class CPPCaseStatement(CPPStatement, CXXCaseStatement, AST):
    pass

class CPPCaseStatement0(CPPCaseStatement, AST):
    pass

class CPPCaseStatement1(CPPCaseStatement, AST):
    pass

class CPPCastExpression(CPPExpression, AST):
    pass

class CPPCatch(CPPAST, TerminalSymbol, AST):
    pass

class CatchAST(StatementAST, AST):
    pass

class CPPCatchClause(CPPAST, CatchAST, AST):
    pass

class CharAST(LiteralAST, AST):
    pass

class CPPCharLiteral(CPPExpression, CXXCharLiteral, CharAST, AST):
    pass

class CPPClass(CPPAST, TerminalSymbol, AST):
    pass

class CPPClassSpecifier(CPPTypeSpecifier, AST):
    pass

class CPPClassSpecifier0(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier1(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier10(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier11(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier12(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier13(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier14(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier15(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier16(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier17(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier2(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier3(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier4(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier5(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier6(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier7(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier8(CPPClassSpecifier, AST):
    pass

class CPPClassSpecifier9(CPPClassSpecifier, AST):
    pass

class CPPCommaExpression(CPPAST, AST):
    pass

class CPPComment(CPPAST, CXXComment, CommentAST, AST):
    pass

class CPPCompoundLiteralExpression(CPPExpression, AST):
    pass

class CPPCompoundLiteralExpression0(CPPCompoundLiteralExpression, AST):
    pass

class CPPCompoundLiteralExpression1(CPPCompoundLiteralExpression, AST):
    pass

class CPPCompoundStatement(CPPStatement, CXXCompoundStatement, CompoundAST, AST):
    pass

class CPPConcatenatedString(CPPExpression, AST):
    pass

class CXXConditionClause(AST):
    pass

class CPPConditionClause(CPPAST, CXXConditionClause, AST):
    pass

class CPPConditionClause0(CPPConditionClause, AST):
    pass

class CPPConditionClause1(CPPConditionClause, AST):
    pass

class CPPConditionalExpression(CPPExpression, AST):
    pass

class CPPConst(CPPAST, TerminalSymbol, AST):
    pass

class CPPConstexpr(CPPAST, TerminalSymbol, AST):
    pass

class CPPContinue(CPPAST, TerminalSymbol, AST):
    pass

class CPPContinueStatement(CPPStatement, CXXContinueStatement, AST):
    pass

class CPPDeclaration(CPPAST, CXXDeclaration, StatementAST, AST):
    pass

class CPPDeclaration0(CPPDeclaration, AST):
    pass

class CPPDeclaration1(CPPDeclaration, AST):
    pass

class CPPDeclarationList(CPPAST, AST):
    pass

class CPPDecltype(CPPTypeSpecifier, AST):
    pass

class CPPDecltypeTerminal(CPPAST, TerminalSymbol, AST):
    pass

class CPPDefault(CPPAST, TerminalSymbol, AST):
    pass

class CPPDefaultMethodClause(CPPAST, AST):
    pass

class CPPDefined(CPPAST, TerminalSymbol, AST):
    pass

class CPPDelete(CPPAST, TerminalSymbol, AST):
    pass

class CPPDeleteExpression(CPPExpression, AST):
    pass

class CPPDeleteExpression0(CPPDeleteExpression, AST):
    pass

class CPPDeleteExpression1(CPPDeleteExpression, AST):
    pass

class CPPDeleteMethodClause(CPPAST, AST):
    pass

class CPPDependentType(CPPTypeSpecifier, AST):
    pass

class CPPDestructorName(CPPDeclarator, AST):
    pass

class CPPDo(CPPAST, TerminalSymbol, AST):
    pass

class CPPDoStatement(CPPStatement, CXXDoStatement, LoopAST, AST):
    pass

class CPPElse(CPPAST, TerminalSymbol, AST):
    pass

class CPPEnum(CPPAST, TerminalSymbol, AST):
    pass

class CPPEnumSpecifier(CPPTypeSpecifier, CXXEnumSpecifier, DefinitionAST, AST):
    pass

class CPPEnumSpecifier0(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier1(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier2(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier3(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier4(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier5(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier6(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier7(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier8(CPPEnumSpecifier, AST):
    pass

class CPPEnumSpecifier9(CPPEnumSpecifier, AST):
    pass

class CPPEnumerator(CPPAST, CXXEnumerator, AST):
    pass

class CPPEnumerator0(CPPEnumerator, AST):
    pass

class CPPEnumerator1(CPPEnumerator, AST):
    pass

class CPPEnumeratorList(CPPAST, AST):
    pass

class CPPEnumeratorList0(CPPEnumeratorList, AST):
    pass

class CPPEnumeratorList1(CPPEnumeratorList, AST):
    pass

class CPPEnumeratorList2(CPPEnumeratorList, AST):
    pass

class CPPEnumeratorList3(CPPEnumeratorList, AST):
    pass

class CPPError(CPPAST, CXXError, ParseErrorAST, AST):
    pass

class CPPEscapeSequence(CPPAST, AST):
    pass

class CPPExplicit(CPPAST, TerminalSymbol, AST):
    pass

class CPPExplicitFunctionSpecifier(CPPAST, AST):
    pass

class CPPExplicitFunctionSpecifier0(CPPExplicitFunctionSpecifier, AST):
    pass

class CPPExplicitFunctionSpecifier1(CPPExplicitFunctionSpecifier, AST):
    pass

class CPPExpressionStatement(CPPStatement, CXXExpressionStatement, ExpressionStatementAST, AST):
    pass

class CPPExpressionStatement0(CPPExpressionStatement, AST):
    pass

class CPPExpressionStatement1(CPPExpressionStatement, AST):
    pass

class CPPExtern(CPPAST, TerminalSymbol, AST):
    pass

class CPPFalse(CPPExpression, BooleanFalseAST, AST):
    pass

class CPPFieldDeclaration(CPPAST, CXXFieldDeclaration, DefinitionAST, AST):
    pass

class CPPFieldDeclaration0(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration1(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration10(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration11(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration12(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration13(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration14(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration15(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration2(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration3(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration4(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration5(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration6(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration7(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration8(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclaration9(CPPFieldDeclaration, AST):
    pass

class CPPFieldDeclarationList(CPPAST, AST):
    pass

class CPPFieldDesignator(CPPAST, AST):
    pass

class CPPFieldExpression(CPPExpression, CXXFieldExpression, FieldAST, AST):
    pass

class CPPFieldIdentifier(CPPFieldDeclarator, CXXFieldIdentifier, AST):
    pass

class CPPFieldInitializer(CPPAST, AST):
    pass

class CPPFieldInitializer0(CPPFieldInitializer, AST):
    pass

class CPPFieldInitializer1(CPPFieldInitializer, AST):
    pass

class CPPFieldInitializerList(CPPAST, AST):
    pass

class CPPFinal(CPPAST, TerminalSymbol, AST):
    pass

class CPPFor(CPPAST, TerminalSymbol, AST):
    pass

class CPPForRangeLoop(CPPStatement, AST):
    pass

class CPPForStatement(CPPStatement, CXXForStatement, LoopAST, AST):
    pass

class CPPForStatement0(CPPForStatement, AST):
    pass

class CPPForStatement1(CPPForStatement, AST):
    pass

class CPPForStatement2(CPPForStatement, AST):
    pass

class CPPForStatement3(CPPForStatement, AST):
    pass

class CPPForStatement4(CPPForStatement, AST):
    pass

class CPPForStatement5(CPPForStatement, AST):
    pass

class CPPFriend(CPPAST, TerminalSymbol, AST):
    pass

class CPPFriendDeclaration(CPPAST, AST):
    pass

class CPPFriendDeclaration0(CPPFriendDeclaration, AST):
    pass

class CPPFriendDeclaration1(CPPFriendDeclaration, AST):
    pass

class CPPFriendDeclaration2(CPPFriendDeclaration, AST):
    pass

class CPPFriendDeclaration3(CPPFriendDeclaration, AST):
    pass

class CPPFriendDeclaration4(CPPFriendDeclaration, AST):
    pass

class CPPFunctionDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXFunctionDeclarator, AST):
    pass

class CPPFunctionDeclarator0(CPPFunctionDeclarator, AST):
    pass

class CPPFunctionDeclarator1(CPPFunctionDeclarator, AST):
    pass

class CPPFunctionDefinition(CPPAST, CXXFunctionDefinition, FunctionAST, StatementAST, AST):
    pass

class CPPFunctionDefinition0(CPPFunctionDefinition, AST):
    pass

class CPPFunctionDefinition1(CPPFunctionDefinition, AST):
    pass

class CPPGoto(CPPAST, TerminalSymbol, AST):
    pass

class CPPGotoStatement(CPPStatement, GotoAST, AST):
    pass

class CPPIdentifier(CPPDeclarator, CPPExpression, CXXIdentifier, IdentifierAST, AST):
    pass

class CPPIf(CPPAST, TerminalSymbol, AST):
    pass

class CPPIfStatement(CPPStatement, CXXIfStatement, AST):
    pass

class CPPIfStatement0(CPPIfStatement, AST):
    pass

class CPPIfStatement1(CPPIfStatement, AST):
    pass

class CPPIfStatement2(CPPIfStatement, AST):
    pass

class CPPIfStatement3(CPPIfStatement, AST):
    pass

class CPPInitDeclarator(CPPAST, CXXInitDeclarator, VariableDeclarationAST, AST):
    pass

class CPPInitDeclarator0(CPPInitDeclarator, AST):
    pass

class CPPInitDeclarator1(CPPInitDeclarator, AST):
    pass

class CPPInitializerList(CPPAST, AST):
    pass

class CPPInitializerList0(CPPInitializerList, AST):
    pass

class CPPInitializerList1(CPPInitializerList, AST):
    pass

class CPPInitializerList2(CPPInitializerList, AST):
    pass

class CPPInitializerList3(CPPInitializerList, AST):
    pass

class CPPInitializerPair(CPPAST, CXXInitializerPair, AST):
    pass

class CPPInline(CPPAST, TerminalSymbol, AST):
    pass

class CPPInnerWhitespace(CPPAST, InnerWhitespace, AST):
    pass

class CPPWcharDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPWcharSingleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPLabeledStatement(CPPStatement, AST):
    pass

class CPPLabeledStatement0(CPPLabeledStatement, AST):
    pass

class CPPLabeledStatement1(CPPLabeledStatement, AST):
    pass

class CPPLabeledStatement2(CPPLabeledStatement, AST):
    pass

class CPPLambdaCaptureSpecifier(CPPAST, AST):
    pass

class CPPLambdaCaptureSpecifier0(CPPLambdaCaptureSpecifier, AST):
    pass

class CPPLambdaCaptureSpecifier1(CPPLambdaCaptureSpecifier, AST):
    pass

class CPPLambdaCaptureSpecifier2(CPPLambdaCaptureSpecifier, AST):
    pass

class CPPLambdaCaptureSpecifier3(CPPLambdaCaptureSpecifier, AST):
    pass

class CPPLambdaDefaultCapture(CPPAST, AST):
    pass

class CPPLambdaExpression(CPPExpression, AST):
    pass

class CPPLambdaExpression0(CPPLambdaExpression, AST):
    pass

class CPPLambdaExpression1(CPPLambdaExpression, AST):
    pass

class CPPLinkageSpecification(CPPAST, AST):
    pass

class CPPLong(CPPAST, TerminalSymbol, AST):
    pass

class CPPMsBasedModifier(CPPAST, AST):
    pass

class CPPMsCallModifier(CPPAST, AST):
    pass

class CPPMsDeclspecModifier(CPPAST, AST):
    pass

class CPPMsPointerModifier(CPPAST, AST):
    pass

class CPPMsRestrictModifier(CPPAST, AST):
    pass

class CPPMsSignedPtrModifier(CPPAST, AST):
    pass

class CPPMsUnalignedPtrModifier(CPPAST, AST):
    pass

class CPPMsUnsignedPtrModifier(CPPAST, AST):
    pass

class CPPMutable(CPPAST, TerminalSymbol, AST):
    pass

class CPPNamespace(CPPAST, TerminalSymbol, AST):
    pass

class CPPNamespaceDefinition(CPPAST, AST):
    pass

class CPPNamespaceIdentifier(CPPAST, AST):
    pass

class CPPNew(CPPAST, TerminalSymbol, AST):
    pass

class CPPNewDeclarator(CPPAST, AST):
    pass

class CPPNewDeclarator0(CPPNewDeclarator, AST):
    pass

class CPPNewDeclarator1(CPPNewDeclarator, AST):
    pass

class CPPNewExpression(CPPExpression, AST):
    pass

class CPPNoexcept(CPPAST, AST):
    pass

class CPPNoexcept0(CPPNoexcept, AST):
    pass

class CPPNoexcept1(CPPNoexcept, AST):
    pass

class CPPNoexcept2(CPPNoexcept, AST):
    pass

class CPPNoexceptTerminal(CPPAST, TerminalSymbol, AST):
    pass

class CPPNull(CPPExpression, AST):
    pass

class CPPNullptr(CPPExpression, AST):
    pass

class CPPNumberLiteral(CPPExpression, CXXNumberLiteral, NumberAST, AST):
    pass

class CPPOperator(CPPAST, TerminalSymbol, AST):
    pass

class CPPOperatorCast(CPPAST, AST):
    pass

class CPPOperatorCast0(CPPOperatorCast, AST):
    pass

class CPPOperatorCast1(CPPOperatorCast, AST):
    pass

class CPPOperatorName(CPPFieldDeclarator, CPPDeclarator, AST):
    pass

class CPPOptionalParameterDeclaration(CPPAST, AST):
    pass

class CPPOptionalTypeParameterDeclaration(CPPAST, AST):
    pass

class CPPOptionalTypeParameterDeclaration0(CPPOptionalTypeParameterDeclaration, AST):
    pass

class CPPOptionalTypeParameterDeclaration1(CPPOptionalTypeParameterDeclaration, AST):
    pass

class CPPOverride(CPPAST, TerminalSymbol, AST):
    pass

class CPPParameterDeclaration(CPPAST, CXXParameterDeclaration, AST):
    pass

class CPPParameterDeclaration0(CPPParameterDeclaration, AST):
    pass

class CPPParameterDeclaration1(CPPParameterDeclaration, AST):
    pass

class CPPParameterList(CPPAST, AST):
    pass

class CPPParameterList0(CPPParameterList, AST):
    pass

class CPPParameterList1(CPPParameterList, AST):
    pass

class CPPParameterPackExpansion(CPPExpression, AST):
    pass

class CPPParameterPackExpansion0(CPPParameterPackExpansion, AST):
    pass

class CPPParameterPackExpansion1(CPPParameterPackExpansion, AST):
    pass

class CPPParenthesizedDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXParenthesizedDeclarator, AST):
    pass

class CPPParenthesizedDeclarator0(CPPParenthesizedDeclarator, AST):
    pass

class CPPParenthesizedDeclarator1(CPPParenthesizedDeclarator, AST):
    pass

class CPPParenthesizedExpression(CPPExpression, CXXParenthesizedExpression, ParenthesizedExpressionAST, AST):
    pass

class CPPParenthesizedExpression0(CPPParenthesizedExpression, AST):
    pass

class CPPParenthesizedExpression1(CPPParenthesizedExpression, AST):
    pass

class CPPPointerDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXPointerDeclarator, AST):
    pass

class CPPPointerDeclarator0(CPPPointerDeclarator, AST):
    pass

class CPPPointerDeclarator1(CPPPointerDeclarator, AST):
    pass

class CPPPointerExpression(CPPExpression, CXXPointerExpression, AST):
    pass

class CPPPreprocArg(CPPAST, CXXPreprocArg, AST):
    pass

class CPPPreprocCall(CPPAST, AST):
    pass

class CPPPreprocDef(CPPAST, CXXPreprocDef, DefinitionAST, AST):
    pass

class CPPPreprocDefined(CPPAST, AST):
    pass

class CPPPreprocDefined0(CPPPreprocDefined, AST):
    pass

class CPPPreprocDefined1(CPPPreprocDefined, AST):
    pass

class CPPPreprocDirective(CPPAST, AST):
    pass

class CPPPreprocElif(CPPAST, CXXPreprocElif, AST):
    pass

class CPPPreprocElif0(CPPPreprocElif, AST):
    pass

class CPPPreprocElif1(CPPPreprocElif, AST):
    pass

class CPPPreprocElse(CPPAST, CXXPreprocElse, AST):
    pass

class CPPPreprocElse0(CPPPreprocElse, AST):
    pass

class CPPPreprocElse1(CPPPreprocElse, AST):
    pass

class CPPPreprocFunctionDef(CPPAST, CXXPreprocFunctionDef, DefinitionAST, AST):
    pass

class CPPPreprocIf(CPPAST, AST):
    pass

class CPPPreprocIf0(CPPPreprocIf, AST):
    pass

class CPPPreprocIf1(CPPPreprocIf, AST):
    pass

class CPPPreprocIfdef(CPPAST, AST):
    pass

class CPPPreprocIfdef0(CPPPreprocIfdef, AST):
    pass

class CPPPreprocIfdef1(CPPPreprocIfdef, AST):
    pass

class CPPPreprocInclude(CPPAST, CXXPreprocInclude, AST):
    pass

class CPPPreprocParams(CPPAST, CXXPreprocParams, AST):
    pass

class CPPPrimitiveType(CPPTypeSpecifier, CXXPrimitiveType, AST):
    pass

class CPPPrivate(CPPAST, TerminalSymbol, AST):
    pass

class CPPProtected(CPPAST, TerminalSymbol, AST):
    pass

class CPPPublic(CPPAST, TerminalSymbol, AST):
    pass

class CPPRawStringLiteral(CPPExpression, StringAST, AST):
    pass

class CPPReferenceDeclarator(CPPFieldDeclarator, CPPDeclarator, AST):
    pass

class CPPReferenceDeclarator0(CPPReferenceDeclarator, AST):
    pass

class CPPReferenceDeclarator1(CPPReferenceDeclarator, AST):
    pass

class CPPRegister(CPPAST, TerminalSymbol, AST):
    pass

class CPPRestrict(CPPAST, TerminalSymbol, AST):
    pass

class CPPReturn(CPPAST, TerminalSymbol, AST):
    pass

class CPPReturnStatement(CPPStatement, CXXReturnStatement, ReturnAST, AST):
    pass

class CPPReturnStatement0(CPPReturnStatement, AST):
    pass

class CPPReturnStatement1(CPPReturnStatement, AST):
    pass

class CPPScopedFieldIdentifier(CPPAST, AST):
    pass

class CPPScopedIdentifier(CPPDeclarator, CPPExpression, AST):
    pass

class CPPScopedNamespaceIdentifier(CPPAST, AST):
    pass

class CPPScopedTypeIdentifier(CPPTypeSpecifier, AST):
    pass

class CPPShort(CPPAST, TerminalSymbol, AST):
    pass

class CPPSigned(CPPAST, TerminalSymbol, AST):
    pass

class CPPSizedTypeSpecifier(CPPTypeSpecifier, AST):
    pass

class CPPSizeof(CPPAST, TerminalSymbol, AST):
    pass

class CPPSizeofExpression(CPPExpression, AST):
    pass

class CPPSizeofExpression0(CPPSizeofExpression, AST):
    pass

class CPPSizeofExpression1(CPPSizeofExpression, AST):
    pass

class CPPSourceTextFragment(CPPAST, SourceTextFragment, AST):
    pass

class CPPStatementIdentifier(CPPAST, AST):
    pass

class CPPStatic(CPPAST, TerminalSymbol, AST):
    pass

class CPPStaticAssert(CPPAST, TerminalSymbol, AST):
    pass

class CPPStaticAssertDeclaration(CPPAST, AST):
    pass

class CPPStaticAssertDeclaration0(CPPStaticAssertDeclaration, AST):
    pass

class CPPStaticAssertDeclaration1(CPPStaticAssertDeclaration, AST):
    pass

class CPPStorageClassSpecifier(CPPAST, AST):
    pass

class CPPStringLiteral(CPPExpression, CXXStringLiteral, StringAST, AST):
    pass

class CPPStruct(CPPAST, TerminalSymbol, AST):
    pass

class CPPStructSpecifier(CPPTypeSpecifier, CXXStructSpecifier, DefinitionAST, AST):
    pass

class CPPStructSpecifier0(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier1(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier10(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier11(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier12(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier13(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier14(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier15(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier16(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier17(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier2(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier3(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier4(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier5(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier6(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier7(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier8(CPPStructSpecifier, AST):
    pass

class CPPStructSpecifier9(CPPStructSpecifier, AST):
    pass

class CPPStructuredBindingDeclarator(CPPDeclarator, AST):
    pass

class CPPSubscriptDesignator(CPPAST, AST):
    pass

class CPPSubscriptExpression(CPPExpression, CXXSubscriptExpression, SubscriptAST, AST):
    pass

class CPPSwitch(CPPAST, TerminalSymbol, AST):
    pass

class CPPSwitchStatement(CPPStatement, CXXSwitchStatement, AST):
    pass

class CPPSystemLibString(CPPAST, AST):
    pass

class CPPTemplate(CPPAST, TerminalSymbol, AST):
    pass

class CPPTemplateArgumentList(CPPAST, AST):
    pass

class CPPTemplateArgumentList0(CPPTemplateArgumentList, AST):
    pass

class CPPTemplateArgumentList1(CPPTemplateArgumentList, AST):
    pass

class CPPTemplateArgumentList2(CPPTemplateArgumentList, AST):
    pass

class CPPTemplateDeclaration(CPPAST, AST):
    pass

class CPPTemplateDeclaration0(CPPTemplateDeclaration, AST):
    pass

class CPPTemplateDeclaration1(CPPTemplateDeclaration, AST):
    pass

class CPPTemplateDeclaration2(CPPTemplateDeclaration, AST):
    pass

class CPPTemplateDeclaration3(CPPTemplateDeclaration, AST):
    pass

class CPPTemplateFunction(CPPDeclarator, CPPExpression, AST):
    pass

class CPPTemplateInstantiation(CPPAST, AST):
    pass

class CPPTemplateInstantiation0(CPPTemplateInstantiation, AST):
    pass

class CPPTemplateInstantiation1(CPPTemplateInstantiation, AST):
    pass

class CPPTemplateMethod(CPPFieldDeclarator, AST):
    pass

class CPPTemplateParameterList(CPPAST, AST):
    pass

class CPPTemplateParameterList0(CPPTemplateParameterList, AST):
    pass

class CPPTemplateParameterList1(CPPTemplateParameterList, AST):
    pass

class CPPTemplateTemplateParameterDeclaration(CPPAST, AST):
    pass

class CPPTemplateType(CPPTypeSpecifier, AST):
    pass

class CPPThis(CPPExpression, AST):
    pass

class CPPThrow(CPPAST, TerminalSymbol, AST):
    pass

class CPPThrowSpecifier(CPPAST, AST):
    pass

class CPPThrowSpecifier0(CPPThrowSpecifier, AST):
    pass

class CPPThrowSpecifier1(CPPThrowSpecifier, AST):
    pass

class CPPThrowStatement(CPPStatement, AST):
    pass

class CPPThrowStatement0(CPPThrowStatement, AST):
    pass

class CPPThrowStatement1(CPPThrowStatement, AST):
    pass

class CPPTrailingReturnType(CPPAST, AST):
    pass

class CPPTrailingReturnType0(CPPTrailingReturnType, AST):
    pass

class CPPTrailingReturnType1(CPPTrailingReturnType, AST):
    pass

class CPPTrailingReturnType2(CPPTrailingReturnType, AST):
    pass

class CPPTrailingReturnType3(CPPTrailingReturnType, AST):
    pass

class CPPTranslationUnit(CPPAST, RootAST, AST):
    pass

class CPPTrue(CPPExpression, BooleanTrueAST, AST):
    pass

class CPPTry(CPPAST, TerminalSymbol, AST):
    pass

class CPPTryStatement(CPPStatement, AST):
    pass

class CPPTypeDefinition(CPPAST, CXXTypeDefinition, DefinitionAST, AST):
    pass

class CPPTypeDescriptor(CPPAST, AST):
    pass

class CPPTypeIdentifier(CPPTypeDeclarator, CPPTypeSpecifier, CXXTypeIdentifier, AST):
    pass

class CPPTypeParameterDeclaration(CPPAST, AST):
    pass

class CPPTypeParameterDeclaration0(CPPTypeParameterDeclaration, AST):
    pass

class CPPTypeParameterDeclaration1(CPPTypeParameterDeclaration, AST):
    pass

class CPPTypeQualifier(CPPAST, AST):
    pass

class CPPTypedef(CPPAST, TerminalSymbol, AST):
    pass

class CPPTypename(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnicodeDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnsignedTerminalDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnicodeSingleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnsignedTerminalSingleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnsigned8bitTerminalDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnsigned8bitTerminalSingleQuote(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnaryExpression(CPPExpression, CXXUnaryExpression, UnaryAST, AST):
    pass

class CPPUnion(CPPAST, TerminalSymbol, AST):
    pass

class CPPUnionSpecifier(CPPTypeSpecifier, CXXUnionSpecifier, DefinitionAST, AST):
    pass

class CPPUnionSpecifier0(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier1(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier10(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier11(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier12(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier13(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier14(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier15(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier16(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier17(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier2(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier3(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier4(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier5(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier6(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier7(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier8(CPPUnionSpecifier, AST):
    pass

class CPPUnionSpecifier9(CPPUnionSpecifier, AST):
    pass

class CPPUnsigned(CPPAST, TerminalSymbol, AST):
    pass

class CPPUpdateExpression(CPPExpression, CXXUpdateExpression, AST):
    pass

class CPPUpdateExpression0(CPPUpdateExpression, AST):
    pass

class CPPUpdateExpression1(CPPUpdateExpression, AST):
    pass

class CPPUsing(CPPAST, TerminalSymbol, AST):
    pass

class CPPUsingDeclaration(CPPAST, AST):
    pass

class CPPUsingDeclaration0(CPPUsingDeclaration, AST):
    pass

class CPPUsingDeclaration1(CPPUsingDeclaration, AST):
    pass

class CPPVariadicDeclaration(CPPParameterDeclaration, CPPIdentifier, AST):
    pass

class CPPVariadicDeclarator(CPPAST, AST):
    pass

class CPPVariadicDeclarator0(CPPVariadicDeclarator, AST):
    pass

class CPPVariadicDeclarator1(CPPVariadicDeclarator, AST):
    pass

class CPPVariadicParameterDeclaration(CPPAST, AST):
    pass

class CPPVariadicTypeParameterDeclaration(CPPAST, AST):
    pass

class CPPVariadicTypeParameterDeclaration0(CPPVariadicTypeParameterDeclaration, AST):
    pass

class CPPVariadicTypeParameterDeclaration1(CPPVariadicTypeParameterDeclaration, AST):
    pass

class CPPVirtual(CPPAST, TerminalSymbol, AST):
    pass

class CPPVirtualFunctionSpecifier(CPPAST, AST):
    pass

class CPPVirtualSpecifier(CPPAST, AST):
    pass

class CPPVolatile(CPPAST, TerminalSymbol, AST):
    pass

class CPPWhile(CPPAST, TerminalSymbol, AST):
    pass

class CPPWhileStatement(CPPStatement, CXXWhileStatement, LoopAST, AST):
    pass

class CPPOpenBracket(CPPAST, TerminalSymbol, AST):
    pass

class CPPOpenAttribute(CPPAST, TerminalSymbol, AST):
    pass

class CPPCloseBracket(CPPAST, TerminalSymbol, AST):
    pass

class CPPCloseAttribute(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseXor(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseXorAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPOpenBrace(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseOr(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseOrAssign(CPPAST, TerminalSymbol, AST):
    pass

class CPPLogicalOr(CPPAST, TerminalSymbol, AST):
    pass

class CPPCloseBrace(CPPAST, TerminalSymbol, AST):
    pass

class CPPBitwiseNot(CPPAST, TerminalSymbol, AST):
    pass

class JavascriptAST(AST):
    pass

class JavascriptLogicalNot(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptNotEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptStrictlyNotEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDoubleQuote(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptOpenTemplateLiteral(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptModulo(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptModuleAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseAnd(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLogicalAnd(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLogicalAndAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseAndAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptSingleQuote(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptOpenParenthesis(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptCloseParenthesis(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptMultiply(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptPow(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptPowAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptMultiplyAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAdd(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptIncrement(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAddAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptComma(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptSubtract(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDecrement(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptSubtractAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAutomaticSemicolon(JavascriptAST, AST):
    pass

class JavascriptTemplateChars(JavascriptAST, AST):
    pass

class JavascriptDot(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptEllipsis(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDivide(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDivideAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptColon(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptSemicolon(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLessThan(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitshiftLeft(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitshiftLeftAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLessThanOrEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptStrictlyEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptArrow(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptGreaterThan(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptGreaterThanOrEqual(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitshiftRight(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitshiftRightAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptUnsignedBitshiftRight(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptUnsignedBitshiftRightAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptQuestion(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptChaining(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptNullishCoalescing(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptNullishCoalescingAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptMatrixMultiply(JavascriptAST, TerminalSymbol, AST):
    pass

class ArgumentsAST(AST):
    pass

class JavascriptArguments(JavascriptAST, ArgumentsAST, AST):
    pass

class JavascriptArguments0(JavascriptArguments, AST):
    pass

class JavascriptArguments1(JavascriptArguments, AST):
    pass

class JavascriptArguments2(JavascriptArguments, AST):
    pass

class JavascriptExpression(JavascriptAST, AST):
    pass

class JavascriptPrimaryExpression(JavascriptExpression, AST):
    pass

class JavascriptArray(JavascriptPrimaryExpression, AST):
    pass

class JavascriptArray0(JavascriptArray, AST):
    pass

class JavascriptArray1(JavascriptArray, AST):
    pass

class JavascriptArray2(JavascriptArray, AST):
    pass

class JavascriptPattern(JavascriptAST, AST):
    pass

class JavascriptArrayPattern(JavascriptPattern, AST):
    pass

class JavascriptArrayPattern0(JavascriptArrayPattern, AST):
    pass

class JavascriptArrayPattern1(JavascriptArrayPattern, AST):
    pass

class JavascriptArrayPattern2(JavascriptArrayPattern, AST):
    pass

class JavascriptArrowFunction(JavascriptPrimaryExpression, FunctionAST, AST):
    pass

class JavascriptArrowFunction0(JavascriptArrowFunction, AST):
    pass

class JavascriptArrowFunction1(JavascriptArrowFunction, AST):
    pass

class JavascriptAs(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAssignmentExpression(JavascriptExpression, AST):
    pass

class JavascriptAssignmentPattern(JavascriptAST, AST):
    pass

class JavascriptAsync(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAugmentedAssignmentExpression(JavascriptExpression, AST):
    pass

class JavascriptAwait(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptAwaitExpression(JavascriptExpression, AST):
    pass

class JavascriptBinaryExpression(JavascriptExpression, BinaryAST, AST):
    pass

class JavascriptBreak(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptStatement(JavascriptAST, StatementAST, AST):
    pass

class JavascriptBreakStatement(JavascriptStatement, AST):
    pass

class JavascriptCallExpression(JavascriptPrimaryExpression, CallAST, AST):
    pass

class JavascriptCallExpression0(JavascriptCallExpression, AST):
    pass

class JavascriptCallExpression1(JavascriptCallExpression, AST):
    pass

class JavascriptCase(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptCatch(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptCatchClause(JavascriptAST, CatchAST, AST):
    pass

class JavascriptCatchClause0(JavascriptCatchClause, AST):
    pass

class JavascriptCatchClause1(JavascriptCatchClause, AST):
    pass

class JavascriptClass(JavascriptPrimaryExpression, AST):
    pass

class JavascriptClass0(JavascriptClass, AST):
    pass

class JavascriptClass1(JavascriptClass, AST):
    pass

class JavascriptClassBody(JavascriptAST, AST):
    pass

class ClassAST(AST):
    pass

class JavascriptDeclaration(JavascriptStatement, AST):
    pass

class JavascriptClassDeclaration(JavascriptDeclaration, ClassAST, AST):
    pass

class JavascriptClassDeclaration0(JavascriptClassDeclaration, AST):
    pass

class JavascriptClassDeclaration1(JavascriptClassDeclaration, AST):
    pass

class JavascriptClassHeritage(JavascriptAST, AST):
    pass

class JavascriptClassTerminal(JavascriptAST, TerminalSymbol, AST):
    pass

class EcmaComment(AST):
    pass

class JavascriptComment(JavascriptAST, EcmaComment, CommentAST, AST):
    pass

class JavascriptComputedPropertyName(JavascriptAST, AST):
    pass

class JavascriptConst(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptContinue(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptContinueStatement(JavascriptStatement, AST):
    pass

class JavascriptDebugger(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDebuggerStatement(JavascriptStatement, AST):
    pass

class JavascriptDecorator(JavascriptAST, AST):
    pass

class JavascriptDecorator0(JavascriptDecorator, AST):
    pass

class JavascriptDecorator1(JavascriptDecorator, AST):
    pass

class JavascriptDecorator2(JavascriptDecorator, AST):
    pass

class JavascriptDefault(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDelete(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDo(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptDoStatement(JavascriptStatement, LoopAST, AST):
    pass

class JavascriptElse(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptElseClause(JavascriptAST, AST):
    pass

class JavascriptEmptyStatement(JavascriptStatement, AST):
    pass

class EcmaError(AST):
    pass

class JavascriptError(JavascriptAST, EcmaError, ParseErrorAST, AST):
    pass

class JavascriptEscapeSequence(JavascriptAST, AST):
    pass

class JavascriptExport(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptExportClause(JavascriptAST, AST):
    pass

class JavascriptExportClause0(JavascriptExportClause, AST):
    pass

class JavascriptExportClause1(JavascriptExportClause, AST):
    pass

class JavascriptExportClause2(JavascriptExportClause, AST):
    pass

class JavascriptExportClause3(JavascriptExportClause, AST):
    pass

class JavascriptExportSpecifier(JavascriptAST, AST):
    pass

class JavascriptExportSpecifier0(JavascriptExportSpecifier, AST):
    pass

class JavascriptExportSpecifier1(JavascriptExportSpecifier, AST):
    pass

class JavascriptExportStatement(JavascriptStatement, AST):
    pass

class JavascriptExportStatement0(JavascriptExportStatement, AST):
    pass

class JavascriptExportStatement1(JavascriptExportStatement, AST):
    pass

class JavascriptExpressionStatement(JavascriptStatement, ExpressionStatementAST, AST):
    pass

class JavascriptExtends(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptFalse(JavascriptPrimaryExpression, BooleanFalseAST, AST):
    pass

class JavascriptFieldDefinition(JavascriptAST, AST):
    pass

class JavascriptFieldDefinition0(JavascriptFieldDefinition, AST):
    pass

class JavascriptFieldDefinition1(JavascriptFieldDefinition, AST):
    pass

class JavascriptFinally(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptFinallyClause(JavascriptAST, AST):
    pass

class JavascriptFor(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptForInStatement(JavascriptStatement, AST):
    pass

class JavascriptForInStatement0(JavascriptForInStatement, AST):
    pass

class JavascriptForInStatement1(JavascriptForInStatement, AST):
    pass

class JavascriptForInStatement2(JavascriptForInStatement, AST):
    pass

class JavascriptForInStatement3(JavascriptForInStatement, AST):
    pass

class JavascriptForStatement(JavascriptStatement, LoopAST, AST):
    pass

class ParametersAST(AST):
    pass

class JavascriptFormalParameters(JavascriptAST, ParametersAST, AST):
    pass

class JavascriptFormalParameters0(JavascriptFormalParameters, AST):
    pass

class JavascriptFormalParameters1(JavascriptFormalParameters, AST):
    pass

class JavascriptFrom(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptFunction(JavascriptPrimaryExpression, FunctionAST, AST):
    pass

class JavascriptFunctionDeclaration(JavascriptDeclaration, FunctionAST, AST):
    pass

class JavascriptFunctionTerminal(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptGeneratorFunction(JavascriptPrimaryExpression, AST):
    pass

class JavascriptGeneratorFunctionDeclaration(JavascriptDeclaration, AST):
    pass

class JavascriptGet(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptHashBangLine(JavascriptAST, AST):
    pass

class JavascriptIdentifier(JavascriptPattern, JavascriptPrimaryExpression, IdentifierAST, AST):
    pass

class JavascriptIf(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptIfStatement(JavascriptStatement, IfAST, AST):
    pass

class JavascriptIfStatement0(JavascriptIfStatement, AST):
    pass

class JavascriptIfStatement1(JavascriptIfStatement, AST):
    pass

class JavascriptImport(JavascriptPrimaryExpression, AST):
    pass

class JavascriptImportClause(JavascriptAST, AST):
    pass

class JavascriptImportClause0(JavascriptImportClause, AST):
    pass

class JavascriptImportClause1(JavascriptImportClause, AST):
    pass

class JavascriptImportSpecifier(JavascriptAST, AST):
    pass

class JavascriptImportSpecifier0(JavascriptImportSpecifier, AST):
    pass

class JavascriptImportSpecifier1(JavascriptImportSpecifier, AST):
    pass

class JavascriptImportStatement(JavascriptStatement, AST):
    pass

class JavascriptImportStatement0(JavascriptImportStatement, AST):
    pass

class JavascriptImportStatement1(JavascriptImportStatement, AST):
    pass

class JavascriptImportTerminal(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptIn(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptInnerWhitespace(JavascriptAST, InnerWhitespace, AST):
    pass

class JavascriptInstanceof(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptJsxAttribute(JavascriptAST, AST):
    pass

class JavascriptJsxAttribute0(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxAttribute1(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxAttribute2(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxAttribute3(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxAttribute4(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxAttribute5(JavascriptJsxAttribute, AST):
    pass

class JavascriptJsxClosingElement(JavascriptAST, AST):
    pass

class JavascriptJsxElement(JavascriptExpression, AST):
    pass

class JavascriptJsxExpression(JavascriptAST, AST):
    pass

class JavascriptJsxExpression0(JavascriptJsxExpression, AST):
    pass

class JavascriptJsxExpression1(JavascriptJsxExpression, AST):
    pass

class JavascriptJsxFragment(JavascriptExpression, AST):
    pass

class JavascriptJsxNamespaceName(JavascriptAST, AST):
    pass

class JavascriptJsxOpeningElement(JavascriptAST, AST):
    pass

class JavascriptJsxSelfClosingElement(JavascriptExpression, AST):
    pass

class JavascriptJsxText(JavascriptAST, AST):
    pass

class JavascriptLabeledStatement(JavascriptStatement, AST):
    pass

class JavascriptLet(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLexicalDeclaration(JavascriptDeclaration, AST):
    pass

class JavascriptMemberExpression(JavascriptPrimaryExpression, FieldAST, AST):
    pass

class JavascriptMemberExpression0(JavascriptMemberExpression, AST):
    pass

class JavascriptMemberExpression1(JavascriptMemberExpression, AST):
    pass

class JavascriptMetaProperty(JavascriptPrimaryExpression, AST):
    pass

class JavascriptMethodDefinition(JavascriptAST, AST):
    pass

class JavascriptMethodDefinition0(JavascriptMethodDefinition, AST):
    pass

class JavascriptMethodDefinition1(JavascriptMethodDefinition, AST):
    pass

class JavascriptMethodDefinition2(JavascriptMethodDefinition, AST):
    pass

class JavascriptMethodDefinition3(JavascriptMethodDefinition, AST):
    pass

class JavascriptNamedImports(JavascriptAST, AST):
    pass

class JavascriptNamedImports0(JavascriptNamedImports, AST):
    pass

class JavascriptNamedImports1(JavascriptNamedImports, AST):
    pass

class JavascriptNamedImports2(JavascriptNamedImports, AST):
    pass

class JavascriptNamedImports3(JavascriptNamedImports, AST):
    pass

class JavascriptNamespaceImport(JavascriptAST, AST):
    pass

class JavascriptNestedIdentifier(JavascriptAST, AST):
    pass

class JavascriptNew(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptNewExpression(JavascriptExpression, AST):
    pass

class JavascriptNull(JavascriptPrimaryExpression, AST):
    pass

class FloatAST(NumberAST, AST):
    pass

class JavascriptNumber(JavascriptPrimaryExpression, FloatAST, AST):
    pass

class JavascriptObject(JavascriptPrimaryExpression, AST):
    pass

class JavascriptObject0(JavascriptObject, AST):
    pass

class JavascriptObject1(JavascriptObject, AST):
    pass

class JavascriptObject2(JavascriptObject, AST):
    pass

class JavascriptObject3(JavascriptObject, AST):
    pass

class JavascriptObjectAssignmentPattern(JavascriptAST, AST):
    pass

class JavascriptObjectPattern(JavascriptPattern, AST):
    pass

class JavascriptObjectPattern0(JavascriptObjectPattern, AST):
    pass

class JavascriptObjectPattern1(JavascriptObjectPattern, AST):
    pass

class JavascriptObjectPattern2(JavascriptObjectPattern, AST):
    pass

class JavascriptObjectPattern3(JavascriptObjectPattern, AST):
    pass

class JavascriptOf(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptPair(JavascriptAST, AST):
    pass

class JavascriptPairPattern(JavascriptAST, AST):
    pass

class JavascriptParenthesizedExpression(JavascriptPrimaryExpression, ParenthesizedExpressionAST, AST):
    pass

class JavascriptPrivatePropertyIdentifier(JavascriptAST, AST):
    pass

class JavascriptProgram(JavascriptAST, RootAST, AST):
    pass

class JavascriptProgram0(JavascriptProgram, AST):
    pass

class JavascriptProgram1(JavascriptProgram, AST):
    pass

class JavascriptPropertyIdentifier(JavascriptAST, IdentifierAST, AST):
    pass

class JavascriptRegex(JavascriptPrimaryExpression, AST):
    pass

class JavascriptRegexFlags(JavascriptAST, AST):
    pass

class JavascriptRegexPattern(JavascriptAST, AST):
    pass

class JavascriptRestPattern(JavascriptPattern, AST):
    pass

class JavascriptRestPattern0(JavascriptRestPattern, AST):
    pass

class JavascriptRestPattern1(JavascriptRestPattern, AST):
    pass

class JavascriptReturn(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptReturnStatement(JavascriptStatement, ReturnAST, AST):
    pass

class JavascriptReturnStatement0(JavascriptReturnStatement, AST):
    pass

class JavascriptReturnStatement1(JavascriptReturnStatement, AST):
    pass

class JavascriptSequenceExpression(JavascriptAST, AST):
    pass

class JavascriptSet(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptShorthandPropertyIdentifier(JavascriptAST, IdentifierAST, AST):
    pass

class JavascriptShorthandPropertyIdentifierPattern(JavascriptAST, IdentifierAST, AST):
    pass

class JavascriptSourceTextFragment(JavascriptAST, SourceTextFragment, AST):
    pass

class JavascriptSpreadElement(JavascriptAST, AST):
    pass

class JavascriptStatementBlock(JavascriptStatement, CompoundAST, AST):
    pass

class JavascriptStatementIdentifier(JavascriptAST, AST):
    pass

class JavascriptStatic(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptString(JavascriptPrimaryExpression, StringAST, AST):
    pass

class JavascriptString0(JavascriptString, AST):
    pass

class JavascriptString1(JavascriptString, AST):
    pass

class JavascriptStringFragment(JavascriptAST, AST):
    pass

class JavascriptSubscriptExpression(JavascriptPrimaryExpression, SubscriptAST, AST):
    pass

class JavascriptSuper(JavascriptPrimaryExpression, AST):
    pass

class JavascriptSwitch(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptSwitchBody(JavascriptAST, AST):
    pass

class JavascriptSwitchCase(JavascriptAST, AST):
    pass

class JavascriptSwitchDefault(JavascriptAST, AST):
    pass

class JavascriptSwitchStatement(JavascriptStatement, ControlFlowAST, AST):
    pass

class JavascriptTarget(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptTemplateString(JavascriptPrimaryExpression, AST):
    pass

class JavascriptTemplateSubstitution(JavascriptAST, AST):
    pass

class JavascriptTernaryExpression(JavascriptExpression, AST):
    pass

class JavascriptThis(JavascriptPrimaryExpression, AST):
    pass

class JavascriptThrow(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptThrowStatement(JavascriptStatement, AST):
    pass

class JavascriptTrue(JavascriptPrimaryExpression, BooleanTrueAST, AST):
    pass

class JavascriptTry(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptTryStatement(JavascriptStatement, ControlFlowAST, AST):
    pass

class JavascriptTryStatement0(JavascriptTryStatement, AST):
    pass

class JavascriptTryStatement1(JavascriptTryStatement, AST):
    pass

class JavascriptTryStatement2(JavascriptTryStatement, AST):
    pass

class JavascriptTryStatement3(JavascriptTryStatement, AST):
    pass

class JavascriptTypeof(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptUnaryExpression(JavascriptExpression, UnaryAST, AST):
    pass

class JavascriptUndefined(JavascriptPrimaryExpression, AST):
    pass

class JavascriptUpdateExpression(JavascriptExpression, AST):
    pass

class JavascriptUpdateExpression0(JavascriptUpdateExpression, AST):
    pass

class JavascriptUpdateExpression1(JavascriptUpdateExpression, AST):
    pass

class JavascriptVar(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptVariableDeclaration(JavascriptDeclaration, AST):
    pass

class JavascriptVariableDeclarator(JavascriptAST, AST):
    pass

class JavascriptVariableDeclarator0(JavascriptVariableDeclarator, AST):
    pass

class JavascriptVariableDeclarator1(JavascriptVariableDeclarator, AST):
    pass

class JavascriptVoid(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptWhile(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptWhileStatement(JavascriptStatement, LoopAST, WhileAST, AST):
    pass

class JavascriptWith(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptWithStatement(JavascriptStatement, AST):
    pass

class JavascriptYield(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptYieldExpression(JavascriptExpression, AST):
    pass

class JavascriptYieldExpression0(JavascriptYieldExpression, AST):
    pass

class JavascriptYieldExpression1(JavascriptYieldExpression, AST):
    pass

class JavascriptYieldExpression2(JavascriptYieldExpression, AST):
    pass

class JavascriptOpenBracket(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptCloseBracket(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseXor(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseXorAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBackQuote(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptOpenBrace(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseOr(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseOrAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLogicalOr(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptLogicalOrAssign(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptCloseBrace(JavascriptAST, TerminalSymbol, AST):
    pass

class JavascriptBitwiseNot(JavascriptAST, TerminalSymbol, AST):
    pass

class PythonAST(AST):
    pass

class PythonNotEqual(PythonAST, TerminalSymbol, AST):
    pass

class PythonDoubleQuote(PythonAST, TerminalSymbol, AST):
    pass

class PythonModulo(PythonAST, TerminalSymbol, AST):
    pass

class PythonModuleAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseAnd(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseAndAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonOpenParenthesis(PythonAST, TerminalSymbol, AST):
    pass

class PythonCloseParenthesis(PythonAST, TerminalSymbol, AST):
    pass

class PythonMultiply(PythonAST, TerminalSymbol, AST):
    pass

class PythonPow(PythonAST, TerminalSymbol, AST):
    pass

class PythonPowAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonMultiplyAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonAdd(PythonAST, TerminalSymbol, AST):
    pass

class PythonAddAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonComma(PythonAST, TerminalSymbol, AST):
    pass

class PythonSubtract(PythonAST, TerminalSymbol, AST):
    pass

class PythonFutureSubtract(PythonAST, TerminalSymbol, AST):
    pass

class PythonSubtractAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonArrow(PythonAST, TerminalSymbol, AST):
    pass

class PythonCompoundStatement(PythonAST, StatementAST, AST):
    pass

class PythonDedent(PythonAST, AST):
    pass

class PythonIndent(PythonAST, AST):
    pass

class PythonNewline(PythonAST, AST):
    pass

class PythonSimpleStatement(PythonAST, StatementAST, AST):
    pass

class PythonStringContent(PythonAST, AST):
    pass

class PythonStringEnd(PythonAST, AST):
    pass

class PythonStringStart(PythonAST, AST):
    pass

class PythonDot(PythonAST, TerminalSymbol, AST):
    pass

class PythonDivide(PythonAST, TerminalSymbol, AST):
    pass

class PythonFloorDivide(PythonAST, TerminalSymbol, AST):
    pass

class PythonFloorDivideAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonDivideAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonColon(PythonAST, TerminalSymbol, AST):
    pass

class PythonWalrus(PythonAST, TerminalSymbol, AST):
    pass

class PythonLessThan(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitshiftLeft(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitshiftLeftAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonLessThanOrEqual(PythonAST, TerminalSymbol, AST):
    pass

class PythonNotEqualFlufl(PythonAST, TerminalSymbol, AST):
    pass

class PythonAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonEqual(PythonAST, TerminalSymbol, AST):
    pass

class PythonGreaterThan(PythonAST, TerminalSymbol, AST):
    pass

class PythonGreaterThanOrEqual(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitshiftRight(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitshiftRightAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonMatrixMultiply(PythonAST, TerminalSymbol, AST):
    pass

class PythonMatrixMultiplyAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonAliasedImport(PythonAST, AST):
    pass

class PythonAnd(PythonAST, TerminalSymbol, AST):
    pass

class PythonArgumentList(PythonAST, ArgumentsAST, AST):
    pass

class PythonArgumentList0(PythonArgumentList, AST):
    pass

class PythonArgumentList1(PythonArgumentList, AST):
    pass

class PythonArgumentList2(PythonArgumentList, AST):
    pass

class PythonArgumentList3(PythonArgumentList, AST):
    pass

class PythonArgumentList4(PythonArgumentList, AST):
    pass

class PythonAs(PythonAST, TerminalSymbol, AST):
    pass

class PythonAssert(PythonAST, TerminalSymbol, AST):
    pass

class PythonAssertStatement(PythonSimpleStatement, AST):
    pass

class PythonAssignment(PythonAST, VariableDeclarationAST, AST):
    pass

class PythonAssignment0(PythonAssignment, AST):
    pass

class PythonAssignment1(PythonAssignment, AST):
    pass

class PythonAssignment2(PythonAssignment, AST):
    pass

class PythonAsync(PythonAST, TerminalSymbol, AST):
    pass

class PythonExpression(PythonAST, ExpressionAST, AST):
    pass

class PythonPrimaryExpression(PythonExpression, AST):
    pass

class PythonPattern(PythonAST, AST):
    pass

class PythonAttribute(PythonPattern, PythonPrimaryExpression, FieldAST, AST):
    pass

class PythonAugmentedAssignment(PythonAST, AST):
    pass

class PythonAwait(PythonExpression, AST):
    pass

class PythonAwaitTerminal(PythonAST, TerminalSymbol, AST):
    pass

class PythonBinaryOperator(PythonPrimaryExpression, BinaryAST, AST):
    pass

class PythonBlock(PythonAST, CompoundAST, AST):
    pass

class PythonBooleanOperator(PythonExpression, BinaryAST, AST):
    pass

class PythonBreak(PythonAST, TerminalSymbol, AST):
    pass

class PythonBreakStatement(PythonSimpleStatement, AST):
    pass

class PythonCall(PythonPrimaryExpression, CallAST, AST):
    pass

class PythonChevron(PythonAST, AST):
    pass

class PythonClass(PythonAST, TerminalSymbol, AST):
    pass

class PythonClassDefinition(PythonCompoundStatement, ClassAST, AST):
    pass

class PythonClassDefinition0(PythonClassDefinition, AST):
    pass

class PythonClassDefinition1(PythonClassDefinition, AST):
    pass

class PythonComment(PythonAST, CommentAST, AST):
    pass

class PythonComparisonOperator(PythonExpression, AST):
    pass

class PythonComparisonOperator0(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator1(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator10(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator2(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator3(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator4(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator5(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator6(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator7(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator8(PythonComparisonOperator, AST):
    pass

class PythonComparisonOperator9(PythonComparisonOperator, AST):
    pass

class PythonConcatenatedString(PythonPrimaryExpression, AST):
    pass

class PythonConditionalExpression(PythonExpression, ControlFlowAST, AST):
    pass

class PythonContinue(PythonAST, TerminalSymbol, AST):
    pass

class PythonContinueStatement(PythonSimpleStatement, AST):
    pass

class PythonDecoratedDefinition(PythonCompoundStatement, AST):
    pass

class PythonDecorator(PythonAST, AST):
    pass

class PythonDef(PythonAST, TerminalSymbol, AST):
    pass

class PythonParameter(PythonAST, AST):
    pass

class PythonDefaultParameter(PythonParameter, AST):
    pass

class PythonDel(PythonAST, TerminalSymbol, AST):
    pass

class PythonDeleteStatement(PythonSimpleStatement, AST):
    pass

class PythonDictionary(PythonPrimaryExpression, AST):
    pass

class PythonDictionary0(PythonDictionary, AST):
    pass

class PythonDictionary1(PythonDictionary, AST):
    pass

class PythonDictionary2(PythonDictionary, AST):
    pass

class PythonDictionary3(PythonDictionary, AST):
    pass

class PythonDictionaryComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    pass

class PythonDictionarySplat(PythonAST, AST):
    pass

class PythonDictionarySplatPattern(PythonParameter, AST):
    pass

class PythonDictionarySplatPattern0(PythonDictionarySplatPattern, AST):
    pass

class PythonDictionarySplatPattern1(PythonDictionarySplatPattern, AST):
    pass

class PythonDottedName(PythonAST, AST):
    pass

class PythonElif(PythonAST, TerminalSymbol, AST):
    pass

class PythonElifClause(PythonAST, AST):
    pass

class PythonElifClause0(PythonElifClause, AST):
    pass

class PythonElifClause1(PythonElifClause, AST):
    pass

class PythonEllipsis(PythonPrimaryExpression, AST):
    pass

class PythonElse(PythonAST, TerminalSymbol, AST):
    pass

class PythonElseClause(PythonAST, AST):
    pass

class PythonElseClause0(PythonElseClause, AST):
    pass

class PythonElseClause1(PythonElseClause, AST):
    pass

class PythonEmptyArgumentList(PythonArgumentList, AST):
    pass

class PythonParameters(PythonAST, ParametersAST, AST):
    pass

class PythonEmptyParameters(PythonParameters, AST):
    pass

class PythonTuple(PythonPrimaryExpression, AST):
    pass

class PythonEmptyTuple(PythonTuple, AST):
    pass

class PythonError(PythonAST, ParseErrorAST, AST):
    pass

class PythonEscapeSequence(PythonAST, AST):
    pass

class PythonExcept(PythonAST, TerminalSymbol, AST):
    pass

class PythonExceptClause(PythonAST, CatchAST, AST):
    pass

class PythonExceptClause0(PythonExceptClause, AST):
    pass

class PythonExceptClause1(PythonExceptClause, AST):
    pass

class PythonExceptClause2(PythonExceptClause, AST):
    pass

class PythonExceptClause3(PythonExceptClause, AST):
    pass

class PythonExceptClause4(PythonExceptClause, AST):
    pass

class PythonExceptClause5(PythonExceptClause, AST):
    pass

class PythonExec(PythonAST, TerminalSymbol, AST):
    pass

class PythonExecStatement(PythonSimpleStatement, AST):
    pass

class PythonExecStatement0(PythonExecStatement, AST):
    pass

class PythonExecStatement1(PythonExecStatement, AST):
    pass

class PythonExpressionList(PythonAST, AST):
    pass

class PythonExpressionList0(PythonExpressionList, AST):
    pass

class PythonExpressionList1(PythonExpressionList, AST):
    pass

class PythonExpressionStatement(PythonSimpleStatement, ExpressionStatementAST, AST):
    pass

class PythonExpressionStatement0(PythonExpressionStatement, AST):
    pass

class PythonExpressionStatement1(PythonExpressionStatement, AST):
    pass

class PythonFalse(PythonPrimaryExpression, BooleanFalseAST, AST):
    pass

class PythonFinally(PythonAST, TerminalSymbol, AST):
    pass

class PythonFinallyClause(PythonAST, AST):
    pass

class PythonFinallyClause0(PythonFinallyClause, AST):
    pass

class PythonFinallyClause1(PythonFinallyClause, AST):
    pass

class PythonFloat(PythonPrimaryExpression, FloatAST, AST):
    pass

class PythonFor(PythonAST, TerminalSymbol, AST):
    pass

class PythonForInClause(PythonAST, LoopAST, AST):
    pass

class PythonForInClause0(PythonForInClause, AST):
    pass

class PythonForInClause1(PythonForInClause, AST):
    pass

class PythonForStatement(PythonCompoundStatement, LoopAST, AST):
    pass

class PythonForStatement0(PythonForStatement, AST):
    pass

class PythonForStatement1(PythonForStatement, AST):
    pass

class PythonFormatExpression(PythonAST, AST):
    pass

class PythonFormatSpecifier(PythonAST, AST):
    pass

class PythonFrom(PythonAST, TerminalSymbol, AST):
    pass

class PythonFunctionDefinition(PythonCompoundStatement, FunctionAST, AST):
    pass

class PythonFunctionDefinition0(PythonFunctionDefinition, AST):
    pass

class PythonFunctionDefinition1(PythonFunctionDefinition, AST):
    pass

class PythonFunctionDefinition2(PythonFunctionDefinition, AST):
    pass

class PythonFunctionDefinition3(PythonFunctionDefinition, AST):
    pass

class PythonFutureImportStatement(PythonSimpleStatement, AST):
    pass

class PythonFutureImportStatement0(PythonFutureImportStatement, AST):
    pass

class PythonFutureImportStatement1(PythonFutureImportStatement, AST):
    pass

class PythonGeneratorExpression(PythonPrimaryExpression, ControlFlowAST, AST):
    pass

class PythonGlobal(PythonAST, TerminalSymbol, AST):
    pass

class PythonGlobalStatement(PythonSimpleStatement, AST):
    pass

class PythonIdentifier(PythonParameter, PythonPattern, PythonPrimaryExpression, IdentifierAST, AST):
    pass

class PythonIf(PythonAST, TerminalSymbol, AST):
    pass

class PythonIfClause(PythonAST, AST):
    pass

class PythonIfStatement(PythonCompoundStatement, IfAST, AST):
    pass

class PythonIfStatement0(PythonIfStatement, AST):
    pass

class PythonIfStatement1(PythonIfStatement, AST):
    pass

class PythonIfStatement2(PythonIfStatement, AST):
    pass

class PythonIfStatement3(PythonIfStatement, AST):
    pass

class PythonImport(PythonAST, TerminalSymbol, AST):
    pass

class PythonImportFromStatement(PythonSimpleStatement, AST):
    pass

class PythonImportFromStatement0(PythonImportFromStatement, AST):
    pass

class PythonImportFromStatement1(PythonImportFromStatement, AST):
    pass

class PythonImportFromStatement2(PythonImportFromStatement, AST):
    pass

class PythonImportPrefix(PythonAST, AST):
    pass

class PythonImportStatement(PythonSimpleStatement, AST):
    pass

class PythonIn(PythonAST, TerminalSymbol, AST):
    pass

class PythonInnerWhitespace(PythonAST, InnerWhitespace, AST):
    pass

class IntegerAST(NumberAST, AST):
    pass

class PythonInteger(PythonPrimaryExpression, IntegerAST, AST):
    pass

class PythonInterpolation(PythonAST, AST):
    pass

class PythonInterpolation0(PythonInterpolation, AST):
    pass

class PythonInterpolation1(PythonInterpolation, AST):
    pass

class PythonInterpolation2(PythonInterpolation, AST):
    pass

class PythonInterpolation3(PythonInterpolation, AST):
    pass

class PythonIs(PythonAST, TerminalSymbol, AST):
    pass

class PythonKeywordArgument(PythonAST, VariableDeclarationAST, AST):
    pass

class PythonKeywordOnlySeparator(PythonParameter, AST):
    pass

class LambdaAST(AST):
    pass

class PythonLambda(PythonExpression, LambdaAST, FunctionAST, AST):
    pass

class PythonLambdaParameters(PythonAST, ParametersAST, AST):
    pass

class PythonLambdaTerminal(PythonAST, TerminalSymbol, AST):
    pass

class PythonList(PythonPrimaryExpression, AST):
    pass

class PythonList0(PythonList, AST):
    pass

class PythonList1(PythonList, AST):
    pass

class PythonListComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    pass

class PythonListPattern(PythonPattern, AST):
    pass

class PythonListPattern0(PythonListPattern, AST):
    pass

class PythonListPattern1(PythonListPattern, AST):
    pass

class PythonListSplat(PythonAST, AST):
    pass

class PythonListSplatPattern(PythonParameter, PythonPattern, AST):
    pass

class PythonListSplatPattern0(PythonListSplatPattern, AST):
    pass

class PythonListSplatPattern1(PythonListSplatPattern, AST):
    pass

class PythonModule(PythonAST, RootAST, AST):
    pass

class PythonNamedExpression(PythonExpression, AST):
    pass

class PythonNone(PythonPrimaryExpression, AST):
    pass

class PythonNonlocal(PythonAST, TerminalSymbol, AST):
    pass

class PythonNonlocalStatement(PythonSimpleStatement, AST):
    pass

class PythonNot(PythonAST, TerminalSymbol, AST):
    pass

class PythonNotOperator(PythonExpression, UnaryAST, AST):
    pass

class PythonOr(PythonAST, TerminalSymbol, AST):
    pass

class PythonPair(PythonAST, AST):
    pass

class PythonParameters0(PythonParameters, AST):
    pass

class PythonParenthesizedExpression(PythonPrimaryExpression, ParenthesizedExpressionAST, AST):
    pass

class PythonParenthesizedExpression0(PythonParenthesizedExpression, AST):
    pass

class PythonParenthesizedExpression1(PythonParenthesizedExpression, AST):
    pass

class PythonParenthesizedListSplat(PythonAST, AST):
    pass

class PythonParenthesizedListSplat0(PythonParenthesizedListSplat, AST):
    pass

class PythonParenthesizedListSplat1(PythonParenthesizedListSplat, AST):
    pass

class PythonPass(PythonAST, TerminalSymbol, AST):
    pass

class PythonPassStatement(PythonSimpleStatement, AST):
    pass

class PythonPatternList(PythonAST, AST):
    pass

class PythonPatternList0(PythonPatternList, AST):
    pass

class PythonPatternList1(PythonPatternList, AST):
    pass

class PythonPositionalOnlySeparator(PythonParameter, AST):
    pass

class PythonPrint(PythonAST, TerminalSymbol, AST):
    pass

class PythonPrintStatement(PythonSimpleStatement, AST):
    pass

class PythonPrintStatement0(PythonPrintStatement, AST):
    pass

class PythonPrintStatement1(PythonPrintStatement, AST):
    pass

class PythonRaise(PythonAST, TerminalSymbol, AST):
    pass

class PythonRaiseStatement(PythonSimpleStatement, AST):
    pass

class PythonRaiseStatement0(PythonRaiseStatement, AST):
    pass

class PythonRaiseStatement1(PythonRaiseStatement, AST):
    pass

class PythonRaiseStatement2(PythonRaiseStatement, AST):
    pass

class PythonRaiseStatement3(PythonRaiseStatement, AST):
    pass

class PythonRelativeImport(PythonAST, AST):
    pass

class PythonRelativeImport0(PythonRelativeImport, AST):
    pass

class PythonRelativeImport1(PythonRelativeImport, AST):
    pass

class PythonReturn(PythonAST, TerminalSymbol, AST):
    pass

class PythonReturnStatement(PythonSimpleStatement, ReturnAST, AST):
    pass

class PythonReturnStatement0(PythonReturnStatement, AST):
    pass

class PythonReturnStatement1(PythonReturnStatement, AST):
    pass

class PythonSet(PythonPrimaryExpression, AST):
    pass

class PythonSetComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    pass

class PythonSlice(PythonAST, AST):
    pass

class PythonSlice0(PythonSlice, AST):
    pass

class PythonSlice1(PythonSlice, AST):
    pass

class PythonSlice10(PythonSlice, AST):
    pass

class PythonSlice11(PythonSlice, AST):
    pass

class PythonSlice2(PythonSlice, AST):
    pass

class PythonSlice3(PythonSlice, AST):
    pass

class PythonSlice4(PythonSlice, AST):
    pass

class PythonSlice5(PythonSlice, AST):
    pass

class PythonSlice6(PythonSlice, AST):
    pass

class PythonSlice7(PythonSlice, AST):
    pass

class PythonSlice8(PythonSlice, AST):
    pass

class PythonSlice9(PythonSlice, AST):
    pass

class PythonSourceTextFragment(PythonAST, SourceTextFragment, AST):
    pass

class PythonString(PythonPrimaryExpression, StringAST, AST):
    pass

class PythonSubscript(PythonPattern, PythonPrimaryExpression, SubscriptAST, AST):
    pass

class PythonTrue(PythonPrimaryExpression, BooleanTrueAST, AST):
    pass

class PythonTry(PythonAST, TerminalSymbol, AST):
    pass

class PythonTryStatement(PythonCompoundStatement, ControlFlowAST, AST):
    pass

class PythonTryStatement0(PythonTryStatement, AST):
    pass

class PythonTryStatement1(PythonTryStatement, AST):
    pass

class PythonTryStatement2(PythonTryStatement, AST):
    pass

class PythonTryStatement3(PythonTryStatement, AST):
    pass

class PythonTryStatement4(PythonTryStatement, AST):
    pass

class PythonTryStatement5(PythonTryStatement, AST):
    pass

class PythonTryStatement6(PythonTryStatement, AST):
    pass

class PythonTryStatement7(PythonTryStatement, AST):
    pass

class PythonTryStatement8(PythonTryStatement, AST):
    pass

class PythonTryStatement9(PythonTryStatement, AST):
    pass

class PythonTuple0(PythonTuple, AST):
    pass

class PythonTuplePattern(PythonParameter, PythonPattern, AST):
    pass

class PythonTuplePattern0(PythonTuplePattern, AST):
    pass

class PythonTuplePattern1(PythonTuplePattern, AST):
    pass

class PythonType(PythonAST, AST):
    pass

class PythonTypeConversion(PythonAST, AST):
    pass

class PythonTypedDefaultParameter(PythonParameter, AST):
    pass

class PythonTypedParameter(PythonParameter, AST):
    pass

class PythonUnaryOperator(PythonPrimaryExpression, UnaryAST, AST):
    pass

class PythonWhile(PythonAST, TerminalSymbol, AST):
    pass

class PythonWhileStatement(PythonCompoundStatement, LoopAST, WhileAST, AST):
    pass

class PythonWhileStatement0(PythonWhileStatement, AST):
    pass

class PythonWhileStatement1(PythonWhileStatement, AST):
    pass

class PythonWhileStatement2(PythonWhileStatement, AST):
    pass

class PythonWhileStatement3(PythonWhileStatement, AST):
    pass

class PythonWildcardImport(PythonAST, AST):
    pass

class PythonWith(PythonAST, TerminalSymbol, AST):
    pass

class PythonWithClause(PythonAST, AST):
    pass

class PythonWithClause0(PythonWithClause, AST):
    pass

class PythonWithClause1(PythonWithClause, AST):
    pass

class PythonWithItem(PythonAST, AST):
    pass

class PythonWithItem0(PythonWithItem, AST):
    pass

class PythonWithItem1(PythonWithItem, AST):
    pass

class PythonWithStatement(PythonCompoundStatement, AST):
    pass

class PythonWithStatement0(PythonWithStatement, AST):
    pass

class PythonWithStatement1(PythonWithStatement, AST):
    pass

class PythonYield(PythonAST, AST):
    pass

class PythonYield0(PythonYield, AST):
    pass

class PythonYield1(PythonYield, AST):
    pass

class PythonYield2(PythonYield, AST):
    pass

class PythonYieldTerminal(PythonAST, TerminalSymbol, AST):
    pass

class PythonOpenBracket(PythonAST, TerminalSymbol, AST):
    pass

class PythonCloseBracket(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseXor(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseXorAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonOpenBrace(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseOr(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseOrAssign(PythonAST, TerminalSymbol, AST):
    pass

class PythonCloseBrace(PythonAST, TerminalSymbol, AST):
    pass

class PythonBitwiseNot(PythonAST, TerminalSymbol, AST):
    pass

