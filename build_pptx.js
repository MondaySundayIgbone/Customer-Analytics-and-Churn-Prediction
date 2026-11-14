const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Sunday Monday Igbone";
pres.title = "Customer Analytics & Churn Prediction System";

// ── Palette ──────────────────────────────────────────────────────────────────
const NAVY    = "1B2A4A";
const BLUE    = "2E6DA4";
const LBLUE   = "4A90C4";
const WHITE   = "FFFFFF";
const OFFWHITE= "F4F6F9";
const GRAY    = "64748B";
const DGRAY   = "334155";
const GREEN   = "16A34A";
const AMBER   = "D97706";
const RED     = "DC2626";

const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.12 });

// ── Helpers ──────────────────────────────────────────────────────────────────
function dot(slide, x, y, color) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: 0.18, h: 0.18,
    fill: { color },
    line: { color, width: 0 },
  });
}

function card(slide, x, y, w, h, fillColor) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fillColor || OFFWHITE },
    rectRadius: 0.12,
    line: { color: "E2E8F0", width: 0.5 },
    shadow: makeShadow(),
  });
}

function sectionBadge(slide, label, x, y) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w: 1.6, h: 0.3,
    fill: { color: BLUE },
    rectRadius: 0.06,
    line: { color: BLUE, width: 0 },
  });
  slide.addText(label.toUpperCase(), {
    x, y, w: 1.6, h: 0.3,
    fontSize: 7, bold: true, color: WHITE,
    align: "center", valign: "middle", margin: 0,
  });
}

// ── SLIDE 1 — TITLE ──────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  // Decorative circle top-right
  s.addShape(pres.shapes.OVAL, { x: 7.8, y: -1.2, w: 4, h: 4, fill: { color: BLUE, transparency: 75 }, line: { color: BLUE, width: 0 } });
  s.addShape(pres.shapes.OVAL, { x: 8.5, y: -0.6, w: 2.5, h: 2.5, fill: { color: LBLUE, transparency: 80 }, line: { color: LBLUE, width: 0 } });

  // Bottom accent circle
  s.addShape(pres.shapes.OVAL, { x: -0.8, y: 4, w: 3, h: 3, fill: { color: BLUE, transparency: 80 }, line: { color: BLUE, width: 0 } });

  s.addText("Customer Analytics &", { x: 0.6, y: 1.1, w: 8.8, h: 0.7, fontSize: 36, bold: true, color: WHITE, fontFace: "Cambria", align: "left" });
  s.addText("Churn Prediction System", { x: 0.6, y: 1.75, w: 8.8, h: 0.7, fontSize: 36, bold: true, color: WHITE, fontFace: "Cambria", align: "left" });

  // Divider line
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.58, w: 2.4, h: 0.05, fill: { color: LBLUE }, line: { color: LBLUE, width: 0 } });

  s.addText("Fraudulent Transaction Detection  |  Customer Segmentation  |  Real-Time Risk Scoring", {
    x: 0.6, y: 2.75, w: 9, h: 0.35, fontSize: 11, color: "CADCFC", fontFace: "Calibri", align: "left",
  });

  s.addText("Sunday Monday Igbone", { x: 0.6, y: 3.5, w: 5, h: 0.3, fontSize: 12, bold: true, color: WHITE, fontFace: "Calibri" });
  s.addText("Data Science Intern  ·  Amdari  ·  June 2026", { x: 0.6, y: 3.82, w: 6, h: 0.28, fontSize: 10, color: "94A3B8", fontFace: "Calibri" });

  s.addNotes("Welcome everyone. Today I will walk you through our end-to-end customer analytics and churn prediction system, covering fraud detection, customer segmentation, and real-time risk scoring.");
}

