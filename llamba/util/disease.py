from dataclasses import dataclass

@dataclass(slots=True)
class Disease:
    short_name: str
    full_name: str
    icd: str

def inflammatory_disease_list(lang: str = "en"):
    lst = []
    if lang == "ru":
        lst.append(Disease(short_name="Туберкулез", icd="A15 -- A19", full_name="A15 -- A19 Туберкулез"))
        lst.append(Disease(short_name="ЗППП", icd="A50 -- A64", full_name="A50 -- A64 Инфекции, передающиеся преимущественно половым путем"))
        lst.append(Disease(short_name="Гепатит B", icd="B16; B18.0; B18.1", full_name="B16; B18.0; B18.1 Гепатит B"))
        lst.append(Disease(short_name="Гепатит C", icd="B17.1; B18.2", full_name="B17.1; B18.2 Гепатит C"))
        lst.append(Disease(short_name="ВИЧ", icd="B20 -- B24", full_name="B20 -- B24 Болезни, вызванные вирусом иммунодефицита человека (ВИЧ)"))
        lst.append(Disease(short_name="Рак", icd="C00 -- C97", full_name="C00 -- C97 Злокачественные новообразования"))
        lst.append(Disease(short_name="Сахарный диабет", icd="E10 -- E14", full_name="E10 -- E14 Сахарный диабет"))
        lst.append(Disease(short_name="Психические расстройства и расстройства поведения", icd="F00 -- F99", full_name="F00 -- F99 Психические расстройства и расстройства поведения"))
        lst.append(Disease(short_name="Болезни, характеризующиеся повышенным кровяным давлением", icd="I10 -- I13.9", full_name="I10 -- I13.9 Болезни, характеризующиеся повышенным кровяным давлением"))
    else:
        lst.append(Disease(short_name="Tuberculosis", icd="A15 -- A19", full_name="A15 -- A19 Tuberculosis"))
        lst.append(Disease(short_name="STD", icd="A50 -- A64", full_name="A50 -- A64 Sexually transmitted diseases"))
        lst.append(Disease(short_name="Hepatitis B", icd="B16; B18.0; B18.1", full_name="B16; B18.0; B18.1 Hepatitis B"))
        lst.append(Disease(short_name="Hepatitis C", icd="B17.1; B18.2", full_name="B17.1; B18.2 Hepatitis C"))
        lst.append(Disease(short_name="HIV", icd="B20 -- B24", full_name="B20 -- B24 Human immunodeficiency virus"))
        lst.append(Disease(short_name="Cancer", icd="C00 -- C97", full_name="C00 -- C97 Malignant neoplasms"))
        lst.append(Disease(short_name="Diabetes", icd="E10 -- E14", full_name="E10 -- E14 Diabetes"))
        lst.append(Disease(short_name="EBD", icd="F00 -- F99", full_name="F00 -- F99 Emotional and behavioral disorders"))
        lst.append(Disease(short_name="Hypertensive diseases", icd="I10 -- I13.9", full_name="I10 -- I13.9 Hypertensive diseases"))
    return lst