import requests, csv
from bs4 import BeautifulSoup

sourceDir = 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculation'

districtListPath = sourceDir + '/Data/DistrictList.py'
execfile(districtListPath)


urlStub = 'https://tea4avfawcett.tea.state.tx.us/Fsp/Reports'
url = urlStub + '/ReportSelection.aspx'


initialRequest = requests.get(url)
initialSoup = BeautifulSoup(initialRequest.text)

initialViewState = initialSoup.findAll('input', {'type': 'hidden', 'name': '__VIEWSTATE'})
initialEventValidation = initialSoup.findAll('input', {'type': 'hidden', 'name': '__EVENTVALIDATION'})

initReportName = 'SummaryOfFinance'

selectedReportDatalist = {'__EVENTVALIDATION':initialEventValidation[0]['value'],
            '__VIEWSTATE':initialViewState[0]['value'],
            '__VIEWSTATEENCRYPTED': '',
            'ctl00$Body$ReportTypeDropDownList': initReportName,
            'ctl00$Body$SelectButton': 'Select'
}

selectedReportRequest = requests.post(url, data = selectedReportDatalist)
selectedReportSoup = BeautifulSoup(selectedReportRequest.text)

selectedReportViewState = selectedReportSoup.findAll('input', {'type': 'hidden', 'name': '__VIEWSTATE'})
selectedReportEventValidation = selectedReportSoup.findAll('input', {'type': 'hidden', 'name': '__EVENTVALIDATION'})

year = '2017'

outDataPath = sourceDir + '/Data/LatestRunID.csv'
f = open(outDataPath, 'wb')
writer = csv.writer(f)

# Header Row
writer.writerow([
    'DistrictID',
    'LatestRunID',
    'UpdateTimeStamp'])

errorCount = 0
for districtID in districtList:
    finalDataList = {'__EVENTVALIDATION':selectedReportEventValidation[0]['value'],
                     '__VIEWSTATE':selectedReportViewState[0]['value'],
                     '__VIEWSTATEENCRYPTED':'',
                     'ctl00$Body$SchoolYearDropDownList':year,
                     'ctl00$Body$DistrictIdTextBox':districtID,
                     'ctl00$Body$SubmitButton':'Submit'
    }
    finalRequest = requests.post(url, data = finalDataList)

    finalSoup = BeautifulSoup(finalRequest.text)
    table = finalSoup.find('table', attrs={'class':'gridView'})

    if table is not None:
        try:
            lastRowIndex = len(table.find_all('tr')[1:])
            lastRow = table.find_all('tr')[lastRowIndex]
            col = lastRow.find_all('td')
            latestRunID = col[0].string
            updateTimeStamp = col[1].string
            writer.writerow([districtID, latestRunID, updateTimeStamp])
        except:
            errorCount += 1
    else: errorCount += 1

f.close()
print 'There were ' + str(errorCount) + ' errors'

