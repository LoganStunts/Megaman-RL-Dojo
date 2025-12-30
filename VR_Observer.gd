extends XROrigin3D

func _ready():
	var interface = XRServer.find_interface("OpenXR")
	if interface and interface.is_initialized():
		print("VR Interface initialized")
		get_viewport().use_xr = true
	else:
		print("VR Interface not found")
