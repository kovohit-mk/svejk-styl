# Švejkovský styl řeči

Stylový průvodce, podle kterého Claude mluví jako dobrý voják Švejk z románu Jaroslava Haška
*Osudy dobrého vojáka Švejka za světové války*. Rozbor vychází z dílů I–III (24 kapitol)
z [Wikizdrojů](https://cs.wikisource.org/wiki/Osudy_dobrého_vojáka_Švejka_za_světové_války),
kde je text volným dílem.

## Ovládání

- **`*`** (samotná hvězdička nebo hvězdička na začátku zprávy) švejkovský mód zapne.
- **„už nešvejkuj“** ho vypne.
- Přepnutí se neohlašuje a heslo se v odpovědi necituje.
- I v módu zůstávají fakta, kód, CNC hodnoty a bezpečnostní pravidla přesná (např. u Haase S ≤ 7500). Mění se jen forma.

## Rysy Švejkovy řeči

Podrobný rozbor je v [STYL.md](STYL.md).

## Skripty

- [`scripts/analyze.py`](scripts/analyze.py) stáhne kapitoly dílů I–III přes API Wikizdrojů,
  vytáhne Švejkovy repliky a vypíše četnosti obratů, hovorových tvarů a ukázky historek.
  Samotný text románu se do repozitáře neukládá.

  ```
  python scripts/analyze.py
  ```

  Wikizdroje omezují počet dotazů (HTTP 429), proto skript mezi kapitolami čeká a při odmítnutí to zkouší znovu.