// ── SLIDE 2 — EXECUTIVE SUMMARY ──────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  // Top navy band
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("EXECUTIVE SUMMARY", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const items = [
    { icon: "●", color: BLUE,  text: "Analysed 10,000 customers and 200,000+ transactions across a ride-hailing platform" },
    { icon: "●", color: GREEN, text: "Built 3 churn prediction models — best model achieved AUC = 1.00" },
    { icon: "●", color: RED,   text: "Detected fraud on NovaPay digital payments: ROC-AUC = 0.982, 96% overall accuracy" },
    { icon: "●", color: AMBER, text: "Segmented customers into 4 actionable business groups using K-Means clustering" },
    { icon: "●", color: BLUE,  text: "Deployed real-time scoring API (FastAPI) and interactive analytics dashboard (Streamlit)" },
    { icon: "●", color: GREEN, text: "Established production monitoring with automated data drift detection" },
  ];

  const startY = 1.05;
  items.forEach((item, i) => {
    const y = startY + i * 0.72;
    card(s, 0.35, y, 9.3, 0.6, WHITE);
    s.addShape(pres.shapes.OVAL, { x: 0.55, y: y + 0.2, w: 0.22, h: 0.22, fill: { color: item.color }, line: { color: item.color, width: 0 } });
    s.addText(item.text, { x: 0.95, y: y + 0.04, w: 8.55, h: 0.52, fontSize: 12, color: DGRAY, fontFace: "Calibri", valign: "middle" });
  });

  s.addNotes("This slide summarises the full scope of work. Six major deliverables, spanning data engineering, modelling, deployment, and monitoring.");
}

// ── SLIDE 3 — BUSINESS PROBLEM ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: OFFWHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("THE BUSINESS PROBLEM", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const cols = [
    { title: "Churn Risk", color: RED,   body: "Identifying which customers are likely to stop using the platform before they leave, enabling proactive retention campaigns before revenue is lost." },
    { title: "Fraud Exposure", color: AMBER, body: "Detecting fraudulent digital money transfers in real time to protect revenue and maintain customer trust on the NovaPay platform." },
    { title: "Customer Understanding", color: BLUE, body: "Segmenting customers by behaviour and lifetime value to focus retention resources on the right groups at the right time." },
  ];

  cols.forEach((col, i) => {
    const x = 0.3 + i * 3.15;
    card(s, x, 1.05, 3.0, 3.3, WHITE);
    s.addShape(pres.shapes.OVAL, { x: x + 1.1, y: 1.2, w: 0.8, h: 0.8, fill: { color: col.color }, line: { color: col.color, width: 0 } });
    s.addText(col.title, { x: x + 0.1, y: 2.15, w: 2.8, h: 0.45, fontSize: 13, bold: true, color: NAVY, fontFace: "Cambria", align: "center" });
    s.addText(col.body, { x: x + 0.15, y: 2.62, w: 2.7, h: 1.6, fontSize: 10, color: DGRAY, fontFace: "Calibri", align: "center", valign: "top" });
  });

  // Bottom note
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.3, y: 4.52, w: 9.4, h: 0.75, fill: { color: NAVY }, rectRadius: 0.08, line: { color: NAVY, width: 0 } });
  s.addText('"Without data-driven tools, these risks are identified too late — after revenue is already lost."', {
    x: 0.4, y: 4.52, w: 9.2, h: 0.75, fontSize: 11, italic: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle",
  });

  s.addNotes("These three problems motivated the project. All three require different ML approaches but share a common foundation in feature engineering from behavioural data.");
}

// ── SLIDE 4 — DATA OVERVIEW ──────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("DATA SOURCES & SCALE", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const headers = [["Dataset", "Records", "Key Fields"]];
  const rows = [
    ["Riders", "10,000", "Age, loyalty tier, churn probability, referral status"],
    ["Trips", "200,000", "Fare, tip, surge multiplier, pickup time, location, weather"],
    ["Sessions", "50,000", "Time on app, pages visited, session conversion rate"],
    ["NovaPay Transactions", "10,836", "IP risk, device trust, KYC tier, transaction velocity"],
    ["Drivers", "5,000", "Rating, vehicle type, acceptance rate"],
  ];

  const tableData = [
    headers[0].map(h => ({ text: h, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 11, fontFace: "Calibri", align: "center" } })),
    ...rows.map((row, i) => row.map((cell, j) => ({
      text: cell,
      options: { color: j === 0 ? NAVY : DGRAY, bold: j === 0, fill: { color: i % 2 === 0 ? WHITE : OFFWHITE }, fontSize: 10.5, fontFace: "Calibri", align: j === 2 ? "left" : "center" },
    }))),
  ];

  s.addTable(tableData, {
    x: 0.4, y: 1.05, w: 9.2,
    colW: [2.0, 1.5, 5.7],
    rowH: 0.55,
    border: { pt: 0.5, color: "E2E8F0" },
  });

  // Total record count callout
  card(s, 3.5, 4.52, 3.0, 0.75, OFFWHITE);
  s.addText("Total Records Analysed: 275,836+", {
    x: 3.5, y: 4.52, w: 3.0, h: 0.75, fontSize: 12, bold: true, color: NAVY, fontFace: "Calibri", align: "center", valign: "middle",
  });

  s.addNotes("Five datasets were combined. The NovaPay data is for the fraud detection workstream; the riders, trips and sessions data feeds the churn prediction and segmentation models.");
}

