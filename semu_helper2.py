import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction,
    QCheckBox, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QTextEdit
)
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt


class TaxHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 환경 변수로 불필요한 로그 메시지 억제
        os.environ["QT_LOGGING_RULES"] = "*.debug=false"

        self.language = "ko"  # 기본 언어는 한국어
        self.initUI()

    def initUI(self):
        self.setWindowTitle("세무 부가가치 신고 도우미")
        self.setGeometry(100, 100, 1000, 600)

        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 툴바 설정
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # 도움말 액션
        help_action = QAction("도움말", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)

        # 그래프 생성 버튼
        graph_action = QAction("그래프 생성", self)
        graph_action.triggered.connect(self.create_graph)
        toolbar.addAction(graph_action)

        # 언어 전환 토글
        self.language_toggle = QComboBox()
        self.language_toggle.addItems(["한국어", "English"])
        self.language_toggle.currentIndexChanged.connect(self.toggle_language)
        toolbar.addWidget(self.language_toggle)

        # 매입/매출 체크박스
        self.transaction_type_label = QLabel("거래 유형:")
        self.purchase_checkbox = QCheckBox("매입")
        self.sales_checkbox = QCheckBox("매출")
        layout.addWidget(self.transaction_type_label)
        layout.addWidget(self.purchase_checkbox)
        layout.addWidget(self.sales_checkbox)

        # 표 추가
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["구분", "물품명", "공급가액", "세액", "비고"])
        layout.addWidget(self.table)

        # 데이터 입력란
        self.item_name_label = QLabel("물품명")
        self.item_name_input = QLineEdit()
        layout.addWidget(self.item_name_label)
        layout.addWidget(self.item_name_input)

        self.supply_price_label = QLabel("공급가액")
        self.supply_price_input = QLineEdit()
        layout.addWidget(self.supply_price_label)
        layout.addWidget(self.supply_price_input)

        self.memo_label = QLabel("비고")
        self.memo_input = QLineEdit()
        layout.addWidget(self.memo_label)
        layout.addWidget(self.memo_input)

        # 행 추가 버튼
        self.add_table_button = QPushButton("행 추가")
        self.add_table_button.clicked.connect(self.add_table)
        layout.addWidget(self.add_table_button)

        # 메시지 표시
        self.message_label = QLabel("메시지")
        self.message_display = QLabel("")
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_display)

    def toggle_language(self):
        if self.language_toggle.currentText() == "English":
            self.language = "en"
            self.translate_to_english()
        else:
            self.language = "ko"
            self.translate_to_korean()

    def translate_to_english(self):
        self.setWindowTitle("Tax Value-Added Report Helper")
        self.transaction_type_label.setText("Transaction Type:")
        self.purchase_checkbox.setText("Purchase")
        self.sales_checkbox.setText("Sales")
        self.item_name_label.setText("Item Name")
        self.supply_price_label.setText("Supply Price")
        self.memo_label.setText("Memo")
        self.add_table_button.setText("Add Row")
        self.message_label.setText("Message")

    def translate_to_korean(self):
        self.setWindowTitle("세무 부가가치 신고 도우미")
        self.transaction_type_label.setText("거래 유형:")
        self.purchase_checkbox.setText("매입")
        self.sales_checkbox.setText("매출")
        self.item_name_label.setText("물품명")
        self.supply_price_label.setText("공급가액")
        self.memo_label.setText("비고")
        self.add_table_button.setText("행 추가")
        self.message_label.setText("메시지")

    def show_help(self):
        self.message_display.setText(
            "도움말: 매입/매출을 구분하고 데이터를 입력하세요."
        )

    def add_table(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # 거래 유형 체크박스 상태 확인
        transaction_type = "매입" if self.purchase_checkbox.isChecked() else "매출" if self.sales_checkbox.isChecked() else ""
        if not transaction_type:
            self.message_display.setText("거래 유형을 선택하세요.")
            return

        # 물품명 및 공급가액 입력
        item_name = self.item_name_input.text()
        supply_price = self.supply_price_input.text()
        memo = self.memo_input.text()

        # 세액 계산
        try:
            supply_price_value = float(supply_price)
            tax_amount = supply_price_value * 0.1
        except ValueError:
            self.message_display.setText("공급가액은 숫자로 입력하세요.")
            return

        # 표에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem(transaction_type))
        self.table.setItem(row_position, 1, QTableWidgetItem(item_name))
        self.table.setItem(row_position, 2, QTableWidgetItem(supply_price))
        self.table.setItem(row_position, 3, QTableWidgetItem(f"{tax_amount:.2f}"))
        self.table.setItem(row_position, 4, QTableWidgetItem(memo))

        # 입력란 초기화
        self.item_name_input.clear()
        self.supply_price_input.clear()
        self.memo_input.clear()

        self.message_display.setText("행이 추가되었습니다.")

    def create_graph(self):
        purchase_total = 0
        sales_total = 0

        for row in range(self.table.rowCount()):
            transaction_type = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            supply_price = self.table.item(row, 2).text() if self.table.item(row, 2) else "0"

            try:
                value = float(supply_price)
                if transaction_type == "매입":
                    purchase_total += value
                elif transaction_type == "매출":
                    sales_total += value
            except ValueError:
                continue

        # 그래프 생성
        labels = ["매입", "매출"]
        values = [purchase_total, sales_total]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, values, color=["blue", "green"])
        plt.title(
            "매입과 매출 비교" if self.language == "ko" else "Comparison of Purchases and Sales"
        )
        plt.ylabel("금액 (원)" if self.language == "ko" else "Amount (KRW)")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TaxHelperApp()
    mainWin.show()
    sys.exit(app.exec_())
