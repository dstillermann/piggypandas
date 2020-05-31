from piggypandas import Mapper2
import shutil

def _main():
    shutil.copy('mapping/demomapping.xlsx', 'tmp/demomapping.xlsx')
    m0: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=False)
    m1: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=True)

    print("\n====\nTesting get without defaultvalue")
    for mname, m in {"m0": m0, "m1": m1}.items():
        for key in ['Vincent', 'Basil', 'InvalidKey']:
            try:
                s = m.get(key)
            except BaseException as e:
                s = f"{type(e)} {e}"
            print(f"{mname}.get(\"{key}\")=\"{s}\"")
            for col in ['Species', 'Colour', 'InvalidCol']:
                try:
                    s = m.get(key, col)
                except BaseException as e:
                    s = f"{type(e)} {e}"
                print(f"{mname}.get(\"{key}\",\"{col}\")=\"{s}\"")

    print("\n====\nTesting get for case-insensitive mapper")
    for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
        for col in ['Colour', 'colour', 'ColouR']:
            try:
                s = m1.get(key, col)
            except BaseException as e:
                s = f"{type(e)} {e}"
            print(f"m1.get(\"{key}\",\"{col}\")=\"{s}\"")

    Mapper2.flush_all()


if __name__ == "__main__":
    _main()
