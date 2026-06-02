% ============================================================================
% seri-report.cls  v3.1
% Schneider Electric — Sustainability Research Institute
% Compile with XeLaTeX — Typography matched to InDesign IDML
% ============================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{seri-report}[2026/03/17 SE SRI Report v3.2]
\LoadClass[a4paper, 9pt]{extarticle}

\RequirePackage[english]{babel}
\RequirePackage[top=22mm, bottom=15mm, left=10.5mm, right=10.5mm, headheight=14pt, headsep=0pt, footskip=10mm]{geometry}

% ---- FONTS (Brand 2026: Special Gothic + Special Gothic Expanded + Fira Sans) --
\RequirePackage{iftex}
\ifxetex
  \RequirePackage{fontspec}
  % Body: Special Gothic Regular — no italic in font family, use AutoFakeItalic
  \setmainfont{SpecialGothic-Regular}[Path=fonts/, Extension=.ttf,
    BoldFont=SpecialGothic-Bold,
    ItalicFont=SpecialGothic-Regular, ItalicFeatures={FakeSlant=0.15},
    BoldItalicFont=SpecialGothic-Bold, BoldItalicFeatures={FakeSlant=0.15}]
  \setsansfont{SpecialGothic-Regular}[Path=fonts/, Extension=.ttf,
    BoldFont=SpecialGothic-Bold,
    ItalicFont=SpecialGothic-Regular, ItalicFeatures={FakeSlant=0.15}]
  \renewcommand{\familydefault}{\sfdefault}
  % Display: Special Gothic Expanded (headlines, chapter titles, stats)
  \newfontfamily\displayfont{SpecialGothic_Expanded-Bold}[Path=fonts/, Extension=.ttf]
  \newfontfamily\displaylight{SpecialGothic_Expanded-Regular}[Path=fonts/, Extension=.ttf]
  \newfontfamily\displaymedium{SpecialGothic_Expanded-Medium}[Path=fonts/, Extension=.ttf]
  % Strong bold for subheadings
  \newfontfamily\strongbold{SpecialGothic-SemiBold}[Path=fonts/, Extension=.ttf]
  % Fira Sans for pullquotes, captions, supporting text
  \newfontfamily\seriffont{FiraSans-LightItalic}[Path=fonts/, Extension=.ttf]
  \newfontfamily\firasans{FiraSans-Regular}[Path=fonts/, Extension=.ttf,
    BoldFont=FiraSans-Bold, ItalicFont=FiraSans-Italic, BoldItalicFont=FiraSans-BoldItalic]
\else
  \RequirePackage[utf8]{inputenc}\RequirePackage[T1]{fontenc}
  \RequirePackage{helvet}\renewcommand{\familydefault}{\sfdefault}
  \let\displayfont\relax\let\displaylight\relax\let\displaymedium\relax
  \let\strongbold\bfseries\newcommand{\seriffont}{\rmfamily}
  \let\firasans\sffamily
  \newcommand{\addfontfeatures}[1]{}
\fi

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{bm}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween}
\RequirePackage{microtype}  % XeLaTeX: no expansion, no tracking — just basic kerning

% ---- NARROW-COLUMN TEXT FLOW (prevent huge inter-word gaps) ----------------
\tolerance=2000                    % allow slightly looser lines before forcing stretch
\emergencystretch=1.5em            % emergency extra stretch per line
\setlength{\parfillskip}{0pt plus 0.75\textwidth}  % allow short last lines
\hyphenpenalty=50                   % encourage hyphenation in narrow columns
\exhyphenpenalty=50
\doublehyphendemerits=5000         % but avoid 3+ consecutive hyphens
\RequirePackage[dvipsnames]{xcolor}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\usetikzlibrary{calc, positioning, backgrounds, shapes.geometric, arrows.meta, fadings}
\RequirePackage{tcolorbox}\tcbuselibrary{skins, breakable}
\RequirePackage{fancyhdr}\RequirePackage{titlesec}
\RequirePackage{hyperref}\RequirePackage{bookmark}
\RequirePackage{enumitem}\RequirePackage{tabularx}\RequirePackage{booktabs}
\RequirePackage{multicol}\RequirePackage{float}\RequirePackage{caption}
\RequirePackage{etoolbox}\RequirePackage{ragged2e}\RequirePackage{setspace}
\RequirePackage{parskip}\RequirePackage{eso-pic}\RequirePackage{xparse}
\RequirePackage{colortbl}\RequirePackage{array}
\RequirePackage[round, authoryear, sort&compress]{natbib}
\setlength{\bibsep}{2pt plus 1pt minus 1pt}\renewcommand{\bibfont}{\footnotesize}

