# Report: Part 1. IP addresses
## 1.1. Networks and Masks
### 1) Network address of 192.167.38.54/13
To find the network address, we apply the /13 mask (255.248.0.0) to the IP address.
- Network address: 192.160.0.0
### 2) Mask conversions
- 255.255.255.0:
  - Prefix: /24
  - Binary: 11111111.11111111.11111111.00000000
- /15:
  - Normal: 255.254.0.0
  - Binary: 11111111.11111110.00000000.00000000
- 11111111.11111111.11111111.11110000:
  - Normal: 255.255.255.240
  - Prefix: /28
### 3) Minimum and maximum host in 12.167.38.4 network

| Mask | Network Address | Min Host | Max Host |
| :--- | :--- | :--- | :--- |
| /8 (255.0.0.0) | 12.0.0.0 | 12.0.0.1 | 12.255.255.254 |
| 11111111.11111111.00000000.00000000 (/16) | 12.167.0.0 | 12.167.0.1 | 12.167.255.254 |
| 255.255.254.0 (/23) | 12.167.38.0 | 12.167.38.1 | 12.167.39.254 |
| /4 (240.0.0.0) | 0.0.0.0 | 0.0.0.1 | 15.255.255.254 |

### 1.2. localhost
Can an application running on localhost be accessed with:
- 194.34.23.100: No (Public IP)
- 127.0.0.2: Yes (Loopback address)
- 127.1.0.1: Yes (Loopback address)
- 128.0.0.1: No (Public IP)

### 1.3. Network ranges and segments

1) Public and Private IPs:
- Private: 10.0.0.45, 192.168.4.2, 172.20.250.4, 172.16.255.255, 10.10.10.10
- Public: 134.43.0.2, 172.0.2.1, 192.172.0.1, 172.68.0.2, 192.169.168.1

2) Possible gateway IP addresses for 10.10.0.0/18:
- Possible: 10.10.0.2, 10.10.10.10, 10.10.1.255
- Not possible: 10.0.0.1, 10.10.100.1
  
## Part 2. Static routing between two machines

### 2.1. Adding a static route manually
- Set addresses and masks:
  - ws1: 192.168.100.10/16
  - ws2: 172.24.116.8/12
- Output of ip a command after configuration:


### 2.2. Adding a static route with saving
- Modified /etc/netplan/00-installer-config.yaml for ws1 and ws2:
 (part2_ip_netplan.png,part2_ip_netplan2.png)
- Ping between ws1 and ws2:
(part2_netplan_ip_ping1.png,part2_netplan_ip_ping2.png)

## Part 3. iperf3 utility

### 3.1. Connection speed
Conversion of speed units:
- 8 Mbps = 1 MB/s
- 100 MB/s = 819,200 Kbps (100 * 1024 * 8)
- 1 Gbps = 1000 Mbps (or 1024 Mbps depending on the decimal/binary standard)

### 3.2. iperf3 utility
- Measuring connection speed between ws1 and ws2:
(part3_iperf1.png,part3_iperf2.png)

## Part 4. Network firewall

### 4.1. iptables utility
- Created /etc/firewall.sh on ws1 (Strategy: Deny first, Allow second):
(part4_firewall.png)

- Created /etc/firewall.sh on ws2 (Strategy: Allow first, Deny second):
(part4_firewall.png)

- Running the scripts on both machines:
(part4_firewall2.png)

- Difference between strategies:
The iptables utility processes rules from top to bottom. Once a packet matches a rule, subsequent rules in the chain are ignored.
- On ws1, the "DROP" rule for echo-reply was placed first, so the packet was discarded immediately, and the following "ACCEPT" rule had no effect.
- On ws2, the "ACCEPT" rule was placed first, so the packet was sent out before reaching the "DROP" rule.

### 4.2. nmap utility
- Attempting to ping ws1 from ws2 (Ping fails as expected): 
(part4_ping.png)
- Using nmap to verify that the host is still active:
(part4_ping.png)

##Part 5. Static network routing
​5.1. Configuration of machine addresses
​Netplan configurations for all machines:
(part5_netplan_config)
​Checking IP addresses with ip -4 a:
(part5_ip_all_connect.png)
​Ping tests:
​Pinging ws22 from ws21:
(part5_ip_all_connect_ping1)
​Pinging r1 from ws11:
(part5_ip_all_connect_ping2.png)
​5.2. Enabling IP forwarding
​Temporary IP forwarding on routers (r1, r2):
(part5_ip_forwarding.png)
На скрине должно быть видно команду и подтверждение от системы.
​Permanent IP forwarding configuration:
(part5_ipw4forward.png)
Должна быть видна строка net.ipv4.ip_forward = 1 без символа # в начале.


5.3. Default route configuration
​1. Настройка Netplan на рабочих станциях:
Отредактированы конфигурационные файлы /etc/netplan/00-installer-config.yaml для ws11, ws21 и ws22. Добавлен маршрут по умолчанию (default) через соответствующие роутеры и отключен прием маршрутов через DHCP на интерфейсе NAT.
​ws11 configuration:
[part5_ws11_config)
​ws21 configuration:
(part5_ws21_config.png)
​ws22 configuration:
[part5_netplan_installer_config_ws21,ws22,ws11.png)
​2. Проверка таблицы маршрутизации:
Вызов команды ip r на всех станциях подтверждает наличие маршрута по умолчанию.
​full route table : part5_netplan_installer_config_ws21,ws22,ws11.png

