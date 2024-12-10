def ip_fragmentation_calculator(total_length, mtu, identification, header_size=20, df_flag=0):
    
    data_size = total_length - header_size
    fragment_size = mtu - header_size  

    fragment_size = (fragment_size // 8) * 8

    fragments = []

    if df_flag == 1 and data_size > fragment_size:
        return "Fragmentation not allowed (DF=1), packet too large."

    if data_size <= fragment_size:
        return [{
            'Fragment Number': 1,
            'Identification': identification,
            'Fragment Length': total_length,
            'More Fragments (MF)': 0,
            'Fragment Offset': 0,
            'DF Flag': df_flag
        }]

    num_fragments = (data_size + fragment_size - 1) // fragment_size

    for i in range(num_fragments):
        offset = i * (fragment_size // 8)  

        if i == num_fragments - 1:  
            frag_data_size = data_size - i * fragment_size
            frag_length = frag_data_size + header_size
            mf = 0  
        else:
            frag_data_size = fragment_size
            frag_length = frag_data_size + header_size
            mf = 1  

        fragments.append({
            'Fragment Number': i + 1,
            'Identification': identification,
            'Fragment Length': frag_length,
            'More Fragments (MF)': mf,
            'Fragment Offset': offset,
            'DF Flag': df_flag
        })

    return fragments


# Example Usage
total_length = 1000  
mtu = 200  
identification = 54321  
df_flag = 0  

fragments = ip_fragmentation_calculator(total_length, mtu, identification, df_flag=df_flag)

for frag in fragments:
    print(f"Fragment {frag['Fragment Number']}: Length={frag['Fragment Length']}, "
          f"MF={frag['More Fragments (MF)']}, Offset={frag['Fragment Offset']} bytes, "
          f"ID={frag['Identification']}, DF={frag['DF Flag']}")