% ---- COLORS (Brand 2026) ----------------------------------------------------
% Primary
\definecolor{SEGreen}{HTML}{3DCD58}        % Life Green — primary brand color
\definecolor{SEDarkGreen}{HTML}{0A2F24}    % Dark Green — depth, premium, overlays
\definecolor{SELogoGreen}{HTML}{009530}    % Logo Green — LOGO ON WHITE ONLY
% Supporting primary
\definecolor{SEElectricGreen}{HTML}{5EFF59}% Electric Green — highlights, CTA
\definecolor{SELightGreen}{HTML}{E7FFD9}   % Light Green — soft backgrounds
\definecolor{SELightGray}{HTML}{FAFAFA}    % Light Gray — neutral base
% Secondary (accents only — no full blocks)
\definecolor{SEYellow}{HTML}{FFCE00}
\definecolor{SECyan}{HTML}{24F0FF}
\definecolor{SEBlue}{HTML}{2040FF}
% Functional
\definecolor{SEBlack}{HTML}{1A1A1A}
\definecolor{SEBody}{HTML}{1A1A1A}         % Near-black for body text readability
\definecolor{SESubtitle}{HTML}{7F7F7F}
\definecolor{SEFooter}{HTML}{B3B3B3}
\definecolor{SEWhite}{HTML}{FFFFFF}
\definecolor{SETableStripe}{HTML}{FAFAFA}  % Matches Light Gray
% Legacy chart colors (kept for dataviz)
\definecolor{SEWarmGold}{HTML}{D4A843}
\definecolor{SERedAccent}{HTML}{FF0050}     % Vivid Red — charts, alerts
\definecolor{SEBlueAccent}{HTML}{3498DB}
\color{SEBody}

% ---- TEXT DEFAULTS (Brand 2026 layout) --------------------------------------
\setstretch{1.10}
\setlength{\parskip}{1.5pt plus 0.5pt}\setlength{\parindent}{0pt}
\setlength{\columnsep}{15pt}   % S/2 = 5.25mm ≈ 15pt per brand grid
\hypersetup{colorlinks=true, linkcolor=SEGreen, urlcolor=SEGreen, citecolor=SEGreen}

\captionsetup{font={footnotesize,sf}, labelfont={color=SEGreen}, labelsep=period,
  justification=raggedright, singlelinecheck=false, skip=6pt}
\renewcommand{\figurename}{Exhibit}

% ---- HEADERS & FOOTERS -------------------------------------------------------
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.3pt}
\renewcommand{\footrule}{\hbox to\headwidth{\color{SELightGray}\leaders\hrule height \footrulewidth\hfill}\vskip-\footrulewidth}
\fancyfoot[L]{\fontsize{7}{9}\selectfont\color{SEFooter}Schneider Electric Research Institute}
\fancyfoot[R]{\fontsize{7}{9}\selectfont\color{SEFooter}\textbf{\thepage}}

\fancypagestyle{chapterstart}{
  \fancyhf{}\renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{\fontsize{7}{9}\selectfont\color{SEFooter}Schneider Electric Research Institute}
  \fancyfoot[R]{\fontsize{7}{9}\selectfont\color{SEFooter}\textbf{\thepage}}}
\fancypagestyle{plain}{
  \fancyhf{}\renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{\fontsize{7}{9}\selectfont\color{SEFooter}Schneider Electric Research Institute}
  \fancyfoot[R]{\fontsize{7}{9}\selectfont\color{SEFooter}\textbf{\thepage}}}

% ---- RUNNING HEAD via eso-pic (bypasses fancyhdr entirely) ------------------
\newif\ifshowrunninghead\showrunningheadfalse
\newif\ifsuppressrunninghead\suppressrunningheadfalse
\newcommand{\enablerunninghead}{\global\showrunningheadtrue}
\newcommand{\suppressnextrunninghead}{\global\suppressrunningheadtrue}

