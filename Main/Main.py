from subprocess import CalledProcessError
from PyQt5.QtCore import Qt, QModelIndex, QRegExp, QRectF, QThread, pyqtSignal, QCoreApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import Collect_data as cd
import Calculation as calc
import cap_stdy as cs
import time
import sys

class FloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setLocale(QtCore.QLocale("en_US"))
        self.setValidator(validator)
class MyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                border: none;
                background-color: white;
                color: #0076c0;
                font-size: 22px;
            }
        """)
class MyLabel2(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                border: none;
                background-color: white;
                color: black;
            }
        """)
class MyButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: white;
                color: black;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #b3dcfd;
            }
        """)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
    def resizeEvent(self, event):
        super().resizeEvent(event)        
        new_size = event.size()
        scene = self.scene()
        scene.setSceneRect(QRectF(0, 0, new_size.width(), new_size.height()))
        self.main_window.graph_build()
        self.main_window.construct_layers()

class MyQGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__()
        self.setPlainText(text)
        font = QFont("Arial", 12)
        self.setFont(font)
        self.setZValue(3)

class FloatDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() != 0:  
            editor = QLineEdit(parent)
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            validator.setLocale(QtCore.QLocale("en_US"))
            editor.setValidator(validator)
            return editor
        else:
            return super().createEditor(parent, option, index)

class CalculationThread(QThread):
    def __init__(self, objects):
        super().__init__()
        self.objects = objects
    def run(self):
        #Calculation
        self.Calcresult = 0
        #Calculation
        star = time.time()
        self.result = calc.calculation(self.objects['user_data'])
        #Water calc
        self.water_result = {}
        for current_name in self.objects['construct_list']:
            if self.objects['water_switch'][current_name] == True:
                geo = self.objects['user_data']['Water_calc'][current_name][0]
                width = self.objects['user_data']['Water_calc'][current_name][1]/2
                t_to_fit = self.objects['user_data']['Water_calc'][current_name][2]
                q = float(self.result['Heat']['Heat flux'][current_name])
                t_top = float(self.result['TemperaturesOut'][current_name])
                print(current_name)
                print(self, geo, width, t_to_fit, q, t_top)
                try:
                    self.water_result[current_name] = round(cs.fit_water_t(self, geo, width, t_to_fit, q, t_top), 1)
                except (ValueError, KeyError, IndexError, AttributeError, TypeError):
                    self.objects['settings_label'].setText('Set all data in parametres')
                    return() 
        self.result['Solution time'] =  str(round(time.time() - star, 3))
   



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.dark_theme = """
        #    QMainWindow {

        #        background-color: #292929;
        #    }           
        #    QTreeWidget {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #    }
        #    QPushButton {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #        border-radius: 5px;
        #        padding: 10px;
        #    }
        #    QComboBox {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #        border-radius: 5px;
        #        padding: 10px;
        #    }
        #    QLabel {
        #        color: #ffffff;
        #        background-color: #292929;
        #    }
        #    QPushButton:hover {
        #        background-color: #454545;
        #    }
        #"""
        self.light_theme = """
            QMainWindow {
                background-color: #ffffff;
            }
            #QTreeWidget {
            #    color: #000000;
            #    background-color: #ffffff;
            #    border: #ffffff;
            #QPushButton {
            #    color: #000000;
            #    background-color: #ffffff;
            #    border: none;
            #    border-radius: 5px;
            #    padding: 10px;
            #}
            #QLabel {
            #    border: none;
            #    background-color: white;
            #    color: black;
            #QPushButton:hover {
            #    background-color: #eeeeee;
            #}
        """
        QApplication.instance().setStyleSheet(self.light_theme)
        #self.setGeometry(100, 100, 1000, 600)
        self.initUI()
    def initUI(self):
        border_style = "border: 0.5px solid gray;"
        #Generate layouts
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.top_menu_widget = QWidget()
        self.top_menu_widget.setFixedHeight(100)       
        self.top_menu_widget.setStyleSheet(border_style)
        self.top_menu_layout = QHBoxLayout()
        self.top_menu_widget.setLayout(self.top_menu_layout)
        self.top_menu_layout.setContentsMargins(5, 0, 0, 0)
        self.top_menu_layout.setSpacing(0)
        self.top_menu_layout.setAlignment(Qt.AlignLeft)
        self.model_layout = QHBoxLayout()
        #Left
        self.left_window_widget = QWidget()
        self.left_window_widget.setStyleSheet(border_style)
        self.left_window_layout = QVBoxLayout()
        self.left_window_layout.setAlignment(Qt.AlignTop)
        self.left_window_widget.setLayout(self.left_window_layout)
        #Central
        self.central_window_widget = QWidget()
        self.central_window_widget.setStyleSheet(border_style)
        self.center_window_layout = QVBoxLayout()
        self.center_window_layout.setAlignment(Qt.AlignTop)
        self.central_window_widget.setLayout(self.center_window_layout)
        self.central_grid = QGridLayout()
        self.central_grid.setAlignment(Qt.AlignLeft)
        self.central_water_button_layout = QHBoxLayout()
        #Right
        self.right_window_widget = QWidget()
        self.right_window_widget.setStyleSheet(border_style)
        self.right_window_layout = QVBoxLayout()
        self.right_window_layout.setAlignment(Qt.AlignTop)
        self.right_window_widget.setLayout(self.right_window_layout)
        self.right_graph_layout = QVBoxLayout()
        self.right_graph_layout.setAlignment(Qt.AlignTop)
        self.right_graph_layout.setAlignment(Qt.AlignLeft)
        #Results
        self.right_results_layout = QVBoxLayout()
        self.right_results_buttons_layout = QHBoxLayout()
        self.right_results_buttons_layout.setAlignment(Qt.AlignLeft)
        self.right_results_layout.setAlignment(Qt.AlignTop)
        self.right_results_widget = QWidget()
        self.right_results_widget.setStyleSheet(border_style)
        self.right_window_layout.addLayout(self.right_graph_layout, 60)
        self.right_window_layout.addLayout(self.right_results_layout, 40)

        #Add layouts to main 
        self.main_layout.addWidget(self.top_menu_widget)
        self.main_layout.addLayout(self.model_layout)
        #Add layouts to model_layout
        self.model_layout.addWidget(self.left_window_widget, 20)
        self.model_layout.addWidget(self.central_window_widget, 20)
        self.model_layout.addWidget(self.right_window_widget, 60)
        #Add main to window
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        #Filling 3 windows
        #Top window
        self.RS_button = MyButton('Radiant\nSurface')
        self.RS_button.setFixedSize(90, 80)
        self.RS_button.clicked.connect(self.RS_create)
        RS_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\RS_icon.png')
        self.RS_button.setIcon(RS_icon)
        self.RS_button.setIconSize(self.RS_button.rect().size()/2.1)
        self.Door_button = MyButton('Door\nWindow')
        door_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\door_icon.png')
        self.Door_button.setIcon(door_icon)
        self.Door_button.setIconSize(self.Door_button.rect().size()/15)
        self.Door_button.setFixedSize(90, 80)
        self.Door_button.clicked.connect(self.Door_create)
        self.Water_button = MyButton('Calculate\nwater\ntemperature')
        self.Water_button.setFixedSize(120,80)
        self.Water_button.clicked.connect(self.water_create)
        water_temp_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\water_temp_icon.png')
        self.Water_button.setIcon(water_temp_icon)
        self.Water_button.setIconSize(self.Water_button.rect().size()/2)
        self.Del_button = MyButton('Delete')
        self.Del_button.setFixedSize(90, 80)
        self.Del_button.clicked.connect(self.Delete)
        delete_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\delete_icon.png')
        self.Del_button.setIcon(delete_icon)
        self.Del_button.setIconSize(self.Del_button.rect().size()/2)
        self.results_button = MyButton('Calculate')
        self.results_button.setFixedSize(90, 80)
        calc_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\calc_icon.png')
        self.results_button.setIcon(calc_icon)
        self.results_button.setIconSize(self.results_button.rect().size()/2.5)
        self.results_button.clicked.connect(self.results)
        self.temp_results_button = MyButton('Temperature')
        self.temp_results_button.setFixedSize(100, 30)
        temp_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\ht_icon.png')
        self.temp_results_button.setIcon(temp_icon)
        self.temp_results_button.setIconSize(self.temp_results_button.rect().size()/1.4)
        self.temp_results_button.clicked.connect(self.temp_results)
        self.heat_balance_results_button = MyButton('Heat balance')
        self.heat_balance_results_button.setFixedSize(100, 30)
        HB_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\HB_icon.png')
        self.heat_balance_results_button.setIcon(HB_icon)
        self.heat_balance_results_button.setIconSize(self.heat_balance_results_button.rect().size()/1.5)
        self.heat_balance_results_button.clicked.connect(self.HB_results)
        self.construct_button = MyButton('Build layers')
        self.construct_button.setFixedSize(110, 80)
        self.construct_button.clicked.connect(self.construct_layers)
        self.water_temperature_results_button = MyButton('Water temperature')
        self.water_temperature_results_button.setFixedSize(120, 30)
        #HB_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\HB_icon.png')
        #self.heat_balance_results_button.setIcon(HB_icon)
        #self.heat_balance_results_button.setIconSize(self.heat_balance_results_button.rect().size()/1.5)
        self.water_temperature_results_button.clicked.connect(self.WT_results)
        construct_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\construct_icon.png')
        self.construct_button.setIcon(construct_icon)
        self.construct_button.setIconSize(self.construct_button.rect().size()/2.1)
        
        #Left window
        #Name
        self.left_label = MyLabel('Model builder')
        #Generate treeview
        self.tree = QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.Model_tree_node = QtWidgets.QTreeWidgetItem(self.tree, ['Model tree'])
        self.Model_tree_node.setExpanded(True)
        self.tree.addTopLevelItem(self.Model_tree_node)
        self.room_node = QtWidgets.QTreeWidgetItem(self.Model_tree_node, ['Room'])
        self.room_node.setExpanded(True)
        self.node = {}
        self.node['Ceiling'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Ceiling'])
        self.node['Floor'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Floor'])
        self.node['Wall 1'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Wall 1'])
        self.node['Wall 2'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Wall 2'])
        self.node['Wall 3'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Wall 3'])
        self.node['Wall 4'] = QtWidgets.QTreeWidgetItem(self.room_node, ['Wall 4'])
        self.results_node = QtWidgets.QTreeWidgetItem(self.Model_tree_node, ['Results'])
        self.tree.selectionModel().selectionChanged.connect(self.treeview_click)
        self.tree.selectionModel().selectionChanged.connect(self.graph_build)
        self.tree.selectionModel().selectionChanged.connect(self.U_calc_layer_data)
        #Set items to left window
        self.left_window_layout.addWidget(self.left_label)       
        self.left_window_layout.addWidget(self.tree)

        #Central window
        #Name
        self.central_label = MyLabel('Settings')
        self.settings_label = MyLabel2('')
        #Inputs
        #Model tree
        self.unit_box = QComboBox()
        self.unit_box.addItem('m')
        self.unit_box.addItem('cm')
        self.unit_box.addItem('mm')
        #self.unit_box.activated[str].connect(self.geom_unit)
        self.temp_box = QComboBox()
        self.temp_box.addItem('°C')
        self.temp_box.addItem('K')
        #self.temp_box.activated[str].connect(self.change_theme)
        #Room size
        self.room = {}
        self.room['RL'] = FloatLineEdit()
        self.room['RW'] = FloatLineEdit()
        self.room['RH'] = FloatLineEdit()
        #Phys parametres
        self.construct_list = ['Ceiling', 'Floor', 'Wall 1', 'Wall 2', 'Wall 3', 'Wall 4']
        self.eps = {}
        self.U = {}
        self.Tout = {}
        for name in self.construct_list:
            self.eps[name] = FloatLineEdit()
            self.eps[name].setText('0.9')
            self.U[name] = FloatLineEdit()
            self.U[name].setText('0.4')
            self.Tout[name] = FloatLineEdit() 

        #Set items to central window
        self.center_window_layout.addWidget(self.central_label)
        #Water table buttons
        self.button_up = MyButton("")
        self.button_up.setEnabled(False)
        self.button_up.setFixedSize(30, 30)
        up_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\_up_icon.png')
        self.button_up.setIcon(up_icon)
        self.button_up.setIconSize(self.button_up.rect().size())
        self.button_up.clicked.connect(self.move_row_up)
        self.button_down = MyButton("")
        self.button_down.setEnabled(False)
        self.button_down.setFixedSize(30, 30)
        down_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\down_icon.png')
        self.button_down.setIcon(down_icon)
        self.button_down.setIconSize(self.button_down.rect().size())
        self.button_down.clicked.connect(self.move_row_down)
        self.button_delete = MyButton("")
        self.button_delete.setEnabled(False)
        self.button_delete.setFixedSize(30, 30)
        delete_row_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\delete_row_icon.png')
        self.button_delete.setIcon(delete_row_icon)
        self.button_delete.setIconSize(self.button_delete.rect().size())
        self.button_delete.clicked.connect(self.delete_rows)
        self.add_button = MyButton("")
        self.add_button.setFixedSize(30, 30)
        row_add_icon = QIcon('C:\MEGAsync\Work\Projects\Latvia\Heat exchanger\Models\Python\RHC_PyQT5\Frontend\_row_add_icon.png')
        self.add_button.setIcon(row_add_icon)
        self.add_button.setIconSize(self.add_button.rect().size())
        self.add_button.clicked.connect(self.add_empty_row)              
        #Right window items
        #Names
        self.result_label = MyLabel('Results')
        self.graph_label = MyLabel('Graphics')
        #Set items to right window
        self.right_graph_layout.addWidget(self.graph_label)
        self.right_results_layout.addWidget(self.result_label)
        self.right_results_layout.addLayout(self.right_results_buttons_layout)
        self.right_results_buttons_layout.addWidget(self.temp_results_button)
        self.right_results_buttons_layout.addWidget(self.heat_balance_results_button)
        self.right_results_buttons_layout.addWidget(self.water_temperature_results_button)
        #Inputs
        #Graphics
        self.right_graphics_view = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.right_graphics_view.setScene(self.scene)
        self.right_graph_layout.addWidget(self.right_graphics_view)


        #Results
        self.result_table = QTableWidget()
        self.right_results_layout.addWidget(self.result_table)
        #Variables
        #All
        #Water
        self.water_switch = {'Ceiling': False, 'Floor': False, 'Wall 1': False, 'Wall 2': False, 'Wall 3': False, 'Wall 4': False}
        self.water_table = {}
        self.water_node = {}
        self.mat_diam_box = {}
        self.mat_step_box = {}
        #Radiant surfaces
        self.RS_num = {'Ceiling': 0, 'Floor': 0, 'Wall 1': 0, 'Wall 2': 0, 'Wall 3': 0, 'Wall 4': 0}
        self.RS_coord = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_area = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_eps = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_T = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_node = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_data = {'Ceiling': [], 'Floor': [], 'Wall 1': [], 'Wall 2': [], 'Wall 3': [], 'Wall 4': []}
        #Door
        self.door_num = {'Wall 1': 0, 'Wall 2': 0, 'Wall 3': 0, 'Wall 4': 0}
        self.door_coord = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_area = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_eps = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_U = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_node = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_data = {'Wall 1': [], 'Wall 2': [], 'Wall 3': [], 'Wall 4': []}
        self.click = -1
        self.wall_num_list = ['1', '2', '3', '4']

    #Calculations
    #RS and window area calculation
    #Ceiling
    def area_calc(self):
        try:
            parent_name = self.tree.currentIndex().parent().data()
            if ('Radiant' in self.tree.currentIndex().data()) == True:
                RS_num = self.tree.currentIndex().data()[-1]
                W = self.RS_coord[parent_name][RS_num]['W'].text()
                L = self.RS_coord[parent_name][RS_num]['L'].text()
                self.RS_area[parent_name][RS_num].setText(str(round(float(W)*float(L), 2)))
            else:
                door_num = self.tree.currentIndex().data()[-1]
                W = self.door_coord[parent_name][door_num]['W'].text()
                H = self.door_coord[parent_name][door_num]['L'].text()
                self.door_area[parent_name][door_num].setText(str(round(float(W)*float(H), 2)))      
        except ValueError:
            return()
    #U calculation from layers table data
    def U_calc_layer_data(self):
        try:
            R_surf_coef = {'Ceiling': 0.17, 'Floor': 0.1, 'Wall 1': 0.13, 'Wall 2': 0.13, 'Wall 3': 0.13, 'Wall 4': 0.13}
            current_name = self.tree.currentIndex().data()
            if self.water_switch[current_name] == True:
                self.U[current_name].setReadOnly(True)
                self.table_name = self.water_table[current_name]
                total_R = 0
                layers_list = []
                for current_row in range(self.table_name.rowCount()):
                    layers_par_list = []
                    item = self.table_name.item(current_row, 1).text()
                    layers_par_list.append(float(item))
                    item = self.table_name.item(current_row, 2).text()
                    layers_par_list.append(float(item))
                    layers_list.append(layers_par_list)
                for parameter in layers_list:
                    total_R += (parameter[0]/1000)/parameter[1]
                self.U[current_name].setText(str(round(1/(total_R + R_surf_coef[current_name]), 2)))

            else:
                self.U[current_name].setReadOnly(False)
        except (KeyError, ZeroDivisionError):
            return()

    #Graphics drawing
    #Drawing RS and door position on wall
    def graph_build(self):
        current_item = self.tree.currentIndex()
        parent_name = current_item.parent()
        self.coord_start = QGraphicsEllipseItem(-7, self.right_graphics_view.size().height()-10, 15, 15)
        self.coord_start.setBrush(QColor(255, 0, 0))
        try:
            if ('Room' in current_item.data()) == True:
                for item in self.scene.items():
                    self.scene.removeItem(item)
                self.graph_text1 = MyQGraphicsTextItem('Wall 1 (Room lenght)')
                self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                self.graph_text1.setRotation(270)
                self.scene.addItem(self.graph_text1)
                self.graph_text2 = MyQGraphicsTextItem('Wall 2')
                self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                self.scene.addItem(self.graph_text2) 
                self.graph_text3 = MyQGraphicsTextItem('Wall 3')
                self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                self.graph_text3.setRotation(90)
                self.scene.addItem(self.graph_text3)
                self.graph_text4 = MyQGraphicsTextItem('Wall 4 (Room width)')
                self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                self.scene.addItem(self.graph_text4)
            if ('Ceiling' in parent_name.data()) == True:
                for item in self.scene.items():
                    self.scene.removeItem(item)
                for RS_num in self.RS_data[parent_name.data()]:
                    self.graph_text1 = MyQGraphicsTextItem('Wall 1')
                    self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                    self.graph_text1.setRotation(270)
                    self.scene.addItem(self.graph_text1)
                    self.graph_text2 = MyQGraphicsTextItem('Wall 2')
                    self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                    self.scene.addItem(self.graph_text2) 
                    self.graph_text3 = MyQGraphicsTextItem('Wall 3')
                    self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                    self.graph_text3.setRotation(90)
                    self.scene.addItem(self.graph_text3)
                    self.graph_text4 = MyQGraphicsTextItem('Wall 4')
                    self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                    self.scene.addItem(self.graph_text4)
                    self.scene.addItem(self.coord_start)
                    W = float(self.RS_coord[parent_name.data()][RS_num]['W'].text())*(self.right_graphics_view.size().width()/float(self.room['RW'].text()))
                    L = float(self.RS_coord[parent_name.data()][RS_num]['L'].text())*(self.right_graphics_view.size().height()/float(self.room['RL'].text()))
                    x = float(self.RS_coord[parent_name.data()][RS_num]['x'].text())*(self.right_graphics_view.size().width()/float(self.room['RW'].text()))
                    y = self.right_graphics_view.size().height() - float(self.RS_coord[parent_name.data()][RS_num]['y'].text())*(self.right_graphics_view.size().height()/float(self.room['RL'].text())) - L
                    self.scene.addRect(x, y, W, L, QPen(Qt.black), QBrush(Qt.red))
            if ('Floor' in parent_name.data()) == True:
                for item in self.scene.items():
                    self.scene.removeItem(item)
                for RS_num in self.RS_data[parent_name.data()]:
                    self.graph_text1 = MyQGraphicsTextItem('Wall 1')
                    self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                    self.graph_text1.setRotation(270)
                    self.scene.addItem(self.graph_text1)
                    self.graph_text2 = MyQGraphicsTextItem('Wall 2')
                    self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                    self.scene.addItem(self.graph_text2) 
                    self.graph_text3 = MyQGraphicsTextItem('Wall 3')
                    self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                    self.graph_text3.setRotation(90)
                    self.scene.addItem(self.graph_text3)
                    self.graph_text4 = MyQGraphicsTextItem('Wall 4')
                    self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                    self.scene.addItem(self.graph_text4)
                    self.scene.addItem(self.coord_start)
                    W = float(self.RS_coord[parent_name.data()][RS_num]['W'].text())*(self.right_graphics_view.size().width()/float(self.room['RW'].text()))
                    L = float(self.RS_coord[parent_name.data()][RS_num]['L'].text())*(self.right_graphics_view.size().height()/float(self.room['RL'].text()))
                    x = float(self.RS_coord[parent_name.data()][RS_num]['x'].text())*(self.right_graphics_view.size().width()/float(self.room['RW'].text()))
                    y = self.right_graphics_view.size().height() - float(self.RS_coord[parent_name.data()][RS_num]['y'].text())*(self.right_graphics_view.size().height()/float(self.room['RL'].text())) - L
                    self.scene.addRect(x, y, W, L, QPen(Qt.black), QBrush(Qt.red))
            if ('Wall' in parent_name.data()) == True:
                for item in self.scene.items():
                    self.scene.removeItem(item)
                R = 0
                if (int(parent_name.data()[-1])%2 == 0):
                    R = 'RW'
                else: 
                    R = 'RL'
                wall_num =  int(parent_name.data()[-1]) - 1
                self.graph_text1 = MyQGraphicsTextItem('Wall ' + self.wall_num_list[wall_num - 1])
                self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                self.graph_text1.setRotation(270)
                self.scene.addItem(self.graph_text1)
                if wall_num != 3:
                    self.graph_text3 = MyQGraphicsTextItem('Wall ' + self.wall_num_list[wall_num + 1])
                    self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                    self.graph_text3.setRotation(90)
                    self.scene.addItem(self.graph_text3)
                else:
                    self.graph_text3 = MyQGraphicsTextItem('Wall 1')
                    self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                    self.graph_text3.setRotation(90)
                    self.scene.addItem(self.graph_text3)
                self.graph_text2 = MyQGraphicsTextItem('Ceiling')
                self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                self.scene.addItem(self.graph_text2) 
                self.graph_text4 = MyQGraphicsTextItem('Floor')
                self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                self.scene.addItem(self.graph_text4)
                self.scene.addItem(self.coord_start)
                try:
                    for RS_num in self.RS_data[parent_name.data()]:
                        W = float(self.RS_coord[parent_name.data()][RS_num]['W'].text())*(self.right_graphics_view.size().width()/float(self.room[R].text()))
                        H = float(self.RS_coord[parent_name.data()][RS_num]['L'].text())*(self.right_graphics_view.size().height()/float(self.room['RH'].text()))
                        x = float(self.RS_coord[parent_name.data()][RS_num]['x'].text())*(self.right_graphics_view.size().width()/float(self.room[R].text()))
                        y = self.right_graphics_view.size().height() - float(self.RS_coord[parent_name.data()][RS_num]['y'].text())*(self.right_graphics_view.size().height()/float(self.room['RH'].text())) - H
                        self.scene.addRect(x, y, W, H, QPen(Qt.black), QBrush(Qt.red))
                except ValueError:
                    next
                for door_num in self.door_data[parent_name.data()]:
                        W = float(self.door_coord[parent_name.data()][door_num]['W'].text())*(self.right_graphics_view.size().width()/float(self.room[R].text()))
                        H = float(self.door_coord[parent_name.data()][door_num]['L'].text())*(self.right_graphics_view.size().height()/float(self.room['RH'].text()))
                        x = float(self.door_coord[parent_name.data()][door_num]['x'].text())*(self.right_graphics_view.size().width()/float(self.room[R].text()))
                        y = self.right_graphics_view.size().height() - float(self.door_coord[parent_name.data()][door_num]['y'].text())*(self.right_graphics_view.size().height()/float(self.room['RH'].text())) - H
                        self.scene.addRect(x, y, W, H, QPen(Qt.black), QBrush(Qt.blue))
        except (ValueError, TypeError):
            return() 

    #Drawing layers in water calculation
    def construct_layers(self):  
        for item in self.scene.items():
            self.scene.removeItem(item)
        parent_name = self.tree.currentIndex().parent().parent().data()
        W = self.right_graphics_view.size().width()
        H = self.right_graphics_view.size().height()-10
        try:
            self.table_name = self.water_table[parent_name]
            i = 0
            layers_list = []
            mat_list = []
            r2 = 3.4
            for current_row in range(self.table_name.rowCount()):
                item = self.table_name.item(current_row, 1).text()
                layers_list.append(float(item))
                mat = self.table_name.item(current_row, 3).text()
                mat_list.append(mat)
            construct_thickness = sum(layers_list)
            coefficient = H/construct_thickness
            for layer_thickness in layers_list: 
                self.scene.addRect(W/4, H-layer_thickness*coefficient, W/2, layer_thickness*coefficient, QPen(Qt.black), QBrush(Qt.gray))
                if mat_list[i] !='':
                    cap_offset = float(mat_list[i])
                    self.scene.addRect(W/4, H-(r2 + cap_offset)*coefficient, W/2, r2*coefficient, QPen(Qt.black), QBrush(Qt.blue))
                H -= layer_thickness*coefficient
                i += 1
        except (ZeroDivisionError, KeyError):
            return()

    #Water table actions
    #Buttons activation update
    def update_button_states(self):
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().parent().data()
        self.table_name = self.water_table[parent_name]
        current_row = self.table_name.currentRow()
        row_count = self.table_name.rowCount()
        if len(self.table_name.selectedItems()) != 0:
            self.button_delete.setEnabled(True)
        else:
            self.button_delete.setEnabled(False)
        if current_row > 0 :
            self.button_up.setEnabled(True)
        else: 
            self.button_up.setEnabled(False)
        if current_row < row_count-1 and current_row >= 0:
            self.button_down.setEnabled(True)
        else:  
            self.button_down.setEnabled(False)
    #Add empty row
    def add_empty_row(self):
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().parent().data()
        self.table_name = self.water_table[parent_name]
        row_count = self.table_name.rowCount()
        self.table_name.setRowCount(row_count + 1)
        for column in range(self.table_name.columnCount()):
            item = QTableWidgetItem("")
            self.table_name.setItem(row_count, column, item)         
    #Move row up
    def move_row_up(self):
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().parent().data()
        self.table_name = self.water_table[parent_name]
        source_items = []   
        current_row = self.table_name.currentRow()
        if current_row > 0:
            self.table_name.insertRow(current_row-1)
            for column in range(self.table_name.columnCount()):
                item = self.table_name.item(current_row + 1, column)
                source_items.append(item)
            for column in range(self.table_name.columnCount()):
                item = source_items[column].clone() if source_items[column] else None
                self.table_name.setItem(current_row - 1, column, item)
            self.table_name.removeRow(current_row + 1)
    #Move row down
    def move_row_down(self):
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().parent().data()
        self.table_name = self.water_table[parent_name]
        source_items = []
        current_row = self.table_name.currentRow()
        if current_row < self.table_name.rowCount() - 1:
            self.table_name.insertRow(current_row + 2)
            for column in range(self.table_name.columnCount()):
                item = self.table_name.item(current_row, column)
                source_items.append(item)
            for column in range(self.table_name.columnCount()):
                item = source_items[column].clone() if source_items[column] else None
                self.table_name.setItem(current_row + 2, column, item)
            self.table_name.removeRow(current_row)
    #Delete selected rows
    def delete_rows(self):
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().parent().data()
        self.table_name = self.water_table[parent_name]
        selected_rows = sorted(set(index.row() for index in self.table_name.selectedIndexes()), reverse=True)
        for row in selected_rows:
            self.table_name.removeRow(row)
      
    #Create and delete nodes def
    #RS
    def RS_create(self):
        current_name = self.tree.currentIndex().data()   
        self.RS_num[current_name] +=1
        RS_num = str(self.RS_num[current_name])
        self.RS_node[current_name][RS_num] = QtWidgets.QTreeWidgetItem(self.node[current_name], ['Radiant surface ' + RS_num])
        self.node[current_name].setExpanded(True)
        self.RS_coord[current_name][RS_num] = {}
        self.RS_coord[current_name][RS_num] = {} 
        self.RS_coord[current_name][RS_num]['x'] = FloatLineEdit()
        self.RS_coord[current_name][RS_num]['y'] = FloatLineEdit()
        self.RS_coord[current_name][RS_num]['W'] = FloatLineEdit()
        self.RS_coord[current_name][RS_num]['L'] = FloatLineEdit()
        for key in self.RS_coord[current_name][RS_num]:
            self.RS_coord[current_name][RS_num][key].textEdited.connect(self.area_calc)
            self.RS_coord[current_name][RS_num][key].textEdited.connect(self.graph_build)
        self.RS_area[current_name][RS_num] = MyLabel2('')
        self.RS_eps[current_name][RS_num] = FloatLineEdit()
        self.RS_eps[current_name][RS_num].setText('0.9')
        self.RS_T[current_name][RS_num] = FloatLineEdit()
        self.RS_data[current_name].append(RS_num)
        if self.water_switch[current_name] == True:
            RS_num = self.RS_data[current_name][-1]
            self.water_node[current_name].parent().takeChild(self.water_node[current_name].parent().indexOfChild(self.water_node[current_name]))
            self.water_node[current_name] = QtWidgets.QTreeWidgetItem(self.RS_node[current_name][RS_num], ['Water calculate'])
            self.RS_node[current_name][RS_num].setExpanded(True)    
    #Door
    def Door_create(self):            
        current_name = self.tree.currentIndex().data()   
        self.door_num[current_name] +=1
        door_num = str(self.door_num[current_name])
        self.door_node[current_name][door_num] = QtWidgets.QTreeWidgetItem(self.node[current_name], ['Door/window ' + door_num])
        self.node[current_name].setExpanded(True)
        self.door_coord[current_name][door_num] = {}
        self.door_coord[current_name][door_num] = {} 
        self.door_coord[current_name][door_num]['x'] = FloatLineEdit()
        self.door_coord[current_name][door_num]['y'] = FloatLineEdit()
        self.door_coord[current_name][door_num]['W'] = FloatLineEdit()
        self.door_coord[current_name][door_num]['L'] = FloatLineEdit()
        for key in self.door_coord[current_name][door_num]:
            self.door_coord[current_name][door_num][key].textEdited.connect(self.area_calc)
            self.door_coord[current_name][door_num][key].textEdited.connect(self.graph_build)
        self.door_area[current_name][door_num] = MyLabel2('')
        self.door_eps[current_name][door_num] = FloatLineEdit()
        self.door_eps[current_name][door_num].setText('0.9')
        self.door_U[current_name][door_num] = FloatLineEdit()
        self.door_data[current_name].append(door_num)

    #Water create
    def water_create(self):            
        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent().data()
        if self.water_switch[parent_name] == False:
            self.water_switch[parent_name] = True
            RS_num = self.RS_data[parent_name][-1]
            self.water_node[parent_name] = QtWidgets.QTreeWidgetItem(self.RS_node[parent_name][RS_num], ['Water calculate'])
            self.RS_node[parent_name][RS_num].setExpanded(True)    
            self.mat_step_box[parent_name]  = QComboBox()
            for item in range(10, 70, 10):
                self.mat_step_box[parent_name].addItem(str(item))            
            self.mat_diam_box[parent_name] = QComboBox()
            self.mat_diam_box[parent_name].setFixedWidth(45)
            self.mat_diam_box[parent_name].addItem('3.4')
            self.mat_diam_box[parent_name].addItem('4.3')
            self.water_table[parent_name] = QTableWidget()
            self.water_table[parent_name].setColumnCount(4)
            self.water_table[parent_name].setItemDelegate(FloatDelegate())
            self.water_table[parent_name].setHorizontalHeaderLabels(["Name", "Thickness, mm", "Lambda, W/mK", "Mat offset, mm"])
            self.water_table[parent_name].setEditTriggers(QTableWidget.AnyKeyPressed | QTableWidget.DoubleClicked)
            self.water_table[parent_name].verticalHeader().setVisible(False)
            self.water_table[parent_name].itemSelectionChanged.connect(self.update_button_states)               
        else:
            return()
    #Delete
    def Delete(self):
        child = self.tree.currentItem()
        parent = child.parent()
        index = parent.indexOfChild(child)
        current_name = self.tree.currentIndex()
        parent_name = current_name.parent().data()   
        if ('Radiant' in current_name.data()) == True:
            RS_num = current_name.data()[-1]
            self.RS_data[parent_name].remove(RS_num)
            if (len(self.RS_data[parent_name]) == 0) and (self.water_switch[parent_name] == True):
                self.water_switch[parent_name] = False
                parent.takeChild(parent.indexOfChild(self.water_node[parent_name]))
            elif (len(self.RS_data[parent_name]) != 0) and (self.water_switch[parent_name] == True):
                RS_num = self.RS_data[parent_name][-1]
                self.water_node[parent_name].parent().takeChild(self.water_node[parent_name].parent().indexOfChild(self.water_node[parent_name]))
                self.water_node[parent_name] = QtWidgets.QTreeWidgetItem(self.RS_node[parent_name][RS_num], ['Water calculate'])
                self.RS_node[parent_name][RS_num].setExpanded(True)
        elif ('Door' in current_name.data()) == True:
            self.door_data[parent_name].remove(current_name.data()[-1])
        elif ('Water' in current_name.data()) == True:
            self.water_switch[current_name.parent().parent().data()] = False
        parent.takeChild(index)

    #Treeview actions
    def treeview_click(self, index):
        current_item = self.tree.currentIndex()
        parent_name = current_item.parent()
        while self.central_grid.count():
            item = self.central_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        while self.center_window_layout.count():
            item = self.center_window_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                item.layout().setParent(None)
        while self.central_water_button_layout.count():
            item = self.central_water_button_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                item.layout().setParent(None)
        while self.top_menu_layout.count():
            item = self.top_menu_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.center_window_layout.addWidget(self.central_label)
        self.center_window_layout.addLayout(self.central_grid)
        if ("Model tree" in current_item.data()) == True:
            self.central_grid.addWidget(MyLabel2('Geometry units'), 0,0)
            self.central_grid.addWidget(self.unit_box,0,1)
            self.central_grid.addWidget(MyLabel2('Temperature units'), 1,0)
            self.central_grid.addWidget(self.temp_box,1,1)
        elif ("Room" in current_item.data()) == True:
            self.central_grid.addWidget(MyLabel2('Room lenght'), 0,0)
            self.central_grid.addWidget(self.room['RL'], 0,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 0,2)
            self.central_grid.addWidget(MyLabel2('Room width'), 1,0)
            self.central_grid.addWidget(self.room['RW'], 1,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 1,2)
            self.central_grid.addWidget(MyLabel2('Room hieght'), 2,0)
            self.central_grid.addWidget(self.room['RH'], 2,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 2,2)
        elif ("Result" in current_item.data()) == True:
            self.top_menu_layout.addWidget(self.results_button) 
            self.central_grid.addWidget(self.settings_label,0,0)
        elif ("Radiant" in current_item.data()) == True:
            parent_name = current_item.parent().data()
            RS_num = current_item.data()[-1]
            self.central_grid.addWidget(MyLabel2('Left corner'), 0,1)
            self.central_grid.addWidget(MyLabel2('x'), 1,0)
            self.central_grid.addWidget(self.RS_coord[parent_name][RS_num]['x'], 1,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 1,2)
            self.central_grid.addWidget(MyLabel2('y'), 2,0)
            self.central_grid.addWidget(self.RS_coord[parent_name][RS_num]['y'], 2,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 2,2)
            self.central_grid.addWidget(MyLabel2('Size'), 3,1)
            self.central_grid.addWidget(MyLabel2('Width'), 4,0)
            self.central_grid.addWidget(self.RS_coord[parent_name][RS_num]['W'], 4,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 4,2)
            self.central_grid.addWidget(MyLabel2('Lenght'), 5,0)
            self.central_grid.addWidget(self.RS_coord[parent_name][RS_num]['L'], 5,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 5,2)
            self.central_grid.addWidget(MyLabel2('Area'), 6,0)
            self.central_grid.addWidget(self.RS_area[parent_name][RS_num], 6,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText() + '²'), 6,2)
            self.central_grid.addWidget(MyLabel2('Physical parametres'), 7,1)
            self.central_grid.addWidget(MyLabel2('EPS'), 8,0)
            self.central_grid.addWidget(self.RS_eps[parent_name][RS_num], 8,1)
            self.central_grid.addWidget(MyLabel2('1'), 8,2)
            self.central_grid.addWidget(MyLabel2('T'), 9,0)
            self.central_grid.addWidget(self.RS_T[parent_name][RS_num], 9,1)
            self.central_grid.addWidget(MyLabel2(self.temp_box.currentText()), 9,2)
            self.top_menu_layout.addWidget(self.Water_button)
            self.top_menu_layout.addWidget(self.Del_button)   
        elif ("Door" in current_item.data()) == True:
            parent_name = current_item.parent().data()
            door_num = current_item.data()[-1]
            self.central_grid.addWidget(MyLabel2('Left corner'), 0,1)
            self.central_grid.addWidget(MyLabel2('x'), 1,0)
            self.central_grid.addWidget(self.door_coord[parent_name][door_num]['x'], 1,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 1,2)
            self.central_grid.addWidget(MyLabel2('y'), 2,0)
            self.central_grid.addWidget(self.door_coord[parent_name][door_num]['y'], 2,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 2,2)
            self.central_grid.addWidget(MyLabel2('Size'), 3,1)
            self.central_grid.addWidget(MyLabel2('Width'), 4,0)
            self.central_grid.addWidget(self.door_coord[parent_name][door_num]['W'], 4,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 4,2)
            self.central_grid.addWidget(MyLabel2('Height'), 5,0)
            self.central_grid.addWidget(self.door_coord[parent_name][door_num]['L'], 5,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText()), 5,2)
            self.central_grid.addWidget(MyLabel2('Area'), 6,0)
            self.central_grid.addWidget(self.door_area[parent_name][door_num], 6,1)
            self.central_grid.addWidget(MyLabel2(self.unit_box.currentText() + '²'), 6,2)
            self.central_grid.addWidget(MyLabel2('Physical parametres'), 7,1)
            self.central_grid.addWidget(MyLabel2('EPS'), 8,0)
            self.central_grid.addWidget(self.door_eps[parent_name][door_num], 8,1)
            self.central_grid.addWidget(MyLabel2('1'), 8,2)
            self.central_grid.addWidget(MyLabel2('U'), 9,0)
            self.central_grid.addWidget(self.door_U[parent_name][door_num], 9,1)
            self.central_grid.addWidget(MyLabel2('W/(K*m²)'), 9, 2)
            self.central_grid.addWidget(MyLabel2('Out temperature'), 10,0)
            self.central_grid.addWidget(MyLabel2(self.Tout[parent_name].text()), 10,1)
            self.central_grid.addWidget(MyLabel2(self.temp_box.currentText()), 10, 2)
            self.top_menu_layout.addWidget(self.Del_button)
        elif ("Water" in current_item.data()) == True:
            parent_name = current_item.parent().parent().data()
            col_width = int(self.central_window_widget.width()/4)
            self.top_menu_layout.addWidget(self.construct_button)
            self.top_menu_layout.addWidget(self.Del_button)   
            self.central_grid.addWidget(MyLabel2('Distance between capillaries'), 0,0)
            self.central_grid.addWidget(self.mat_step_box[parent_name], 0,1)
            self.central_grid.addWidget(MyLabel2('mm'), 0,2)
            self.central_grid.addWidget(MyLabel2('Diameter of capillaries'), 1,0)
            self.central_grid.addWidget(self.mat_diam_box[parent_name], 1,1)
            self.central_grid.addWidget(MyLabel2('mm'), 1,2)
            self.water_table[parent_name].setFixedSize(self.central_window_widget.width(), 500)
            for i in range(4):
                self.water_table[parent_name].setColumnWidth(i, col_width)
            self.center_window_layout.addWidget(self.water_table[parent_name])
            self.center_window_layout.addLayout(self.central_water_button_layout)
            self.central_water_button_layout.addWidget(self.button_up)
            self.central_water_button_layout.addWidget(self.button_down)
            self.central_water_button_layout.addWidget(self.add_button)
            self.central_water_button_layout.addWidget(self.button_delete)
            self.center_window_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        else:
            self.central_grid.addWidget(MyLabel2(current_item.data()), 0,0)
            self.central_grid.addWidget(MyLabel2('EPS'), 1,0)
            self.central_grid.addWidget(self.eps[current_item.data()], 1,1)
            self.central_grid.addWidget(MyLabel2('1'), 1,2)
            self.central_grid.addWidget(MyLabel2('U-value'), 2,0)
            self.central_grid.addWidget(self.U[current_item.data()], 2,1)
            self.central_grid.addWidget(MyLabel2('W/(K*m²)'), 2,2)
            self.central_grid.addWidget(MyLabel2('Out temperature'), 3,0)
            self.central_grid.addWidget(self.Tout[current_item.data()], 3,1)
            self.central_grid.addWidget(MyLabel2(self.temp_box.currentText()), 3,2)
            self.top_menu_layout.addWidget(self.RS_button)
            if ("Wall" in current_item.data()) == True:
                self.top_menu_layout.addWidget(self.Door_button)
 

    #Results
    #Calculation
    def results(self):     
        self.settings_label.setText('Calculate...')     
        QCoreApplication.processEvents()
        self.user_data = cd.collect(self)
        try:           

            self.objects = {
                'construct_list': self.construct_list,
                'water_switch': self.water_switch,
                'user_data': self.user_data,
                'settings_label': self.settings_label
            }
            thread  = CalculationThread(self.objects)
            thread.start()
            thread.wait()
            self.Calcresult = thread.result
            self.water_temp_result = {}
            for current_name in self.objects['construct_list']:
                if self.objects['water_switch'][current_name] == True:
                    self.water_temp_result[current_name] = thread.water_result[current_name]
        except (ValueError, KeyError, IndexError, TypeError):
            self.settings_label.setText('Set all data in parametres')
            return()   
        #Clear data
        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)
        #New data
        row_num = 0
        self.result_table.setColumnCount(3)
        self.result_table.setRowCount(len(self.Calcresult['Temperatures']))          
        self.result_table.verticalHeader().setVisible(False)
        header_labels = ['Structure', 'Inner temperatures, °C', 'Outer temperatures, °C']
        self.result_table.setHorizontalHeaderLabels(header_labels)
        for key in self.Calcresult['Temperatures']:
            self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
            self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Temperatures'][key])))
            self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['TemperaturesOut'][key])))
            row_num +=1
        self.result_table.resizeColumnsToContents()
        self.settings_label.setText('Last calculation time: ' + self.Calcresult['Solution time'] + ' sec') 
        return self.Calcresult, self.user_data



    #Temperature results
    def temp_results(self):
        try:
            if (self.Calcresult != 0):
                #Clear data
                self.result_table.clearContents()
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
                #New data
                row_num = 0
                self.result_table.setColumnCount(3)
                self.result_table.setRowCount(len(self.Calcresult['Temperatures']))          
                self.result_table.verticalHeader().setVisible(False)
                header_labels = ['Structure', 'Inner temperatures, °C', 'Outer temperatures, °C']
                self.result_table.setHorizontalHeaderLabels(header_labels)
                for key in self.Calcresult['Temperatures']:
                    self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                    self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Temperatures'][key])))
                    self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['TemperaturesOut'][key])))
                    row_num +=1
                self.result_table.resizeColumnsToContents()
        except AttributeError:
            return()    
    #Heat balance results
    def HB_results(self):
        try:
            if (self.Calcresult != 0):
                #Clear data
                self.result_table.clearContents()
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
                #New data
                row_num = 0
                self.result_table.setColumnCount(4)
                self.result_table.setRowCount(len(self.Calcresult['Heat']['Heat flux']))          
                self.result_table.verticalHeader().setVisible(False)
                header_labels = ['Structure', 'Source flux, W/m²', 'Power source, W', 'Power losses, W']
                self.result_table.setHorizontalHeaderLabels(header_labels)
                for key in self.Calcresult['Heat']['Heat flux']:
                    self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                    self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Heat']['Heat flux'][key])))
                    self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['Heat']['Heat power'][key])))
                    self.result_table.setItem(row_num, 3, QTableWidgetItem(str(self.Calcresult['Losses'][key])))
                    row_num +=1
                self.result_table.resizeColumnsToContents()
        except AttributeError:
            return()  
    #Water temperature
    def WT_results(self):
        try:
            if (self.water_temp_result != 0):
                #Clear data
                self.result_table.clearContents()
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
                #New data
                row_num = 0
                self.result_table.setColumnCount(3)               
                self.result_table.setRowCount(len(self.water_temp_result))          
                self.result_table.verticalHeader().setVisible(False)
                header_labels = ['Mat position','Surface temperature, °C' , 'Water temperature, °C']
                self.result_table.setHorizontalHeaderLabels(header_labels)
                for key in self.water_temp_result:
                    self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                    self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.user_data['Water_calc'][key][2])))
                    self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.water_temp_result[key])))
                    row_num +=1
                self.result_table.resizeColumnsToContents()
        except AttributeError:
            return()  

    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec_()
