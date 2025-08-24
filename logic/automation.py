import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tkinter import messagebox
import time 
import traceback
class Ticket:
    def __init__(self, org_sn, new_sn, new_pn):
        self.org_sn = org_sn
        self.new_sn = new_sn
        self.new_pn = new_pn
        self.close_date = time.strftime("%Y-%m-%d")

class Automation:

    def __init__(self, config):
        self.config = config
        self.driver = None
        self.progress_queue = None

    def login(self,username, password, chrome_path, driver_path):
        """
        Log in to the UCS system using provided credentials and paths.
        
        Args:
            username (str): The username for login.
            password (str): The password for login.
            chrome_path (str): The path to the Chrome browser executable.
            driver_path (str): The path to the ChromeDriver executable.
        
        Returns:
            webdriver.Chrome: An instance of the Chrome WebDriver after successful login.
        """
        print("start login...")
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        
        self.driver.get(self.config["login_url"])  # Replace with actual UCS login URL
        self.driver.maximize_window()
        # Locate username and password fields and login button
        
        wait = WebDriverWait(self.driver, self.config['page_load'])

        # Handle iframe if present
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        if len(iframes) > 0:
            #self.progress_queue.put(("log", f"Found {len(iframes)} iframe(s), switching to first one...", "info"))
            self.driver.switch_to.frame(iframes[0])
            
        try:
            account_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#\\2f login_username")))
            password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#\\2f login_pazwod")))
            
            #self.progress_queue.put(("log", "Filling in credentials...", "info"))
            account_input.clear()
            account_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
        except Exception as login_error:
            self.progress_queue.put(("log", f"Login form error: {login_error}", "error"))
            return False
        
        return True
    def __check_ticket_exists(self):
        try:
            error_element = self.driver.find_element_by_css_selector(
                "body > div.MuiDialog-root-22 > div.MuiDialog-container-25.MuiDialog-scrollPaper-23 > div > div > div.MuiBox-root-119.jss818.jss20 > span"
            )
            # If element is found, show error dialog
            if error_element.is_displayed():
                #print("Ticket Error: The ticket does not exist. Please search the Org SN# in the account Atravesar_01")
                return False
        except NoSuchElementException:
            # If not found, no error - ticket likely exists
            return True
    def __isECN(self):

        """
        Check the ticket type to determine if it is an ECN (Engineering Change Notice).
        If there is a mandatory item in ECN list, return True.


        """
        
        return False

    def search(self, sn):
        try:
            wait = WebDriverWait(self.driver, self.config['page_load'])

            search = wait.until(EC.presence_of_element_located((By.ID, "barcodeTextField_searchCondition")))
            search.clear()
            search.send_keys(sn)
            search.send_keys(Keys.ENTER)
            if self.__check_ticket_exists() is False:
                raise ValueError("The ticket does not exist. Please search the Org SN# in the account Atravesar_01")
            
        except Exception as search_error:
            #self.progress_queue.put(("log", f"Search error: {search_error}", "error"))
            return False
        return True
    def append_record_to_excel_txt(self, ticket, status, failure_reason, file_path='../EXCEL.txt'):
        row = f"{ticket.org_sn}\t{ticket.new_sn}\t{ticket.new_pn}\tclosed\t{ticket.close_date}\t{status}\t{failure_reason}\n"
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(row)
    def close_ticket(self, batch_list):
        wait = WebDriverWait(self.driver, self.config['page_load'])
        # 1. Users using GUI to enter the scan org SN# and new SN# of the ticket.
        # 2. Users select the ticket type (e.g., Normal Pass, ECN Pass, Fail).
        # tuple list of (org_sn, new_sn, pass_type)
        for record in batch_list:
            org_sn, new_sn, pass_type = record
            try:
                # Search by New SN# 
                # If the ticket is not found, it raises an error.
                print("Search SN#")
                if not self.search(new_sn) :
                    continue 

                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiBackdrop-root-2")))
                # If Org SN# and the input field of ORG SN# in UCS are not matched, it raises an error.
                org_sn_in_page_element = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.refurbish_orgSn")))
                time.sleep(1)
                org_sn_in_page = org_sn_in_page_element.get_attribute("value")
                if org_sn_in_page.endswith(org_sn) is False:
                    print(f"Org SN# mismatch for ticket {new_sn}. Expected: {org_sn}, Found: {org_sn_in_page}")
                    continue
                # checks if the ticket type is ECN. It checks if there are mandatory items in the ECN list.
                print("Check ECN...")
                isECN = self.__isECN()

                if pass_type == 'Normal':
                    if isECN:  #If user selected Normal Pass but the ticket is an ECN, it raises an error.
                        print("This ticket is ECN, but user selected Normal Pass. Please check again.")
                        continue
                    else:
                        # Process Normal Pass
                        self.close_normal_ticket()
                        pass
                elif pass_type == 'ECN':
                    if not isECN: # If user selected ECN but the ticket is not an ECN, it raises an error.
                        print("This ticket is not ECN, but user selected ECN Pass. Please check again.")
                        continue
                    else:
                        # Process ECN Pass
                        self.close_ecn_ticket()
                        pass

                #generate log record in excel.txt   
                '''
                    - Org SN
                    - New SN
                    - New PN
                    - Ticket Type
                    - Status
                    - Closed Time
                    - Result
                    - Failure Reason (if any)
                '''
                time.sleep(self.config['request_delay'])  # Delay between requests
                
                print(f"Ticket {new_sn} processed successfully.")
                # Add logic to verify org_sn matches and ticket type
                # Add logic to close the ticket based on pass_type
                # Log success or failure for each ticket
            except Exception as e:
                # Log the exception for this ticket
                print(f"Error processing ticket {new_sn}: {str(e)}")
                traceback.print_exc()

    def close_normal_ticket(self):
        wait = WebDriverWait(self.driver, self.config['page_load'])
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "MuiBackdrop-root-2")))
        #RN not match: /repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.rn_repair.dic.rnMatch.match
        wait.until(EC.element_to_be_clickable((By.ID, "/repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.rn_repair.dic.rnMatch.notMatch"))).click()

        #Save RN
        wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.rn_common.static.general.save"))).click()
        time.sleep(self.config['request_delay'])  # Delay between requests
        #Add Repair Detail: /repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.repairDetail_common.static.general.add
        wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_common.static.general.repair_repair.static.repair.repairDetail_common.static.general.add"))).click()

        #1./repair/operation/rma/create/repair_Add Repair Detail_claimGroup
        f1 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_claimGroup")))
        time.sleep(1)
        f1.send_keys("[NBZU00] Software / OS error")
        f1.send_keys(Keys.DOWN)
        f1.send_keys(Keys.ENTER)

        #2. /repair/operation/rma/create/repair_Add Repair Detail_claimCode
        f2 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_claimCode")))
        time.sleep(1)
        f2.send_keys("[NBZU99] Other OS (Software) issue")
        f2.send_keys(Keys.DOWN)
        f2.send_keys(Keys.ENTER)

        f3 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_problemGroup")))
        time.sleep(1)
        f3.send_keys("[N0Z000] Test ok")
        f3.send_keys(Keys.DOWN)
        f3.send_keys(Keys.ENTER)

        f4 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_problemCode")))
        time.sleep(1)
        f4.send_keys("[N0Z000]Test ok")
        f4.send_keys(Keys.DOWN)
        f4.send_keys(Keys.ENTER)

        f5 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_actionGroup")))
        f5.send_keys("[N] NTF")
        f5.send_keys(Keys.DOWN)
        f5.send_keys(Keys.ENTER)

        f6 = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_actionCode")))
        f6.send_keys("[N05] Cannot duplicate the symptom, and update Software/ Firmware/ BIOS") 
        f6.send_keys(Keys.DOWN)
        f6.send_keys(Keys.ENTER)

        #Save Repair Detail
        save_detail = wait.until(EC.presence_of_element_located((By.ID, "/repair/operation/rma/create/repair_Add Repair Detail_common.static.general.submit")))
        save_detail.click()




        '''
            Psuedo code of closing a single ticket is below:

            1. Users using GUI to enter the scan org SN# and new SN# of the ticket.
            2. Users select the ticket type (e.g., Normal Pass, ECN Pass, Fail).
            3. Search by New SN#
                1. If the ticket is not found, it raises an error.
                2. If Org SN# is not matched, it raises an error.
            4. Program checks if the ticket type is ECN. It checks if there are mandatory items in the ECN list.
                1. If user selected ECN but the ticket is not an ECN, it raises an error.
                2. If user selected Normal Pass but the ticket is an ECN, it raises an error.
            5a. If it is a Normal Pass, Do the following:
                1. In IRN list, check all items.
                2. In ECN list, select [Do not match the condition] for conditional items.
                3. In Repair Detail, fill the fields:
                    - Claim Group: [NBZU00] Software / OS error
                    - Claim Code: [NBZU99] Other OS(Software) issues
                    - Problem Group: [N0Z000] Test ok
                    - Problem Code: [N0Z000]Test ok
                    - Action Group: [N] NTF
                    - Action Code: [N05] Cannot duplicate the symptom
            5b. If it is an ECN Pass, Do the following:
                1. In IRN list, check all items.
                2. In ECN list, select [Do not match the condition] for conditional items; select [Part Shortage] for all mandatory items.
                3. In Repair Detail, fill the fields:
                    - Claim Group: [NBZU00] Software / OS error
                    - Claim Code: [NBZU01] Boot hangs at ASUS logo
                    - Problem Group: [N0FZ00] Other Error
                    - Problem Code: [N0FZZZ] inspection Fail
                    - Action Group: [F] Repair Failed
                    - Action Code: [F20] Cannot duplicate the symptom
                    - Org PN: (Org PN of the ticket)
                4. Click the Memo button, Enter `Sent to ECN(pass)` in Problem Description.
            6. Click Next to proceed.
            7a. Check WTP result.
                1. if it pass the test, click Confirm result.
                2. if it fails the test, it raises an error that test is not finish.
            7b. Click Confirm result directly.
            8. Click No to the question "Do you want to move to Ship state?".
            9. Complete the ticket.
            10. add a row of recoed in excel.txt with the following information:
                - Org SN
                - New SN
                - New PN
                - Ticket Type
                - Status
                - Closed Time
                - Result
                - Failure Reason (if any)

        '''

