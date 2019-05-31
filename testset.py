# this file is a csv writter
import csv

class test_csv:

    # create a csv file
    def __init__(self, path: str):
        self.fp = open(path, 'w')
        self.csv_writer = csv.writer(self.fp)
        #csv_head = ["claim", "evidence", "label"]
        csv_head = ["key", "claim", "evidence", "title", "line", "label"]
        self.csv_writer.writerow(csv_head)


    # wite csv file
    def write(self, claim, evidence: str, label):
        if not evidence is None:
            data = [claim, evidence, label]
            self.csv_writer.writerow(data)

    def write_dev(self, key, claim, evidence, title, line, label):
        if not evidence is None:
            data = [key, claim, evidence, title, line, label]
            self.csv_writer.writerow(data)
        else:
            data = [key, "None","None","None","None","NOT ENOUGH INFO"]
            self.csv_writer.writerow(data)
    def close(self):
        self.fp.close()