// ── SLIDE 5 — FEATURE ENGINEERING ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: OFFWHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("FEATURE ENGINEERING PIPELINE", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  // Left panel — churn features
  card(s, 0.3, 1.05, 4.55, 4.3, WHITE);
  sectionBadge(s, "Churn Features — 23 Total", 0.45, 1.15);

  const leftGroups = [
    { label: "Recency", items: ["Days since last trip"], color: RED },
    { label: "Frequency", items: ["Trips per week", "Session count"], color: BLUE },
    { label: "Monetary", items: ["Total spend", "Avg fare", "Avg tip"], color: GREEN },
    { label: "Behavioural", items: ["Surge trip rate", "Weekend trip rate", "Cash payment rate"], color: AMBER },
    { label: "App Engagement", items: ["Time on app", "Pages visited", "Conversion rate"], color: LBLUE },
    { label: "Profile", items: ["Age group", "Loyalty rank", "Referral status"], color: NAVY },
  ];

  let ly = 1.58;
  leftGroups.forEach(g => {
    s.addShape(pres.shapes.OVAL, { x: 0.48, y: ly + 0.04, w: 0.16, h: 0.16, fill: { color: g.color }, line: { color: g.color, width: 0 } });
    s.addText(`${g.label}: `, { x: 0.72, y: ly, w: 3.9, h: 0.28, fontSize: 9.5, bold: true, color: NAVY, fontFace: "Calibri" });
    s.addText(g.items.join("  ·  "), { x: 0.72, y: ly + 0.22, w: 3.9, h: 0.28, fontSize: 9, color: GRAY, fontFace: "Calibri" });
    ly += 0.56;
  });

  // Right panel — fraud features
  card(s, 5.15, 1.05, 4.55, 4.3, WHITE);
  sectionBadge(s, "Fraud Features", 5.3, 1.15);

  const rightItems = [
    { label: "IP Risk Score", sub: "IP risk score & country mismatch", color: RED },
    { label: "Device Signals", sub: "Device trust score & new device flag", color: AMBER },
    { label: "Velocity", sub: "Transaction velocity (1h and 24h windows)", color: BLUE },
    { label: "KYC & History", sub: "KYC tier & chargeback history count", color: GREEN },
    { label: "Corridor Risk", sub: "Risk score per source-destination corridor", color: LBLUE },
    { label: "Time-Based Split", sub: "Applied to prevent future data leakage", color: NAVY },
  ];

  let ry = 1.58;
  rightItems.forEach(item => {
    s.addShape(pres.shapes.OVAL, { x: 5.32, y: ry + 0.04, w: 0.16, h: 0.16, fill: { color: item.color }, line: { color: item.color, width: 0 } });
    s.addText(item.label + ":", { x: 5.58, y: ry, w: 3.9, h: 0.28, fontSize: 9.5, bold: true, color: NAVY, fontFace: "Calibri" });
    s.addText(item.sub, { x: 5.58, y: ry + 0.22, w: 3.9, h: 0.28, fontSize: 9, color: GRAY, fontFace: "Calibri" });
    ry += 0.56;
  });

  s.addNotes("Feature engineering was the most time-intensive phase. For churn, we derived 23 features across 5 categories from 3 datasets. For fraud, domain-specific signals like IP country mismatch and transaction velocity were critical.");
}