% Pre-print watermark — ALWAYS visible, all pages, top right, red
\AddToShipoutPictureFG{%
  \AtPageUpperLeft{%
    \raisebox{-7mm}{\hspace{\dimexpr\paperwidth-10.5mm\relax}%
      \makebox[0pt][r]{\fontsize{7}{9}\selectfont\color{SERedAccent}%
        Pre Print Version --- No External Distribution Allowed}}}%
}

% Running head — conditional, top left, gray (suppressed on chapter/cover pages)
\AddToShipoutPictureFG{%
  \ifshowrunninghead
    \ifsuppressrunninghead\else
      \AtPageUpperLeft{%
        \raisebox{-7mm}{\hspace{10.5mm}%
          {\fontsize{7}{9}\selectfont\color{SESubtitle}\@runninghead}}}%
    \fi
  \fi
  \global\suppressrunningheadfalse  % reset for next page
}

% ---- SECTIONS (IDML: H1=32pt green, H2=20pt gray, H3=9pt green bold) -------
\titleformat{\section}{\displayfont\fontsize{32}{38}\selectfont\color{SEGreen}}{}{0pt}{}
\titleformat{\subsection}{\displayfont\fontsize{20}{30}\selectfont\color{SEGreen}}{}{0pt}{}
\titleformat{\subsubsection}{\strongbold\fontsize{9}{11}\selectfont\color{SEGreen}}{}{0pt}{}
\titlespacing*{\section}{0pt}{14pt}{6pt}
\titlespacing*{\subsection}{0pt}{8pt}{6pt}
\titlespacing*{\subsubsection}{0pt}{8pt}{3pt}

