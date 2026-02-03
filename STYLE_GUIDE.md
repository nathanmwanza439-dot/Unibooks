Palette UniBooks

Couleurs principales (variables CSS) :

- --cta: #D32F2F — Rouge vif. Usage : boutons principaux, alertes critiques, CTAs importants.
- --cta-600: #B71C1C — Variante foncée du CTA (hover / active).
- --interactive: #FBC02D — Jaune soleil. Usage : icônes interactives, accents au survol, informations non-primaires.
- --primary: #1976D2 — Bleu profond. Usage : barres de navigation, titres, fonds structurants.
- --primary-600: #1565C0 — Variante foncée du bleu primaire.
- --light-blue: #64B5F6 — Bleu clair. Usage : cartes, encadrés, effets hover doux.
- --notify: #FFA726 — Orange doux. Usage : badges, pastilles de notification, actions dynamiques.
- --surface: #FFFFFF — Surface principale (fonds de cartes, boutons secondaires).
- --bg: #f4f6f9 — Fond de page (neutre clair).
- --text: #0b1a2b — Texte principal (suffisamment sombre pour le contraste).

Règles d'utilisation

1. Hiérarchie visuelle
   - Les éléments structurants (header, titres) utilisent `--primary` pour stabilité et confiance.
   - Les actions importantes (envoi, confirmation, prise de décision) utilisent `--cta` (rouge) pour attirer l'œil.
   - Les éléments secondaires ou interactifs (icônes, hints) utilisent `--interactive` (jaune) pour la chaleur et la vivacité.
   - Les cartes et encadrés utilisent `--light-blue` en fond léger pour contraste doux.
   - Les badges/notifications utilisent `--notify` pour une couleur chaude et distincte.

2. Boutons
   - `.ub-btn--primary` : fond `linear-gradient(90deg,var(--cta),var(--cta-600))`, texte blanc.
   - Boutons secondaires : utiliser `var(--surface)` ou `transparent` avec bord `var(--border)` et texte `var(--text)`.
   - Survols : assombrir la teinte (utiliser `--cta-600` ou `--primary-600`).

3. Contraste & accessibilité
   - Conserver un contraste AA minimum pour textes sur fonds colorés. Les boutons CTA utilisent texte blanc sur fond rouge — vérifie contraste sur boutons petits.
   - Pour les icônes jaunes (`--interactive`) sur fond clair, préférer un contour ou un fond semi-opaque pour améliorer le contraste.

4. Composants à normaliser
   - Header / sidebar : fonds `--primary` avec texte blanc.
   - Cards : fond `--surface` ou `linear-gradient(var(--surface), var(--bg))`, bord léger `--border`.
   - Toasters :
     - info → `linear-gradient(90deg,var(--primary),var(--primary-600))`
     - success → `linear-gradient(90deg,var(--light-blue), rgba(100,181,246,0.6))`
     - error → `linear-gradient(90deg,var(--cta),var(--cta-600))`

5. Mobile
   - Garder des paddings généreux (8–12px) et boutons full-width pour confort tactile.
   - Eviter d'utiliser uniquement `--interactive` (jaune) pour texte important (contraste faible) — préférer icônes ou fonds contrastés.

Prochaines étapes recommandées

- Auditer automatiquement les contrastes (WCAG AA/AAA) et corriger les contre-exemples.
- Remplacer les dernières couleurs "hard-coded" restantes par des variables si besoin.
- Fournir un fichier SCSS partiel (variables + mixins) si tu veux une maintenance plus simple.

Si tu veux, je peux lancer l'audit contraste maintenant (générer un rapport liste/valide), ou appliquer la palette à d'autres fichiers CSS/templates restants. Dis-moi la priorité.