// @Author Ethan McDonald
// @Version 1.1 4/22/2026
// This currently works on my sheet, the cells for the variables may need to be switched around
// This method needs to be run everyday @ 5pm (Arbitrary time), it checks each User to see if todays date is the reminder date, then sends reminder email.
// Requires GlobalVariables.gs
// :3 yay

function sendReminder() {
  var name = '';
  var sendDate = ''; //Send date currently = 20 month after Add date
  var emailAddress = '';
  var hasSent = true;
  var count = 1;
  var todayDate = new Date();
//forEach all users.
  allData.slice(1, allData.length).forEach(function (userInfoArr) {
    count +=1;
    sendDate = new Date(userInfoArr[5]);
    hasSent = userInfoArr[6];
    name = userInfoArr[1];
    emailAddress = userInfoArr[0];
    range = reminderSheet.getRange("G" + count);
    //Checks values in console
    Logger.log(range);
    Logger.log(sendDate);
    Logger.log(todayDate);
    Logger.log(hasSent);
    //Checks if date matches (currently doesn't care about day just year/month)
    if (sendDate.getFullYear() == todayDate.getFullYear() && sendDate.getMonth() == todayDate.getMonth() && hasSent == false) {

      try {
        GmailApp.sendEmail(emailAddress, "Test!", "This is a reminder, " + name);
        range.setValue(true); //Sets hasSent to true on sheet

      }
      catch (e) {
        try {
          GmailApp.sendEmail(errorEmail, "Error sending email", "There was an error sending email to " + name + " - " + emailAddress + " with script ID " + ScriptApp.getScriptId);
        }
        catch (e) {
          Logger.log("Failed to send email for " + name + " to " + emailAddress + ". Make sure the data in the sheet is valid (valid email address). If it is, is the API down?");
        }
      }
    }
  })
}
