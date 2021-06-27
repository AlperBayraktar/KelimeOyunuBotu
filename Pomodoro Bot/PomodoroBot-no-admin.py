import asyncio, io, os
from functools import reduce
from discord import File
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

async def showPomodoroData():
    return f"Çalışma Süresi: {bot.pomodoro.study} dakika\nMola Süresi: 5 dakika"

def howMuchLeft():
    secondsLeft = bot.pomodoro.secondsForFinish - bot.pomodoro.countedSeconds
    if secondsLeft < 60:
        return f"{bot.pomodoro.counting} sürenizin bitmesine: {secondsLeft} saniye.", secondsLeft
    else:
        return f"{bot.pomodoro.counting} sürenizin bitmesine: { round(secondsLeft/60, 1) } dakika", secondsLeft

async def renderOnCanvas(ctx, text, doFitToRow=True):
    imgWidth = 588
    imgHeight= 288
    bgPATH = os.path.join( os.path.dirname(os.path.abspath(__file__)), "bg.jpeg")
    image = Image.open(bgPATH)
    display = ImageDraw.Draw(image)

    if doFitToRow:
        text = fitToRow(toSplit=text, maxRowLength=30)

    font = ImageFont.truetype('font.ttf', 28)
    textWidth, textHeight = display.textsize(text, font=font)
    textX = (imgWidth - textWidth) // 2
    textY = (imgHeight - textHeight) // 2
    display.text( (textX, textY), text, fill=(255, 255, 255), font=font)

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 
    return await ctx.send(file=File(buffer, 'pomodoroResponse.png'))

def fitToRow(**args):
    maxRowLength, rowLength, row, toReturn = args["maxRowLength"], 0, [], ""
    for word in args["toSplit"].split() :
        row.append(word)
        rowLength += len(word)
        if rowLength > maxRowLength:
            toReturn  += " ".join(row[:-1]) + "\n"
            row = [row[-1]]
            rowLength = len(row[0])

    return toReturn[:-1] + "\n" + " ".join(row)

async def mentionUser(ctx, mention):
    message = await ctx.send(mention)
    await asyncio.sleep(1)
    await message.delete()

def getName(ctx):
    if ctx.author.nick == None:
        return ctx.author.name
    else:
        return ctx.author.nick

class Pomodoro:
    def __init__(self, study):
        self.study, self.break_= round(study, 1), 5
        self.isCounting, self.counting, self.secondsForFinish, self.countedSeconds =  False, "Çalışma", self.study*60, 0


bot = commands.Bot(command_prefix='$bot ')
bot.pomodoro = Pomodoro( 25 )


### Sayaç İşlemleri ###

@bot.command(name="başlat")
async def start_counter(ctx):
    if bot.pomodoro.isCounting:
        return await mentionUser(ctx, f"{ctx.author.mention} sayaç zaten çalışıyor!")


    mention = ctx.author.mention
    await renderOnCanvas(ctx, await showPomodoroData())

    bot.pomodoro.isCounting = True

    timerMessage = await ctx.send(f"{mention} tarafından sayaç başlatıldı!")
    await asyncio.sleep(3)

    while bot.pomodoro.isCounting:
        await asyncio.sleep(1)
        bot.pomodoro.countedSeconds += 1

        left = howMuchLeft()

        await timerMessage.edit(content=left[0])

        if left[1] == 0:
            bot.pomodoro.countedSeconds = 0

            if bot.pomodoro.counting == "Çalışma":
                bot.pomodoro.counting = "Mola"
                bot.pomodoro.secondsForFinish =  bot.pomodoro.break_ * 60
                await timerMessage.edit(content=f"{mention} Çalışma süresi bitti. Şimdi mola başlıyor, keyfini çıkar!")
                await asyncio.sleep(5)
            else:
                bot.pomodoro.counting = "Çalışma"
                bot.pomodoro.secondsForFinish =  bot.pomodoro.study * 60
                await timerMessage.edit(content=f"{mention} Mola süresi bitti. Şimdi çalışma vakti, verimli çalışmalar!")
                await asyncio.sleep(5)


