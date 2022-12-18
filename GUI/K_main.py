import platform, subprocess, os, sys, traceback
import tkinter as tk
from tkinter import ttk
from Translator.K_lexer import Lexer
from Translator.K_parser import Parser
from Translator.K_runner import Runner
from Translator.token import token_types
from External.K_csv import Csv_Working
from External.K_db import Db_Working
from GUI.K_table import Table
from GUI.log_frame import Log
from sources import *

class Table_Work(tk.Tk):
    def __init__(self, files, wd):
        super().__init__()

        self.Db = Db_Working()
        self.Csv = Csv_Working(wd = wd)
        self.lang = int(self.Csv.Read('.config')[0][0])
        self.Lexer = Lexer()
        self.Parser = Parser()
        self.Runner = Runner(self)

        self.modifiers = {
            'ALL': token_types['ALL_MODE'].regex.split('|'),
        }

        self.table_notebook = ttk.Notebook(self)
        self.table_notebook.pack(expand = True, fill = 'both')
        self.tables = {}

        self.replace = True

        self.title(main_title[self.lang])
        self.geometry(f'{main_width}x{main_height}+{main_x_offset}+{main_y_offset}')

        self.command_entry = ttk.Entry(self, width=main_width, state='disabled')
        self.command_entry.pack(anchor='se', side='bottom')

        self.Bindings = {
            '<t>': self.change_tab,
            '<T>': self.change_tab,
            '<Cyrillic_te>': self.change_tab,
            '<Cyrillic_TE>': self.change_tab,
            '<colon>': self.to_command_mode,
        }

        self.bind_all()
        self.bind('<Return>', self.run_command)
        self.bind('<Escape>', lambda replace: self.abort_enterings(replace = False))
        #self.bind('<Any-Key>', lambda e: print(e.keysym))

        self.echo(main_intro[self.lang], 1)
        self.Add_Tables(files, modifier = '', lang = self.lang)

# HELPFUL, USER INTERFACE
    def bind_all(self):
        for trig, event in self.Bindings.items():
            self.bind(trig, event)

    def ubind_all(self):
        for trig in self.Bindings.keys():
            self.unbind(trig)

    def change_tab(self, event = None):
        tabs = self.table_notebook.tabs()
        cur = self.table_notebook.index(self.table_notebook.select())
        cur = (cur + [-1, 1][event.keysym in ['t', 'Cyrillic_te']]) % len(tabs)

        self.table_notebook.select(tabs[cur])

    def echo(self, data, mode=0, pos = 0):
        data = str(data)
        if mode == 0:
            self.command_entry['state'] = 'normal'
            self.command_entry.delete(0, 'end')
            self.command_entry.insert(pos, data)
            self.command_entry['state'] = 'disabled'
        elif mode == 1:
            if not 'log' in self.tables.keys():
                log = Log(container = self.table_notebook, text=data)
                self.table_notebook.add(log, text = 'log')
                self.tables['log'] = [len(self.tables), log]
            else:
                self.tables['log'][1].Out(data)

    def manual(self, event = None):
        file = ['README_en.txt', 'README_ru.txt'][self.lang]
        if platform.system() == 'Darwin':
            subprocess.call(('open', file))
        elif platform.system() == 'Windows':
            os.startfile(file)
        else:
            subprocess.call(('xdg-open', file))

    def to_command_mode(self, event):
        self.ubind_all()
        self.command_entry['state'] = 'normal'
        if self.replace:
            self.command_entry.delete(0, 'end')
        self.command_entry.focus_set()

    def run_command(self, event = None, command = None):
        try:
            if not command:
                command = self.command_entry.get()
            
            if not command:
                self.abort_enterings(replace = True)
                return
                
            command += '|'
            exprs = self.Lexer.Lex_Analysis(code = command)
            exprs = self.Parser.Parse(exprs)
            self.Runner.Run(exprs)

        except Exception as _e:
            self.echo(traceback.format_exc(chain=True), 1)

        finally:
            self.abort_enterings(replace = True)

    def abort_enterings(self, event = None, replace = True):
        self.replace = replace
        self.command_entry['state'] = 'disabled'
        self.bind_all()


