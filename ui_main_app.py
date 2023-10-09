# !pip install streamlit -q
import Condition_5_select_30
import streamlit as st
# import streamlit_extras as stx

st.title("PE Valuation")
tab_input,tab_output =st.tabs(['input','output'])
with tab_input:
    with st.expander('Select Mode and EXCHANGE'):
        exchange_lst = ['BO', 'NS']
        mode_lst =['test','final']
        mode_selected = st.selectbox('Select Mode test or final', mode_lst)
        exchange_selected =st.selectbox('Select Exchange BO = BSE NS = NSE', exchange_lst)
    with st.expander('Select dividend Yield'):
        dividend_yield_slect = st.checkbox('Dividend Yield',value=True)
        dividend_yield_value = st.number_input('Dividend yield \
        |based on current price| unit is %| should more than 1% |', min_value=0.0, max_value=1.0, step=0.1, value=0.5)
    with st.expander('Select small cap value'):
        small_cap_select = st.checkbox('Small Cap',value=True)
        small_cap_value = st.slider('market cap more than inr 83105000000',
                                            min_value=83105000000, max_value=83105000000*2, step=int(83105000000/10))
    with st.expander('Select Debet to Equity'):
        debtToEquity_select = st.checkbox('Debet to Equity',value=True)
        debtToEquity_value = st.slider('Debt to Equity | Unit is Ratio |\
        should be less than 0.5', min_value=0.5, max_value=2.0, step=0.25)
    with st.expander('Select Current Ratio'):
        current_ratio_select = st.checkbox("Current Ratio",value=True)
        current_ratio_value = st.slider('Current Ratio |unit is ratio |should \
        be more than 2', min_value=0.0, max_value=2.0, step=0.25)
    with st.expander('Select Current Ratio'):
        return_on_equity_select = st.checkbox("Return on Equity",value=True)
        return_on_Equity_value = st.slider('Return on Equity | unit is % |\
        should be more than 15%', min_value=0, max_value=15, step=1)
        
        ui_dict = {'mode_select':mode_selected,
                    'exchange_select': exchange_selected,
                    'devidend_yield_ckbox': dividend_yield_slect,
                    'small_cap_ckbox': small_cap_select,
                    'debitToEquity_ckbox': debtToEquity_select,
                    'current_ratio_ckbox': current_ratio_select,
                    'return_on_equity_ckbox': return_on_equity_select,
                    'devidend_yield_vl': dividend_yield_value,
                    'small_cap_vl': small_cap_value,
                    'debitToEquity_vl': debtToEquity_value,
                    'current_ratio_vl': current_ratio_value,
                    'return_on_equity_vl': return_on_Equity_value
                }
        def run_result():
            bse = Condition_5_select_30.select_30_stock(ui_dict)
            output_print_lst=bse.write_2_drive()
            # return output_print_lst
    submit_bt = st.button(
    "Submit", key='submit_button_key', on_click=run_result,disabled=False)

with tab_output:
    st.write(ui_dict)
    # st.write(output_print_lst)


    







