// ============================================================
// PRODUCT CATALOG  (edit prices here, everything else reads it)
// Copy is composition and specifications only: no activity, mechanism, or effect language.
// Set retail prices below in whole dollars (USD).
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
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/CJC-Front-NoShadow-01K18XRHEPZPDRJ9VEFXTVSBAV.png",
    short: "A research blend containing GHK-Cu, BPC-157, and TB-500. Supplied as 30 count strips, net wt 3.75 g. Sold for laboratory research use only.",
    sections: [
      { h: "Composition", p: "Per strip:", li: ["BPC-157 300 mcg", "TB-500 250 mcg", "GHK-Cu 2 mg"] },
      { h: "Specifications", p: "", li: ["Form: strip", "Count: 30", "Net weight: 3.75 g", "Storage: store sealed in a cool, dry place away from light"] },
      { h: "Documentation", p: "Certificate of Analysis available on request.", li: [] }
    ]
  },
  {
    id: "wolverine",
    name: "WOLVERINE",
    subtitle: "BPC-157 / TB-500",
    sku: "WLV-PEP-003",
    price: 120,
    count: "30 ct",
    weight: "3.75 g",
    perStrip: ["BPC-157 500 mcg", "TB-500 500 mcg"],
    color: "peach",
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/Wolverine-Front-NoShadow-01K18YVGAX29D769SHG2RKYG3Q.png",
    short: "A research blend containing BPC-157 and TB-500. Supplied as 30 count strips, net wt 3.75 g. Sold for laboratory research use only.",
    sections: [
      { h: "Composition", p: "Per strip:", li: ["BPC-157 500 mcg", "TB-500 500 mcg"] },
      { h: "Specifications", p: "", li: ["Form: strip", "Count: 30", "Net weight: 3.75 g", "Storage: store sealed in a cool, dry place away from light"] },
      { h: "Documentation", p: "Certificate of Analysis available on request.", li: [] }
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
    short: "Nicotinamide adenine dinucleotide (NAD+), a naturally occurring coenzyme, supplied as 30 count strips, net wt 8.55 g. Sold for laboratory research use only.",
    sections: [
      { h: "Composition", p: "Per strip:", li: ["NAD+ 100 mg"] },
      { h: "Specifications", p: "", li: ["Form: strip", "Count: 30", "Net weight: 8.55 g", "Storage: store sealed in a cool, dry place away from light"] },
      { h: "Documentation", p: "Certificate of Analysis available on request.", li: [] }
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
    image: "https://thepeptide.s3.us-east-1.amazonaws.com/Glow-Front-NoShadow 1 (1)-01K18YQWGPQRKRYGZXY7K4QFFC.png",
    short: "A research blend containing CJC-1295 and Ipamorelin. Supplied as 20 count strips, net wt 2.6 g. Sold for laboratory research use only.",
    sections: [
      { h: "Composition", p: "Per strip:", li: ["CJC-1295 250 mcg", "Ipamorelin 250 mcg"] },
      { h: "Specifications", p: "", li: ["Form: strip", "Count: 20", "Net weight: 2.6 g", "Storage: store sealed in a cool, dry place away from light"] },
      { h: "Documentation", p: "Certificate of Analysis available on request.", li: [] }
    ]
  }
];
