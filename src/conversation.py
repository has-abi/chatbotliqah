from flask import Blueprint, request, jsonify,send_from_directory
from http_constants.status import HttpStatus
from flasgger import swag_from

#from src.database import db
from src.outils import load_model_assets, predict, selenium_driver_init,checkLiqahCenter,take_screenshoot



conversation = Blueprint("conversation", __name__, url_prefix="/api/v1/conversation")


#load model assets
model_assets = load_model_assets()

#init vars
driver = None
index = 0

@conversation.route("/chat",methods=["POST"])
@swag_from('./docs/conversation/chat.yaml')
def chat():
    input = request.json.get("message")
    response = predict(model_assets["model"],model_assets["tokenizer"],
        model_assets["encoder"],model_assets["data"],input)
    return jsonify({"response": response}), HttpStatus.OK



@conversation.route("/check",methods=["POST","GET"])
@swag_from('./docs/conversation/check.yaml')
def check():
    global driver
    global index

    if request.method == "GET":
        driver = selenium_driver_init()
        take_screenshoot(driver,index)
        filname = "captcha" + str(index) + ".png"
        return send_from_directory("./", filname, as_attachment=True), HttpStatus.OK
        
    else:
        if 1 == 2:
            return jsonify({"error":"Something went wrong. Try again!"}), HttpStatus.INTERNAL_SERVER_ERROR
        else:
            CNIE = request.json.get("CNIE","")
            nomAr = request.json.get("NomAr","")
            dateExperationCNE = request.json.get("DateExperationCNE")

            txtJour = request.json.get("txtJour")
            txtMois = request.json.get("txtMois")
            txtAnnee = request.json.get("txtAnnee")
            captcha = request.json.get("AC_Captcha")
            print(driver.page_source)
            response = checkLiqahCenter(driver,CNIE,dateExperationCNE,nomAr,txtJour,txtMois,txtAnnee,captcha)
        
            return jsonify({"response":response}), HttpStatus.OK


