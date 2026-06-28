from tensorflow.keras.models import load_model

classes = {
    0:"Speed limit 20",1:"Speed limit 30",2:"Speed limit 50",
    3:"Speed limit 60",4:"Speed limit 70",5:"Speed limit 80",
    6:"End 80",7:"Speed limit 100",8:"Speed limit 120",
    9:"No passing",10:"No passing trucks",11:"Right-of-way",
    12:"Priority road",13:"Yield",14:"Stop",15:"No vehicles",
    16:"Vehicles prohibited",17:"No entry",18:"General caution",
    19:"Danger curve left",20:"Danger curve right",21:"Double curve",
    22:"Bumpy road",23:"Slippery road",24:"Road narrows",
    25:"Road work",26:"Traffic signals",27:"Pedestrians",
    28:"Children crossing",29:"Bicycle crossing",30:"Ice/Snow",
    31:"Wild animals",32:"End limits",33:"Turn right",
    34:"Turn left",35:"Ahead only",36:"Straight/right",
    37:"Straight/left",38:"Keep right",39:"Keep left",
    40:"Roundabout",41:"End no passing",42:"End truck no passing"
}

def get_model():
    return load_model("models/traffic_sign_model.h5")