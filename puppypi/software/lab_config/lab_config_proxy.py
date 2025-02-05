import roslibpy
import threading

class LabConfigProxy:
    def __init__(self, host, port):
        self.client = roslibpy.Ros(host=host, port=port)
        self.client.run()
        self.heartbeat_timer = threading.Timer(2, self.heartbeat)

    def __del__(self):
        self.exit_func()

    def heartbeat(self):
        srv = roslibpy.Service(self.client, '/lab_config_manager/heartbeat', 'std_srvs/SetBool')
        rq = roslibpy.ServiceRequest()
        rq['data'] = True
        srv.call(rq)
        self.heartbeat_timer = threading.Timer(2, self.heartbeat)
        self.heartbeat_timer.start()

    def enter_func(self):
        srv = roslibpy.Service(self.client, '/lab_config_manager/enter', 'std_srvs/Trigger')
        req = roslibpy.ServiceRequest()
        self.heartbeat()
        return srv.call(req)

    def exit_func(self):
        srv = roslibpy.Service(self.client, '/lab_config_manager/exit', 'std_srvs/Trigger')
        req = roslibpy.ServiceRequest()
        self.heartbeat_timer.cancel()
        return srv.call(req)

    def get_all_color_name(self):
        srv = roslibpy.Service(self.client, '/lab_config_manager/get_all_color_name', 'std_srv/Trigger')
        req = roslibpy.ServiceRequest()
        rsl = srv.call(req)
        return rsl['color_names']

    def get_range_by_name(self, name):
        srv = roslibpy.Service(self.client, '/lab_config_manager/get_range', 'lab_config/GetRange')
        req = roslibpy.ServiceRequest()
        req.data = {"color_name": name}
        return srv.call(req)

    def set_current_range(self, range_min, range_max):
        srv = roslibpy.Service(self.client, '/lab_config_manager/change_range', 'lab_config/ChangeRange')
        req = roslibpy.ServiceRequest()
        req.data = dict(min=range_min, max=range_max)
        return srv.call(req)

    def apply_current_range(self, name):
        srv = roslibpy.Service(self.client, '/lab_config_manager/stash_range', 'lab_config/StashRange')
        req = roslibpy.ServiceRequest()
        req.data = dict(color_name=name)
        return srv.call(req)

    def save_ranges_to_disk(self):
        srv = roslibpy.Service(self.client, 'lab_config_manager/save_to_disk', 'std_srvs/Trigger')
        req = roslibpy.ServiceRequest()
        return srv.call(req)
