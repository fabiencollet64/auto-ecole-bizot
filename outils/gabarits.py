# -*- coding: utf-8 -*-
"""Fragments partagés par toutes les pages de la maquette Bizot.

Source unique de vérité pour l'en-tête, la navigation, le pied de page et les
données structurées. C'est ce qui garantit que le téléphone, l'adresse et les
horaires — les trois informations que Google et les moteurs de réponse lisent
en priorité — sont strictement identiques sur toutes les pages.
"""
import hashlib
import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Établissement — une seule source, reprise en clair dans le pied de page et
# dans le balisage Schema.org. Un écart entre les deux dégrade le référencement
# local : Google compare la fiche Google Business Profile au site.
# ---------------------------------------------------------------------------
NOM = "Auto Moto École Bizot"
NOM_LEGAL = "AUTO MOTO ECOLE BIZOT"
RUE = "113 avenue du Général Michel Bizot"
CODE_POSTAL = "75012"
VILLE = "Paris"
ARRONDISSEMENT = "Paris 12e"
TEL_AFFICHE = "01 45 85 22 14"
TEL_LIEN = "+33145852214"
COURRIEL = "contact@automotoecolebizot.com"   # à confirmer avec l'auto-école
SITE = "https://www.automotoecolebizot.com"
# Coordonnées approximatives de l'avenue du Général Michel Bizot — à relever
# précisément sur la fiche Google Business Profile avant mise en ligne.
LATITUDE = "48.8368"
LONGITUDE = "2.4048"

HORAIRES = [
    ("Lundi",    "10h–13h · 14h–18h"),
    ("Mardi",    "10h–13h · 14h–18h"),
    ("Mercredi", "10h–13h"),
    ("Jeudi",    "10h–13h · 14h–16h"),
    ("Vendredi", "10h–13h · 14h–18h"),
    ("Samedi",   "10h–13h"),
    ("Dimanche", "Fermé"),
]

# Format Schema.org des mêmes horaires.
HORAIRES_SCHEMA = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Friday"],
     "opens": "10:00", "closes": "13:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Friday"],
     "opens": "14:00", "closes": "18:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Saturday"],
     "opens": "10:00", "closes": "13:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "10:00", "closes": "13:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "14:00", "closes": "16:00"},
]

AGENCE = "Collet Marketing"
AGENCE_SITE = "https://colletmarketing.com"

VERSION = "0"  # empreinte des ressources, injectée par generer.py

# Logo officiel de l'auto-école. Déposez le fichier fourni par le client sous
# ce chemin (SVG de préférence, sinon PNG détouré) : il remplace alors
# automatiquement le logotype reconstitué en HTML, sur toutes les pages.
LOGO_FICHIER = "assets/img/logo-bizot.svg"

# Navigation — deux niveaux assumés. Les trois formations sont regroupées :
# à plat, le menu mélangeait des choses qui ne sont pas de même nature (une
# formation, une grille de prix, une page de référencement local, un blog).
FORMATIONS = [
    ("permis-voiture.html",    "Permis voiture"),
    ("permis-moto.html",       "Permis moto"),
    ("code-de-la-route.html",  "Code de la route"),
]

GROUPE_FORMATIONS = "__formations__"
NAV = [
    (GROUPE_FORMATIONS,        "Formations"),
    ("tarifs.html",            "Tarifs"),
    ("financement.html",       "Financement"),
    ("blog.html",              "Conseils"),
    ("a-propos.html",          "L'auto-école"),
]

# Pages atteignables depuis le tiroir et le pied de page, mais pas depuis la
# barre : la page locale sert le référencement, le contact a déjà son bouton.
SECONDAIRE = [
    ("auto-ecole-paris-12.html", "Auto-école Paris 12"),
    ("contact.html",             "Contact et accès"),
]

_empreintes = {}


def empreinte(chemin_relatif):
    """Empreinte du contenu d'une ressource, ajoutée à son URL.

    Sans elle, un navigateur qui a gardé l'ancienne feuille de style en cache
    l'applique au nouveau HTML : la page s'affiche cassée sans que rien ne le
    signale.
    """
    if chemin_relatif not in _empreintes:
        try:
            with open(os.path.join(RACINE, chemin_relatif), "rb") as f:
                _empreintes[chemin_relatif] = hashlib.sha256(f.read()).hexdigest()[:10]
        except OSError:
            _empreintes[chemin_relatif] = "0"
    return _empreintes[chemin_relatif]