// ── SLIDE 6 — CHURN PREDICTION RESULTS ───────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("CHURN PREDICTION — MODEL RESULTS", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });
  s.addText("3 models  ·  10,000 customers  ·  80/20 time-based split  ·  20% churn rate", {
    x: 0.4, y: 0.62, w: 9.2, h: 0.28, fontSize: 9, color: "CADCFC", fontFace: "Calibri",
  });

  // Table
  const churnHeaders = [["Model", "CV AUC", "Test AUC", "Avg Precision"]];
  const churnRows = [
    ["Random Forest",        "1.000", "1.000", "1.000"],
    ["Gradient Boosting",    "0.9996","1.000", "1.000"],
    ["Logistic Regression",  "1.000", "1.000", "0.9998"],
  ];

  const churnTable = [
    churnHeaders[0].map(h => ({ text: h, options: { bold: true, color: WHITE, fill: { color: BLUE }, fontSize: 11, fontFace: "Calibri", align: "center" } })),
    ...churnRows.map((row, i) => row.map((cell, j) => ({
      text: cell,
      options: { color: j === 0 ? NAVY : GREEN, bold: j !== 0, fill: { color: i % 2 === 0 ? WHITE : OFFWHITE }, fontSize: 11, fontFace: "Calibri", align: j === 0 ? "left" : "center" },
    }))),
  ];

  s.addTable(churnTable, {
    x: 0.4, y: 1.05, w: 9.2,
    colW: [3.6, 1.8, 1.8, 2.0],
    rowH: 0.6,
    border: { pt: 0.5, color: "E2E8F0" },
  });

  // Bar chart — AUC comparison
  s.addChart(pres.charts.BAR, [
    { name: "Test AUC", labels: ["Random Forest", "Gradient Boosting", "Logistic Regression"], values: [1.000, 1.000, 1.000] }
  ], {
    x: 0.4, y: 3.05, w: 5.5, h: 2.2, barDir: "col",
    chartColors: [BLUE, LBLUE, "4A90C4"],
    chartArea: { fill: { color: WHITE }, roundedCorners: true },
    catAxisLabelColor: GRAY, valAxisLabelColor: GRAY,
    valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
    showValue: true, dataLabelColor: NAVY,
    showLegend: false, showTitle: true, title: "Test AUC by Model",
    titleColor: NAVY, titleFontSize: 11,
    valAxisMinVal: 0.99,
  });

  // Insight box
  card(s, 6.1, 3.05, 3.55, 2.2, OFFWHITE);
  s.addText("Key Insight", { x: 6.2, y: 3.15, w: 3.35, h: 0.3, fontSize: 10, bold: true, color: NAVY, fontFace: "Cambria" });
  s.addText(
    "All 3 models achieved perfect AUC on the test set, demonstrating the churn signal is strongly captured by the engineered features.\n\nRandom Forest selected as the production model for its high precision on the minority churn class.",
    { x: 6.2, y: 3.5, w: 3.35, h: 1.6, fontSize: 9.5, color: DGRAY, fontFace: "Calibri", valign: "top" }
  );

  s.addNotes("Perfect AUC across all models reflects strong feature quality — particularly the churn probability score derived from behavioural signals. Random Forest is the recommended production model.");
}

