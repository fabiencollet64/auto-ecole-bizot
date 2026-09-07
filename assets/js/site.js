/* Maquette Auto Moto École Bizot — comportements d'interface.
   Le site fonctionne sans JavaScript : le menu est visible au clavier, les
   questions fréquentes sont des <details>, et les formulaires sont de vrais
   formulaires. Ce fichier n'ajoute que le confort. */
(function () {
  "use strict";

  /* Menu en petit écran ---------------------------------------------------- */
  var bouton = document.querySelector("[data-menu-bouton]");
  var nav = document.querySelector("[data-menu]");

  if (bouton && nav) {
    bouton.addEventListener("click", function () {
      var ouvert = nav.getAttribute("data-ouvert") === "true";
      nav.setAttribute("data-ouvert", String(!ouvert));
      bouton.setAttribute("aria-expanded", String(!ouvert));
    });

    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.setAttribute("data-ouvert", "false");
        bouton.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.getAttribute("data-ouvert") === "true") {
        nav.setAttribute("data-ouvert", "false");
        bouton.setAttribute("aria-expanded", "false");
        bouton.focus();
      }
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