def logotype(prof=0):
    """Le logo de l'en-tête.

    Si le fichier officiel a été déposé (LOGO_FICHIER), il est servi tel quel.
    Sinon, le logotype est reconstitué en HTML d'après l'enseigne : AUTOMOTO
    dont les O sont des anneaux rouges, encadré de la voiture et de la moto.
    """
    if os.path.exists(os.path.join(RACINE, LOGO_FICHIER)):
        return ('<img class="logo__image" src="%s%s?v=%s" alt="" width="160" height="40">'
                % (prefixe(prof), LOGO_FICHIER, empreinte(LOGO_FICHIER)))
    anneau = '<i class="logo__o"></i>'
    return (
        '<span class="logo__lockup" aria-hidden="true">'
        '%s'
        '<span class="logo__mot">AUT%sM%sT%s</span>'
        '%s'
        '</span>'
        '<span class="logo__sous" aria-hidden="true">ÉCOLE · BIZOT · PARIS 12<sup>e</sup></span>'
        % (icone("voiture", "logo__vehicule"), anneau, anneau, anneau,
           icone("moto", "logo__vehicule"))
    )


def prefixe(profondeur):
    """'' à la racine, '../' dans blog/."""
    return "../" * profondeur


# ---------------------------------------------------------------------------
# Icônes — un seul trait, héritant de la couleur du composant.
# ---------------------------------------------------------------------------
ICONES = {
    "coche":    '<path d="M9.6 16.6 5 12l1.4-1.4 3.2 3.2 8-8L19 7.2z"/>',
    "tel":      '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .58 3.6 1 1 0 0 1-.25 1z"/>',
    "voiture":  '<path d="M5 11l1.5-4.3A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.7L19 11h1a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-1v1a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H8v1a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-1H4a1 1 0 0 1-1-1v-4a1 1 0 0 1 1-1zm2.2 0h9.6l-1.1-3.4a.6.6 0 0 0-.5-.4H8.8a.6.6 0 0 0-.5.4zM7 13.2a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6zm10 0a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6z"/>',
    "moto":     '<path d="M5.5 13a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm13 0a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm-13 2a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zm13 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM14 5h4v2h-2.6l1.3 2.4A5.5 5.5 0 0 1 18.5 12h-2a3.5 3.5 0 0 0-.8-1.6L14.4 12H9.9a5.5 5.5 0 0 0-4.4-2H3V8h2.5a7.5 7.5 0 0 1 5.6 2.5h2.1l-2-3.7A1.5 1.5 0 0 1 14 5z"/>',
    "code":     '<path d="M6 3h9l4 4v14a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm8 1.8V8h3.2zM8 11h8v2H8zm0 4h8v2H8z"/>',
    "euro":     '<path d="M15.6 6.2a5.4 5.4 0 0 0-5.2 3.4H15v1.8h-5.1a6 6 0 0 0 0 1.2H15v1.8h-4.6a5.4 5.4 0 0 0 5.2 3.4c.9 0 1.7-.2 2.4-.6v2.1c-.8.3-1.6.5-2.5.5a7.4 7.4 0 0 1-7.2-5.4H6v-1.8h2a7.7 7.7 0 0 1 0-1.2H6V9.6h2.3A7.4 7.4 0 0 1 15.5 4c.9 0 1.7.2 2.5.5v2.1c-.7-.3-1.5-.4-2.4-.4z"/>',
    "epingle":  '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    "horloge":  '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm1-13h-2v6l5 3 1-1.7-4-2.3z"/>',
    "bouclier": '<path d="M12 2 4 5v6.5c0 4.7 3.4 9.1 8 10.5 4.6-1.4 8-5.8 8-10.5V5zm-1 14-4-4 1.4-1.4L11 13.2l4.6-4.6L17 10z"/>',
    "etoile":   '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8-6.2-3.3-6.2 3.3L7 14.2l-5-4.9 6.9-1z"/>',
    "metro":    '<path d="M12 2C7.6 2 4 2.5 4 6v9.5A3.5 3.5 0 0 0 7.5 19L6 20.5v.5h12v-.5L16.5 19a3.5 3.5 0 0 0 3.5-3.5V6c0-3.5-3.6-4-8-4zM7.5 16A1.5 1.5 0 1 1 9 14.5 1.5 1.5 0 0 1 7.5 16zM11 11H6V6.5h5zm2 0V6.5h5V11zm3.5 5a1.5 1.5 0 1 1 1.5-1.5 1.5 1.5 0 0 1-1.5 1.5z"/>',
    "calendrier": '<path d="M7 2h2v2h6V2h2v2h2a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h2zm12 7H5v10h14zM7 11h4v4H7z"/>',
    "personne": '<path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 2c-4.4 0-8 2.5-8 5.5V22h16v-2.5c0-3-3.6-5.5-8-5.5z"/>',
    "eclair":   '<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
}