% ---- METADATA ---------------------------------------------------------------
\newcommand{\@doctitle}{}\newcommand{\@docsubtitle}{}
\newcommand{\@docdate}{}\newcommand{\@docauthors}{}
\newcommand{\@coverimage}{}\newcommand{\@runninghead}{}
\newcommand{\@partnerlabel}{}\newcommand{\@partnerlogo}{}
\newcommand{\doctitle}[1]{\renewcommand{\@doctitle}{#1}}
\newcommand{\docsubtitle}[1]{\renewcommand{\@docsubtitle}{#1}}
\newcommand{\docdate}[1]{\renewcommand{\@docdate}{#1}}
\newcommand{\docauthors}[1]{\renewcommand{\@docauthors}{#1}}
\newcommand{\coverimage}[1]{\renewcommand{\@coverimage}{#1}}
\newcommand{\runninghead}[1]{\renewcommand{\@runninghead}{#1}}
\newcommand{\partnerlabel}[1]{\renewcommand{\@partnerlabel}{#1}}
\newcommand{\partnerlogo}[1]{\renewcommand{\@partnerlogo}{#1}}

% =============================================================================
% COVER PAGE — FULL-BLEED IMAGE (Microgrids style)
% Image covers entire page. All text white, overlaid.
% SRI label top-left, title bottom-left. Brand 2026: Dark Green bg, oval, no Life Is On.
% =============================================================================
\newcommand{\makecover}{%
  \newgeometry{top=0mm, bottom=0mm, left=0mm, right=0mm}\thispagestyle{empty}
  \begin{tikzpicture}[remember picture, overlay]
    % Dark Green full-bleed background
    \fill[SEDarkGreen] (current page.south west) rectangle (current page.north east);
    % Cover image (oval visualization on dark green)
    \node[anchor=center, inner sep=0pt] at (current page.center) {%
      \includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio=false]{\@coverimage}};
    % Radial vignette — true transparent fade, no white
    \fill[black, opacity=0.6, path fading=circle with fuzzy edge 20 percent]
      ([shift={(2cm,3cm)}]current page.south west) circle (28cm);
    % SRI label (top-left)
    \node[anchor=north west, text width=0.5\paperwidth, inner sep=0pt]
      at ([shift={(20mm,-18mm)}]current page.north west) {%
        {\fontsize{13}{16}\selectfont\bfseries\color{white}%
         Schneider Electric\textsuperscript{TM}\\Research Institute\par}
        \ifdefempty{\@partnerlabel}{}{%
          \vspace{4mm}
          {\displaymedium\fontsize{14}{17}\selectfont\color{SEGreen}\@partnerlabel\par}}};
    % Partner logo (top-right)
    \ifdefempty{\@partnerlogo}{}{%
      \node[anchor=north east, inner sep=0pt]
        at ([shift={(-20mm,-18mm)}]current page.north east) {%
          \includegraphics[height=16mm]{\@partnerlogo}};
    }
    % SE logo (top-right, below partner logo if present)
    \node[anchor=north east, inner sep=0pt]
      at ([shift={(-20mm,-18mm)}]current page.north east) {%
        \includegraphics[height=14mm]{images/logo_se_white_screen.png}};
    % Title — lower third, on dark zone
    \node[anchor=west, text width=0.75\paperwidth, inner sep=0pt]
      at ([shift={(20mm,-50mm)}]current page.west) {%
        {\displayfont\fontsize{52}{56}\selectfont\spaceskip=0.18em plus 0.05em\hyphenpenalty=10000\exhyphenpenalty=10000\tolerance=9999\color{white}\@doctitle\par}};
    % Subtitle — below title
    \node[anchor=north west, text width=0.75\paperwidth, inner sep=0pt]
      at ([shift={(20mm,-85mm)}]current page.west) {%
        {\displaylight\fontsize{17}{21}\selectfont\hyphenpenalty=10000\color{SEGreen}\@docsubtitle\par}};
    % Authors (bottom-left, just above date)
    \node[anchor=south west, inner sep=0pt]
      at ([shift={(20mm,22mm)}]current page.south west) {%
        {\fontsize{12}{15}\selectfont\color{white!80}\@docauthors}};
    % Date (bottom-left, aligned with Advancing Energy Tech)
    \node[anchor=south west, inner sep=0pt]
      at ([shift={(20mm,12mm)}]current page.south west) {%
        {\fontsize{12}{15}\selectfont\color{white!60}\@docdate}};
  \end{tikzpicture}\restoregeometry\clearpage}

% ---- CHAPTER OPENER (IDML: 48pt/36pt white on image) ------------------------
\newcommand{\chapterpage}[3]{%
  \clearpage
  \suppressnextrunninghead
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, inner sep=0pt, minimum width=\paperwidth, minimum height=0.35\paperheight]
      at (current page.north) {\includegraphics[width=\paperwidth, height=0.35\paperheight, keepaspectratio=false]{#3}};
    \fill[black, opacity=0.4] (current page.north west) rectangle ([yshift=-0.35\paperheight]current page.north east);
    \node[anchor=north west, text width=0.7\paperwidth] at ([shift={(20mm,-20mm)}]current page.north west) {
      {\displayfont\fontsize{36}{40}\selectfont\color{white}#1\par}\vspace{2mm}
      {\displaylight\fontsize{24}{28}\selectfont\color{white!85}#2\par}};
  \end{tikzpicture}\vspace*{0.35\paperheight}\vspace{-10mm}}

% ---- FOREWORD PAGE (image header like TOC, name+affiliation below) ----------
\newcommand{\forewordpage}[5][]{%
  \clearpage\thispagestyle{plain}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, inner sep=0pt, minimum width=\paperwidth, minimum height=0.35\paperheight]
      at (current page.north) {\includegraphics[width=\paperwidth, height=0.35\paperheight, keepaspectratio=false]{#2}};
    \fill[black, opacity=0.3] (current page.north west) rectangle ([yshift=-0.35\paperheight]current page.north east);
    % "Foreword" — top-left of banner
    \node[anchor=north west, text width=0.6\paperwidth]
      at ([shift={(25mm,-18mm)}]current page.north west) {%
        {\displayfont\fontsize{28}{32}\selectfont\color{white}#3\par}};
    % Name + title — vertically centered in banner, left-aligned
    \node[anchor=west, text width=0.6\paperwidth]
      at ([shift={(25mm,-0.175\paperheight)}]current page.north west) {%
        {\displaymedium\fontsize{20}{24}\selectfont\color{white}#4\par}
        \vspace{2mm}
        {\fontsize{11}{14}\selectfont\color{white!80}#5\par}};
    % Logo — independent node, bottom-left of banner
    \ifx\relax#1\relax\else
      \node[anchor=south west]
        at ([shift={(25mm,-0.30\paperheight)}]current page.north west) {%
          \includegraphics[height=82pt]{#1}};
    \fi
  \end{tikzpicture}\vspace*{0.35\paperheight}\vspace{10mm}}

% Variante photo à gauche/centre — nom/titre au centre
\newcommand{\forewordpageright}[5][]{%
  \clearpage\thispagestyle{plain}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, inner sep=0pt, minimum width=\paperwidth, minimum height=0.35\paperheight]
      at (current page.north) {\includegraphics[width=\paperwidth, height=0.35\paperheight, keepaspectratio=false]{#2}};
    \fill[black, opacity=0.3] (current page.north west) rectangle ([yshift=-0.35\paperheight]current page.north east);
    % Label — top, starting at 50% page width
    \node[anchor=north west, text width=0.5\paperwidth, align=left]
      at ([shift={(0.5\paperwidth,-18mm)}]current page.north west) {%
        {\displayfont\fontsize{28}{32}\selectfont\color{white}#3\par}};
    % Name + title — same left anchor at 50%
    \node[anchor=west, text width=0.5\paperwidth, align=left]
      at ([shift={(0.5\paperwidth,-0.175\paperheight)}]current page.north west) {%
        {\displaymedium\fontsize{20}{24}\selectfont\color{white}#4\par}
        \vspace{2mm}
        {\fontsize{11}{14}\selectfont\color{white!80}#5\par}};
  \end{tikzpicture}\vspace*{0.35\paperheight}\vspace{10mm}}

% ---- FULL-BLEED / TOC / BACK COVER ------------------------------------------
\newcommand{\fullbleedpage}[3]{%
  \clearpage
  \suppressnextrunninghead
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=center, inner sep=0pt] at (current page.center) {
      \includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio=false]{#3}};
    \fill[black, opacity=0.45] (current page.south west) rectangle (current page.north east);
    \node[anchor=north west, text width=0.7\paperwidth] at ([shift={(25mm,-50mm)}]current page.north west) {
      {\displayfont\fontsize{42}{48}\selectfont\color{white}#1\par}\vspace{8mm}
      {\fontsize{9}{11}\selectfont\color{white!85}#2\par}};
  \end{tikzpicture}}

\newcommand{\backcover}{%
  \clearpage
  \suppressnextrunninghead
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture, overlay]
    % Full-bleed cover image (same as front page)
    \node[anchor=center, inner sep=0pt] at (current page.center) {%
      \includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio=false]{\@coverimage}};
    % Dark overlay
    \fill[black, opacity=0.55] (current page.south west) rectangle (current page.north east);
    % SRI label (centered upper third)
    \node[anchor=center, text width=0.7\paperwidth, align=center] at ([yshift=30mm]current page.center) {%
      {\displaymedium\fontsize{18}{22}\selectfont\color{SEGreen}Schneider Electric\textsuperscript{TM}\par}
      \vspace{3mm}
      {\displaylight\fontsize{14}{18}\selectfont\color{white!80}Research Institute\par}};
    % URL bottom
    \node[anchor=south, inner sep=0pt] at ([yshift=15mm]current page.south) {%
      {\fontsize{8}{10}\selectfont\color{white!60}www.se.com}};
  \end{tikzpicture}}

\newcommand{\tocpage}[1]{%
  \clearpage
  \suppressnextrunninghead
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north, inner sep=0pt, minimum width=\paperwidth, minimum height=0.4\paperheight]
      at (current page.north) {\includegraphics[width=\paperwidth, height=0.4\paperheight, keepaspectratio=false]{#1}};
    \fill[black, opacity=0.3] (current page.north west) rectangle ([yshift=-0.4\paperheight]current page.north east);
    \node[anchor=south east, text width=0.5\paperwidth, align=right]
      at ([shift={(-25mm,-0.4\paperheight+15mm)}]current page.north east) {
        {\displayfont\fontsize{42}{48}\selectfont\color{white}Table of\\Contents\par}};
  \end{tikzpicture}\vspace*{0.4\paperheight}\vspace{5mm}}

% ---- TWO-COLUMN + DATA TABLES + COMPONENTS ----------------------------------
\newenvironment{twocolbody}{\begin{multicols}{2}\tolerance=3000\emergencystretch=2em}{\end{multicols}}
\newcommand{\fullwidthbreak}{\end{multicols}\vspace{2mm}}
\newcommand{\resumetwocol}{\vspace{2mm}\begin{multicols}{2}}

\newcommand{\datatablesetup}{\rowcolors{2}{SETableStripe}{white}\fontsize{8}{10}\selectfont\renewcommand{\arraystretch}{1.25}}
\newcommand{\datatableheader}{\rowcolor{SEGreen}}
\newcommand{\datatableclear}{\rowcolors{1}{}{}\normalsize\renewcommand{\arraystretch}{1.0}}
\newcommand{\thd}[1]{\textbf{\color{white}#1}}

\newtcolorbox{pullquote}{enhanced, colback=SELightGreen!30, colframe=SEWhite, boxrule=0pt,
  borderline west={3pt}{0pt}{SEGreen}, left=10pt, right=6pt, top=4pt, bottom=4pt,
  fontupper=\firasans\fontsize{9.5}{12}\selectfont\itshape\color{SEBody}, sharp corners, breakable}

\newenvironment{statstrip}{\vspace{4mm}\noindent\begin{center}}{\end{center}\vspace{4mm}}
\newcommand{\statbox}[3][SEGreen]{%
  \begin{minipage}[t]{0.22\linewidth}\centering
    {\displayfont\fontsize{22}{26}\selectfont\color{#1}#2}\\[2mm]
    {\fontsize{7}{9}\selectfont\color{SESubtitle}#3}
  \end{minipage}\hfill}
\newcommand{\statcallout}[2]{%
  \begin{center}\begin{minipage}{0.85\linewidth}
    \begin{tcolorbox}[enhanced, colback=SELightGray, colframe=SELightGray,
      boxrule=0pt, sharp corners, halign=center, top=10pt, bottom=10pt]
    {\displayfont\fontsize{28}{34}\selectfont\color{SEGreen}#1\par}\vspace{3mm}
    {\fontsize{8}{10}\selectfont\color{SESubtitle}#2\par}
    \end{tcolorbox}\end{minipage}\end{center}}

\newtcolorbox{keyfindings}{enhanced, colback=SELightGray, colframe=SEGreen,
  coltitle=SEWhite, fonttitle=\bfseries, title=Key Findings,
  attach boxed title to top left={xshift=5mm, yshift=-3mm},
  boxed title style={colback=SEGreen, sharp corners},
  sharp corners, left=8pt, right=8pt, top=10pt, bottom=8pt,
  boxrule=0pt, borderline west={3pt}{0pt}{SEGreen}, breakable,
  fontupper=\fontsize{8}{11}\selectfont}

\newtcolorbox{highlightbox}[1][]{enhanced, colback=SEWhite, colframe=SEGreen,
  boxrule=1pt, sharp corners, left=8pt, right=8pt, top=6pt, bottom=6pt,
  fontupper=\fontsize{9}{11}\selectfont, #1}

\newcommand{\metriccard}[4][SEGreen]{%
  \begin{tcolorbox}[enhanced, colback=SEWhite, colframe=#1,
    boxrule=1.5pt, sharp corners, halign=center, top=6pt, bottom=6pt]
  \centering{\fontsize{7}{9}\selectfont\color{SESubtitle}#2\par}\vspace{2mm}
  {\displayfont\fontsize{18}{22}\selectfont\color{#1}#3\par}\vspace{1mm}
  {\fontsize{7}{9}\selectfont\color{SESubtitle}#4\par}\end{tcolorbox}}

% ---- UTILITIES ---------------------------------------------------------------
% Math operator used by appendix_climvar
\DeclareMathOperator{\CDF}{CDF}

\newcommand{\greensep}{\vspace{3pt}\noindent\textcolor{SEGreen}{\rule{35pt}{1.5pt}}\vspace{3pt}}
\newcommand{\exhibitcaption}[2]{{\fontsize{8}{10}\selectfont\color{SEGreen}Exhibit #1.\enspace\color{SEBody}#2\par}\vspace{2pt}}
\newcommand{\exhibitsource}[1]{\par\vspace{1pt}{\fontsize{7}{8}\selectfont\itshape\color{SESubtitle}#1}\par}
\newcommand{\sectionsubtitle}[1]{{\displaylight\fontsize{14}{18}\selectfont\color{SESubtitle}#1}\vspace{3mm}}
\renewcommand{\footnoterule}{\vspace{2pt}\noindent\textcolor{SELightGray}{\rule{0.3\textwidth}{0.3pt}}\vspace{2pt}}