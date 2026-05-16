from pyModbusTCP.client import ModbusClient
import time
import struct

c = ModbusClient(host="localhost", port=502, unit_id=1, auto_open=True)

def decode_float(reg_low, reg_high):
    # junta dois registros de 16 bits em um float de 32 bits
    packed_data = struct.pack('<HH', reg_low, reg_high)
    return struct.unpack('<f', packed_data)[0]

status_anterior = None

try:
    while True:
        if c.is_open:
                registro = c.read_input_registers(0, 4)
                if registro:
                    status_atual = {
                            "valvula produto": bool(registro[0] & (1 << 0)),
                            "valvula acida": bool(registro[0] & (1 << 1)),
                            "valvula alcalina":  bool(registro[0] & (1 << 2)),
                            "valvula descarte":  bool(registro[0] & (1 << 3)),
                            "atuador mistura":  bool(registro[0] & (1 << 4)),
                            "nivel maximo":  bool(registro[0] & (1 << 5)),
                            "nivel minimo":  bool(registro[0] & (1 << 6)),
                            "estado ph": registro[1],
                            "valor ph": round(decode_float(registro[2], registro[3]),2)} # estado 1 = neutro, 2 = basico, 3 = acido
                    
                    if status_anterior != status_atual:
                        print("-"*30)
                        for chave, valor in status_atual.items():
                            print(f"{chave}: {valor}")
                        status_anterior = status_atual
                
        else:
            print("Tentando conectar...")
            c.open()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Scanner parado.")
