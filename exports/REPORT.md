# Byblos corpus audit

Snapshot version: 0.5.0
Scientific 1.0 ready: **False**

Structural validity is not proof of accuracy or exhaustive coverage.

| Count | Value |
|---|---:|
| catalogue records | 38 |
| reported core | 14 |
| disputed candidates | 24 |
| sources and leads | 36 |
| surfaces described | 6 |
| signs registered | 0 |
| transcriptions | 0 |
| verified core sequences | 0 |
| independent approvals | 0 |
| external entries | 43 |

| Gate | Result |
|---|---|
| structure | PASS |
| nonempty core | PASS |
| core sequences | OPEN |
| independent core review | OPEN |
| object identity | OPEN |
| surface inventory | OPEN |
| external crosswalk | OPEN |
| research gaps resolved | OPEN |
| exhaustiveness audit | OPEN |

## Open research gaps

- **GAP-COUNT**: Reconcile 14 entries with 15 reported inscriptions using object, surface and edition crosswalks.
- **GAP-FRAGMENTS**: Identify the 28 proposed fragments individually, their sources, and membership arguments; do not assume they are disjoint from other counts.
- **GAP-DIGITAL**: OCBI located; reconcile provider units and metadata crosswalk, obtain explicit transcription rights and encoding map, inspect edition provenance.
- **GAP-EDITIONS**: Acquire and inspect original editions; resolve exact bibliography and plates.
- **GAP-BIBLIOGRAPHY**: Build a systematic bibliographic search log including later additions, reviews and opposing interpretations.
- **GAP-REVIEW**: Arrange independent specialist review; none performed.
- **GAP-OCBI**: Map all 43 rendered entries to objects, faces, readings and inscription identities; distinguish provider certainty from our assessment.
- **GAP-RIGHTS**: Record explicit permission or licence for every proposed redistributed sequence, image or plate.
- **GAP-SIGNS**: Collate published sign lists and tokens; do not instantiate unseen signs from reported inventory sizes.
- **GAP-TRANSCRIPTION**: Prepare rights-supported sign sequences for each in-scope inscription with uncertainties and independent checks.
- **GAP-PROVIDER-LINK**: Resolve b'c link to Kahun slide versus O-3c label on separate slide.
- **GAP-DIRECTION-M**: Collate m: conditional left-to-right in survey, right-to-left in provider config.
- **GAP-UMM**: Examine Schwartz 2010 and 2021; establish O-3a/b/c identity and evaluate alphabetic alternatives.

## Counting claims

These counts describe different source-defined units; do not sum them.

| Source | Count | Unit |
|---|---:|---|
| mnamon-merlo | 14 | labelled_inscription_entries |
| maeder-baf | 15 | inscriptions_reported |
| maeder-baf | 28 | tentatively_assigned_fragments_reported |
| ocbi-current | 18 | provider_claimed_certain_inscriptions |
| ocbi-current | 14 | provider_claimed_potential_inscriptions |
| ocbi-current | 43 | rendered_record_entries |
| aub-mendenhall | 9 | publisher_reported_discovered_texts |

## Catalogue

