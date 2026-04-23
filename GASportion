#### This is going to be over the course of multiple files. The only issue I ran into is adding multiple files to the GitHub branch. 

*Apps Scrips supports multiple .gs files. What I include will mirror that structure.
 
*In the meantime, I will use the following format to put multiple .gs files into one Google Apps Script file.

*For each .gs file will have a title followed w/ code such that:
	“main.gs”
	Followed by some code

*PS. I know not everything in the code follows the same format (more specifically the comments), I will work/update on making everything in the code consistent. I tried to refactor as much as I can, but there’s always room for improvement. 

PSS Regarding the part two of this project, we can implement a Google Calendar API to implement scheduling into this code too. 

###



MAIN.gs

/// CSC 131 - PIT CREW - Ethan Willform 
/// This portion of the project is programmed in JAVASCRIPT Utilzing GOOGLE APPS SCRIPT
/// !! IMPORTANT !! 
/// YOU WILL HAVE TO RUN THIS WITHIN THE "AHA SIGNUPS" GOOGLE SHEETS which will be shared in the project drive


/// keeping queued emails at 10 and aha emails at 1 as a tester. This will change once we get access to main account. 

/// *NOTE* The email funcs are subject to change due to Ethan M's Email Task. 

function main() {
  const aha = pollAhaEmails_();
  const queued = queueRegistrationEmails_();
  const sent = sendQueuedEmails_(10);
  refreshDashboard(); 
  applyStatusFormatting();
  SpreadsheetApp.getActive().toast(`Main done → AHA:${aha}, queued:${queued}, sent:${sent}`);
};
function sendOneEmail() {
  return sendQueuedEmails_(1);
}

function runPipeline() {
  main();
};


CONSTS.gs

/// constants for SHEET,STATUS,and PAY used to simplify in sheet. 

const SHEET = {
  CONFIG: "Config",
  AHA_INBOX: "AHA_INBOX",
  ENROLL: "Enrollments",
  OUTBOX: "Email_outbox"
};

const STATUS = {
  AWAITING_DETAILS: "AWAITING_STUDENT_DETAILS",
  READY_TO_EMAIL: "READY_TO_EMAIL",
  EMAIL_QUEUED: "EMAIL_QUEUED",
  EMAIL_SENT: "EMAIL_SENT",
  ERROR: "ERROR",
};

const PAY = {
  UNKNOWN: "UNKNOWN",
  UNPAID: "UNPAID",
  PAID: "PAID",
};


utilities.gs

function ensureSheet_(name, headers) {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);

  if (sh.getLastRow() === 0 && headers?.length) {
    sh.getRange(1, 1, headers.length, headers[0].length).setValues(headers);
  }
}

function getConfig_(key) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.CONFIG);
  if (!sh) throw new Error(`Missing sheet: ${SHEET.CONFIG}`);

  const rows = sh.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === key) return String(rows[i][1] ?? "");
  }
  return "";
}

function setConfigIfMissing_(key, value) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.CONFIG);
  if (!sh) throw new Error(`Missing sheet: ${SHEET.CONFIG}`);

  const rows = sh.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === key) return;
  }
  sh.appendRow([key, value]);
}

function appendRow_(sheetName, row) {
  const sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  if (!sh) throw new Error(`Missing sheet: ${sheetName}`);
  sh.appendRow(row);
}

function readTable_(sheetName) {
  const sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  if (!sh) throw new Error(`Missing sheet: ${sheetName}`);

  const values = sh.getDataRange().getValues();
  if (values.length < 1) throw new Error(`Sheet ${sheetName} missing header row`);

  const header = values[0].map(h => String(h).trim());
  const rows = values.slice(1).map(row => {
    const obj = {};
    header.forEach((h, i) => obj[h] = row[i]);
    return obj;
  });

  return { sh, values, header, rows };
}

function updateRowById_(table, id, patch, idColName) {
  const header = table.header;
  const values = table.values;
  const sh = table.sh;

  const idIdx = header.indexOf(idColName);
  if (idIdx === -1) throw new Error(`Missing id column: ${idColName}`);

  for (let r = 1; r < values.length; r++) {
    if (String(values[r][idIdx]) === String(id)) {
      for (const k in patch) {
        const c = header.indexOf(k);
        if (c !== -1) values[r][c] = patch[k];
      }
      sh.getRange(r + 1, 1, 1, header.length).setValues([values[r]]);
      return;
    }
  }
}

function renderTemplate_(tpl, vars) {
  let out = String(tpl || "");
  for (const k in vars) out = out.replaceAll(`{{${k}}}`, String(vars[k]));
  return out;
}


/// * NOTE * THIS IS SUBJECT TO CHANGE DUE TO ETHAN M's EMAIL TASK/ALG

emailOutbox.gs

