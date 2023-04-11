Feature: Verification of Output File

  Scenario: Validating Output File against Input File
    Given User reads InputFile1 InstrumentDetails.csv and InputFile2 PositionDetails.csv
    When The user receives the OutputFile PositionReport.csv by application loading and transforming
    Then The user validates the Output File data against the InputFiles data