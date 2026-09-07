# -*- coding: utf-8 -*-
"""Génère les pages de la maquette Auto Moto École Bizot.

    python3 outils/generer.py

Les pages HTML ne s'écrivent pas à la main : l'en-tête, le pied de page, les
coordonnées et les données structurées viennent de gabarits.py. Le contenu
rédactionnel ci-dessous est un contenu d'amorçage, à faire valider par
l'auto-école — voir README.md § Contenu à valider.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gabarits as g

RACINE = g.RACINE
PAGES = []


def ecrire(chemin_relatif, contenu):
    chemin = os.path.join(RACINE, chemin_relatif)
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print("écrit  " + chemin_relatif)


def publier(fichier, **kwargs):
    ecrire(fichier, g.page(fichier, **kwargs))
    PAGES.append(fichier)


# ---------------------------------------------------------------------------
# Fragments réutilisables
# ---------------------------------------------------------------------------
def carte(icone, titre, texte, points=(), prix=None, lien=None, classe="carte"):
    html = ['<article class="%s">' % classe]
    html.append('<span class="carte__icone">%s</span>' % g.icone(icone))
    html.append('<h3>%s</h3>' % titre)
    if prix:
        html.append('<p class="carte__prix">%s<small>%s</small></p>' % prix)
    html.append('<p>%s</p>' % texte)
    if points:
        html.append('<ul class="liste-cochee">%s</ul>'
                    % "".join('<li>%s<span>%s</span></li>' % (g.coche(), pt) for pt in points))
    if lien:
        html.append('<p class="carte__pied"><a class="bouton bouton--secondaire bouton--large" '
                    'href="%s">%s</a></p>' % lien)
    html.append('</article>')
    return "".join(html)


def etapes(liste):
    return '<div class="grille grille--4">%s</div>' % "".join(
        '<div class="etape"><span class="etape__numero">%d</span><h3>%s</h3><p>%s</p></div>'
        % (rang, titre, texte) for rang, (titre, texte) in enumerate(liste, start=1))


def faq_html(questions, titre="Questions fréquentes"):
    blocs = "".join(
        '<details><summary>%s</summary><div><p>%s</p></div></details>' % (q, r)
        for q, r in questions)
    return """
<section class="section section--claire">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">Vous vous demandez…</span>
      <h2>%s</h2>
      <p>Les réponses ci-dessous sont volontairement courtes et complètes : c'est sous cette
      forme que Google les affiche en résultat enrichi et que ChatGPT ou Gemini les citent.</p>
    </div>
    <div class="faq">%s</div>
  </div>
</section>""" % (titre, blocs)


def photo(legende, classe="photo"):
    return ('<div class="%s" role="img" aria-label="%s"><span>Emplacement photo — %s</span></div>'
            % (classe, legende, legende))


def avis(note, texte, auteur, detail):
    etoiles = "".join(g.icone("etoile") for _ in range(note))
    return """<figure class="avis">
  <p class="note"><span class="note__etoiles" aria-hidden="true">%s</span>
    <span class="note__texte">%d sur 5</span></p>
  <blockquote>%s</blockquote>
  <figcaption>%s — %s</figcaption>
</figure>""" % (etoiles, note, texte, auteur, detail)


def tableau(titre, colonnes, lignes):
    entetes = "".join('<th scope="col">%s</th>' % c for c in colonnes)
    corps = "".join(
        '<tr><th scope="row">%s</th>%s</tr>'
        % (l[0], "".join('<td>%s</td>' % c for c in l[1:]))
        for l in lignes)
    return """<div class="tableau-enveloppe">
  <table class="tarifs">
    <caption>%s</caption>
    <thead><tr>%s</tr></thead>
    <tbody>%s</tbody>
  </table>
</div>""" % (titre, entetes, corps)


def formulaire(identifiant, titre, intro, compact=False):
    """Formulaire de contact. Sans serveur : la maquette confirme à l'écran."""
    formations = ["Permis B — boîte manuelle", "Permis B — boîte automatique",
                  "Conduite accompagnée (AAC)", "Permis moto A1 / A2",
                  "Formation 125 cm³ (7 h)", "Code de la route seul", "Je ne sais pas encore"]
    options = "".join('<option>%s</option>' % f for f in formations)
    message = "" if compact else """
      <div class="champ">
        <label for="%s-message">Votre message (facultatif)</label>
        <textarea id="%s-message" name="message" rows="4"
          placeholder="Vos disponibilités, vos questions…"></textarea>
      </div>""" % (identifiant, identifiant)
    courriel = "" if compact else """
        <div class="champ">
          <label for="%s-courriel">Courriel</label>
          <input id="%s-courriel" name="courriel" type="email" autocomplete="email">
        </div>""" % (identifiant, identifiant)
    return """<form class="pile" data-demo novalidate>
  <h2>%s</h2>
  <p>%s</p>
  <div class="champs-2">
    <div class="champ">
      <label for="%s-prenom">Prénom</label>
      <input id="%s-prenom" name="prenom" type="text" autocomplete="given-name" required>
    </div>
    <div class="champ">
      <label for="%s-tel">Téléphone</label>
      <input id="%s-tel" name="telephone" type="tel" autocomplete="tel" required>
    </div>%s
  </div>
  <div class="champ">
    <label for="%s-formation">Formation souhaitée</label>
    <select id="%s-formation" name="formation">%s</select>
  </div>%s
  <p class="champ"><button class="bouton bouton--principal bouton--large" type="submit">
    Être rappelé gratuitement</button></p>
  <p class="mention">Réponse sous 24 h ouvrées. Vos données servent uniquement à vous
  recontacter et ne sont jamais transmises à un tiers.</p>
  <div class="formulaire__retour" data-retour role="status" hidden></div>
</form>""" % (titre, intro, identifiant, identifiant, identifiant, identifiant, courriel,
              identifiant, identifiant, options, message)


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
FAQ_ACCUEIL = [
    ("Combien coûte le permis de conduire chez Auto Moto École Bizot ?",
     "Le forfait permis B de 20 heures est affiché à 990 € tout inclus, en boîte manuelle "
     "comme en boîte automatique. Le forfait moto A2 de 20 heures est à 890 € tout inclus. "
     "Ces montants comprennent l'accès au code en ligne, l'accompagnement du dossier et la "
     "présentation aux examens ; les heures supplémentaires éventuelles sont facturées à l'unité."),
    ("Où se trouve l'auto-école dans le 12e arrondissement ?",
     "Au 113 avenue du Général Michel Bizot, 75012 Paris, à trois minutes à pied du métro "
     "Michel Bizot (ligne 8) et à sept minutes de Porte Dorée. Les bus 46 et 87 desservent "
     "l'avenue."),
    ("Puis-je bénéficier de l'aide de la Région Île-de-France ?",
     "Oui. L'auto-école est partenaire du dispositif régional : les jeunes Franciliens de 18 à "
     "25 ans peuvent obtenir jusqu'à 1 000 € d'aide, sous conditions de ressources et "
     "d'engagement citoyen. Nous montons le dossier avec vous lors de l'inscription."),
    ("En combien de temps peut-on obtenir son permis ?",
     "Comptez en moyenne trois à quatre mois entre l'inscription et l'examen pratique, en "
     "tenant compte du délai d'obtention du code et de l'attribution d'une place d'examen. "
     "Une formule accélérée permet de passer le permis en quelques semaines si votre "
     "disponibilité le permet."),
    ("Proposez-vous la conduite accompagnée ?",
     "Oui, dès 15 ans, ainsi que la conduite supervisée à partir de 18 ans. Les deux formules "
     "incluent la formation initiale de 20 heures, les rendez-vous pédagogiques et le suivi "
     "de l'accompagnateur."),
    ("Faut-il déjà avoir le code pour s'inscrire ?",
     "Non. Vous pouvez vous inscrire à la formation complète — code et conduite — ou à la "
     "conduite seule si vous détenez déjà un code en cours de validité (valable cinq ans et "
     "cinq présentations à l'examen pratique)."),
]

