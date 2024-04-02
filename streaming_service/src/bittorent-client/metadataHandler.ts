"use strict";
import * as fs from "fs/promises";
// import fs from "fs";
import https from "https";
import bencode from "bencode";
import * as ttypes from "./ft_torrent_types.js";
import parseTorrent, { toMagnetURI } from "parse-torrent";
import path from "path";
function generatePath(torrentUrl: string): string {
  const splitedUrl: string[] = torrentUrl.split("/");
  return `./torrents/metadata/${splitedUrl[splitedUrl.length - 1].toLowerCase()}.torrent`;
}

function filterNonHtppTrackers(trackers: string[][]): string[][] {
  const httpTrackers: string[][] = [];

  for (let i = 0; i < trackers.length; i++) {
    const tracker: string[] = trackers[i].filter((t: string) => t.startsWith("http"));
    if (tracker.length > 0) {
      httpTrackers.push(tracker);
    }
  }

  return httpTrackers;
}

function normalizeTorrentMeta(decodedMetadata: any, originalMetaData: any): ttypes.TorrentMeta {
  const torrentMetaData = {} as ttypes.TorrentMeta;
  const info = {} as ttypes.Info;
  // Determine if the .torrent file have one or multiples files
  if (Object.prototype.hasOwnProperty.call(decodedMetadata?.info, "length")) {
    const file: ttypes.SingleFileMode = {
      name: decodedMetadata?.info?.name,
      length: decodedMetadata?.info?.length,
      md5sum: decodedMetadata?.info?.md5sum,
    };

    info.file = file;
  } else if (Object.prototype.hasOwnProperty.call(decodedMetadata?.info, "files")) {
    const file: ttypes.MultiFileMode = {
      name: decodedMetadata?.info?.name,
      files: decodedMetadata?.info?.files.map((rawFile: any) => ({
        length: rawFile?.length,
        path: rawFile?.length,
        md5sum: rawFile?.md5sum,
      })),
    };
    info.file = file;
  } else {
    throw new Error("Torrent type unhandled");
  }

  info.pieceLength = decodedMetadata?.info["piece length"];
  info.pieces = originalMetaData.pieces;
  info.piecesBuffer = originalMetaData.info.pieces;
  info.private = parseInt(decodedMetadata?.info?.private, 10) === 1 ? true : false;

  torrentMetaData.announce = decodedMetadata.announce;
  torrentMetaData.announceList = decodedMetadata["announce-list"];

  if (torrentMetaData.announceList) {
    torrentMetaData.announceList = filterNonHtppTrackers(torrentMetaData.announceList);
  }

  if (torrentMetaData.announce.toLowerCase().startsWith("udp")) {
    torrentMetaData.announce = torrentMetaData?.announceList[0][0];
  }

  torrentMetaData.createdBy = decodedMetadata["created by"];
  torrentMetaData.creationDate = decodedMetadata["creation date"];
  torrentMetaData.encoding = decodedMetadata?.encoding;
  torrentMetaData.comment = decodedMetadata?.comment;
  torrentMetaData.info = info;
  torrentMetaData.infoHashHex = originalMetaData.infoHash;
  torrentMetaData.infoHash = originalMetaData.infoHashBuffer;

  return torrentMetaData;
}

export async function downloadTorrentMeta(torrentUrl: string): Promise<string> {
  const path = generatePath(torrentUrl);

  return new Promise((resolve, reject) => {
    https.get(torrentUrl, (response) => {
      response.on("data", (chunk) => {
        fs.appendFile(path, chunk);
      });

      response.on("end", () => {
        resolve(path);
      });

      response.on("error", (err: Error) => {
        reject(err.message);
      });
    });
  });
}
function announceToMagnet(announce: string[]): string {
  let announceUrl = "";
  for (const tracker of announce) {
    announceUrl = announceUrl.concat(`&tr=${encodeURI(tracker)}`);
  }
  return announceUrl;
}

// TODO change meta for the type of the metadata Object (result of: parseTorrent(bytes))
export function generateMagnetURI(meta: any, source: string): string {
  const magnetURI = toMagnetURI({
    infoHash: meta.infoHash,
  });
  return `${magnetURI}&dn=${encodeURI(meta.name)}${announceToMagnet(meta.announce)}&xs=${encodeURI(source)}`;
}
export async function parseTorrentMeta(torrentPath: string) {
  try {
    const torrent = await fs.readFile(torrentPath);
    const parsed = await parseTorrent(torrent);
    return parsed;
  } catch (error) {
    console.error(error.message);
  }
}

// export async function deleteTorrentMeta(torrentPath: string) {
//   await fs.unlink(torrentPath);
// }
