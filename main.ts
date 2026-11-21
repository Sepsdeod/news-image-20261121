// news-image-20261121 entrypoint (Node 22, standard library only).
//
// The entry image is the entry.png shipped beside this file; the program
// copies it to the grader's output directory. It runs with no network and
// writes the same bytes on every run.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));
writeFileSync(join(outDir, "entry.png"), bytes);