CORPS_ACCUEIL = """
<section class="heros sur-fond-sombre">
  <div class="conteneur heros__grille">
    <div>
      <span class="badge badge--sombre">Auto-école familiale · Paris 12e</span>
      <h1>Votre permis <em>voiture</em> ou <em>moto</em> à Paris 12, sans stress</h1>
      <p class="heros__accroche">Formation au permis B, à la moto et au code de la route,
      à trois minutes du métro Michel Bizot. Des moniteurs disponibles, des places d'examen
      suivies, et un forfait tout inclus annoncé dès le premier rendez-vous.</p>
      <ul class="heros__preuves">
        <li>%s<span><strong>990 € tout inclus</strong> — forfait 20 h, boîte manuelle ou automatique</span></li>
        <li>%s<span><strong>890 € tout inclus</strong> — forfait moto A2 de 20 h</span></li>
        <li>%s<span><strong>Jusqu'à 1 000 € d'aide</strong> Région Île-de-France pour les 18-25 ans</span></li>
      </ul>
      <div class="boutons" style="margin-top:2rem">
        <a class="bouton bouton--principal" href="tarifs.html">Voir les tarifs</a>
        <a class="bouton bouton--secondaire" href="tel:%s">Appeler le %s</a>
      </div>
    </div>
    <div class="encart-devis">%s</div>
  </div>
</section>

<section class="rassurance">
  <div class="conteneur">
    <ul class="rassurance__liste">
      <li>%s<span>Auto-école agréée par la préfecture</span></li>
      <li>%s<span>Métro Michel Bizot — ligne 8</span></li>
      <li>%s<span>Boîte manuelle et boîte automatique</span></li>
      <li>%s<span>Permis moto A1, A2 et 125 cm³</span></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">Nos formations</span>
      <h2>Trois parcours, un seul interlocuteur</h2>
      <p>Vous êtes suivi par le même moniteur du premier cours au jour de l'examen. Le
      programme est fixé après une évaluation de départ, et le nombre d'heures réellement
      utile vous est annoncé avant de signer.</p>
    </div>
    <div class="grille grille--3">%s%s%s</div>
  </div>
</section>

<section class="section section--claire">
  <div class="conteneur">
    <div class="grille grille--texte-media">
      <div>
        <span class="surtitre">L'auto-école</span>
        <h2>Une école familiale, pas une usine à permis</h2>
        <p>Auto Moto École Bizot est une structure indépendante du 12<sup>e</sup>
        arrondissement. Les plannings sont tenus par la même équipe que celle qui vous
        accueille : quand vous appelez, on sait où vous en êtes.</p>
        <ul class="liste-cochee">
          <li>%s<span>Évaluation de départ offerte, sans engagement</span></li>
          <li>%s<span>Leçons de 1 h ou 2 h, du lundi au samedi</span></li>
          <li>%s<span>Véhicules récents en boîte manuelle et automatique</span></li>
          <li>%s<span>Suivi de progression remis après chaque leçon</span></li>
          <li>%s<span>Accompagnement du dossier ANTS de bout en bout</span></li>
        </ul>
        <p><a class="bouton bouton--secondaire" href="a-propos.html">Découvrir l'équipe</a></p>
      </div>
      %s
    </div>
  </div>
</section>

<section class="section section--sombre">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">En bref</span>
      <h2>Ce qui compte quand on choisit son auto-école</h2>
    </div>
    <div class="grille grille--4">
      <div class="chiffre"><span class="chiffre__valeur">20 h</span>
        <p>La formation minimale légale, incluse dans nos forfaits — et le point de départ
        d'un programme ajusté à votre niveau.</p></div>
      <div class="chiffre"><span class="chiffre__valeur">1 000 €</span>
        <p>L'aide maximale de la Région Île-de-France pour les 18-25 ans, que nous montons
        avec vous à l'inscription.</p></div>
      <div class="chiffre"><span class="chiffre__valeur">3 min</span>
        <p>À pied depuis le métro Michel Bizot, ligne 8. Bus 46 et 87 au pied de l'agence.</p></div>
      <div class="chiffre"><span class="chiffre__valeur">6 j / 7</span>
        <p>Du lundi au samedi, leçons de conduite et cours de code en salle.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">Comment ça se passe</span>
      <h2>De votre premier appel au jour de l'examen</h2>
      <p>Aucune étape administrative n'est laissée à votre charge&nbsp;: nous montons le
      dossier, réservons les examens et suivons les délais de convocation.</p>
    </div>
    %s
  </div>
</section>

<section class="section section--claire">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">Ils ont passé leur permis ici</span>
      <h2>Ce que disent les élèves</h2>
      <p>Emplacement prévu pour vos avis Google réels — le module se connecte à la fiche
      Google Business Profile et se met à jour tout seul.</p>
    </div>
    <div class="grille grille--3">%s%s%s</div>
    <p style="margin-top:1.5rem"><a class="bouton bouton--secondaire"
      href="contact.html">Laisser un avis / nous contacter</a></p>
  </div>
</section>

%s

<section class="section">
  <div class="conteneur">
    <div class="grille grille--texte-media">
      <div>
        <span class="surtitre">Nous trouver</span>
        <h2>113 avenue du Général Michel Bizot, Paris 12<sup>e</sup></h2>
        <p>Passez à l'agence pour l'évaluation de départ&nbsp;: elle dure vingt minutes et
        ne vous engage à rien. Pensez à apporter une pièce d'identité si vous souhaitez
        ouvrir votre dossier dans la foulée.</p>
        <dl class="pile" style="font-size:1rem">%s</dl>
        <div class="boutons" style="margin-top:1.5rem">
          <a class="bouton bouton--principal" href="contact.html">Prendre rendez-vous</a>
          <a class="bouton bouton--secondaire" href="tel:%s">%s</a>
        </div>
      </div>
      <div class="plan"><span>Emplacement carte — plan Google Maps de l'agence,
      chargé après consentement aux cookies.</span></div>
    </div>
  </div>
</section>
"""


def accueil():
    horaires = "".join(
        '<div style="display:flex;justify-content:space-between;gap:2rem;max-width:22rem;'
        'border-bottom:1px solid var(--trait);padding:.35rem 0">'
        '<dt>%s</dt><dd style="margin:0;font-weight:700">%s</dd></div>' % (j, h)
        for j, h in g.HORAIRES)

    corps = CORPS_ACCUEIL % (
        g.coche(), g.coche(), g.coche(), g.TEL_LIEN, g.TEL_AFFICHE,
        formulaire("accueil", "Être rappelé sous 24 h",
                   "Laissez votre numéro : nous vous rappelons pour faire le point sur "
                   "votre situation et le budget réel de votre permis.", compact=True),
        g.icone("bouclier"), g.icone("metro"), g.icone("voiture"), g.icone("moto"),
        carte("voiture", "Permis B — voiture",
              "Boîte manuelle ou automatique, en formation classique, accompagnée ou supervisée.",
              ["Forfait 20 h tout inclus", "Conduite accompagnée dès 15 ans",
               "Boîte automatique en 13 h possible", "Formule accélérée sur demande"],
              prix=("990 €", "forfait 20 h, tout inclus"),
              lien=("permis-voiture.html", "Voir la formation voiture"),
              classe="carte carte--formation"),
        carte("moto", "Permis moto — A1 et A2",
              "Plateau et circulation avec un moniteur moto dédié, sur des machines adaptées à "
              "votre gabarit.",
              ["Forfait A2 20 h tout inclus", "Permis A1 dès 16 ans",
               "Passerelle A2 vers A en 7 h", "Formation 125 cm³ en 7 h"],
              prix=("890 €", "forfait A2 20 h, tout inclus"),
              lien=("permis-moto.html", "Voir la formation moto"),
              classe="carte carte--formation"),
        carte("code", "Code de la route",
              "Cours en salle avec un enseignant et entraînement en ligne illimité depuis chez vous.",
              ["Accès en ligne illimité", "Cours en salle chaque semaine",
               "Inscription à l'examen prise en charge", "Code accéléré possible"],
              prix=("Inclus", "dans les forfaits permis"),
              lien=("code-de-la-route.html", "Voir la formation au code"),
              classe="carte carte--formation"),
        g.coche(), g.coche(), g.coche(), g.coche(), g.coche(),
        photo("l'équipe de l'auto-école devant l'agence, avenue du Général Michel Bizot",
              "photo photo--haute"),
        etapes([
            ("Le premier rendez-vous",
             "Vingt minutes à l'agence : évaluation de départ, nombre d'heures conseillé et "
             "budget annoncé sans surprise."),
            ("Le dossier",
             "Nous créons votre compte ANTS, réunissons les pièces et suivons l'attribution "
             "de votre numéro NEPH."),
            ("Le code",
             "Cours en salle et entraînement en ligne illimité, puis inscription à l'examen "
             "théorique dès que vos scores le permettent."),
            ("La conduite et l'examen",
             "Leçons de 1 h ou 2 h avec le même moniteur, bilan à mi-parcours, puis "
             "présentation à l'examen pratique."),
        ]),
        avis(5, "« Équipe très à l'écoute, on sent qu'ils connaissent chaque élève. J'ai eu "
                "mon permis du premier coup après un parcours calme et bien organisé. »",
             "Avis d'illustration", "à remplacer par un avis Google"),
        avis(5, "« Les moniteurs prennent le temps d'expliquer et les créneaux sont faciles à "
                "trouver, même en travaillant. »",
             "Avis d'illustration", "à remplacer par un avis Google"),
        avis(5, "« Formation moto sérieuse, du plateau jusqu'à la circulation dans Paris. »",
             "Avis d'illustration", "à remplacer par un avis Google"),
        faq_html(FAQ_ACCUEIL),
        horaires, g.TEL_LIEN, g.TEL_AFFICHE,
    )

    publier("index.html",
            titre="Auto-école à Paris 12 — permis voiture et moto | Auto Moto École Bizot",
            description="Auto-école familiale au 113 avenue du Général Michel Bizot, Paris 12e. "
                        "Permis B dès 990 € tout inclus, permis moto A2 dès 890 €, code inclus. "
                        "Aide Région jusqu'à 1 000 €.",
            corps=corps,
            schemas=[g.etablissement(), g.faq_schema(FAQ_ACCUEIL),
                     {"@context": "https://schema.org", "@type": "WebSite",
                      "name": g.NOM, "url": g.SITE + "/"}])


# ---------------------------------------------------------------------------
# Bandeau de titre des pages internes
# ---------------------------------------------------------------------------
def bandeau(surtitre, titre, chapeau, boutons=True):
    actions = ""
    if boutons:
        actions = """
      <div class="boutons" style="margin-top:1.75rem">
        <a class="bouton bouton--principal" href="contact.html">Demander un rappel</a>
        <a class="bouton bouton--secondaire" href="tel:%s">Appeler le %s</a>
      </div>""" % (g.TEL_LIEN, g.TEL_AFFICHE)
    return """
<section class="heros sur-fond-sombre" style="padding-block:3.5rem 3rem">
  <div class="conteneur">
    <span class="surtitre">%s</span>
    <h1>%s</h1>
    <p class="heros__accroche">%s</p>%s
  </div>
</section>""" % (surtitre, titre, chapeau, actions)


def section_texte(surtitre, titre, contenu, claire=False):
    return """
<section class="section%s">
  <div class="conteneur">
    <div class="section__intro">
      <span class="surtitre">%s</span>
      <h2>%s</h2>
    </div>
    %s
  </div>
</section>""" % (" section--claire" if claire else "", surtitre, titre, contenu)


