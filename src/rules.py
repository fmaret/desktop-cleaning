import json
import re


def readLinesTxt(path: str):
    lines = []
    for line in open(path):
        if line.startswith("#"):
            continue

        lines.append(line.strip())

        if not line:
            continue

    return lines


def isInList(file_name: str, list_: list[str]):
    for item in list_:
        regex = r"\b(" + item.lower() + r")\b"
        if bool(re.match(regex, file_name.lower().replace(u'\xa0', u' '))):
            return True

    return False


def readJson(path: str):
    with open(path) as f:
        return json.load(f)


rules = readJson("./src/data/default_rules.json")


def getNameAndExtension(file: str):
    extension = file.split(".")[-1]
    name = ".".join(file.split(".")[:-1])

    return name, extension


def transformRule(file: str):
    try:
        contain = file.split("%")[1].split("%")[0]
        name = ""
        extension = file.split("%")[-1].split(".")[-1]
    except Exception as e:
        contain = ""
        name, extension = getNameAndExtension(file)

        if name == "*":
            name = ""

    return name, contain, extension


def matchSingleRule(file_name: str, file_extension: str, rule: str):
    rule_name, rule_contain, rule_extension = transformRule(rule)

    if rule_extension != "" and rule_extension != file_extension:
        return False

    if rule_name != "" and rule_name != file_name:
        return False

    if rule_contain != "" and rule_contain not in file_name:
        return False

    return True


def ruleMatch(file: str, rule):
    file_name, file_extension = getNameAndExtension(file)

    try:
        names = readLinesTxt(rule["names"])
    except Exception as e:
        names = []

    if len(names) > 0:
        if isInList(file_name, names):
            return True
        else:
            return False

    if type(rule["rule"]) == str:
        return matchSingleRule(file_name, file_extension, rule['rule'])
    elif type(rule["rule"]) == list:
        for item in rule["rule"]:
            if matchSingleRule(file_name, file_extension, item):
                return True

        return False
    else:
        return False


def chooseFolder(file: str):
    file = file.lower()
    for rule in rules:
        if ruleMatch(file, rule):
            return rule["out"]
    return "Other"


if __name__ == "__main__":
    file_test = ["test.txt", "mon cv.pdf", "vc.img", "Calendar.ics",
                 "Facture.pdf", "Battle.net.lnk", "Bloons TD 6.url", "Owawatch.lnk"]

    for file in file_test:
        print(file + ":" + chooseFolder(file))
