import gzip
import sys
from ..util import writer

opener = gzip.open

if __name__!="__main__":
    print("gzipped imported")

if __name__=="__main__":
#     f = opener(sys.argv[1], mode='wt')
#     f.write(' '.join(sys.argv[2:]))
#     f.close()
    writer.main(opener)