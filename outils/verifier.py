# -*- coding: utf-8 -*-
"""Contrôles non négociables sur les pages générées.

    python3 outils/verifier.py

Sort en erreur si une page manque un élément que le référencement ou
l'accessibilité rendent obligatoire. Le but est qu'une régression se voie
avant la mise en ligne, pas après.
"""
import glob
import html.parser
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
erreurs = []
titres, descriptions = {}, {}


class Analyseur(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.liens = []
        self.images_sans_alt = 0
        self.boutons_sans_libelle = 0
        self.dans_titre = False
        self.titre = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self.dans_titre = True
        elif tag == "a" and "href" in a:
            self.liens.append(a["href"])
        elif tag == "img" and "alt" not in a:
            self.images_sans_alt += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.dans_titre = False

    def handle_data(self, data):
        if self.dans_titre:
            self.titre += data


def controler(chemin):
    nom = os.path.relpath(chemin, RACINE)
    source = open(chemin, encoding="utf-8").read()

    def erreur(message):
        erreurs.append("%s : %s" % (nom, message))

    analyseur = Analyseur()
    analyseur.feed(source)

    # --- Référencement -----------------------------------------------------
    if analyseur.h1 != 1:
        erreur("%d balise(s) h1, il en faut exactement une" % analyseur.h1)

    titre = analyseur.titre.strip()
    if not titre:
        erreur("titre absent")
    elif len(titre) > 70:
        erreur("titre de %d caractères, Google en affiche environ 60" % len(titre))
    elif titre in titres:
        erreur("titre identique à celui de %s" % titres[titre])
    else:
        titres[titre] = nom

    m = re.search(r'<meta name="description" content="([^"]*)"', source)
    if not m:
        erreur("meta description absente")
    else:
        description = m.group(1)
        if not 100 <= len(description) <= 175:
            erreur("meta description de %d caractères, viser 150 à 160" % len(description))
        if description in descriptions:
            erreur("meta description identique à celle de %s" % descriptions[description])
        descriptions[description] = nom

    if '<link rel="canonical"' not in source:
        erreur("URL canonique absente")

    # --- Données structurées ----------------------------------------------
    blocs = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    if not blocs:
        erreur("aucune donnée structurée Schema.org")
    for bloc in blocs:
        try:
            json.loads(bloc)
        except ValueError as e:
            erreur("données structurées illisibles (%s)" % e)

    # --- Accessibilité -----------------------------------------------------
    if analyseur.images_sans_alt:
        erreur("%d image(s) sans attribut alt" % analyseur.images_sans_alt)
    if 'class="saut-navigation"' not in source:
        erreur("lien d'évitement absent")

    # --- Liens internes ----------------------------------------------------
    dossier = os.path.dirname(chemin)
    for lien in analyseur.liens:
        if lien.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        cible = os.path.normpath(os.path.join(dossier, lien.split("#")[0]))
        if not os.path.exists(cible):
            erreur("lien mort vers %s" % lien)

    # --- Résidus de génération --------------------------------------------
    if "%s" in source or "%(" in source:
        erreur("marque de formatage non substituée")

    # --- Coordonnées présentes partout ------------------------------------
    if "01 45 85 22 14" not in source:
        erreur("téléphone absent de la page")


def principal():
    # maquette-complete.html est l'assemblage de démonstration : il réunit les
    # douze pages en un fichier et ne suit donc pas les règles ci-dessus.
    pages = sorted(p for p in glob.glob(os.path.join(RACINE, "*.html")) +
                   glob.glob(os.path.join(RACINE, "blog", "*.html"))
                   if os.path.basename(p) != "maquette-complete.html")
    for page in pages:
        controler(page)

    print("%d pages contrôlées." % len(pages))
    if erreurs:
        print("\n%d problème(s) :" % len(erreurs))
        for e in erreurs:
            print("  - " + e)
        return 1
    print("Aucun problème.")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
