# Maquette — Auto Moto École Bizot

Site vitrine proposé par **Collet Marketing** à l'auto-école
**Auto Moto École Bizot**, 113 avenue du Général Michel Bizot, 75012 Paris,
à la suite de l'audit de présence en ligne (`audit_auto_moto_ecole_bizot.pptx`).

HTML et CSS statiques, sans dépendance ni étape de compilation : le site peut
être hébergé tel quel (OVH, Netlify, GitHub Pages…) ou porté dans un thème
existant.

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```

## Ce que la maquette répond, point par point

L'audit relevait quatre faiblesses côté site. Voici où chacune est traitée.

| Constat de l'audit | Réponse dans la maquette |
|---|---|
| « Contenu textuel répétitif, peu structuré » | Une page par intention de recherche (permis B, moto, code, tarifs, financement, local), un seul `h1` par page, titres hiérarchisés, aucun paragraphe recopié d'une page à l'autre. |
| « Pas de blog ni contenu éditorial » | `blog.html` et deux articles complets, plus un calendrier éditorial visible qui montre le rythme proposé (deux articles par mois). |
| « Absent des réponses ChatGPT et des IA » | Réponses courtes et autonomes en tête de page et en FAQ, balisage `FAQPage` et `Article`, `robots.txt` autorisant explicitement GPTBot, OAI-SearchBot, PerplexityBot et Google-Extended. |
| « Pas de prise de contact ou réservation en ligne » | Formulaire de rappel sur la page d'accueil et page `contact.html` dédiée, téléphone cliquable dans l'en-tête de toutes les pages, liste des pièces à apporter pour ouvrir un dossier. |

Le référencement local (« auto-école Paris 12 ») s'appuie sur trois leviers :

- **NAP identique partout** — nom, adresse, téléphone et horaires viennent d'une
  seule source (`outils/gabarits.py`) et sont repris à l'identique dans le pied
  de page et dans le balisage Schema.org. Un écart entre le site et la fiche
  Google Business Profile coûte des positions.
- **Balisage `DrivingSchool` / `LocalBusiness`** sur chaque page, avec adresse,
  coordonnées géographiques, horaires, zone desservie et catalogue d'offres.
- **Une page locale dédiée** (`auto-ecole-paris-12.html`) : quartiers desservis,
  points de conduite du 12<sup>e</sup> travaillés en leçon, questions locales.

## Arborescence

```
index.html                       Accueil
permis-voiture.html              Permis B — classique, AAC, accéléré
permis-moto.html                 Permis A1, A2, 125 cm³, passerelle A2 → A
code-de-la-route.html            Code en salle et en ligne
tarifs.html                      Grille tarifaire complète
financement.html                 Aides : Région, permis à 1 €, CPF, apprentis
auto-ecole-paris-12.html         Page locale « auto-école Paris 12 »
a-propos.html                    L'équipe, les engagements, les mentions
contact.html                     Coordonnées, horaires, accès, formulaire
blog.html                        Liste des articles et calendrier éditorial
blog/prix-permis-de-conduire-paris.html
blog/permis-a2-moto-paris.html
sitemap.xml, robots.txt          GÉNÉRÉS
maquette-complete.html           GÉNÉRÉ — les 12 pages en un fichier unique
assets/css/bizot.css             Feuille de style unique
assets/js/site.js                Menu en petit écran, retour des formulaires
outils/gabarits.py               En-tête, pied, coordonnées, données structurées
outils/generer.py                Contenu des pages et génération
outils/verifier.py               Contrôles avant mise en ligne
outils/maquette-unique.py        Assemblage du fichier unique
```

## Modifier le site

Les pages HTML sont **générées** : ne les éditez pas à la main, elles seront
écrasées.

```bash
python3 outils/generer.py          # les 12 pages, sitemap.xml, robots.txt
python3 outils/verifier.py         # contrôles — doit finir sans erreur
python3 outils/maquette-unique.py  # le fichier unique de démonstration
```

- **Coordonnées, horaires, tarifs du balisage** : `outils/gabarits.py`, en tête
  de fichier. Ils se propagent partout, y compris dans le Schema.org.
- **Contenu d'une page** : la fonction correspondante dans `outils/generer.py`.
- **Couleurs, tailles, espacements** : uniquement le bloc « jetons » en tête de
  `assets/css/bizot.css`. Aucune couleur n'est écrite en dur ailleurs.

`outils/verifier.py` échoue si une page perd son `h1` unique, sa description,
son URL canonique, ses données structurées, son lien d'évitement ou son
téléphone, si un lien interne pointe dans le vide, ou si un titre dépasse la
longueur affichée par Google.

## Charte visuelle

La palette est relevée sur l'enseigne et le logo de l'auto-école, pour que le
site prolonge ce que le passant voit avenue du Général Michel Bizot :

| Jeton | Valeur | Origine et usage |
|---|---|---|
| `--bleu` | `#123fa8` | Le bleu de la devanture — couleur de marque, aplats, liens (7,4:1 sur blanc) |
| `--bleu-nuit` | `#0a2468` | Version profonde — en-tête, héros, pied de page |
| `--rouge` | `#c81d2b` | Les anneaux du logotype — bouton principal, jamais du texte courant (blanc sur rouge : 5,9:1) |
| `--turquoise` | `#0e727f` | Le mur d'accueil de l'agence — badges et accents sur fond clair |
| `--turquoise-vif` | `#57d2e0` | Le même, éclairci pour rester lisible sur le bleu nuit (8,9:1) |
| `--gris` | `#f1f4fa` | Fonds de section, neutre légèrement bleuté |
| `--encre` | `#14181c` | Le noir du logotype — texte courant (15,8:1 sur blanc) |