# ---------------------------------------------------------------------------
# Permis voiture
# ---------------------------------------------------------------------------
FAQ_VOITURE = [
    ("Combien d'heures de conduite faut-il pour avoir le permis B ?",
     "La loi impose au minimum 20 heures de conduite en boîte manuelle et 13 heures en boîte "
     "automatique. La moyenne nationale se situe plutôt autour de 30 à 35 heures : c'est "
     "pourquoi nous annonçons un forfait de départ à 20 heures et un tarif horaire clair pour "
     "les heures supplémentaires, plutôt qu'un forfait gonflé."),
    ("Quelle différence entre conduite accompagnée et conduite supervisée ?",
     "La conduite accompagnée (AAC) démarre dès 15 ans, après 20 heures de formation, et impose "
     "3 000 km sur au moins un an avant l'examen. La conduite supervisée s'adresse aux plus de "
     "18 ans, sans kilométrage minimum : elle sert à prendre de l'expérience avant l'examen ou "
     "après un échec."),
    ("Le permis boîte automatique permet-il de conduire une boîte manuelle ?",
     "Non, pas immédiatement. Après trois mois de permis boîte automatique, une formation "
     "passerelle de 7 heures, sans examen, permet d'obtenir le permis boîte manuelle."),
    ("Combien de temps mon code reste-t-il valable ?",
     "Cinq ans, et pour cinq présentations à l'examen pratique. Au-delà, il faut le repasser."),
]

DEROULE_VOITURE = [
    ("Évaluation de départ",
     "Une heure sur simulateur ou en voiture pour situer votre niveau et estimer honnêtement "
     "le volume d'heures nécessaire."),
    ("Le code",
     "Cours en salle et entraînement en ligne illimité jusqu'à l'obtention de l'examen théorique."),
    ("La conduite",
     "Quatre compétences travaillées dans l'ordre du programme national : maîtriser, "
     "appréhender, circuler, pratiquer."),
    ("L'examen",
     "Bilan de fin de formation, puis présentation à l'examen pratique sur un centre "
     "d'examen parisien que vous aurez travaillé en leçon."),
]


def permis_voiture():
    corps = "".join([
        bandeau("Permis B", "Permis voiture à Paris 12 — boîte manuelle ou automatique",
                "Formation classique, conduite accompagnée dès 15 ans ou conduite supervisée : "
                "trois chemins vers le même permis, avec le même suivi et un budget annoncé "
                "à l'avance."),
        section_texte("Les formules", "Choisissez le parcours qui vous ressemble",
                      '<div class="grille grille--3">%s%s%s</div>' % (
            carte("voiture", "Formation classique",
                  "Le parcours le plus courant : code puis conduite, à votre rythme, "
                  "avec un objectif d'examen fixé ensemble.",
                  ["Dès 17 ans pour la conduite", "20 h minimum en boîte manuelle",
                   "13 h minimum en boîte automatique", "Leçons de 1 h ou 2 h"],
                  prix=("990 €", "forfait 20 h tout inclus")),
            carte("personne", "Conduite accompagnée (AAC)",
                  "À partir de 15 ans. Après la formation initiale, vous conduisez avec un "
                  "proche pendant au moins un an et 3 000 km.",
                  ["Meilleur taux de réussite à l'examen", "Assurance souvent réduite ensuite",
                   "2 rendez-vous pédagogiques inclus", "Examen possible dès 17 ans"],
                  prix=("À partir de 1 090 €", "forfait AAC, rendez-vous inclus")),
            carte("eclair", "Formule accélérée",
                  "Un permis en quelques semaines quand votre planning le permet : leçons "
                  "groupées et place d'examen réservée en amont.",
                  ["Conduite tous les jours ou presque", "Code accéléré possible",
                   "Sous réserve des places d'examen", "Devis établi au rendez-vous"],
                  prix=("Sur devis", "selon disponibilité des places")),
        )),
        section_texte("Le déroulé", "Comment se passe la formation", etapes(DEROULE_VOITURE),
                      claire=True),
        section_texte("Bon à savoir", "Le détail qui change le budget", """
    <div class="grille grille--2">
      <div>
        <p>Un forfait n'est pas un prix final : la moyenne nationale tourne autour de
        30 heures de conduite. Nous préférons annoncer un forfait de 20 heures au prix juste
        et un tarif horaire clair, plutôt qu'un forfait gonflé dont vous n'utiliserez
        peut-être pas la moitié.</p>
        <ul class="liste-cochee">
          <li>%s<span>Heure supplémentaire : 55 € — sans majoration de dernière minute</span></li>
          <li>%s<span>Frais de dossier et présentation à l'examen inclus</span></li>
          <li>%s<span>Aucun frais de résiliation caché : le contrat est remis à l'inscription</span></li>
        </ul>
        <p><a class="bouton bouton--secondaire" href="tarifs.html">Voir la grille complète</a></p>
      </div>
      %s
    </div>""" % (g.coche(), g.coche(), g.coche(),
                 photo("une leçon de conduite dans le 12e arrondissement")), ),
        faq_html(FAQ_VOITURE),
        g.appel_action(0, lien_secondaire=("financement.html", "Aides et financement")),
    ])
    publier("permis-voiture.html",
            titre="Permis voiture à Paris 12 — permis B dès 990 € | Auto Moto École Bizot",
            description="Permis B boîte manuelle ou automatique à Paris 12 : forfait 20 h à "
                        "990 € tout inclus, conduite accompagnée dès 15 ans, formule accélérée. "
                        "Inscription en ligne ou à l'agence.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Permis voiture")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_VOITURE),
                     {"@context": "https://schema.org", "@type": "Service",
                      "serviceType": "Formation au permis de conduire catégorie B",
                      "provider": {"@id": g.SITE + "/#etablissement"},
                      "areaServed": {"@type": "City", "name": "Paris"},
                      "offers": {"@type": "Offer", "price": "990", "priceCurrency": "EUR",
                                 "description": "Forfait 20 heures tout inclus"}}])


# ---------------------------------------------------------------------------
# Permis moto
# ---------------------------------------------------------------------------
FAQ_MOTO = [
    ("Quelle est la différence entre le permis A1, A2 et A ?",
     "Le permis A1 se passe dès 16 ans et donne accès aux motos de 125 cm³ (11 kW). Le permis "
     "A2, accessible dès 18 ans, autorise les motos jusqu'à 35 kW. Après deux ans de permis A2, "
     "une formation passerelle de 7 heures donne accès au permis A, sans limitation de puissance."),
    ("Comment se passe l'examen du permis moto ?",
     "L'examen comporte deux épreuves pratiques : le plateau — vérifications, maniabilité à "
     "allure lente puis à allure normale, freinage d'urgence — puis la circulation, environ "
     "40 minutes sur route avec l'inspecteur en liaison radio."),
    ("Puis-je conduire un 125 cm³ avec mon permis B ?",
     "Oui, après deux ans de permis B et une formation de 7 heures : 2 heures de théorie, "
     "2 heures de plateau et 3 heures en circulation. Aucun examen à passer à l'issue."),
    ("Faut-il un équipement personnel pour commencer ?",
     "L'auto-école prête le casque et les gants homologués pour les premières séances. Pour la "
     "suite de la formation, un équipement personnel — blouson, gants, bottes — est demandé, "
     "et nous vous conseillons avant l'achat."),
]


def permis_moto():
    corps = "".join([
        bandeau("Permis A1, A2 et 125 cm³", "Permis moto à Paris 12 — du plateau à la circulation",
                "Un moniteur moto dédié, des machines adaptées à votre gabarit et un plateau "
                "travaillé jusqu'à ce que les trajectoires deviennent naturelles."),
        section_texte("Les formations", "Quatre parcours moto",
                      '<div class="grille grille--2">%s%s%s%s</div>' % (
            carte("moto", "Permis A2",
                  "La formation de référence dès 18 ans : motos jusqu'à 35 kW, plateau et "
                  "circulation.",
                  ["20 h de formation pratique minimum", "8 h de plateau, 12 h de circulation",
                   "Prêt du casque et des gants au démarrage", "Présentation aux deux examens incluse"],
                  prix=("890 €", "forfait 20 h tout inclus")),
            carte("moto", "Permis A1 — dès 16 ans",
                  "Pour rouler en 125 cm³ dès 16 ans, avec le même programme adapté aux petites "
                  "cylindrées.",
                  ["Accessible dès 16 ans", "Motos 125 cm³ de l'auto-école",
                   "Plateau et circulation", "Code moto (ETM) inclus"],
                  prix=("890 €", "forfait 20 h tout inclus")),
            carte("eclair", "Formation 125 cm³ (7 h)",
                  "Vous avez le permis B depuis deux ans : sept heures suffisent pour rouler en "
                  "125 cm³ ou en scooter à trois roues.",
                  ["2 h de théorie", "2 h de plateau hors circulation",
                   "3 h en circulation", "Attestation remise le jour même"],
                  prix=("330 €", "formation complète, sans examen")),
            carte("bouclier", "Passerelle A2 → A",
                  "Après deux ans de permis A2, sept heures de formation donnent accès au "
                  "permis A sans limitation de puissance.",
                  ["2 h de théorie et d'analyse d'accident", "2 h de maniabilité",
                   "3 h en circulation", "Aucun examen final"],
                  prix=("330 €", "formation passerelle")),
        )),
        section_texte("Le déroulé", "Ce que vous travaillez, séance après séance", etapes([
            ("Prise en main",
             "Position, embrayage, équilibre à allure lente : les fondamentaux, sur le plateau, "
             "hors circulation."),
            ("Le plateau",
             "Maniabilité lente et rapide, freinage d'urgence, vérifications et questions "
             "orales du permis."),
            ("La circulation",
             "Insertion, trajectoires de sécurité, angles morts et cohabitation avec le trafic "
             "parisien."),
            ("Les examens",
             "Présentation au plateau, puis à la circulation, avec une séance de révision "
             "juste avant chaque épreuve."),
        ]), claire=True),
        section_texte("Sécurité", "Rouler à Paris, ça s'apprend", """
    <div class="grille grille--texte-media">
      <div>
        <p>Le 12<sup>e</sup> arrondissement concentre tout ce qui met un motard débutant en
        difficulté : couloirs de bus avenue Daumesnil, pavés, giratoires de la place Félix-Éboué
        et de la Nation, circulation dense sur le boulevard périphérique voisin.</p>
        <p>Nos parcours de formation passent par ces points précis, aux heures où ils sont
        réellement chargés. Vous ne découvrez pas la difficulté le jour de l'examen.</p>
        <ul class="liste-cochee">
          <li>%s<span>Stages de perfectionnement pour motards déjà titulaires du permis</span></li>
          <li>%s<span>Reprise de guidon après une longue interruption</span></li>
          <li>%s<span>Conseils d'équipement avant achat</span></li>
        </ul>
      </div>
      %s
    </div>""" % (g.coche(), g.coche(), g.coche(),
                 photo("une moto d'auto-école sur le plateau d'entraînement"))),
        faq_html(FAQ_MOTO),
        g.appel_action(0, titre="Prêt à monter sur la moto&nbsp;?",
                       texte="Passez à l'agence : nous regardons ensemble votre gabarit, votre "
                             "expérience et le calendrier des places d'examen plateau.",
                       lien_secondaire=("tarifs.html", "Voir les tarifs moto")),
    ])
    publier("permis-moto.html",
            titre="Permis moto à Paris 12 — A1, A2, 125 cm³ | Auto Moto École Bizot",
            description="Permis moto A1 et A2 à Paris 12e : forfait 20 h à 890 € tout inclus, "
                        "formation 125 cm³ en 7 h, passerelle A2 vers A. Moniteur moto dédié, "
                        "plateau et circulation.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Permis moto")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_MOTO),
                     {"@context": "https://schema.org", "@type": "Service",
                      "serviceType": "Formation au permis moto A1 et A2",
                      "provider": {"@id": g.SITE + "/#etablissement"},
                      "areaServed": {"@type": "City", "name": "Paris"},
                      "offers": {"@type": "Offer", "price": "890", "priceCurrency": "EUR",
                                 "description": "Forfait moto A2, 20 heures tout inclus"}}])