CHEVRON = ('<svg class="nav__chevron" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
           '<path d="M12 15.4 5.6 9l1.4-1.4 5 5 5-5L18.4 9z"/></svg>')

ICONE_MENU = ('<svg class="bouton-menu__icone" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
              '<path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>')

ICONE_CROIX = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
               '<path d="m12 10.6 5.3-5.3 1.4 1.4-5.3 5.3 5.3 5.3-1.4 1.4-5.3-5.3-5.3 5.3'
               '-1.4-1.4 5.3-5.3-5.3-5.3 1.4-1.4z"/></svg>')


def icone(nom, classe=""):
    c = ' class="%s"' % classe if classe else ""
    return ('<svg%s viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
            % (c, ICONES[nom]))


def coche():
    return icone("coche")


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
def etablissement():
    """Fiche DrivingSchool : le bloc que Google et les moteurs de réponse
    lisent pour associer l'établissement à « auto-école Paris 12 »."""
    return {
        "@context": "https://schema.org",
        "@type": ["DrivingSchool", "LocalBusiness"],
        "@id": SITE + "/#etablissement",
        "name": NOM,
        "legalName": NOM_LEGAL,
        "url": SITE + "/",
        "telephone": TEL_LIEN,
        "email": COURRIEL,
        "image": SITE + "/assets/img/devanture.jpg",
        "priceRange": "€€",
        "currenciesAccepted": "EUR",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": RUE,
            "postalCode": CODE_POSTAL,
            "addressLocality": VILLE,
            "addressRegion": "Île-de-France",
            "addressCountry": "FR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": LATITUDE, "longitude": LONGITUDE},
        "openingHoursSpecification": HORAIRES_SCHEMA,
        "areaServed": [
            {"@type": "City", "name": "Paris 12e"},
            {"@type": "City", "name": "Saint-Mandé"},
            {"@type": "City", "name": "Charenton-le-Pont"},
            {"@type": "City", "name": "Vincennes"},
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Formations au permis de conduire",
            "itemListElement": [
                {"@type": "Offer", "name": "Permis B — forfait 20 h boîte manuelle",
                 "price": "990", "priceCurrency": "EUR"},
                {"@type": "Offer", "name": "Permis B — forfait 20 h boîte automatique",
                 "price": "990", "priceCurrency": "EUR"},
                {"@type": "Offer", "name": "Permis A2 — forfait 20 h moto",
                 "price": "890", "priceCurrency": "EUR"},
            ],
        },
        "publicAccess": True,
        "sameAs": ["https://www.instagram.com/"],  # compléter : Instagram, fiche Google
    }


def jsonld(*blocs):
    return "".join(
        '\n<script type="application/ld+json">%s</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in blocs
    )


def fil_ariane_schema(fil, prof):
    elements = []
    for rang, (url, libelle) in enumerate(fil, start=1):
        element = {"@type": "ListItem", "position": rang, "name": libelle}
        if url:
            element["item"] = SITE + "/" + url
        elements.append(element)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def faq_schema(questions):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for q, r in questions
        ],
    }


# ---------------------------------------------------------------------------
# Fragments d'interface
# ---------------------------------------------------------------------------
def bandeau_maquette():
    return (
        '<div class="bandeau-maquette">'
        'Maquette de démonstration réalisée par <strong>%s</strong> pour %s — '
        'contenus, tarifs et photographies à valider avant mise en ligne.'
        '</div>' % (AGENCE, NOM)
    )