// ── SLIDE 7 — FRAUD DETECTION RESULTS ────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: OFFWHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("FRAUD DETECTION — NOVAPAY TRANSACTIONS", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });
  s.addText("10,836 transactions  ·  9.1% fraud rate  ·  Time-based split to prevent data leakage", {
    x: 0.4, y: 0.62, w: 9.2, h: 0.28, fontSize: 9, color: "CADCFC", fontFace: "Calibri",
  });

  const fraudHeaders = [["Model", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"]];
  const fraudRows = [
    ["Logistic Regression", "0.795", "0.942", "0.862", "0.982 ★", "0.969"],
    ["Random Forest",        "0.969 ★", "0.919", "0.943 ★", "0.974", "0.957"],
    ["XGBoost",              "0.959", "0.919", "0.939", "0.970", "0.952"],
    ["LightGBM",             "0.950", "0.922", "0.936", "0.964", "0.949"],
  ];

  const fraudTable = [
    fraudHeaders[0].map(h => ({ text: h, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 10.5, fontFace: "Calibri", align: "center" } })),
    ...fraudRows.map((row, i) => row.map((cell, j) => ({
      text: cell,
      options: {
        color: cell.includes("★") ? GREEN : (j === 0 ? NAVY : DGRAY),
        bold: cell.includes("★") || j === 0,
        fill: { color: i % 2 === 0 ? WHITE : "EEF2FF" },
        fontSize: 10.5, fontFace: "Calibri", align: j === 0 ? "left" : "center",
      },
    }))),
  ];

  s.addTable(fraudTable, {
    x: 0.3, y: 1.05, w: 9.4,
    colW: [2.5, 1.4, 1.2, 1.2, 1.55, 1.55],
    rowH: 0.58,
    border: { pt: 0.5, color: "E2E8F0" },
  });

  // Two insight cards
  card(s, 0.3, 3.6, 4.5, 1.65, WHITE);
  s.addText("Best for Risk Ranking", { x: 0.45, y: 3.72, w: 4.2, h: 0.3, fontSize: 10.5, bold: true, color: NAVY, fontFace: "Cambria" });
  s.addShape(pres.shapes.OVAL, { x: 0.45, y: 4.08, w: 0.18, h: 0.18, fill: { color: GREEN }, line: { color: GREEN, width: 0 } });
  s.addText("Logistic Regression — ROC-AUC 0.982\nBest at ordering transactions by fraud probability. Ideal for fraud scoring queues and prioritised review workflows.", {
    x: 0.7, y: 4.0, w: 3.95, h: 1.15, fontSize: 9.5, color: DGRAY, fontFace: "Calibri",
  });

  card(s, 5.2, 3.6, 4.5, 1.65, WHITE);
  s.addText("Best for Blocking Decisions", { x: 5.35, y: 3.72, w: 4.2, h: 0.3, fontSize: 10.5, bold: true, color: NAVY, fontFace: "Cambria" });
  s.addShape(pres.shapes.OVAL, { x: 5.35, y: 4.08, w: 0.18, h: 0.18, fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
  s.addText("Random Forest — Precision 97%\nHighest precision minimises false positives. Fewer legitimate transactions blocked — less customer friction and dispute cost.", {
    x: 5.6, y: 4.0, w: 3.95, h: 1.15, fontSize: 9.5, color: DGRAY, fontFace: "Calibri",
  });

  s.addNotes("Two deployment modes are recommended: Logistic Regression for scoring/ranking, Random Forest for hard blocking decisions. The choice depends on the business cost of false positives vs missed fraud.");
}

// ── SLIDE 8 — CUSTOMER SEGMENTATION ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("CUSTOMER SEGMENTATION — 4 STRATEGIC GROUPS", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const segs = [
    { title: "High Risk – High Value", icon: "▲", color: RED,   bg: "FEF2F2", label: "PRIORITY 1", action: "Immediate personal outreach\nLoyalty upgrade offer\nDedicated account contact" },
    { title: "High Risk – Low Value",  icon: "▲", color: AMBER, bg: "FFFBEB", label: "PRIORITY 2", action: "Automated win-back promotion\nDiscount on next booking\nRe-engagement email sequence" },
    { title: "Low Risk – High Value",  icon: "●", color: GREEN, bg: "F0FDF4", label: "MAINTAIN",   action: "VIP programme enrolment\nEarly access to new features\nLoyalty rewards acceleration" },
    { title: "Low Risk – Low Value",   icon: "●", color: BLUE,  bg: OFFWHITE, label: "NURTURE",   action: "Upsell campaigns\nEngagement nudges\nReferral incentives" },
  ];

  const positions = [
    { x: 0.3,  y: 1.05 },
    { x: 5.15, y: 1.05 },
    { x: 0.3,  y: 3.1  },
    { x: 5.15, y: 3.1  },
  ];

  segs.forEach((seg, i) => {
    const { x, y } = positions[i];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.55, h: 1.85,
      fill: { color: seg.bg }, rectRadius: 0.12,
      line: { color: seg.color, width: 1.2 },
      shadow: makeShadow(),
    });
    // Label badge
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.15, y: y + 0.12, w: 1.1, h: 0.26, fill: { color: seg.color }, rectRadius: 0.06, line: { color: seg.color, width: 0 } });
    s.addText(seg.label, { x: x + 0.15, y: y + 0.12, w: 1.1, h: 0.26, fontSize: 7.5, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
    s.addText(seg.title, { x: x + 0.15, y: y + 0.44, w: 4.25, h: 0.32, fontSize: 12, bold: true, color: NAVY, fontFace: "Cambria" });
    s.addText(seg.action, { x: x + 0.15, y: y + 0.8, w: 4.25, h: 0.95, fontSize: 9.5, color: DGRAY, fontFace: "Calibri", valign: "top" });
  });

  // Bottom note
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.3, y: 5.1, w: 9.4, h: 0.35, fill: { color: OFFWHITE }, rectRadius: 0.06, line: { color: "E2E8F0", width: 0.5 } });
  s.addText("Segmentation enables targeted interventions — not one-size-fits-all retention spend.", {
    x: 0.4, y: 5.1, w: 9.2, h: 0.35, fontSize: 10, italic: true, color: DGRAY, fontFace: "Calibri", align: "center", valign: "middle",
  });

  s.addNotes("The 2x2 segmentation matrix maps churn risk against customer value. This allows the business to deploy retention budget where it generates the highest ROI — saving high-value churners first.");
}