Le logotype de l'en-tête reprend celui de l'enseigne : le mot AUTOMOTO dont les
O sont des anneaux rouges, encadré de la voiture et de la moto. Il est
reconstitué en HTML et en CSS — les anneaux sont des bordures, pas des images,
donc nets à toute échelle et sans requête réseau. **Dès que l'auto-école
fournit son fichier officiel**, déposez-le en `assets/img/logo-bizot.svg` : il
remplace automatiquement la reconstitution sur toutes les pages (le chemin est
réglé par `LOGO_FICHIER` dans `outils/gabarits.py`).

Corps de texte à 18 px minimum, zones cliquables de 48 px, navigation
utilisable au clavier, lien d'évitement sur chaque page.

## Contenu à valider avant mise en ligne

Le contenu rédactionnel est un contenu d'amorçage, rédigé à partir des
informations publiques disponibles en ligne. Il doit être relu et corrigé par
l'auto-école. En particulier :

- **Les tarifs** (990 € le forfait 20 h, 890 € le forfait A2, 55 € l'heure
  supplémentaire, 330 € la formation 125 cm³…) : à remplacer par la grille
  officielle. L'affichage des prix est une obligation légale.
- **L'agrément préfectoral**, le numéro de médiateur de la consommation et les
  mentions légales, laissés en `XX` dans le pied de page et sur `a-propos.html`.
- **Les prénoms, portraits et ancienneté de l'équipe** sur `a-propos.html`.
- **Les avis** de la page d'accueil, qui sont des textes d'illustration
  explicitement signalés comme tels : à remplacer par un module connecté à la
  fiche Google Business Profile.
- **Les coordonnées géographiques** du balisage Schema.org, à relever sur la
  fiche Google Business Profile.
- **Le courriel de contact**, à confirmer.
- **Les photographies** : neuf emplacements sont réservés dans les pages, avec
  la description de la photo attendue. Aucune image d'illustration générique
  n'a été mise à la place — sur un site local, une vraie photo de la devanture,
  des véhicules et de l'équipe pèse davantage qu'un visuel de banque d'images.
- **Le bandeau « maquette de démonstration »** en haut de chaque page, à retirer
  au moment de la mise en ligne (`outils/gabarits.py`, fonction
  `bandeau_maquette`).

## À prévoir pour la mise en ligne

- Formulaires : la maquette n'envoie rien, elle confirme à l'écran. Prévoir un
  service d'envoi (Formspree, un script PHP ou l'API de l'hébergeur) et une
  page de confirmation.
- Bandeau de consentement avant le chargement de la carte Google Maps.
- Mentions légales, politique de confidentialité et conditions de vente.
- Déclaration du site dans Google Search Console, dépôt du `sitemap.xml`.
- Mise à jour de la fiche Google Business Profile avec exactement les mêmes
  nom, adresse, téléphone et horaires que ceux du pied de page.
