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
  var eDate; //Expiration date
  var hasSent = false;
  var count = 1;
  var todayDate = new Date();
//forEach all users.
  allData.slice(1, allData.length).forEach(function (userInfoArr) {
    count +=1;
    sendDate = new Date(userInfoArr[5]);
    hasSent = userInfoArr[6];
    name = userInfoArr[1];
    emailAddress = userInfoArr[0];
    eDate = userInfoArr[5];
    range = reminderSheet.getRange("G" + count);
    //Checks values in console
    Logger.log(range);
    Logger.log(sendDate);
    Logger.log(todayDate);
    Logger.log(hasSent);
    //Checks if date matches (currently doesn't care about day just year/month)
    if (sendDate.getFullYear() == todayDate.getFullYear() && sendDate.getMonth() == todayDate.getMonth() && hasSent == false) {

      try {
          var htmlTemplate = HtmlService.createTemplateFromFile('RemEmail');
          htmlTemplate.name = name;
          htmlTemplate.edate = eDate;
           var htmlForEmail = htmlTemplate.evaluate().getContent();
        GmailApp.sendEmail(emailAddress, name + ', your CPR certification is expiring soon', 'this email contains html',
    {htmlBody: htmlForEmail});
        range.setValue(true); //Sets hasSent to true on sheet

      }
        catch (e) {
          Logger.log("Failed to send email for " + name + " to " + emailAddress + ". Make sure the data in the sheet is valid (valid email address). If it is, is the API down?");
        }
      }
  })
}
