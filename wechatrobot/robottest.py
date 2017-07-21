# -*- coding:utf-8 -*-

from wxpy import *

bot = Bot()

hellokitty = bot.friends().search(u'小渣女')[0]

@bot.register(hellokitty)
def print_messages(msg):
    print(msg)
    hellokitty.send(u'浪起来!')

embed()