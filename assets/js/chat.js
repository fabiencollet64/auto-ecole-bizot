/* Assistant de l'Auto Moto École Bizot.

   Volontairement sans intelligence artificielle : toutes les réponses sont
   écrites à l'avance et validées par l'auto-école. Un assistant branché sur un
   modèle de langage inventerait des tarifs, des délais ou des conditions
   d'aide — sur un site d'auto-école, une réponse fausse sur le prix d'un
   forfait est un litige. Ici, la saisie libre ne fait que chercher le sujet le
   plus proche parmi ceux ci-dessous ; quand rien ne correspond, l'assistant le
   dit et propose d'appeler.

   POUR MODIFIER LES RÉPONSES : tout est dans SUJETS, ci-dessous. */
(function () {
  "use strict";

  var TEL_AFFICHE = "01 45 85 22 14";
  var TEL_LIEN = "+33145852214";

  var ACCUEIL =
    "Bonjour ! Je réponds aux questions courantes sur les formations, les tarifs " +
    "et les aides. Sur quoi puis-je vous renseigner ?";

  var SUJETS = [
    {
      clef: "tarifs",
      titre: "Combien coûte le permis ?",
      mots: ["prix", "tarif", "cout", "coute", "combien", "cher", "budget", "euro", "€", "payer"],
      reponse:
        "<p>Le forfait <strong>permis B de 20 h est à 990 €</strong> tout inclus, en boîte " +
        "manuelle comme en boîte automatique. Le <strong>forfait moto A2 est à 890 €</strong>. " +
        "Le code, les frais de dossier et la présentation à l'examen sont compris.</p>" +
        "<p>L'heure supplémentaire est à 55 € en voiture, 65 € en moto — sans majoration.</p>" +
        "<p><a href=\"{p}tarifs.html\">Voir la grille complète</a></p>",
      suites: ["aides", "heures", "rappel"],
    },
    {
      clef: "aides",
      titre: "Quelles aides puis-je obtenir ?",
      mots: ["aide", "aides", "financement", "financer", "region", "cpf", "subvention",
             "1 euro", "un euro", "apprenti", "gratuit", "pole emploi", "france travail"],
      reponse:
        "<p>Selon votre situation : <strong>jusqu'à 1 000 € de la Région Île-de-France</strong> " +
        "pour les 18-25 ans, le <strong>permis à 1 € par jour</strong> (prêt à taux zéro pour les " +
        "15-25 ans), le <strong>CPF</strong> quand le permis sert un projet professionnel, et " +
        "<strong>500 € pour les apprentis</strong> majeurs.</p>" +
        "<p>Nous vérifions votre éligibilité au premier rendez-vous et montons le dossier avec vous.</p>" +
        "<p><a href=\"{p}financement.html\">Le détail des aides</a></p>",
      suites: ["tarifs", "inscription", "rappel"],
    },
    {
      clef: "voiture",
      titre: "La formation voiture",
      mots: ["voiture", "auto", "permis b", "conduire", "conduite", "accompagnee", "aac",
             "supervisee", "boite", "automatique", "manuelle"],
      reponse:
        "<p>Trois parcours : la <strong>formation classique</strong> (20 h minimum en boîte " +
        "manuelle, 13 h en boîte automatique), la <strong>conduite accompagnée dès 15 ans</strong> " +
        "et la <strong>formule accélérée</strong> quand votre planning le permet.</p>" +
        "<p>Après trois mois de permis boîte automatique, une passerelle de 7 h — sans examen — " +
        "donne accès à la boîte manuelle.</p>" +
        "<p><a href=\"{p}permis-voiture.html\">La formation voiture en détail</a></p>",
      suites: ["heures", "tarifs", "delais"],
    },
    {
      clef: "moto",
      titre: "La formation moto",
      mots: ["moto", "a1", "a2", "125", "scooter", "plateau", "circulation", "passerelle",
             "deux roues", "cylindree"],
      reponse:
        "<p><strong>Permis A1 dès 16 ans</strong>, <strong>A2 dès 18 ans</strong> — 20 h de " +
        "formation, 8 h de plateau et 12 h en circulation, casque et gants prêtés pour les " +
        "premières séances.</p>" +
        "<p>Avec deux ans de permis B, la <strong>formation 125 cm³ de 7 h (330 €)</strong> suffit, " +
        "sans examen. Et après deux ans de permis A2, la passerelle vers le permis A prend 7 h " +
        "elle aussi.</p>" +
        "<p><a href=\"{p}permis-moto.html\">La formation moto en détail</a></p>",
      suites: ["tarifs", "inscription", "rappel"],
    },
    {
      clef: "code",
      titre: "Le code de la route",
      mots: ["code", "theorique", "etg", "examen theorique", "salle", "reviser", "serie", "questions"],
      reponse:
        "<p>Cours en salle avec un enseignant <strong>et</strong> entraînement en ligne illimité " +
        "depuis chez vous. Nous inscrivons à l'examen dès que vos scores le permettent.</p>" +
        "<p>L'épreuve compte 40 questions : <strong>35 bonnes réponses</strong> sont exigées, soit " +
        "5 fautes au maximum. La redevance d'examen est de 30 €, le code reste valable 5 ans.</p>" +
        "<p><a href=\"{p}code-de-la-route.html\">La préparation au code</a></p>",
      suites: ["delais", "inscription", "tarifs"],
    },
    {
      clef: "heures",
      titre: "Combien d'heures faut-il ?",
      mots: ["heure", "heures", "nombre", "20h", "20 h", "supplementaire", "assez", "suffit"],
      reponse:
        "<p>Le minimum légal est de <strong>20 h en boîte manuelle</strong> et de 13 h en boîte " +
        "automatique. La moyenne nationale se situe plutôt <strong>entre 30 et 35 h</strong>.</p>" +
        "<p>Nous annonçons donc un forfait de 20 h au prix juste et une heure supplémentaire à " +
        "55 €, plutôt qu'un forfait gonflé. Votre moniteur vous prévient deux leçons à l'avance " +
        "s'il estime qu'il faudra prolonger.</p>",
      suites: ["tarifs", "delais", "rappel"],
    },
    {
      clef: "delais",
      titre: "En combien de temps ?",
      mots: ["delai", "delais", "temps", "duree", "rapidement", "vite", "accelere", "quand",
             "combien de temps", "mois"],
      reponse:
        "<p>Comptez <strong>trois à quatre mois</strong> entre l'inscription et l'examen pratique, " +
        "en tenant compte du code et de l'attribution d'une place d'examen.</p>" +
        "<p>Une <strong>formule accélérée</strong> permet de passer le permis en quelques semaines " +
        "si vous êtes disponible — sous réserve des places d'examen.</p>",
      suites: ["inscription", "tarifs", "rappel"],
    },
    {
      clef: "inscription",
      titre: "Comment s'inscrire ?",
      mots: ["inscrire", "inscription", "dossier", "papier", "papiers", "piece", "pieces",
             "document", "neph", "ants", "commencer", "demarrer"],
      reponse:
        "<p>Passez à l'agence pour un rendez-vous de vingt minutes : évaluation de départ offerte, " +
        "nombre d'heures conseillé et budget annoncé sans surprise.</p>" +
        "<p>À apporter : pièce d'identité, justificatif de domicile de moins de six mois, photo " +
        "d'identité numérique (code ephoto), attestation de recensement ou JDC pour les moins de " +
        "25 ans, ASSR 2 ou ASR si vous êtes né après 1987.</p>" +
        "<p><a href=\"{p}contact.html\">Prendre rendez-vous</a></p>",
      suites: ["horaires", "aides", "rappel"],
    },
    {
      clef: "horaires",
      titre: "Horaires et accès",
      mots: ["horaire", "horaires", "ouvert", "ouverture", "adresse", "acces", "venir", "metro",
             "ou etes", "situe", "samedi", "dimanche", "bus"],
      reponse:
        "<p><strong>113 avenue du Général Michel Bizot, 75012 Paris</strong> — métro Michel Bizot " +
        "(ligne 8) à 3 minutes à pied, Porte Dorée à 7 minutes, bus 46 et 87.</p>" +
        "<p>Ouvert du lundi au samedi : 10h–13h et 14h–18h du lundi au vendredi (16h le jeudi, " +
        "fermé l'après-midi le mercredi), 10h–13h le samedi.</p>" +
        "<p><a href=\"{p}contact.html\">Plan d'accès</a></p>",
      suites: ["inscription", "rappel"],
    },
  ];

  /* Le sujet « rappel » n'est pas une réponse mais un formulaire. */
  var RAPPEL = {
    clef: "rappel",
    titre: "Être rappelé",
    mots: ["rappel", "rappeler", "telephone", "appeler", "numero", "contact", "parler",
           "quelqu un", "humain", "conseiller"],
  };

  var INCOMPRIS =
    "<p>Je n'ai pas de réponse préparée à cette question — et je préfère vous le dire plutôt " +
    "que d'inventer.</p><p>L'auto-école y répondra mieux que moi : <a href=\"tel:" + TEL_LIEN +
    "\">" + TEL_AFFICHE + "</a>. Vous pouvez aussi choisir un sujet ci-dessous.</p>";

  var chat = document.querySelector("[data-chat]");
  if (!chat) return;

  var panneau = chat.querySelector("[data-chat-panneau]");
  var fil = chat.querySelector("[data-chat-fil]");
  var suggestions = chat.querySelector("[data-chat-suggestions]");
  var formulaire = chat.querySelector("[data-chat-form]");
  var champ = chat.querySelector("[data-chat-champ]");
  var lanceur = chat.querySelector("[data-chat-ouvrir]");
  var fermeture = chat.querySelector("[data-chat-fermer]");
  var prefixe = chat.getAttribute("data-prefixe") || "";
  var sansAnimation = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Utilitaires ------------------------------------------------------- */
  function normaliser(texte) {
    var minuscules = String(texte).toLowerCase();
    /* Sans accents : « délai » et « delai » doivent trouver le même sujet. */
    return minuscules.normalize
      ? minuscules.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      : minuscules;
  }

  function echapper(texte) {
    return String(texte).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function sujetParClef(clef) {
    for (var i = 0; i < SUJETS.length; i++) if (SUJETS[i].clef === clef) return SUJETS[i];
    return clef === RAPPEL.clef ? RAPPEL : null;
  }

  /* --- Affichage --------------------------------------------------------- */
  /* Le fil se remet en bas après chaque ajout — y compris après les
     suggestions, qui changent la hauteur du panneau et laissaient sinon la
     dernière réponse coupée. */
  function defiler() {
    window.requestAnimationFrame(function () {
      var derniere = fil.lastElementChild;
      /* Une réponse plus haute que le cadre se lit par le début : aller au bas
         du fil afficherait sa fin, et le visiteur croirait avoir manqué
         quelque chose. */
      if (derniere && derniere.offsetHeight > fil.clientHeight) {
        fil.scrollTop = Math.max(0, derniere.offsetTop - fil.offsetTop - 8);
      } else {
        fil.scrollTop = fil.scrollHeight;
      }
    });
  }

  function bulle(role, html) {
    var element = document.createElement("div");
    element.className = "chat__bulle chat__bulle--" + role;
    element.innerHTML = html.replace(/\{p\}/g, prefixe);
    fil.appendChild(element);
    defiler();
    return element;
  }

  function proposer(clefs) {
    suggestions.innerHTML = "";
    clefs.forEach(function (clef) {
      var sujet = sujetParClef(clef);
      if (!sujet) return;
      var bouton = document.createElement("button");
      bouton.type = "button";
      bouton.className = "chat__suggestion";
      bouton.textContent = sujet.titre;
      bouton.addEventListener("click", function () { demander(sujet.titre, sujet.clef); });
      suggestions.appendChild(bouton);
    });
    defiler();
  }

  function reflechir(action) {
    if (sansAnimation) { action(); return; }
    var attente = bulle("assistant", '<span class="chat__points"><i></i><i></i><i></i></span>');
    attente.classList.add("chat__bulle--attente");
    window.setTimeout(function () { attente.remove(); action(); }, 450);
  }

  /* --- Conversation ------------------------------------------------------ */
  function demander(libelle, clef) {
    bulle("visiteur", echapper(libelle));
    repondre(clef);
  }

  function repondre(clef) {
    if (clef === RAPPEL.clef) { reflechir(afficherRappel); return; }
    var sujet = sujetParClef(clef);
    reflechir(function () {
      if (sujet) {
        bulle("assistant", sujet.reponse);
        proposer(sujet.suites);
      } else {
        bulle("assistant", INCOMPRIS);
        proposer(["tarifs", "voiture", "moto", "rappel"]);
      }
    });
  }

  /* Recherche du sujet le plus proche : on compte les mots-clés présents dans
     la question, le sujet qui en réunit le plus l'emporte. Sans correspondance,
     l'assistant l'admet. */
  function chercher(question) {
    var texte = normaliser(question);
    var meilleur = null;
    var score = 0;
    SUJETS.concat([RAPPEL]).forEach(function (sujet) {
      var points = 0;
      sujet.mots.forEach(function (mot) { if (texte.indexOf(normaliser(mot)) !== -1) points++; });
      if (points > score) { score = points; meilleur = sujet; }
    });
    return score > 0 ? meilleur.clef : null;
  }

  function afficherRappel() {
    var identifiant = "chat-rappel-" + Date.now();
    var element = bulle("assistant",
      "<p>Laissez votre prénom et votre numéro : l'auto-école vous rappelle sous 24 h ouvrées.</p>" +
      '<form class="chat__rappel" data-chat-rappel novalidate>' +
      '<label for="' + identifiant + '-prenom">Prénom</label>' +
      '<input id="' + identifiant + '-prenom" name="prenom" type="text" autocomplete="given-name" required>' +
      '<label for="' + identifiant + '-tel">Téléphone</label>' +
      '<input id="' + identifiant + '-tel" name="telephone" type="tel" autocomplete="tel" required>' +
      '<button class="bouton bouton--principal bouton--large" type="submit">Être rappelé</button>' +
      "</form>" +
      '<p class="chat__mention">Ou appelez directement le <a href="tel:' + TEL_LIEN + '">' +
      TEL_AFFICHE + "</a>.</p>");

    element.querySelector("[data-chat-rappel]").addEventListener("submit", function (e) {
      e.preventDefault();
      var prenom = e.target.querySelector("[name=prenom]").value.trim();
      var tel = e.target.querySelector("[name=telephone]").value.trim();
      if (!prenom || !tel) {
        bulle("assistant", "<p>Il me manque votre prénom ou votre numéro pour transmettre la demande.</p>");
        return;
      }
      e.target.remove();
      bulle("visiteur", echapper(prenom + " — " + tel));
      reflechir(function () {
        bulle("assistant",
          "<p><strong>C'est noté, " + echapper(prenom) + ".</strong> Sur le site en production, " +
          "l'auto-école recevrait cette demande par courriel et vous rappellerait sous 24 h " +
          "ouvrées.</p><p class=\"chat__mention\">Ceci est une maquette : aucune donnée n'est envoyée.</p>");
        proposer(["tarifs", "inscription", "horaires"]);
      });
    });
    suggestions.innerHTML = "";
  }

  /* --- Ouverture et fermeture -------------------------------------------- */
  var demarree = false;

  function ouvrir() {
    chat.setAttribute("data-ouvert", "true");
    lanceur.setAttribute("aria-expanded", "true");
    if (!demarree) {
      demarree = true;
      bulle("assistant", "<p>" + ACCUEIL + "</p>");
      proposer(["tarifs", "voiture", "moto", "aides", "inscription", "horaires"]);
    }
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { champ.focus(); });
    });
  }

  function fermer() {
    chat.removeAttribute("data-ouvert");
    lanceur.setAttribute("aria-expanded", "false");
    lanceur.focus();
  }

  lanceur.addEventListener("click", function () {
    if (chat.getAttribute("data-ouvert") === "true") fermer(); else ouvrir();
  });
  fermeture.addEventListener("click", fermer);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && chat.getAttribute("data-ouvert") === "true") fermer();
  });

  formulaire.addEventListener("submit", function (e) {
    e.preventDefault();
    var question = champ.value.trim();
    if (!question) return;
    champ.value = "";
    bulle("visiteur", echapper(question));
    repondre(chercher(question));
  });

  /* Le panneau ne doit pas rester ouvert derrière le tiroir de navigation. */
  var boutonTiroir = document.querySelector("[data-tiroir-ouvrir]");
  if (boutonTiroir) boutonTiroir.addEventListener("click", function () {
    if (chat.getAttribute("data-ouvert") === "true") chat.removeAttribute("data-ouvert");
  });
})();
