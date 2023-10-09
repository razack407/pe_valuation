# !pip install yfinance===0.2.28 -q
# !pip install pendulum -q

import pandas as pd
import shutil
import yfinance as yf
import pandas as pd
import csv
import pendulum
from io import StringIO
import requests

# Read the CSV file into a Pandas DataFrame


def ticker_list(ui_input):
    # Get the file ID of the CSV file in Google Drive
    file_id_bse_short = "1hrE0Fsomu7oXi0iTjT84L1jbsObddkWE" #BSE_Equity_short.csv
    file_id_nse_short = "1Q1z30lSsnnwi-vZTFEsMhqj4L83BWLS6" #nse_short.csv 
    file_id_bse_full  = "1MUatwA_FVPjINzWCDSlVm3MVm68PA_sK" #bse_equity.csv
    file_id_nse_full  = "1OcwJRdlBfvY76eyj21ixzW2zgmhwE2GT" #nse_full.csv
    
    if ui_input['exchange_select']=='BO' and ui_input['mode_select']=='test' :
        file_id = file_id_bse_short
    elif ui_input['exchange_select']=='BO' and ui_input['mode_select']=='final' :
        file_id = file_id_bse_full
    elif  ui_input['exchange_select']=='NS' and ui_input['mode_select']=='test' :
        file_id = file_id_nse_short
    elif  ui_input['exchange_select']=='NS' and ui_input['mode_select']=='final' :
        file_id = file_id_nse_full
    else:
        print (' excahnge and mode not selected propery')
        file_id= None
    
    # Construct the download URL for the CSV file
    download_url = f"https://drive.google.com/uc?id={file_id}"

    # Download the CSV file using the requests library
    response = requests.get(download_url)
    # print (response.content)

    # Decode the response content to a string object
    decoded_content = response.content.decode()
    # Read the CSV file contents into a Pandas DataFrame
    df_bse_ticker = pd.read_csv(StringIO(decoded_content))
    if ui_input['exchange_select']=='BO':
        df_bse_ticker['Security Id']= df_bse_ticker['Security Id']+'.'+ui_input['exchange_select']
        ticker_lst = df_bse_ticker['Security Id'].tolist()   
    elif ui_input['exchange_select']=='NS':
        df_bse_ticker['SYMBOL']= df_bse_ticker['SYMBOL']+'.'+ui_input['exchange_select']
        ticker_lst = df_bse_ticker['SYMBOL'].tolist()
    else:
        print("exchange not selected properly")
        return []
     
    # for nse use ['SYMBOL']
    # for bse use ['Security Id']
    
    return ticker_lst



# new Method | used here | BO = Bombay stock exchange


class select_30_stock:
    def __init__(self, ui_input):
        self.ui_input = ui_input
        self.ticker_lst = ticker_list(self.ui_input)
        self.stock_30_selected = []
        self.stock_not_selected = []
        # self.now = datetime.datetime.now()
        self.now = pendulum.now()
        self.current_date_time = self.now.in_tz('Asia/Kolkata')