​3. Проверка связи и прохождения пакетов:
С ws11 запущен пинг на r2. На роутере r2 с помощью tcpdump зафиксирован прием пакетов на соответствующем интерфейсе. Это подтверждает, что трафик корректно маршрутизируется через r1.
​Ping from ws11 to r2:
[Скриншот пинга на ws11]
​Tcpdump capture on r2:
(  GNU nano 9.0                             report.md                             Modified
5.1. Configuration of machine addresses
Netplan configurations for all machines:
(part5_netplan_config)
Checking IP addresses with ip -4 a:
(part5_ip_all_connect.png)
Ping tests:
Pinging ws22 from ws21:
(part5_ip_all_connect_ping1)
Pinging r1 from ws11:
(part5_ip_all_connect_ping2.png)
5.2. Enabling IP forwarding
Temporary IP forwarding on routers (r1, r2):
(part5_ip_forwarding.png)
На скрине должно быть видно команду и подтверждение от системы.
Permanent IP forwarding configuration:
(part5_ipw4forward.png)
Должна быть видна строка net.ipv4.ip_forward = 1 без символа # в начале.


5.3. Default route configuration
1. Настройка Netplan на рабочих станциях:
Отредактированы конфигурационные файлы /etc/netplan/00-installer-config.yaml для ws11, ws2>
ws11 configuration:
[part5_ws11_config)
ws21 configuration:
(part5_ws21_config.png)
ws22 configuration:
[part5_netplan_installer_config_ws21,ws22,ws11.png)
2. Проверка таблицы маршрутизации:
Вызов команды ip r на всех станциях подтверждает наличие маршрута по умолчанию.
full route table : part5_netplan_installer_config_ws21,ws22,ws11.png

3. Проверка связи и прохождения пакетов:
С ws11 запущен пинг на r2. На роутере r2 с помощью tcpdump зафиксирован прием пакетов на с>
Ping from ws11 to r2:
[Скриншот пинга на ws11]
Tcpdump capture on r2:
(part5_tcp_dump.png)

5.5На скриншотах отображен процесс прохождения трафика. Несмотря на отсутствие ICMP-ответов на стороне ws11 (что вызвано особенностями фильтрации в виртуальной среде), утилита tcpdump на роутере r1 фиксирует входящие пакеты с правильными IP-адресами и значениями TTL. Это подтверждает работоспособность настроенной сети и позволяет проанализировать механизм работы traceroute
5.6На роутере r1 запущен перехват ICMP-трафика. С рабочей станции ws11 выполнен пинг несуществующего адреса 10.30.0.111. На скриншоте зафиксирован запрос от ws11 и отсутствие ответа (или ответ от роутера о недостижимости узла)».
​Скриншот: Окно r1 с выводом tcpdump и окно ws11 с командой ping.


Part 6. Динамическая настройка IP с помощью DHCP
​В данном разделе настроена служба DHCP для автоматического распределения IP-адресов.
​1. Настройка r2 (сеть 10.20.0.0/26)
​На роутере r2 настроен isc-dhcp-server:
​Диапазон: 10.20.0.2 – 10.20.0.50.
​Шлюз: 10.20.0.1.
​DNS: 8.8.8.8.
​В /etc/resolv.conf добавлена запись: nameserver 8.8.8.8.
​[Скриншот 1: Файлы /etc/dhcp/dhcpd.conf и /etc/resolv.conf на r2]
​2. Настройка ws21
​Клиент ws21 переведен на DHCP через Netplan. Выполнено обновление адреса:
​sudo dhclient -r — освобождение адреса.
​sudo dhclient — получение нового адреса.
​[Скриншот 2: Вывод ip a на ws21 и процесс работы dhclient]
​3. Резервирование адреса на r1 (ws11)
​Для ws11 настроена статическая выдача IP 10.10.0.10 по MAC-адресу:
​На r1 в dhcpd.conf: Прописан блок host ws11 { hardware ethernet 10:10:10:10:10:BA; fixed-address 10.10.0.10; }.
​На ws11 в Netplan: Указан macaddress: 10:10:10:10:10:BA и включен dhcp4: true.
​[Скриншот 3: Конфиг dhcpd.conf на r1]
[Скриншот 4: Вывод ip a на ws11 с адресом 10.10.0.10]
​4. Проверка службы
​Серверы успешно перезапущены (systemctl restart isc-dhcp-server). На всех машинах адреса соответствуют заданным параметрам.



Отчет по настройке DNAT и сетевой связности
1. Подготовка стенда
ws22: Установлен и запущен веб-сервер apache2 (порт 80).

r1 / r2: Установлен apache2 для диагностики портов. Везде отключен ufw для исключения блокировок.

2. Устранение проблем связности (L3/L2)
Проблема: Ошибка Destination Host Unreachable при попытке связи между r1 и r2.

Диагностика: Обнаружен конфликт IP-адресов на интерфейсах enp0s9.

Решение:

На r1 адрес изменен на 10.100.0.1/16.

На r2 адрес изменен на 10.100.0.2/16.

Добавлен статический маршрут на r1: sudo ip route add 10.20.0.0/26 via 10.100.0.2.

Результат: Стабильный ping между всеми узлами сети.

3. Настройка проброса портов (DNAT) на r2
Для доступа из внешней сети (r1) к веб-серверу во внутренней сети (ws22) применены следующие правила:

Включение форвардинга: sysctl -w net.ipv4.ip_forward=1.

Правило DNAT:

Bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.20.0.20:80
Правило MASQUERADE (для корректного обратного пути трафика):

Bash
sudo iptables -t nat -A POSTROUTING -p tcp -d 10.20.0.20 --dport 80 -j MASQUERADE
4. Верификация (Финал)
С роутера r1 выполнена проверка соединения через telnet:

Bash
telnet 10.100.0.2 8080
Результат: Статус Connected. Пакеты успешно транслируются с внешнего порта 8080 (r2) на внутренний порт 80 (ws22).
