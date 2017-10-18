# coding: utf-8

from xml.etree.ElementTree import ElementTree
from pymorphy2 import MorphAnalyzer
from rus_to_open import convert_rnc_oc

"""<corpus>
<se>
<w><ana lex="надо" gr="PRAEDIC"></ana>Н`адо</w> 
<w><ana lex="быть" gr="V,ipf,intr,act=n,sg,praet,indic"></ana>б`ыло</w> 
<w><ana lex="либо" gr="CONJ"></ana>л`ибо</w> 
<w><ana lex="вставать" gr="V,ipf,intr,act=inf"></ana>встав`ать</w>
<w><ana lex="и" gr="CONJ"></ana>и</w> 
</se>
</corpus>
"""

from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument('-t', '--text', action='store_true',
               help='Convert xml to text (one token per line).')
p.add_argument('-m', '--mrph', action='store_true',
               help='Convert xml to tab morph format (one token per line).')
p.add_argument('-new', action='store_true', help='New RNC xml format.')
p.add_argument('-old', action='store_true', help='Old RNC xml format.')
p.add_argument('xml', help='Xml file to convert.')
args = p.parse_args()

et = ElementTree(file=args.xml)
i = 1

m = MorphAnalyzer()

if args.new:
    for s in et.findall('se'):
        print 'sent'
        for w in s.findall('w'):
            for a in w.getchildren():
                tag = a.get('gr')
                lex = a.get('lex')
                if a.tail:
                    a = a.tail.strip()
                    if a:
                        tag = convert_rnc_oc(tag).replace(',', ' ')
                        print (str(i) + '\t' + a.replace('`', '') + '\t' +
                                        ' '.join(('0', lex, tag))).encode('utf-8')
                        i += 1
            if w.tail:
                w = w.tail.strip()
                if w:
                    if len(set(w.split())) > 1:
                        for c in w.split():
                            print (str(i) + '\t' + c + '\t' + ' '.join(('0', c, 'PNCT'))).encode('utf-8')
                            i += 1
                    else:
                        print (str(i) + '\t' + w + '\t' +
                               ' '.join(('0', w, 'PNCT'))).encode('utf-8')
        print '/sent'
if args.old:
    for s in et.findall('p'):
        print 'sent'
        for w in s.findall('w'):
            tag = w.get('gr')
            lex = w.get('lex')
            if w.text:
                if a.tail.strip():
                    print (str(i) + '\t' + w.text.replace('`', '') + '\t' +
                                    ' '.join(('0', lex, convert_rnc_oc(tag)))).encode('utf-8')
                    i += 1
            if w.tail:
                if w.tail.strip():
                    if len(set(w.tail.strip())) > 1:
                        for c in w.tail.strip():
                            print (str(i) + '\t' + c + '\t' + ' '.join(('0', c, 'PNCT'))).encode('utf-8')
                            i += 1
                    else:
                        print (str(i) + '\t' + w.tail.strip() + '\t' +
                               ' '.join(('0', w.tail.strip(), 'PNCT'))).encode('utf-8')
        print '/sent'
