import scapy.all as scapy 
import argparse

class Network_scan():
	def __init__(self):
		self.broadcast = "ff:ff:ff:ff:ff:ff"
		
	def input(self):
		usage = "%prog [options] \n[-i 192.168.1.0/24]"
		arg_object = argparse.ArgumentParser(usage)
		arg_object.add_argument("-i","--ip",dest="ip",help="ip aralıgi gir")
		args = arg_object.parse_args()
		
		if args.ip:
			return args 
	
	def scan(self,ip):
		arp_request_packet = scapy.ARP(pdst=ip) # ip-mac eşleştirmesi için 
		broadcast_packet = scapy.Ether(dst=self.broadcast) # broadcast yayın yapacağı anlamına gelir.
		combined_packet = broadcast_packet/arp_request_packet # paketleri birleştirdik...
		(answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1) # birleştirilmiş paket gönderimi için srp() kullandık bu bize cevaplananlar ve cevaplanmayanlar olarak iki farklı paket döndürüyor, timeout=1 de cevaplanmayan paketleri geçmek için kullanılır.
		answered_list.summary()
		
		
network_scan = Network_scan()
options = network_scan.input()
network_scan.scan(options.ip)
