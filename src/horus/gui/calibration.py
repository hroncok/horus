#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
#                                                                       #
# This file is part of the Horus Project                                #
#                                                                       #
# Copyright (C) 2014 Mundo Reader S.L.                                  #
#                                                                       #
# Date: August 2014                                                     #
# Author: Jesús Arroyo Torrens <jesus.arroyo@bq.com>   	                #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                       #
#-----------------------------------------------------------------------#

__author__ = "Jesús Arroyo Torrens <jesus.arroyo@bq.com>"
__license__ = "GNU General Public License v3 http://www.gnu.org/licenses/gpl.html"

from horus.util import profile

from horus.gui.util.workbenchConnection import *
from horus.gui.util.calibrationPanels import *
from horus.gui.util.calibrationPages import *

class CalibrationWorkbench(WorkbenchConnection):

    def __init__(self, parent):
        WorkbenchConnection.__init__(self, parent)

        #-- Add Calibration Workbench Panels

        self.cameraIntrinsicsPanel = CalibrationWorkbenchPanel(self._panel,
                                                               titleText=_("Camera Intrinsics"),
                                                               parametersType=CameraIntrinsicsParameters,
                                                               buttonStartCallback=self.onCameraIntrinsicsStartCallback,
                                                               description=_("Determines the camera matrix and the distortion coefficients using Zhang2000 algorithm and pinhole camera model."))

        self.laserTriangulationPanel = CalibrationWorkbenchPanel(self._panel,
                                                                 titleText=_("Laser Triangulation"),
                                                                 parametersType=LaserTriangulationParameters,
                                                                 buttonStartCallback=self.onLaserTriangulationStartCallback,
                                                                 description=_("Determines the depth of the intersection camera-laser considering the inclination of the lasers."))

        self.platformExtrinsicsPanel = CalibrationWorkbenchPanel(self._panel,
                                                                 titleText=_("Platform Extrinsics"),
                                                                 parametersType=PlatformExtrinsicsParameters,
                                                                 buttonStartCallback=self.onPlatformExtrinsicsStartCallback,
                                                                 description=_("Determines the transformation matrix between the camera and the platform using a circular interpolation method."))

        self.addToPanel(self.cameraIntrinsicsPanel, 1)
        self.addToPanel(self.laserTriangulationPanel, 1)
        self.addToPanel(self.platformExtrinsicsPanel, 1)

        #-- Add CalibrationPages

        self.laserTriangulationMainPage = LaserTriangulationMainPage(self._panel,
                                                                     buttonCancelCallback=self.onLaserTriangulationCancelCallback,
                                                                     buttonPerformCallback=self.onLaserTriangulationPerformCallback)

        self.laserTriangulationResultPage = LaserTriangulationResultPage(self._panel,
                                                                         buttonRejectCallback=self.onLaserTriangulationRejectCallback,
                                                                         buttonAcceptCallback=self.onLaserTriangulationAcceptCallback)

        self.laserTriangulationMainPage.Hide()
        self.laserTriangulationResultPage.Hide()

        self.addToPanel(self.laserTriangulationMainPage, 1)
        self.addToPanel(self.laserTriangulationResultPage, 1)

        self.Layout()

    def onCameraIntrinsicsStartCallback(self):
        self.cameraIntrinsicsPanel.Hide()
        self.laserTriangulationPanel.Hide()
        self.platformExtrinsicsPanel.Hide()
        self.laserTriangulationMainPage.Show()
        self.Layout()

    def onLaserTriangulationStartCallback(self):
        self.cameraIntrinsicsPanel.Hide()
        self.laserTriangulationPanel.Hide()
        self.platformExtrinsicsPanel.Hide()
        self.laserTriangulationMainPage.Show()
        self.Layout()

    def onPlatformExtrinsicsStartCallback(self):
        self.cameraIntrinsicsPanel.Hide()
        self.laserTriangulationPanel.Hide()
        self.platformExtrinsicsPanel.Hide()
        self.laserTriangulationMainPage.Show()
        self.Layout()

    def onLaserTriangulationCancelCallback(self):
        self.cameraIntrinsicsPanel.Show()
        self.laserTriangulationPanel.Show()
        self.platformExtrinsicsPanel.Show()
        self.laserTriangulationMainPage.Hide()
        self.Layout()

    def onLaserTriangulationPerformCallback(self):
        self.laserTriangulationMainPage.Hide()
        self.laserTriangulationResultPage.Show()
        self.Layout()

    def onLaserTriangulationRejectCallback(self):
        self.laserTriangulationMainPage.Show()
        self.laserTriangulationResultPage.Hide()
        self.Layout()

    def onLaserTriangulationAcceptCallback(self):
        self.cameraIntrinsicsPanel.Show()
        self.laserTriangulationPanel.Show()
        self.platformExtrinsicsPanel.Show()
        self.laserTriangulationResultPage.Hide()
        self.Layout()

    def updateToolbarStatus(self, status):
        if status:
            self.cameraIntrinsicsPanel.buttonStart.Enable()
            self.laserTriangulationPanel.buttonStart.Enable()
            self.platformExtrinsicsPanel.buttonStart.Enable()
        else:
            self.cameraIntrinsicsPanel.buttonStart.Disable()
            #self.laserTriangulationPanel.buttonStart.Disable()
            self.platformExtrinsicsPanel.buttonStart.Disable()

    def updateProfileToAllControls(self):
        self.cameraIntrinsicsPanel.parameters.updateProfileToAllControls()
        self.laserTriangulationPanel.parameters.updateProfileToAllControls()
        self.platformExtrinsicsPanel.parameters.updateProfileToAllControls()