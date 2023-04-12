
def mac_raw(mac: str) -> bytes:
    if len(mac) < 6:
        return None
    if type(mac) == bytes:
        return mac
    from binascii import unhexlify
    mac = mac.replace(' ', '').replace(':', '').replace('-', '')
    return unhexlify(mac)


def ap(en: bool = True, ap_essid: str = '', ap_password: str = '', ap_mac: str = '', ap_ifconfig: tuple = None, ap_hidden: bool = None, ap_channel: int = None, ap_authmode: int = None, mode: int = None):
    from time import sleep

    import network

    # global ap_if
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(en)
    if en == False:
        del ap_if
        print('AP disable')
        return False
    network.phy_mode(mode or network.MODE_11N)
    ap_if.config(essid=ap_essid or 'ESP_ap')
    ap_if.config(password=ap_password or '12345678')
    ap_if.config(authmode=ap_authmode or network.AUTH_WPA_PSK)
    ap_if.config(channel=ap_channel or 1)
    ap_if.config(hidden=ap_hidden or False)
    ap_if.config(mac=mac_raw(ap_mac) or ap_if.config('mac'))
    if ap_ifconfig:
        ap_if.ifconfig(ap_ifconfig)
    sleep(1)
    print('AP enable, ', ap_if.isconnected(), ap_if.status(), ap_if.ifconfig())


def wlan(en: bool = False, sta_essid: str = '', sta_password: str = '', sta_dhcp_hostname: str = '', sta_mac: str = '', sta_ifconfig: tuple = None, mode: int = None):
    from time import sleep

    import network

    # global sta_if
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(en)
    if en == False:
        del sta_if
        print('WLAN disable')
        return False
    network.phy_mode(mode or network.MODE_11N)
    sta_if.disconnect()
    sta_if.connect(sta_essid, sta_password)

    sta_if.config(dhcp_hostname=sta_dhcp_hostname or 'ESP_sta')
    sta_if.config(mac=mac_raw(sta_mac) or sta_if.config('mac'))
    if sta_ifconfig:
        sta_if.ifconfig(sta_ifconfig)
    i = 30
    while not sta_if.isconnected() and i > 0:
        print('WLAN connectting...', i)
        i -= 1
        sleep(1)
    print('WLAN enable, ', sta_if.isconnected(),
          sta_if.status(), sta_if.ifconfig())
    return sta_if.isconnected()

def web(en=1):
    import webrepl
    if en == 0:
        try:
            webrepl.stop()
            print('webrepl stop')
        except:
            print('no webrepl')
        finally:
            del webrepl
        return
    webrepl.start()
    print('webrepl run')
