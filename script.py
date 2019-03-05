from PyQt5.QtCore import *
from PyQt5.QtGui import *
def open(dialog, layer, feature):
    asset_type = dialog.findChild(QObject,"asst_type")
    asset_subtype = dialog.findChild(QObject,"sub-type")
    asset_owner = dialog.findChild(QObject, "owner")
    feature_code = dialog.findChild(QObject, "feat_code")
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
        asset_subtype.clear()
        for i in range (0, len(dependencies[asset_type.currentText()])):
                data = dependencies[asset_type.currentText()][i]
                asset_subtype.addItem(dependencies[asset_type.currentText()][i], data)
    def disable_field():
        text = feature_code.text()
        if text == "NULL" or text is "":
            asset_owner.setEnabled(True)
        else:
            asset_owner.setDisabled(True)
    feature_code.textChanged.connect(disable_field)
    subAssetChange()
    value = asset_subtype.currentIndex()
    asset_subtype.setCurrentIndex(value)
    asset_type.currentTextChanged.connect(subAssetChange)

    # AllItems = [changemenu.itemText(i) for i in range(changemenu.count())]
    # lineEdit.setText(" ".join(str(x) for x in AllItems))
    # Poshel gulyat asgasg