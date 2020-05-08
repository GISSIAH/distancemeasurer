
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .DistanceMeasurer_dialog import DistanceMeasureDialog
import os.path
from qgis.core import *
from qgis.gui import *
class DistanceMeasure:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DistanceMeasure_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Distance Measure')
        self.first_start = None
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DistanceMeasure', message)
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)
        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action
    def initGui(self):
        icon_path = ':/plugins/DistanceMeasurer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Measures Distance'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.first_start = True
    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Distance Measure'),
                action)
            self.iface.removeToolBarIcon(action)            
    def GitWhoop(self,layer,le,cb):
        for zemp in layer.getFeatures():
            if zemp[cb] == le.text():
                layer.select(zemp.id())
                return zemp        
    def MeasureD(self):
        self.dlg.lineEdit_3.clear()
        F1=self.GitWhoop(self.ptlayer,self.dlg.lineEdit,self.dlg.comboBox_3.currentText())
        F2=self.GitWhoop(self.stlayer,self.dlg.lineEdit_2,self.dlg.comboBox_4.currentText())
        try:
            geom1 = F1.geometry()
            geom2 = F2.geometry()
            Distance = geom1.distance(geom2)
            c=str(Distance)
            self.dlg.lineEdit_3.setText(c)
        except:
            self.dlg.lineEdit.setText('error!! check the feature name/field ')
            self.dlg.lineEdit_2.setText('error!! check the feature name/field') 


        
    def GetFields(self):
        self.dlg.comboBox_3.clear()
        currentlayer= self.dlg.comboBox.currentText()
        for s in self.lays:
            if s.name() == currentlayer:
                self.ptlayer=s
                fds=s.dataProvider().fields()
                fdnames=[]
                for f in fds:
                    fdnames.append(f.name())
                self.dlg.comboBox_3.addItems(fdnames)           
    def GetFields2(self):
        self.dlg.comboBox_4.clear()
        currentlayer= self.dlg.comboBox_2.currentText()
        for p in self.lays:
            if p.name() == currentlayer:
                self.stlayer=p
                fdp=p.dataProvider().fields()
                fdnames=[]
                for f in fdp:
                    fdnames.append(f.name())
                self.dlg.comboBox_4.addItems(fdnames)
    def GitVals(self,le,pt,):
        for temp in self.lays:
            if temp.name() == self.dlg.comboBox_5.currentText(): 
                ras_layer=temp
        qry = ras_layer.dataProvider().identify(pt,QgsRaster.IdentifyFormatValue)
        r=qry.results()
        le.setText(str(r[1]))       
    def RunFunctions(self):
        self.MeasureD()
        try:
            self.GitVals(self.dlg.lineEdit_4,self.GitWhoop(self.ptlayer,self.dlg.lineEdit,self.dlg.comboBox_3.currentText()).geometry().asPoint())
            self.GitVals(self.dlg.lineEdit_5,self.GitWhoop(self.stlayer,self.dlg.lineEdit_2,self.dlg.comboBox_4.currentText()).geometry().asPoint())
        except:
            print('ggg')

    def run(self):
        if self.first_start == True:
            self.first_start = False
            self.dlg = DistanceMeasureDialog()
        self.lays = self.iface.mapCanvas().layers()
        self.dlg.comboBox.clear()
        self.dlg.comboBox_2.clear()
        self.dlg.comboBox_5.clear()
        names=[]
        ras_names=[]
        for lay in self.lays:
            names.append(lay.name())    
        self.dlg.comboBox.addItems(names)
        self.dlg.comboBox_2.addItems(names)
        for lay in self.lays:
            if lay.type() == 1:
                ras_names.append(lay.name())
        self.dlg.comboBox_5.addItems(ras_names)
        self.dlg.pushButton_2.clicked.connect(self.GetFields)
        self.dlg.pushButton_3.clicked.connect(self.GetFields2)
        self.dlg.pushButton.clicked.connect(self.RunFunctions)
        self.dlg.show()
        result = self.dlg.exec_()