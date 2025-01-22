import db_access

import sys
import os
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic


## python실행파일 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from_class = uic.loadUiType(BASE_DIR + r'/base.ui')[0]

# MainWindow Class 선언
class WindowClass(QWidget, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# --------------------db server info --------------------------#
        self.host_name = 'localhost'
        self.user_name = 'root'
        self.password = '0329'
        self.database_name = 'dbtermproject'
        self.port_number = 3305


# -------------------- db tab refresh --------------------------#
        self.MainTab: QTabWidget
        self.MainTab.tabBarClicked.connect(self.maintab_clicked)


# ------------------- Machine Information ---------------------#
        self.tableWidget_3: QTableWidget
        self.pushButton_10: QPushButton 
        self.comboBox_7: QComboBox

        self.pushButton_10.clicked.connect(self.load_machine_information)

        self.load_machine_information()

# ------------------- Vendor Information ---------------------#
        self.sort_vendor_combo_box: QComboBox = self.comboBox_10  
        self.vendor_table_widget: QTableWidget = self.tableWidget_6  
        self.confirm_vendor_button: QPushButton = self.pushButton_13 

        self.confirm_vendor_button.clicked.connect(self.load_vendor_information)

        self.sort_vendor_combo_box.setCurrentText("Highest Trading Volume")
        self.load_vendor_information()

# ------------------- Technician Information ---------------------#
        self.sort_technician_combo_box: QComboBox
        self.technician_table_widget: QTableWidget
        self.confirm_technician_button: QPushButton

        self.confirm_technician_button.clicked.connect(self.load_technician_info_table)

        self.sort_technician_combo_box.setCurrentText("Most Worked") 
        self.load_technician_info_table()
        
# ------------------- Order - Purchase ---------------------#
        self.purchase_button: QPushButton = self.pushButton_3 
        self.add_product_button: QPushButton = self.pushButton_4  
        self.remove_button: QPushButton = self.pushButton_5

        self.product_combo_box: QComboBox = self.comboBox 
        self.vendor_combo_box: QComboBox = self.comboBox_2  

        self.price_text_browser: QTextBrowser = self.textBrowser_6  
        self.vendor_address_text_browser: QTextBrowser = self.textBrowser_2  
        self.tel_text_browser: QTextBrowser = self.textBrowser_3 
        self.fax_text_browser: QTextBrowser = self.textBrowser_4

        self.qty_spin_box: QSpinBox = self.spinBox  
        self.order_table_widget: QTableWidget = self.tableWidget 
        self.total_order_amount_text_browser: QTextBrowser = self.textBrowser_5

        self.order_id_text_browser: QTextBrowser = self.textBrowser
        self.date_edit: QDateEdit = self.dateEdit 

        self.load_products_and_vendors()
        self.product_combo_box.currentIndexChanged.connect(self.update_product_details)
        self.vendor_combo_box.currentIndexChanged.connect(self.update_vendor_details)
        self.add_product_button.clicked.connect(self.add_product_to_table)
        self.purchase_button.clicked.connect(self.create_order)
        self.purchase_button.clicked.connect(self.set_order_id)
        self.remove_button.clicked.connect(self.remove_selected_product)

        self.set_today_date()
        self.set_order_id()

        self.initialize_vendor_and_product_details()

# ------------------- Order - Machine Install/Remove ---------------------#
        self.machine_move_id_text_browser: QTextBrowser = self.textBrowser_7
        self.machine_list_table_widget: QTableWidget = self.tableWidget_2
        self.selected_machine_text_browser: QTextBrowser = self.textBrowser_8
        self.location_combo_box: QComboBox = self.comboBox_3
        self.move_type_combo_box: QComboBox = self.comboBox_4
        self.technician_combo_box: QComboBox = self.comboBox_5
        self.movedate_dateedit: QDateEdit = self.dateEdit_2
        self.machine_move_cancel_pushbuttom: QPushButton = self.pushButton_8
        self.machine_move_confirm_pushbutton: QPushButton = self.pushButton_7

        self.set_machine_move_id()
        self.load_machine_info_table()
        self.load_location_information()
        self.load_technician_information()
        self.load_date()
        self.machine_list_table_widget.clicked.connect(self.update_machine_name_browser)
        self.machine_move_confirm_pushbutton.clicked.connect(self.moveorder_confirm)
        self.machine_move_confirm_pushbutton.clicked.connect(self.set_machine_move_id)
        self.machine_move_cancel_pushbuttom.clicked.connect(self.moveorder_cancel)
        self.move_type_combo_box.currentIndexChanged.connect(self.move_type_changed)



# ------------------- History - Purchase Order History ---------------------#
        self.order_history_table_widget: QTableWidget = self.tableWidget_4
        self.order_history_confirm_pushButton: QPushButton = self.pushButton_11
        self.order_history_year_combo_box: QComboBox = self.comboBox_8
    
        self.load_purchase_year()
        self.order_history_confirm_pushButton.clicked.connect(self.load_purchase_order_table_byyear)

# ------------------- History - Purchase Order History ---------------------#
        self.move_history_table_widget: QTableWidget
        self.move_history_confirm_pushButton: QPushButton
        self.move_history_year_combo_box: QComboBox

        self.load_move_year()
        self.move_history_confirm_pushButton.clicked.connect(self.load_move_order_table_byyear)



# -----------------------------------------------------------------------------------------------------------------------------------------------------#
# DEF: DB refresh ###################################
# -----------------------------------------------------
    # main tab clicked
    def maintab_clicked(self):
        self.load_machine_information()
        self.sort_vendor_combo_box.setCurrentText("Highest Trading Volume")
        self.load_vendor_information()
        self.sort_technician_combo_box.setCurrentText("Most Worked")
        self.load_technician_info_table()

        self.load_machine_info_table()

        self.load_purchase_year()
        self.load_move_year()




# DEF:  Machine Information ---------------------------------------------------------#
    def display_table_widget(self, table, sql_query):
        db_access.init_table_widget(table, sql_query)
    sql_query = ""
    def load_machine_information(self):
        sort_criteria = self.comboBox_7.currentText()
        if sort_criteria == "Business Location":
            sql_query = """
                SELECT 
                    m.Machine_ID, p.Product_name AS Name, b.Location_name AS Location, 
                    m.Machine_condition AS `Condition`, m.Pur_date AS `Pur. Date`, 
                    p.Manufacturer AS Manuf, m.Cost 
                FROM 
                    Machine m
                LEFT JOIN 
                    Business_Location b ON m.Location_ID = b.Location_ID 
                JOIN 
                    Product p ON m.Product_ID = p.Product_ID 
                ORDER BY 
                    b.Location_name IS NULL, b.Location_name
            """
        elif sort_criteria == "Machine Name Ascending":
            sql_query = """
                SELECT 
                    m.Machine_ID, p.Product_name AS Name, b.Location_name AS Location, 
                    m.Machine_condition AS `Condition`, m.Pur_date AS `Pur. Date`, 
                    p.Manufacturer AS Manuf, m.Cost 
                FROM 
                    Machine m
                LEFT JOIN 
                    Business_Location b ON m.Location_ID = b.Location_ID 
                JOIN 
                    Product p ON m.Product_ID = p.Product_ID 
                ORDER BY 
                    p.Product_name
            """
        
        self.display_table_widget(self.tableWidget_3, sql_query)

# DEF:  Vendor Information ---------------------------------------------------------#
    def load_vendor_information(self):
        sort_criteria = self.sort_vendor_combo_box.currentText()
        sql_query = ""
        if sort_criteria == "Highest Total Sales Amount":
            sql_query = """
                SELECT 
                    v.Vendor_ID, v.Vendor_name, COUNT(po.Pur_order_ID) AS `No. of Worked`, 
                    v.Vendor_address AS Address, v.Fax_No AS `Fax No`, 
                    COALESCE(SUM(popq.Quantity * p.Unit_price), 0) AS `Total Sales Amount`
                FROM 
                    Vendor v
                LEFT JOIN 
                    Purchase_Order po ON v.Vendor_ID = po.Vendor_ID
                LEFT JOIN 
                    Purchase_Order_Product_Quantity popq ON po.Pur_order_ID = popq.Pur_order_ID
                LEFT JOIN 
                    Product p ON popq.Product_ID = p.Product_ID
                GROUP BY 
                    v.Vendor_ID
                ORDER BY 
                    `Total Sales Amount` DESC
            """
        elif sort_criteria == "Lowest Total Sales Amount":
            sql_query = """
                SELECT 
                    v.Vendor_ID, v.Vendor_name, COUNT(po.Pur_order_ID) AS `No. of Worked`, 
                    v.Vendor_address AS Address, v.Fax_No AS `Fax No`, 
                    COALESCE(SUM(popq.Quantity * p.Unit_price), 0) AS `Total Sales Amount`
                FROM 
                    Vendor v
                LEFT JOIN 
                    Purchase_Order po ON v.Vendor_ID = po.Vendor_ID
                LEFT JOIN 
                    Purchase_Order_Product_Quantity popq ON po.Pur_order_ID = popq.Pur_order_ID
                LEFT JOIN 
                    Product p ON popq.Product_ID = p.Product_ID
                GROUP BY 
                    v.Vendor_ID
                ORDER BY 
                    `Total Sales Amount` ASC
            """
        else:
            sql_query = """
                SELECT 
                    v.Vendor_ID, v.Vendor_name, COUNT(po.Pur_order_ID) AS `No. of Worked`, 
                    v.Vendor_address AS Address, v.Fax_No AS `Fax No`, 
                    COALESCE(SUM(popq.Quantity * p.Unit_price), 0) AS `Total Sales Amount`
                FROM 
                    Vendor v
                LEFT JOIN 
                    Purchase_Order po ON v.Vendor_ID = po.Vendor_ID
                LEFT JOIN 
                    Purchase_Order_Product_Quantity popq ON po.Pur_order_ID = popq.Pur_order_ID
                LEFT JOIN 
                    Product p ON popq.Product_ID = p.Product_ID
                GROUP BY 
                    v.Vendor_ID
            """
    
        self.display_table_widget(self.vendor_table_widget, sql_query)

# DEF:  Technician Information ---------------------------------------------------------#
    def load_technician_info_table(self):
        sort_criteria = self.sort_technician_combo_box.currentText()
        sql_query = ""
        if sort_criteria == "Most Worked":
            sql_query = """
                SELECT 
                    t.Technician_ID,
                    t.Technician_name, 
                    COUNT(o.Order_ID) AS `No. of Worked`
                FROM 
                    Technician t
                LEFT JOIN 
                    `Order` o ON t.Technician_ID = o.Technician_ID
                GROUP BY 
                    t.Technician_ID
                ORDER BY 
                    `No. of Worked` DESC, t.Technician_ID ASC
            """
        elif sort_criteria == "Technician Name Ascending":
            sql_query = """
                SELECT 
                    t.Technician_ID,
                    t.Technician_name, 
                    COUNT(o.Order_ID) AS `No. of Worked`
                FROM 
                    Technician t
                LEFT JOIN 
                    `Order` o ON t.Technician_ID = o.Technician_ID
                GROUP BY 
                    t.Technician_ID
                ORDER BY 
                    t.Technician_name ASC
            """
        elif sort_criteria == "Technician ID Ascending":
            sql_query = """
                SELECT 
                    t.Technician_ID,
                    t.Technician_name, 
                    COUNT(o.Order_ID) AS `No. of Worked`
                FROM 
                    Technician t
                LEFT JOIN 
                    `Order` o ON t.Technician_ID = o.Technician_ID
                GROUP BY 
                    t.Technician_ID
                ORDER BY 
                    t.Technician_ID ASC
            """
        self.display_table_widget(self.technician_table_widget, sql_query)


# DEF: Order - Purchase ---------------------------------------------------------#
    def load_products_and_vendors(self):
        product_sql = "SELECT Product_ID, Product_name FROM Product"
        vendor_sql = "SELECT Vendor_ID, Vendor_name FROM Vendor"

        products_table = QTableWidget()
        vendors_table = QTableWidget()

        db_access.init_table_widget(products_table, product_sql)
        db_access.init_table_widget(vendors_table, vendor_sql)

        # Clear the combo boxes before adding new items
        # self.product_combo_box.clear()
        # self.vendor_combo_box.clear()

        for row in range(products_table.rowCount()):
            product_id = products_table.item(row, 0).text()
            product_name = products_table.item(row, 1).text()
            self.product_combo_box.addItem(product_name, product_id)

        for row in range(vendors_table.rowCount()):
            vendor_id = vendors_table.item(row, 0).text()
            vendor_name = vendors_table.item(row, 1).text()
            self.vendor_combo_box.addItem(vendor_name, vendor_id)

    def update_product_details(self):
        product_id = self.product_combo_box.currentData()
        sql_query = f"SELECT Unit_price FROM Product WHERE Product_ID = {product_id}"
        product_table = QTableWidget()
        db_access.init_table_widget(product_table, sql_query)
        if product_table.rowCount() > 0:
            price = product_table.item(0, 0).text()
            self.price_text_browser.setText(price)

    def update_vendor_details(self):
        vendor_id = self.vendor_combo_box.currentData()
        sql_query = f"SELECT Vendor_address, Tel_No, Fax_No FROM Vendor WHERE Vendor_ID = {vendor_id}"
        vendor_table = QTableWidget()
        db_access.init_table_widget(vendor_table, sql_query)
        if vendor_table.rowCount() > 0:
            vendor_address = vendor_table.item(0, 0).text()
            tel_no = vendor_table.item(0, 1).text()
            fax_no = vendor_table.item(0, 2).text()
            self.vendor_address_text_browser.setText(vendor_address)
            self.tel_text_browser.setText(tel_no)
            self.fax_text_browser.setText(fax_no)
            
    def initialize_vendor_and_product_details(self):
        if self.product_combo_box.count() > 0:
            self.product_combo_box.setCurrentIndex(0)
            self.update_product_details()
        if self.vendor_combo_box.count() > 0:
            self.vendor_combo_box.setCurrentIndex(0)
            self.update_vendor_details()


    def reset_order_fields(self, complete_order=False):
        # Reset product combo box to first item
        if self.product_combo_box.count() > 0:
            self.product_combo_box.setCurrentIndex(0)
            self.update_product_details()

        # Reset vendor combo box to first item
        if self.vendor_combo_box.count() > 0:
            self.vendor_combo_box.setCurrentIndex(0)
            self.update_vendor_details()

        # Reset quantity spin box
        self.qty_spin_box.setValue(1)

        if complete_order:
            # Clear the order table
            self.order_table_widget.setRowCount(0)
            # Clear the total order amount
            self.total_order_amount_text_browser.clear()


    def add_product_to_table(self):
        product_name = self.product_combo_box.currentText()
        product_id = self.product_combo_box.currentData()
        manufacturer = self.get_product_manufacturer(product_id)  # Assume this function gets the manufacturer from the database
        price = float(self.price_text_browser.toPlainText())
        qty = self.qty_spin_box.value()
        total_price = round((price * qty),2)

        existing_row = -1
        for row in range(self.order_table_widget.rowCount()):
            if self.order_table_widget.item(row, 0).text() == str(product_id):
                existing_row = row
                break

        if existing_row >= 0:
            existing_qty = int(self.order_table_widget.item(existing_row, 4).text())
            new_qty = existing_qty + qty
            new_total_price = round((price * new_qty),2)
            self.order_table_widget.setItem(existing_row, 4, QTableWidgetItem(str(new_qty)))
            self.order_table_widget.setItem(existing_row, 5, QTableWidgetItem(str(new_total_price)))
        else:
            row_position = self.order_table_widget.rowCount()
            self.order_table_widget.insertRow(row_position)

            self.order_table_widget.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
            self.order_table_widget.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.order_table_widget.setItem(row_position, 2, QTableWidgetItem(manufacturer))
            self.order_table_widget.setItem(row_position, 3, QTableWidgetItem(str(price)))
            self.order_table_widget.setItem(row_position, 4, QTableWidgetItem(str(qty)))
            self.order_table_widget.setItem(row_position, 5, QTableWidgetItem(str(total_price)))

        self.update_total_order_amount()
        self.qty_spin_box.setValue(1)

    def get_product_manufacturer(self, product_id):
        sql_query = f"SELECT Manufacturer FROM Product WHERE Product_ID = {product_id}"
        product_table = QTableWidget()
        db_access.init_table_widget(product_table, sql_query)
        if product_table.rowCount() > 0:
            manufacturer = product_table.item(0, 0).text()
            return manufacturer
            
    def remove_selected_product(self):
        selected_row = self.order_table_widget.currentRow()
        if selected_row >= 0:
            self.order_table_widget.removeRow(selected_row)
            self.update_total_order_amount()

    def update_total_order_amount(self):
        total_amount = 0.0
        for row in range(self.order_table_widget.rowCount()):
            total_amount += round(float(self.order_table_widget.item(row, 5).text()),2)
        total_amount = round(total_amount, 2)
        self.total_order_amount_text_browser.setText(str(total_amount))

    def set_today_date(self):
        today = datetime.today().date()
        self.date_edit.setDate(today)
        self.date_edit.setMinimumDate(today)

    # order_id 채우기
    def set_order_id(self):
        self.order_id_text_browser.clear()

        # connect db
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT MAX(Pur_order_ID) AS NewOrderID FROM Purchase_Order
                """
                cursor.execute(sql_query)
                result = cursor.fetchall()
                max = result[0]['NewOrderID']
                # 오늘 날짜의 yyddmm 형식을 가져옴
                date_str = datetime.today().date().strftime('%y%m%d')

                if str(max)[:6] == date_str:
                    # 번호를 3자리로 포맷팅 (0으로 채움)
                    order_number_str = str(int(str(max)[6:])+1).zfill(3)
                    # ID 생성
                    order_id = date_str + order_number_str
                    self.order_id_text_browser.append(order_id)
                else:
                    self.order_counter = 1
                    # 번호를 3자리로 포맷팅 (0으로 채움)
                    order_number_str = str(self.order_counter).zfill(3)
                    # ID 생성
                    order_id = date_str + order_number_str
                    self.order_id_text_browser.append(order_id)

        except Exception as e:
            pass

    def create_order(self):
        try:
            order_id = self.order_id_text_browser.toPlainText()
            vendor_id = self.vendor_combo_box.currentData()
            date = self.date_edit.date().toString("yyyy-MM-dd")
            total_amount = self.total_order_amount_text_browser.toPlainText()

            # Check if any variable is empty or None
            if not total_amount or total_amount=="0.0":
                raise ValueError("You haven't choose a product")

            connection = db_access.connect_db(host_name=self.host_name,
                                            user_name=self.user_name,
                                            pw=self.password,
                                            db_name=self.database_name,
                                            port_num=self.port_number)

            try:
                with connection.cursor() as cursor:
                    # Insert into Purchase_Order
                    po_sql = f"""INSERT INTO Purchase_Order (Pur_order_ID, Vendor_ID, Date) 
                                VALUES ({order_id}, {vendor_id}, '{date}')"""
                    cursor.execute(po_sql)

                    # Insert into Purchase_Order_Product_Quantity
                    for row in range(self.order_table_widget.rowCount()):
                        product_id = self.order_table_widget.item(row, 0).text()
                        qty = self.order_table_widget.item(row, 3).text()
                        popq_sql = f"""INSERT INTO Purchase_Order_Product_Quantity (Pur_order_ID, Product_ID, Quantity) 
                                    VALUES ({order_id}, {product_id}, {qty})"""
                        cursor.execute(popq_sql)

                    connection.commit()
                    self.success_pop_up_message()
                    self.reset_order_fields(complete_order=True)
                    self.set_order_id()
            except Exception as e:
                connection.rollback()
                self.fail_pop_up_message(err_msg=str(e))
            finally:
                connection.close()
        except ValueError as ve:
            self.fail_pop_up_message(err_msg=str(ve))
        except Exception as e:
            self.fail_pop_up_message(err_msg=str(e))



# DEF: Order - Machine Install/Remove --------------------------------------------------------------#
    # machine info 테이블 채우기
    def load_machine_info_table(self):
        sql_query = """
                SELECT 
                    m.Machine_ID, p.Product_name AS Name, b.Location_name AS Location, 
                    m.Machine_condition AS `Condition`, m.Pur_date AS `Pur. Date`, 
                    p.Manufacturer AS Manuf, m.Cost 
                FROM 
                    Machine m
                LEFT JOIN 
                    Business_Location b ON m.Location_ID = b.Location_ID 
                JOIN 
                    Product p ON m.Product_ID = p.Product_ID 
            """
        
        self.display_table_widget(self.machine_list_table_widget, sql_query)

    # move id 채우기
    def set_machine_move_id(self):
        self.machine_move_id_text_browser.clear()

        # connect db
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT COALESCE(MAX(Order_ID), 0) AS max_orderID FROM `Order`
                """
                cursor.execute(sql_query)
                result = cursor.fetchall()
                max = result[0]['max_orderID']
                # 오늘 날짜의 yyddmm 형식을 가져옴
                date_str = datetime.today().date().strftime('%y%m%d')

                if str(max)[:6] == date_str:
                    # 번호를 3자리로 포맷팅 (0으로 채움)
                    order_number_str = str(int(str(max)[6:])+1).zfill(3)
                    # ID 생성
                    order_id = date_str + order_number_str
                    self.machine_move_id_text_browser.append(order_id)
                else:
                    self.order_counter = 1
                    # 번호를 3자리로 포맷팅 (0으로 채움)
                    order_number_str = str(self.order_counter).zfill(3)
                    # ID 생성
                    order_id = date_str + order_number_str
                    self.machine_move_id_text_browser.append(order_id)

        except Exception as e:
            pass

    # machine name 채우기
    def update_machine_name_browser(self):
        selected_items = self.machine_list_table_widget.selectedItems()

        if selected_items:
            table_index = self.machine_list_table_widget.selectedIndexes()[0].row()  # 현재 클릭된 머신 id 가져오기
            machine_name = self.machine_list_table_widget.item(table_index, 1).text()  # machine name
            self.selected_machine_text_browser.setText(machine_name)
        
            machine_location = self.machine_list_table_widget.item(table_index, 2).text()  # machine location
        
            if self.move_type_combo_box.currentText() == "Remove":
                self.location_combo_box.setCurrentText(machine_location)
                self.location_combo_box.setEnabled(False)
            else:
                self.location_combo_box.setEnabled(True)
                self.location_combo_box.setCurrentText(machine_location)


    def move_type_changed(self):
        selected_items = self.machine_list_table_widget.selectedItems()
        if selected_items:
            table_index = self.machine_list_table_widget.selectedIndexes()[0].row()  # 현재 클릭된 머신 id 가져오기
            machine_location = self.machine_list_table_widget.item(table_index, 2).text()  # machine location

            if self.move_type_combo_box.currentText() == "Remove":
                self.location_combo_box.setCurrentText(machine_location)
                self.location_combo_box.setEnabled(False)
            else:
                self.location_combo_box.setEnabled(True)

    # location comboBox 채우기
    def load_location_information(self):
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT Location_name FROM Business_Location;
                """
                cursor.execute(sql_query)
                result = cursor.fetchall()

                self.location_combo_box.clear()
                # location name을 콤보박스에 설정
                for location in result:
                    self.location_combo_box.addItem(str(location['Location_name']))
                
                self.location_combo_box.addItem("None")
                
        except Exception as e:
            pass
    
    # technician comboBox 채우기
    def load_technician_information(self):
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT Technician_name FROM Technician;
                """
                cursor.execute(sql_query)
                result = cursor.fetchall()

                self.technician_combo_box.clear()
                # technician name을 콤보박스에 설정
                for tech in result:
                    self.technician_combo_box.addItem(str(tech['Technician_name']))

        except Exception as e:
            pass

    # 날짜 박스
    def load_date(self):
        today = datetime.today().date()
        self.movedate_dateedit.setDate(today)
        self.movedate_dateedit.setMinimumDate(today)


    # confirm 버튼 클릭
    def moveorder_confirm(self):
        selected_items = self.machine_list_table_widget.selectedItems()
        if len(selected_items) == 1: # 한 개만 선택되었을 때
            # 현재 선택된 개체 저장 
            order_id = self.machine_move_id_text_browser.toPlainText()
            location_name = self.location_combo_box.currentText()
            move_type = self.move_type_combo_box.currentText()
            technician_name = self.technician_combo_box.currentText()
            movedate = self.movedate_dateedit.date()

            table_index = self.machine_list_table_widget.selectedIndexes()[0].row() # 현재 클릭된 머신 id 가져오기
            machine_id = self.machine_list_table_widget.item(table_index, 0).text() # machine id
            year, month, day = movedate.year(), movedate.month(), movedate.day()
            
            # db 'order' 테이블에 값 저장
            # MySQL에서 날짜 형식인 'YYYY-MM-DD'로 변환
            date_str = f"{year:04d}-{month:02d}-{day:02d}"

            connection = db_access.connect_db(host_name=self.host_name,
                                              user_name=self.user_name,
                                              pw=self.password,
                                              db_name=self.database_name,
                                              port_num=self.port_number)

            
            try:
                with connection.cursor() as cursor:
                    # location의 이름을 보고 location id select
                    loc_sql_query = f'SELECT Location_ID FROM Business_Location WHERE Location_name = "{location_name}"'
                    cursor.execute(loc_sql_query)
                    result = cursor.fetchall()
                    location_id = result[0]['Location_ID']

                    # location 안 바꾸고 현재 location 클릭할 경우
                    current_loc_query = f'SELECT Location_ID FROM Machine WHERE Machine_ID = {machine_id}'
                    cursor.execute(current_loc_query)
                    result = cursor.fetchall()
                    current_location_id = result[0]['Location_ID']
                    if location_id == current_location_id and move_type=='Install':
                        raise ValueError("Change the location to something other than the current one")


                    tech_sql_query = f'SELECT Technician_ID FROM Technician WHERE Technician_name = "{technician_name}"'
                    cursor.execute(tech_sql_query)
                    result = cursor.fetchall()
                    tech_id = result[0]['Technician_ID']

                    insert_sql_query = f'INSERT INTO `Order` VALUES ("{int(order_id)}","{int(location_id)}","{int(tech_id)}","{int(machine_id)}","{move_type}","{date_str}")'
                    cursor.execute(insert_sql_query)

                    # db 'machine' 테이블에 location 값 변경 (move_date가 지나면 location 위치가 바뀜)
                    # [문제] move_date가 지나야 location 위치가 바뀌어야 함!
                    if move_type == 'Install':
                        sql_change_loc = f'UPDATE Machine SET Location_ID = {int(location_id)} WHERE Machine_ID = {int(machine_id)}'
                        cursor.execute(sql_change_loc)
                    elif move_type == "Remove":
                        sql_change_loc = f'UPDATE Machine SET Location_ID = NULL WHERE Machine_ID = {int(machine_id)}'
                        cursor.execute(sql_change_loc)

                    connection.commit()
                    self.success_pop_up_message()
            except Exception as e:
                if location_name == "None" and move_type=="Install":
                    QMessageBox.about(self, 'ERROR', "Select a location except None")
                elif location_name == "None" and move_type=="Remove":
                    QMessageBox.about(self, 'ERROR', "This machine's Location is Already Removed(Location: None)")
                else:
                    connection.rollback()
                    self.fail_pop_up_message(err_msg=str(e))
            finally:
                connection.close()
        else:
            QMessageBox.about(self, 'ERROR', "You haven't selected a machine or selected too many machines")

    # cancel 버튼 클릭
    def moveorder_cancel(self):
        # 현재 선택된 개체 저장 
        self.location_combo_box.setCurrentIndex(0)
        self.move_type_combo_box.setCurrentIndex(0)
        self.technician_combo_box.setCurrentIndex(0)
        self.selected_machine_text_browser.clear()
        today = datetime.today().date()
        self.movedate_dateedit.setDate(today)


    def success_pop_up_message(self):
        QMessageBox.about(self,'Order Confirmation', 'Your order has been successfully placed.')

    def fail_pop_up_message(self, err_msg):
        QMessageBox.about(self,'Order Error', f'There was an error placing your order. \nError Message: {err_msg}')








# DEF:  History - Purchase Order History ---------------------------------------------------------#
    def load_purchase_year(self):
        # connect db
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT DISTINCT YEAR(Date) FROM Purchase_Order ORDER BY YEAR(Date) ASC;
                """
                cursor.execute(sql_query)
                years = cursor.fetchall()

                # 연도 목록을 콤보박스에 설정
                self.order_history_year_combo_box.clear()
                for year in years:
                    self.order_history_year_combo_box.addItem(str(year['YEAR(Date)']))

        except Exception as e:
            pass


    def load_purchase_order_table_byyear(self):
        self.order_history_year_combo_box.model().sort(0)
        year = self.order_history_year_combo_box.currentText()

        sql_query = f"""SELECT po.Pur_order_ID, p.Product_name, p.Unit_price, qty.Quantity, v.Vendor_name, po.Date
        FROM Purchase_Order AS po, Product AS p, Purchase_Order_Product_Quantity AS qty, Vendor AS v
        WHERE po.Pur_order_ID = qty.Pur_order_ID and
        qty.Product_ID = p.Product_ID and
        po.Vendor_ID = v.Vendor_ID and
        YEAR(po.Date) = {year}
        ORDER BY po.Pur_order_ID""" 

        order_history_table_widget = QTableWidget()

        db_access.init_table_widget(order_history_table_widget, sql_query)

        self.order_history_table_widget.setRowCount(order_history_table_widget.rowCount())

        for row in range(order_history_table_widget.rowCount()):
            purchase_id = order_history_table_widget.item(row, 0).text()
            product_name = order_history_table_widget.item(row, 1).text()
            unit_price = order_history_table_widget.item(row, 2).text()
            qty = order_history_table_widget.item(row, 3).text()
            vendor = order_history_table_widget.item(row, 4).text()
            date = order_history_table_widget.item(row, 5).text()

            self.order_history_table_widget.setItem(row, 0, QTableWidgetItem(str(purchase_id)))
            self.order_history_table_widget.setItem(row, 1, QTableWidgetItem(product_name))
            self.order_history_table_widget.setItem(row, 2, QTableWidgetItem(str(unit_price)))
            self.order_history_table_widget.setItem(row, 3, QTableWidgetItem(str(qty)))
            self.order_history_table_widget.setItem(row, 4, QTableWidgetItem(vendor))
            self.order_history_table_widget.setItem(row, 5, QTableWidgetItem(str(date)))
        self.tableWidget.sortByColumn(5, QtCore.Qt.AscendingOrder) # 구매 날짜 기준 오름차순



# DEF:  History - Move Order History ---------------------------------------------------------#
    def load_move_year(self):
        # connect db
        connection = db_access.connect_db(host_name = self.host_name,
                                          user_name = self.user_name,
                                          pw = self.password,
                                          db_name = self.database_name,
                                          port_num= self.port_number
                                          )
        
        try:
            with connection.cursor() as cursor:
                sql_query = """
                SELECT DISTINCT YEAR(Move_date) FROM `Order` ORDER BY YEAR(Move_date) ASC;
                """
                cursor.execute(sql_query)
                years = cursor.fetchall()

                # 연도 목록을 콤보박스에 설정
                self.move_history_year_combo_box.clear()
                for year in years:
                    self.move_history_year_combo_box.addItem(str(year['YEAR(Move_date)']))

        except Exception as e:
            pass


    def load_move_order_table_byyear(self):
        self.move_history_year_combo_box.model().sort(0)
        year = self.move_history_year_combo_box.currentText()

        sql_query = f"""SELECT o.Order_ID, l.Location_name, t.Technician_name, o.Machine_ID, p.Product_name, o.Move_type, o.Move_date
        FROM `Order` AS o, Business_Location AS l, Technician AS t, Product AS p, Machine AS m
        WHERE o.Location_ID = l.Location_ID and
        o.Technician_ID = t.Technician_ID and
        o.Machine_ID = m.Machine_ID and
        m.Product_ID = p.Product_ID and
        YEAR(o.Move_date) = {year}
        ORDER BY o.Order_ID""" 

        move_history_table_widget = QTableWidget()

        db_access.init_table_widget(move_history_table_widget, sql_query)

        self.move_history_table_widget.setRowCount(move_history_table_widget.rowCount())

        for row in range(move_history_table_widget.rowCount()):
            move_id = move_history_table_widget.item(row, 0).text()
            location_name = move_history_table_widget.item(row, 1).text()
            tech_name = move_history_table_widget.item(row, 2).text()
            machine_id = move_history_table_widget.item(row, 3).text()
            product_name = move_history_table_widget.item(row, 4).text()
            move_type = move_history_table_widget.item(row, 5).text()
            move_date = move_history_table_widget.item(row, 6).text()

            self.move_history_table_widget.setItem(row, 0, QTableWidgetItem(move_id))
            self.move_history_table_widget.setItem(row, 1, QTableWidgetItem(str(location_name)))
            self.move_history_table_widget.setItem(row, 2, QTableWidgetItem(str(tech_name)))
            self.move_history_table_widget.setItem(row, 3, QTableWidgetItem(machine_id))
            self.move_history_table_widget.setItem(row, 4, QTableWidgetItem(str(product_name)))
            self.move_history_table_widget.setItem(row, 5, QTableWidgetItem(str(move_type)))
            self.move_history_table_widget.setItem(row, 6, QTableWidgetItem(str(move_date)))
        self.tableWidget.sortByColumn(6, QtCore.Qt.AscendingOrder) # 구매 날짜 기준 오름차순



# -----------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()