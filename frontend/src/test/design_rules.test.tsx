import { describe, it, expect } from "vitest";
import fs from "fs";
import path from "path";

describe("Phase 01 Design Rules and Compliance Audit", () => {
  it("verifies index.html references the custom SVG favicon", () => {
    const htmlPath = path.resolve(__dirname, "../../index.html");
    const htmlContent = fs.readFileSync(htmlPath, "utf-8");
    expect(htmlContent).toMatch(/<link\s+[^>]*href="\/favicon\.svg"[^>]*\/>/);
  });

  it("verifies custom SVG favicon file exists and is not empty", () => {
    const faviconPath = path.resolve(__dirname, "../../public/favicon.svg");
    expect(fs.existsSync(faviconPath)).toBe(true);
    const svg = fs.readFileSync(faviconPath, "utf-8");
    expect(svg).toContain("<svg");
    expect(svg).toContain("</svg>");
    // verify no purple in favicon
    expect(svg.toLowerCase()).not.toContain("purple");
  });

  it("verifies zero em dash characters (U+2014) in frontend source files", () => {
    const srcDir = path.resolve(__dirname, "..");
    const filesToScan: string[] = [];

    const walkSync = (dir: string) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          walkSync(fullPath);
        } else if (/\.(ts|tsx|css|html)$/.test(entry.name)) {
          filesToScan.push(fullPath);
        }
      }
    };

    walkSync(srcDir);

    const violations: { file: string; line: number }[] = [];
    for (const filePath of filesToScan) {
      const content = fs.readFileSync(filePath, "utf-8");
      const lines = content.split("\n");
      lines.forEach((line, index) => {
        if (line.includes("\u2014")) {
          violations.push({ file: path.relative(srcDir, filePath), line: index + 1 });
        }
      });
    }

    expect(violations).toEqual([]);
  });

  it("verifies zero prohibited AI badges in frontend source files", () => {
    const srcDir = path.resolve(__dirname, "..");
    const filesToScan: string[] = [];

    const walkSync = (dir: string) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && entry.name !== "test") {
          walkSync(fullPath);
        } else if (/\.(ts|tsx)$/.test(entry.name) && !dir.includes("test")) {
          filesToScan.push(fullPath);
        }
      }
    };

    walkSync(srcDir);

    const violations: string[] = [];
    for (const filePath of filesToScan) {
      const content = fs.readFileSync(filePath, "utf-8");
      if (/Made with AI/i.test(content) || /Powered by AI/i.test(content)) {
        violations.push(path.relative(srcDir, filePath));
      }
    }

    expect(violations).toEqual([]);
  });

  it("verifies no purple gradients or generic gradients in frontend styling", () => {
    const srcDir = path.resolve(__dirname, "..");
    const filesToScan: string[] = [];

    const walkSync = (dir: string) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && entry.name !== "test") {
          walkSync(fullPath);
        } else if (/\.(ts|tsx|css)$/.test(entry.name) && !dir.includes("test")) {
          filesToScan.push(fullPath);
        }
      }
    };

    walkSync(srcDir);

    const violations: string[] = [];
    for (const filePath of filesToScan) {
      const content = fs.readFileSync(filePath, "utf-8");
      if (
        /from-purple/i.test(content) ||
        /to-purple/i.test(content) ||
        /via-purple/i.test(content) ||
        /bg-gradient/i.test(content)
      ) {
        violations.push(path.relative(srcDir, filePath));
      }
    }

    expect(violations).toEqual([]);
  });
});
