# coding:gbk
from PyPoli import jr_jr
from PyPoli import qq_JZ
from PyPoli import weather_api
from PyPoli import baid_dr
from PyPoli import sj_pz
from PyPoli import Hello
from PyPoli import Time
from PyPoli import calculation
from PyPoli import open_url_exe
from PyPoli import qq_tx_mz
from PyPoli import chp
from PyPoli import LT
from PyPoli import kgmv
from PyPoli import xh
from PyPoli import lishi
from PyPoli import twqh
from PyPoli import tgrj
from PyPoli import djt
from PyPoli import rkl
from PyPoli import sao_hua
from PyPoli import sjyy
from PyPoli import yq
from PyPoli import fy
from PyPoli import gen
from RandomKey import key as k

HELLO = ['hello']
AGE = ['�����', '����']
XZ_TIME = ['����ʱ��']
ADDITION_JIA = ['������һ�¼ӷ�']
MULTIPLICATION = ['������һ�³˷�']
DIVISION = ['���Ҽ���һ�³���']
OPEN_URL_EXE = ['���Ҵ�']
JR_JR = ['������ʲô����']
QQ_JZ = ['QQ��ֵ���']
WEATHER_API = ['��ѯ����']
BAIDU_RS = ['�ٶ�����']
SJ_PZ = ['�ֻ����ò�ѯ']
QQ_TX_MZ = ['��ѯQQͷ��']
CHP = ['����']
KGMV = ['����mv']
XH = ['Ц��']
LS_SJ = ['������ʷ�¼�']
TWQH = ['��ζ�黰']
TGRJ = ['���ռ�']
DJT = ['������']
RKL = ['�ƿ���']
SAO = ['ɧ��']
SJYY = ['���һ��']
YQ = ['��ѯ����']
FY = ['����']
GEN = ['���ٿ�']

KEY_letter = '����һ����ĸ����'
KEY_str = '����һ���ַ�������'
YK_LT = '�ſ�api����'
TL_BOT = 'ͼ�������'
List_PRINT = (
    HELLO,
    AGE,
    XZ_TIME,
    ADDITION_JIA,
    MULTIPLICATION,
    DIVISION,
    OPEN_URL_EXE,
    JR_JR,
    QQ_JZ,
    WEATHER_API,
    BAIDU_RS,
    SJ_PZ,
    XH,
    LS_SJ,
    TWQH,
    TGRJ,
    DJT,
    RKL,
    SAO,
    SJYY,
    YQ,
    FY,
    GEN,
)
str_PRINT = (KEY_letter, KEY_str, YK_LT, TL_BOT)
while True:
    message = input("USER:")
    h = Hello.PoliRobot_Hello('Poli', '1', '����ʲô��˵���أ�')
    '''hello'''
    if message in HELLO:
        h.Hello()
        # h.Poilage()
        h.Poilmessage()
        continue

    '''����'''
    if message in AGE:
        h.Poilage()
        continue
    '''����ʱ��'''
    if message in XZ_TIME:
        Time.xz_time()
        continue
    '''����ӷ�'''
    if message in ADDITION_JIA:
        calculation.addition()
        continue
    '''����˷�'''
    if message in MULTIPLICATION:
        calculation.multiplication()
        continue
    '''�������'''
    if message in DIVISION:
        calculation.division()
        continue
    '''open��'''
    if message in OPEN_URL_EXE:
        open_url_exe.open_url_exe()
        continue
    '''��Сд��ĸ��������'''
    if message == KEY_letter:
        sl = int(input("������Ҫ��������λ����"))
        k.key_letter(sl)
        continue
    '''�ַ�����������'''
    if message == KEY_str:
        num = int(input("������Ҫ���ɼ�λ��"))
        k.key_str(num)
        continue
    '''���ս���'''
    if message in JR_JR:
        jr_jr.jr_jr()
        continue
    '''QQ��ֵ'''
    if message in QQ_JZ:
        qq_JZ.qq_JZ()
        continue
    '''������ѯ'''
    if message in WEATHER_API:
        weather_api.weather_api()
        continue
    '''�ٶ�����'''
    if message in BAIDU_RS:
        baid_dr.baidu_rs()
        continue
    '''�ֻ����ò�ѯ'''
    if message in SJ_PZ:
        sj_pz.sj_pz()
        continue
    '''QQͷ�����ֲ�ѯ'''
    if message in QQ_TX_MZ:
        qq_tx_mz.qq_tx_mz()
        continue
    '''����'''
    if message in CHP:
        chp.chp()
        continue
    '''�ſ�API����'''
    if message == YK_LT:
        print("�Ѵ��ſ�api����")
        print("����q�˳���")
        LT.LT()
        continue
    '''ͼ�������'''
    if message == TL_BOT:
        print("����q�˳�")
        from tl_bot import bot

        continue
    '''�ṷmv'''
    if message in KGMV:
        kgmv.gn()
        continue
    '''Ц��'''
    if message in XH:
        xh.XH()
        continue
    '''��ʷ�Ͻ���'''
    if message in LS_SJ:
        lishi.ls_sj()
        continue
    '''��ζ�黰'''
    if message in TWQH:
        twqh.twqh()
        continue
    '''���ռ�'''
    if message in TGRJ:
        tgrj.tgrj()
        continue
    '''������'''
    if message in DJT:
        djt.djt()
        continue
    '''�ƿ���'''
    if message in RKL:
        rkl.rkl()
        continue
    '''ɧ��'''
    if message in SAO:
        sao_hua.SAO()
        continue
    '''���һ��'''
    if message in SJYY:
        sjyy.yi()
        continue
    '''����'''
    if message in YQ:
        yq.yq()
        continue
    '''����'''
    if message in FY:
        fy.fy()
        continue
    '''���ٿ�'''
    if message in GEN:
        gen.gen()
        continue
    '''help'''
    if message == 'help':
        for i in List_PRINT:
            print(i)
        for i in str_PRINT:
            print(i)
        continue
    '''quit'''
    if message == 'q' or message == 'quit':
        print("�ټ����ˣ�")
        break
    else:
        print("\nδʶ�𵽴����")
        print("����help����ѯָ��\n")
        sjyy.yi()
        print("\n")
        continue
