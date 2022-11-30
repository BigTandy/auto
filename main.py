#Bud Patterson

import re
from dataclasses import dataclass
from classdefs import *



# for el in pt.elements:
#     print(f"{el.symbol} {el.name} :: {el.mass}")

# print(pt.elements.symbol("H").name)

GRAMMAR = (
    ("SPACE", ' +'), #Ignore

    #("COMPOUND", r'([0-9]? *[A-Z][a-z]?[0-9]?)+'),
    #("COMPOUND", r'(#?[0-9]?) *(\<|[A-Z][a-z]?[0-9]?|\>)+[0-9]?'),

    # (#[0-9]?)? *((\<)|([A-Z][a-z]?[0-9]?)|(\>))+([0-9]?)

    # (#[0-9]? *)?((\<)|([A-Z][a-z]?[0-9]?)|(\>))+([0-9]?)

    #("COMPOUND",r'(#[0-9]? *)?((\<)|([A-Z][a-z]?[0-9]?)|(\>))+([0-9]?)'),
    ("COMPOUND",r'(#[0-9]? *)?((\()|([A-Z][a-z]?[0-9]?)|(\)))+([0-9]?)'),

    ("ARROW", '-\>'),
    ("PLUS", '\+'),

    ("AMP", '@\S+'), #Ignore for now, going to be used to give commands to the program
    #("SYMBOL", r'(\&|\@)\S*'),

)

#TODO
COMMAND_GRAMMAR = [
    ()
]

SUBGRAMMAR = (
    ("CIGIL", r'#[0-9]+'),
    ("SUBSCRIPT", r'[0-9]+'),
    ("ELEMENT", r'[A-Z][a-z]?'),
    ("SPACE", '( +)|(\t+)'),
    ("GROUP_START", r'\('),
    ("GROUP_END", r'\)'),
    #("GROUP_START", r'\<'),
    #("GROUP_END", r'(?!-)\>'),  # TODO (?!-) ?
)


class TokenizerError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error



class Tokenizer:
    def __init__(self, inp: str, grammar: list | tuple, flags=""):
        self._pos = 0
        self.stream = inp

        self.grammar = grammar
        self.flags = ""

        #Its done this way to catch unsupported flags
        flags = flags.lower()
        # if 'w' in flags: self.flags += 'w'
        # else: raise NotImplemented("Incorrect Flag")


    def __call__(self, *args, **kwargs):
        out = []
        for _ in self:
            out.append(_)
        return out

    def __iter__(self):
        return self

    def done(self):
        return self._pos >= len(self.stream)

    def __next__(self):
        if not self.done():
            return self.scan_next()
        else:
            raise StopIteration

    def scan_next(self):

        #matches = []
        for name, rule in self.grammar:
            #matches.append((name, re.match(rule, self.stream[self._pos:])))
            m = re.match(rule, self.stream[self._pos:])

            #NEW vvvvv
            if 'g' in self.flags:
                pass
                #return m.groups()
            # ^^^^^^^

            if m:
                self._pos += m.end()                       #NEW~vvvvv
                return (name, m.string[m.start():m.end()])
        else:
            #raise Tokenizer_Error(f"Invalid Token") #where end? # : '{self.stream[self._pos:]}'
            raise TokenizerError(f"Invalid Token:: {self.stream[self._pos:]}")





# # "Al2<SO4>3"
# for _ in tokenizer("Al + CuSO4 -> Cu + Al2<SO4>3", GRAMMAR):
#     print(_)




class ParserError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class Parser:
    def __init__(self, inp: str, gram=GRAMMAR, echo=False):
        #TODO:
        # Check for syntatical correctness
        self.tokenizer = Tokenizer(inp, gram, flags='g')
        self.tokens = self.tokenizer()
        self.echo: bool = echo
        if echo:
            for _ in self.tokens: print("Token:", _)

        self.meaning = [None]

        for token in self.tokens:
            match token[0]:
                case "SPACE": continue
                case "COMPOUND":
                    try:
                        self.meaning.append(self.COMPOUND_PARSER(token))
                    except ValueError as e:
                        raise ParserError(e)
                case "ARROW":
                    self.meaning.append(token[0])
                case "PLUS":
                    self.meaning.append(token[0])
                case "AMP":
                    #Directive Parsing
                    match token[1][1:].lower():
                        case "cls":
                            pass  #TODO make clear screen
                        case "e" | "echo":
                            self.echo = True
                        case "b":
                            pass  #TODO Call Balancer
                        case "l":
                            pass  #TODO Call limiting reaction
                        case "m":
                            pass  #TODO Call Molecular Moles stuffs


        if echo: print(f"MEAN: {self.meaning}")

        pluses = 0
        arrow = False
        for token in self.meaning:
            if token == 'PLUS': pluses += 1
            if token == 'ARROW': arrow = True


    def __call__(self):
        return self.meaning[1:]


    def balance(self):
        pass


    def COMPOUND_PARSER(self, tk):

        if self.echo: print(f"tk: {tk}")

        subSearch = Tokenizer(tk[1], SUBGRAMMAR)()

        comp = Compound()

        coeff = 1
        if subSearch[0][0] == "CIGIL":
            coeff = int(subSearch[0][1][1:])

        comp.coeff = coeff

        current_grouping = [False]

        for tdx, tok in enumerate(subSearch):
            if tok[0] == "SPACE":
                continue

            if current_grouping[0]:
                if self.echo: print("CG: ", current_grouping)

            match tok[0]:
                case "CIGIL":
                    continue
                case "ELEMENT":
                    if current_grouping[0]:
                        current_grouping[1] + elem(pt.elements.symbol(tok[1]), 1)
                    else:
                        comp + elem(pt.elements.symbol(tok[1]), 1)
                case "SUBSCRIPT":
                    if current_grouping[0]:
                        current_grouping[1].subs_set(int(tok[1]))
                    else:
                        comp.subs_set(int(tok[1]))
                case "GROUP_START":
                    current_grouping.clear()
                    current_grouping.append(True)
                    current_grouping.append(Compound())

                case "GROUP_END":
                    if not current_grouping[0]: raise ParserError("Unmatched 'GROUP_END' Token")
                    comp + current_grouping[1]
                    current_grouping.clear()
                    current_grouping.append(False)




            if self.echo: print("tok ", tdx, " ", tok)

        if self.echo: print(f"COMP: {comp}")

        starts = 0
        stops = 0
        for token in subSearch:
            if token[0] == "GROUP_START": starts += 1
            elif token[0] == "GROUP_END": stops += 1
            else: continue
        if starts != stops: raise ParserError(f"Unmatched Grouping, Starts: {starts}, Stops: {stops}")

        return comp








#Parser("Al + CuSO4 -> Cu + Al2<SO4>3")


#import AST as a

#AbST = a.Start_Node()

while True:
    try:
        meaning = Parser(input("?: "), echo=True)()
        print(meaning)
        #for _ in meaning: print(_)
        #for _ in meaning:
            #AbST + a.Node(_)
    except TokenizerError as e:
        print(f"Token Error: {e}")
        continue
    except ParserError as e:
        print(f"Parser Error:", e)
        continue


    if "ARROW" in meaning:
        pass  #TODO Call equation Solver
    else:
        #Print info on compound
        print(meaning)

    # for token in meaning:
    #     #TODO Actually impliment shit or something
    #     pass

