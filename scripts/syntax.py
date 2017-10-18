# Программа использует морфологические данные разбора PyMorphy2 и синтаксические правила АОТ для автоматического синтаксического разобра текста на русском языки в NLTK.
# Python 3, NLTK, pymorphy2
# -*- coding: utf-8 -*- 
import nltk
from nltk import load_parser, word_tokenize
import pymorphy2 as pm
import codecs
#import re

## загружаем PyMorphy2
m = pm.MorphAnalyzer()
## открываем (создаем)файл с грамматикой, куда будут записываться правила
f = codecs.open("C:\\nltk_data\\grammars\\book_grammars\\test.fcfg", mode= "w", encoding = "utf-8")
## записываем правила, которые вручную делаем (некоторые на основе правил из АОТ)

f.writelines("% start XP\n")
f.writelines("XP -> NP\n")
f.writelines("XP -> VP\n")
f.writelines("XP -> AdjP\n")
f.writelines("XP -> AdvP\n")
f.writelines("XP -> COMP\n")
f.writelines("XP -> PP\n")
f.writelines("XP -> NUMRNP\n")
f.writelines("XP -> NUMR\n")
f.writelines("XP -> S\n")
f.writelines("XP -> CONJP\n")
f.writelines("XP -> PREDP\n")
f.writelines("XP -> PrtfP\n")


f.writelines("S[-inv] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=0, G=?g]\n") 
f.writelines("S[-inv] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=?p, G=0]\n")
f.writelines("S[-inv] -> AdjP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=0, G=?g]\n") 
f.writelines("S[-inv] -> AdjP[C=nomn, NUM=?n, PER=?p, G=?g] VP[NUM=?n, PER=?p, G=0]\n")
#f.writelines("S[-inv, +1] -> NP[C=nomn, NUM=plur, PER=?p] VP[NUM=?n, PER=0, G=None]\n")
f.writelines("S[+adj] -> NP[C=nomn, NUM=?n, PER=?p, G=?g] AdjP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
f.writelines("S[-inv] -> NUMRNP[C=nomn] VP\n")
f.writelines("S[+inv] -> VP[NUM=?n, PER=0, G=?g] NP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
f.writelines("S[+inv] -> VP[NUM=?n, PER=?p, G=0] NP[C=nomn, NUM=?n, PER=?p, G=?g]\n")
f.writelines("S[+advp] -> AdvP S[+advp]\n")
f.writelines("S[+advp] -> NP[C=gent, NUM=?n, PER=?p, G=?g] AdvP\n")
#f.writelines("S[+infn] -> VP[+infn] VP\n")
f.writelines("S[+predp] -> NP[C=datv] PREDP\n")
f.writelines("S[+comp] -> NP[C=datv] COMP\n")

f.writelines("S -> CONJ S\n") 
f.writelines("S -> NP[C=nomn, NUM=?n] '-' NP[C=nomn, NUM=?n]\n") 
f.writelines("S[+S] -> S ',' CONJ S\n")
f.writelines("S[+S] -> S ',' S\n")
f.writelines("S[+S] -> S ',' VP\n") 

#f.writelines("S[+advp] -> NP[C=datv, NUM=?n, PER=?p, G=?g] VP[+advp]\n")

f.writelines("PREDP -> PREDP  VP[TR=?tr, NUM=0, PER=0, G=0]\n")
f.writelines("PREDP -> AdvP PREDP\n")
f.writelines("PREDP -> PRED\n")


f.writelines("NUMRNP[C=?c] -> NUMR[C=?c] NP[C=?c, NUM=plur]\n") # числительные в неименительном
f.writelines("NUMRNP[C=accs] -> NUMR[C=accs] NP[C=gent]\n") # числительные в винительном
f.writelines("NUMRNP[+nomn, C=nomn] -> NUMR[C=nomn] NP[C=gent]\n")
f.writelines("NUMR[C=?c] -> NUMR[C=?c] NUMR[C=?c]\n") # ????

f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=datv, G=?g, NUM=?n, PER=?p]\n")
f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=loct, G=?g, NUM=?n, PER=?p]\n")
f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=accs, G=?g, NUM=?n, PER=?p]\n")
f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=gent, G=?g, NUM=?n, PER=?p]\n")
f.writelines("PP[C=?c, G=?g, NUM=?n, PER=?p] -> PREP NP[C=ablt, G=?g, NUM=?n, PER=?p]\n") #предлог + ИГ (ПГ)
f.writelines("PP -> PREP NUMRNP[-nomn]\n") #предлог + гуппа числ
f.writelines("PP[+advb] -> AdvP PP\n")
f.writelines("PP -> PP AdvP\n")

