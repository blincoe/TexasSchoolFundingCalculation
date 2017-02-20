import csv, xlrd

sourceDir = 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculation'
workingDir = 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculationWD'

################################################################################
##  Specified Output                                                          ##
################################################################################

# Get districtList
districtRunIdListPath = sourceDir + '/Data/LatestRunID.csv'
fDistrictRunIdList = open(districtRunIdListPath, 'rb')
readerDistrictRunIdList = csv.reader(fDistrictRunIdList)
districtRunIdList = list(readerDistrictRunIdList)
nDistricts = len(districtRunIdList[1:])


# Open output file for writing
outDataPath = sourceDir + '/Data/SpecifiedOutput.csv'
f = open(outDataPath, 'wb')
writer = csv.writer(f)

# Header Row
writer.writerow([
    'DistrictID',
    'DistrictName',
    'UpdateTimeStamp',
    'CharterSchoolInd',
    'RegularProgramADA',
    'RegularSpEdADA',
    'MainstreamSpEdADA',
    'ResCareSpEdADA',
    'StateSchoolsSpEdADA',
    'NonPublicContractSpEdADA',
    'ExtYearSpEdADA',
    'RegCTEADA',
    'GTADA',
    'StateCompEdADA',
    'PregnantADA',
    'BilingualADA',
    'PegADA',
    'HighSchoolAllotment',
    'AdvCTEAllotment',
    'EarlyChildIntervSetAside',
    'APTests',
    'NIFA',
    'TransportationAllotment',
    'BilingualAllotmentTot',
    'CompressedMOTaxRate',
    'AdjCEI',
    'SparseDistrictInd',
    'HHMOTaxCollection',
    'HHCEDDistr',
    'HHWADA',
    'HHDPV',
    'MOTaxCollectionLev1',
    'MOTaxCollectionLev3',
    'MOTaxCollectionTot',
    'MOTaxRate',
    'DPV',
    'ASFAmt',
    'TransfersOut',
    'TuitionPaidPerStudent',
    'CADAppraisalCost',
    'CADCreditBalance',
    'CADCreditUnclaimed',
    'BasicAllotmentCheck',
    'AdjustedBasicAllotmentCheck',
    'TierICostCheck',
    'WADACheck',
    'WADACheckCoR',
    'AACheckString',
    'FinalCostLev1Check',
    'FinalCostLev3Check',
    'EarlyAgreementCreditLev1Check',
    'EarlyAgreementCreditLev3Check'])

