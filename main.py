import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask, request

# ==========================================
# 1. CONFIGURAÇÕES DO NOVO BOT (#3)
# ==========================================
TOKEN_BOT = "8638229733:AAEN-utrV_BXikCwTKKtVvFE2By31fEzVx0"
SEU_ID_TELEGRAM = 7665685378
ID_GRUPO_VIP = -1004348254600

# Mande as fotos para o bot para pegar os novos códigos e substituir aqui depois!
LINK_BANNER_BOAS_VINDAS = "COLOQUE_O_FILE_ID_DO_BANNER_AQUI"
LINK_QRCODE_PIX = "COLOQUE_O_FILE_ID_DO_QRCODE_AQUI"

# Suas carteiras oficiais configuradas
CARTEIRA_BTC = "bc1qv0vt52xa356n5sfz6ayq9enfr77teemr4htqtf"
CARTEIRA_ETH = "0x68c4a8312b50D1506619314b29981Fe3731035E0"
CARTEIRA_LTC = "ltc1qpcuzhk48n0udpcv64n5x8fjapf505j2qj3ketf"
CARTEIRA_USDT = "0x1e75616b576d7f66f0cd8176ee2f70bef1fe8ddb"

bot = telebot.TeleBot(TOKEN_BOT, threaded=False)
app = Flask(__name__)

# Dicionário para rastrear quem está comprando
usuarios_comprando = {}

# ==========================================
# 2. COMANDOS E FLUXO DO BOT
# ==========================================

# --- MENSAGEM DE BOAS VINDAS DO BOT ---
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    try:
        idioma_usuario = message.from_user.language_code
        markup = InlineKeyboardMarkup(row_width=1)
        
        if idioma_usuario and 'pt' in idioma_usuario:
            texto = "👋 Bem-vindo ao bot oficial do Criador!\n\nGaranta seu *ACESSO VITALÍCIO* (pague uma vez e fique para sempre) escolhendo sua forma de pagamento:"
            btn_pix = InlineKeyboardButton("🇧🇷 PIX (R$ 30,00)", callback_data="menu_pix")
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            markup.add(btn_pix, btn_stars, btn_crypto)
        else:
            texto = "👋 Welcome to the Creator's official bot!\n\nGet your *LIFETIME ACCESS* (pay once, stay forever) by choosing your payment method:"
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            btn_pix = InlineKeyboardButton("🇧🇷 Brazilian PIX (R$ 30,00)", callback_data="menu_pix")
            markup.add(btn_stars, btn_crypto, btn_pix)
        
        bot.send_photo(message.chat.id, LINK_BANNER_BOAS_VINDAS, caption=texto, reply_markup=markup, parse_mode="Markdown")
        
    except Exception:
        # Texto alternativo caso os File IDs ainda não tenham sido configurados nas variáveis
        texto_config = "👋 Bot #3 Configurado!\n\n📥 *Como gerar os File IDs agora:*\nBasta enviar a foto do seu Banner e do seu QR Code aqui no chat. O bot vai ler e te devolver o código de texto na hora!"
        bot.send_message(message.chat.id, texto_config, reply_markup=markup, parse_mode="Markdown")


