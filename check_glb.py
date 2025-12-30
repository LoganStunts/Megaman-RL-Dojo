import json
import struct

def check_glb_scale(file_path):
    with open(file_path, 'rb') as f:
        # GLB Header
        magic = f.read(4)
        if magic != b'glTF':
            print("Not a valid GLB file")
            return
        
        version = struct.unpack('<I', f.read(4))[0]
        length = struct.unpack('<I', f.read(4))[0]
        
        # First Chunk (JSON)
        chunk_length = struct.unpack('<I', f.read(4))[0]
        chunk_type = f.read(4)
        
        if chunk_type != b'JSON':
            print("First chunk is not JSON")
            return
        
        json_data = json.loads(f.read(chunk_length).decode('utf-8'))
        
        # Look for nodes with scale
        print(f"File: {file_path}")
        found_scale = False
        for i, node in enumerate(json_data.get('nodes', [])):
            if 'scale' in node:
                print(f"Node {i} ('{node.get('name', 'unnamed')}') has scale: {node['scale']}")
                found_scale = True
        
        if not found_scale:
            print("No explicit scale found in nodes (defaulting to 1.0, 1.0, 1.0)")

print("Checking scale of the GLB in the Clean Repo...")
check_glb_scale(r"C:\Users\logan\Documents\Megaman_Clean_Repo\Tinpet_Male_New.glb")
