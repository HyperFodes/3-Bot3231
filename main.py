import os
import telebot
from flask import Flask, request

# ==========================================
# CONFIGURAÇÕES DO NOVO BOT (#3)
# ==========================================
TOKEN_BOT = "8638229733:AAEN-utrV_BXikCwTKKtVvFE2By31fEzVx0"
SEU_ID_TELEGRAM = 7665685378
ID_GRUPO_VIP = -1004348254600

bot = telebot.TeleBot(TOKEN_BOT, threaded=False)
app = Flask(__name__)

# --- GERADOR AUTOMÁTICO DE FILE ID ---
@bot.message_handler(content_types=['photo'])
def receber_qualquer_foto(message):
    file_id_gerado = message.photo[-1].file_id
    texto_resposta = (
        f"📸 *Nova imagem detectada pelo seu Bot #3!*\n\n"
        f"Copie o código abaixo:\n\n"
        f"`{file_id_gerado}`"
    )
    bot.reply_to(message, texto_resposta, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    bot.send_message(message.chat.id, "👋 Bot #3 Online!\n\nEnvie o Banner e o QR Code aqui no chat para coletarmos os novos File IDs.")

# ==========================================
# ROTAS DO SERVIDOR WEB (RENDER)
# ==========================================
@app.route('/' + TOKEN_BOT, methods=['POST'])
def getMessage():
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    except Exception:
        return "Erro", 500

@app.route("/")
def webhook():
    bot.remove_webhook()
    
    # 🛑 Altere aqui para a URL pública (.onrender.com) que aparece no seu painel!
    url_render = "https://SUA_URL_AQUI.onrender.com" 
    
    bot.set_webhook(url=f"{url_render}/{TOKEN_BOT}")
    return "Webhook configurado com sucesso no Bot 3!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)
