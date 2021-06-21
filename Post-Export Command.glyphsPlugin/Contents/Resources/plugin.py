# Guten Tag
# =========
#
# Copyright 2021 Florian Pircher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import subprocess
import objc
from GlyphsApp import (Glyphs, DOCUMENTEXPORTED)
from GlyphsApp.plugins import GeneralPlugin


customParameterKey = "Post-Export Command"


class PostExportCommand(GeneralPlugin):
    @objc.python_method
    def start(self):
        Glyphs.addCallback(self.exportCallback, DOCUMENTEXPORTED)

    @objc.python_method
    def exportCallback(self, info):
        try:
            note = info.object()
            instance = note["instance"]
            fontFilePath = note["fontFilePath"]
            font = instance.font
            fontURL = font.parent.fileURL()
            fontDirectory = None

            if fontURL:
                fontDirectory = os.path.dirname(fontURL.path())

            command = None

            if instance.customParameters[customParameterKey]:
                command = instance.customParameters[customParameterKey]
            elif font.customParameters[customParameterKey]:
                command = font.customParameters[customParameterKey]

            print(command)

            if command:
                result = subprocess.run(
                    [command, fontFilePath],
                    cwd=fontDirectory,
                    capture_output=True)

                if result.returncode != 0:
                    print(
                        f"Error running plugin “Post-Export Command” for exported file {fontFilePath} for instance {instance.name}. Command terminated with return code {result.returncode}:")
                    print(result.stdout)
        except:
            import traceback
            print(traceback.format_exc())

    @objc.python_method
    def __del__(self):
        Glyphs.removeCallback(self.exportCallback)

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