# ---------------------------------------------------------------------------
# Code de la route
# ---------------------------------------------------------------------------
FAQ_CODE = [
    ("Comment s'inscrire à l'examen du code de la route ?",
     "L'auto-école s'occupe de tout : création du dossier ANTS, obtention du numéro NEPH puis "
     "réservation d'une place d'examen théorique dans un centre agréé proche du 12e "
     "arrondissement. Vous recevez la convocation par courriel."),
    ("Combien de fautes sont autorisées à l'examen du code ?",
     "L'examen comporte 40 questions ; il faut au moins 35 bonnes réponses, soit 5 fautes "
     "maximum, pour être reçu."),
    ("Combien coûte l'examen du code ?",
     "La redevance d'examen théorique est de 30 €, versée à l'organisme agréé. Dans nos "
     "forfaits permis, la préparation et l'accompagnement à l'inscription sont inclus."),
    ("Peut-on réviser le code depuis chez soi ?",
     "Oui. Chaque élève reçoit un accès personnel à la plateforme d'entraînement en ligne : "
     "séries illimitées, examens blancs et suivi des scores, consultables par le moniteur qui "
     "vous conseille selon vos erreurs."),
]


def code_route():
    corps = "".join([
        bandeau("Code de la route", "Préparer le code à Paris 12 — en salle et en ligne",
                "Un enseignant en salle pour comprendre, une plateforme en ligne pour "
                "s'entraîner autant que nécessaire, et une inscription à l'examen prise en "
                "charge dès que vos scores sont au niveau."),
        section_texte("La méthode", "Deux façons d'apprendre, une seule progression", """
    <div class="grille grille--3">%s%s%s</div>""" % (
            carte("code", "Cours en salle",
                  "Des séances animées par un enseignant : on corrige, on explique, et surtout "
                  "on comprend pourquoi la bonne réponse est la bonne.",
                  ["Plusieurs créneaux par semaine", "Séries commentées en direct",
                   "Questions posées à voix haute"]),
            carte("horloge", "Entraînement en ligne",
                  "Un accès personnel, valable pendant toute la formation, pour réviser depuis "
                  "le téléphone ou l'ordinateur.",
                  ["Séries illimitées", "Examens blancs chronométrés",
                   "Suivi des scores par le moniteur"]),
            carte("eclair", "Code accéléré",
                  "Une formation intensive sur quelques jours pour les candidats pressés ou "
                  "déjà à l'aise.",
                  ["Programme condensé", "Place d'examen réservée en amont",
                   "Bilan quotidien avec l'enseignant"]),
        )),
        section_texte("L'examen", "Ce qui vous attend le jour J", """
    <div class="grille grille--2">
      <div>
        <p>L'examen théorique général se déroule sur tablette, dans un centre agréé, en présence
        d'un surveillant. Quarante questions, une réponse par question, huit secondes environ
        de réflexion. Il faut 35 bonnes réponses pour être reçu.</p>
        <ul class="liste-cochee">
          <li>%s<span>Résultat transmis sous 48 heures par courriel</span></li>
          <li>%s<span>Code valable 5 ans et 5 présentations à l'examen pratique</span></li>
          <li>%s<span>En cas d'échec, nouvelle place réservée sans frais de dossier</span></li>
        </ul>
        <p><a class="bouton bouton--principal" href="contact.html">S'inscrire au code</a></p>
      </div>
      %s
    </div>""" % (g.coche(), g.coche(), g.coche(),
                 photo("la salle de code de l'auto-école", "photo photo--large")), claire=True),
        faq_html(FAQ_CODE),
        g.appel_action(0, lien_secondaire=("permis-voiture.html", "Et après : la conduite")),
    ])
    publier("code-de-la-route.html",
            titre="Code de la route à Paris 12 — cours en salle et en ligne | AME Bizot",
            description="Préparez le code de la route à Paris 12e : cours en salle avec un "
                        "enseignant, entraînement en ligne illimité, code accéléré et "
                        "inscription à l'examen prise en charge.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Code de la route")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_CODE)])


# ---------------------------------------------------------------------------
# Tarifs
# ---------------------------------------------------------------------------
FAQ_TARIFS = [
    ("Le prix affiché est-il vraiment tout compris ?",
     "Le forfait comprend l'évaluation de départ, les heures de conduite annoncées, l'accès au "
     "code en ligne, les frais de dossier et la présentation à l'examen. Restent à votre charge "
     "les éventuelles heures supplémentaires, la redevance d'examen du code de 30 € et une "
     "nouvelle présentation en cas d'échec à la conduite."),
    ("Peut-on payer en plusieurs fois ?",
     "Oui. Le règlement peut être échelonné sans frais sur la durée de la formation ; les "
     "modalités sont écrites dans le contrat remis à l'inscription."),
    ("Que se passe-t-il si j'ai besoin de plus de 20 heures ?",
     "Les heures supplémentaires sont facturées à l'unité, au tarif affiché, sans majoration. "
     "Votre moniteur vous prévient au moins deux leçons à l'avance quand il estime qu'il faudra "
     "prolonger, afin que vous puissiez anticiper le budget."),
    ("Le contrat prévoit-il des frais si j'arrête en cours de route ?",
     "En cas d'arrêt, seules les prestations réalisées sont dues, et le solde vous est restitué. "
     "Les conditions figurent en toutes lettres dans le contrat de formation."),
]


