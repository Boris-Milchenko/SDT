import os, platform

class Csv_Working:
    def __init__(self, wd):
        self.sep = ['/', '\\'][platform.system() == 'Windows']
        self.wd = wd + self.sep

    def preprocess_file(self, file):
        if file[0] == '/':
            return file
        for part in self.wd.split(self.sep):
            if part and part in file:
                return file
        return self.wd + file

    def Cwd(self, file):
        if file[-1] != self.sep:
            file += self.sep
        self.wd = file
        return self.wd

    def Read(self, file):
        file = self.preprocess_file(file)
        try:
            with open(file, 'r', encoding = 'utf-8') as f:
                lines = []
                line = f.readline().strip()
                while line:
                    lines.append(line.split(','))
                    line = f.readline().strip()
        except Exception as _e:
            with open(file, 'w+', encoding = 'utf-8'):
                lines = []

        return lines

    def Write(self, file = 'new.csv', lines = None):
        file = self.preprocess_file(file)
        print(file)
        with open(file, 'w', encoding = 'utf-8') as f:
            if lines:
                for line in lines:
                    n = len(line) - 1
                    for i in range(len(line)):
                        f.write(str(line[i]) + ['', ','][i != n])
                    f.write('\n')

        print('Written!')

    def Del(self, file):
        file = self.preprocess_file(file)
        os.remove(file)

    def Get_Tables(self, directory = None):
        if directory == None:
            directory = self.wd

        files = []
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file() and (entry.name.endswith('.csv') or entry.name.endswith('.зрз')):
                    files.append(entry.name)

        return files

