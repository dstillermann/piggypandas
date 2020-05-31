from piggypandas import Mapper2
import shutil


def _main():
    shutil.copy('mapping/demomapping.xlsx', 'tmp/demomapping.xlsx')
    m0: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=False)
    m1: Mapper2 = Mapper2('tmp/demomapping.xlsx', columns=['Name'], ignore_case=True)

    print("\n====\nTesting get/getc without defaultvalue")
    for mname, m in {"m0": m0, "m1": m1}.items():
        for key in ['Vincent', 'Basil', 'InvalidKey']:
            try:
                s = m.get(key)
            except BaseException as e:
                s = f"{type(e)} {e}"
            print(f"{mname}.get(\"{key}\")=\"{s}\"")
            for col in ['Species', 'Colour', 'InvalidCol']:
                try:
                    s = m[col][key]
                except BaseException as e:
                    s = f"{type(e)} {e}"
                print(f"{mname}.getc(\"{key}\",\"{col}\")=\"{s}\"")

    print("\n====\nTesting get for case-insensitive mapper")
    for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
        for col in ['Colour', 'colour', 'ColoUr']:
            try:
                s = m1[col][key]
            except BaseException as e:
                s = f"{type(e)} {e}"
            print(f"m1.getc(\"{key}\",\"{col}\")=\"{s}\"")

    print("\n====\nTesting touch/touchc with no default value")
    for mname, m in {"m0": m0, "m1": m1}.items():
        for key in ['Vincent', 'Mary']:
            b = m.touch(key)
            print(f"{mname}.touch(\"{key}\")={b}")
            for col in ['Species', 'Sex']:
                b = m.touchc(key, col)
                print(f"{mname}.touchc(\"{key}\",\"{col}\")={b}")

    print("\n====\nTesting touchc with default value")
    for mname, m in {"m0": m0, "m1": m1}.items():
        for key, col, defaultvalue in [
            ('Vincent', 'Species', 'Lamb'),
            ('Vincent', 'Sex', 'Male'),
            ('Mary', 'Species', 'Rat'),
            ('Mary', 'Sex', 'Female')
        ]:
            b = m.touchc(key, col, defaultvalue)
            print(f"{mname}.touchc(\"{key}\",\"{col}\",\"{defaultvalue}\",)={b}")

    print("\n====\nTesting set, incl. for case sensitivity")
    for mname, m in {"m0": m0, "m1": m1}.items():
        for key, col, value in [
            ('Vincent', 'Species', 'Mutton'),
            ('VinCent', 'Species', 'Mutton'),
            ('Mary', 'Species', 'Hamster'),
            ('MarY', 'SPECIES', 'Hamster')
        ]:
            b = m.setc(key, col, value)
            print(f"{mname}.touchc(\"{key}\",\"{col}\",\"{value}\",)={b}")

    Mapper2.flush_all()


if __name__ == "__main__":
    _main()
