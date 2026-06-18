// ============================================================
//  ChatOnline — Visitor Tracker
//  Google Apps Script Webhook
//  Paste this into Extensions → Apps Script in your Sheet
//  Then: Deploy → New Deployment → Web App → Anyone → Deploy
// ============================================================

const SHEET_NAME = "Visitors"; // Tab name in your Google Sheet

function doPost(e) {
  try {
    const sheet = getOrCreateSheet();
    const data  = JSON.parse(e.postData.contents);

    // Append one row per visitor
    sheet.appendRow([
      data.timestamp   || new Date().toISOString(),
      data.ip          || "—",
      data.city        || "—",
      data.region      || "—",
      data.country     || "—",
      data.isp         || "—",
      data.lat         || "—",
      data.lon         || "—",
      data.gpsLat      || "—",
      data.gpsLon      || "—",
      data.deviceType  || "—",
      data.os          || "—",
      data.browser     || "—",
      data.screen      || "—",
      data.language    || "—",
      data.referrer    || "Direct",
      data.ua          || "—",
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle CORS preflight (GET ping)
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ChatOnline tracker active" }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Get existing sheet tab or create it with headers
function getOrCreateSheet() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  let   sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      "Timestamp", "IP Address", "City", "Region", "Country",
      "ISP / Org", "IP Latitude", "IP Longitude",
      "GPS Latitude", "GPS Longitude",
      "Device Type", "Operating System", "Browser",
      "Screen Resolution", "Language", "Referrer", "User-Agent"
    ]);

    // Style the header row
    const header = sheet.getRange(1, 1, 1, 17);
    header.setBackground("#1a1a18");
    header.setFontColor("#c9a84c");
    header.setFontWeight("bold");
    sheet.setFrozenRows(1);
  }

  return sheet;
}
