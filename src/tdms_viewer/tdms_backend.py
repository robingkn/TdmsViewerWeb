from nptdms import TdmsFile

def load_tdms(file):
    return TdmsFile.read(file)

def get_tdms_nodes(tdms):
    file_node = "📄 File"
    group_nodes = [f"📁 {group.name}" for group in tdms.groups()]
    channel_nodes = [f"📊 {group.name}/{channel.name}" for group in tdms.groups() for channel in group.channels()]
    return [file_node] + group_nodes + channel_nodes

def get_properties(tdms, node_type, *, group=None, channel=None):
    if node_type == "file":
        return tdms.properties
    elif node_type == "group":
        return tdms[group].properties
    elif node_type == "channel":
        ch = tdms[group][channel]
        return {
            "Group": ch.group_name,
            "Name": ch.name,
            "Unit": ch.properties.get("unit_string", "N/A"),
            "Length": len(ch),
            **ch.properties
        }
    return {}