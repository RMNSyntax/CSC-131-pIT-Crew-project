from datetime import datetime, timezone


def dateparser(datestr):
    mm = int(datestr[:2])
    dd = int(datestr[3:5])
    yy = int(datestr[6:10])
    return [mm, dd, yy]

def urlmaker(mm, dd, yy):

    start = datetime(yy, mm, dd, 8, tzinfo=timezone.utc)
    end = datetime(yy, mm, dd+2, 7, 59, tzinfo=timezone.utc)
    start_ms = int(start.timestamp()) * 1000
    end_ms = int(end.timestamp()) * 1000
    print(end_ms, "\n")
    url = f"https://atlas.heart.org/organisation/classes-i-teach?orgSwitch=true&applyTsFilter=true&isFirstTsSelected=false&instructorIds=26027755195&classStartDate={start_ms}&classEndDate={end_ms}&fromDate={yy}-0{mm}-{dd}&toDate={yy}-0{mm}-{dd+1}&sortBy=startDateTime&sortDir=desc&pageSize=10&classTeachTrainingCenter=false"
    return url



"""
https://atlas.heart.org/organisation/classes-i-teach?orgSwitch=true&applyTsFilter=true&isFirstTsSelected=false&instructorIds=26027755195&classStartDate=1771833600000&classEndDate=1772006340000&fromDate=2026-02-23&toDate=2026-02-24&sortBy=startDateTime&sortDir=desc&pageSize=10&classTeachTrainingCenter=false
https://atlas.heart.org/organisation/classes-i-teach?orgSwitch=true&applyTsFilter=true&isFirstTsSelected=false&instructorIds=26027755195&classStartDate=1771833600000&classEndDate=1772006340000&fromDate=2026-02-23&toDate=2026-02-24&sortBy=startDateTime&sortDir=desc&pageSize=10&classTeachTrainingCenter=false
"""
