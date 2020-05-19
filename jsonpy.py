import json


def pywrite(jsonpy):
    # test = {"def fun():": {"value": "1", "print(": "'test',value)"}}
    with open("dynampy.py", "w", encoding="utf-8") as f:
        json.dump(jsonpy, f, ensure_ascii=False, indent=4)
    pyjson = ""
    with open("dynampy.py", "r", encoding="utf-8") as f:
        pyjson = (
            f.read()
            .replace("{", "")
            .replace("}", "")
            .replace("        ", "\t")
            .replace("    ", "")
            # .replace('(":', "(")
            .replace(':":', "@")
            .replace(":", "")
            .replace("@", ":")
            .replace('"', "")
            .replace("'", '"')
            .replace(",\n", "\n")
        )
        print(pyjson)
    with open("dynampy.py", "w", encoding="utf-8") as f:
        f.write(pyjson)

    import dynampy

    dynampy.run()
