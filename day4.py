import re

TEST_PASSPORTS = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""".split("\n")

REQ_FIELDS = {"byr",
            "iyr",
            "eyr",
            "hgt",
            "hcl", 
            "ecl",
            "pid"}

def count_valid_passports(lines):
    num_valids = 0
    fields = set()
    for line in lines:
        if line == "":
            if REQ_FIELDS.issubset(fields):
                num_valids += 1
            fields = set()
        else:
            elems = {elem.split(":")[0] for elem in line.strip().split()}
            fields.update(elems)

    return num_valids


assert count_valid_passports(TEST_PASSPORTS) == 2

with open("./inputs/day4.txt") as f:
    passport_data = [line.strip() for line in f]


# PART A:
print("Part A:", count_valid_passports(passport_data))


# PART B

TEST_DATA_B_INVALID = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""".split("\n")


TEST_DATA_B_VALID = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""".split("\n")


def count_valid_passports2(lines):
    num_valids = 0
    num_passports = 0
    fields = {}
    for line in lines:
        if line == "":
            num_passports += 1
            if REQ_FIELDS.issubset(set(fields.keys())):
                hgt_re = re.search(r'^(\d*)(cm|in)$', fields["hgt"])
                if hgt_re is not None:
                    unit = hgt_re.group(2)
                    meas = int(hgt_re.group(1)) if hgt_re.group(1).isdigit() else None
                    if all((
                        fields["byr"].isdigit() and 1920 <= int(fields["byr"]) <= 2002,
                        fields["iyr"].isdigit() and 2010 <= int(fields["iyr"]) <= 2020,
                        fields["eyr"].isdigit() and 2020 <= int(fields["eyr"]) <= 2030,
                        re.search(r'^#(?:[0-9a-f]{6})$', fields["hcl"]),
                        meas is not None,
                        (unit == "cm" and 150 <= meas <= 193) or (unit == "in" and 59 <= meas <= 76),
                        fields["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
                        fields["pid"].isdigit() and len(fields["pid"]) == 9
                        )):
                        num_valids += 1

            fields = {}
        else:
            for elem in line.strip().split():
                fields[elem.split(":")[0]] = elem.split(":")[1]

    # the last passport handled by adding empty row to the input data (if not exists)

    #print("Total # of passports:", num_passports)
    return num_valids
            

assert count_valid_passports2(TEST_DATA_B_VALID) == 4
assert count_valid_passports2(TEST_DATA_B_INVALID) == 0

print("Part B:", count_valid_passports2(passport_data))
# 223 too low... something invalidated ihan turhaan.  224