# Format the date and time as a string
        self.current_date_time = self.current_date_time.format(
            'YYYY-MM-DD___HH-mm-ss')
        self.filename_ticker =    "ticker_log_______"+self.current_date_time+".csv"
        self.filename_parameter = "parameter_log__"+self.current_date_time+".csv"
        self.filename_result =    "share_30_select__"+self.current_date_time+".csv"
        
        # self.test_app_dividend_yield_value=app.dividend_yield_value
        
        

    def check_5_condition_select30(self):

        # Create a CSV file
        with open(self.filename_ticker, "w", newline="") as f_ticker:
            self.writer_ticker = csv.writer(f_ticker)
            with open(self.filename_parameter, "w", newline="") as f_parameter:
                self.writer_parameter = csv.writer(f_parameter)
                for symbol_index in self.ticker_lst:
                    try:
                        # writer.writerow([str(count)+'   '+symbol_index+'.BO'])
                        self.stock = yf.Ticker(symbol_index)
                        # print('1',self.stock.basic_info)
                        # print('2',(self.stock.ticker))
                        # count = count +1
                        self.writer_ticker.writerow(
                            ["                                                        "])
                        self.writer_ticker.writerow(
                            [symbol_index +' from excel list  is exist in yahoo finace as '+self.stock.ticker])
                    except Exception as e:
                        self.writer_ticker.writerow(
                            [symbol_index +'     does not exist in yahoo finance      '])
                        try:
                            self.stock = yf.Ticker(symbol_index)
                            self.writer_ticker.writerow(
                                [symbol_index+" without BO(from excel) does exist in yahoo finance"])
                        except Exception as e:

                            self.writer_ticker.writerow(
                                [symbol_index+"without BO (from excel) does not  exist in yahoo finance"])

                #! condition 1
                    self.small_cap_value = self.ui_input['devidend_yield_vl']#83105000000
                    # empty line for sepearation
                    self.writer_parameter.writerow(["      "])
                    try:
                        # divident Yield | based on the current price | should more than 1 % | unit is %
                        if self.ui_input['devidend_yield_ckbox'] :
                            self.dividendYield_select = self.stock.info['dividendYield']
                            if self.dividendYield_select >  self.ui_input['devidend_yield_vl']: #1:
                                self.stock_dividendYield = True
                            else:
                                self.stock_dividendYield = False
                        else:
                            self.stock_dividendYield = True
                    except:
                        self.writer_parameter.writerow(
                            ["The key 'dividendYield' does not exist in "+symbol_index])
                        self.stock_dividendYield = False
                #! condition 2
                    try:
                        # market capitalization | should be less than 83105000000 inr for small cap                      
                        if self.ui_input['small_cap_ckbox']:
                            self.marketCap_select = self.stock.info['marketCap']
                            if self.marketCap_select < self.ui_input['small_cap_vl']:
                                self.stock_marketCap = True
                            else:
                                self.stock_marketCap = False
                        else:
                            self.stock_marketCap = True
                    except:
                        self.writer_parameter.writerow(
                            ["The key 'marketCap' does not exist in "+symbol_index])
                        self.stock_marketCap = False
                # !condition 3
                    try:
                        # debtToEquity| D/E  | should less than 0.5 | unit is ratio (times)                      
                        if self.ui_input['debitToEquity_ckbox']:
                            self.debtToEquity_select = self.stock.info['debtToEquity']
                            if self.debtToEquity_select < self.ui_input['debitToEquity_vl']:#0.5:
                                self.stock_debtToEquity = True
                            else:
                                self.stock_debtToEquity = False
                        else:
                            self.stock_debtToEquity = True
                    except:
                        self.writer_parameter.writerow(
                            ["The key 'debtToEquity' does not exist in "+symbol_index])
                        self.stock_debtToEquity = False
                #! condition 4
                    try:
                        # currentRatio  | should more than 2 | unit is ratio (times)                     
                        if self.ui_input['current_ratio_ckbox']:
                            self.currentRatio_select = self.stock.info['currentRatio']
                            if self.currentRatio_select > self.ui_input['current_ratio_vl']:#2:
                                self.stock_currentRatio = True
                            else:
                                self.stock_currentRatio = False
                        else:
                            self.stock_currentRatio = True
                    except:
                        self.writer_parameter.writerow(
                            ["The key 'currentRatio' does not exist in "+symbol_index])
                        self.stock_currentRatio = False
                #! condition 5
                    try:
                        # returnOnEquity  | should more than 15% | unit is %
                        if self.ui_input['return_on_equity_ckbox']:
                            self.returnOnEquity_select = self.stock.info['returnOnEquity']
                            if self.returnOnEquity_select > self.ui_input['return_on_equity_vl']:#2:
                                self.stock_returnOnEquity = True
                            else:
                                self.stock_returnOnEquity = False
                        else:
                            self.stock_returnOnEquity = True
                            
                    except:
                        self.writer_parameter.writerow(
                            ["The key 'returnOnEquity' does not exist in "+symbol_index])
                        self.stock_returnOnEquity = False
                # Final selection of Stock Ticker
                    if (self.stock_dividendYield and
                        self.stock_marketCap and
                        self.stock_debtToEquity and
                        self.stock_currentRatio and
                            self.stock_returnOnEquity):
                        self.stock_30_selected.append(symbol_index)

                    else:
                        self.stock_not_selected.append(symbol_index)
        with open(self.filename_result, "w", newline="") as f_result:
            self.writer_result = csv.writer(f_result)
            self.writer_result.writerow(['selected 30 stocks :'])
            self.writer_result.writerow(['                    '])
            self.writer_result.writerow([str(self.stock_30_selected)])
            self.writer_result.writerow(['stock_not_selected :  '])
            self.writer_result.writerow([str(self.stock_not_selected)])
            return self.stock_30_selected     # check it 

    def write_2_drive(self):
        self.output_to_screen=self.check_5_condition_select30()

        target_directory_test = "G:/My Drive/1_Project_running_/014_Stremlit_Python_web_Application_for_Finance/vsc/test_output/"
        target_directory_result = "G:/My Drive/1_Project_running_/014_Stremlit_Python_web_Application_for_Finance/vsc/result/"

        shutil.move(self.filename_ticker,
                    target_directory_test+self.filename_ticker)
        shutil.move(self.filename_parameter,
                    target_directory_test+self.filename_parameter)
        shutil.move(self.filename_result,
                    target_directory_result+self.filename_result)
        return self.output_to_screen
       
       
# Use !gupload command to upload a file to Google Drive
# !gupload [local_file_path] [drive_folder_path]
# gupload has some problem needs to mount the google drive. so letu use shutil only as of now