def entete(page, prof):
    p = prefixe(prof)
    formation_courante = any(url == page for url, _ in FORMATIONS)

    def lien(url, libelle, classe="nav__lien"):
        courant = ' aria-current="page"' if url == page else ""
        return '<a class="%s" href="%s%s"%s>%s</a>' % (classe, p, url, courant, libelle)

    sous_menu = "".join('<li>%s</li>' % lien(url, libelle, "nav__sous-lien")
                        for url, libelle in FORMATIONS)

    entrees = []
    for url, libelle in NAV:
        if url == GROUPE_FORMATIONS:
            entrees.append(
                '<li class="nav__groupe" data-groupe>'
                '<button class="nav__lien nav__declencheur" type="button" data-groupe-bouton'
                ' aria-expanded="false" aria-controls="menu-formations"%s>%s%s</button>'
                '<ul class="nav__sous" id="menu-formations">%s</ul>'
                '</li>'
                % (' data-courant="true"' if formation_courante else "", libelle,
                   CHEVRON, sous_menu))
        else:
            entrees.append('<li>%s</li>' % lien(url, libelle))

    tiroir_formations = "".join(
        '<li>%s</li>' % lien(url, libelle, "tiroir__lien") for url, libelle in FORMATIONS)
    tiroir_infos = "".join(
        '<li>%s</li>' % lien(url, libelle, "tiroir__lien")
        for url, libelle in [(u, l) for u, l in NAV if u != GROUPE_FORMATIONS] + SECONDAIRE)

    return """%s
<header class="entete">
  <div class="conteneur entete__barre">
    <a class="logo" href="%sindex.html"%s>
      %s
      <span class="visuellement-cache">Auto Moto École Bizot — accueil</span>
    </a>
    <nav class="nav" aria-label="Navigation principale">
      <ul class="nav__liste">%s</ul>
    </nav>
    <div class="entete__actions">
      <a class="tel-entete" href="tel:%s">%s<span class="tel-entete__texte">%s</span></a>
      <a class="bouton bouton--principal entete__cta" href="%scontact.html">S'inscrire</a>
      <button class="bouton-menu" type="button" data-tiroir-ouvrir
              aria-expanded="false" aria-controls="tiroir">%sMenu</button>
    </div>
  </div>
</header>

<div class="voile" data-voile></div>
<div class="tiroir" id="tiroir" data-tiroir role="dialog" aria-modal="true" aria-label="Menu">
  <div class="tiroir__entete">
    <span class="tiroir__titre">Menu</span>
    <button class="tiroir__fermer" type="button" data-tiroir-fermer aria-label="Fermer le menu">%s</button>
  </div>
  <nav class="tiroir__corps" aria-label="Navigation du menu">
    <p class="tiroir__section" id="tiroir-formations">Formations</p>
    <ul class="tiroir__liste" aria-labelledby="tiroir-formations">%s</ul>
    <p class="tiroir__section" id="tiroir-infos">Infos pratiques</p>
    <ul class="tiroir__liste" aria-labelledby="tiroir-infos">%s</ul>
  </nav>
  <div class="tiroir__pied">
    <a class="tiroir__tel" href="tel:%s">%s%s</a>
    <p class="tiroir__horaire">Ouvert du lundi au samedi</p>
    <a class="bouton bouton--principal bouton--large" href="%scontact.html">S'inscrire</a>
  </div>
</div>""" % (bandeau_maquette(), p,
             ' aria-current="page"' if page == "index.html" else "",
             logotype(prof), "".join(entrees),
             TEL_LIEN, icone("tel"), TEL_AFFICHE, p, ICONE_MENU, ICONE_CROIX,
             tiroir_formations, tiroir_infos,
             TEL_LIEN, icone("tel"), TEL_AFFICHE, p)


def fil_ariane(fil, prof):
    if not fil:
        return ""
    p = prefixe(prof)
    items = []
    for url, libelle in fil:
        if url:
            items.append('<li><a href="%s%s">%s</a></li>' % (p, url, libelle))
        else:
            items.append('<li aria-current="page">%s</li>' % libelle)
    return ('<div class="conteneur fil-ariane"><nav aria-label="Fil d\'Ariane">'
            '<ol>%s</ol></nav></div>' % "".join(items))


