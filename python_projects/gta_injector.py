from pymem import *
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(current_dir, 'dump.dll')
dll_path_bytes = bytes(dll_path, "UTF-8")
process_name = 'gta_sa.exe'

open_process = Pymem(process_name)
process.inject_dll(open_process.process_handle, dll_path_bytes)

print('DLL injected successfulled')
