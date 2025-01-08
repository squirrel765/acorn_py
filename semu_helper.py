import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QToolBar, QAction, QCheckBox, QLabel, QLineEdit,
    QTextEdit, QSpinBox, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont


class TaxHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("세무 부가가치 신고 도우미")
        self.setGeometry(100, 100, 800, 600)

        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 툴바 설정
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        help_action = QAction("도움말", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)

        increase_font_action = QAction("+", self)
        increase_font_action.triggered.connect(self.increase_font)
        toolbar.addAction(increase_font_action)

        decrease_font_action = QAction("-", self)
        decrease_font_action.triggered.connect(self.decrease_font)
        toolbar.addAction(decrease_font_action)

        add_table_action = QAction("표 추가", self)
        add_table_action.triggered.connect(self.add_table)
        toolbar.addAction(add_table_action)

        # 폰트 크기 변수
        self.font_size = 12

        # 간이과세자/일반과세자 체크박스
        self.taxpayer_type_label = QLabel("과세자 유형:")
        self.simple_taxpayer_checkbox = QCheckBox("간이과세자")
        self.general_taxpayer_checkbox = QCheckBox("일반과세자")
        self.simple_taxpayer_checkbox.stateChanged.connect(self.update_message)
        self.general_taxpayer_checkbox.stateChanged.connect(self.update_message)

        layout.addWidget(self.taxpayer_type_label)
        layout.addWidget(self.simple_taxpayer_checkbox)
        layout.addWidget(self.general_taxpayer_checkbox)

        # 이름 입력란
        self.name_label = QLabel("이름")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # 사업자 등록번호 입력란
        self.business_number_label = QLabel("사업자 등록번호(필수):")
        self.business_number_input = QLineEdit()
        layout.addWidget(self.business_number_label)
        layout.addWidget(self.business_number_input)

        # 주민등록번호 입력란
        self.id_number_label = QLabel("주민등록번호")
        self.id_number_input = QLineEdit()
        layout.addWidget(self.id_number_label)
        layout.addWidget(self.id_number_input)

        # 업종 기재란
        self.industry_label = QLabel("업종")
        self.industry_input = QLineEdit()
        layout.addWidget(self.industry_label)
        layout.addWidget(self.industry_input)

        # 매출자료 개수 입력란
        self.sales_data_label = QLabel("매출자료 개수")
        self.sales_data_input = QSpinBox()
        layout.addWidget(self.sales_data_label)
        layout.addWidget(self.sales_data_input)

        # 매입자료 개수 입력란
        self.purchase_data_label = QLabel("매입자료 개수")
        self.purchase_data_input = QSpinBox()
        layout.addWidget(self.purchase_data_label)
        layout.addWidget(self.purchase_data_input)

        # 메모장
        self.memo_label = QLabel("메모")
        self.memo_text = QTextEdit()
        layout.addWidget(self.memo_label)
        layout.addWidget(self.memo_text)

        # 메시지 표시
        self.message_label = QLabel("메시지")
        self.message_display = QLabel("")
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_display)

        # 표 추가
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["구매 물품", "공급가액", "세액 (10%)"])
        self.table.cellDoubleClicked.connect(self.open_detail_dialog)
        layout.addWidget(self.table)

    def show_help(self):
        self.message_display.setText("도움말: 간이 일반 구분은 1억 400기준 ")


    def increase_font(self):
        self.font_size += 2
        self.update_font()

    def decrease_font(self):
        if self.font_size > 8:
            self.font_size -= 2
            self.update_font()

    def update_font(self):
        font = QFont()
        font.setPointSize(self.font_size)
        self.setFont(font)

    def update_message(self):
        if self.simple_taxpayer_checkbox.isChecked() and self.general_taxpayer_checkbox.isChecked():
            self.message_display.setText("하나의 과세자 유형만 선택하세요!")
        elif self.simple_taxpayer_checkbox.isChecked():
            self.message_display.setText("간이과세자를 선택, 공급대가 적용")
        elif self.general_taxpayer_checkbox.isChecked():
            self.message_display.setText("일반과세자를 선택, 공급가액 적용")
        else:
            self.message_display.setText("과세자 유형을 선택하세요.")

    def add_table(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def open_detail_dialog(self, row, column):
        dialog = DetailDialog(self, row)
        dialog.exec_()
        # 다이얼로그에서 업데이트된 데이터를 표에 반영
        if dialog.result == "OK":
            self.table.setItem(row, 0, QTableWidgetItem(dialog.item_name_input.text()))
            self.table.setItem(row, 1, QTableWidgetItem(dialog.supply_price_input.text()))
            # 세액 자동 계산
            try:
                supply_price = float(dialog.supply_price_input.text())
                tax_amount = supply_price * 0.1
                self.table.setItem(row, 2, QTableWidgetItem(f"{tax_amount:.2f}"))
            except ValueError:
                self.table.setItem(row, 2, QTableWidgetItem("오류"))


class DetailDialog(QDialog):
    def __init__(self, parent, row):
        super().__init__(parent)
        self.result = None
        self.row = row
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"상세 입력 (행 {self.row + 1})")
        self.setGeometry(200, 200, 400, 200)
        layout = QVBoxLayout()

        # 구매 물품 입력
        item_layout = QHBoxLayout()
        item_label = QLabel("매입/매출:")
        self.item_name_input = QLineEdit()
        item_layout.addWidget(item_label)
        item_layout.addWidget(self.item_name_input)

        # 공급가액 입력
        price_layout = QHBoxLayout()
        price_label = QLabel("공급가액:")
        self.supply_price_input = QLineEdit()
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.supply_price_input)

        # 버튼 추가
        button_layout = QHBoxLayout()
        ok_button = QPushButton("확인")
        cancel_button = QPushButton("취소")
        ok_button.clicked.connect(self.accept_dialog)
        cancel_button.clicked.connect(self.reject_dialog)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # 레이아웃 조립
        layout.addLayout(item_layout)
        layout.addLayout(price_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept_dialog(self):
        self.result = "OK"
        self.close()

    def reject_dialog(self):
        self.result = "CANCEL"
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TaxHelperApp()
    mainWin.show()
    sys.exit(app.exec_())
