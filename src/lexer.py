import re
from enum import Enum, auto

class TokenType(Enum):
    # Console
    CONSOLE_LOG = auto()
    CONSOLE_WARN = auto()
    CONSOLE_ERROR = auto()

    LOGIC_WAIT = auto()
    NAVIGATION_REDIRECT = auto()
    AUDIO_PLAY = auto()
    AUDIO_SET_VOLUME = auto()
    AUDIO_STOP = auto()
    AUDIO_PAUSE = auto()
    AUDIO_RESUME = auto()
    LOOKS_SHOW = auto()
    LOOKS_HIDE = auto()
    LOOKS_SET_TEXT = auto()
    LOOKS_SET_PROPERTY = auto()
    LOOKS_GET_PROPERTY = auto()
    LOOKS_GET_TEXT = auto()
    LOOKS_DUPLICATE = auto()
    LOOKS_DELETE = auto()
    LOOKS_SET_PARENT = auto()
    NETWORK_BROADCAST = auto()
    NETWORK_GLOBAL_BROADCAST = auto()
    NETWORK_GET_USERNAME = auto()
    NETWORK_GET_DISPLAYNAME = auto()
    NETWORK_GET_USERID = auto()
    COOKIES_SET_COOKIE = auto()
    COOKIES_INCREASE_COOKIE = auto()
    COOKIES_DELETE_COOKIE = auto()
    COOKIES_GET_COOKIE = auto()
    MATH_ROUND = auto()
    MATH_FLOOR = auto()
    MATH_RANDOM = auto()
    STRINGS_SUBSTRING = auto()
    STRINGS_REPLACE = auto()
    STRINGS_GET_LENGTH = auto()
    STRINGS_SPLIT = auto()
    TABLES_NEW = auto()
    TABLES_SET_ENTRY = auto()
    TABLES_GET_ENTRY = auto()
    TABLES_DELETE_ENTRY = auto()
    TABLES_GET_LENGTH = auto()
    FUNCTIONS_RUN = auto()
    VAR = auto()

    IF = auto()
    REPEAT_FOREVER = auto()
    END = auto()

    # Operators and Punctuation
    EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    NOT_EQUAL = auto()
    ASSIGN = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LSQUARE = auto()
    RSQUARE = auto()
    LBRACE = auto()
    RBRACE = auto()

    # Other
    IDENTIFIER = auto()
    OBJECT_IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    EOF = auto()
    FUNCTION = auto()
    FUNCTION_CALL = auto()
    COMMENT = auto()
    EVENT = auto()
    LENGTH_OF = auto()


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        patterns = [
            (r'Console:Log', TokenType.CONSOLE_LOG),
            (r'Console:Warn', TokenType.CONSOLE_WARN),
            (r'Console:Error', TokenType.CONSOLE_ERROR),
            (r'Logic:Wait', TokenType.LOGIC_WAIT),
            (r'Navigation:Redirect', TokenType.NAVIGATION_REDIRECT),
            (r'Audio:Play', TokenType.AUDIO_PLAY),
            (r'Audio:SetVolume', TokenType.AUDIO_SET_VOLUME),
            (r'Audio:Stop', TokenType.AUDIO_STOP),
            (r'Audio:Pause', TokenType.AUDIO_PAUSE),
            (r'Audio:Resume', TokenType.AUDIO_RESUME),
            (r'Looks:Show', TokenType.LOOKS_SHOW),
            (r'Looks:Hide', TokenType.LOOKS_HIDE),
            (r'Looks:SetText', TokenType.LOOKS_SET_TEXT),
            (r'Looks:SetProperty', TokenType.LOOKS_SET_PROPERTY),
            (r'Looks:GetProperty', TokenType.LOOKS_GET_PROPERTY),
            (r'Looks:GetText', TokenType.LOOKS_GET_TEXT),
            (r'Looks:Duplicate', TokenType.LOOKS_DUPLICATE),
            (r'Looks:Delete', TokenType.LOOKS_DELETE),
            (r'Looks:SetParent', TokenType.LOOKS_SET_PARENT),
            (r'Network:Broadcast', TokenType.NETWORK_BROADCAST),
            (r'Network:GlobalBroadcast', TokenType.NETWORK_GLOBAL_BROADCAST),
            (r'Network:GetUsername', TokenType.NETWORK_GET_USERNAME),
            (r'Network:GetDisplayName', TokenType.NETWORK_GET_DISPLAYNAME),
            (r'Network:GetUserId', TokenType.NETWORK_GET_USERID),
            (r'Cookies:SetCookie', TokenType.COOKIES_SET_COOKIE),
            (r'Cookies:IncreaseCookie', TokenType.COOKIES_INCREASE_COOKIE),
            (r'Cookies:DeleteCookie', TokenType.COOKIES_DELETE_COOKIE),
            (r'Cookies:GetCookie', TokenType.COOKIES_GET_COOKIE),
            (r'Math:Round', TokenType.MATH_ROUND),
            (r'Math:Floor', TokenType.MATH_FLOOR),
            (r'Math:Random', TokenType.MATH_RANDOM),
            (r'Strings:Substring', TokenType.STRINGS_SUBSTRING),
            (r'Strings:Replace', TokenType.STRINGS_REPLACE),
            (r'Strings:GetLength', TokenType.STRINGS_GET_LENGTH),
            (r'Strings:Split', TokenType.STRINGS_SPLIT),
            (r'Tables:New', TokenType.TABLES_NEW),
            (r'Tables:SetEntry', TokenType.TABLES_SET_ENTRY),
            (r'Tables:GetEntry', TokenType.TABLES_GET_ENTRY),
            (r'Tables:DeleteEntry', TokenType.TABLES_DELETE_ENTRY),
            (r'Tables:GetLength', TokenType.TABLES_GET_LENGTH),
            (r'Functions:Run', TokenType.FUNCTIONS_RUN),
            (r'if', TokenType.IF),
            (r'repeat_forever', TokenType.REPEAT_FOREVER),
            (r'end', TokenType.END),
            (r'<#\d+>', TokenType.OBJECT_IDENTIFIER),
            (r'@event ([a-zA-Z]*)', TokenType.EVENT),
            (r'@function ([a-zA-Z]*)', TokenType.FUNCTION),
            (r'#', TokenType.LENGTH_OF),
            (r'==', TokenType.EQUALS),
            (r'>', TokenType.GREATER_THAN),
            (r'<', TokenType.LESS_THAN),
            (r'!=', TokenType.NOT_EQUAL),
            (r'=', TokenType.ASSIGN),
            (r',', TokenType.COMMA),
            (r':', TokenType.COLON),
            (r';', TokenType.SEMICOLON),
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\[', TokenType.LSQUARE),
            (r'\]', TokenType.RSQUARE),
            (r'\{', TokenType.LBRACE),
            (r'\}', TokenType.RBRACE),
            (r'\d+', TokenType.NUMBER),
            (r'\".*?\"', TokenType.STRING),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            (r'--.*', None), # Ignore comments
            (r'\s+', None),  # Ignore whitespace
        ]

        while self.current_position < len(self.source_code):
            match = None
            for pattern, token_type in patterns:
                regex = re.compile(pattern, re.MULTILINE) if token_type == TokenType.COMMENT else re.compile(pattern)
                match = regex.match(self.source_code, self.current_position)
                if match:
                    if token_type:
                        token_value = match.group(1 if token_type in [TokenType.EVENT] else 0)
                        token = Token(token_type, token_value)
                        self.tokens.append(token)
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: '{self.source_code[self.current_position]}' Index:{self.current_position}")

            self.current_position += len(match.group(0))

        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens

    def validate_semicolons(self):
        """
        Validates that all appropriate statements are followed by a semicolon.
        Raises a SyntaxError if any rule is violated.
        """
        semicolon_required_tokens = {
            TokenType.CONSOLE_LOG,
            TokenType.CONSOLE_WARN,
            TokenType.CONSOLE_ERROR,
            TokenType.LOGIC_WAIT,
            TokenType.NAVIGATION_REDIRECT,
            TokenType.AUDIO_PLAY,
            TokenType.AUDIO_SET_VOLUME,
            TokenType.AUDIO_STOP,
            TokenType.AUDIO_PAUSE,
            TokenType.AUDIO_RESUME,
            TokenType.LOOKS_SHOW,
            TokenType.LOOKS_HIDE,
            TokenType.LOOKS_SET_TEXT,
            TokenType.LOOKS_SET_PROPERTY,
            TokenType.LOOKS_GET_PROPERTY,
            TokenType.LOOKS_GET_TEXT,
            TokenType.LOOKS_DUPLICATE,
            TokenType.LOOKS_DELETE,
            TokenType.LOOKS_SET_PARENT,
            TokenType.NETWORK_BROADCAST,
            TokenType.NETWORK_GLOBAL_BROADCAST,
            TokenType.NETWORK_GET_USERNAME,
            TokenType.NETWORK_GET_DISPLAYNAME,
            TokenType.NETWORK_GET_USERID,
            TokenType.COOKIES_SET_COOKIE,
            TokenType.COOKIES_INCREASE_COOKIE,
            TokenType.COOKIES_DELETE_COOKIE,
            TokenType.COOKIES_GET_COOKIE,
            TokenType.MATH_ROUND,
            TokenType.MATH_FLOOR,
            TokenType.MATH_RANDOM,
            TokenType.STRINGS_SUBSTRING,
            TokenType.STRINGS_REPLACE,
            TokenType.STRINGS_GET_LENGTH,
            TokenType.STRINGS_SPLIT,
            TokenType.TABLES_NEW,
            TokenType.TABLES_SET_ENTRY,
            TokenType.TABLES_GET_ENTRY,
            TokenType.TABLES_DELETE_ENTRY,
            TokenType.TABLES_GET_LENGTH,
            TokenType.FUNCTIONS_RUN,
        }

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.type in semicolon_required_tokens:
                # Check the next token to ensure it's a semicolon
                if i + 1 < len(self.tokens) and self.tokens[i + 1].type != TokenType.SEMICOLON:
                    raise SyntaxError(f"Expected ';' after '{token.value}'")
            elif token.type in {TokenType.EVENT, TokenType.FUNCTION}:
                # Skip the block for these control structures
                brace_count = 0
                while i < len(self.tokens):
                    if self.tokens[i].type == TokenType.LBRACE:
                        brace_count += 1
                    elif self.tokens[i].type == TokenType.RBRACE:
                        brace_count -= 1
                        if brace_count == 0:
                            break
                    i += 1
            i += 1
