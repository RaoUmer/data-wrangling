from lxml.html import parse
parsed = parse(open('comtrade_trade_data.sdmx'))



doc = parsed.getroot()
XHTML_NAMESPACE = "http://unstats.un.org/structure/key_families/cross/UN_COMTRADE_HS"
XHTML = "{%s}" % XHTML_NAMESPACE
NSMAP = {'unsc': XHTML_NAMESPACE}