def tarifs():
    disclaimer = """
  <div class="encadre" style="margin-top:0">
    <p><strong>Maquette&nbsp;:</strong> les montants ci-dessous reprennent les informations
    publiques disponibles en ligne et des ordres de grandeur du marché parisien. Ils doivent
    être remplacés par la grille tarifaire officielle de l'auto-école avant mise en ligne —
    l'affichage des prix est une obligation légale et une des premières choses que les
    candidats comparent.</p>
  </div>"""
    corps = "".join([
        bandeau("Tarifs", "Tarifs du permis à Paris 12 — affichés, sans surprise",
                "Un forfait de départ au prix juste, un tarif horaire clair pour les heures "
                "supplémentaires, et aucun frais caché ajouté en cours de route."),
        """
<section class="section">
  <div class="conteneur">
    %s
    <div class="grille grille--2" style="align-items:start">
      %s
      %s
    </div>
    <div class="grille grille--2" style="align-items:start;margin-top:1.5rem">
      %s
      %s
    </div>
    <p class="mention" style="margin-top:1.5rem">Tarifs TTC. La redevance d'examen du code
    (30 €) est versée à l'organisme agréé. Offre de lancement mentionnée en agence&nbsp;:
    −50 € sur les premiers forfaits.</p>
  </div>
</section>""" % (
            disclaimer,
            tableau("Permis voiture (B)", ["Prestation", "Tarif"], [
                ["Forfait 20 h — boîte manuelle", "990 €"],
                ["Forfait 20 h — boîte automatique", "990 €"],
                ["Forfait conduite accompagnée (AAC)", "1 090 €"],
                ["Heure de conduite supplémentaire", "55 €"],
                ["Passerelle boîte auto → boîte manuelle (7 h)", "390 €"],
                ["Évaluation de départ", "Offerte"],
            ]),
            tableau("Permis moto (A1, A2)", ["Prestation", "Tarif"], [
                ["Forfait A2 — 20 h", "890 €"],
                ["Forfait A1 — 20 h", "890 €"],
                ["Formation 125 cm³ (7 h)", "330 €"],
                ["Passerelle A2 → A (7 h)", "330 €"],
                ["Heure de conduite moto supplémentaire", "65 €"],
                ["Stage de perfectionnement", "Sur devis"],
            ]),
            tableau("Code de la route", ["Prestation", "Tarif"], [
                ["Code inclus dans un forfait permis", "Inclus"],
                ["Forfait code seul — salle et en ligne, 12 mois", "390 €"],
                ["Redevance d'examen théorique (organisme agréé)", "30 €"],
                ["Code accéléré", "Sur devis"],
            ]),
            tableau("Frais administratifs", ["Prestation", "Tarif"], [
                ["Frais de dossier et gestion ANTS", "Inclus"],
                ["Présentation à l'examen pratique", "1re incluse"],
                ["Nouvelle présentation à l'examen pratique", "70 €"],
                ["Location du véhicule le jour de l'examen", "Incluse"],
            ]),
        ),
        section_texte("Financement", "Ce que vous ne payez peut-être pas vous-même", """
    <div class="grille grille--texte-media">
      <div>
        <p>Selon votre âge et votre situation, une partie du permis peut être prise en charge.
        Nous vérifions votre éligibilité au rendez-vous d'inscription et montons le dossier
        avec vous.</p>
        <ul class="liste-cochee">
          <li>%s<span>Aide de la Région Île-de-France : jusqu'à 1 000 € pour les 18-25 ans</span></li>
          <li>%s<span>Permis à 1 € par jour : prêt à taux zéro pour les 15-25 ans</span></li>
          <li>%s<span>Compte personnel de formation (CPF), sous conditions</span></li>
          <li>%s<span>Aide de 500 € pour les apprentis majeurs</span></li>
          <li>%s<span>Paiement échelonné sans frais</span></li>
        </ul>
        <p><a class="bouton bouton--principal" href="financement.html">Voir les aides en détail</a></p>
      </div>
      %s
    </div>""" % (g.coche(), g.coche(), g.coche(), g.coche(), g.coche(),
                 photo("un candidat signant son contrat de formation à l'agence")), claire=True),
        faq_html(FAQ_TARIFS),
        g.appel_action(0, lien_secondaire=("financement.html", "Aides et financement")),
    ])
    publier("tarifs.html",
            titre="Tarifs permis voiture et moto à Paris 12 | Auto Moto École Bizot",
            description="Grille tarifaire de l'auto-école Bizot à Paris 12 : permis B 20 h à "
                        "990 € tout inclus, moto A2 à 890 €, code, heures supplémentaires et "
                        "frais administratifs affichés.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Tarifs")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_TARIFS)])


# ---------------------------------------------------------------------------
# Financement
# ---------------------------------------------------------------------------
FAQ_FINANCEMENT = [
    ("Qui peut bénéficier de l'aide au permis de la Région Île-de-France ?",
     "Le dispositif s'adresse aux Franciliens de 18 à 25 ans, sous conditions de ressources et "
     "en contrepartie d'un engagement citoyen ou d'une action bénévole. L'aide peut atteindre "
     "1 000 € et se déduit directement du coût de la formation. Le dossier se dépose en ligne "
     "auprès de la Région ; nous fournissons les pièces émanant de l'auto-école."),
    ("Comment fonctionne le permis à 1 € par jour ?",
     "C'est un prêt à taux zéro, de 600 à 1 200 € selon la formule, accordé par une banque "
     "partenaire aux 15-25 ans. Vous remboursez 30 € par mois, l'État prend en charge les "
     "intérêts. L'auto-école doit être conventionnée : la nôtre remet l'attestation nécessaire "
     "au montage du dossier."),
    ("Le permis est-il finançable avec le CPF ?",
     "Le permis B et certains permis professionnels sont éligibles au compte personnel de "
     "formation lorsque l'obtention du permis contribue à un projet professionnel et que vous "
     "ne faites pas l'objet d'une suspension. La démarche se fait sur moncompteformation.gouv.fr."),
    ("Peut-on cumuler plusieurs aides ?",
     "Oui dans la plupart des cas, à condition que le total des aides ne dépasse pas le coût "
     "réel de la formation. Nous faisons le calcul avec vous avant l'inscription."),
]


def financement():
    corps = "".join([
        bandeau("Aides et financement", "Financer son permis à Paris : les aides existantes",
                "Aide régionale, prêt à taux zéro, CPF, dispositifs pour les apprentis et les "
                "demandeurs d'emploi : nous vérifions votre éligibilité au premier rendez-vous "
                "et montons le dossier avec vous."),
        section_texte("Les dispositifs", "Cinq façons de réduire la facture",
                      '<div class="grille grille--3">%s%s%s%s%s%s</div>' % (
            carte("euro", "Aide de la Région Île-de-France",
                  "Jusqu'à 1 000 € pour les Franciliens de 18 à 25 ans, sous conditions de "
                  "ressources et en contrepartie d'un engagement citoyen.",
                  ["Déduite du coût de la formation", "Dossier déposé en ligne",
                   "Attestations fournies par l'auto-école"]),
            carte("calendrier", "Permis à 1 € par jour",
                  "Un prêt à taux zéro de 600 à 1 200 € pour les 15-25 ans, remboursé 30 € par "
                  "mois. L'État prend en charge les intérêts.",
                  ["Auto-école conventionnée", "Cumulable avec l'aide régionale",
                   "Souscription auprès d'une banque partenaire"]),
            carte("personne", "Compte personnel de formation",
                  "Le permis B est mobilisable via le CPF lorsqu'il sert un projet "
                  "professionnel, sur moncompteformation.gouv.fr.",
                  ["Sans avance de frais", "Complément possible par vos soins",
                   "Devis remis pour la démarche"]),
            carte("bouclier", "Aide aux apprentis",
                  "500 € pour les apprentis d'au moins 18 ans préparant le permis B, sans "
                  "condition de ressources.",
                  ["Cumulable avec les autres aides", "Demande auprès du CFA",
                   "Facture fournie par l'auto-école"]),
            carte("horloge", "Demandeurs d'emploi",
                  "France Travail peut participer au financement lorsque le permis lève un "
                  "frein à l'embauche. Le montant dépend de votre situation.",
                  ["Devis conforme fourni", "Étude avec votre conseiller",
                   "Prise en charge partielle ou totale"]),
            carte("eclair", "Paiement échelonné",
                  "Si aucune aide ne s'applique, le règlement peut être étalé sans frais sur "
                  "la durée de la formation.",
                  ["Aucun frais supplémentaire", "Échéancier écrit au contrat",
                   "Adaptable en cours de formation"]),
        )),
        section_texte("La marche à suivre", "Comment on s'y prend, concrètement", etapes([
            ("On fait le point",
             "Âge, situation, projet professionnel, ressources : vingt minutes suffisent pour "
             "savoir à quoi vous avez droit."),
            ("On monte le dossier",
             "Devis conforme, attestation d'inscription, pièces de l'auto-école : tout ce que "
             "l'organisme financeur réclame, préparé pour vous."),
            ("Vous déposez la demande",
             "En ligne dans la plupart des cas. Nous vous accompagnons pendant la saisie si "
             "vous le souhaitez."),
            ("La formation démarre",
             "Vous commencez sans attendre la réponse dans la majorité des dispositifs, l'aide "
             "venant en déduction du solde."),
        ]), claire=True),
        faq_html(FAQ_FINANCEMENT),
        g.appel_action(0, titre="Vérifions ensemble vos droits",
                       texte="Un appel de dix minutes suffit souvent pour savoir si votre permis "
                             "peut être financé en partie. C'est gratuit et sans engagement.",
                       lien_secondaire=("tarifs.html", "Voir les tarifs")),
    ])
    publier("financement.html",
            titre="Financer son permis à Paris 12 — aides et permis à 1 € | AME Bizot",
            description="Aide Région Île-de-France jusqu'à 1 000 €, permis à 1 € par jour, CPF, "
                        "aide apprentis et France Travail : les aides pour financer votre permis "
                        "à Paris 12, montées avec vous.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Financement")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_FINANCEMENT)])


# ---------------------------------------------------------------------------
# Page locale — « auto-école Paris 12 »
# ---------------------------------------------------------------------------
FAQ_LOCALE = [
    ("Quelle auto-école choisir dans le 12e arrondissement de Paris ?",
     "Comparez quatre points concrets : le prix affiché du forfait et celui de l'heure "
     "supplémentaire, le délai moyen pour obtenir une place d'examen, la possibilité de garder "
     "le même moniteur, et les avis récents. Auto Moto École Bizot est une auto-école familiale "
     "du 12e, située au 113 avenue du Général Michel Bizot, qui forme au permis B, au permis "
     "moto et au code."),
    ("Où passe-t-on l'examen du permis quand on habite Paris 12 ?",
     "Les candidats parisiens sont convoqués dans l'un des centres d'examen d'Île-de-France, "
     "souvent en proche banlieue est. Les leçons de fin de formation se déroulent sur les "
     "itinéraires du centre où vous serez présenté."),
    ("Quels quartiers l'auto-école dessert-elle ?",
     "Le quartier Bel-Air, Picpus, Daumesnil, Bercy, la Nation et le bois de Vincennes, ainsi "
     "que les communes limitrophes : Saint-Mandé, Charenton-le-Pont, Vincennes et Ivry-sur-Seine "
     "pour les élèves qui travaillent dans le 12e."),
    ("Est-ce plus difficile d'apprendre à conduire à Paris ?",
     "La circulation parisienne est dense, mais elle prépare à tout : couloirs de bus, "
     "deux-roues, giratoires chargés, livraisons en double file. Un candidat formé à Paris est "
     "à l'aise partout ensuite. La contrepartie, ce sont des délais d'examen plus longs — d'où "
     "l'importance d'un dossier déposé tôt."),
]


