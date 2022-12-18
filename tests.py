import unittest

from GUI.K_main import Table_Work
from GUI.K_table import Table

class Test(unittest.TestCase):
    def setUp(self):
        self.clauses = Test_Rules()
        self.main = Table_Work('/home/Borey/Documents/test.csv', '/home/Borey/Python/SDT')
        self.main.run_command(command = 'q')

        self.cur_table = self.main.table_notebook.tab(self.main.table_notebook.select(), 'text')
        self.cur_table = self.main.tables[self.cur_table][1].table

    def test_delTable(self):
        res = len(self.main.tables)
        self.main.run_command(command = 'q')

        self.assertEqual(len(self.main.tables) - res, -1)

    def test_pick(self):
        self.main.run_command(command = 'new ~1.csv~')
        new_table = self.main.tables['1.csv'][1].table
        before = len(new_table.get_children())

        self.main.run_command(command = 'p ~1.csv~')
        self.assertEqual(len(new_table.get_children()) - before, len(self.cur_table.get_children()))

    def test_addTable(self):
        datas = [['~1.csv~'], ['~1.csv~', '~3.csv~'], ['~h.csv~', '~4.csv~', '~kuh.csv~'], []]
        for data in datas:
            self.assertTrue(self.clauses.add_table(data))

    def test_addRow(self):
        datas = [[], ['~fbjh~', '~h~', '~42~', '~jhfk~', '~gis~'], ['~kjg~', '~f~', '~53~']]
        for data in datas:
            self.assertTrue(self.clauses.add_row(data))

    def test_delRows(self):
        datas = ['0,1..3', '2', '0..4', '1,3']
        controls = [4, 1, 5, 2]

        for i in range(len(datas)):
            self.assertTrue(self.clauses.del_rows(arg = datas[i], control = controls[i]))

    def test_changeRow(self):
        datas = ['3 name ~Kule~', '~Heart~ ~ku~ i', '(name = ~John~) sex ~g~ 1']
        control_ids = [[3, 1], [4, 5], [0, 2]]
        exps = ['Kule', 'ku', 'g']

        for i in range(len(datas)):
            self.assertTrue(self.clauses.change_row(datas[i], control_ids[i], exps[i]))


class Test_Rules:
    def init(self):
        self.main = Table_Work('/home/Borey/Documents/test.csv', '/home/Borey/Python/SDT')
        self.main.run_command(command = 'q')

        self.cur_table = self.main.table_notebook.tab(self.main.table_notebook.select(), 'text')
        self.cur_table = self.main.tables[self.cur_table][1].table

    def add_table(self, args):
        self.init()

        res = len(self.main.tables)
        self.main.run_command(command = 'new ' + ' '.join(args))

        return (len(self.main.tables) - res) == len(args)

    def add_row(self, args):
        self.init()

        l = len(self.cur_table.get_children())

        self.main.run_command(command = 'n ' + ' '.join(args))

        res = self.cur_table.item(self.cur_table.get_children()[l], 'values')
        for i in range(len(args)):
            if res[i+1] != args[i][1:-1]:
                return False
        return True

    def del_rows(self, arg, control):
        self.init()

        before = len(self.cur_table.get_children())
        self.main.run_command(command = 'd ' + arg)

        return (before - len(self.cur_table.get_children())) == control

    def change_row(self, arg, control_id, exp):
        self.init()

        self.main.run_command(command = 'r ' + arg)

        res = self.cur_table.item(self.cur_table.get_children()[control_id[0]], 'values')[control_id[1]]

        return res == exp


if __name__ == '__main__':
    unittest.main()

