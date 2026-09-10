// ============================================================
// PRODUCT CATALOG  (edit prices here, everything else reads it)
// thepeptide.com only shows prices after login, so set your own
// retail prices below in whole dollars (USD).
// ============================================================
const PRODUCTS = [
  {
    id: "glow",
    name: "GLOW",
    subtitle: "GHK-Cu / BPC-157 / TB-500",
    sku: "GLW-PEP-001",
    price: 120,
    count: "30 ct",
    weight: "3.75 g",
    perStrip: ["BPC-157 300 mcg", "TB-500 250 mcg", "GHK-Cu 2 mg"],
    color: "cyan",
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/Glow-Front-NoShadow 1 (1)-01K18YQWGPQRKRYGZXY7K4QFFC.png",
    short: "A three peptide research blend of GHK-Cu, BPC-157, and TB-500, each studied for tissue remodeling, cell migration, and regeneration in experimental models.",
    sections: [
      { h: "GHK-Cu (Copper Tripeptide-1)", p: "A naturally occurring copper binding tripeptide (glycyl-L-histidyl-L-lysine). Research has examined its role in:", li: ["Tissue remodeling and wound healing", "Regulation of gene expression related to repair and regeneration", "Supporting angiogenesis (formation of new blood vessels)", "Anti-inflammatory and antioxidant properties in in vitro models", "Stimulating collagen and elastin synthesis in cell cultures"] },
      { h: "BPC-157 (Body Protection Compound)", p: "A pentadecapeptide derived from a protein found in gastric juice. Research indicates its potential in:", li: ["Supporting endothelial function and angiogenesis in vascular models", "Promoting cell migration and fibroblast activity", "Tendon and ligament structural integrity in animal studies", "Gastrointestinal mucosal protection", "Modulating nitric oxide pathways in oxidative stress environments"] },
      { h: "TB-500 (Thymosin Beta-4 Fragment)", p: "A synthetic segment of Thymosin Beta-4, a peptide involved in tissue regeneration. Studied in lab settings for:", li: ["Enhancing actin polymerization, supporting cell migration and structural integrity", "Promoting angiogenesis and tissue regeneration", "Modulating inflammatory responses in wound models", "Extracellular matrix remodeling"] },
      { h: "The Blend", p: "Combining these three peptides in one formula lets researchers explore the potential synergy of GHK-Cu, BPC-157, and TB-500 in a single blend.", li: [] }
    ]
  },
  {
    id: "wolverine",
    name: "WOLVERINE",
    subtitle: "BPC-157 / TB-500 Research Blend",
    sku: "WLV-PEP-003",
    price: 120,
    count: "30 ct",
    weight: "3.75 g",
    perStrip: ["BPC-157 500 mcg", "TB-500 500 mcg"],
    color: "peach",
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/Wolverine-Front-NoShadow-01K18YVGAX29D769SHG2RKYG3Q.png",
    short: "A research only formulation pairing BPC-157 and TB-500, two peptides independently explored for their roles in cellular dynamics, tissue structure, and molecular signaling.",
    sections: [
      { h: "BPC-157 (Body Protection Compound)", p: "A pentadecapeptide derived from a protein found in gastric juice. Research indicates its potential in:", li: ["Supporting endothelial function and angiogenesis in vascular models", "Promoting cell migration and fibroblast activity", "Tendon and ligament structural integrity in animal studies", "Gastrointestinal mucosal protection", "Modulating nitric oxide pathways in oxidative stress environments"] },
      { h: "TB-500 (Thymosin Beta-4 Fragment)", p: "A synthetic segment of Thymosin Beta-4, a peptide involved in tissue regeneration. Studied in lab settings for:", li: ["Enhancing actin polymerization, supporting cell migration and structural integrity", "Promoting angiogenesis and tissue regeneration", "Modulating inflammatory responses in wound models", "Extracellular matrix remodeling"] },
      { h: "The Blend", p: "Pairing BPC-157 and TB-500 lets researchers examine how two peptides with activity in tissue structure and signaling may function together. This dual peptide combination is commonly studied in research exploring repair mechanisms, inflammatory modulation, and vascular remodeling.", li: [] }
    ]
  },
  {
    id: "nad",
    name: "NAD+",
    subtitle: "Nicotinamide Adenine Dinucleotide",
    sku: "NAD-PEP-004",
    price: 120,
    count: "30 ct",
    weight: "8.55 g",
    perStrip: ["NAD+ 100 mg"],
    color: "lime",
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/NAD-Front-NoShadow-01K18YXJT1HGR2CKQHD9MV0JT7.png",
    short: "A naturally occurring coenzyme present in all living cells and a central component of cellular metabolism, energy transfer, and redox balance.",
    sections: [
      { h: "Biochemical Function", p: "NAD+ exists in an oxidized form (NAD+) and a reduced form (NADH). These forms participate in redox reactions essential for:", li: ["Electron transport in glycolysis, the citric acid cycle, and oxidative phosphorylation", "Mitochondrial activity and cellular energy balance in experimental models", "Maintenance of cellular redox state under varying physiological conditions"] },
      { h: "Research Applications", p: "Studies involving NAD+ commonly investigate its role in:", li: ["Enzymatic activity as a co-substrate for sirtuins and PARPs, implicated in DNA repair, epigenetic regulation, and cellular stress responses", "Metabolic regulation, mitochondrial efficiency, and overall bioenergetic status", "Aging and stress response models linked to longevity and cellular resilience"] },
      { h: "Why NAD+ Is Widely Studied", p: "Because NAD+ is integral to core cellular functions, it is widely used as a research tool for investigating metabolic regulation, oxidative stress, and cell signaling in controlled scientific studies.", li: [] }
    ]
  },
  {
    id: "cjc-1295-ipamorelin",
    name: "CJC-1295",
    subtitle: "/ Ipamorelin",
    sku: "CJC-PEP-002",
    price: 120,
    count: "20 ct",
    weight: "2.6 g",
    perStrip: ["CJC-1295 250 mcg", "Ipamorelin 250 mcg"],
    color: "lemon",
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/CJC-Front-NoShadow-01K18XRHEPZPDRJ9VEFXTVSBAV.png",
    short: "A research blend of two growth hormone secretagogues: CJC-1295, a synthetic GHRH analog, and Ipamorelin, a selective growth hormone releasing peptide.",
    sections: [
      { h: "CJC-1295", p: "A tetrasubstituted GHRH analog developed to extend the half-life and stability of native GHRH. In experimental models it has been observed to:", li: ["Prolong GH releasing activity via GHRH receptor binding", "Increase GH pulse amplitude without significantly affecting frequency", "Reduced degradation through albumin binding (DAC modified variant)", "Allow less frequent administration in research applications due to extended plasma half-life"] },
      { h: "Ipamorelin", p: "A pentapeptide GHRP that selectively binds the ghrelin receptor (GHS-R1a). Widely studied for:", li: ["Stimulating GH release in a dose dependent manner in lab models", "Minimal activity on cortisol, prolactin, or aldosterone levels", "Working independently of GHRH pathways, often examined for additive effects with GHRH analogs"] },
      { h: "The Blend", p: "One peptide targets the GHRH receptor and the other engages the ghrelin receptor. This dual receptor approach lets researchers investigate two independent signaling pathways involved in growth hormone regulation.", li: [] }
    ]
  }
];