def page_locale():
    corps = "".join([
        bandeau("Auto-école Paris 12", "Auto-école à Paris 12 : permis voiture, moto et code",
                "Nous formons les habitants du 12<sup>e</sup> arrondissement et des communes "
                "voisines, à trois minutes du métro Michel Bizot. Voici tout ce qu'il faut "
                "savoir avant de choisir votre auto-école dans le quartier."),
        section_texte("Zone desservie", "Où sont nos élèves", """
    <div class="grille grille--texte-media">
      <div>
        <p>La plupart de nos candidats habitent ou travaillent à moins de vingt minutes de
        l'agence. Les leçons partent de l'avenue du Général Michel Bizot et rejoignent
        rapidement les axes que vous emprunterez tous les jours.</p>
        <div class="grille grille--2" style="gap:.5rem 2rem">
          <ul class="liste-cochee">
            <li>%s<span>Bel-Air et Picpus</span></li>
            <li>%s<span>Daumesnil et Michel Bizot</span></li>
            <li>%s<span>Bercy et Cour Saint-Émilion</span></li>
            <li>%s<span>Nation et Reuilly-Diderot</span></li>
          </ul>
          <ul class="liste-cochee">
            <li>%s<span>Porte Dorée et bois de Vincennes</span></li>
            <li>%s<span>Saint-Mandé et Vincennes</span></li>
            <li>%s<span>Charenton-le-Pont</span></li>
            <li>%s<span>Paris 11e et 20e limitrophes</span></li>
          </ul>
        </div>
        <p><a class="bouton bouton--secondaire" href="contact.html">Venir à l'agence</a></p>
      </div>
      <div class="plan"><span>Emplacement carte — zone d'intervention autour du
      113 avenue du Général Michel Bizot.</span></div>
    </div>""" % ((g.coche(),) * 8)),
        section_texte("Conduire à Paris 12", "Les points du quartier que nous travaillons en leçon", """
    <div class="grille grille--3">
      <article class="carte"><h3>Place Félix-Éboué</h3>
        <p>Un giratoire à plusieurs voies, très fréquenté, où l'on apprend à choisir sa file
        et à sortir sans hésiter.</p></article>
      <article class="carte"><h3>Avenue Daumesnil</h3>
        <p>Couloirs de bus, cyclistes et livraisons : l'exercice type du contrôle des angles
        morts et de la distance latérale.</p></article>
      <article class="carte"><h3>Place de la Nation</h3>
        <p>Le passage obligé pour comprendre les priorités et l'insertion dans un flux dense.</p></article>
      <article class="carte"><h3>Boulevards des Maréchaux</h3>
        <p>Tramway T3a, feux rapprochés, changements de file : l'anticipation y devient un
        réflexe.</p></article>
      <article class="carte"><h3>Bois de Vincennes</h3>
        <p>Un terrain plus calme, idéal pour les premières heures et pour les manœuvres.</p></article>
      <article class="carte"><h3>Périphérique, porte Dorée</h3>
        <p>Insertion et vitesse, travaillées en fin de formation quand les bases sont acquises.</p></article>
    </div>""", claire=True),
        section_texte("Nos formations", "Ce que vous pouvez préparer chez nous", """
    <div class="grille grille--3">%s%s%s</div>""" % (
            carte("voiture", "Permis B", "Boîte manuelle ou automatique, conduite accompagnée "
                  "ou supervisée, formule accélérée.", (),
                  lien=("permis-voiture.html", "Permis voiture")),
            carte("moto", "Permis moto", "A1 dès 16 ans, A2 dès 18 ans, formation 125 cm³ et "
                  "passerelle A2 vers A.", (),
                  lien=("permis-moto.html", "Permis moto")),
            carte("code", "Code de la route", "Cours en salle et entraînement en ligne "
                  "illimité, code accéléré possible.", (),
                  lien=("code-de-la-route.html", "Code de la route")),
        )),
        faq_html(FAQ_LOCALE, "Auto-école à Paris 12 : les questions qu'on nous pose"),
        g.appel_action(0, titre="Votre auto-école est à trois minutes du métro",
                       texte="113 avenue du Général Michel Bizot, 75012 Paris. Métro Michel Bizot "
                             "ligne 8, bus 46 et 87. Ouvert du lundi au samedi."),
    ])
    publier("auto-ecole-paris-12.html",
            titre="Auto-école Paris 12 — permis voiture, moto et code | AME Bizot",
            description="Auto-école du 12e arrondissement de Paris : permis B, permis moto et "
                        "code, à 3 min du métro Michel Bizot. Quartiers desservis et tarifs "
                        "affichés.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Auto-école Paris 12")],
            schemas=[g.etablissement(), g.faq_schema(FAQ_LOCALE)])


# ---------------------------------------------------------------------------
# À propos
# ---------------------------------------------------------------------------
def a_propos():
    corps = "".join([
        bandeau("L'auto-école", "Une auto-école familiale du 12<sup>e</sup> arrondissement",
                "Une petite structure indépendante, ouverte en 2024 avenue du Général Michel "
                "Bizot, où l'on connaît les élèves par leur prénom et où le moniteur qui vous "
                "évalue est celui qui vous présente à l'examen."),
        section_texte("Notre façon de faire", "Trois engagements simples", """
    <div class="grille grille--3">%s%s%s</div>""" % (
            carte("personne", "Le même moniteur",
                  "Changer d'enseignant à chaque leçon fait perdre des heures. Chez nous, votre "
                  "moniteur vous suit du premier cours à l'examen.", ()),
            carte("euro", "Un budget annoncé",
                  "Le nombre d'heures conseillé et le coût des heures supplémentaires vous sont "
                  "donnés avant de signer, pas découverts en cours de route.", ()),
            carte("horloge", "Des créneaux tenus",
                  "Les plannings sont gérés à l'agence. Une leçon annulée par l'auto-école est "
                  "reprogrammée en priorité.", ()),
        )),
        section_texte("L'équipe", "Qui vous accompagne", """
    <div class="grille grille--3">
      <article class="carte">%s<h3>Direction</h3>
        <p>Accueil, montage des dossiers, suivi des places d'examen et relation avec la
        préfecture. <em>Nom et parcours à compléter par l'auto-école.</em></p></article>
      <article class="carte">%s<h3>Enseignant·e voiture</h3>
        <p>Titulaire du BEPECASER ou du titre professionnel ECSR.
        <em>Nom, ancienneté et spécialité à compléter.</em></p></article>
      <article class="carte">%s<h3>Enseignant·e moto</h3>
        <p>Mention deux-roues, plateau et circulation.
        <em>Nom, ancienneté et spécialité à compléter.</em></p></article>
    </div>
    <p class="mention" style="margin-top:1.5rem">Les portraits de l'équipe sont un levier de
    confiance sous-estimé&nbsp;: une page « qui sommes-nous » nourrie de vrais prénoms, de
    photos et d'ancienneté est aussi ce que les moteurs de réponse citent pour justifier une
    recommandation.</p>""" % (photo("portrait", "photo photo--large"),
                              photo("portrait", "photo photo--large"),
                              photo("portrait", "photo photo--large")), claire=True),
        section_texte("Informations légales", "L'essentiel à afficher", """
    <div class="grille grille--2">
      <ul class="liste-cochee">
        <li>%s<span>Agrément préfectoral n° E XX XXX XXXX 0 — à compléter</span></li>
        <li>%s<span>SAS immatriculée à Paris, SIREN 933 196 297</span></li>
        <li>%s<span>Établissement ouvert en 2024</span></li>
      </ul>
      <ul class="liste-cochee">
        <li>%s<span>Contrat de formation remis à l'inscription</span></li>
        <li>%s<span>Tarifs affichés en agence et sur ce site</span></li>
        <li>%s<span>Médiateur de la consommation — à préciser</span></li>
      </ul>
    </div>""" % ((g.coche(),) * 6)),
        g.appel_action(0, lien_secondaire=("auto-ecole-paris-12.html", "L'auto-école dans le quartier")),
    ])
    publier("a-propos.html",
            titre="L'auto-école — équipe et engagements | Auto Moto École Bizot",
            description="Auto Moto École Bizot, auto-école familiale du 12e arrondissement de "
                        "Paris : notre équipe, nos engagements et nos informations légales.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "L'auto-école")],
            schemas=[g.etablissement()])


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def contact():
    horaires = "".join(
        '<div style="display:flex;justify-content:space-between;gap:2rem;'
        'border-bottom:1px solid var(--trait);padding:.45rem 0">'
        '<dt>%s</dt><dd style="margin:0;font-weight:700">%s</dd></div>' % (j, h)
        for j, h in g.HORAIRES)
    corps = "".join([
        bandeau("Contact et inscription", "Prendre rendez-vous à l'auto-école",
                "Appelez-nous, passez à l'agence ou laissez votre numéro : nous vous rappelons "
                "sous 24 h ouvrées pour faire le point sur votre situation.", boutons=False),
        """
<section class="section">
  <div class="conteneur">
    <div class="grille grille--2" style="align-items:start;gap:3rem">
      <div>%s</div>
      <div class="pile">
        <h2>Coordonnées</h2>
        <p><strong>%s</strong><br>%s<br>%s %s</p>
        <p class="pile">
          <a class="bouton bouton--principal" href="tel:%s">%s</a>
        </p>
        <p><a href="mailto:%s">%s</a></p>
        <h3>Horaires d'ouverture</h3>
        <dl style="font-size:1rem;max-width:24rem">%s</dl>
        <h3>Venir à l'agence</h3>
        <ul class="liste-cochee">
          <li>%s<span>Métro Michel Bizot (ligne 8) — 3 minutes à pied</span></li>
          <li>%s<span>Métro Porte Dorée (ligne 8) — 7 minutes à pied</span></li>
          <li>%s<span>Bus 46 et 87, arrêt Général Michel Bizot</span></li>
          <li>%s<span>Stationnement payant dans l'avenue, gratuit le dimanche</span></li>
        </ul>
        <div class="plan"><span>Emplacement carte — plan Google Maps interactif,
        chargé après consentement aux cookies.</span></div>
      </div>
    </div>
  </div>
</section>""" % (
            formulaire("contact", "Demander un rappel gratuit",
                       "Renseignez vos coordonnées et la formation qui vous intéresse. "
                       "Nous vous rappelons sous 24 h ouvrées, sans engagement."),
            g.NOM, g.RUE, g.CODE_POSTAL, g.VILLE, g.TEL_LIEN, g.TEL_AFFICHE,
            g.COURRIEL, g.COURRIEL, horaires,
            g.coche(), g.coche(), g.coche(), g.coche()),
        section_texte("Inscription", "Ce qu'il faut apporter pour ouvrir un dossier", """
    <div class="grille grille--2">
      <ul class="liste-cochee">
        <li>%s<span>Une pièce d'identité en cours de validité</span></li>
        <li>%s<span>Un justificatif de domicile de moins de six mois</span></li>
        <li>%s<span>Une photo d'identité numérique (code ephoto)</span></li>
      </ul>
      <ul class="liste-cochee">
        <li>%s<span>L'attestation de recensement ou la JDC pour les moins de 25 ans</span></li>
        <li>%s<span>L'ASSR 2 ou l'ASR pour les candidats nés après 1987</span></li>
        <li>%s<span>Votre numéro NEPH si vous avez déjà été inscrit ailleurs</span></li>
      </ul>
    </div>""" % ((g.coche(),) * 6), claire=True),
    ])
    publier("contact.html",
            titre="Contact et inscription — auto-école Paris 12 | AME Bizot",
            description="Contactez l'auto-école Bizot, 113 avenue du Général Michel Bizot, "
                        "Paris 12e. Téléphone, horaires, plan d'accès et demande de rappel "
                        "gratuit sous 24 h.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Contact")],
            schemas=[g.etablissement(),
                     {"@context": "https://schema.org", "@type": "ContactPage",
                      "name": "Contact — " + g.NOM, "url": g.SITE + "/contact.html"}])


