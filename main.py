import os, math, telebot
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# ambil token bot dari environment variable
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    bot.reply_to(message, "🎬 Proses video... teks muncul detik ke-3 dan mantul lembut...")

    file_info = bot.get_file(message.video.file_id)
    video = bot.download_file(file_info.file_path)

    # simpan video sementara
    with open("input.mp4", "wb") as f:
        f.write(video)

    clip = VideoFileClip("input.mp4")
    dur = clip.duration

    # teks atas dan bawah
    top = TextClip("@LOKALANN", fontsize=60, color='white',
                   stroke_color='black', stroke_width=4, font="Arial-Bold")
    bottom = TextClip("only tele", fontsize=60, color='white',
                      stroke_color='black', stroke_width=4, font="Arial-Bold")

    top = top.set_duration(dur).set_start(3)
    bottom = bottom.set_duration(dur).set_start(3)

    # fungsi posisi mantul lembut
    amp, period = 30, 4
    def pos_top(t): return ('center', abs(math.sin((t-3)*math.pi/period))*amp+10)
    def pos_bottom(t): return ('center', clip.h - bottom.h - abs(math.sin((t-3)*math.pi/period))*amp - 10)

    top = top.set_position(pos_top)
    bottom = bottom.set_position(pos_bottom)

    final = CompositeVideoClip([clip, top, bottom])
    final.write_videofile("output.mp4", codec="libx264", audio_codec="aac", threads=4, logger=None)

    with open("output.mp4", "rb") as outvid:
        bot.send_video(chat_id, outvid, caption="✅ Selesai!")

    # bersihin file sementara
    os.remove("input.mp4")
    os.remove("output.mp4")

print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
