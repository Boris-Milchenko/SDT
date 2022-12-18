import sys, os
from GUI.K_main import Table_Work

if __name__ == '__main__':
    cur = os.path.abspath(__file__)
    app = Table_Work(files = sys.argv[1:], wd = os.path.dirname(cur))
    app.mainloop()
