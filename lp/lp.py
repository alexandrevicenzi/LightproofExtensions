#!/usr/bin/python
#!/opt/libreoffice4.1/program/python
import socket  # only on win32-OOo3.0.0
import uno, os, time

LIBREOFFICE = "soffice"
#LIBREOFFICE = "/opt/libreoffice4.1/program/soffice"
#LIGHTPROOF = "com.sun.star.linguistic2.Proofreader"
#LIGHTPROOF = "org.openoffice.comp.pyuno.Lightproof.lightproof_hu"
LIGHTPROOF = "org.openoffice.comp.pyuno.Lightproof.en"
TESTLANG = "en-US"

from com.sun.star.lang import Locale 

# get the uno component context from the PyUNO runtime
localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )

# connect to the running office (start it, if needed)
while 1:
  try:
#    ctx = resolver.resolve( "uno:socket,host=localhost,port=42424;urp;StarOffice.ComponentContext" )
    ctx = resolver.resolve( "uno:pipe,name=addtemppipe;urp;StarOffice.ComponentContext" )
    break
  except:
    print ('Start LibreOffice...')
#    os.system(LIBREOFFICE + ' "--accept=socket,host=localhost,port=42424;urp;StarOffice.ServiceManager" --headless --nologo --nofirststartwizard &')
    os.system(LIBREOFFICE + ' --accept="pipe,name=addtemppipe;urp;StarOffice.ServiceManager" --headless --nologo --nofirststartwizard &')
    time.sleep(4)

smgr = ctx.ServiceManager

# spell checker
spellchecker = smgr.createInstanceWithContext("com.sun.star.linguistic2.SpellChecker", localContext)
# grammar checker
gc = smgr.createInstanceWithContext(LIGHTPROOF, localContext)

# check object
print ("Grammar checker: ", str(gc))
# eg. spell("foobar", "en_US")

def spell(word, lang):
	loc = Locale(lang[0:2], lang[3:5], "")
	print (loc)
	res = spellchecker.isValid(word, loc, ())
	if res:
		print ("ok")
	else:
		sug = spellchecker.spell(word, loc, ())
		if sug:
			print ("Suggestions:")
			for i in sug.getAlternatives():
				print (i)
	#if lang == "en-US":
	t = u"And  an an fox , is." # double space and space before comma
	bu = gc.doProofreading(5, t, loc, 0, len(t), ())
	print (bu.aDocumentIdentifier)
	print (bu.aErrors)
	print (bu.aText)

spell("foobarxxx", TESTLANG)
