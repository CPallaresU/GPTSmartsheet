import smartsheet
from pyChatGPT import ChatGPT
import time
import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver





column_map = {}

# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)

def evaluate_row_and_build_updates(source_row):
    # Find the cell and value we want to evaluate
    request_cell = get_cell_by_column_name(source_row, "Request")
    request_value = request_cell.display_value

    response_cell = get_cell_by_column_name(source_row, "Response")
    response_value = response_cell.display_value

    if request_value != None and response_value == None:
        #gpt_prompt = api.send_message(request_value)  # ChatGPT Prompt
        #gpt_response=gpt_prompt['message'] # ChatGPT Response
        completion = openai.Completion.create(model="text-davinci-003",prompt=request_value,max_tokens=2048)
    
        # Build new cell value
        new_cell = smart.models.Cell()
        new_cell.column_id = column_map["Response"]
        new_cell.value = completion.choices[0].text #gpt_response

        # Build the row to update
        new_row = smart.models.Row()
        new_row.id = source_row.id
        new_row.cells.append(new_cell)

        print("################")
        print(new_row)
        return new_row
    



openai.api_key="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"



count=0
while True:
    ######## Auth for Smartsheet and ChatGPT ########



    #chatgpt_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..PKzFCO6Iofg6EjDO.HOxB0JBXR0jrHiMQW1vNUPHuuzzTCntQEwn_LBiV1W0oqEURBabsc_6Fl77guKdIQZuzvbPUFz1kM6DIsL3fPDRZH3tlfjMuo1poMsI9_mc_apoL_TPu5VyRw4mbkmWDN_FcesjpylgIGCXsax5fbDXQi14WgJuydckLCNysK7H7hqdFeMrYtpQSaEAc3CVKCTnCa9S5DAZpOSJ0lowGc8a3s5dl2qucakZBRSM7KyXlsbpxkAXyTIMFYptFvm8Yd6b9SigAeLCSe4AICG8Nol1aR9GSnhs5nVXNJVQ2gh2gksSonURJMZDLlcBkueduHzfTvkLpgayz2NQD8nfsBLskDOBRNcaN-Cz75qyU602TIg3QqOFYCosVq9AMiOc5p78Z8akAnu9LjyN0HLMIFBxVAWtsAeS1GdoG5n6gDChfBVi9FPcRlL_U0Ouwl3p8wG2IRgHdsrj0uHtx1aRVaHck4S2gSP_l29RIisys_vBK9xIKB0T3vDPr4dLZkw1EvUniijAEGfELRUnEyfxnzGbb_pGh3DeXCWmESvhswbPuKQDANHVEqsp48wYxkkxuoQOHJXXfL1SsAda2-Wp3iv2dNUsbMudprJI_K3Ky0ulcPPGcKJQRVkeYoVQypx8apNDTtrJqL3c6vrZVIpsYKIxJtVnyOD3IuxnJIfW9BDBUGS0B5rMQuhFKGn-Be4ptzYgwlU-CqzALAzyDiYIjr54zlkJaBccSgwk2UmNoxcEMx2knal05befE5oeKO-kYYEYWmiCCJzHQCprpVBnCK98IUQkFu0oBcablydjLYW7F-ygY_MlpfQ1o8Nr7YTpcl03gLnbwmNV9PusXnuyPDEDKvcIpG1fBB28iqTW8jqOOaIZLFeZ9u842zy8SEg4afnZv2Sudh7j3Y5AkCQfm0M8YrO3l9DDnv3HW83g2q9lwEM_OEs5cd9L0qtY8lIgzNmvjMQ3jON5_IbHU7DNRxOKeqYyNdwrvlBcFX6PiJsPFMX56evLgplO9KxE8u3XEqaMqczri1V8wWNqFlu5ghWV3ZrEhbPsG41Nn2hObVveXD-15cjhbFMIo2CSr7T9imLuFZHVmhPSLjBc9J8WAVwj7sC8XQD0dcvRDpYtJG2oQ2h9G61QR3Ku-lC4hZ4N8vqHV-bYjUMmKXdkbav9WKvjeHSv7LQU3LwIgQtikV-3gJFto86L7zskAZ6JOy0N28Qt208dHRmWc2LCoWvaZBQ7Ob97RdWX2oWV1KzsvWAoVhMQyIialU1buR-R_VxPqsAr_cn9RIdsO9PNes3OnXVvlKYp5VukLFZf1xc3nHmci0vuCfIYQhd7UH8iLUaKoLVX85_Dy9yvbanIsdlY4Nd8a4Kvjk8PXZXmR5S0F_sEaMVCWbt5nWP-lh4mzYM1VQxtMu5YtdvlQhavTZPFBWvYkpsIhcFvssf2HolqnSIbgoyXh3WZxxROv3Yae8EnvE2guM8eAuy5k7fSiJ4Y8TjV9MzQDMH3FGPofF5-O-4hsGSZ5CEf-esDmS542fzpcSxx0M13Sqvu9kERsRiLNP4EdqvPjrY6b3YeWploAhQQ1Y3b036f7XbeKJ1HcQXgep9wzVwn4KaGB5DMGnu5IFxV2BfEJqtoTjdG_-lwdOjlCnjG6ZEttnLmPFQcCGD08LatR2JRgRjj6szpBiM8nhB2zNBnItfEwnxRmRkFlLXOs-CmqYyzCfux-gyOl1Iw-jVWFigQR28g8XO7b_ISE1LsqE5jWIS84wqZ9TOQZusibJOrhNYPDz8W28kK8IKxSNz8onaDYYFgTt5hH74Ep-FRV8_QPiOSs8n7yEpBtOP2HXRES1jZf7AWTWSfOG6OTOlEn8yg9zHZHmVLU8bVlnes2E-2cI8cD3YD2JoTZ3TMbaka2kipPqNqEaNbXydzhqlp_YS-TZCgQi9sestHqE23sQCyHhIA2mrFDzTGz_9VM0affUfYanv6UCEXTk8_P-pLeX4PR2Y6U3SbZeLMA0XfLRZEgreJJD_dEeno5ef5VPUrZXNjfwNIQcWGmbVdpkdc60r_FhMLqPNLY7qoaaWmpugBlp0EKNjomHq_iqq10hWy_Zc1HV566gYRhyfrYFjouK3EYGQWi9BPRCiRfC4HrscHzDXGxhNOGE_CKZmaHDGtjK0dyKuxsBtPjpNYtnnMRwadqajyKEgn072KTMpwFD9OcUsba5dVB1qLdp0nLcCO-4z9sZN2nwu89Fj5KG2JZ0xEF04OPl8f6IxlykjTpbsjwTikeo5bi_V_tD2s4CvfMHl8GTRoSToOXF48H1H-Mqe8w5JueYHWJlRqylWMgw0CHDI1NTn4lQ4fm1y2QaBXVP_Xwz4QDGH4tk4H-oOx5_iMHjgDYslBQyfId5w8JC_oowMCecTHVTXBiUW43JxWiIOErbPUXKbU3W2az_ok3xZeM3X8msF9EjknwYhTdGrAsArtACjYU_WHigCX6UV0rkJC-vHiW51ZPH95VLMHb9F95Na-NsX8ZtTW1DSVqpelaXwLxxaLPaUYVg9AwY4X_Giudbm96dtJBtVlZ8g.ZZhsKVwJGdY3VKqG6M55BQ"
    #api=ChatGPT(chatgpt_token)

    smart = smartsheet.Smartsheet("RJwq7hX5mKtd5qS9yEtmRXbCauzkTVza3uyV7")             # Create a Smartsheet client 

    response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
    sheetId = response.data[0].id               # Get the ID of the first sheet in the response
    sheet = smart.Sheets.get_sheet(4650849919100804)     # Load the sheet by using its ID

    ######## Auth for Smartsheet and ChatGPT ########

    for column in sheet.columns:
        column_map[column.title] = column.id

    rowsToUpdate = []

    for row in sheet.rows:
        print(row)
        rowToUpdate = evaluate_row_and_build_updates(row)
        if rowToUpdate is not None:
            rowsToUpdate.append(rowToUpdate)

    # Finally, write updated cells back to Smartsheet
    if rowsToUpdate:
        print("Writing " + str(len(rowsToUpdate)) + " rows back to sheet id " + str(sheet.id))
        result = smart.Sheets.update_rows(4650849919100804, rowsToUpdate)
    else:
        print("No updates required")
    count+=1
    #api.reset_conversation()
    time.sleep(20)
    print("Cycle: #"+str(count))

    break