baseOutFilesDir = workingDir + '/OutFiles/SummaryOfFinances'
errorCount = 0
for districtIndex in range(nDistricts):
    districtID = districtRunIdList[districtIndex + 1][0]
    reportRunID = districtRunIdList[districtIndex + 1][1]
    updateTimeStamp = districtRunIdList[districtIndex + 1][2]
    try:
        TierIDetail = xlrd.open_workbook(workingDir + '/OutFiles/TierIDetail/Dat' + districtID + '.xls')
        SummaryOfFinances = xlrd.open_workbook(workingDir + '/OutFiles/SummaryOfFinances/Dat' + districtID + '.xls')
        AdjAllotmentDetail = xlrd.open_workbook(workingDir + '/OutFiles/AdjAllotmentDetail/Dat' + districtID + '.xls')
        CostOfRecapture = xlrd.open_workbook(workingDir + '/OutFiles/CostOfRecapture/Dat' + districtID + '.xls')
        MOCollectionsDetail = xlrd.open_workbook(workingDir + '/OutFiles/MOCollectionsDetail/Dat' + districtID + '.xls')
        WADADetail = xlrd.open_workbook(workingDir + '/OutFiles/WADADetail/Dat' + districtID + '.xls')
        DistrictNameString = SummaryOfFinances.sheets()[0].cell(3,0).value
        DistrictName = DistrictNameString[0:-9]
        PaymentClassString = SummaryOfFinances.sheets()[0].cell(5,6).value
        CharterSchoolInd = 'Y'
        if PaymentClassString.find('4') == -1 and PaymentClassString.find('5') == -1:
            CharterSchoolInd = 'N'
        RegularProgramADA = TierIDetail.sheets()[0].cell(14,14).value
        RegularSpEdADA = TierIDetail.sheets()[0].cell(16,14).value
        MainstreamSpEdADA = TierIDetail.sheets()[0].cell(17,14).value
        ResCareSpEdADA = TierIDetail.sheets()[0].cell(18,14).value
        StateSchoolsSpEdADA = TierIDetail.sheets()[0].cell(19,14).value
        NonPublicContractSpEdADA = TierIDetail.sheets()[0].cell(20,14).value
        ExtYearSpEdADA = TierIDetail.sheets()[0].cell(21,14).value
        RegCTEADA = TierIDetail.sheets()[0].cell(25,14).value
        GTADA = TierIDetail.sheets()[0].cell(29,14).value
        StateCompEdADA = TierIDetail.sheets()[0].cell(33,14).value
        PregnantADA = TierIDetail.sheets()[0].cell(34,14).value
        BilingualADA = TierIDetail.sheets()[0].cell(40,14).value
        PegADA = TierIDetail.sheets()[0].cell(42,14).value
        HighSchoolAllotment = TierIDetail.sheets()[0].cell(38,17).value
        AdvCTEAllotment = TierIDetail.sheets()[0].cell(26,17).value
        EarlyChildIntervSetAside = TierIDetail.sheets()[0].cell(22,17).value
        APTests = TierIDetail.sheets()[0].cell(30,17).value
        NIFA = TierIDetail.sheets()[0].cell(44,17).value
        TransportationAllotment = SummaryOfFinances.sheets()[0].cell(54,12).value
        BilingualAllotmentTot = TierIDetail.sheets()[0].cell(40,17).value
        CompressedMOTaxRate = SummaryOfFinances.sheets()[0].cell(31,12).value
        AdjCEI = SummaryOfFinances.sheets()[0].cell(42,12).value
        Question2 = AdjAllotmentDetail.sheets()[0].cell(13,0).value
        SparseDistrictInd = 'Y'
        if Question2.find("Yes") == -1:
            SparseDistrictInd = 'N'
        HHMOTaxCollection = CostOfRecapture.sheets()[0].cell(14,17).value
        HHCEDDistr = CostOfRecapture.sheets()[0].cell(15,17).value
        HHWADA = CostOfRecapture.sheets()[0].cell(16,17).value
        HHDPV = CostOfRecapture.sheets()[0].cell(17,17).value
        MOTaxCollectionLev1 = MOCollectionsDetail.sheets()[0].cell(20,12).value
        MOTaxCollectionLev3 = MOCollectionsDetail.sheets()[0].cell(23,12).value
        MOTaxCollectionTot = MOCollectionsDetail.sheets()[0].cell(13,12).value
        MOTaxRate = MOCollectionsDetail.sheets()[0].cell(17,12).value
        DPV = CostOfRecapture.sheets()[0].cell(23,17).value
        ASFAmt = SummaryOfFinances.sheets()[0].cell(69,12).value
        TransfersOut = CostOfRecapture.sheets()[0].cell(25,17).value
        TuitionPaidPerStudent = CostOfRecapture.sheets()[0].cell(26,17).value
        CADAppraisalCost = CostOfRecapture.sheets()[0].cell(60,17).value
        CADCreditBalance = CostOfRecapture.sheets()[0].cell(64,17).value
        CADCreditUnclaimed = CostOfRecapture.sheets()[0].cell(65,17).value
        BasicAllotmentCheck = WADADetail.sheets()[0].cell(18,12).value
        AdjustedBasicAllotmentCheck = WADADetail.sheets()[0].cell(19,12).value
        TierICostCheck = WADADetail.sheets()[0].cell(12,12).value
        WADACheck = WADADetail.sheets()[0].cell(21,12).value
        WADACheckCoR = CostOfRecapture.sheets()[0].cell(22,17).value
        AACheckString = TierIDetail.sheets()[0].cell(11,5).value
        FinalCostLev1Check = CostOfRecapture.sheets()[0].cell(69,17).value
        try:
            FinalCostLev3Check = CostOfRecapture.sheets()[0].cell(152,17).value
        except:
            FinalCostLev3Check = 0
        EarlyAgreementCreditLev1Check = CostOfRecapture.sheets()[0].cell(58,17).value
        try:
            EarlyAgreementCreditLev3Check = CostOfRecapture.sheets()[0].cell(141,17).value
        except:
            EarlyAgreementCreditLev3Check = 0
        writer.writerow([
            districtID,
            DistrictName,
            updateTimeStamp,
            CharterSchoolInd,
            RegularProgramADA,
            RegularSpEdADA,
            MainstreamSpEdADA,
            ResCareSpEdADA,
            StateSchoolsSpEdADA,
            NonPublicContractSpEdADA,
            ExtYearSpEdADA,
            RegCTEADA,
            GTADA,
            StateCompEdADA,
            PregnantADA,
            BilingualADA,
            PegADA,
            HighSchoolAllotment,
            AdvCTEAllotment,
            EarlyChildIntervSetAside,
            APTests,
            NIFA,
            TransportationAllotment,
            BilingualAllotmentTot,
            CompressedMOTaxRate,
            AdjCEI,
            SparseDistrictInd,
            HHMOTaxCollection,
            HHCEDDistr,
            HHWADA,
            HHDPV,
            MOTaxCollectionLev1,
            MOTaxCollectionLev3,
            MOTaxCollectionTot,
            MOTaxRate,
            DPV,
            ASFAmt,
            TransfersOut,
            TuitionPaidPerStudent,
            CADAppraisalCost,
            CADCreditBalance,
            CADCreditUnclaimed,
            BasicAllotmentCheck,
            AdjustedBasicAllotmentCheck,
            TierICostCheck,
            WADACheck,
            WADACheckCoR,
            AACheckString,
            FinalCostLev1Check,
            FinalCostLev3Check,
            EarlyAgreementCreditLev1Check,
            EarlyAgreementCreditLev3Check])
    except:
        errorCount += 1
        print 'Failed for ' + fn
f.close()
print 'There were ' + str(errorCount) + ' errors'
