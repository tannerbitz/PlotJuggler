from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeDeps, CMakeToolchain, CMake
from conan.tools.files import copy
from conan.errors import ConanInvalidConfiguration
import os

class PlotJugglerConan(ConanFile):
    name = "plotjuggler"
    description = "PlotJuggler is a tool to visualize time series that is fast, powerful and intuitive."
    license = "Mozilla Public License 2.0"
    author = "Davide Faconti"
    topics = ("Time-serieis visualization")
    homepage = "https://plotjuggler.io/"
    url = "https://github.com/facontidavide/PlotJuggler"
    package_type = "application"
    settings = "os", "compiler", "build_type", "arch"

    default_options = {
        "zeromq/*:shared": False,
        "qt/*:qtsvg": True,
        "qt/*:qtx11extras": True,
        "qt/*:qtwebsockets": True,
    }
    
    def requirements(self):
        self.requires("protobuf/3.21.12")
        self.requires("mosquitto/2.0.18")
        self.requires("zeromq/4.3.5")
        self.requires("zlib/1.2.13")
        self.requires("lua/5.4.6") # 3rd part asked for 5.4.7, but version mismatch with sol2/3.5.0
        self.requires("fast-cdr/2.2.5") # 3rd party asked for 2.2.6
        self.requires("backward-cpp/1.6")
        self.requires("nlohmann_json/3.12.0") # 3rd party ask for 3.11.3
        self.requires("sol2/3.5.0") # 3rd party asked for 3.3.0
        self.requires("zstd/1.5.7", override=True) # resolve issue with libmysqlclient (dep of qt5) requiring zstd/1.5.5

        # maybe we skip this since it is source included?
        self.requires("qt/5.15.16")
        self.requires("qwt/6.2.0") # 3rd party may have had 6.1?
        # other requirements that are source included are:
        # - QCodeEditor
        # - color_widgets
        # - Qt-Advanced-Docking

        # other dependencies without publically available conanfile
        # data_tamer https://github.com/PickNikRobotics/data_tamer.  there is a conanfile.py, but it appears out of data (from the version at least)

    def validate(self):
        if self.dependencies["zeromq"].options.shared:
            raise ConanInvalidConfiguration("plotjuggler requires zeromq to be compiled static")
        if not self.dependencies["qt"].options.qtsvg:
            raise ConanInvalidConfiguration("plotjuggler requires qt to be built with qtsvg")
        if not self.dependencies["qt"].options.qtwebsockets:
            raise ConanInvalidConfiguration("plotjuggler requires qt to be built with qtwebsockets")
        # TODO: does this need to be linux only?
        if not self.dependencies["qt"].options.qtx11extras:
            raise ConanInvalidConfiguration("plotjuggler requires qt to be built with qtx11extras")

    def source(self):
        pass

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE.md", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()

        # TODO: REMOVE cmake config files

    def package_info(self):
        pass

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()

    def layout(self):
        cmake_layout(self)

