"""Random fantasy name generator"""

import random as r  # ɂ/Ɂ


def name_gen(race, gender):
    if gender == "male":
        if race == "dwarf":
            onset = [["", 10], ["k", 8], ["p", 6], ["q", 2], ["g", 9], ["ts", 5], ["t", 7], ["x", 7], ["kr", 4],
                     ["gt", 5], ["kl", 4], ["d", 5], ["dl", 3], ["t-h", 5], ["jf", 7], ["ks", 6], ["bz", 4], ["gp", 7],
                     ["gf", 6], ["br", 7], ["dr", 8], ["tl", 4], ["td", 7], ["sd", 2], ["l", 1]]
            nucleas = [["a", 10], ["o", 20], ["e", 10], ["oa", 5], ["oe", 6], ["ao", 2], ["ea", 1], ["ae", 2],
                       ["u", 20], ["uo", 12], ["ou", 10], ["au", 5], ["ua", 10], ["uɂu", 20], ["oɂo", 20]]
            coda = [["ls", 10], ["wk", 9], ["lk", 6], ["p", 6], ["b", 6], ["k", 9], ["dk", 3], ["g", 7], ["ng", 6],
                    ["", 20]]
            if r.randint(1, 10) >= 2:
                name = r.choices(onset, weights=[l[1] for l in onset])[0][0]
                name += r.choices(nucleas, weights=[l[1] for l in nucleas])[0][0]
                name += r.choices(coda, weights=[l[1] for l in coda])[0][0]
            else:
                name = r.choices(onset, weights=[l[1] for l in onset])[0][0]
                name += r.choices(nucleas, weights=[l[1] for l in nucleas])[0][0]
                name += r.choices(coda, weights=[l[1] for l in coda])[0][0]
                name += r.choices(onset, weights=[l[1] for l in onset])[0][0]
                name += r.choices(nucleas, weights=[l[1] for l in nucleas])[0][0]
                name += r.choices(coda, weights=[l[1] for l in coda])[0][0]
            return name
        elif race == "elf":
            onset = ["", "s", "r", "v", "f", "h", "l", "rr", "bb", "z", "m", "n", "hf", "fh", "sz", "shw", "ln", "vl",
                     "zs", "hz", "hv", "vf", "hr", "hrr", "pp", "ppr", "bbr", "rrs", "pps", "ppv", "bbv", "ppf", "bbv",
                     "bbs", "bbn", "ppn", "hs", "hm", "sw", "fn", "sn", "shs", "shz", "zhm", "zh", "zhl", "zhn", "ls",
                     "bbl", "rrl", "rrn", "rn", "vw", "lv", "nl", "nm", "mn", "zv", "lr", "rrv", "hl", "sw", "s-h",
                     "ml", "bbrr", "fw", "bbm", "wn", "mw", "ms", "zhf", "frr", "mbb", "wrr", "w", "zhs"]
            nucleas = ["a", "e", "i", "o", "u", "ae", "ai", "ao", "au", "ea", "ei", "eo", "eu", "ia", "ie", "io", "iu",
                       "oa", "oe", "oi", "ou", "ua", "ue", "ui", "uo"]
            coda = ["", "s", "r", "v", "f", "h", "l", "rr", "bb", "z", "m", "n", "hf", "fh", "sz", "shw", "ln", "vl",
                    "zs", "hz", "hv", "vf", "hr", "hrr", "pp", "ppr", "bbr", "rrs", "pps", "ppv", "bbv", "ppf", "bbv",
                    "bbs", "bbn", "ppn", "hs", "hm", "sw", "fn", "sn", "shs", "shz", "zhm", "zh", "zhl", "zhn", "ls",
                    "bbl", "rrl", "rrn", "rn", "vw", "lv", "nl", "nm", "mn", "zv", "lr", "rrv", "hl", "sw", "s-h", "ml",
                    "bbrr", "fw", "bbm", "wn", "mw", "ms", "zhf", "frr", "mbb", "wrr", "w", "zhs"]
            options = range(1, 10)
            cyl = r.choices(options, weights=[60, 5, 5, 5, 5, 5, 5, 5, 1])[0]
            name = r.choice(onset)
            name += r.choice(nucleas)
            name += r.choice(coda)
            for x in range(1, cyl):
                name = r.choice(onset)
                name += r.choice(nucleas)
                name += r.choice(coda)
            return name
