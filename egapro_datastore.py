from csv import DictReader
 
egapro_data = {}
 
with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv:
    reader = DictReader(csv, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)
