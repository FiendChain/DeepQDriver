import io
import pickle
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("map_file")

args = parser.parse_args()

class Renamer(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module == 'src.Map':
            renamed_module = 'src.Environment.Map'
        
        return super().find_class(renamed_module, name)

with open(args.map_file, "rb") as fp:
    data = bytearray(fp.read())
    M = Renamer(io.BytesIO(data)).load()

with open(args.map_file, "wb") as fp:
    pickle.dump(M, fp)
