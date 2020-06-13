import json

def pywrite(jsonpy, filename = "dynampy.py"):
    # test = {"def fun():": {"value": "1", "print(": "'test',value)"}}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jsonpy, f, ensure_ascii=False, indent=4)
    pyjson = ""
    with open(filename, "r", encoding="utf-8") as f:
        content = ''
        for line in f.readlines():
            content = content + line[4:]
        pyjson = (
            content.replace("{in_curly}", "__open_currly__")
            .replace("{fin_curly}", "__close_currly__")
            .replace("{is}", "__colon__")
            .replace("{with}", "__camma__")
            .replace("{nextline}","__next_line__")
            .replace("{tab}", "    ")
            .replace("{quote}", "__single_quote__")
            .replace("{", "")
            .replace("}", "")
            .replace("(:", "(")
            .replace(":", "")
            .replace('"', "")
            .replace("'", '"')
            .replace(",\n", "\n")
            .replace("__single_quote__","'")
            .replace("__colon__", ":")
            .replace("__open_currly__", "{")
            .replace("__close_currly__", "}")
            .replace("__camma__", ",")
            .replace("__next_line__ ", "\\")
        )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pyjson)
