from tkinter import ttk
from sources import Columns, int_cols

class Table(ttk.Frame):
    def __init__(self, container, lines, lang):
        super().__init__(container)
        
        self.columns = list(Columns[lang].keys())
        crutch = {0: 50, 2: 40, 3: 60}

        self.table = ttk.Treeview(self, columns = self.columns, show='headings')
        self.last = 0
        for i, column in enumerate(self.columns):
            if i in [0, 2, 3]:
                self.table.column(column, width = crutch[i], stretch='NO', anchor = 'center')
            else:
                self.table.column(column)
            self.table.heading(column, text = column.capitalize())

        scrollbars = []
        pars = [['vertical', 'right', 'x'], ['horizontal', 'bottom', 'y']]
        for i in range(len(pars)):
            scrollbars.append(ttk.Scrollbar(self, orient = pars[i][0]))
            scrollbars[i].pack(side = pars[i][1], fill = pars[i][2])


        scrollbars[0].configure(command = self.table.yview)
        scrollbars[1].configure(command = self.table.xview)
        self.table.configure(yscrollcommand = scrollbars[0].set)
        self.table.configure(xscrollcommand = scrollbars[1].set)

        if lines:
            self.Write(lines)


        self.table.pack(fill = 'both', expand = True)

        self.pack(fill = 'both', expand = True)

    def Get_Item(self, descr, isrow):
        rows = self.table.get_children()
        if isrow:
            values = self.table.item(rows[int(descr)], 'values')
            return {self.columns[i] : values[i] for i in range(len(values))}
        else:
            return {i: self.table.set(rows[i], descr) for i in range(len(rows))}

    def Read(self, scope, log=False):
        rows = self.table.get_children()
        data = []
        for i in scope:
            data.append(self.table.item(rows[i], 'values'))
        return data

    def Write(self, values):
        for value in values:
            self.table.insert('', text = self.last, index = 'end', values = (self.last, *value[1:]))
            self.last += 1

    def Sort(self, column, order):
        items = self.table.get_children()
        columns = [(self.table.set(item, column), self.table.item(item, 'values')) for item in items]
        if column in int_cols:
            columns = [(int(column[0]), column[1]) for column in columns]
        columns.sort(reverse=(order in ['desc', 'убыв']))

        scope = [i for i in range(len(items))]
        self.Del_Rows(scope)
        self.Write([column[1] for column in columns])

    def Del_Rows(self, scope):
        rows = self.table.get_children()
        for i in scope:
            self.table.delete(rows[i])
            self.last -= 1

        if self.last != 0:
            start = max(0, min(scope) - 1)
            self.__update(start)

    # i - inclusion, e - word itself, c - change all inclusions in whole row
    def Change_Rows(self, what, subst, scope, num, mode):
        if num == None:
            num = 100000000000

        if what in self.columns:
            self.__change_rows_by_column(what, subst, scope, num)
        else:
            self.__change_rows_by_name(what, subst, scope, num, mode)

    def __change_rows_by_column(self, col, subst, scope, num):
        rows = self.table.get_children()
        for i in scope:
            if num <= 0:
                break
            self.table.set(rows[i], column = col, value = subst)
            num -= 1

    def __change_rows_by_name(self, search, subst, scope, num, mode):
        modes = {
            0: lambda x, y: x in y,
            1: lambda x, y: x == y,
        }

        rows = self.table.get_children()
        if mode == None:
            mode = 'i'

        fl = 'e' in mode
        for i in scope:
            for j, value in enumerate(self.table.item(rows[i], 'values')):
                if modes[fl](search, value):
                    self.table.set(rows[i], self.columns[j], subst)
                    num -= 1

                    if not 'c' in mode:
                        break

                if num <= 0:
                    break

    def __update(self, start):
        rows = self.table.get_children()
        if start == 0:
            self.last = 0
        else:
            self.last = int(self.table.set(rows[start], column = 'num'))
        for i in range(start, len(rows)):
            self.table.set(rows[i], column = self.columns[0], value = self.last)
            self.last += 1
