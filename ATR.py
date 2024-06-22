// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © matincrypto0

//@version=5

indicator("ATR / MA",format=format.percent)
ma(source, length, type) =>
    type == "SMA" ? ta.sma(source, length) :
     type == "EMA" ? ta.ema(source, length) :
     type == "WMA" ? ta.wma(source, length) :
     type == "VWMA" ? ta.vwma(source, length) :
     na
//
tf_i = input.timeframe(defval = "",title = "Indicator Timeframe")

ma_type   = input.string("EMA"  ,title="MA", group="Calculations",inline="1", options=["SMA", "EMA", "WMA", "VWMA"])
ma_source = input(close,title="", group="Calculations",inline="1")
ma_length = input.int(67,title="", group="Calculations", minval=1,inline="1")
ma = ma(ma_source, ma_length, ma_type)

sorsmv = input(defval = 30)
matf=request.security(symbol=syminfo.tickerid,timeframe=tf_i,expression=ma,gaps = barmerge.gaps_on)
atr_i = input.int(defval= 7,title="ATR",options=[3,7,14],group= "Calculations",tooltip= "Better not to change")
atr = ta.atr(atr_i)
atrtf=request.security(symbol=syminfo.tickerid,timeframe=tf_i,expression=atr,gaps = barmerge.gaps_on)
change_i= input.bool(defval=false,title="Sudden Change",group="Signal",inline="1")
change_i2=input.float(defval=0.099,title="Value",group = "Signal",inline="1")

breakout_i= input.bool(defval=false,title="Slope Breakout",group="Signal",inline="2")
band_i= input.float(defval= 0.075,title= "Limit",group= "Signal",inline= "2",minval= 0.001, maxval=0.999 )

//
diff = ma-ma[3]
maslope= diff/atr
maslopetf= request.security(symbol = syminfo.tickerid,timeframe=tf_i,expression = maslope)

mov = ta.sma(maslope,sorsmv)


plot(maslopetf,title="MA Slope",color=color.red)
upline= hline(band_i,title="Upper Band",linestyle = hline.style_solid)
hline(0.0,editable = false)
downline=hline(band_i * -1,title="Lower Band",linestyle= hline.style_solid)

sudden = maslopetf > maslopetf[1] + change_i2 or maslopetf < maslopetf[1] - change_i2
suddenchange = sudden and change_i
alertcondition(suddenchange,title="Sudden Change")
bgcolor(suddenchange==true ? color.rgb(230, 36, 36, 70) : na ,title="Sudden Change")


crossmatfup= ta.crossover(maslopetf,band_i)
crossmatfdown= ta.crossunder(maslopetf,band_i * -1)
if breakout_i ==  false
    crossmatfup:= false
    crossmatfdown :=false

for i=1 to 9
    if crossmatfup[i] == true
        crossmatfup := false
for i=1 to 9
    if crossmatfdown[i] == true
        crossmatfdown := false
anycross= crossmatfup or crossmatfdown
alertcondition(anycross,title="Slope Breakout")
// bgcolor(crossmatfup == true or crossmatfdown == true ?  color.rgb(240, 13, 164, 70) : na,title= "Slope Breakout")
plot(mov)
