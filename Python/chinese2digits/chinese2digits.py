from  decimal import Decimal
import re


CHINESE_CHAR_LIST = ['幺','零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']
CHINESE_SIGN_LIST = ['负','正','-','+']
CHINESE_CONNECTING_SIGN_LIST = ['.','点','·']
CHINESE_PERCENT_STRING = '百分之'
CHINESE_PURE_NUMBER_LIST = ['幺', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十','零']

CHINESE_SIGN_DICT = {'负':'-','正':'+','-':'-','+':'+'}
CHINESE_PERCENT_DICT = {'百分之':'%'}
CHINESE_CONNECTING_SIGN_DICT = {'.':'.','点':'.','·':'.'}
CHINESE_COUNTING_STRING = {'十':10, '百':100, '千':1000, '万':10000, '亿':100000000}
CHINESE_PURE_COUNTING_UNIT_LIST = list(CHINESE_COUNTING_STRING.keys())

TRADITIONAl_CONVERT_DICT = {'壹': '一', '贰': '二', '叁': '三', '肆': '四', '伍': '五', '陆': '六', '柒': '七',
                           '捌': '八', '玖': '九'}
SPECIAL_TRADITIONAl_COUNTING_UNIT_CHAR_DICT = {'拾': '十', '佰': '百', '仟':'千', '萬':'万', '億':'亿'}

SPECIAL_NUMBER_CHAR_DICT = {'两':'二','俩':'二'}

"""
中文转阿拉伯数字
"""
common_used_ch_numerals = {'幺':1,'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}

def coreCHToDigits(chineseChars,simpilfy=None,resultType='string'):
    if simpilfy is None:
        if chineseChars.__len__()>1:
            """
            如果字符串大于1 且没有单位 ，simpilfy 规则
            """
            for chars in chineseChars:
                if CHINESE_COUNTING_STRING.get(chars) is None:
                    simpilfy = True

                else:
                    simpilfy = False
                    break

    if simpilfy is False:
        total = 0
        countingUnit = 1              #表示单位：个十百千,用以计算单位相乘 例如八百万 百万是相乘的方法，但是如果万前面有 了一千八百万 这种，千和百不能相乘，要相加...
        countingUnitFromString = [1]                            #原始字符串提取的单位应该是一个list  在计算的时候，新的单位应该是本次取得的数字乘以已经发现的最大单位，例如 4千三百五十万， 等于 4000万+300万+50万
        for i in range(len(chineseChars) - 1, -1, -1):
            val = common_used_ch_numerals.get(chineseChars[i])
            if val >= 10 and i == 0:  #应对 十三 十四 十*之类，说明为十以上的数字，看是不是十三这种
                #取最近一次的单位
                if val > countingUnit:  #如果val大于 contingUnit 说明 是以一个更大的单位开头 例如 十三 千二这种
                    countingUnit = val   #赋值新的计数单位
                    total = total + val    #总值等于  全部值加上新的单位 类似于13 这种
                    countingUnitFromString.append(val)
                else:
                    countingUnitFromString.append(val)
                    # 计算用的单位是最新的单位乘以字符串中最大的原始单位
                    # countingUnit = countingUnit * val
                    countingUnit = max(countingUnitFromString) * val
                    #total =total + r * x
            elif val >= 10:
                if val > countingUnit:
                    countingUnit = val
                    countingUnitFromString.append(val)
                else:
                    countingUnitFromString.append(val)
                    # 计算用的单位是最新的单位乘以字符串中最大的原始单位
                    # countingUnit = countingUnit * val
                    countingUnit = max(countingUnitFromString) * val
            else:
                total = total + countingUnit * val
        total = str(total)
    else:
        total=''
        for i in chineseChars:
            if common_used_ch_numerals.get(i) is None:
                raise TypeError ('string contains illegal char')
            total = total+str(common_used_ch_numerals.get(i))
    return total
def chineseToDigits(chineseChars,simpilfy=None,percentConvert = True,resultType='string'):
    #kaka
    chineseCharsDotSplitList = []
    chineseChars = str(chineseChars)
    tempChineseChars = chineseChars


    """
    看有没有符号
    """
    sign = ''
    for chars in tempChineseChars:
        if CHINESE_SIGN_DICT.get(chars) is not None:
            sign = CHINESE_SIGN_DICT.get(chars)
            tempChineseChars = tempChineseChars.replace(chars, '')
    """
    防止没有循环完成就替换 报错
    """
    chineseChars = tempChineseChars
    """
    看有没有百分号
    """
    percentString = ''
    if CHINESE_PERCENT_STRING in chineseChars:
        percentString = '%'
        chineseChars = chineseChars.replace(CHINESE_PERCENT_STRING,'')

    """
    小数点切割，看看是不是有小数点
    """
    for chars in list(CHINESE_CONNECTING_SIGN_DICT.keys()):
        if chars in chineseChars:
            chineseCharsDotSplitList = chineseChars.split(chars)

    if chineseCharsDotSplitList.__len__()==0:
        convertResult = coreCHToDigits(chineseChars,simpilfy)
    else:
        convertResult = ''
        if chineseCharsDotSplitList[0] == '':
            """
            .01234 这种开头  用0 补位
            """
            convertResult = '0.'+ coreCHToDigits(chineseCharsDotSplitList[1],simpilfy)
        else:
            convertResult = coreCHToDigits(chineseCharsDotSplitList[0],simpilfy) + '.' + coreCHToDigits(chineseCharsDotSplitList[1],simpilfy)

    convertResult = sign + convertResult

    if percentConvert == True:
        if percentString == '%':
            convertResult = float(Decimal(convertResult)/100)
        if resultType == 'int':
            total = int(convertResult)
        elif resultType == 'float':
            total = float(convertResult)
        elif resultType == 'string':
            total = str(convertResult)
        else:
            total = str(convertResult)
    else:
        if percentString == '%':
            if resultType == 'string':
                total = convertResult + percentString
            else:
                convertResult =  float(Decimal(convertResult)/100)
                if resultType == 'int':
                    total = int(convertResult)
                elif resultType == 'float':
                    total = float(convertResult)
                else:
                    total = str(convertResult)
        else:
            if resultType == 'int':
                total = int(convertResult)
            elif resultType == 'float':
                total = float(convertResult)
            elif resultType == 'string':
                total = str(convertResult)
            else:
                total = str(convertResult)
    return total


def checkChineseNumberReasonable(chNumber):
    if chNumber.__len__()>0:
        """
        如果汉字长度大于0 则判断是不是 万  千  单字这种
        """
        for i in CHINESE_PURE_NUMBER_LIST:
            if i in chNumber:
                return True
    return False

"""
繁体简体转换 及  单位  特殊字符转换 两千变二千
"""
def traditionalTextConvertFunc(chString,simplifConvertSwitch=True):
    chStringList = list(chString)
    stringLength = len(list(chStringList))

    if simplifConvertSwitch == True:
        for i in range(stringLength):
            #繁体中文数字转简体中文数字
            if TRADITIONAl_CONVERT_DICT.get(chStringList[i],'') != '':
                chStringList[i] = TRADITIONAl_CONVERT_DICT.get(chStringList[i],'')

    #检查繁体单体转换
    for i in range(stringLength):
        #如果 前后有 pure 汉字数字 则转换单位为简体
        if SPECIAL_TRADITIONAl_COUNTING_UNIT_CHAR_DICT.get(chStringList[i],'') != '':
            # 如果前后有单纯的数字 则进行单位转换
            if i == 0:
                if chStringList[i+1] in CHINESE_PURE_NUMBER_LIST:
                    chStringList[i] = SPECIAL_TRADITIONAl_COUNTING_UNIT_CHAR_DICT.get(chStringList[i], '')
            elif i == stringLength-1:
                if chStringList[i-1] in CHINESE_PURE_NUMBER_LIST:
                    chStringList[i] = SPECIAL_TRADITIONAl_COUNTING_UNIT_CHAR_DICT.get(chStringList[i], '')
            else:
                if chStringList[i-1] in CHINESE_PURE_NUMBER_LIST or \
                        chStringList[i+1] in CHINESE_PURE_NUMBER_LIST :
                    chStringList[i] = SPECIAL_TRADITIONAl_COUNTING_UNIT_CHAR_DICT.get(chStringList[i], '')
        #特殊变换 俩变二
        if SPECIAL_NUMBER_CHAR_DICT.get(chStringList[i], '') != '':
            # 如果前后有单位 则进行转换
            if i == 0:
                if chStringList[i+1] in CHINESE_PURE_COUNTING_UNIT_LIST:
                    chStringList[i] = SPECIAL_NUMBER_CHAR_DICT.get(chStringList[i], '')
            elif i == stringLength-1:
                if chStringList[i-1] in CHINESE_PURE_COUNTING_UNIT_LIST:
                    chStringList[i] = SPECIAL_NUMBER_CHAR_DICT.get(chStringList[i], '')
            else:
                if chStringList[i-1] in CHINESE_PURE_COUNTING_UNIT_LIST or \
                        chStringList[i+1] in CHINESE_PURE_COUNTING_UNIT_LIST :
                    chStringList[i] = SPECIAL_NUMBER_CHAR_DICT.get(chStringList[i], '')
    return ''.join(chStringList)

"""
标准表述转换  三千二 变成 三千零二  三千十二变成 三千零一十二
"""
def standardChNumberConvert(chNumberString):
    chNumberStringList = list(chNumberString)
    #十位补一：
    for i in range(len(chNumberStringList)):
        if chNumberStringList[i] == '十':
            if i == 0 :
                chNumberStringList.insert(i,'一')
            else:
                #如果没有左边计数数字 插入1
                if chNumberStringList[i-1] in CHINESE_PURE_NUMBER_LIST:
                    chNumberStringList.insert(i,'一')

    #差位补零
    #逻辑 如果最后一个单位 不是十结尾 而是百以上 则数字后面补一个比最后一个出现的单位小一级的单位
    lastCountingUnit = 0
    for i in range(len(chNumberStringList)-1, -1, -1):
        if chNumberStringList[i] == '十':
            if i == 0 :
                chNumberStringList.insert(i,'一')
            else:
                #如果没有左边计数数字 插入1
                if chNumberStringList[i-1] in CHINESE_PURE_NUMBER_LIST:
                    chNumberStringList.insert(i,'一')



#以百分号作为大逻辑区分。 是否以百分号作为新的数字切割逻辑 所以同一套切割逻辑要有  或关系   有百分之结尾 或者  没有百分之结尾
takingChineseNumberRERules = re.compile('(?:(?:(?:百分之){0,1}[正负]{0,1})|(?:[正负]{0,1}(?:百分之){0,1}))'
                                        '(?:(?:[一二三四五六七八九十千万亿兆幺零(?:百(?!分之))]+(?:点[一二三四五六七八九幺零]+){0,1})'
                                        '|(?:(?:[一二三四五六七八九十千万亿兆幺零(?:百(?!分之))]+){0,1}点[一二三四五六七八九幺零]+))(?=百分之)'
                                        '|(?:(?:(?:百分之){0,1}[正负]{0,1})|(?:[正负]{0,1}(?:百分之){0,1}))'
                                        '(?:(?:[一二三四五六七八九十千万亿兆幺零(?:百(?!分之))]+(?:点[一二三四五六七八九幺零]+){0,1})'
                                        '|(?:(?:[一二三四五六七八九十千万亿兆幺零(?:百(?!分之))]+){0,1}点[一二三四五六七八九幺零]+))')

def takeChineseNumberFromString(chText,simpilfy=None,percentConvert = True,method = 'regex',simplifConvert= True):
    """
    :param chText: chinese string
    :param simpilfy: convert type.Default is None which means check the string automatically. True means ignore all the counting unit and just convert the number.
    :param percentConvert: convert percent simple. Default is True.  3% will be 0.03 in the result
    :param method: chinese number string cut engine. Default is regex. Other means cut using python code logic only
    :param simplifConvert: Switch to convert the Traditional Chinese character to Simplified chinese
    :return: Dict like result. 'inputText',replacedText','CHNumberStringList':CHNumberStringList,'digitsStringList'
    """

    """
    简体转换开关
    """

    chText = traditionalTextConvertFunc(chText,simplifConvert)

    """
    字符串 汉字数字字符串切割提取
    正则表达式方法
    """
    if method == 'regex':
        CHNumberStringListTemp = takingChineseNumberRERules.findall(chText)
        CHNumberStringList= []
        for tempText in CHNumberStringListTemp:
            if checkChineseNumberReasonable(tempText):
                CHNumberStringList.append(tempText)
    else:
        tempCHNumberChar = ''
        tempCHSignChar = ''
        tempCHConnectChar = ''
        tempCHPercentChar = ''
        CHNumberStringList = []
        tempTotalChar = ''
        """
        将字符串中所有中文数字列出来
        """
        i = 0
        while i < chText.__len__():
            """
            看是不是符号。如果是，就记录。
            """
            if chText[i] in CHINESE_SIGN_LIST:


                """
                如果 符号前面有数字  则 存到结果里面
                """
                if tempCHNumberChar != '':
                    if checkChineseNumberReasonable(tempTotalChar):
                        CHNumberStringList.append(tempTotalChar)
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''
                    else:
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''
                """
                如果 前一个符号赋值前，临时符号不为空，则把之前totalchar里面的符号替换为空字符串
                """
                if tempCHSignChar != '':
                    tempTotalChar = tempTotalChar.replace(tempCHSignChar, '')

                tempCHSignChar = chText[i]
                tempTotalChar = tempTotalChar + tempCHSignChar
                i = i + 1
                continue

            """
            不是字符是不是"百分之"。
            """
            if chText[i:(i + 3)] == CHINESE_PERCENT_STRING:


                """
                如果 百分之前面有数字  则 存到结果里面
                """
                if tempCHNumberChar != '':
                    if checkChineseNumberReasonable(tempTotalChar):
                        CHNumberStringList.append(tempTotalChar)
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''
                    else:
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''

                """
                如果 前一个符号赋值前，临时符号不为空，则把之前totalchar里面的符号替换为空字符串
                """
                if tempCHPercentChar != '':
                    tempTotalChar = tempTotalChar.replace(tempCHPercentChar, '')

                tempCHPercentChar = chText[i:(i + 3)]
                tempTotalChar = tempTotalChar + tempCHPercentChar
                i = i + 3
                continue
            """
            看是不是点
            """
            if chText[i] in CHINESE_CONNECTING_SIGN_LIST:
                """
                如果 前一个符号赋值前，临时符号不为空，则把之前totalchar里面的符号替换为空字符串
                """
                if tempCHConnectChar != '':
                    tempTotalChar = tempTotalChar.replace(tempCHConnectChar, '')

                tempCHConnectChar = chText[i]
                tempTotalChar = tempTotalChar + tempCHConnectChar
                i = i + 1
                continue

            """
            看是不是数字
            """
            if chText[i] in CHINESE_CHAR_LIST:
                """
                如果 在字典里找到，则记录该字符串
                """
                tempCHNumberChar = chText[i]
                tempTotalChar = tempTotalChar + tempCHNumberChar
                i = i + 1
                continue
            else:
                """
                遇到第一个在字典里找不到的，且最终长度大于符号与连接符的。所有临时记录清空, 最终字符串被记录
                """
                if tempTotalChar.__len__()>len(tempCHPercentChar + tempCHConnectChar + tempCHSignChar):
                    if checkChineseNumberReasonable(tempTotalChar):
                        CHNumberStringList.append(tempTotalChar)
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''
                    else:
                        tempCHPercentChar = ''
                        tempCHConnectChar = ''
                        tempCHSignChar = ''
                        tempCHNumberChar = ''
                        tempTotalChar = ''
                """
                遇到第一个在字典里找不到的，且最终长度小于符号与连接符的。所有临时记录清空,。
                """
                i = i + 1
        """
        将temp 清干净
        """
        if tempTotalChar.__len__() > len(tempCHPercentChar + tempCHConnectChar + tempCHSignChar):
            if checkChineseNumberReasonable(tempTotalChar):
                CHNumberStringList.append(tempTotalChar)
                tempCHPercentChar = ''
                tempCHConnectChar = ''
                tempCHSignChar = ''
                tempCHNumberChar = ''
                tempTotalChar = ''
            else:
                tempCHPercentChar = ''
                tempCHConnectChar = ''
                tempCHSignChar = ''
                tempCHNumberChar = ''
                tempTotalChar = ''


    """
    进行标准汉字字符串转换 例如 二千二  转换成二千零二
    """
    CHNumberStringListTemp = CHNumberStringList

    """
    将中文转换为数字
    """
    digitsStringList = []
    replacedText = chText
    if CHNumberStringList.__len__()>0:
        digitsStringList = list(map(lambda x:chineseToDigits(x,simpilfy=simpilfy,percentConvert=percentConvert),CHNumberStringList))
        tupleToReplace = list(zip(CHNumberStringList,digitsStringList,list(map(len,CHNumberStringList))))


        """
        按照提取出的中文数字字符串长短排序，然后替换。防止百分之二十八 ，二十八，这样的先把短的替换完了的情况
        """
        tupleToReplace = sorted(tupleToReplace, key=lambda x: -x[2])
        for i in range(tupleToReplace.__len__()):
            replacedText = replacedText.replace(tupleToReplace[i][0],tupleToReplace[i][1])


    finalResult = {
        'inputText':chText,
        'replacedText':replacedText,
        'CHNumberStringList':CHNumberStringList,
        'digitsStringList':digitsStringList
    }
    return finalResult


DIGITS_CHAR_LIST = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
DIGITS_SIGN_LIST = ['-','+']
DIGITS_CONNECTING_SIGN_LIST = ['.']
DIGITS_PERCENT_STRING = '%'
takingDigitsRERule = re.compile('(?:\+|\-){0,1}\d+(?:\.\d+){0,1}(?:\%){0,1}|(?:\+|\-){0,1}\.\d+(?:\%){0,1}')

def takeDigitsNumberFromString(textToExtract,percentConvert = False):
    digitsNumberStringList = takingDigitsRERule.findall(textToExtract)
    """
    最后检查有没有百分号
    """
    """
    看有没有百分号
    """
    if percentConvert is True:
        for i in range(digitsNumberStringList.__len__()):
            if digitsNumberStringList[i].__contains__('%'):
                digitsNumberStringList[i] = str(Decimal(digitsNumberStringList[i].replace('%', '')) / 100)

    finalResult = {
        'inputText':textToExtract,
        'digitsNumberStringList':digitsNumberStringList
    }

    return finalResult

if __name__=='__main__':
    #将百分比转为小数
    print(takeDigitsNumberFromString('234%lalalal-%nidaye+2.34%',percentConvert=True))
    #使用正则表达式，用python的pcre引擎，没有使用re2引擎，所以， 因此不建议输入文本过长造成递归问题
    print(takeChineseNumberFromString('三亿二千一十七'))
    print(takeChineseNumberFromString('五亿七千万'))
    #使用普通顺序逻辑引擎
    print(takeChineseNumberFromString('负百分之点二八你好啊百分之三五是不是点五零百分之负六十五点二八',method='normal'))