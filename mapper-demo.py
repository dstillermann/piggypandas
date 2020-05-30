from piggypandas import Mapper2
import shutil

def _main():
    shutil.copy('mapping/demomapping.xlsx', 'tmp/demomapping.xlsx')
    m: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'])
    Mapper2.flush_all()

if __name__ == "__main__":
    _main()
