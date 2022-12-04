'''
These files can be used only with permission from the author Gad Halevy.
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock


# from gpiozero import LED,OutputDevice,Button

class Door(Widget):
    '''
    Elevator door
    '''
    pass


class Bar(Widget):
    '''
    Elevator bar
    '''
    pass


class Limit(Widget):
    '''
    Floor limit switches.
    '''
    pass


class Ta(Widget):
    '''
    Elevator car
    '''
    pass


class ElLimit(Widget):
    '''
    Door limit switch.
    '''
    pass


class DoorBar(Widget):
    '''
    Door limit for door open, door close.
    '''
    pass


class Logi(Widget):
    '''
    Simulation of elevator.
    '''
    # 3 floor buttons
    first = ObjectProperty
    second = ObjectProperty
    third = ObjectProperty
    # Elevator bar collide with floor limit switch.
    bar = ObjectProperty
    # car of elevator.
    body = ObjectProperty
    # elevator door.
    delet = ObjectProperty
    # 3 indicator lights shows in which floor the car is located.
    noora1 = ObjectProperty
    noora2 = ObjectProperty
    noora3 = ObjectProperty
    # lighted arrow shows whether car is moving up or down.
    direction = ObjectProperty
    # 3 limit switches for each floor
    lSwitch1 = ObjectProperty
    lSwitch2 = ObjectProperty
    lSwitch3 = ObjectProperty
    # spinner choosing logy physi or service mode
    status = ObjectProperty
    # door bar collides with door open and door close limit switches
    doorBar = ObjectProperty
    # 3 physical buttons of elevator to be used in Phisi class
    # don't have any role here, are used because of inheriting.
    elFirst = ObjectProperty
    elSecond = ObjectProperty
    elThird = ObjectProperty
    # dooropen limit switch
    doorOpen = ObjectProperty
    # door close limit switch
    doorClose = ObjectProperty

    def __init__(self, **kwargs):
        '''
        Constructor overrides default constructor
        :param kwargs:
        '''
        super(Logi, self).__init__(**kwargs)
        self.state = 'begin'
        #####################
        # Dictionary that works only on linux raspberrypi is
        # a linux machine.
        self.colides = {'dOpen': (self.doorBar, self.doorOpen),
                        'dClose': (self.doorBar, self.doorClose),
                        'ls1': (self.bar, self.lSwitch1),
                        'ls2': (self.bar, self.lSwitch2),
                        'ls3': (self.bar, self.lSwitch3),
                        }
        #############################

    def closeDoor(self, dt):
        '''
        Close elevator door.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        self.delet.size[0] += 1
        self.doorBar.pos[0] = self.delet.size[0] - self.doorBar.size[0] / 2 + self.delet.pos[0] - 10

    def openDoor(self, dt):
        '''
        Open elevator door.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        # todo complete 2 lines of code


    def doorStop(self, dt):
        '''
        Stops door of real elevator exists because inheritance.
        :param dt:
        :return:
        '''
        pass

    def moveFirst(self):
        '''
        Called by first floor button
        :return:
        '''
        if self.checkColide(self.doorOpen, self.doorBar):
            Clock.schedule_interval(self.koma1, 1.0 / 45.0)

    def moveSecond(self):
        '''
        Called by second floor button is_pressed.
        :return:
        '''
        # todo complete 2 lines of code

    def moveThird(self):
        '''
        Called by third floor button
        :return:
        '''
        # todo complete 2 lines of code

    def moveUp(self):
        '''
        Fires when elevator car moves up
        :return:
        '''
        self.direction.color = 1, 1, 1, 1
        self.direction.source = 'up.png'
        self.body.pos[1] += 1

    def moveDown(self):
        '''
        Fires when elevator car moves down
        :return:
        '''
        # todo complete 3 lines of code

    def moveEnd(self):
        '''
        Exists because inheritance.
        :return:
        '''
        pass

    def selector(self, dt):
        '''
        Exists beacause inheritance.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        pass

    def changeOptions(self):
        '''
        Controls the spinner by which user select
        operation mode.
        :return:
        '''
        if self.status.text == 'Service':
            self.clear_widgets()
            self.add_widget(Service())
        elif self.status.text == 'Phisi':
            self.clear_widgets()
            self.add_widget(Phisi())

    def ipusNoorot(self):
        '''
        Turn indicator lights off.
        set sources to first.png,second.png,third.png
        :return:
        '''
        # todo complete 3 lines of code

    def ipusDirection(self):
        '''
        Turns direction arrow off.
        set source to '', and mask thecolor (0, 0, 0, 1)
        :return:
        '''
        # todo complete 2 lines of code

    def checkColide(self, obj1, obj2):
        '''
        Check if bars (door and elevator) collides with
        some limit switch.
        use obj1.collide_widget(obj2)
        :param obj1: bar.
        :param obj2: limit switch.
        :return: true if colides, false if not.
        '''
        # todo 1 line of code

    def lightOn(self, obj, src):
        '''
        Turn on indictor lights.
        :param obj: some indicator light.
        :param src: image path of lighted number.
        :return:
        '''
        # todo 1 line of code

    def koma3(self, dt):
        '''
        Controls what happens after third floor button was pressed.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        # initialize state machine
        if self.state == 'begin':
            ######################
            # in linux this line should be:
            # if self.checkColide(*self.colides['dOpen']) and \
            #         (self.checkColide(*self.colides['ls1']) or \
            #          self.checkColide(*self.colides['ls2'])):
            ####################
            # if door open and the car in first floor or car second floor
            if self.checkColide(self.doorOpen, self.doorBar) and \
                    (self.checkColide(self.bar, self.lSwitch1) or \
                     self.checkColide(self.bar, self.lSwitch2)):
                # turn off indicator lights
                self.ipusNoorot()
                # initials "loop" of close door.
                Clock.schedule_interval(self.closeDoor, 1.0 / 40.0)
                self.state = 'doorClosing3'
                print 'koma3'
        elif self.state == 'doorClosing3':
            ###############
            # in linux:
            #if self.checkColide(*self.colides['dClose']):
            ####################
            # if door is closed
            if self.checkColide(self.doorBar, self.doorClose):
                # finish "loop" of close door.
                Clock.unschedule(self.closeDoor)
                self.state = 'up3'
                # initials "loop" of door stop made for phisi class
                Clock.schedule_interval(self.doorStop, 1.0 / 40.0)
        elif self.state == 'up3':
            # light up indicator, and move car up.
            self.moveUp()
            ################
            # in linux:
            #if self.checkColide(*self.colides['ls3']):
            ########################
            # if the car reaches third floor
            if self.checkColide(self.bar, self.lSwitch3):
                # made for phisi class.
                self.moveEnd()
                self.state = 'inplace3'
        elif self.state == 'inplace3':
            # stops "loop" of door stop made for phisi class
            Clock.unschedule(self.doorStop)
            # initials "loop" of door open
            Clock.schedule_interval(self.openDoor, 1.0 / 40.0)
            #########################
            # linux:
            #if self.checkColide(*self.colides['dOpen']):
            ######################
            # if door is opened
            if self.checkColide(self.doorOpen, self.doorBar):
                # stops "loop" of door open
                Clock.unschedule(self.openDoor)
                self.state = 'end3'
                Clock.schedule_interval(self.doorStop, 1.0 / 55.0)
        elif self.state == 'end3':
            # stops this "loop"
            Clock.unschedule(self.koma3)
            # turn on third floor indicator light
            self.lightOn(self.noora3, 'thirdLight.png')
            # close direction arrow.
            self.ipusDirection()
            # init state machine
            self.state = 'begin'
            # init selector "loop" in phisi class.
            Clock.schedule_interval(self.selector, 1.0 / 40)

    def koma2(self, dt):
        '''
        Controls what happens after second floor button was pressed.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        # todo complete code for second floor

    def koma1(self, dt):
        '''
        Controls what happens after first floor button was pressed.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        # todo complete code for first floor


class Phisi(Logi):
    status = ObjectProperty

    def __init__(self):
        super(Phisi, self).__init__()
        ##        leds
        self.ledUp = LED(14)
        self.ledDown = LED(15)
        self.noora1 = LED(2)
        self.noora2 = LED(3)
        self.noora3 = LED(4)
        ##        elevator motor
        self.elDir = OutputDevice(21)
        self.elPwm = OutputDevice(20)
        ##        door motor
        self.doDir = OutputDevice(26)
        self.doPwm = OutputDevice(19)
        ##        door limit switches
        self.doorOpen = Button(16)
        self.doorClose = Button(12)
        ##        floor push buttoms
        self.first = Button(27)
        self.second = Button(18)
        self.third = Button(17)
        ##        in cage push buttoms
        self.elFirst = Button(24)
        self.elSecond = Button(23)
        self.elThird = Button(22)
        ##        floor push buttoms
        self.lSwitch1 = Button(7)
        self.lSwitch2 = Button(8)
        self.lSwitch3 = Button(25)
        self.colides = {'dOpen': (self.doorOpen,),
                        'dClose': (self.doorClose,),
                        'ls2': (self.lSwitch2,),
                        'ls3': (self.lSwitch3,),
                        'ls1': (self.lSwitch1,),
                        }
        Clock.schedule_interval(self.selector, 1.0 / 40.0)

    def selector(self, dt):
        if self.checkButtns(self.first, self.elFirst):
            Clock.schedule_interval(self.koma1, 1.0 / 40.0)
            Clock.unschedule(self.selector)
        elif self.checkButtns(self.second, self.elSecond):
            Clock.schedule_interval(self.koma2, 1.0 / 40.0)
            Clock.unschedule(self.selector)
        elif self.checkButtns(self.third, self.elThird):
            Clock.schedule_interval(self.koma3, 1.0 / 40.0)
            Clock.unschedule(self.selector)

    def changeOptions(self):
        if self.status.text == 'Logi':
            self.clear_widgets()
            self.add_widget(Logi())
        if self.status.text == 'Service':
            self.clear_widgets()
            self.add_widget(Service())

    def lightOn(self, obj, src=None):
        return obj.on()

    def ipusNoorot(self):
        self.noora1.off()
        self.noora2.off()
        self.noora3.off()

    def closeDoor(self, dt):
        self.doPwm.on()
        self.doDir.on()

    def doorStop(self, dt):
        self.doPwm.off()
        self.doDir.off()

    def openDoor(self, dt):
        self.doPwm.on()
        self.doDir.off()

    def checkButtns(self, but1, but2):
        return but1.is_pressed or but2.is_pressed

    def checkColide(self, obj):
        return obj.is_pressed

    def moveUp(self):
        self.ledUp.on()
        self.elPwm.on()
        self.elDir.on()

    def moveEnd(self):
        self.ledUp.off()
        self.ledDown.off()
        self.elPwm.off()
        self.elDir.off()

    def moveDown(self):
        self.ledDown.on()
        self.elPwm.on()
        self.elDir.off()


class Service(Phisi):
    status = ObjectProperty

    def __init__(self):
        super(Service, self).__init__()
        self.status.text = 'Service'
        Clock.schedule_interval(self.start, 1.0 / 40.0)

    def changeOptions(self):
        if self.status.text == 'Logi':
            self.clear_widgets()
            self.add_widget(Logi())
        elif self.status.text == 'Phisi':
            self.clear_widgets()
            self.add_widget(Service())

    def start(self, dt):
        if self.second.is_pressed:
            self.openDoor()
        if self.checkColide(self.doorOpen, ):
            self.doorStop()
        elif self.first.is_pressed:
            self.moveDown()
        elif self.checkColide(self.lSwitch1, ):
            self.moveEnd()
        elif self.third.is_pressed:
            self.moveUp()
        elif not self.third.is_pressed:
            self.moveEnd()


class PiApp(App):
    pass


if __name__ == '__main__':
    PiApp().run()