function queueRegistrationEmails_() {
  const enroll = readTable_(SHEET.ENROLL);
  let queued = 0;

  for (const r of enroll.rows) {
    if (r.pipelineStatus !== STATUS.READY_TO_EMAIL) continue;

    const to = String(r.Email || "").trim();
    if (!to) continue;

    const subject = getConfig_("REG_EMAIL_SUBJECT");
    const link = getConfig_("REG_LINK");
    const tpl = getConfig_("REG_EMAIL_TEMPLATE");

    const body = renderTemplate_(tpl, {
      firstName: r.FirstName || "there",
      link,
    });

    appendRow_(SHEET.OUTBOX, [
      Utilities.getUuid(), // emailId
      r.recordId,          // recordId FK
      to,                  // TO
      subject,
      body,
      "QUEUED",
      new Date(),          // queuedAt
      "",                  // sentAt
      "",                  // error
    ]);

    // Move enrollment forward
  updateRowById_(enroll, r.recordId, {
      pipelineStatus: STATUS.EMAIL_QUEUED,
      UpdatedAt: new Date(),
    }, "recordId");

    queued++;
  }

  SpreadsheetApp.getActive().toast(`Queued emails: ${queued}`);
  return queued;
}


function sendQueuedEmails_(maxToSend) {
  const enabled = String(getConfig_("SEND_EMAILS_ENABLED")).toUpperCase() === "TRUE";
  if (!enabled) {
    SpreadsheetApp.getActive().toast("SEND_EMAILS_ENABLED is FALSE (no emails sent)");
    return 0;
  }

  const out = readTable_(SHEET.OUTBOX);
  let sent = 0;

  for (const r of out.rows) {
    if (sent >= maxToSend) break;
    if (r.Status !== "QUEUED") continue;

    try {
      GmailApp.sendEmail(r.TO, r.Subject, r.BODY);

      updateRowById_(out, r.emailId, {
        Status: "SENT",
        sentAt: new Date(),
        error: "",
      }, "emailId");

      markEnrollmentEmailed_(r.recordId);
      sent++;
    } catch (e) {
      updateRowById_(out, r.emailId, {
        Status: "ERROR",
        error: String(e),
      }, "emailId");
    }
  }

  SpreadsheetApp.getActive().toast(`Sent emails: ${sent}`);
  return sent;
}

function markEnrollmentEmailed_(recordId) {
  const enroll = readTable_(SHEET.ENROLL);
  updateRowById_(enroll, recordId, {
    pipelineStatus: STATUS.EMAIL_SENT,
    RegistrationEmailSentAt: new Date(),
    UpdatedAt: new Date(),
  }, "recordId");
}



AHAintake.gs

function pollAhaEmails_() {
// 1) Scans the Gmail query from Config
  const query = getConfig_("AHA_GMAIL_QUERY");
  if (!query) throw new Error("Missing Config key AHA_GMAIL_QUERY");

// 2) Searches through Gmail for matching threads/messages
  const threads = GmailApp.search(query, 0, 20);
  let processed = 0;

  for (const thread of threads) {
    for (const msg of thread.getMessages()) {
      const messageId = msg.getId();

    // 3) Skips if we already processed this message
      if (ahaMessageAlreadyLogged_(messageId)) continue;

      const body = msg.getPlainBody() || "";

    // 4) Log the raw email into AHA_INBOX
      appendRow_(SHEET.AHA_INBOX, [
        messageId,                        // messageID
        msg.getDate(),                    // receivedAt
        msg.getSubject(),                 // subject
        body.slice(0, 200),               // snippet
        new Date(),                       // processedAt
      ]);

    // 5) Extract identity if possible
      const fullName = extractNameFromLabel_(body);
      const nameParts = splitFirstLast_(fullName);
      const email = extractEmail_(body);

    // If we got an email, we can advance them to READY_TO_EMAIL automatically
      const pipelineStatus = email ? STATUS.READY_TO_EMAIL : STATUS.AWAITING_DETAILS;

    // 6) Creates corresponding rows in Enrollments
      const now = new Date();
      appendEnrollmentRow_({
        "recordId": Utilities.getUuid(),
        "pipelineStatus": pipelineStatus,
        "ahaMessageID": messageId,
        "acuityMessageID": "",
        "locationName": "",
        "FirstName": nameParts.first,
        "LastName": nameParts.last,
        "Email": email,
        "PaymentStatus": PAY.UNKNOWN,
        "RegistrationEmailSentAt": "",
        "PaidAt": "",
        "CreatedAt": now,
        "UpdatedAt": now,
      });

      processed++;
    }
  }

  SpreadsheetApp.getActive().toast(`AHA intake processed: ${processed}`);
  return processed;
}

/**
 * !!dupe prevention!!
 * Returns true if there's a Gmail messageId already in AHA_INBOX column A.
 */
function ahaMessageAlreadyLogged_(messageId) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.AHA_INBOX);
  if (!sh) throw new Error(`Missing sheet: ${SHEET.AHA_INBOX}`);

  const last = sh.getLastRow();
  if (last < 2) return false;

// Looks back up to last 300 emails , we can adjust according to business email/data if we ever get the login.
  const start = Math.max(2, last - 300);
  const ids = sh.getRange(start, 1, last - start + 1, 1).getValues().flat();

  return ids.includes(messageId);
}