f.writelines("AdvP[+conj] -> AdvP CONJ AdvP\n") # ОДНОР_НАР
f.writelines("AdvP[+numr] -> AdvP NUMRNP\n")
# f.writelines("AdvP -> ADVB ADVB\n")
f.writelines("AdvP -> ADVB AdvP\n")
f.writelines("AdvP -> ADVB\n")	
f.writelines("PrtfP[C=?c, G=?g, NUM=?n] -> PRTF[C=?c, G=?g, NUM=?n]\n")	
f.writelines("PrtfP[+pp, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] PP\n")
f.writelines("PrtfP[+instr, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] NP[C=ablt]\n")
f.writelines("PrtfP[+instr, C=?c, G=?g, NUM=?n] -> PrtfP[C=?c, G=?g, NUM=?n] AdvP\n")



f.writelines("NP[+adjf, C=?c, G=?g, NUM=sing] -> AdjP[C=?c, G=?g, NUM=sing] NP[C=?c, G=?g, NUM=sing]\n") # именная группа (ПРИЛ-СУЩ)
f.writelines("NP[+adjf, C=?c, NUM=plur] -> AdjP[C=?c, NUM=plur] NP[C=?c, NUM=plur]\n") # именная группа мн.ч. (ПРИЛ-СУЩ)
f.writelines("NP[+gent, C=?c, G=?g, NUM=?n] -> NP[C=?c, G=?g, NUM=?n] NP[C=gent]\n") #ГЕНИТ_ИГ
f.writelines("NP[+prtf, C=?c, G=?g, NUM=sing] -> PrtfP[C=?c, G=?g, NUM=sing] NP[C=?c, G=?g, NUM=sing]\n") # именная группа (ПРИЛ-СУЩ)
f.writelines("NP[+prtf, C=?c, NUM=plur] -> PrtfP[C=?c, NUM=plur] NP[C=?c, NUM=plur]\n") # именная группа мн.ч. (ПРИЛ-СУЩ)
f.writelines("NP[C=?c, +conj] -> NP[C=?c] CONJ NP[C=?c]\n")
f.writelines("NP[C=?c, G=?g, NUM=?n, PER=?p] -> NOUN[C=?c, G=?g, NUM=?n, PER=?p]\n")
f.writelines("NP[C=?c, NUM=?n, PER=?p, G=?g] -> NPRO[C=?c, NUM=?n, PER=?p, G=?g]\n")
f.writelines("NP[+pp, C=?c, G=?g, NUM=?n] -> NP[C=?c, G=?g, NUM=?n] PP\n")
f.writelines("NP[+prcl, C=?c, G=?g, NUM=?n] ->PRCL NP[C=?c, G=?g, NUM=?n]\n")

f.writelines("NP[+particip, C=?c, NUM=plur] -> NP[C=?c, NUM=?n] ',' PrtfP[C=?c, NUM=?n] \n") 