| ID | Membership | Description | Evidence |
|---|---|---|---|
| BYB-A | reported_core | a | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos; dunand-1930, p. 1 |
| BYB-B | reported_core | b | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-C | reported_core | c | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-CAND-BALUA | disputed | Balu'a stele | ocbi-plate-z_a, caption and labelled example |
| BYB-CAND-CYLINDER-2004 | disputed | Cylinder seal published by Garbini and colleagues | vita-zamora-2018, p. 89, fig. 21 |
| BYB-CAND-DEIR-RIFA | disputed | Deir Rifa seal-amulet | ocbi-plate-z_d, caption and labelled example |
| BYB-CAND-KAHUN | disputed | Kahun object with proposed writing | ocbi-plate-z_c, caption and labelled example |
| BYB-CAND-LAMP-1 | disputed | Egyptian lamp inscription 1 | vita-zamora-2018, p. 88, fig. 20d |
| BYB-CAND-LAMP-2 | disputed | Egyptian lamp inscription 2 | vita-zamora-2018, p. 88, fig. 20e |
| BYB-CAND-LAMP-3 | disputed | Egyptian lamp inscription 3 | vita-zamora-2018, p. 88, fig. 20f |
| BYB-CAND-LINEAR-STELA | disputed | Linear pseudo-hieroglyphic block | vita-zamora-2018, pp. 85–86, fig. 16 |
| BYB-CAND-MEGIDDO-RING | disputed | Megiddo ring | vita-zamora-2018, p. 88, fig. 20a; n. 7 |
| BYB-CAND-PALIMPSEST-KAI1 | disputed | Ahirom inscription underlying layer | vita-zamora-2018, p. 88, fig. 19 and n. 6 |
| BYB-CAND-PALIMPSEST-KAI3 | disputed | Spatula associated with KAI 3 | vita-zamora-2018, pp. 86–87, fig. 17 |
| BYB-CAND-PALIMPSEST-KAI4 | disputed | Yehimilk inscription underlying layer | vita-zamora-2018, pp. 87–88, fig. 18 |
| BYB-CAND-RIETI | disputed | Rieti votive object | ocbi-plate-s, caption and labelled example |
| BYB-CAND-SCARABOID | disputed | Scaraboid seal of unknown origin | vita-zamora-2018, p. 88, fig. 20g |
| BYB-CAND-SINAI-526 | disputed | Sinai inscription 526 | vita-zamora-2018, p. 88, fig. 20b |
| BYB-CAND-STONE-SEAL-2010 | disputed | Stone seal discussed by Colless | ocbi-plate-z, caption and labelled example |
| BYB-CAND-TEL-HALIF | disputed | Tel Halif jar handle | ocbi-plate-v, caption and labelled example |
| BYB-CAND-TELL-JISR | disputed | Tell Jisr sherd | ocbi-plate-w, caption and labelled example |
| BYB-CAND-THEBES-OSTRACON | disputed | Thebes ostracon | vita-zamora-2018, p. 88, fig. 20c |
| BYB-CAND-TRIESTE | disputed | Trieste plaque | vita-zamora-2018, p. 88, fig. 20h |
| BYB-CAND-ULUBURUN | disputed | Uluburun writing-board marks | ocbi-plate-x, caption and labelled example |
| BYB-CAND-UMM-O3A | disputed | Schwartz O-3a example | ocbi-plate-z_b, caption and labelled example |
| BYB-CAND-UMM-O3B | disputed | Schwartz O-3b example | ocbi-plate-z_b, caption and labelled example |
| BYB-CAND-UMM-O3C | disputed | Schwartz O-3c example | ocbi-plate-z_b, caption and labelled example |
| BYB-D | reported_core | d | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-E | reported_core | e | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-F | reported_core | f | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-G | reported_core | g | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-H | reported_core | h | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-I | reported_core | i | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-J | reported_core | j | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-K | reported_core | k | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-L | reported_core | l | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-M | reported_core | m | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |
| BYB-N | reported_core | n | mnamon-merlo, Corpus of the pseudo-hieroglyphic inscriptions of Byblos |

## Sources and rights

- **archive-dunand**: Internet Archive catalogue, Byblia grammata, bybliagrammatado0000duna.
  Consultation: metadata_only; rights: not_assessed.
  Source: https://archive.org/details/bybliagrammatado0000duna
- **aub-mendenhall**: AUB Press, The Syllabic Inscriptions from Byblos (publisher description).
  Consultation: consulted_online; rights: not_assessed.
  Source: https://www.aub.edu.lb/aubpress/pages/thesyllabic.aspx
- **colless-deir-rifa**: B. E. Colless (2011), Amulet from Deir Rifa, Cryptcracker.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://cryptcracker.blogspot.com/2011/09/from-deir-rifa-gordon-hamilton-has.html
- **commons-e**: Hans van Deukeren, stylized redraw of spatula e, Wikimedia Commons.
  Consultation: metadata_only; rights: license_stated.
  Source: https://commons.wikimedia.org/wiki/File:Byblos_syll_spat_e.png
- **dunand-1930**: M. Dunand (1930), Nouvelle inscription découverte à Byblos. Syria 11(1), pp. 1–10.
  Consultation: selected_pages; rights: not_assessed.
  Source: https://www.persee.fr/doc/syria_0039-7946_1930_num_11_1_3456
- **dunand-1945**: Maurice Dunand (1945), Byblia Grammata, Beirut, pp. 71–138 (bibliographic lead via Mnamon).
  Consultation: not_consulted; rights: not_assessed.
- **dunand-1978**: M. Dunand, Nouvelles inscriptions pseudo-hiéroglyphiques découvertes à Byblos. Bulletin du Musée de Beyrouth 30 (nominal 1978). Pagination and actual publication year disputed in secondary metadata.
  Consultation: not_consulted; rights: not_assessed.
- **izreel-1988**: S. Izre'el (1988), review of Mendenhall, The Syllabic Inscriptions from Byblos. JAOS 108(3), pp. 519–521.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://www.tau.ac.il/~izreel/publications/RevMendenhall_JAOS1988.pdf
- **keibi-dunand-1978**: KeiBi online, Dunand 1978 record KEI00067546.
  Consultation: consulted_online; rights: not_assessed.
  Source: https://ocb.uni-tuebingen.de/Record/KEI00067546/Details
- **keibi-schwartz**: KeiBi online, Schwartz 2010, KEI00104326.
  Consultation: consulted_online; rights: not_assessed.
  Source: https://vergil.uni-tuebingen.de/keibi/Record/KEI00104326/Description
