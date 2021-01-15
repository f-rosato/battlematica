from battlematica import Bot, translate_battlang_file
# translate_battlang_string is also available


TEAM_1 = 1

mybot = Bot(100, 100, 0, TEAM_1)
my_battlang_ai = translate_battlang_file('./sample_battlang_ai/ultimate.blng')
mybot.set_ai(my_battlang_ai)
