from bcsfe.core import io


class DeviceIDNotSet(Exception):
    pass


class AdbHandler(io.root_handler.RootHandler):
    def __init__(self, adb_path: io.path.Path):
        self.adb_path = adb_path
        self.start_server()
        self.root()
        self.device_id = None
        self.cc = None

    def start_server(self):
        self.adb_path.run("start-server")

    def kill_server(self):
        self.adb_path.run("kill-server")

    def root(self):
        self.adb_path.run("root")

    def get_connected_devices(self) -> list[str]:
        devices = self.adb_path.run("devices").result.split("\n")
        devices = [device.split("\t")[0] for device in devices[1:-2]]
        return devices

    def set_device(self, device_id: str):
        self.device_id = device_id

    def get_device(self) -> str:
        if self.device_id is None:
            raise DeviceIDNotSet("Device ID is not set")
        return self.device_id

    def get_device_name(self) -> str:
        return self.adb_path.run(
            f"-s {self.get_device()} shell getprop ro.product.model"
        ).result.strip()

    def pull_file(self, device_path: io.path.Path, local_path: io.path.Path):
        self.adb_path.run(
            f"-s {self.get_device()} pull {device_path} {local_path}"
        ).result

    def push_file(self, local_path: io.path.Path, device_path: io.path.Path):
        self.adb_path.run(f"-s {self.get_device()} push {local_path} {device_path}")

    def get_packages(self) -> list[str]:
        return self.adb_path.run(
            f"-s {self.get_device()} shell pm list packages"
        ).result.split("\n")

    def get_package_name(self, package: str) -> str:
        return package.split(":")[1]

    def get_battlecats_packages(self) -> list[str]:
        packages = self.get_packages()
        return [
            self.get_package_name(package)
            for package in packages
            if "jp.co.ponos.battlecats" in package
        ]

    def save_battlecats_save(self, local_path: io.path.Path):
        self.pull_file(self.get_battlecats_save_path(), local_path)

    def load_battlecats_save(self, local_path: io.path.Path):
        self.push_file(local_path, self.get_battlecats_save_path())

    def close_game(self):
        self.adb_path.run(
            f"-s {self.get_device()} shell am force-stop {self.get_battlecats_package_name()}"
        )

    def run_game(self):
        self.adb_path.run(
            f"-s {self.get_device()} shell monkey -p {self.get_battlecats_package_name()} -c android.intent.category.LAUNCHER 1"
        )
