import express from "express";
import path from "path";
import fs from "node:fs";
import { fileURLToPath } from "url";
import { dirname } from "path";
import { parseGPXWithCustomParser } from "@we-gold/gpxjs";
import { DOMParser } from "xmldom-qsa";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const customParseMethod = (txt) => {
  return new DOMParser().parseFromString(txt, "text/xml");
};

const app = express();

app.get("/", (_, res) => {
  res.send("Wello world !");
});

app.get("/gpx/split", async (_, res) => {
  const data = await fs.readFileSync(path.resolve(__dirname, "./gr38.gpx"), "utf8");
  if (data) {
    const [gpx, error] = parseGPXWithCustomParser(data, customParseMethod);
    if (error) throw error;
    const totalDistance = gpx.tracks[0].distance.total
    console.log(totalDistance);
  }
  res.send("OK");
});

export default app;
