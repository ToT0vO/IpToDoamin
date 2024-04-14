import sys
import socket
import dns.resolver
import dns.reversename

def reverse_dns_lookup(ip):
    results = {}
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        results['socket'] = hostname
    except socket.herror as e:
        results['socket'] = f"Socket method failed: {e}"

    try:
        addr = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(addr, "PTR")
        if answers:
            result = str(answers[0].target)
            if result.endswith('.'):
                result = result[:-1]  # 移除末尾的点号
            results['dnspython'] = result
    except Exception as e:
        results['dnspython'] = f"DNSPython method failed: {e}"

    return results

def process_ip_addresses(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            ip = line.strip()
            if ip:
                results = reverse_dns_lookup(ip)
                socket_result = results.get('socket', 'No result')
                dnspython_result = results.get('dnspython', 'No result')
                # 写入结果
                if socket_result == dnspython_result:
                    outfile.write(f"{socket_result}\n")
                else:
                    if socket_result != 'No result':
                        outfile.write(f"{socket_result}\n")
                    if dnspython_result != 'No result':
                        outfile.write(f"{dnspython_result}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_filename> <output_filename>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    process_ip_addresses(input_filename, output_filename)

if __name__ == "__main__":
    main()
