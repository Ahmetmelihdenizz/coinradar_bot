import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from src.main import get_recommendations, MIN_DAILY_PROFIT, TOP_N

TOKEN = "none"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Merhaba! CoinRadar botuna hoş geldiniz.\nÖneri için /recommend yazın.'
    )

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🔍 Öneriler hazırlanıyor, lütfen bekleyin...')
    try:
        recs, ok = get_recommendations(invest_amount=10000.0)
        if recs.empty:
            return await update.message.reply_text(
                '⚠️ Teklif üretilemedi, veri eksik olabilir.'
            )
    
        if ok:
            header = f"🔔 Günün Önerileri (₺10.000 yatırımla, net kâr ≥ ₺{MIN_DAILY_PROFIT}):"
        else:
            header = (f"⚠️ Hiç coin ₺{MIN_DAILY_PROFIT} net kâr eşiklerini geçemedi,\n"
                      f"   yine de en iyi {TOP_N} öneri:")
        msg = [header]
        for i, r in recs.iterrows():
            msg.append(
                f"{i+1}. {r['symbol']} — Net Kâr: {r['net_profit']} ₺ "
                f"(P={r['prob']:.3f}, Score={r['score']})"
            )
        await update.message.reply_text('\n'.join(msg))
    except Exception as e:
        import traceback
        logger.error(f'/recommend hata: {e}')
        logger.error(traceback.format_exc())
        await update.message.reply_text(f'🚫 Hata oluştu:\n{e}')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('recommend', recommend))
    app.run_polling()

if __name__ == '__main__':
    main()
