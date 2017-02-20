import requests, csv

sourceDir = 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculation'
workingDir = 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculationWD'

# Get districtList
districtRunIdListPath = sourceDir + '/Data/LatestRunID.csv'
f = open(districtRunIdListPath, 'rb')
reader = csv.reader(f)
districtRunIdList = list(reader)
nDistricts = len(districtRunIdList[1:])


urlStub = 'https://tea4avfawcett.tea.state.tx.us/Fsp/Reports/CrystalReportViewer.aspx?'
schoolYear = '2017'

reportList = [ # Report ID, Report Name
    ['6', 'SummaryOfFinances'],
    ['13', 'AdjAllotmentDetail'],
    ['14', 'MOCollectionsDetail'],
    ['18', 'TierIDetail'],
    ['30', 'CostOfRecapture'],
    ['42', 'WADADetail']]


def scrapeReport(districtID, reportID, reportName, reportRunID):
    outFilesDir = workingDir + '/OutFiles/' + reportName
    outFilePath = outFilesDir + '/Dat' + districtID + '.xls'
    url = urlStub + 'rpt=' + reportID + '&year=' + schoolYear + '&run=' + reportRunID + '&cdn=' + districtID + '&format=excel'
    outRequest = requests.get(url)
    if (outRequest.status_code == 200):
        outFile = open(outFilePath, 'wb')
        outFile.write(outRequest.content)
        outFile.close()
    else:
        print '    Failure: ' + reportName + ' for district ' + districtID + ' not downloaded'


def extractReports(districtID, reportRunID, districtIndex):
    print 'Getting reports for ' + districtID + ' (' + str(districtIndex) + ' / ' + str(nDistricts) + ')'
    for reportIndex in range(len(reportList)):
        scrapeReport(districtID, reportList[reportIndex][0], reportList[reportIndex][1], reportRunID)


for districtIndex in range(nDistricts):
    districtID = districtRunIdList[districtIndex + 1][0]
    reportRunID = districtRunIdList[districtIndex + 1][1]
    extractReports(districtID, reportRunID, districtIndex + 1)