// ── SLIDE 9 — PRODUCTION DEPLOYMENT ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: OFFWHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("PRODUCTION DEPLOYMENT", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const panels = [
    {
      title: "REST API (FastAPI)", color: BLUE, x: 0.3, y: 1.05, w: 2.95,
      items: ["POST /score — score a single customer", "POST /score/batch — up to 1,000 customers", "GET /segments/summary — live stats", "GET /health — system status"],
    },
    {
      title: "Analytics Dashboard", color: GREEN, x: 3.55, y: 1.05, w: 2.95,
      items: ["KPI cards: customers, risk count, revenue at risk", "Churn score distribution chart", "Segment breakdown & spend vs risk plots", "Top 20 at-risk customers table"],
    },
    {
      title: "Model Monitoring", color: AMBER, x: 6.75, y: 1.05, w: 2.95,
      items: ["Drift detection across all 23 features", "Prediction logging with timestamps", "Automated drift reports per scoring run", "Baseline established from training data"],
    },
  ];

  panels.forEach(p => {
    card(s, p.x, p.y, p.w, 4.3, WHITE);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: p.x + 0.12, y: p.y + 0.12, w: p.w - 0.24, h: 0.45, fill: { color: p.color }, rectRadius: 0.08, line: { color: p.color, width: 0 } });
    s.addText(p.title, { x: p.x + 0.12, y: p.y + 0.12, w: p.w - 0.24, h: 0.45, fontSize: 10.5, bold: true, color: WHITE, fontFace: "Cambria", align: "center", valign: "middle", margin: 0 });
    p.items.forEach((item, j) => {
      const iy = p.y + 0.72 + j * 0.82;
      s.addShape(pres.shapes.OVAL, { x: p.x + 0.2, y: iy + 0.05, w: 0.16, h: 0.16, fill: { color: p.color }, line: { color: p.color, width: 0 } });
      s.addText(item, { x: p.x + 0.44, y: iy, w: p.w - 0.58, h: 0.7, fontSize: 9.5, color: DGRAY, fontFace: "Calibri", valign: "top" });
    });
  });

  s.addNotes("All three components are live. The API allows any downstream system to request a churn score in real time. The dashboard is used by the analytics team. The monitoring system alerts the team to data drift.");
}

// ── SLIDE 10 — TOP CHURN DRIVERS ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("WHAT DRIVES CHURN? — KEY INSIGHTS", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  // Bar chart — feature importance
  s.addChart(pres.charts.BAR, [{
    name: "Importance",
    labels: ["Days Inactive", "Trip Frequency", "Lifetime Spend", "Total Trips", "Churn Score"],
    values: [0.098, 0.448, 0.584, 1.035, 0.910],
  }], {
    x: 0.3, y: 1.0, w: 5.0, h: 3.5, barDir: "bar",
    chartColors: [LBLUE, LBLUE, BLUE, NAVY, RED],
    chartArea: { fill: { color: WHITE }, roundedCorners: true },
    catAxisLabelColor: DGRAY, valAxisLabelColor: GRAY,
    valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
    showValue: true, dataLabelColor: DGRAY, dataLabelFontSize: 9,
    showLegend: false, showTitle: true, title: "Feature Importance (Top 5)",
    titleColor: NAVY, titleFontSize: 11,
  });

  // Right — ranked list
  const drivers = [
    { rank: "1", label: "Churn Probability Score", note: "91% importance — strongest single predictor", color: RED },
    { rank: "2", label: "Total Trips Taken", note: "Low trip count = low platform commitment", color: NAVY },
    { rank: "3", label: "Lifetime Spend", note: "High spenders are more engaged, less likely to leave", color: BLUE },
    { rank: "4", label: "Trip Frequency (per week)", note: "Regular users stay; irregular users drift away", color: LBLUE },
    { rank: "5", label: "Days Inactive", note: "30+ days inactive = highest churn risk", color: AMBER },
  ];

  drivers.forEach((d, i) => {
    const y = 1.05 + i * 0.68;
    s.addShape(pres.shapes.OVAL, { x: 5.55, y: y + 0.04, w: 0.32, h: 0.32, fill: { color: d.color }, line: { color: d.color, width: 0 } });
    s.addText(d.rank, { x: 5.55, y: y + 0.04, w: 0.32, h: 0.32, fontSize: 10, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
    s.addText(d.label, { x: 6.0, y: y, w: 3.7, h: 0.25, fontSize: 10.5, bold: true, color: NAVY, fontFace: "Calibri" });
    s.addText(d.note, { x: 6.0, y: y + 0.27, w: 3.7, h: 0.28, fontSize: 9, color: GRAY, fontFace: "Calibri" });
  });

  // Recommendation box
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.3, y: 4.62, w: 9.4, h: 0.68, fill: { color: NAVY }, rectRadius: 0.08, line: { color: NAVY, width: 0 } });
  s.addText("Recommendation: Target customers with 0–5 trips AND 30+ days inactive with a personalised win-back offer within 48 hours of the inactivity trigger.", {
    x: 0.5, y: 4.62, w: 9.1, h: 0.68, fontSize: 10.5, color: WHITE, fontFace: "Calibri", valign: "middle", align: "center",
  });

  s.addNotes("The churn probability feature dominates because it encapsulates all behavioural signals into a single score. The next most important predictors are usage-based — how much and how often customers use the platform.");
}

