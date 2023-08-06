import os
from file_reader.compressed import bzipped, gzipped



extension_map = {
    '.bz2': bzipped.opener,
    '.gz': gzipped.opener
}

class MultiReader():
    
    def __init__(self, filename):
        extension = os.path.splitext(filename)[1]
        opener = extension_map.get(extension, open)
        self.f = opener(filename, 'r', )
        
    def close(self):
        self.f.close()
        
    def read(self):
        return self.f.read()
    

if __name__ !="__main__":
    print("multi reader imported")