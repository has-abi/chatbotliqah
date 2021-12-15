import numpy as np
from tensorflow import keras
import pickle
import json
from selenium import webdriver
import time
from PIL import Image

def load_model_assets():
    """
    Load the necessary assets for prediction such as the intents, model, tokenizer...

    Returns:
    dictionary: contains all the loaded files and data
    """
    # load model
    model = keras.models.load_model('./assets/chat_model')
    #load intents
    with open("./assets/data/intents.json") as file:
        data = json.load(file)
    # load tokenizer object
    with open('./assets/data/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # load label encoder object
    with open('./assets/data/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    assets = {"model":model,"data":data,"tokenizer":tokenizer,"encoder":lbl_encoder}    
    return assets




def predict(model, tokenizer, encoder,data ,input):
    """
    Predict the output message based on an input

    Parameters:
    model: the loaded NLP model
    tokenizer: the loaded tokenizer
    encoder: the loaded encoder
    data: the loaded data
    input: input data

    Returns:
    dictionary: returns the predicted response
    """
    result = model.predict(
    keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([input]),
     truncating='post',maxlen=20))
    tag = encoder.inverse_transform([np.argmax(result)])
    response = {}
    for i in data['intents']:
        if i['tag'] == tag:
            response['message'] = np.random.choice(i['responses'])
            if 'action' in i.keys():
                response['action'] = i['action']
    return response



def selenium_driver_init():
    """
    Initiate the webdriver

    Returns:
    driver: the initiated driver
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("./driver/chromedriver",chrome_options=chrome_options)
    return driver




def checkLiqahCenter(driver,CNIEp,DateExpirationCniep,NomArp,txtJourp,txtMoisp,txtAnneep,AC_Captchap):
    """
    Scrap for informations about the location of vacination 
    
    Paramerters:
    driver (driver): the webdriver
    CNIE (string): CNIE of the sender
    DateExpirationCnie (string): The end date of CNIE
    NomAr (string): the arabic name
    txtJour (string): the day of birth
    txtMois (string): the month of birth
    txtAnnee (string): the year of birth 
    AC_Captcha (string): the captcha code

    Returns:
    dictionary: returns the infos about the location of vacination
        essbAdresse: adress
        province: province
        commune: local
    """
    CNIE = driver.find_element_by_id("CNIE")
    DateExpirationCnie = driver.find_element_by_id("DateExpirationCnie")
    NomAr = driver.find_element_by_id("NomAr")
    txtJour = driver.find_element_by_id("txtJour")
    txtMois = driver.find_element_by_id("txtMois")
    txtAnnee = driver.find_element_by_id("txtAnnee")
    AC_Captcha = driver.find_element_by_id("AC_Captcha")
   
    CNIE.send_keys(CNIEp)
    DateExpirationCnie.send_keys(DateExpirationCniep)
    NomAr.send_keys(NomArp)
    txtJour.send_keys(txtJourp)
    txtMois.send_keys(txtMoisp)
    txtAnnee.send_keys(txtAnneep)
    AC_Captcha.send_keys(AC_Captchap)

    driver.find_element_by_id("btnRecherche").click()
    time.sleep(5)

    SpanEssbAdresse = driver.find_element_by_id("SpanEssbAdresse")
    SpanProvince = driver.find_element_by_id("SpanProvince")
    SpanCommune = driver.find_element_by_id("SpanCommune")
    print(driver)
    response = {}
    response['essbAdresse'] = SpanEssbAdresse.text
    response['province'] = SpanProvince.text
    response['commune'] = SpanCommune.text
    
    driver.quit()
    return response



def take_screenshoot(driver,index):
    """
    Initiate the web page and then take a screenshoot for the captcha code and save it

    Parameters:
    driver (driver): the webdriver
    index (int): an index
    """
    driver.get("https://services.liqahcorona.ma/")
    AC_Captcha = driver.find_element_by_id("AC_Captcha")
    AC_Captcha.send_keys("")
    time.sleep(2)
    driver.get_screenshot_as_file("./temp/screenshot.png")
    im = np.asarray(Image.open("./temp/screenshot.png"))
    im = im[700:778, 1210:1500]
    image = Image.fromarray(im)
    imname = "captcha" + str(index) + ".png"
    image.save("./temp/"+imname)
    time.sleep(2)




