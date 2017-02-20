# -*- coding: utf-8 -*-

import sys
import pygame
import traceback
from . import serialLogNotifier
import queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

from . import predictorBuilder
from .view import *
from .controller import *
from . import resource_manager

import ast


class TheApp:
    pressed = None
    isButtonUp = True

    config = None
    predBuilder = None
    predictor = None
    leftPredictor = None
    rightPredictor = None
    workQueue = None
    notifier = None
    surface = None
    myThread = None

    dispatcher = None

    def __init__(self):
        self.workQueue = queue.Queue(10)
        self.config = resource_manager.ConfigurationReader()
        self.config.loadFromFile("../../resources/att.conf")

    def isPressed(self, key):
        if self.pressed[key] and self.isButtonUp:
            self.isButtonUp = False
            return True
        return False

    def isAnyPressed(self):
        if len(self.pressed) > 0:
            return True
        return False

    def buildScene(self):
        pygame.init()

        windowWidth = None
        windowHeight = None

        if self.config.props["att.display.screen.fullscren"] == "SI":
            info = pygame.display.Info()
            windowWidth = info.current_w
            windowHeight = info.current_h
            self.surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
        elif self.config.props["att.display.screen.fullscren"] == "NO":
            windowWidth = int(self.config.props["att.display.screen.width"])
            windowHeight = int(self.config.props["att.display.screen.height"])
            self.surface = pygame.display.set_mode((windowWidth, windowHeight))

        strSize = self.config.props["att.display.log_notifier.size"]
        tplSize = ast.literal_eval(strSize)
        self.notifier = serialLogNotifier.SerialLogNotifier(self.surface, tplSize)

    def buildHitDataSource(self):

        port = self.config.props["att.hit.datasource.port"]
        baud = self.config.props["att.hit.datasource.baud"]

        serial_port = None
        serial_builder = None

        if self.config.props["att.hit.datasource"] == "FILE":
            serial_builder = ATTHitsFromFilePortBuilder()
        elif self.config.props["att.hit.datasource"] == "DUMMY_RANDOM":
            serial_builder = DummySerialPortBuilder()
        elif self.config.props["att.hit.datasource"] == "SILENT":
            serial_builder = SilentSerialPortBuilder();
        elif self.config.props["att.hit.datasource"] == "RANDOM_SET":
            serial_builder = ATTEmulatedSerialPortBuilder()
        elif self.config.props["att.hit.datasource"] == "SERIAL":
            serial_builder = ATTArduinoSerialPortBuilder()

        if serial_builder != None:
            serial_port = serial_builder.build_serial_port(port, baud)

        if self.config.props["att.hit.reader_thread"] == "DEFAULT_SERIAL_READER":
            self.myThread = ThreadedSerialReader(1, "Thread-1", self.workQueue, None, serial_builder, port, baud,
                                                 serial_port, True)

        if self.myThread != None:
            self.myThread.start()

    def main(self):

        self.predictor = TableHitPredictor()

        self.buildHitDataSource()
        self.buildScene()

        self.dispatcher = ATTDispatcher(self)
        self.dispatcher.init()

        # self.dispatcher.setCurrentController(LogonController.ID)
        self.dispatcher.setCurrentController(MenuController.ID)

        try:
            done = False
            clock = pygame.time.Clock()

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        break

                self.pressed = pygame.key.get_pressed()
                if not (self.pressed[pygame.K_UP]) and not (self.pressed[pygame.K_DOWN]) and not (
                self.pressed[pygame.K_RETURN]) and not (self.pressed[pygame.K_ESCAPE]):
                    self.isButtonUp = True

                done = self.dispatcher.process(self, event)

                clock.tick(60)

        except Exception:
            print(Exception)
            traceback.print_exc(file=sys.stdout)

        finally:
            print("Thread STOP")
            self.myThread.stop()
            print("Thread STOPPED")
            pygame.quit()
            print("Pygame quit")
            try:
                sys.exit()
                print("SYS exit")
            except Exception:
                print(Exception)
                traceback.print_exc(file=sys.stdout)


class ATTDispatcher:
    app = None

    currentController = None
    controllers = None

    def __init__(self, app):
        self.app = app
        self.controllers = {}

    def init(self):
        self.buildControllers()

    def buildControllers(self):
        view = LogonView(self.app.surface)
        controller = LogonController(view)
        self.appendController(controller)

        view = MenuView(self.app.surface)
        controller = MenuController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

        view = ShortServiceView(self.app.surface)
        controller = ShortServiceController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

        view = MultiBallView(self.app.surface)
        controller = MultiBallController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

        view = RallyView(self.app.surface)
        controller = RallyController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

        view = SandboxView(self.app.surface)
        controller = SandboxController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

        view = CalibrationView(self.app.surface)
        controller = CalibrationController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
        self.appendController(controller)

    def appendController(self, controller):
        self.controllers[controller.ID] = controller

    def getCurrentController(self, controller_id):
        return self.controllers[controller_id]

    def setCurrentController(self, controller_id):
        self.currentController = self.getCurrentController(controller_id)
        self.currentController.start()

    def process(self, app, event):
        return self.currentController.process(app, event)


class TableHitPredictor(object):
    leftPredictor = None
    rightPredictor = None

    def __init__(self):

        predBuilder = predictorBuilder.PredictorBuilder()
        self.leftPredictor = predBuilder.buildInstance("../../data/train_points_20160303_left.txt")
        self.rightPredictor = predBuilder.buildInstance("../../data/train_points_20160303_right.txt")

    def predictHit(self, hit):
        side = hit["side"]
        if side == 'l':
            return self.leftPredictor.predictHit(hit)
        else:
            return self.rightPredictor.predictHit(hit)


if __name__ == '__main__':
    theApp = TheApp()
    theApp.main()
