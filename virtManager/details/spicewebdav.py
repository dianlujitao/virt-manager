# Copyright (C) 2019-2020 Jitao Lu <dianlujitao@gmail.com>
#
# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

from ..baseclass import vmmGObjectUI


class vmmSpiceWebdav(vmmGObjectUI):
    SHARE_FOLDER = "share-folder"
    SHARE_FOLDER_RO = "share-folder-ro"
    SHARED_FOLDER = "shared-folder"

    __gsignals__ = {
        SHARE_FOLDER: (vmmGObjectUI.RUN_FIRST, None, [bool]),
        SHARE_FOLDER_RO: (vmmGObjectUI.RUN_FIRST, None, [bool]),
        SHARED_FOLDER: (vmmGObjectUI.RUN_FIRST, None, [str]),
    }

    def __init__(self, enabled, ro, folder):
        vmmGObjectUI.__init__(self, "spicewebdav.ui",
                              "vmm-spice-webdav-folder-share")
        self._cleanup_on_app_close()
        self.bind_escape_key_close()

        self.builder.connect_signals({
            "on_vmm_spice_webdav_folder_share_delete_event":
            self.close,
            "on_vmm_spice_webdav_folder_share_close_clicked":
            self.close,
        })

        share_folder_cb = self.widget("share-folder-cb")
        share_folder_cb.set_active(enabled)
        share_folder_cb.connect(
            "toggled", lambda src: self.emit(self.__class__.SHARE_FOLDER,
                                             src.get_active()))

        share_folder_ro_cb = self.widget("share-folder-ro-cb")
        share_folder_ro_cb.set_active(ro)
        share_folder_ro_cb.connect(
            "toggled", lambda src: self.emit(self.__class__.SHARE_FOLDER_RO,
                                             src.get_active()))

        shared_folder_fc = self.widget("shared-folder-fc")
        shared_folder_fc.set_current_folder(folder)
        shared_folder_fc.connect(
            "file-set", lambda src: self.emit(self.__class__.SHARED_FOLDER,
                                              src.get_filename()))

    def show(self, parent):
        self.topwin.set_transient_for(parent)
        self.topwin.present()

    def _cleanup(self):
        pass

    def close(self, ignore1=None, ignore2=None):
        self.topwin.hide()
        return 1
