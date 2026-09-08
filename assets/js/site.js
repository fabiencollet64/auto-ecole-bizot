/* Maquette Auto Moto École Bizot — comportements d'interface.
   Le site fonctionne sans JavaScript : les liens du tiroir sont de vrais
   liens, les questions fréquentes des <details>, les formulaires de vrais
   formulaires. Ce fichier n'ajoute que le confort — et le confort, ici, tient
   surtout à ce que le clavier et les lecteurs d'écran suivent. */
(function () {
  "use strict";

  var FOCALISABLES = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';

  /* Tiroir de navigation ---------------------------------------------------- */
  var tiroir = document.querySelector("[data-tiroir]");
  var voile = document.querySelector("[data-voile]");
  var ouvrir = document.querySelector("[data-tiroir-ouvrir]");
  var fermer = document.querySelector("[data-tiroir-fermer]");

  if (tiroir && voile && ouvrir && fermer) {
    var declencheur = null;

    var ouvrirTiroir = function () {
      declencheur = document.activeElement;
      tiroir.setAttribute("data-ouvert", "true");
      voile.setAttribute("data-ouvert", "true");
      ouvrir.setAttribute("aria-expanded", "true");
      document.body.classList.add("tiroir-ouvert");
      // Le tiroir passe de visibility:hidden à visible : tant que ce style
      // n'est pas appliqué, le bouton refuse le focus — l'appeler tout de
      // suite laisse le clavier sur le bouton « Menu », derrière le voile.
      // Deux images d'attente suffisent, le style est alors recalculé.
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { fermer.focus(); });
      });
    };

    var fermerTiroir = function () {
      tiroir.removeAttribute("data-ouvert");
      voile.removeAttribute("data-ouvert");
      ouvrir.setAttribute("aria-expanded", "false");
      document.body.classList.remove("tiroir-ouvert");
      if (declencheur && document.contains(declencheur)) declencheur.focus();
    };

    var estOuvert = function () { return tiroir.getAttribute("data-ouvert") === "true"; };

    ouvrir.addEventListener("click", ouvrirTiroir);
    fermer.addEventListener("click", fermerTiroir);
    voile.addEventListener("click", fermerTiroir);

    tiroir.addEventListener("click", function (e) {
      if (e.target.closest("a")) fermerTiroir();
    });

    /* Tant que le tiroir est ouvert, la tabulation y reste enfermée : sinon le
       clavier part se promener dans la page masquée derrière le voile. */
    document.addEventListener("keydown", function (e) {
      if (!estOuvert()) return;
      if (e.key === "Escape") { fermerTiroir(); return; }
      if (e.key !== "Tab") return;
      var cibles = tiroir.querySelectorAll(FOCALISABLES);
      if (!cibles.length) return;
      var premier = cibles[0];
      var dernier = cibles[cibles.length - 1];
      if (e.shiftKey && document.activeElement === premier) {
        e.preventDefault();
        dernier.focus();
      } else if (!e.shiftKey && document.activeElement === dernier) {
        e.preventDefault();
        premier.focus();
      }
    });

    /* Repassé en grand écran, le tiroir n'a plus lieu d'être. */
    if (window.matchMedia) {
      var large = window.matchMedia("(min-width: 80.0625rem)");
      var surveiller = function (m) { if (m.matches && estOuvert()) fermerTiroir(); };
      if (large.addEventListener) large.addEventListener("change", surveiller);
      else if (large.addListener) large.addListener(surveiller);
    }
  }

  /* Déroulant « Formations » de la barre ------------------------------------ */
  var groupe = document.querySelector("[data-groupe]");
  var groupeBouton = document.querySelector("[data-groupe-bouton]");

  if (groupe && groupeBouton) {
    var basculer = function (ouvert) {
      groupe.setAttribute("data-ouvert", String(ouvert));
      groupeBouton.setAttribute("aria-expanded", String(ouvert));
    };

    groupeBouton.addEventListener("click", function () {
      basculer(groupe.getAttribute("data-ouvert") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && groupe.getAttribute("data-ouvert") === "true") {
        basculer(false);
        groupeBouton.focus();
      }
    });

    document.addEventListener("click", function (e) {
      if (!groupe.contains(e.target)) basculer(false);
    });

    groupe.addEventListener("focusout", function (e) {
      if (!groupe.contains(e.relatedTarget)) basculer(false);
    });
  }

  /* Formulaires de démonstration ------------------------------------------
     Aucun envoi réel : la maquette n'a pas de serveur. On confirme à l'écran
     ce que ferait le site en production (courriel à l'auto-école + accusé de
     réception au candidat), et on annonce le message aux lecteurs d'écran. */
  Array.prototype.forEach.call(
    document.querySelectorAll("form[data-demo]"),
    function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var retour = form.querySelector("[data-retour]");
        if (!retour) return;
        var prenom = (form.querySelector("[name=prenom]") || {}).value || "";
        retour.innerHTML =
          "<strong>Demande enregistrée" + (prenom ? ", " + escapeHtml(prenom) : "") + ".</strong> " +
          "Sur le site en production, l'auto-école reçoit cette demande par courriel " +
          "et vous rappelle sous 24 h ouvrées. Ceci est une maquette&nbsp;: aucune donnée n'est envoyée.";
        retour.hidden = false;
        retour.setAttribute("tabindex", "-1");
        retour.focus();
      });
    }
  );

  function escapeHtml(t) {
    return String(t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
})();
