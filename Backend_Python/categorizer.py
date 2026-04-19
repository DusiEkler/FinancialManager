MCC = {
    7997: "Клуби",
    5411: "Продукти",
    4899: "Телебачення",
    7299: "Різне",
    4121: "Таксі та транспорт"
}

KeyWords = {
    "Продукти": ["атб", "сільпо", "ашан"],
    "Таксі та транспорт": ["uklon", "bolt", "uber"],
    "Телебачення": ["netflix", "megogo"],
    "Клуби": ["club"]
}

def get_category(mcc: int, description: str) -> str:
    category = MCC.get(mcc, "")

    if category == "":
        description_lower = description.lower()

        for key in KeyWords:
            for word in KeyWords[key]:
                if word in description_lower:
                    return key
     
    return category or "Інше"