# --- GERENCIAMENTO DOS BOTÕES ---
@bot.callback_query_handler(func=lambda call: True)
def escutar_botoes(call):
    chat_id = call.message.chat.id

    if call.data == "menu_pix":
        usuarios_comprando[chat_id] = "PIX - R$ 30"
        texto_instrucao = (
            f"⚡ *Plano Vitalício de R$ 30 selecionado!*\n\n"
            f"1️⃣ Escaneie o QR Code acima no app do seu banco.\n"
            f"2️⃣ *ATENÇÃO:* Digite manualmente o valor exato de: *R$ 30,00*\n\n"
            f"👇 Após fazer o pagamento, envie a *FOTO DO COMPROVANTE* aqui no chat para liberação!\n\n"
            f"ℹ️ Suporte: @HardHandsG"
        )
        try:
            bot.send_photo(chat_id, LINK_QRCODE_PIX, caption=texto_instrucao, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, texto_instrucao, parse_mode="Markdown")

    elif call.data == "stars_900":
        bot.send_invoice(
            chat_id=chat_id,
            title="Lifetime VIP — 900 Stars",
            description="Permanent access to the Creator's Minecraft VIP group.",
            invoice_payload="vip_stars_900",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Stars", amount=900)]
        )

    elif call.data == "menu_crypto":
        usuarios_comprando[chat_id] = "Crypto - $ 5.00"
        texto_crypto = (
            f"🪙 *Lifetime VIP Access — Crypto Dollars*\n\n"
            f"Value: *$ 5.00 USD*\n\n"
            f"🔹 *USDT (Network: BEP-20 / BSC):*\n`{CARTEIRA_USDT}`\n\n"
            f"🔸 *LTC (Litecoin):*\n`{CARTEIRA_LTC}`\n\n"
            f"🔹 *BTC (Bitcoin):*\n`{CARTEIRA_BTC}`\n\n"
            f"🔸 *ETH (Ethereum):*\n`{CARTEIRA_ETH}`\n\n"
            f"👇 After sending the payment, upload the *TRANSACTION RECEIPT* here!\n\n"
            f"ℹ️ Support: @HardHandsG"
        )
        bot.send_message(chat_id, texto_crypto, parse_mode="Markdown")

    elif call.data.startswith("aprovar_"):
        bot.answer_callback_query(call.id)
        id_cliente = call.data.split("_")[1]
        try:
            link_grupo = bot.create_chat_invite_link(chat_id=ID_GRUPO_VIP, member_limit=1)
            bot.send_message(id_cliente, f"✅ Seu pagamento foi aprovado! / Your payment has been approved!\n\nLink para entrar no grupo VIP:\n{link_grupo.invite_link}")
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption="✅ Cliente aprovado e link permanente enviado!", reply_markup=None)
        except Exception as e:
            bot.send_message(chat_id, f"❌ Erro ao gerar link. Certifique-se de que o BOT #3 está no grupo VIP como ADMINISTRADOR.\n\nErro: {e}")

    elif call.data.startswith("recusar_"):
        bot.answer_callback_query(call.id)
        id_cliente = call.data.split("_")[1]
        try:
            bot.send_message(id_cliente, "❌ Pagamento recusado / Payment declined.\nSuporte: @HardHandsG")
            bot.edit_message_caption(chat_id=chat_id, message_id=call.message.message_id, caption="❌ Pagamento recusado.", reply_markup=None)
        except Exception as e:
            bot.send_message(chat_id, f"Erro ao processar recusa. Erro: {e}")


# --- 3. RECONHECIMENTO DE FOTOS (COMPROVANTE OU EXTRATOR DE FILE ID) ---
@bot.message_handler(content_types=['photo'])
def tratar_fotos(message):
    chat_id = message.chat.id
    file_id_gerado = message.photo[-1].file_id
    
    # Se o usuário iniciou um processo de compra, a foto é tratada como comprovante
    if chat_id in usuarios_comprando:
        forma_pagamento = usuarios_comprando[chat_id]
        markup_admin = InlineKeyboardMarkup()
        markup_admin.add(
            InlineKeyboardButton("✅ Aprovar", callback_data=f"aprovar_{chat_id}"),
            InlineKeyboardButton("❌ Recusar", callback_data=f"recusar_{chat_id}")
        )
        bot.send_photo(
            SEU_ID_TELEGRAM, 
            file_id_gerado, 
            caption=f"🔔 NOVO COMPROVANTE (BOT #3)!\n\nUsuário: @{message.from_user.username} (ID: {chat_id})\nMétodo: {forma_pagamento}", 
            reply_markup=markup_admin
        )
        bot.send_message(chat_id, "⏳ Comprovante recebido! Aguarde a verificação.\n⏳ Receipt received! Please wait for verification.")
        del usuarios_comprando[chat_id]
        
    # Se for VOCÊ enviando fotos fora do fluxo de compra, o bot vira um extrator de File ID automático!
    else:
        texto_resposta = (
            f"📸 *Nova imagem detectada pelo seu Bot #3!*\n\n"
            f"Copie o código abaixo para colocar nas variáveis:\n\n"
            f"`{file_id_gerado}`"
        )
        bot.reply_to(message, texto_resposta, parse_mode="Markdown")


# --- 4. ENTREGA VIA STARS ---
@bot.pre_checkout_query_handler(func=lambda query: True)
def processar_pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def pagamento_stars_sucesso(message):
    chat_id = message.chat.id
    try:
        link_grupo = bot.create_chat_invite_link(chat_id=ID_GRUPO_VIP, member_limit=
