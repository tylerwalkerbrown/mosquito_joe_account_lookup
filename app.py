import streamlit as st
import pandas as pd
def streamlit_main():
    st.title("Streamlit App Requirements")

    requirements = """
    streamlit==1.10.0
    pandas==1.4.2
    """

    st.text("Below are the requirements for this Streamlit app:")
    st.code(requirements, language='bash')

def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

def perform_merge(df1, df2, df3):
    merge1 = pd.merge(df1, df2, on='accountnum')
    merge2 = pd.merge(merge1, df3, on='accountnum')
    return merge2[['Businessname', 'completeddate', 'accountnum', 'SumOfbillamount', 'saledate', 'duration', 'measurement']]

def calculate_aggregates(df):
    total_bill = pd.DataFrame(df.groupby(['Businessname', 'accountnum'])['SumOfbillamount'].sum()).reset_index()
    count = pd.DataFrame(df.groupby(['Businessname', 'accountnum'])['completeddate'].count()).reset_index()
    merge3 = pd.merge(count, total_bill, on='accountnum')
    merge3.rename(columns={'completeddate': 'Total_Completed', 'SumOfbillamount': 'Total_Bill'}, inplace=True)
    merge3['avg_bill'] = merge3['Total_Bill'] / merge3['Total_Completed']
    return merge3

# Streamlit app
def streamlit_main():
    st.title("CSV Merger, Aggregator, and Search")

    # File uploaders
    st.write("Completed WO Detail By Date - ")
    csv_1 = st.file_uploader("Choose the first CSV file", type=["csv"])
    st.write("price History of Events")
    csv_2 = st.file_uploader("Choose the second CSV file", type=["csv"])
    st.write("Account Detail by Event By Sort")
    csv_3 = st.file_uploader("Choose the third CSV file", type=["csv"])

    if csv_1 and csv_2 and csv_3:
        df1 = load_data(csv_1)
        df2 = load_data(csv_2)
        df3 = load_data(csv_3)

        # Merge and calculate aggregates
        merged_df = perform_merge(df1, df2, df3)
        aggregates_df = calculate_aggregates(merged_df)

        # Search box to filter results
        account_search = st.text_input("Enter an account number to search:")

        if account_search:
            # Filter both DataFrames based on the search_value
            filtered_merged_df = merged_df[merged_df['accountnum'] == account_search]
            filtered_aggregates_df = aggregates_df[aggregates_df['accountnum'] == account_search]

            # Display the filtered merged DataFrame
            st.write("Filtered Merged Data")
            st.dataframe(filtered_merged_df)

            # Display the filtered aggregates DataFrame
            st.write("Filtered Aggregated Data")
            st.dataframe(filtered_aggregates_df)
        else:
            # Display instructions
            st.write("Enter an account number to filter the data.")

if __name__ == "__main__":
    streamlit_main()