# ---------------------------------------------------------------------------
# Conseils (blog)
# ---------------------------------------------------------------------------
ARTICLES = [
    {
        "fichier": "blog/prix-permis-de-conduire-paris.html",
        "titre_page": "Prix du permis de conduire à Paris en 2026 : le budget réel",
        "titre": "Prix du permis de conduire à Paris en 2026 | AME Bizot",
        "description": "Combien coûte vraiment le permis à Paris ? Forfait, heures "
                       "supplémentaires, examens, aides : le détail poste par poste, avec les "
                       "montants pratiqués dans le 12e arrondissement.",
        "date": "2026-08-26",
        "date_affichee": "26 août 2026",
        "chapeau": "Un forfait à 990 € ne veut pas dire un permis à 990 €. Voici les postes "
                   "qui composent réellement la facture, ceux qui varient d'une auto-école à "
                   "l'autre, et les aides qui font baisser le total.",
        "lecture": "6 min",
    },
    {
        "fichier": "blog/permis-a2-moto-paris.html",
        "titre_page": "Permis A2 : déroulé, examens et budget de la formation moto",
        "titre": "Permis A2 à Paris — déroulé, examens et budget | AME Bizot",
        "description": "Permis moto A2 : conditions d'accès, plateau et circulation, nombre "
                       "d'heures, coût et passerelle vers le permis A. Le guide complet pour "
                       "les candidats parisiens.",
        "date": "2026-09-02",
        "date_affichee": "2 septembre 2026",
        "chapeau": "Le permis A2 ouvre l'accès aux motos jusqu'à 35 kW dès 18 ans. Entre le "
                   "plateau, la circulation et le code moto, voici comment se déroule "
                   "réellement la formation, et ce qu'elle coûte à Paris.",
        "lecture": "7 min",
    },
]

FAQ_ARTICLE_PRIX = [
    ("Combien coûte le permis de conduire à Paris en 2026 ?",
     "Comptez entre 1 200 et 1 800 € pour un permis B à Paris, en tenant compte d'un forfait "
     "de 20 heures autour de 990 € et d'une dizaine d'heures supplémentaires. Les aides "
     "publiques — jusqu'à 1 000 € pour la Région Île-de-France — peuvent réduire fortement "
     "cette somme."),
    ("Pourquoi le permis coûte-t-il plus cher à Paris qu'en province ?",
     "Le coût horaire des enseignants et des locaux y est plus élevé, et la circulation dense "
     "allonge souvent la formation de quelques heures. En contrepartie, un candidat formé à "
     "Paris conduit ensuite partout sans difficulté."),
    ("Combien d'heures de conduite faut-il en moyenne ?",
     "Le minimum légal est de 20 heures en boîte manuelle, mais la moyenne nationale se situe "
     "autour de 30 à 35 heures. C'est cette différence qu'il faut anticiper dans le budget."),
]

CORPS_ARTICLE_PRIX = """
<article class="section" style="padding-top:2.5rem">
  <div class="conteneur">
    <div class="article">
      <p class="article-meta">Conseils · %(date_affichee)s · %(lecture)s de lecture</p>
      <h1>Prix du permis de conduire à Paris en 2026 : le budget réel</h1>
      <p class="article__chapeau">%(chapeau)s</p>

      <h2>La réponse courte</h2>
      <p>À Paris, un permis B revient en moyenne entre <strong>1 200 et 1 800 €</strong> :
      un forfait de 20 heures autour de 990 €, auquel s'ajoutent une dizaine d'heures
      supplémentaires à 50-60 € et la redevance d'examen du code de 30 €. Les aides publiques
      peuvent en retirer jusqu'à 1 000 €.</p>

      <h2>Poste par poste</h2>
      %(tableau)s
      <p>Le forfait initial est le prix d'appel, pas le prix final. Deux auto-écoles affichant
      le même forfait peuvent aboutir à des factures très différentes selon le tarif de l'heure
      supplémentaire et les frais annexes.</p>

      <h2>Les trois questions à poser avant de signer</h2>
      <ol>
        <li><strong>Combien coûte l'heure supplémentaire&nbsp;?</strong> C'est le poste qui fait
        varier la facture finale, puisque la moyenne nationale dépasse 30 heures.</li>
        <li><strong>Que se passe-t-il en cas d'échec&nbsp;?</strong> Une nouvelle présentation
        est-elle facturée&nbsp;? À quel prix&nbsp;? Sous quel délai&nbsp;?</li>
        <li><strong>Quels frais restent à ma charge&nbsp;?</strong> Frais de dossier,
        accompagnement à l'examen, location du véhicule le jour J : tout doit figurer au
        contrat.</li>
      </ol>

      <div class="encadre">
        <p><strong>À retenir :</strong> depuis 2020, le contrat de formation doit détailler le
        contenu, la durée et le prix de chaque prestation. Une auto-école qui refuse de le
        remettre avant paiement est en tort.</p>
      </div>

      <h2>Les aides qui font baisser la note</h2>
      <ul>
        <li><strong>Région Île-de-France</strong> : jusqu'à 1 000 € pour les 18-25 ans, sous
        conditions de ressources et en contrepartie d'un engagement citoyen.</li>
        <li><strong>Permis à 1 € par jour</strong> : un prêt à taux zéro de 600 à 1 200 € pour
        les 15-25 ans, remboursé 30 € par mois.</li>
        <li><strong>Compte personnel de formation</strong> : mobilisable quand le permis sert
        un projet professionnel.</li>
        <li><strong>Apprentis</strong> : une aide forfaitaire de 500 € dès 18 ans, sans
        condition de ressources.</li>
      </ul>
      <p>Ces dispositifs se cumulent dans la limite du coût réel de la formation.
      <a href="../financement.html">Le détail des aides et la marche à suivre</a> sont
      expliqués sur notre page dédiée.</p>

      <h2>Faire baisser le coût sans rogner sur la formation</h2>
      <ul>
        <li><strong>La conduite accompagnée</strong> : plus chère au départ, elle réduit le
        nombre d'heures nécessaires et améliore nettement le taux de réussite.</li>
        <li><strong>La boîte automatique</strong> : 13 heures minimum au lieu de 20, avec une
        passerelle de 7 heures si vous voulez la boîte manuelle plus tard.</li>
        <li><strong>Réviser le code sérieusement</strong> : chaque échec à l'examen théorique
        coûte 30 € et repousse la conduite de plusieurs semaines.</li>
        <li><strong>Enchaîner les leçons</strong> : deux leçons par semaine valent mieux qu'une
        toutes les trois semaines — on ne réapprend pas ce qui est déjà acquis.</li>
      </ul>

      <div class="encadre">
        <p><strong>Chez Auto Moto École Bizot</strong>, le forfait 20 heures est affiché à
        990 € tout inclus et l'heure supplémentaire à 55 €, sans majoration.
        <a href="../tarifs.html">Voir la grille complète</a> ou
        <a href="../contact.html">demander un rappel gratuit</a>.</p>
      </div>
    </div>
  </div>
</article>
%(faq)s
%(appel)s
"""

FAQ_ARTICLE_A2 = [
    ("Combien d'heures faut-il pour le permis A2 ?",
     "La formation pratique minimale est de 20 heures : 8 heures de plateau hors circulation et "
     "12 heures en circulation. Beaucoup de candidats ajoutent quelques heures de plateau, "
     "l'épreuve de maniabilité étant la plus exigeante."),
    ("Faut-il repasser le code pour le permis moto ?",
     "Oui, sauf si vous avez obtenu une autre catégorie de permis depuis moins de cinq ans. "
     "L'épreuve théorique moto (ETM) est spécifique : elle porte sur l'équipement, la "
     "trajectoire de sécurité et la mécanique du deux-roues."),
    ("Quel budget prévoir pour le permis A2 à Paris ?",
     "Comptez environ 890 € pour un forfait de 20 heures tout inclus, auquel s'ajoutent les "
     "éventuelles heures supplémentaires — autour de 65 € — et l'équipement personnel."),
]

