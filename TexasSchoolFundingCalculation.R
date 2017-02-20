src <- 'C:/Users/blincoeshirey/Documents/Ian/Analysis/TexasSchoolFundingCalculation'

datPath <- paste0(src, '/Data/SpecifiedOutput.csv')
dat <- read.csv(datPath, stringsAsFactors = FALSE)

convertDollarToNumber <- function(x){
    out <- as.numeric(gsub('\\(', '',
                          gsub('\\$', '',
                              gsub('\\)', '',
                                  gsub(',', '',
                                      x
                                      )
                                  )
                              )
                          )
                      ) * ifelse(substring(x, 1, 1) == "(",
                                 -1,
                                 1)
    return(out)
}

texasSchoolFinanceCalc <- function(iDat = dat,
                                   districtSubset = c(),
                                   EWLev1 = 514000,
                                   EWLev3 = 319500,
                                   SmallDistrictMult = 0.00025,
                                   SparseSmallDistrictMult = 0.0004,
                                   MedDistrictMult = 0.000025,
                                   SmallDistrictADACap = 1600,
                                   MedDistrictADACap = 5000,
                                   RegularProgramTIAAWeight = 1,
                                   RegularSpEdTIAAWeight = 1,
                                   MainstreamSpEdTIAAWeight = 1.1,
                                   ResCareSpEdTIAAWeight = 4,
                                   StateSchoolsSpEdTIAAWeight = 2.8,
                                   NonPublicContractSpEdTIAAWeight = 1.7,
                                   ExtYearSpEdTIAAWeight = 1,
                                   RegCTETIAAWeight = 1.35,
                                   GTTIAAWeight = 0.12,
                                   StateCompEdTIAAWeight = 0.2,
                                   PregnantTIAAWeight = 2.41,
                                   BilingualTIAAWeight = 0.1,
                                   PegTIAAWeight = 0.1,
                                   HHCEDRate = 0.0082,
                                   HHEWL = 280000,
                                   HHMOTaxRate = 1.17,
                                   HHTaxRateFloor = 0.015,
                                   CostPerWADAFloorLev1 = 3146.52,
                                   CostPerWADAFloorLev3 = 71.62,
                                   EarlyAgreementCreditPct = 0.04,
                                   EarlyAgreementCreditPerWADA = 80,
                                   CharterSchoolAdjCEI = 1.0795,
                                   useCostOfRecaptureReportedWADA = FALSE
                                   ) {
    if (is.null(districtSubset)){
        fDat <- iDat
    } else {
        fDat <- iDat[iDat$DistrictID %in% districtSubset, ]
    }

    fDat$EarlyChildIntervSetAside <- convertDollarToNumber(fDat$EarlyChildIntervSetAside)

    fDat$APTests <- convertDollarToNumber(fDat$APTests)

    fDat$AACheckVal <- as.numeric(sub(',', '',
                                      substring(fDat$AACheckString,
                                                nchar(fDat$AACheckString) - 4,
                                                nchar(fDat$AACheckString)
                                                )
                                      )
                                  )

    fDat$CompressedMOTaxRateAlt <- ifelse(fDat$CompressedMOTaxRate < 0.1,
                                          1,
                                          fDat$CompressedMOTaxRate)

    fDat$BasicAllotment <- round(ifelse(fDat$CharterSchoolInd == 'Y',
                                        EWLev1 / 100 * fDat$BasicAllotmentCheck / 5140,
                                        EWLev1 * pmin(1, fDat$CompressedMOTaxRateAlt)/100
                                        )
                                  )

    fDat$AdjustedBasicAllotment <- round(ifelse(fDat$CharterSchoolInd == 'Y',
                                                EWLev1 / 100 * fDat$BasicAllotmentCheck / 5140,
                                                EWLev1 * pmin(1,
                                                             ifelse(fDat$CompressedMOTaxRate < 0.1,
                                                                    1,
                                                                    fDat$CompressedMOTaxRate
                                                                    )
                                                             ) / 100
                                                ) * (1 + (ifelse(fDat$CharterSchoolInd == 'Y',
                                                                 CharterSchoolAdjCEI,
                                                                 fDat$AdjCEI
                                                                 ) - 1) * 0.71)
                                         )

    fDat$AdjustedAllotment <- round(
        ifelse(fDat$CharterSchoolInd == 'Y',
               EWLev1 / 100 * fDat$AACheckVal / 5140,
               fDat$AdjustedBasicAllotment * pmax(1,
                                                 1 + ifelse(fDat$RegularProgramADA < SmallDistrictADACap,
                                                            (SmallDistrictADACap - fDat$RegularProgramADA) *
                                                                ifelse(fDat$SparseDistrictInd == "Y",
                                                                       SparseSmallDistrictMult,
                                                                       SmallDistrictMult
                                                                       ), 0),
                                                 1 + ifelse(fDat$RegularProgramADA < MedDistrictADACap,
                                                            (MedDistrictADACap - fDat$RegularProgramADA) * MedDistrictMult,
                                                            0)
                                                 )
               )
        )

    fDat$TierICost <- fDat$AdjustedAllotment * (
        fDat$RegularProgramADA * RegularProgramTIAAWeight +
            fDat$RegularSpEdADA * RegularSpEdTIAAWeight +
                fDat$MainstreamSpEdADA * MainstreamSpEdTIAAWeight +
                    fDat$ResCareSpEdADA * ResCareSpEdTIAAWeight +
                        fDat$StateSchoolsSpEdADA * StateSchoolsSpEdTIAAWeight +
                            fDat$NonPublicContractSpEdADA * NonPublicContractSpEdTIAAWeight +
                                fDat$ExtYearSpEdADA * ExtYearSpEdTIAAWeight +
                                    fDat$RegCTEADA * RegCTETIAAWeight +
                                        fDat$GTADA * GTTIAAWeight +
                                            fDat$StateCompEdADA * StateCompEdTIAAWeight +
                                                fDat$PregnantADA * PregnantTIAAWeight +
                                                    fDat$BilingualADA * BilingualTIAAWeight +
                                                        fDat$PegADA * PegTIAAWeight) +
        fDat$HighSchoolAllotment +
            fDat$AdvCTEAllotment +
                fDat$EarlyChildIntervSetAside +
                    fDat$APTests +
                        fDat$NIFA +
                            fDat$TransportationAllotment +
                                ifelse(fDat$BilingualADA == 0,
                                       fDat$BilingualAllotmentTot * EWLev1 / 514000,
                                       0)

    fDat$AdjustedTierICost <- fDat$TierICost - (
        fDat$HighSchoolAllotment +
            fDat$EarlyChildIntervSetAside +
                fDat$NIFA +
                    fDat$TransportationAllotment)

    if (useCostOfRecaptureReportedWADA){
        fDat$WADA <- fDat$WADACheckCoR
    } else {
        fDat$WADA <- fDat$AdjustedTierICost / fDat$BasicAllotment * (fDat$AdjustedBasicAllotment + fDat$BasicAllotment) /
                (2 * fDat$AdjustedBasicAllotment)
    }

    fDat$HHTaxRate <- pmax(HHTaxRateFloor,
                          ifelse(fDat$HHDPV > 0,
                                 fDat$HHMOTaxCollection / fDat$HHDPV,
                                 0) + HHCEDRate
                          )

    fDat$HHAdjMORevenue <- ifelse(fDat$HHWADA > 0,
                                  (fDat$HHMOTaxCollection + fDat$HHCEDDistr) * fDat$HHTaxRate / fDat$HHWADA - fDat$ASFAmt,
                                  0)

    fDat$HHAdjTaxBaseLev1 <- fDat$WADA * pmax(EWLev1,
                                             fDat$HHAdjMORevenue / fDat$HHTaxRate / fDat$WADA *
                                                 ((EWLev1 / HHEWL - 1) * fDat$MOTaxRate / HHMOTaxRate + 1)
                                             )

    fDat$ExcessTaxBaseLev1 <- pmax(0, fDat$DPV - fDat$HHAdjTaxBaseLev1)

    fDat$CostBeforeDiscountsLev1 <- ifelse(fDat$DPV > 0, fDat$ExcessTaxBaseLev1 / fDat$DPV * fDat$MOTaxCollectionLev1, 0)

    fDat$CostPerWADALev1 <- ifelse(fDat$CostBeforeDiscountsLev1 == 0,
                                   0,
                                   pmax(CostPerWADAFloorLev1,
                                       fDat$CostBeforeDiscountsLev1 /
                                           (fDat$ExcessTaxBaseLev1 /
                                                (fDat$HHAdjTaxBaseLev1 / fDat$WADA)
                                            )
                                       )
                                   )

    fDat$EarlyAgreementCreditLev1 <- ifelse(fDat$HHAdjTaxBaseLev1 > 0,
                                            pmin(fDat$CostBeforeDiscountsLev1 * EarlyAgreementCreditPct,
                                                fDat$ExcessTaxBaseLev1 /
                                                    (fDat$HHAdjTaxBaseLev1 / fDat$WADA) *
                                                        EarlyAgreementCreditPerWADA,
                                                 fDat$EarlyAgreementCreditLev1Check
                                                ),
                                            0)

    fDat$CADCreditAmountLev1 <- ifelse(fDat$MOTaxCollectionTot > 0,
                                       fDat$CADAppraisalCost * fDat$CostBeforeDiscountsLev1 / fDat$MOTaxCollectionTot +
                                               fDat$CADCreditBalance + fDat$CADCreditUnclaimed,
                                       0)

    fDat$FinalCostLev1 <- pmax(0,
                              ifelse(fDat$HHAdjTaxBaseLev1 > 0,
                                     fDat$CostPerWADALev1 * fDat$ExcessTaxBaseLev1 / (fDat$HHAdjTaxBaseLev1 / fDat$WADA) - (
                                         fDat$EarlyAgreementCreditLev1 +
                                             fDat$CADCreditAmountLev1 * 0 +
                                                 fDat$TransfersOut * fDat$TuitionPaidPerStudent +
                                                     fDat$NIFA),
                                     0)
                              )

    fDat$HHAdjTaxBaseLev3 <- fDat$WADA * pmax(EWLev3,
                                             fDat$HHAdjMORevenue / fDat$HHTaxRate / fDat$WADA *
                                                 ((EWLev3 / HHEWL - 1) * fDat$MOTaxRate / HHMOTaxRate + 1)
                                             )

    fDat$ExcessTaxBaseLev3 <- pmax(0, fDat$DPV - fDat$HHAdjTaxBaseLev3)

    fDat$CostBeforeDiscountsLev3 <- ifelse(fDat$DPV > 0, fDat$ExcessTaxBaseLev3 / fDat$DPV * fDat$MOTaxCollectionLev3, 0)

    fDat$CostPerWADALev3 <- ifelse(fDat$CostBeforeDiscountsLev3 == 0,
                                   0,
                                   pmax(CostPerWADAFloorLev3,
                                       fDat$CostBeforeDiscountsLev3 /
                                           (fDat$ExcessTaxBaseLev3 /
                                                (fDat$HHAdjTaxBaseLev3 / fDat$WADA)
                                            )
                                       )
                                   )

    fDat$EarlyAgreementCreditLev3 <- ifelse(fDat$HHAdjTaxBaseLev3 > 0,
                                            pmin(fDat$ExcessTaxBaseLev3 / (fDat$HHAdjTaxBaseLev3 / fDat$WADA) *
                                                    fDat$CostPerWADALev3 * EarlyAgreementCreditPct,
                                                fDat$ExcessTaxBaseLev3 / (fDat$HHAdjTaxBaseLev3 / fDat$WADA) *
                                                    EarlyAgreementCreditPerWADA,
                                                fDat$EarlyAgreementCreditLev3Check), 0)

    fDat$CADCreditAmountLev3 <- ifelse(fDat$MOTaxCollectionTot > 0,
                                       fDat$CADAppraisalCost * fDat$CostBeforeDiscountsLev3 / fDat$MOTaxCollectionTot +
                                               fDat$CADCreditBalance + fDat$CADCreditUnclaimed,
                                       0)

    fDat$FinalCostLev3 <- pmax(0,
                              ifelse(fDat$HHAdjTaxBaseLev3 > 0,
                                     fDat$CostPerWADALev3 * fDat$ExcessTaxBaseLev3 / (fDat$HHAdjTaxBaseLev3 / fDat$WADA) - (
                                         fDat$EarlyAgreementCreditLev3 +
                                             fDat$CADCreditAmountLev3 * 0 +
                                                 fDat$TransfersOut * fDat$TuitionPaidPerStudent +
                                                     fDat$NIFA),
                                     0)
                              )
    fDat$CostofRecapture <- fDat$FinalCostLev1 + fDat$FinalCostLev3
    fDat$TierIStateShare <- pmax(0,
                                fDat$TierICost - fDat$DPV * fDat$CompressedMOTaxRate / 100)

    fDat$CostofRecapture <- ifelse(is.na(fDat$CostofRecapture), 0, fDat$CostofRecapture)

    return(fDat)
}


## Example of default calculation
calcDat <- texasSchoolFinanceCalc()
View(calcDat)
sum(calcDat$CostofRecapture)


## Example of a scenario run with simply plotted results
out <- rep(NA, 10)
for (altEWLIndex in 1:10){
    altEWL <- (514000 + (altEWLIndex - 1) * 50000)
    x <- texasSchoolFinanceCalc(EWLev1 = altEWL, districtSubset = c(227901))
    out[altEWLIndex] <- x$CostofRecapture
}
plot(out, type = "l", ylim = c(0, 400000000))

