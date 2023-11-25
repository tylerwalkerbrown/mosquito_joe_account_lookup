import streamlit as st
import pandas as pd

def load_data(file1, file2, file3):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
    
    merge1 = pd.merge(df1, df2, on='accountnum', how='left')
    merge2 = pd.merge(merge1, df3, on='accountnum', how='left')
    
    return merge2

def calculate_aggregates(df):
    total_bill = pd.DataFrame(df.groupby(['Businessname', 'accountnum'])['SumOfbillamount'].sum()).reset_index()
    count = pd.DataFrame(df.groupby(['Businessname', 'accountnum'])['completeddate'].count()).reset_index()
    merge3 = pd.merge(count, total_bill, on='accountnum')
    merge3.rename(columns={'completeddate': 'Total_Completed', 'SumOfbillamount': 'Total_Bill'}, inplace=True)
    merge3['avg_bill'] = merge3['Total_Bill'] / merge3['Total_Completed']
    
    return merge3

def streamlit_main():
    st.title("Data Aggregation and Display")

    uploaded_file_1 = st.file_uploader("Upload first CSV file", type="csv", key="file1")
    uploaded_file_2 = st.file_uploader("Upload second CSV file", type="csv", key="file2")
    uploaded_file_3 = st.file_uploader("Upload third CSV file", type="csv", key="file3")

    if uploaded_file_1 and uploaded_file_2 and uploaded_file_3:
        merged_df = load_data(uploaded_file_1, uploaded_file_2, uploaded_file_3)

        # Extracting unique account numbers for the dropdown
        unique_accounts = merged_df['accountnum'].unique()
        selected_account = st.selectbox("Select an account number", unique_accounts)

        # Multiplier input
        multiplier = st.number_input("Enter a multiplier for avg_bill", value=1, step=1)
        discount = st.number_input("Discount Amount")

        # Search button
        if st.button("Search"):
            if discount == 0:
                filtered_df = merged_df[merged_df['accountnum'] == selected_account]
                df = filtered_df[['Businessname', 'completeddate', 'accountnum', 'SumOfbillamount', 'saledate', 'duration', 'measurement']]
                aggregates_df = calculate_aggregates(df)
                st.subheader("Filtered Aggregated Data")
                st.dataframe(df)
                st.dataframe(aggregates_df)
                st.dataframe((multiplier *  aggregates_df['avg_bill']))

            else:
                filtered_df = merged_df[merged_df['accountnum'] == selected_account]
                df = filtered_df[['Businessname', 'completeddate', 'accountnum', 'SumOfbillamount', 'saledate', 'duration', 'measurement']]
                aggregates_df = calculate_aggregates(df)
                st.subheader("Filtered Aggregated Data")
                st.dataframe(df)
                st.dataframe(aggregates_df)
                st.dataframe((multiplier *  aggregates_df['avg_bill'])*(1 - discount))


    else:
        st.write("Please upload all three CSV files to proceed.")

if __name__ == "__main__":
    streamlit_main()