CORPS_ARTICLE_A2 = """
<article class="section" style="padding-top:2.5rem">
  <div class="conteneur">
    <div class="article">
      <p class="article-meta">Conseils · %(date_affichee)s · %(lecture)s de lecture</p>
      <h1>Permis A2 : déroulé, examens et budget de la formation moto</h1>
      <p class="article__chapeau">%(chapeau)s</p>

      <h2>La réponse courte</h2>
      <p>Le permis A2 s'obtient dès 18 ans, après une épreuve théorique moto et
      <strong>20 heures de formation pratique minimum</strong> — 8 heures de plateau,
      12 heures en circulation. Comptez environ 890 € pour un forfait complet à Paris, et
      deux ans avant de pouvoir passer au permis A par une formation de 7 heures.</p>

      <h2>Les conditions d'accès</h2>
      <ul>
        <li>Avoir 18 ans révolus le jour de l'examen.</li>
        <li>Avoir réussi l'épreuve théorique moto (ETM), valable cinq ans.</li>
        <li>Être apte médicalement — un contrôle est exigé dans certains cas seulement.</li>
      </ul>

      <h2>Le plateau, l'épreuve qui inquiète</h2>
      <p>L'épreuve hors circulation enchaîne quatre exercices : les vérifications et questions
      orales, le déplacement de la moto sans moteur, le parcours à allure lente, puis le
      parcours à allure normale avec évitement et freinage d'urgence.</p>
      <p>Elle se travaille par répétition. C'est la partie de la formation où le nombre
      d'heures varie le plus d'un candidat à l'autre : les réflexes d'équilibre et de regard
      ne s'acquièrent pas au même rythme pour tout le monde.</p>

      <h2>La circulation</h2>
      <p>Environ 40 minutes sur route, en liaison radio avec l'inspecteur qui suit en voiture.
      À Paris, l'épreuve porte surtout sur la trajectoire de sécurité, la gestion des angles
      morts et la cohabitation avec les bus, les taxis et les cyclistes.</p>

      <div class="encadre">
        <p><strong>Ce qui fait échouer le plus souvent :</strong> une trajectoire trop proche
        du bord droit, un regard fixé sur la roue avant plutôt que loin devant, et une
        insertion trop hésitante dans un flux dense.</p>
      </div>

      <h2>Le budget</h2>
      %(tableau)s

      <h2>Et après : la passerelle vers le permis A</h2>
      <p>Après deux ans de permis A2, une formation de 7 heures — 2 heures de théorie,
      2 heures de plateau, 3 heures en circulation — donne accès au permis A, sans limitation
      de puissance et sans examen final.</p>

      <div class="encadre">
        <p><strong>Chez Auto Moto École Bizot</strong>, la formation A2 est assurée par un
        enseignant moto dédié, avec prêt du casque et des gants pour les premières séances.
        <a href="../permis-moto.html">Voir la formation moto</a> ou
        <a href="../contact.html">prendre rendez-vous</a>.</p>
      </div>
    </div>
  </div>
</article>
%(faq)s
%(appel)s
"""


def article_schema(meta):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta["titre_page"],
        "description": meta["description"],
        "datePublished": meta["date"],
        "dateModified": meta["date"],
        "inLanguage": "fr-FR",
        "author": {"@type": "Organization", "name": g.NOM, "url": g.SITE + "/"},
        "publisher": {"@id": g.SITE + "/#etablissement"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": g.SITE + "/" + meta["fichier"]},
    }


def articles():
    prix = ARTICLES[0]
    corps_prix = CORPS_ARTICLE_PRIX % dict(
        prix,
        tableau=tableau("Budget type d'un permis B à Paris", ["Poste", "Montant courant"], [
            ["Forfait de base — 20 h de conduite, code inclus", "950 à 1 200 €"],
            ["Heures supplémentaires (10 h en moyenne)", "500 à 600 €"],
            ["Redevance d'examen du code", "30 €"],
            ["Frais de dossier et présentation à l'examen", "0 à 150 €"],
            ["Nouvelle présentation après un échec", "70 à 120 €"],
            ["Total constaté", "1 200 à 1 800 €"],
        ]),
        faq=faq_html(FAQ_ARTICLE_PRIX, "Le prix du permis : questions fréquentes"),
        appel=g.appel_action(1, lien_secondaire=("financement.html", "Les aides au financement")),
    )
    publier(prix["fichier"], titre=prix["titre"], description=prix["description"],
            corps=corps_prix, prof=1, page_nav="blog.html",
            fil=[("index.html", "Accueil"), ("blog.html", "Conseils"), (None, prix["titre_page"])],
            schemas=[article_schema(prix), g.faq_schema(FAQ_ARTICLE_PRIX)])

    a2 = ARTICLES[1]
    corps_a2 = CORPS_ARTICLE_A2 % dict(
        a2,
        tableau=tableau("Coût d'un permis A2 à Paris", ["Poste", "Montant courant"], [
            ["Forfait 20 h — plateau et circulation, code moto inclus", "850 à 1 100 €"],
            ["Heure de conduite supplémentaire", "60 à 70 €"],
            ["Redevance d'examen théorique moto", "30 €"],
            ["Équipement personnel (casque, gants, blouson, bottes)", "300 à 700 €"],
            ["Passerelle A2 vers A (7 h), deux ans plus tard", "300 à 400 €"],
        ]),
        faq=faq_html(FAQ_ARTICLE_A2, "Permis A2 : questions fréquentes"),
        appel=g.appel_action(1, lien_secondaire=("permis-moto.html", "La formation moto")),
    )
    publier(a2["fichier"], titre=a2["titre"], description=a2["description"],
            corps=corps_a2, prof=1, page_nav="blog.html",
            fil=[("index.html", "Accueil"), ("blog.html", "Conseils"), (None, a2["titre_page"])],
            schemas=[article_schema(a2), g.faq_schema(FAQ_ARTICLE_A2)])


def blog():
    cartes = "".join("""<article class="carte article-carte">
  <p class="article-meta">%s · %s de lecture</p>
  <h3><a href="%s">%s</a></h3>
  <p>%s</p>
  <p class="carte__pied"><a class="bouton bouton--secondaire bouton--large" href="%s">Lire l'article</a></p>
</article>""" % (a["date_affichee"], a["lecture"], a["fichier"], a["titre_page"],
                 a["chapeau"], a["fichier"]) for a in ARTICLES)

    a_venir = "".join('<li>%s<span>%s</span></li>' % (g.coche(), t) for t in [
        "Conduite accompagnée : ce que ça change vraiment sur le taux de réussite",
        "Passer son permis en boîte automatique à Paris : pour qui, à quel prix",
        "Délais d'examen en Île-de-France : comment ne pas perdre trois mois",
        "Rouler en scooter 125 avec le permis B : la formation de 7 heures",
    ])

    corps = "".join([
        bandeau("Conseils", "Comprendre le permis avant de s'inscrire",
                "Prix, délais, examens, aides : les articles qui répondent aux questions que "
                "se posent nos candidats — et que les moteurs de recherche nous posent aussi.",
                boutons=False),
        section_texte("Nos articles", "À lire en ce moment",
                      '<div class="grille grille--2">%s</div>' % cartes),
        section_texte("Calendrier éditorial", "Ce qui arrive ensuite", """
    <div class="grille grille--2">
      <div>
        <p>Deux articles par mois, choisis à partir des questions réellement tapées dans
        Google par les habitants du 12<sup>e</sup> arrondissement. C'est ce rythme qui fait
        remonter le site sur les recherches longues — et qui donne aux moteurs de réponse
        de quoi vous citer.</p>
        <ul class="liste-cochee">%s</ul>
      </div>
      %s
    </div>""" % (a_venir, photo("un moniteur et une élève devant l'agence", "photo photo--large")),
                      claire=True),
        g.appel_action(0),
    ])
    publier("blog.html",
            titre="Conseils permis de conduire — auto-école Paris 12 | AME Bizot",
            description="Prix du permis à Paris, permis A2, délais d'examen, aides au "
                        "financement : les conseils de l'auto-école Bizot, dans le 12e "
                        "arrondissement.",
            corps=corps,
            fil=[("index.html", "Accueil"), (None, "Conseils")],
            schemas=[g.etablissement(),
                     {"@context": "https://schema.org", "@type": "Blog",
                      "name": "Conseils — " + g.NOM, "url": g.SITE + "/blog.html",
                      "blogPost": [article_schema(a) for a in ARTICLES]}])


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------
def fichiers_techniques():
    urls = []
    for fichier in PAGES:
        chemin = "" if fichier == "index.html" else fichier
        priorite = "1.0" if fichier == "index.html" else "0.8"
        urls.append("  <url>\n    <loc>%s/%s</loc>\n    <changefreq>monthly</changefreq>"
                    "\n    <priority>%s</priority>\n  </url>" % (g.SITE, chemin, priorite))
    ecrire("sitemap.xml",
           '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    ecrire("robots.txt",
           "User-agent: *\nAllow: /\n\n"
           "# Moteurs de réponse : explicitement autorisés, c'est ce qui permet\n"
           "# au site d'être cité par ChatGPT, Perplexity ou Gemini.\n"
           "User-agent: GPTBot\nAllow: /\n\n"
           "User-agent: OAI-SearchBot\nAllow: /\n\n"
           "User-agent: PerplexityBot\nAllow: /\n\n"
           "User-agent: Google-Extended\nAllow: /\n\n"
           "Sitemap: %s/sitemap.xml\n" % g.SITE)


def main():
    accueil()
    permis_voiture()
    permis_moto()
    code_route()
    tarifs()
    financement()
    page_locale()
    a_propos()
    contact()
    blog()
    articles()
    fichiers_techniques()
    print("\n%d pages générées." % len(PAGES))


if __name__ == "__main__":
    main()
