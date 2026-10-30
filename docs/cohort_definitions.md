# Cohort, outcome and covariate definitions (TriNetX study 410410)

## Target trial specification


| Component | Target trial | Emulation in TriNetX |
|---|---|---|
| Eligibility | Adults with type 2 diabetes (E11) needing a new glucose-lowering drug; or adults with obesity (E66) without diabetes | Diagnosis on or before index; no prior GLP-1 receptor agonist or tirzepatide; comparator users with no prior use of the same class before 2018; GLP-1 drug users with no prior SGLT2 inhibitor |
| Treatment strategies | Start semaglutide or tirzepatide versus start an SGLT2 inhibitor (primary); secondary: each drug separately versus an SGLT2 inhibitor, a DPP-4 inhibitor, the other drug, or no GLP-1 drug | First prescription (RxNorm ingredient) between 13 May 2022 and 28 Oct 2025 (primary and tirzepatide versus semaglutide) or between 1 Jan 2018 and 28 Oct 2025 (other secondary comparisons) |
| Assignment | Random | 1:1 propensity-score matching on 43 baseline variables (nearest neighbour, calliper 0.1 pooled SD) |
| Start of follow-up | Treatment start | Day 1 after first prescription |
| Outcomes | First diagnosis of each of 19 psychiatric disorders | ICD-10-CM codes (Supplementary Table 2); patients with the outcome before follow-up excluded per outcome |
| Follow-up | 3 years | Days 1–1,095; censored at last record |
| Causal contrast | Intention-to-treat | Analogue of intention-to-treat (initial treatment, no censoring at switching or stopping) |
| Analysis | Cox model | Cox proportional hazards in TriNetX; empirical calibration with 6 negative controls; Benjamini–Hochberg FDR; E-values |

**Primary analysis.** Semaglutide or tirzepatide vs SGLT2 inhibitors in type 2 diabetes, both groups restricted to new users from 13 May 2022 to 28 October 2025; drug users with no prior GLP-1 receptor agonist, tirzepatide or SGLT2 inhibitor; comparator users with no prior GLP-1 receptor agonist or tirzepatide and no SGLT2 inhibitor before 13 May 2022.

**Secondary comparisons.** (1) Semaglutide vs SGLT2 inhibitors, type 2 diabetes, from 2018. (2) Tirzepatide vs SGLT2 inhibitors. (3) Semaglutide vs DPP-4 inhibitors. (4) Tirzepatide vs semaglutide, new users from 13 May 2022; semaglutide use before that date excluded. (5) Semaglutide vs no GLP-1 drug: type 2 diabetes with obesity and metformin use, index 2020–2025. (6) Tirzepatide vs the same untreated type 2 diabetes group. (7) Semaglutide vs no anti-obesity drug in obesity without type 2 diabetes; comparison group required obstructive sleep apnoea (G47.33) and no GLP-1 drugs, tirzepatide, orlistat, phentermine or bariatric surgery. (8) Tirzepatide vs the same obesity comparison group; tirzepatide users had no prior semaglutide, other GLP-1 receptor agonist or SGLT2 inhibitor.

**Drug definitions (RxNorm ingredients).** Semaglutide 1991302; tirzepatide 2601723; liraglutide 475968; dulaglutide 1551291; exenatide 60548; lixisenatide 1440051; albiglutide 1534763; empagliflozin 1545653; dapagliflozin 1488564; canagliflozin 1373458; ertugliflozin 1992672; DPP-4 inhibitors by ingredient (sitagliptin, saxagliptin, linagliptin, alogliptin).

**Matching covariates (43).** Age at index; sex; ethnicity; race; ICD-10-CM blocks E78, E65–E68, I10–I1A, I30–I5A, I20–I25, F40–F48, F30–F39, F10–F19, F50–F59, F90–F98, F20–F29, F60–F69, N17–N19, K70–K77, G47; VA drug classes HS502 (oral hypoglycaemics), HS501 (insulin), CN300 (sedatives/hypnotics), CN600 (antidepressants), CN400 (anticonvulsants), CN700 (antipsychotics), CN101 (opioid analgesics), CV350 (antilipemic agents), CV700 (diuretics), CV100 (beta blockers), CV800 (ACE inhibitors), CV200 (calcium channel blockers), CV805 (angiotensin II inhibitors); BMI (TNX 9083) and HbA1c (TNX 9037) in categories.

**Extended-adjustment sensitivity analysis.** The 43 covariates plus BMI in nine bands (<25, 25–27.5, 27.5–30, 30–32.5, 32.5–35, 35–37.5, 37.5–40, 40–45, ≥45 kg/m²), HbA1c in seven bands (<6.5, 6.5–7, 7–7.5, 7.5–8, 8–9, 9–10, ≥10%) and any prior CPT 1013711 (emergency department services), 1013626 (office or other outpatient services), 1013659 (hospital inpatient and observation care) and 1012681 (psychiatry services and procedures). TriNetX assigns a patient to a band if any recorded value fell in it.

**TriNetX queries and analyses.** Primary: cohort queries 15334422 (semaglutide or tirzepatide, 2022–2025) and 15334477 (SGLT2 inhibitors, 2022–2025).

## Outcome and negative-control definitions

| Domain | Outcome | ICD-10-CM |
|---|---|---|
| Substance use | Alcohol related disorders | F10 |
| | Opioid related disorders | F11 |
| | Cannabis related disorders | F12 |
| | Cocaine related disorders | F14 |
| | Other stimulant related disorders | F15 |
| | Nicotine dependence | F17 |
| Psychosis and bipolar | Schizophrenia | F20 |
| | Bipolar disorder | F31 |
| Suicidality | Suicidal ideations | R45.851 |
| | Suicide attempt | T14.91 |
| Depression, anxiety, stress, sleep | Depressive episode | F32 |
| | Major depressive disorder, recurrent | F33 |
| | Other anxiety disorders | F41 |
| | Reaction to severe stress, and adjustment disorders | F43 |
| | Insomnia | G47.0 |
| Eating, impulse, compulsive | Bulimia nervosa | F50.2 |
| | Anorexia nervosa | F50.0 |
| | Pathological gambling | F63.0 |
| | Obsessive-compulsive disorder | F42 |
| Negative control | Ingrowing nail | L60.0 |
| | Otitis externa | H60 |
| | Vasomotor and allergic rhinitis | J30 |
| | Melanocytic naevi | D22 |
| | Fracture of forearm | S52 |
| | Disorders of refraction and accommodation | H52 |


## Obesity tirzepatide cohort

Identical to the semaglutide obesity cohort with tirzepatide (RxNorm 2601723) as the index drug and semaglutide (RxNorm 1991302) added to the prior-use exclusions.