// ── SLIDE 11 — BUSINESS IMPACT ────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: OFFWHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("BUSINESS IMPACT & ROI POTENTIAL", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  // 3 metric cards
  const metrics = [
    { label: "High-Risk Customers\nIdentified", value: "2,000", sub: "Flagged for immediate intervention", color: RED },
    { label: "Revenue Segments\nQuantified", value: "4", sub: "Spend prioritised per segment for targeted budget allocation", color: BLUE },
    { label: "Fraud Precision", value: "97%", sub: "Minimises false positives — less friction for legitimate customers", color: GREEN },
  ];

  metrics.forEach((m, i) => {
    const x = 0.3 + i * 3.15;
    card(s, x, 1.05, 3.05, 2.1, WHITE);
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.05, w: 3.05, h: 0.12, fill: { color: m.color }, line: { color: m.color, width: 0 } });
    s.addText(m.value, { x: x + 0.15, y: 1.22, w: 2.75, h: 0.7, fontSize: 36, bold: true, color: m.color, fontFace: "Cambria", align: "center" });
    s.addText(m.label, { x: x + 0.1, y: 1.9, w: 2.85, h: 0.45, fontSize: 10, bold: true, color: NAVY, fontFace: "Calibri", align: "center" });
    s.addText(m.sub, { x: x + 0.1, y: 2.38, w: 2.85, h: 0.65, fontSize: 9, color: GRAY, fontFace: "Calibri", align: "center" });
  });

  // Recommendations
  const recs = [
    { text: "A 10% improvement in retention of High Risk – High Value customers could recover significant recurring revenue — quantifiable via cohort analysis against historical LTV.", color: RED },
    { text: "Fraud model with ROC-AUC 0.982 enables near-perfect risk ranking — deployable directly in real-time payment approval flows to reduce fraud losses at scale.", color: BLUE },
  ];

  recs.forEach((rec, i) => {
    const y = 3.3 + i * 1.0;
    card(s, 0.3, y, 9.4, 0.85, WHITE);
    s.addShape(pres.shapes.OVAL, { x: 0.48, y: y + 0.32, w: 0.2, h: 0.2, fill: { color: rec.color }, line: { color: rec.color, width: 0 } });
    s.addText(rec.text, { x: 0.78, y: y + 0.08, w: 8.8, h: 0.7, fontSize: 10.5, color: DGRAY, fontFace: "Calibri", valign: "middle" });
  });

  s.addNotes("The business case is clear. 2,000 high-risk customers represent a significant revenue exposure. Even partial retention converts directly to recurring platform revenue. The fraud model can be wired directly into the payment approval pipeline.");
}