/**
 * adds one enrollment row by mapping object keys to sheet headers.
 */
function appendEnrollmentRow_(obj) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.ENROLL);
  if (!sh) throw new Error(`Missing sheet: ${SHEET.ENROLL}`);

  const headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  const row = headers.map(h => obj[h] ?? "");
  sh.appendRow(row);
}

/**
 * Extracts the first email-looking string from the text.
 */
function extractEmail_(text) {
  const m = String(text || "").match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i);
  return m ? m[0].trim() : "";
}

/**
 * Extracts a name from a line like:
 *   Name: John Doe
 * If it doesn't exist, returns "".
 */
function extractNameFromLabel_(text) {
  const m = String(text || "").match(/Name\s*:\s*([^\n\r]+)/i);
  return m ? m[1].trim() : "";
}

/**
 * Splits a full name into first + last.
 * From "John Doe" to {first:"John", last:"Doe"}
 * From "Joe" to {first:"Joe", last:""}
 */
function splitFirstLast_(fullName) {
  const parts = String(fullName || "").trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return { first: "", last: "" };
  if (parts.length === 1) return { first: parts[0], last: "" };
  return { first: parts[0], last: parts[parts.length - 1] };
}


setup.gs

function setupProject() {
  ensureSheet_(SHEET.CONFIG, [["KEY", "VALUE"]]);

/// To test it out, I can potentially put my email, but I am not going to for the time being. 

/// This is fine if you send yourself "AHA Enrollment" emails.
  setConfigIfMissing_("AHA_GMAIL_QUERY", 'subject:("AHA Enrollment") newer_than:14d');

  setConfigIfMissing_("REG_EMAIL_SUBJECT", "Complete your registration");
  setConfigIfMissing_("REG_LINK", "https://ahasso.heart.org/");
  setConfigIfMissing_("REG_EMAIL_TEMPLATE",
    "Hi {{firstName}},\n\nPlease complete your registration here:\n{{link}}\n\nThanks!"
  );

/// Safety switch: set TRUE only when you want to actually send email, could break if set to true .
  setConfigIfMissing_("SEND_EMAILS_ENABLED", "FALSE");

  SpreadsheetApp.getActive().toast("Setup complete (check Config).");
}



dashboard.gs

/**
 * ######################
 * This is the backend of the dashboard tab
 * ######################
 */

function refreshDashboard() {
  const ss = SpreadsheetApp.getActive();
  const dashName = "MAIN";
  let dash = ss.getSheetByName(dashName);
  if (!dash) dash = ss.insertSheet(dashName);

  const enroll = readTable_(SHEET.ENROLL);
  const out = readTable_(SHEET.OUTBOX);

  const countBy = (rows, key) => {
    const m = {};
    for (const r of rows) {
      const k = String(r[key] ?? "").trim() || "(blank)";
      m[k] = (m[k] || 0) + 1;
    }
    return m;
  };

  const byStatus = countBy(enroll.rows, "pipelineStatus");
  const byOutStatus = countBy(out.rows, "Status");

  dash.clear();

  const lines = [];
  lines.push(["Metric", "Value"]);
  lines.push(["Last refreshed", new Date()]);
  lines.push(["Total enrollments", enroll.rows.length]);
  lines.push(["--- Enrollment Status Counts ---", ""]);
  for (const k of Object.keys(byStatus).sort()) lines.push([k, byStatus[k]]);
  lines.push(["--- Email Outbox Status Counts ---", ""]);
  for (const k of Object.keys(byOutStatus).sort()) lines.push([k, byOutStatus[k]]);

  dash.getRange(1, 1, lines.length, 2).setValues(lines);
  dash.autoResizeColumns(1, 2);

  SpreadsheetApp.getActive().toast("Dashboard refreshed");
}


formatting.gs
function applyStatusFormatting() {
  const ss = SpreadsheetApp.getActive();
  const sh = ss.getSheetByName(SHEET.ENROLL);
  if (!sh) throw new Error(`Missing sheet: ${SHEET.ENROLL}`);

  const header = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  const statusCol = header.indexOf("pipelineStatus") + 1;
  if (statusCol < 1) throw new Error("Enrollments missing pipelineStatus column");

  const range = sh.getRange(2, statusCol, Math.max(1, sh.getLastRow() - 1), 1);
  const rules = [];

  const makeRule = (text, bg) =>
    SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(text)
      .setBackground(bg)
      .setRanges([range])
      .build();

  rules.push(makeRule(STATUS.AWAITING_DETAILS, "#E0E0E0")); /// gray
  rules.push(makeRule(STATUS.READY_TO_EMAIL, "#BBDEFB")); /// light blue
  rules.push(makeRule(STATUS.EMAIL_QUEUED, "#FFF9C4")); /// light yellow
  rules.push(makeRule(STATUS.EMAIL_SENT, "#C8E6C9")); /// light green
  rules.push(makeRule(STATUS.ERROR, "#FFCDD2")); /// light red

  sh.setConditionalFormatRules(rules);
  SpreadsheetApp.getActive().toast("Status formatting applied");
}
