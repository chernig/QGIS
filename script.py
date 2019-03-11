from PyQt5.QtCore import *
from PyQt5.QtGui import *
project = QgsProject.instance()
def open(dialog, layer, feature):
    def get_feature(featureName):
        name = dialog.findChild(QObject, featureName)
        return name
    dependencies = {
        'Communication' : ('coax','conduit','data','optic fibre', 'shielded twisted pair', 'unshielded twisted pair'),
        'Fire Service' : ('chemical','potable'),
        'Electricity' : ('high voltage assets', 'medium voltage assets', 'low voltage assets', 'public lighting', 'private lighting', 'electrical transmission assets'),
        'Gas' : ('ethan gas assets','liquefied natural gas assets', 'liquefied petroleum gas assets'),
        'ITS' : ('coax', 'shielded twisted pair', 'unshieled twisted pair', 'data', 'optic fibre'),
        'Petroleum' : ('medium pressure', 'high pressure'),
        'Drainage' : ('harvested stormwater', 'raw stormwater', 'run off stormwater'),
        'Sewer' : ('gravity sewer','rising main sewer','sliphon sewer', 'vacuum sewer', 'trade waste','grey water', 'abandoned'),
        'Wastewater' : '',
        'Lighting Assets' : '',
        'Water' : ('irrigation', 'potable', 'recycled/re-used', 'river/stream', 'raw', 'sea', 'chilled', 'heated', 'abandoned'),
        'Not Specified' : ['uknown feature'],
        '':''
        }
    def subAssetChange():
        current_index=get_feature("sub-type").currentIndex()
        get_feature("sub-type").clear()
        for i in range (0, len(dependencies[get_feature("asst_type").currentText()])):
                data = dependencies[get_feature("asst_type").currentText()][i]
                get_feature("sub-type").addItem(dependencies[get_feature("asst_type").currentText()][i], data)
        get_feature("sub-type").setCurrentIndex(current_index)
        text = str(get_feature("sub-type").count())
        get_feature("config").setText(text)
    def disable_feature(feature1,feature_list):
        text = get_feature(feature1).text()
        if text == "NULL" or text is "":
            for x in feature_list:
                get_feature(x).setEnabled(True)
        else:
            for x in feature_list:
                get_feature(x).clear()
                get_feature(x).setDisabled(True)
    def enable_feature(feature1, feature2):
        text = get_feature(feature1).text()
        if text == "NULL" or text is "":
            get_feature(feature2).clear()
            get_feature(feature2).setDisabled(True)
        else:
            get_feature(feature2).setEnabled(True)
    def concatenate():
        value = get_feature("loc_abs").text()
        value = value.split(",")
        get_feature("loc_abs").setText(value)
    def set_owner():
        owner = get_feature("owner").text()
        QgsExpressionContextUtils.setProjectVariable(project,'project_owner', owner)
    get_feature("loc_abs").textChanged.connect(lambda: disable_feature("loc_abs",["loc_indic","loc_indic_desc","loc_intrpl","pos_rel_horz","pos_rel_virt"]))
    test = QgsExpressionContextUtils.projectScope(project).variable("project_owner")
    get_feature("owner").setText(test)
    subAssetChange()
    get_feature("asst_type").currentTextChanged.connect(subAssetChange)
    get_feature("asst_size").textChanged.connect(lambda: enable_feature("asst_size","size_desc"))
    get_feature("owner").editingFinished.connect(set_owner)
    ######################################
    # Absolute spatial position (concatenate): data should be stored like 1 variable? 2-3 variables? Tuple? Array? No user request
    # Asset owner: Asset owner and project owner are the same variable or 2 different? Pop up?
    # Material: Where is the data?
    # GID: Autonumber? Enabled/disabled?
    # QgsExpressionContextUtils.setProjectVariable(project,'myvar','Hello World!')
    # QgsExpressionContextUtils.projectScope(project).variable('myvar')
    # Tooltip (absolute spatial position)
    #Tooltip = "Enter the X, Y and Z values as comma seperated elements, e.g. 545423.12,678678.43, 2.35
    # #Applicattion run it check code"