@bot.command(name="durdur")
async def pause_counter(ctx):
    if not bot.pomodoro.isCounting:
        return await renderOnCanvas(ctx, "Sayaç zaten çalışmıyor!", False)

    bot.pomodoro.isCounting = False
    await renderOnCanvas(ctx, "Sayaç durduruldu! " + howMuchLeft()[0])

@bot.command(name="sayaç_sıfırla")
async def reset_counter(ctx):
    if not bot.pomodoro.isCounting:
        return await renderOnCanvas(ctx, "Sayaç zaten çalışmamakta!", False)

    bot.pomodoro.__init__( bot.pomodoro.study )
    await renderOnCanvas(ctx, "Sayaç sıfırlandı! Sayacı başlatmak için $bot başlat yazın")


#---------------------------------------------------------------------------------------------------------------------------------------------

### Ayarlar ###

@bot.command(name="ayarla")
async def set_counter(ctx, *, arg):
    print("ctx:", ctx)
    print("author:", ctx.author)
    print("message:", ctx.message)
    print("guild:", ctx.guild)
    print("arg:", arg)

    try:
        if float(arg)  < 0.1:
            raise TypeError
        bot.pomodoro = Pomodoro( float(arg) )
    except Exception as e:
        print(e)
        return await renderOnCanvas(ctx, f"{getName(ctx) }, çalışma süresi için lütfen sadece 0'dan büyük bir sayı giriniz!\nKomut `$bot ayarla dakika` şeklinde olmalıdır.")

    text = f"""
Sayaç ayarları değiştirildi!
{await showPomodoroData()}

-Değiştiren: {getName(ctx)}     
"""

    await renderOnCanvas(ctx, text, False)

@bot.command(name="ayar_sıfırla")
async def reset_counter(ctx):
    bot.pomodoro.__init__( 25 )
    await renderOnCanvas(ctx, f"Süre ayarları sıfırlandı!", False)

@bot.command(name="ayar_bilgi")
async def counter_info(ctx):
    await renderOnCanvas(ctx, await showPomodoroData(), False)

#---------------------------------------------------------------------------------------------------------------------------------------------

### Yardım ###

@bot.command(name="yardım")
async def yardım(ctx):
    info = """
The Domates Nasıl kullanılır?

`$bot başlat`: Daha öncesinde ayarlamış olduğunuz ya da durdurduğunuz sayacı başlatabilirsiniz. Sayaç otomatik bir şekilde saymaya başlayacaktır. Eğer ki bir süre ayarlamamışsanız, sayaç hazır ayarlarda başlayacaktır.

`$bot durdur`: Başlatmış olduğunuz sayacı durdurabilirsiniz.

`$bot sayaç_sıfırla`: Sayma işlemini sıfırlayabilirsiniz.

----------------------------------

`$bot ayarla dakika`: Çalışma süresini dakika yerine yazılan sayıya ayarlar. (Mola süresi 5 dakikadır.)

`$bot ayar_sıfırla`: Süre ayarını hazır ayarla değiştirir. Hazır ayar 25 dakika çalışma, 5 dakika moladır.

`$bot ayar_bilgi`: O anki süre ayarı hakkında bilgi verir.
"""

    await ctx.send(info)

@bot.command(name="pomodoro")
async def whatIsPomodoro(ctx):
    text = """
Pomodoro Tekniği, 1980'lerin sonunda Francesco Cirillo tarafından geliştirilen bir zaman yönetimi yöntemidir. Çalışma geleneksel olarak 25 dakika uzunluğunda, kısa molalarla ayrılır. Bunun içinse zamanlayıcı kullanılır. Her aralık, Cirillo'nun üniversite öğrencisiyken kullandığı domates şeklindeki mutfak zamanlayıcısından sonra, İtalyanca 'domates' kelimesinden bir pomodoro olarak ifade edilmeye başlanır. The Domates botu bu işlemi sizler için hazır komutlar ile daha kolay bir şekilde yapmanızı amaçlamaktadır."""
    await ctx.send(text)

with open("TOKEN.txt", "r", encoding="utf-8") as reader:
    bot.run( reader.read() ) 