#### This is going to be over the course of multiple files. The only issue I ran into is adding multiple files to the GitHub branch. 

*Apps Scrips supports multiple .gs files. What I include will mirror that structure.
 
*In the meantime, I will use the following format to put multiple .gs files into one Google Apps Script file.

*For each .gs file will have a title followed w/ code such that:
	“main.gs”
	Followed by some code

*PS. I know not everything in the code follows the same format (more specifically the comments), I will work/update on making everything in the code consistent. I tried to refactor as much as I can, but there’s always room for improvement. 

PSS Regarding the part two of this project, we can implement a Google Calendar API to implement scheduling into this code too. 

###


// CSC 131 - PIT CREW - Ethan Willform 
// This portion of the project is programmed in JAVASCRIPT Utilzing GOOGLE APPS SCRIPT
// !! IMPORTANT !! 
// YOU WILL HAVE TO RUN THIS WITHIN THE "AHA SIGNUPS" GOOGLE SHEETS which will be shared in the project drive

Main.gs File

function main() {
  const processed = pollAhaEmails_();

  SpreadsheetApp.getActive().toast(`Processed: ${processed}`);
}


CONSTS.gs File
/// constants for SHEET,STATUS used to simplify in sheet. 

const SHEET = {
  CONFIG: "Config",
  AHA_INBOX: "AHA_INBOX",
  ENROLL: "Enrollments",
};

utilities.gs


function getConfig_(key) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.CONFIG);
  const rows = sh.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === key) return String(rows[i][1] ?? "");
  }
  return "";
}

function appendRow_(sheetName, row) {
  const sh = SpreadsheetApp.getActive().getSheetByName(sheetName);
  sh.appendRow(row);
}

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



AHAintake.gs Files 

function pollAhaEmails_() {
  const query = "newer_than:1d";
  const threads = GmailApp.search(query, 0, 20);

  let processed = 0

  for (const thread of threads) {
    for (const msg of thread.getMessages()) {

      const messageId = msg.getId();
      if (alreadyProcessed_(messageId)) continue;

      const subject = msg.getSubject();
      if (!subject.includes("New Appointment")) continue;

      const parsed = parseAhaSubject_(subject);
      const nameParts = splitFirstLast_(parsed.fullName);

      const now = new Date();

      /**
       * Log raw email (optional but useful for debugging)
       */
      appendRow_(SHEET.AHA_INBOX, [
        messageId,
        msg.getDate(),
        subject,
        now,
      ]);

      /**
       * Add clean structured data to Enrollments
       */
      appendRow_(SHEET.ENROLL, [
        Utilities.getUuid(),
        parsed.fullName,
        nameParts.first,
        nameParts.last,
        parsed.className,
        parsed.classDate,
        parsed.instructor,
        now
      ]);

      processed++;
    }
  }

  return processed;
}



function parseAhaSubject_(subject) {
  const text = String(subject || "");

  const nameMatch = text.match(/\(([^)]+)\)/);
  const fullName = nameMatch ? nameMatch[1].trim() : "";

  const classMatch = text.match(/New Appointment\s+(.+?)\s*\(/i);
  const className = classMatch ? classMatch[1].trim() : "";

  const dateMatch = text.match(/on\s+(.+?)\s+with/i);
  const classDate = dateMatch ? dateMatch[1].trim() : "";

  const instructorMatch = text.match(/with\s+(.+)$/i);
  const instructor = instructorMatch ? instructorMatch[1].trim() : "";

  return { fullName, className, classDate, instructor };
}

function splitFirstLast_(fullName) {
  const parts = String(fullName || "").split(/\s+/).filter(Boolean);

  if (parts.length === 0) return { first: "", last: "" };
  if (parts.length === 1) return { first: parts[0], last: "" };

  return {
    first: parts[0],
    last: parts[parts.length - 1],
  };
}

// checks if email is already processed

function alreadyProcessed_(messageId) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET.AHA_INBOX);
  const last = sh.getLastRow();

  if (last < 2) return false;

  const ids = sh.getRange(2, 1, last - 1, 1)
    .getValues()
    .flat()
    .map(String);

  return ids.includes(String(messageId));
}
