var rootSheet = SpreadsheetApp.getActive();
var reminderSheet = rootSheet.getSheetByName('Email List');
var allData = reminderSheet.getDataRange().getValues();
var errorEmail = "2egmcd2@gmail.com";
