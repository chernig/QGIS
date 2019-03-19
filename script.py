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
        # current_index=get_feature("sub-type").currentIndex()
        get_feature("sub-type").clear()
        for i in range (0, len(dependencies[get_feature("asst_type").currentText()])):
                data = dependencies[get_feature("asst_type").currentText()][i]
                get_feature("sub-type").addItem(dependencies[get_feature("asst_type").currentText()][i], data)
        # get_feature("sub-type").setCurrentIndex(current_index)
        # text = str(get_feature("sub-type").count())
        # get_feature("config").setText(text)
    def disable_feature(feature1,feature_list):
        text = get_feature(feature1).text()
        if text == "NULL" or text is "":
            for x in feature_list:
                get_feature(x).setEnabled(True)
        else:
            for x in feature_list:
                get_feature(x).clear()
                get_feature(x).setDisabled(True)
    def enable_feature(feature1, feature_list):
        text = get_feature(feature1).text()
        if text == "NULL" or text is "":
            for i in feature_list:
                get_feature(i).clear()
                get_feature(i).setDisabled(True)
        else:
            for i in feature_list:
                get_feature(i).setEnabled(True)
    # def concatenate():
    #     value = get_feature("loc_abs").text()
    #     value = value.split(",")
    #     get_feature("loc_abs").setText(value)
    def set_owner():
        owner = get_feature("owner").text()
        QgsExpressionContextUtils.setProjectVariable(project,'project_owner', owner)
    features_associated = {
        "loc_abs" : ["loc_indic","loc_indic_desc","loc_intrpl","pos_rel_horz","pos_rel_virt"],
        "loc_indic" : ["loc_abs","loc_intrpl","pos_rel_horz","pos_rel_virt"],
        "pos_rel_virt" : ["loc_abs","loc_indic_desc","loc_indic"],
        "pos_rel_horz" : ["loc_abs","loc_indic_desc","loc_indic"],
        "loc_intrpl" : ["loc_abs","loc_indic_desc","loc_indic"]
        }
    def check_fields(feature_list):
        for i in feature_list:
            text = get_feature(i).text()
            if text == "NULL" or text == "":
                continue
            else:
                for x in features_associated[i]:
                    get_feature(x).setDisabled(True)
                return

    get_feature("loc_abs").textChanged.connect(lambda: disable_feature("loc_abs",["loc_indic","loc_indic_desc","loc_intrpl","pos_rel_horz","pos_rel_virt"]))
    get_feature("loc_indic").textChanged.connect(lambda: disable_feature("loc_indic",["loc_abs","loc_intrpl","pos_rel_horz","pos_rel_virt"]))
    get_feature("pos_rel_virt").textChanged.connect(lambda: disable_feature("pos_rel_virt",["loc_abs","loc_indic_desc","loc_indic"]))
    get_feature("pos_rel_horz").textChanged.connect(lambda: disable_feature("pos_rel_horz",["loc_abs","loc_indic_desc","loc_indic"]))
    get_feature("loc_intrpl").textChanged.connect(lambda: disable_feature("loc_intrpl",["loc_abs","loc_indic_desc","loc_indic"]))
    owner_name = QgsExpressionContextUtils.projectScope(project).variable("project_owner")
    get_feature("owner").setText(owner_name)
    subAssetChange()
    check_fields(["loc_abs","loc_indic","pos_rel_virt","pos_rel_horz","loc_intrpl"])
    get_feature("asst_type").currentTextChanged.connect(subAssetChange)
    get_feature("asst_size").textChanged.connect(lambda: enable_feature("asst_size",["size_desc"]))
    get_feature("owner").editingFinished.connect(set_owner)
    get_feature("")
    ######################################
    # QgsExpressionContextUtils.setProjectVariable(project,'myvar','Hello World!')
    # QgsExpressionContextUtils.projectScope(project).variable('myvar')
