from PyQt5.QtChart import QPieSeries, QChart, QChartView
from PyQt5.QtCore import Qt
from transaction import Transaction
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QTextEdit, QCheckBox
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
import sys


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.categories = []
        self.transactions = []  # only expenses
        self.expenses_by_category = {}
        self.groups = {}
        self.savings = 0.0
        self.importance = {}
        self.all_expenses = 0.00
        self.setWindowTitle("Money management")
        self.resize(800, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(140, 195, 160))
        self.setPalette(p)
        self.set_buttons()

    def create_pie_chart(self, exclude_categories):
        series = QPieSeries()
        for category in self.expenses_by_category:
            if category not in exclude_categories and self.expenses_by_category[category] > 0.0:
                percent = (self.expenses_by_category[category] / self.all_expenses) * 100
                series.append(str(round(self.expenses_by_category[category], 2)) + "€ " + str(round(percent, 2)) + "% "
                              + str(category), self.expenses_by_category[category])

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignLeft)

        chart.setTheme(QChart.ChartThemeDark)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setFixedSize(600, 550)
        self.setCentralWidget(chart_view)

    def upload_csv(self):
        dialog = QtWidgets.QFileDialog()
        selected_file = dialog.getOpenFileName(None, "Transactions input dialog", "", "CSV data files (*.csv)")
        selected_file_name = selected_file[0]
        if selected_file_name == '':
            return
        file = open(selected_file_name)
        line = file.readline()
        while line:
            line = file.readline()
            if not line:
                break
            word = line.split(',')
            if float(word[4]) > 0.0:  # saving only expenses which are negative
                break
            transaction = Transaction(word[0], word[1], word[2], word[3],
                                      float(word[4]) * -1, word[5], word[6], word[7])
            self.transactions.append(transaction)
        self.calculate_expenses()
        self.make_categories()
        self.fill_expenses_by_category()
        self.calculate_importance()
        self.create_pie_chart([])
        file.close()

    def fill_expenses_by_category(self):
        self.expenses_by_category.clear()
        for transaction in self.transactions:
            if transaction.category in self.expenses_by_category:
                self.expenses_by_category.update(
                    {transaction.category: (self.expenses_by_category[transaction.category] + transaction.amount)})
            else:
                self.expenses_by_category.update({transaction.category: transaction.amount})

    def calculate_expenses(self):
        for transaction in self.transactions:
            x = transaction.amount
            self.all_expenses += x

    def make_categories(self):
        for transaction in self.transactions:
            if transaction.category not in self.categories:
                self.categories.append(transaction.category)

    def calculate_importance(self):
        self.importance.clear()
        for transaction in self.transactions:
            if transaction.category != "Rent" and transaction.category != "Electricity bill" \
                    and transaction.category != "Loan":
                if transaction.category in self.importance:
                    self.importance.update({transaction.category: (self.importance[transaction.category] + 1)})
                else:
                    self.importance.update({transaction.category: 1})

    def add_savings(self):
        dialog = QtWidgets.QInputDialog()
        savings, ok = dialog.getDouble(None, "Savings input dialog", "Enter amount you wish to save:")
        if ok:
            self.savings += savings
            self.expenses_by_category.update({"Savings": self.savings})
            while savings > 0:
                key_with_min_value = min(self.importance, key=self.importance.get)  # find the least important first, smallest importance number
                if savings <= self.expenses_by_category.get(key_with_min_value):
                    self.expenses_by_category.update(
                        {key_with_min_value: (self.expenses_by_category[key_with_min_value] - savings)})
                    savings = 0.0
                else:  # continue the loop as not able to save the whole amount from one category
                    savings = savings - self.expenses_by_category.get(key_with_min_value)
                    self.expenses_by_category.update({key_with_min_value: 0.0})
                    self.importance.pop(key_with_min_value)
            self.create_pie_chart([])

    def change_importance(self):
        dialog = QtWidgets.QInputDialog()
        importance_order, ok = dialog.getText(None,
                                              "Importance input dialog", "Enter categories in the order of importance:")
        if ok:
            for category in self.importance:
                self.importance.update({category: 0})
            importance = importance_order.split(",")
            max_importance = len(importance) + 1  # maximum importance number which is possible is the number of categories
            for category in importance:
                self.importance.update({category: max_importance})
                max_importance -= 1

    def combine_group(self, group_name):
        dialog = QtWidgets.QInputDialog()
        categories_to_combine, ok = dialog.getText(None, "Group input dialog", "Enter categories to combine:")
        if ok:
            group_expenses = 0.0
            group_importance = 0
            group = categories_to_combine.split(",")
            self.groups.update({group_name: group})
            for category in group:
                group_expenses += self.expenses_by_category.get(category)
                self.expenses_by_category.pop(category)
                group_importance += self.importance.get(category)
                self.importance.pop(category)
            self.importance.update(({group_name: group_importance}))
            self.expenses_by_category.update({group_name: group_expenses})
            self.create_pie_chart([])

    def remove_group(self, group_name):
        for transaction in self.transactions:
            if transaction.category in self.groups.get(group_name):
                if transaction.category in self.expenses_by_category:
                    self.expenses_by_category.update(
                        {transaction.category: (self.expenses_by_category[transaction.category] + transaction.amount)})
                else:
                    self.expenses_by_category.update({transaction.category: transaction.amount})

        self.groups.pop(group_name)
        self.expenses_by_category.pop(group_name)
        self.calculate_importance()
        self.create_pie_chart([])

    def create_pie_chart_based_on_check_box_state(self, check_box, exclude_categories):
        if check_box.isChecked():
            self.create_pie_chart(exclude_categories)
        else:
            self.create_pie_chart([])

    def set_buttons(self):

        check_box_rent = QCheckBox(" without rent", self)
        check_box_rent.move(600, 120)
        check_box_rent.stateChanged.connect(
            lambda: self.create_pie_chart_based_on_check_box_state(check_box_rent, ["Rent"]))

        group_input = QTextEdit(self)
        group_input.setFixedSize(150, 35)
        group_input.move(600, 160)
        group_input.setStyleSheet(
            "QTextEdit { background-color: #FFFFFF; border: 1px solid black; border-radius: 5px;}")

        combine_group_btn = QPushButton("Add group", self)
        combine_group_btn.setFixedSize(72, 25)
        combine_group_btn.move(600, 200)
        combine_group_btn.setStyleSheet(
            "QPushButton { background-color: #f4c095; border: 1px solid black; border-radius: 5px;}")
        combine_group_btn.clicked.connect(lambda: self.combine_group(group_input.toPlainText()))

        separate_group_btn = QPushButton("Remove", self)
        separate_group_btn.setFixedSize(72, 25)
        separate_group_btn.move(678, 200)
        separate_group_btn.setStyleSheet(
            "QPushButton { background-color: #f4c095; border: 1px solid black; border-radius: 5px;}")
        separate_group_btn.clicked.connect(lambda: self.remove_group(group_input.toPlainText()))

        read_csv_btn = QPushButton("Read new csv-file", self)
        read_csv_btn.setFixedSize(150, 35)
        read_csv_btn.move(600, 70)
        read_csv_btn.setStyleSheet(
            "QPushButton { background-color: #f4c095; border: 1px solid black; border-radius: 5px;}")
        read_csv_btn.clicked.connect(self.upload_csv)

        add_savings_btn = QPushButton("Add savings", self)
        add_savings_btn.setFixedSize(150, 35)
        add_savings_btn.move(600, 280)
        add_savings_btn.setStyleSheet(
            "QPushButton { background-color: #f4c095; border: 1px solid black; border-radius: 5px;}")
        add_savings_btn.clicked.connect(self.add_savings)

        change_importance_btn = QPushButton("Change importance", self)
        change_importance_btn.setFixedSize(150, 35)
        change_importance_btn.move(600, 320)
        change_importance_btn.setStyleSheet(
            "QPushButton { background-color: #f4c095; border: 1px solid black; border-radius: 5px;}")
        change_importance_btn.clicked.connect(self.change_importance)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