def pied(prof):
    p = prefixe(prof)
    horaires = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (j, h) for j, h in HORAIRES)
    def colonne(entrees):
        return "".join('<li><a href="%s%s">%s</a></li>' % (p, url, libelle)
                       for url, libelle in entrees)

    liens_formations = colonne(FORMATIONS)
    liens_infos = colonne([(u, l) for u, l in NAV if u != GROUPE_FORMATIONS] + SECONDAIRE)
    return """
<footer class="pied">
  <div class="conteneur">
    <div class="pied__grille">
      <div>
        <h2>%s</h2>
        <address>
          %s<br>%s %s<br>
          <a href="tel:%s">%s</a><br>
          <a href="mailto:%s">%s</a>
        </address>
        <p class="mention" style="color:rgba(255,255,255,.7)">
          Agrément préfectoral n° E&nbsp;XX&nbsp;XXX&nbsp;XXXX&nbsp;0 — à compléter.
        </p>
      </div>
      <div>
        <h2>Formations</h2>
        <ul>%s</ul>
      </div>
      <div>
        <h2>Infos pratiques</h2>
        <ul>%s</ul>
      </div>
      <div>
        <h2>Horaires</h2>
        <dl class="pied__horaires">%s</dl>
      </div>
      <div>
        <h2>Venir nous voir</h2>
        <p class="mention" style="color:rgba(255,255,255,.85);max-width:16rem">
          Métro Michel Bizot (ligne 8) à 3 minutes à pied, Porte Dorée (ligne 8) à 7 minutes.
          Bus 46 et 87.
        </p>
        <p><a class="bouton bouton--principal" href="%scontact.html">Prendre rendez-vous</a></p>
      </div>
    </div>
    <div class="pied__bas">
      <p class="sans-marge-bas">© 2026 %s — %s %s %s</p>
      <p class="sans-marge-bas">Maquette réalisée par <a href="%s">%s</a></p>
    </div>
  </div>
</footer>""" % (NOM, RUE, CODE_POSTAL, VILLE, TEL_LIEN, TEL_AFFICHE, COURRIEL, COURRIEL,
                liens_formations, liens_infos, horaires, p, NOM, RUE, CODE_POSTAL,
                VILLE, AGENCE_SITE, AGENCE)


def appel_action(prof, titre="Envie de commencer&nbsp;?",
                 texte="Un rendez-vous de 15 minutes à l'agence suffit pour monter votre dossier, "
                       "choisir votre formule et fixer votre première leçon.",
                 lien_secondaire=("tarifs.html", "Voir les tarifs")):
    p = prefixe(prof)
    return """
<section class="section">
  <div class="conteneur">
    <div class="appel">
      <h2>%s</h2>
      <p>%s</p>
      <div class="boutons">
        <a class="bouton bouton--principal" href="%scontact.html">Demander un rappel</a>
        <a class="bouton bouton--secondaire" href="tel:%s">Appeler le %s</a>
        <a class="bouton bouton--secondaire" href="%s%s">%s</a>
      </div>
    </div>
  </div>
</section>""" % (titre, texte, p, TEL_LIEN, TEL_AFFICHE, p,
                 lien_secondaire[0], lien_secondaire[1])


# ---------------------------------------------------------------------------
# Gabarit de page
# ---------------------------------------------------------------------------
def page(fichier, titre, description, corps, prof=0, fil=None, schemas=(), page_nav=None):
    """Assemble une page complète.

    titre       — balise <title>, 60 caractères visés, mot-clé en tête.
    description — meta description, 150 à 160 caractères, avec un appel à l'action.
    """
    p = prefixe(prof)
    canonique = SITE + "/" + ("" if fichier == "index.html" else fichier)
    blocs = list(schemas)
    if fil:
        blocs.append(fil_ariane_schema(fil, prof))
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="theme-color" content="#123fa8">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="%sassets/css/bizot.css?v=%s">%s
</head>
<body>
<a class="saut-navigation" href="#contenu">Aller au contenu</a>
%s
<main id="contenu">
%s
%s
</main>
%s
<script src="%sassets/js/site.js?v=%s" defer></script>
</body>
</html>
""" % (titre, description, canonique, NOM, titre, description, canonique,
       p, empreinte("assets/css/bizot.css"), jsonld(*blocs),
       entete(page_nav or fichier, prof), fil_ariane(fil, prof), corps,
       pied(prof), p, empreinte("assets/js/site.js"))