# MAIN
    def Add_Tables(self, titles, modifier, lang = None):
        if lang == None:
            lang = self.lang
        if not isinstance(titles, (list, tuple, set)):
            titles = [titles]

        for title in titles:
            data = self.__choose_handler(title).Read(title)

            table_frame = Table(container = self.table_notebook, lines = data, lang = lang)
            self.table_notebook.add(table_frame, text = title)
            self.tables[title] = [len(self.tables), table_frame]

    def Connect(self, host, username, password, db):
        self.Db.Connect(host, username, password, db)

    def Get_Item(self, table, descr, isrow):
        table_name = self.__modifier(table, '')[0]
        table = self.tables[table_name][1]
        return table.Get_Item(descr, isrow)

    def Get_Tables(self, source):
        tables = self.__choose_handler(source, mode=1).Get_Tables(source)
        self.echo(tables, 0)

    def Insert(self, tables, modifier, rows):
        table_names = self.__modifier(tables, modifier)
        for table_name in table_names:
            table = self.tables[table_name][1]
            table.Write(rows)

    def Change_Rows(self, table_name, modifier, scope, condition, what, subst, num, mode):
        table_names = self.__modifier(table_name, modifier)

        for table_name in table_names:
            table = self.tables[table_name][1]
            scope1 = self.__unchaos_scope(scope, table.table)
            scope1 = self.__unchaos_condition(scope1, condition, table.table)
            table.Change_Rows(what, subst, scope1, num, mode)

    def Transfer(self, source, dests, modifier, scope, condition, mode):
        dest_tables = self.__modifier(dests, modifier)

        if not 'w' in mode or source != None:
            source = self.__modifier(source, '')
            source_table = self.tables[source[0]][1]

        data_to_write = {}
        for dest_table_name in dest_tables:
            dest_table = self.tables[dest_table_name][1]
            if source == None:
                source_table = dest_table

            scope1 = self.__unchaos_scope(scope, source_table.table)
            scope1 = self.__unchaos_condition(scope1, condition, source_table.table)
            data = source_table.Read(scope1)
            data_to_write[dest_table_name] = data

            if '0' in mode:
                source_table.Del_Rows(scope1)

            if 'w' in mode:
                dest_table.Del_Rows(self.__unchaos_scope(None, dest_table.table))

        for table_name in data_to_write.keys():
            table = self.tables[table_name][1]
            table.Write(data_to_write[table_name])

            if 'w' in mode:
                self.__choose_handler(table_name).Write(table_name, data_to_write[table_name])

    def Filter(self, table_names, modifier, scope, condition):
        table_names = self.__modifier(table_names, modifier)

        if scope or condition:
            for table_name in table_names:
                table = self.tables[table_name][1]
                scope1 = self.__unchaos_scope(scope, table.table)
                scope1 = self.__unchaos_condition(scope1, condition, table.table, inverse=True)

                table.Del_Rows(scope1)

        else:
            for table_name in table_names:
                table = self.tables[table_name][1]
                scope1 = self.__unchaos_scope(scope, table.table)

                data = self.__choose_handler(table_name).Read(table_name)
                table.Del_Rows(scope1)
                table.Write(data)

    def Quit(self, option, titles, modifier):
        if option in ['Q', 'В']:
            sys.exit()

        titles = self.__modifier(titles, modifier)

        for title in titles:
            self.table_notebook.forget(self.tables[title][1])
            del self.tables[title]

    def Del(self, table_names, modifier, scope, condition):
        table_names = self.__modifier(table_names, modifier)

        if scope == None and condition == None:
            for table_name in table_names:
                table = self.tables[table_name][1]
                self.__choose_handler(table_name).Del(table_name)
                self.table_notebook.forget(table)
                del self.tables[table_name]

        else:
            for table_name in table_names:
                table = self.tables[table_name][1]

                scope1 = self.__unchaos_scope(scope, table.table)
                scope1 = self.__unchaos_condition(scope1, condition, table.table)

                table.Del_Rows(scope1)

    def Sort(self, table_names, modifier, column, order):
        table_names = self.__modifier(table_names, modifier)

        for table_name in table_names:
            table = self.tables[table_name][1]
            table.Sort(column, order)

    def Get_Length(self, table_name):
        table_names = self.__modifier(table_name, '')
        for table_name in table_names:
            self.echo(len(self.tables[table_name][1].table.get_children()), mode = 0)


# HELPFUL, INNER LOGIC
    def __unchaos_scope(self, scope, table):
        if isinstance(scope, int):
            return [scope]
        if scope == None:
            return [i for i in range(len(table.get_children()))]
        return scope

    def __unchaos_condition(self, scope, condition, table, inverse=False):
        if condition == None:
            return scope
        rows = table.get_children()
        ret_scope = []
        for i in scope:
            subst = table.item(rows[i], 'values')
            conditio = self.Runner.run(condition, subst = subst)
            if conditio in Columns[self.lang].keys():
                return scope
            if conditio ^ inverse:
                ret_scope.append(i)
        return ret_scope

    def __choose_handler(self, shard, mode = 0):
        if mode == 0:
            if '.' in shard:
                return self.Csv
            return self.Db
        else:
            if shard == None:
                return self.Db
            return self.Csv

    def __modifier(self, table_names, modifier):
        if not table_names:
            table_names = [self.table_notebook.tab(self.table_notebook.select(), 'text')]
        elif not isinstance(table_names, (tuple, list, set)):
            table_names = [table_names]

        for option in self.modifiers['ALL']:
            if option in modifier:
                table_names = list(self.tables.keys())

        return table_names
