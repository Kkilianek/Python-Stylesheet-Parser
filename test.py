from lexer import Lexer
from parser import Parser

good_string = '''
//to jest komentarz, np. z nazwą pliku: correct.ppap
#abc
	background: url(watch?v=Ct6BUPvE2sM);
	color: #f00;
	box-shadow: none;
	text-shadow: none;

.def
	content: "see below";

p > pre
	border: 1px solid #999;
	page-break-inside: avoid;

div + p,
div > p
	font-weight: bolder

p img
	max-width: 100% !important;

pine + apple,
* + * // * jest poprawnym selektorem
	orphans: 3;
	widows: 3rem;

a:visited
	color: white;
'''

bad_string = '''
p + + q // kombinator (np. +, >) nie może pojawić się więcej niż raz między selektorami
	content: "see below";
	border: 1px solid #999;
	page-break-inside: avoid;

div+p,
div>p
    font-size: smaller; // nie cztery spacje to niepoprawne wcięcie
		font-family: serif; // ale zbyt duże wcięcie to też problem
	font-weight: bolder; // powinna być tabulacja, jak tutaj
	font-style: normal; // ta linia jest dobrze wcięta

pine + apple
	max-width: 100% !oops; // !important jest jedynym słowem kluczowym z !

foo _bar, // identyfikatory poprawne
&baz, // identyfikator niepoprawny
:quax // ten też jest poprawny
	display: flex // brak średnika jest niedopuszczalny między deklaracjami
	margin: 1px // ale jest OK na końcu
'''


if __name__ == '__main__':
    lexer = Lexer(good_string)
    print(lexer.tokens)

    parser = Parser(lexer)
    parser.start()

