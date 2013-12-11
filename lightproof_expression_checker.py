# -*- encoding: UTF-8 -*-
# External checker for Lightproof regular expressions.
# 2013 - Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import pygtk
pygtk.require('2.0')
import gtk

import sys

TEMP_PATH = './temp'
LIGHTPROOF_DIC = './temp/pythonpath/lightproof_%s.py'

def open_file():
    ''' https://github.com/majorsilence/pygtknotebook/blob/master/examples/more-pygtk/gtk-filechooser-dialog-example.py '''

    dialog = gtk.FileChooserDialog(title="Select a File", action=gtk.FILE_CHOOSER_ACTION_OPEN,
        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    text_filter = gtk.FileFilter()
    text_filter.set_name("OXT files")
    text_filter.add_pattern("*.oxt")

    all_filter = gtk.FileFilter()
    all_filter.set_name("All files")
    all_filter.add_pattern("*")
    
    dialog.add_filter(text_filter)
    dialog.add_filter(all_filter)
    
    response = dialog.run()
            
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()

    elif response == gtk.RESPONSE_CANCEL:
        filename = None

    dialog.destroy()

    return filename

def show_message(msg, wait=True, buttons=gtk.BUTTONS_CLOSE, icon=gtk.MESSAGE_INFO):
    md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, icon, buttons, msg)
    
    if wait:
        ret = md.run()
        md.destroy()
        return ret
    else:
        md.show_all()
        return md

def extract_file(oxt):
    import zipfile

    if not zipfile.is_zipfile(oxt):
        show_message(msg='Invalid OXT file.',icon=gtk.MESSAGE_ERROR)
        sys.exit(0)

    with zipfile.ZipFile(oxt, "r") as z:
        z.extractall(TEMP_PATH)

def get_language():
    import os

    for root, dirs, files in os.walk(TEMP_PATH):
        for file in files:
            if file.endswith(".aff"):
                 return file[:-4]

def load_dic(path):
    import imp
    lightproof = imp.load_source('lightproof', path)
    return lightproof.dic

def compile_rules(dic):
    import re
    errors = []
    
    position = 1

    for i in dic:
        try:
            i[0] = re.compile(i[0])
        except Exception, e:
            msg = e.message or 'Unknown error.'
            errors.append(u'Bad regular expression at position %d:\nError message: %s\nExpression: %s\nLine: %s\n' % (position, msg, i[0], i))

        position += 1

    return errors

def write_errors_to_file(errors):
    try:
        import codecs
        from datetime import datetime

        filename = 'invalid_rules_%s.log' % datetime.now().strftime('%d-%m-%Y-%H-%M')

        f = codecs.open(filename, 'w', 'utf-8')
        f.write('# -*- encoding: UTF-8 -*-\n')

        for s in errors:
            f.write(s)
        
        f.close()

        return filename

    except Exception, e:
        message = 'Error while creating log file: ', e.message or 'Unknown error.'
        show_message(msg=message, icon=gtk.MESSAGE_ERROR)
        sys.exit(0)

def check_rules(rules):
    # TODO: Doesn't show...
    md = show_message(msg='Checking regular expressions....', wait=False)

    errors = compile_rules(rules)

    md.destroy()

    if errors:
        filename = write_errors_to_file(errors)

        if filename:
            ret = show_message(msg='Bad regular expressions found.\nOpen log file?',buttons=gtk.BUTTONS_YES_NO)
            
            if ret == gtk.RESPONSE_YES:
                import os

                if sys.platform == 'linux2':
                    os.system('gedit %s' % filename)
                else:
                    os.system('notepad %s' % filename)
    else:
        show_message(msg='Done. Everything is fine.')

def run():
    filename = open_file()

    if filename:
        extract_file(filename)

        try:
            lang = get_language()
            dic = load_dic(LIGHTPROOF_DIC % lang)
            check_rules(dic)
        except Exception, e:
            show_message(msg=e.message, icon=gtk.MESSAGE_ERROR)
        finally:
            import shutil
            shutil.rmtree(TEMP_PATH)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == '-compile':
            print u'Compiling...'
            
            import py_compile
            py_compile.compile('lightproof_expression_checker.py')
            
            print 'Compiled.'
            sys.exit(0)
    
    run()