f.writelines("VP[+advb, TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> AdvP VP[TENSE=?t, TR=?tr, G=?g, NUM=?n, PER=?p]\n") #наречие + глагол (НАРЕЧ_ГЛАГОЛ)
f.writelines("VP[+advb, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] AdvP\n")
f.writelines("VP[+infn, TR=?tr, NUM=?n, PER=?p, G=?g] -> VP[NUM=?n, PER=?p, G=?g] VP[TR=?tr, NUM=0, PER=0, G=0]\n") #ГГ + инфинитив (ПЕР_ГЛАГ_ИНФ)
f.writelines("VP[+objt, NUM=?n, PER=?p, G=?g] -> VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran] NP[C=accs]\n")#глагол + прямое дополнение (ПРЯМ_ДОП)
f.writelines("VP[+objt, NUM=?n, PER=?p, G=?g] -> VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran] NP[C=gent]\n")#глагол + прямое дополнение в генетиве(ПРЯМ_ДОП)
f.writelines("VP[+objt, NUM=?n, PER=?p, G=?g, TR=tran] -> NP[C=accs] VP[-objt, NUM=?n, PER=?p, G=?g, TR=tran]\n")#глагол + прямое дополнение (ПРЯМ_ДОП)
f.writelines("VP[TENSE=?t, G=?g, NUM=?n, PER=?p, TR=?tr] -> INFN[TENSE=?t, G=?g, NUM=?n, PER=?p, TR=?tr]\n") #CHTO ETO??
f.writelines("VP[+instr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NP[C=ablt]\n")
f.writelines("VP[+pp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] PP\n")
f.writelines("VP[+pp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> PP VP[TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
f.writelines("VP[+datv, TENSE=?t, G=?g, NUM=?n, PER=?p] ->VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NP[C=datv]\n")
f.writelines("VP[+adj, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] AdjP[С=ablt]\n")
f.writelines("VP[+comp, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] COMP\n")
f.writelines("VP[+numr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VP[TENSE=?t, G=?g, NUM=?n, PER=?p] NUMRNP\n")
f.writelines("VP[+neg, TENSE=?t, G=?g, NUM=?n, PER=?p] -> 'не' VP[TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
f.writelines("VP[TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p] -> VERB[TR=?tr, TENSE=?t, G=?g, NUM=?n, PER=?p]\n")
#f.writelines("VP[+infn] -> VP VP[+infn]\n")

f.writelines("AdjP[+advb, C=?c, G=?g, NUM=?n] -> AdvP AdjP[C=?c, G=?g, NUM=?n]\n") #наречие + прилагательное (НАР_ПРИЛ)
f.writelines("AdjP[+advb, C=?c, G=?g, NUM=?n] -> AdjP[C=?c, G=?g, NUM=?n] PP\n")
f.writelines("AdjP[C=?c, G=?g, NUM=?n, +conj] -> AdjP[C=?c, G=?g, NUM=?n] CONJ AdjP[C=?c, G=?g, NUM=?n]\n") # ОДНОР_ПРИЛ
f.writelines("AdjP[C=?c, G=?g, NUM=?n] -> ADJF[C=?c, G=?g, NUM=?n]\n")
f.writelines("AdjP[+adjs, G=?g, NUM=?n] -> ADJS[G=?g, NUM=?n]\n")

f.writelines("COMP[+conj] -> COMP CONJ COMP\n")
f.writelines("COMP[+advb] -> AdvP COMP\n")
f.writelines("COMP[+noun, +comp] -> COMP[-comp] NP[C=gent]\n")
f.writelines("COMP[+vp] -> COMP VP\n")

f.writelines("INFN[+conj] -> INFN CONJ INFN\n\n\n") # ОДНОР_ИНФ

f.writelines("CONJP[+vp] -> CONJ VP\n\n\n")

f.close()

## функция, которая переводит нужную нам информацию из пайморфи в вид, читаемый парсером NLTK
## принимает (токенизированное) словосочетание на входе, записывает правила (lexical productions) в тот же файл с грамматикой

def pm2fcfg (phrase): ## phrase - это словосочетание, которое мы разбираем
    f = codecs.open("C:\\nltk_data\\grammars\\book_grammars\\test.fcfg", mode= "a", encoding = "utf-8")
    for x in phrase:
        a = m.parse(x) ## a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
		## от части речи зависит, какие признаки отправляются в грамматику, осюда условия
        for y in a:
            if (y.tag.POS == "NOUN") or (y.tag.POS == "ADJF") or (y.tag.POS == "PRTF"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=3" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADJS") or (y.tag.POS == "PRTS"):
                strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "NUMR"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADVB") or (y.tag.POS == "GRND") or (y.tag.POS == "COMP") or (y.tag.POS == "PRED") or (y.tag.POS == "PRCL") or (y.tag.POS == "INTJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "PREP") or (y.tag.POS == "CONJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                break
            elif (y.tag.POS == "NPRO") & (y.normal_form != "это")& (y.normal_form != "нечего"):
                if ((y.tag.person[0] == "3") & (y.tag.number == "sing")):                    
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "VERB")  or (y.tag.POS == "INFN"):
                if (y.tag.tense == "past"):                    
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + "0" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                elif (y.tag.POS == "INFN"):
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=0, G=0, NUM=0, PER=0, NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + "0" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
    f.close()
                
    
text = input("") ## сюда пишется словосочетание для разбора
words = word_tokenize(text.lower()) ## разбиваем словосочетание на токены

pm2fcfg(words) ## запускаем функцию, описанную выше
cp = load_parser('grammars/book_grammars/test.fcfg', trace=1) ## открываем нашу грамматику, смотрим на разбор в консоли или ещё где
for tree in cp.parse(words):
         print (tree)




