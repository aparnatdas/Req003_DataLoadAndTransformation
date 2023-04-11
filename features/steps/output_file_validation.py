from behave import *

import pandas as pd
import numpy as np


@given('User reads InputFile1 {input_file1} and InputFile2 {input_file2}')
def reading_input_files(context, input_file1, input_file2):
    input_df1 = pd.read_csv("features/data/InstrumentDetails.csv")
    input_df2 = pd.read_csv("features/data/PositionDetails.csv")

    context.input_df1 = input_df1
    context.input_df2 = input_df2
    print(input_df1, "\n", input_df2)


@when('The user receives the OutputFile {output_file} by application loading and transforming')
def reading_output_file(context, output_file):
    output_df = pd.read_csv("features/data/PositionReport.csv")
    assert (len(output_df) != 0), "Output DataFrame is Empty"
    context.output_df = output_df


@then('The user validates the Output File data against the InputFiles data')
def test_method(context):
    input_df1 = context.input_df1
    input_df2 = context.input_df2
    output_df = context.output_df

    merged_df = pd.merge(input_df1, input_df2, left_on='ID', right_on='InstrumentID')
    merged_df = pd.merge(merged_df, output_df, left_on='ID_y', right_on='PositionID')

    # Validating ISIN Data
    merged_df["ISIN_comparison"] = merged_df["ISIN_x"] == merged_df["ISIN_y"]
    print(f"ISIN_comparison - {np.unique(merged_df['ISIN_comparison'], return_counts=True)}")
    assert np.all(np.unique(merged_df['ISIN_comparison']) == True), "ISIN validation failed"

    # Validating Quantity Data
    merged_df["qty_comparison"] = merged_df["Quantity_x"] == merged_df["Quantity_y"]
    print(f"qty_comparison - {np.unique(merged_df['qty_comparison'], return_counts=True)}")
    assert np.all(np.unique(merged_df['qty_comparison']) == True), "Quantity validation failed"

    # Validating Total Price
    merged_df["total_price_validation"] = merged_df["Quantity_x"] * merged_df["Unit Price"] == merged_df["Total Price"]
    print(f"total_price_validation - {np.unique(merged_df['total_price_validation'], return_counts=True)}")
    assert np.all(np.unique(merged_df['total_price_validation']) == True), "Total price validation failed"
