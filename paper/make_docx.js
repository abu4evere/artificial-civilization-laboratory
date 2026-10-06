// Convert paper/draft.md into a Word document (paper/draft.docx) with academic formatting.
//   cd paper/.tools && npm install docx      (once; the folder is kept out of git)
//   node paper/make_docx.js
// Handles the markdown this draft uses: headings, paragraphs, **bold**, *italic*, `code`, [links](url), bullet and
// numbered lists, pipe tables, ![figures](file.png) and horizontal rules.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, ImageRun, ExternalHyperlink, Footer, PageNumber, LevelFormat,
} = require(path.join(__dirname, ".tools", "node_modules", "docx"));

const HERE = __dirname;
const SRC = path.join(HERE, "draft.md");
const OUT = path.join(HERE, "draft.docx");
const FONT = "Times New Roman";
const BODY = 22;            // half-points: 11 pt
const TEXT_WIDTH = 9026;    // A4 with 1-inch margins, in DXA

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// Inline markdown -> runs
function inline(text, base = {}) {
  const out = [];
  const re = /(\*\*([^*]+)\*\*)|(\*([^*]+)\*)|(`([^`]+)`)|(\[([^\]]+)\]\(([^)]+)\))/g;
  let last = 0, m;
  const run = (t, extra = {}) => new TextRun({ text: t, font: FONT, size: base.size || BODY, ...base, ...extra });
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(run(text.slice(last, m.index)));
    if (m[2] !== undefined) out.push(...inline(m[2], { ...base, bold: true }));
    else if (m[4] !== undefined) out.push(...inline(m[4], { ...base, italics: !base.italics }));
    else if (m[6] !== undefined) out.push(run(m[6], { font: "Consolas", size: (base.size || BODY) - 2 }));
    else if (m[8] !== undefined) {
      out.push(new ExternalHyperlink({ link: m[9], children: [run(m[8], { style: "Hyperlink" })] }));
    }
    last = re.lastIndex;
  }
  if (last < text.length) out.push(run(text.slice(last)));
  return out;
}

function para(text, opts = {}) {
  return new Paragraph({ children: inline(text, opts.run || {}), spacing: { after: 120, line: 276 },
    alignment: opts.align || AlignmentType.JUSTIFIED, ...opts.p });
}

function table(rows) {
  const cells = rows.map(r => r.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(c => c.trim()));
  const head = cells[0];
  const body = cells.slice(2);
  const n = head.length;
  const widths = Array(n).fill(Math.floor(TEXT_WIDTH / n));
  widths[n - 1] += TEXT_WIDTH - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
  const borders = { top: border, bottom: border, left: border, right: border };
  const mk = (row, header) => new TableRow({
    tableHeader: header,
    children: row.map((c, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA }, borders,
      shading: header ? { type: ShadingType.CLEAR, fill: "E8E8E8", color: "auto" } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({ children: inline(c, { size: 18, bold: header || undefined }),
        alignment: AlignmentType.LEFT })],
    })),
  });
  return new Table({ width: { size: TEXT_WIDTH, type: WidthType.DXA }, columnWidths: widths,
    rows: [mk(head, true), ...body.map(r => mk(r, false))] });
}

const lines = fs.readFileSync(SRC, "utf8").replace(/\r\n/g, "\n").split("\n");
const children = [];
let i = 0;
let first = true;
while (i < lines.length) {
  const line = lines[i];
  if (!line.trim()) { i++; continue; }
  if (/^---\s*$/.test(line)) {
    children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "BBBBBB", space: 1 } },
      spacing: { after: 200 } }));
    i++; continue;
  }
  let m;
  if ((m = line.match(/^(#{1,3}) (.*)$/))) {
    const level = m[1].length;
    if (level === 1 && first) {
      children.push(new Paragraph({ children: inline(m[2], { size: 32, bold: true }), alignment: AlignmentType.CENTER,
        spacing: { after: 240 } }));
      first = false;
    } else {
      children.push(new Paragraph({ heading: level <= 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
        children: inline(m[2], { size: level <= 2 ? 26 : 23, bold: true, color: "000000" }),
        spacing: { before: 280, after: 120 }, keepNext: true }));
    }
    i++; continue;
  }
  if ((m = line.match(/^!\[([^\]]*)\]\(([^)]+)\)/))) {
    const file = path.join(HERE, m[2]);
    const { w, h } = pngSize(file);
    const width = 600;                                    // pixels at 96 dpi, about 15.9 cm
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data: fs.readFileSync(file),
        transformation: { width, height: Math.round(width * h / w) }, altText: { title: m[1], description: m[1], name: m[1] } })] }));
    i++; continue;
  }
  if (line.startsWith("|")) {
    const rows = [];
    while (i < lines.length && lines[i].startsWith("|")) rows.push(lines[i++]);
    children.push(table(rows));
    children.push(new Paragraph({ spacing: { after: 120 } }));
    continue;
  }
  if ((m = line.match(/^(\s*)(- |\d+\. )(.*)$/))) {
    const numbered = /\d/.test(m[2]);
    let text = m[3];
    i++;
    while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*(- |\d+\. )/.test(lines[i])) {
      text += " " + lines[i].trim(); i++;
    }
    children.push(new Paragraph({ children: inline(text), spacing: { after: 80, line: 276 },
      numbering: { reference: numbered ? "numbers" : "bullets", level: 0 } }));
    continue;
  }
  // paragraph: join until blank line or a block start
  let text = line.trim();
  i++;
  while (i < lines.length && lines[i].trim() && !/^(#{1,3} |\||- |\d+\. |!\[|---\s*$)/.test(lines[i].trim())) {
    text += " " + lines[i].trim(); i++;
  }
  const caption = /^\*(Figure|Table) \d/.test(text);
  children.push(para(text, caption ? { run: { size: 20 }, align: AlignmentType.LEFT, p: { spacing: { after: 200 } } } : {}));
}

const doc = new Document({
  creator: "Abdurashid Khudoyberdiev",
  title: "Failed pairing, not hunger: why small simulated forager populations die out",
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log(`wrote ${path.relative(path.dirname(HERE), OUT)}`); });
