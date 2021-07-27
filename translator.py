from googletrans import Translator
#pip install googletrans==4.0.0-rc1
# in other file , from translator import translate
# then t = translate("text")
translator = Translator()

def translate(text):
    
    print("Log:  ",translator.detect(text))
    
    return translator.translate(text,dest='ar').text

if __name__=='__main__':
    
    user_text = input("Enter text: ")
    translate(user_text)
