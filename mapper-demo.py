from piggypandas import Mapper2
import shutil

def _main():
    shutil.copy('mapping/demomapping.xlsx', 'tmp/demomapping.xlsx')
    m0: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=False)
    m1: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=True)

    for mname, m in {"m0": m0, "m1": m1}.items():
        for key in ['Vincent', 'Basil', 'Murray']:
            print(f"{mname}.get(\"{key}\")=\"{m.get(key)}\"")
            for col in ['Species', 'Colour']:
                print(f"{mname}.get(\"{key}\",\"{col}\")=\"{m.get(key, col)}\"")

    Mapper2.flush_all()


if __name__ == "__main__":
    _main()
