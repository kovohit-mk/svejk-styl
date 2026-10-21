"""Stáhne díly I–III Švejka z Wikizdrojů a rozebere Švejkovy repliky (text se neukládá)."""
import collections, html as H, json, random, re, time
import urllib.error, urllib.parse, urllib.request

BASE = "Osudy dobrého vojáka Švejka za světové války"
CH = ["Zasáhnutí dobrého vojáka Švejka do světové války", "Dobrý voják Švejk na policejním ředitelství",
      "Švejk před soudními lékaři", "Švejka vyhodili z blázince", "Švejk na policejním ředitelství v Salmově ulici",
      "Švejk opět doma, proraziv začarovaný kruh", "Švejk jde na vojnu", "Švejk simulantem", "Švejk na garnizóně",
      "Švejk vojenským sluhou u polního kuráta", "Švejk jede s polním kurátem sloužit polní mši", "Náboženská debata",
      "Švejk jde zaopatřovat", "Švejk vojenským sluhou u nadporučíka Lukáše", "Katastrofa",
      "Švejkovy nehody ve vlaku", "Švejkova budějovická anabaze", "Švejkovy příhody v Királyhidě", "Nová utrpení",
      "Z Mostu nad Litavou k Sokalu", "Přes Uhry", "V Budapešti", "Z Hatvanu na hranice Haliče", "Marschieren marsch!"]

VERB = (r"(řekl|odpověděl|odvětil|ozval|otázal|pravil|poznamenal|vykládal|hlásil|dodal|pokračoval|vzdychl|zvolal|"
        r"vykřikl|bránil|hájil|namítl|prohlásil|mluvil|hovořil|povídal|vyprávěl|zašeptal|křičel|volal|vysvětloval)")
ATTR = re.compile(VERB + r"[^„“]{0,50}Švejk|Švejk[^„“]{0,50}" + VERB)


def fetch(title):
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "text", "format": "json", "formatversion": "2"})
    req = urllib.request.Request("https://cs.wikisource.org/w/api.php?" + q, headers={"User-Agent": "svejk-styl/1.0"})
    for attempt in range(8):
        try:
            h = json.load(urllib.request.urlopen(req, timeout=60))["parse"]["text"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(10 * (attempt + 1))
    else:
        raise SystemExit("Wikizdroje stále odmítají dotazy (429), zkus to později.")
    h = re.sub(r"(?s)<table.*?</table>|<sup.*?</sup>", "", h)
    t = H.unescape(re.sub(r"<[^>]+>", "", re.sub(r"</p>|<br\s*/?>", "\n", h)))
    return [p.strip() for p in t.split("\n") if p.strip()]


def main():
    utt = []
    for i, c in enumerate(CH):
        for p in fetch(BASE + "/" + c):
            quotes = re.findall(r"„([^“]+)“", p)
            if quotes and (ATTR.search(re.sub(r"„[^“]+“", " | ", p)) or p.startswith("„Poslušně hlásím")):
                utt.append((i, " ".join(quotes)))
        print(f"kapitola {i + 1:2d}/{len(CH)}: {c}")
        time.sleep(3)

    low = " ".join(u for _, u in utt).lower()
    wc = collections.Counter(re.findall(r"\w+", low))
    print(f"\nŠvejkových replik: {len(utt)}, slov: {sum(wc.values())}")

    def top(pattern, n=50, minimum=4):
        return ", ".join(f"{w}({c})" for w, c in wc.most_common() if re.search(pattern, w) and c >= minimum)[:2000]

    print("\nProtetické v-:", top(r"^v[oů]"))
    print("\nKoncovky -ej/-ýho:", top(r"(ej|ejch|ejm|ýho|ýmu)$"))
    for ph in ["poslušně hlásím", "pane obrlajtnant", "pane feldkurát", "poněvadž", "jednou", "kdyby", "povídá", "prej", "račte", "u nás v"]:
        print(f"  {ph!r}: {low.count(ph)}")
    print("\nNáhodné repliky:")
    for i, u in random.Random(7).sample(utt, min(40, len(utt))):
        print(f"[{i + 1:2d}] {u[:200]}")


if __name__ == "__main__":
    main()
