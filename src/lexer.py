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

    DEF = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    REPEAT_FOREVER = auto()

    # Operators and Punctuation
    EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    NOT_EQUAL = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LSQUARE = auto()
    RSQUARE = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    CONCAT = auto()

    # Other
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    EOF = auto()
    COMMENT = auto()
    EVENT = auto()


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
            (r'Console:Log\b', TokenType.CONSOLE_LOG),
            (r'Console:Warn\b', TokenType.CONSOLE_WARN),
            (r'Console:Error\b', TokenType.CONSOLE_ERROR),
            (r'Logic:Wait\b', TokenType.LOGIC_WAIT),
            (r'Navigation:Redirect\b', TokenType.NAVIGATION_REDIRECT),
            (r'Audio:Play\b', TokenType.AUDIO_PLAY),
            (r'Audio:SetVolume\b', TokenType.AUDIO_SET_VOLUME),
            (r'Audio:Stop\b', TokenType.AUDIO_STOP),
            (r'Audio:Pause\b', TokenType.AUDIO_PAUSE),
            (r'Audio:Resume\b', TokenType.AUDIO_RESUME),
            (r'Looks:Show\b', TokenType.LOOKS_SHOW),
            (r'Looks:Hide\b', TokenType.LOOKS_HIDE),
            (r'Looks:SetText\b', TokenType.LOOKS_SET_TEXT),
            (r'Looks:SetProperty\b', TokenType.LOOKS_SET_PROPERTY),
            (r'Looks:GetProperty\b', TokenType.LOOKS_GET_PROPERTY),
            (r'Looks:GetText\b', TokenType.LOOKS_GET_TEXT),
            (r'Looks:Duplicate\b', TokenType.LOOKS_DUPLICATE),
            (r'Looks:Delete\b', TokenType.LOOKS_DELETE),
            (r'Looks:SetParent\b', TokenType.LOOKS_SET_PARENT),
            (r'Network:Broadcast\b', TokenType.NETWORK_BROADCAST),
            (r'Network:GlobalBroadcast\b', TokenType.NETWORK_GLOBAL_BROADCAST),
            (r'Network:GetUsername\b', TokenType.NETWORK_GET_USERNAME),
            (r'Network:GetDisplayName\b', TokenType.NETWORK_GET_DISPLAYNAME),
            (r'Network:GetUserId\b', TokenType.NETWORK_GET_USERID),
            (r'Cookies:SetCookie\b', TokenType.COOKIES_SET_COOKIE),
            (r'Cookies:IncreaseCookie\b', TokenType.COOKIES_INCREASE_COOKIE),
            (r'Cookies:DeleteCookie\b', TokenType.COOKIES_DELETE_COOKIE),
            (r'Cookies:GetCookie\b', TokenType.COOKIES_GET_COOKIE),
            (r'Math:Round\b', TokenType.MATH_ROUND),
            (r'Math:Floor\b', TokenType.MATH_FLOOR),
            (r'Math:Random\b', TokenType.MATH_RANDOM),
            (r'Strings:Substring\b', TokenType.STRINGS_SUBSTRING),
            (r'Strings:Replace\b', TokenType.STRINGS_REPLACE),
            (r'Strings:GetLength\b', TokenType.STRINGS_GET_LENGTH),
            (r'Strings:Split\b', TokenType.STRINGS_SPLIT),
            (r'Tables:New\b', TokenType.TABLES_NEW),
            (r'Tables:SetEntry\b', TokenType.TABLES_SET_ENTRY),
            (r'Tables:GetEntry\b', TokenType.TABLES_GET_ENTRY),
            (r'Tables:DeleteEntry\b', TokenType.TABLES_DELETE_ENTRY),
            (r'Tables:GetLength\b', TokenType.TABLES_GET_LENGTH),
            (r'Functions:Run\b', TokenType.FUNCTIONS_RUN),
            (r'\bdef\b', TokenType.DEF),
            (r'\bif\b', TokenType.IF),
            (r'\bthen\b', TokenType.THEN),
            (r'\belse\b', TokenType.ELSE),
            (r'\brepeat_forever\b', TokenType.REPEAT_FOREVER),
            (r'@event ([a-zA-Z_0-9]*)', TokenType.EVENT),
            (r'==', TokenType.EQUALS),
            (r'>', TokenType.GREATER_THAN),
            (r'<', TokenType.LESS_THAN),
            (r'!=', TokenType.NOT_EQUAL),
            (r'=', TokenType.ASSIGN),
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULTIPLY),
            (r'/', TokenType.DIVIDE),
            (r'%', TokenType.MODULO),
            (r'::', TokenType.CONCAT),
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\[', TokenType.LSQUARE),
            (r'\]', TokenType.RSQUARE),
            (r'\d+', TokenType.NUMBER),
            (r'\".*?\"', TokenType.STRING),
            (r'[a-zA-Z_][a-zA-Z0-9_\-\?]*', TokenType.IDENTIFIER),
            (r'#.*', None), # Ignore comments
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
