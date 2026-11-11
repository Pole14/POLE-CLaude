import json,sys
BAD={'fr':[(0,2.93),(8.655,9.6),(10.105,10.255),(11.8,99)],'es':[],'en':[(11.95,99)]}
def rt(RX,RY,t):
    if t<=RX[0]: return RY[0]
    if t>=RX[-1]: return RY[-1]
    for i in range(len(RX)-1):
        if RX[i]<=t<RX[i+1]:
            if RX[i+1]-RX[i]<=0.04 and abs(RY[i+1]-RY[i])>0.15: return RY[i]
            return RY[i]+(RY[i+1]-RY[i])*(t-RX[i])/(RX[i+1]-RX[i])
for f,lang in [(a.split(':')[0],a.split(':')[1]) for a in sys.argv[1:]]:
    sp=json.load(open(f)); RX=[a for a,_ in sp['rmap']]; RY=[b for _,b in sp['rmap']]
    bad=[]
    for i in range(int(round(sp['tot']*60))):
        t=i/60; r=round(rt(RX,RY,t)*60)/60
        for a,b in BAD[lang]:
            if a<=r<=b: bad.append((round(t,3),round(r,3)))
    print(f,'OK' if not bad else ('BAD',len(bad),bad[:6]))
