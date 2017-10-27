import re
import sqlite3


class Genome(object):
    def __init__(self, identifier, datafilename):
        self._identifier = identifier
        self._dataFileName = datafilename
        self._sequence_dictionary = {}
        self._databaseName = "genome.db"
        self._connection = None
        self._cursor = None

    def parsefile(self, filename):
        tab_expression = re.compile(r'\t')
        comma_expression = re.compile(r',')
        semi_colon_expression = re.compile(r";")

        print("starting parse")
        with open(filename, 'r') as f:
            self._connection = sqlite3.connect(self._databaseName)
            self._cursor = self._connection.cursor()
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS Genome (ChromID, BaseSite, ReferenceBase, Depth, PhredScore)")
            self._cursor.execute("CREATE TABLE IF NOT EXISTS Variants (ChromID, BaseSite, VariantBase)")
            self._cursor.execute("CREATE TABLE IF NOT EXISTS FileList (Files)")
            self._connection.commit()

            self._cursor.execute("SELECT Files FROM FileList WHERE Files = ?", (filename,))
            if self._cursor.fetchone() is not None:
                print("exiting parse")
                return
                # file is already in the database, don't parse the file

            print("continuing parse")
            self._cursor.execute("INSERT INTO FileList (Files) VALUES(?)", (filename,))
            self._connection.commit()

            for line in f:
                if line[0] == '#':
                    continue
                else:
                    # use the split method of a compiled regular expression to get a list of things in the line
                    categories = tab_expression.split(line)

                    info = semi_colon_expression.split(categories[7])
                    depth = 1
                    for entry in info:
                        if entry[0:3] == "DP=":
                            depth = entry[3:]
                            break

                    variant_list = comma_expression.split(categories[4])
                    if variant_list[0] == ".":
                        variant_list = None
                    else:
                        while True:
                            try:
                                variant_list.remove("<NON_REF>")
                            except:
                                break

                    # thingy is a tuple of format: (ChromID, BaseSite, ReferenceBase, Depth, PhredScore, list(variants))
                    thingy = categories[0], categories[1], categories[3], depth, categories[5], variant_list
                    self.add_entry(thingy)
        self._connection.commit()
        print("finished parse")
        self._connection.close()

    def get_depths(self):
        depths = []
        self._connection = sqlite3.connect(self._databaseName)
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Depth FROM Genome")

        while True:
            row = self._cursor.fetchone()
            if row is None:
                break
            depths.append(float(row[0]))

        self._connection.close()
        return depths

    def get_average_depth(self):
        i = 1
        total = 0.0

        self._connection = sqlite3.connect(self._databaseName)
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Depth FROM Genome")

        while True:
            row = self._cursor.fetchone()
            if row is None:
                break
            i += 1
            total += float(row[0])

        self._connection.close()
        return total / i

    def get_identifier(self):
        return self._identifier

    # entry is a tuple of format: (ChromID, BaseSite, ReferenceBase, Depth, PhredScore, list(variants))
    def add_entry(self, entry):
        self._cursor.execute(
            "INSERT INTO Genome (ChromID, BaseSite, ReferenceBase, Depth, PhredScore) VALUES (?,?,?,?,?)",
            (entry[0], entry[1], entry[2], entry[3], entry[4]))
        for variant in entry[5]:
            self._cursor.execute("INSERT INTO Variants (ChromID, BaseSite, VariantBase) VALUES(?,?,?)",
                                 (entry[0], entry[1], variant))