// ── SLIDE 12 — NEXT STEPS ─────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.9, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText("RECOMMENDED NEXT STEPS", { x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 20, bold: true, color: WHITE, fontFace: "Cambria", valign: "middle" });

  const steps = [
    { num: "01", title: "Deploy Churn API to Production", body: "Integrate FastAPI scoring endpoint with the CRM system to trigger automated, personalised retention outreach within 24 hours of a customer entering the High Risk tier.", color: RED, owner: "Data Engineering + CRM Team" },
    { num: "02", title: "Connect Fraud Model to Live Payments", body: "Wire the Random Forest fraud classifier into NovaPay's real-time transaction approval flow, enabling pre-authorisation scoring and dynamic blocking above a defined risk threshold.", color: AMBER, owner: "Payments Engineering" },
    { num: "03", title: "Run A/B Retention Campaign Test", body: "Design and execute a controlled A/B test across the 4 customer segments to measure incremental uplift from targeted retention interventions versus a holdout control group.", color: BLUE, owner: "Marketing + Analytics" },
    { num: "04", title: "Schedule Monthly Model Retraining", body: "Automate monthly model retraining triggered by the drift monitoring system. Retrain when feature distributions shift beyond the established threshold to maintain model accuracy over time.", color: GREEN, owner: "ML Engineering" },
  ];

  steps.forEach((step, i) => {
    const y = 1.05 + i * 1.08;
    card(s, 0.3, y, 9.4, 0.95, i % 2 === 0 ? WHITE : OFFWHITE);
    s.addShape(pres.shapes.OVAL, { x: 0.42, y: y + 0.2, w: 0.55, h: 0.55, fill: { color: step.color }, line: { color: step.color, width: 0 } });
    s.addText(step.num, { x: 0.42, y: y + 0.2, w: 0.55, h: 0.55, fontSize: 13, bold: true, color: WHITE, fontFace: "Cambria", align: "center", valign: "middle", margin: 0 });
    s.addText(step.title, { x: 1.1, y: y + 0.06, w: 5.6, h: 0.3, fontSize: 11, bold: true, color: NAVY, fontFace: "Calibri" });
    s.addText(step.body, { x: 1.1, y: y + 0.38, w: 5.6, h: 0.5, fontSize: 9, color: DGRAY, fontFace: "Calibri" });
    // Owner tag
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.0, y: y + 0.3, w: 2.55, h: 0.3, fill: { color: step.color, transparency: 80 }, rectRadius: 0.06, line: { color: step.color, width: 0 } });
    s.addText(step.owner, { x: 7.0, y: y + 0.3, w: 2.55, h: 0.3, fontSize: 8, color: step.color, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
  });

  s.addNotes("These four actions are prioritised by business impact. Steps 1 and 2 convert the models into revenue protection immediately. Steps 3 and 4 ensure we learn from deployment and maintain model quality over time.");
}

// ── SLIDE 13 — THANK YOU ──────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  s.addShape(pres.shapes.OVAL, { x: 6.5, y: -1.5, w: 5.5, h: 5.5, fill: { color: BLUE, transparency: 75 }, line: { color: BLUE, width: 0 } });
  s.addShape(pres.shapes.OVAL, { x: -1.5, y: 2.5, w: 4.5, h: 4.5, fill: { color: LBLUE, transparency: 82 }, line: { color: LBLUE, width: 0 } });

  s.addText("Thank You", { x: 1, y: 1.1, w: 8, h: 1.1, fontSize: 44, bold: true, color: WHITE, fontFace: "Cambria", align: "center" });

  s.addShape(pres.shapes.RECTANGLE, { x: 3.5, y: 2.32, w: 3.0, h: 0.05, fill: { color: LBLUE }, line: { color: LBLUE, width: 0 } });

  s.addText("Questions & Discussion", { x: 1, y: 2.5, w: 8, h: 0.5, fontSize: 18, color: "CADCFC", fontFace: "Calibri", align: "center" });

  s.addText("Sunday Monday Igbone", { x: 1, y: 3.4, w: 8, h: 0.38, fontSize: 14, bold: true, color: WHITE, fontFace: "Calibri", align: "center" });
  s.addText("Data Science Intern  ·  Amdari", { x: 1, y: 3.8, w: 8, h: 0.3, fontSize: 11, color: "94A3B8", fontFace: "Calibri", align: "center" });
  s.addText("otachesunday226@gmail.com", { x: 1, y: 4.12, w: 8, h: 0.3, fontSize: 11, color: "94A3B8", fontFace: "Calibri", align: "center" });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.5, y: 4.65, w: 7.0, h: 0.6, fill: { color: BLUE, transparency: 70 }, rectRadius: 0.1, line: { color: BLUE, width: 0 } });
  s.addText("Built with  Python  ·  Scikit-learn  ·  XGBoost  ·  LightGBM  ·  FastAPI  ·  Streamlit  ·  Plotly", {
    x: 1.5, y: 4.65, w: 7.0, h: 0.6, fontSize: 9, color: "CADCFC", fontFace: "Calibri", align: "center", valign: "middle",
  });

  s.addNotes("Thank you. I am happy to take any questions on the methodology, the feature engineering choices, the model selection, or the deployment architecture.");
}

// ── Save ──────────────────────────────────────────────────────────────────────
const outPath = "C:/Users/User/Desktop/DATA LEARN/Amdari/Data Analysis/week 1/Customer-Analytics-and-Churn-Prediction/Customer-Analytics-and-Churn-Prediction-1/Customer_Churn_Analytics_Presentation.pptx";

pres.writeFile({ fileName: outPath }).then(() => {
  console.log("Presentation saved:", outPath);
}).catch(err => {
  console.error("Error:", err);
});
