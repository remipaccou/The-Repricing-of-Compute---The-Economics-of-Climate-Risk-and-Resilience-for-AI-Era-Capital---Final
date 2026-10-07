# Couverture SERI Digital Research — The Repricing of Compute

La couverture reprend la composition standard de `template_SERI` :
Signatures inversées, ligne horizontale continue et ligne verticale blanche
dégradée, symbole du domaine en haut à droite et logo officiel en bas à droite.

Ce papier relève du **domaine 4 — Digitalization and systemic change**.
Le choix est défini par `domain=systemic-change` dans `frontpage.tex`.

Le titre, le sous-titre, les auteurs et la date d'origine sont conservés :
**The Repricing of Compute**, **The Economics of Climate Risk and Resilience
for AI-Era Capital**, **Rémi Paccou & Thomas Epelbaum**, **June 2026**.

L'image reste `images/Front_Page.jpeg`, avec le même placement pleine page
que dans la couverture d'origine. Aucun recadrage n'est appliqué et le fichier
image n'est pas modifié. L'assombrissement est noir et transparent, sans filtre vert.

La bibliothèque `seri-digital-cover.sty` et les ressources `seri-digital-assets/`
sont fournies dans ce projet. Les quatre symboles sont inclus en PDF et SVG,
même si ce papier utilise uniquement le quatrième.

Compiler `main.tex` avec **XeLaTeX**. La classe du rapport et les fichiers du
corps de l'article restent ceux du projet existant. L'aperçu de couverture
est enregistré dans `digital-research-cover.pdf`.

Les options `table,dvipsnames` de `xcolor` sont transmises avant le chargement
de la classe pour éviter un conflit de chargement avec TikZ.
