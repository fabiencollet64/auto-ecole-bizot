# -*- coding: utf-8 -*-
"""Assemble les pages générées en un seul fichier, pour partager la maquette.

    python3 outils/generer.py && python3 outils/maquette-unique.py

Produit maquette-complete.html : un fichier autonome, sans ressource
externe, qui contient les douze pages et une navigation interne par ancre.
Utile pour envoyer la maquette par courriel, l'ouvrir hors ligne ou la publier
telle quelle. Le site réel reste le jeu de pages HTML séparées : c'est lui qui
est référencé, ce fichier n'est qu'un véhicule de démonstration.
"""
import os
import posixpath
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    "index.html", "permis-voiture.html", "permis-moto.html", "code-de-la-route.html",
    "tarifs.html", "financement.html", "auto-ecole-paris-12.html", "a-propos.html",
    "contact.html", "blog.html",
    "blog/prix-permis-de-conduire-paris.html", "blog/permis-a2-moto-paris.html",
]


def lire(chemin):
    with open(os.path.join(RACINE, chemin), encoding="utf-8") as f:
        return f.read()


def extraire(source, balise, attributs=""):
    motif = r"<%s%s>(.*?)</%s>" % (balise, attributs, balise)
    trouve = re.search(motif, source, re.S)
    return trouve.group(1) if trouve else ""


def clef(page, href):
    """Transforme un lien relatif en identifiant de section."""
    return posixpath.normpath(posixpath.join(posixpath.dirname(page), href))


def reecrire_liens(html, page):
    """Les liens internes deviennent des ancres ; le reste est laissé intact."""
    def remplacer(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            return m.group(0)
        ancre, _, fragment = href.partition("#")
        cible = clef(page, ancre)
        if cible in PAGES:
            return 'href="#%s"' % cible
        return m.group(0)
    return re.sub(r'href="([^"]+)"', remplacer, html)


def construire():
    index = lire("index.html")
    css = lire("assets/css/bizot.css")
    js = lire("assets/js/site.js")

    entete = extraire(index, "header", r' class="entete"')
    pied = extraire(index, "footer", r' class="pied"')
    bandeau = re.search(r'<div class="bandeau-maquette">.*?</div>', index, re.S).group(0)

    sections, titres = [], {}
    for page in PAGES:
        source = lire(page)
        titre = extraire(source, "title")
        corps = extraire(source, "main", r' id="contenu"')
        titres[page] = titre
        sections.append(
            '<section class="page" data-page="%s" hidden>%s</section>'
            % (page, reecrire_liens(corps, page)))

    entete = reecrire_liens(entete, "index.html")
    pied = reecrire_liens(pied, "index.html")

    routeur = """
(function () {
  "use strict";
  var titres = %s;
  var pages = document.querySelectorAll("[data-page]");
  function afficher(clef) {
    if (!titres[clef]) clef = "index.html";
    Array.prototype.forEach.call(pages, function (p) {
      p.hidden = p.getAttribute("data-page") !== clef;
    });
    document.title = titres[clef];
    Array.prototype.forEach.call(document.querySelectorAll(".nav__lien"), function (a) {
      var cible = (a.getAttribute("href") || "").replace(/^#/, "");
      if (cible === clef) { a.setAttribute("aria-current", "page"); }
      else { a.removeAttribute("aria-current"); }
    });
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", function () {
    afficher(decodeURIComponent(location.hash.slice(1)));
  });
  afficher(decodeURIComponent(location.hash.slice(1)) || "index.html");
})();
""" % _json(titres)

    return """<title>Maquette Auto-école Bizot</title>
<style>
%s
/* Assemblage en fichier unique : les douze pages cohabitent, une seule est
   affichée à la fois. */
.page[hidden] { display: none !important; }
</style>
<a class="saut-navigation" href="#contenu">Aller au contenu</a>
%s
%s
<div id="contenu">
%s
</div>
%s
<script>
%s
%s
</script>
""" % (css, bandeau, entete, "\n".join(sections), pied, js, routeur)


def _json(dictionnaire):
    import json
    return json.dumps(dictionnaire, ensure_ascii=False)


if __name__ == "__main__":
    sortie = os.path.join(RACINE, "maquette-complete.html")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(construire())
    print("écrit  maquette-complete.html (%d Ko)"
          % (os.path.getsize(sortie) // 1024))