- **maeder-baf**: Michael Mäder (2022), Detecting word boundaries in an undeciphered script: The Byblos syllabary. BAF-Online 4(1), proceedings of the 2019 forum.
  Consultation: abstract_only; rights: license_stated.
  Source: https://bop.unibe.ch/baf/article/view/7186
- **mnamon-bibliography**: Mnamon, Byblos bibliography.
  Consultation: consulted_online; rights: not_assessed.
  Source: https://mnamon.sns.it/index.php?id=3&lang=en&page=Bibliografia
- **mnamon-merlo**: Paolo Merlo, Byblos (Pseudo-hieroglyphic), Mnamon, updated March 2022.
  Consultation: consulted_online; rights: not_assessed.
  Source: https://mnamon.sns.it/index.php?id=3&lang=en&page=Scrittura
- **ocbi-current**: GEAS / Byblicon, Online Corpus of Byblos Inscriptions (OCBI), live compiled application.
  Consultation: metadata_only; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/elamicon.js
- **ocbi-introduction**: GEAS, Introduction to the decipherment tool and Byblicon citation guidance.
  Consultation: consulted_online; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool-introduction/
- **ocbi-plate-o_recto**: GEAS / OCBI, explanatory slide o_recto.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/o_recto.jpg
- **ocbi-plate-p**: GEAS / OCBI, explanatory slide p.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/p.jpg
- **ocbi-plate-q**: GEAS / OCBI, explanatory slide q.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/q.jpg
- **ocbi-plate-r**: GEAS / OCBI, explanatory slide r.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/r.jpg
- **ocbi-plate-s**: GEAS / OCBI, explanatory slide s.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/s.jpg
- **ocbi-plate-t**: GEAS / OCBI, explanatory slide t.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/t.jpg
- **ocbi-plate-u**: GEAS / OCBI, explanatory slide u.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/u.jpg
- **ocbi-plate-v**: GEAS / OCBI, explanatory slide v.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/v.jpg
- **ocbi-plate-w**: GEAS / OCBI, explanatory slide w.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/w.jpg
- **ocbi-plate-x**: GEAS / OCBI, explanatory slide x.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/x.jpg
- **ocbi-plate-y**: GEAS / OCBI, explanatory slide y.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/y.jpg
- **ocbi-plate-z**: GEAS / OCBI, explanatory slide z.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/z.jpg
- **ocbi-plate-z_a**: GEAS / OCBI, explanatory slide z_a.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/z_a.jpg
- **ocbi-plate-z_b**: GEAS / OCBI, explanatory slide z_b.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/z_b.jpg
- **ocbi-plate-z_c**: GEAS / OCBI, explanatory slide z_c.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/z_c.jpg
- **ocbi-plate-z_d**: GEAS / OCBI, explanatory slide z_d.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/tool/plates/byblos/z_d.jpg
- **ocbi-repository**: Elamicon project, README legalese and encoding notes.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://github.com/elamicon/elamicon/blob/69b4cc2822493146045cb9969586bf5bd9195380/README.md
- **ocbi-source**: Elamicon / GEAS, src/Scripts/Byblos.elm.
  Consultation: metadata_only; rights: not_assessed.
  Source: https://github.com/elamicon/elamicon/blob/69b4cc2822493146045cb9969586bf5bd9195380/src/Scripts/Byblos.elm
- **schmutz-maeder-2024**: E. Schmutz and M. Mäder, Die Byblos-Schrift: Beurteilung des Entzifferungsvorschlags von F. Woudhuizen und J. Best anhand der GEAS-Methodologie. Assessing Decipherment Attempts Series 1, No. 2024/1.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://center-for-decipherment.ch/journal/2024_01__Schmutz-%26-Maeder__Die-Byblos-Schrift_Beurteilung-Woudhuizen-Best.pdf
- **schwartz-cv**: G. M. Schwartz, institutional CV (2025), bibliography.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://krieger.jhu.edu/near-east/wp-content/uploads/sites/73/2016/03/SCHWARTZ-CV-2025.ACC_.pdf
- **vita-zamora-2018**: J.-P. Vita and J.-Á. Zamora (2018), The Byblos Script. Paths into Script Formation in the Ancient Mediterranean, SMEA NS Supplemento 1, pp. 75–102.
  Consultation: selected_sections; rights: not_assessed.
  Source: https://www.academia.edu/37706221/The_Byblos_Script

## Interpretation

Passing software checks validates recorded structure, not archaeological truth, licence validity or completeness.
No corpus sequences, font files or source plate images are republished.
CSV empty fields mean null/unknown in this view; use bundle.json for exact types.
Checksums establish snapshot integrity, not authenticity or scholarly correctness.
