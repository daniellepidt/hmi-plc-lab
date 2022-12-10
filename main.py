'''
These files can be used only with permission from the author Gad Halevy.
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from gpiozero import LED,OutputDevice,Button

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
        # Dictionary that works only on linux raspberry pi is
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
        self.delet.size[0] -= 1
        self.doorBar.pos[0] = self.delet.size[0] - self.doorBar.size[0] / 2 + self.delet.pos[0] + 10

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
        if self.checkColide(self.doorOpen, self.doorBar):
            Clock.schedule_interval(self.koma2, 1.0 / 45.0)

    def moveThird(self):
        '''
        Called by third floor button
        :return:
        '''
        if self.checkColide(self.doorOpen, self.doorBar):
            Clock.schedule_interval(self.koma3, 1.0 / 45.0)

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
        self.direction.color = 1, 1, 1, 1
        self.direction.source = 'down.png'
        self.body.pos[1] -= 1

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
        self.noora1.source = 'first.png'
        self.noora2.source = 'second.png'
        self.noora3.source = 'third.png'

    def ipusDirection(self):
        '''
        Turns direction arrow off.
        set source to '', and mask thecolor (0, 0, 0, 1)
        :return:
        '''
        self.direction.source = ''
        self.direction.color = 0, 0, 0, 1

    def checkColide(self, obj1, obj2):
        '''
        Check if bars (door and elevator) collides with
        some limit switch.
        use obj1.collide_widget(obj2)
        :param obj1: bar.
        :param obj2: limit switch.
        :return: true if colides, false if not.
        '''
        return obj1.collide_widget(obj2)

    def lightOn(self, obj, src):
        '''
        Turn on indictor lights.
        :param obj: some indicator light.
        :param src: image path of lighted number.
        :return:
        '''
        obj.source = src

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
                print('koma3')
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
        if self.state == 'begin':
            # if door open and the car in first floor or in third floor
            if self.checkColide(self.doorOpen, self.doorBar) and (
                    self.checkColide(self.bar, self.lSwitch1) or self.checkColide(self.bar, self.lSwitch3)):
                # turn off indicator lights
                self.ipusNoorot()
                # initials "loop" of close door.
                Clock.schedule_interval(self.closeDoor, 1.0 / 40.0)
                self.state = 'doorClosing2'
                print('koma2')
        elif self.state == 'doorClosing2':
            # if door is closed
            if self.checkColide(self.doorBar, self.doorClose):
                # finish "loop" of close door.
                Clock.unschedule(self.closeDoor)
                if self.checkColide(self.bar, self.lSwitch1):
                    self.state = 'up2'
                elif self.checkColide(self.bar, self.lSwitch3):
                    self.state = 'down2'
                # initials "loop" of door stop made for phisi class
                Clock.schedule_interval(self.doorStop, 1.0 / 40.0)
        elif self.state == 'up2':
            # light up indicator, and move car up.
            self.moveUp()
            # if the car reaches second floor
            if self.checkColide(self.bar, self.lSwitch2):
                # made for phisi class.
                self.moveEnd()
                self.state = 'inplace2'
        elif self.state == 'down2':
            # light up indicator, and move car down.
            self.moveDown()
            # if the car reached second floor
            if self.checkColide(self.bar, self.lSwitch2):
                # made for phisi class.
                self.moveEnd()
                self.state = 'inplace2'
        elif self.state == 'inplace2':
            # stops "loop" of door stop made for phisi class
            Clock.unschedule(self.doorStop)
            # initials "loop" of door open
            Clock.schedule_interval(self.openDoor, 1.0 / 40.0)
            # if door is opened
            if self.checkColide(self.doorOpen, self.doorBar):
                # stops "loop" of door open
                Clock.unschedule(self.openDoor)
                self.state = 'end2'
                Clock.schedule_interval(self.doorStop, 1.0 / 55.0)
        elif self.state == 'end2':
            # stops this "loop"
            Clock.unschedule(self.koma2)
            # turn on second floor indicator light
            self.lightOn(self.noora2, 'secondLighted.png')
            # close direction arrow.
            self.ipusDirection()
            # init state machine
            self.state = 'begin'
            # init selector "loop" in phisi class.
            Clock.schedule_interval(self.selector, 1.0 / 40)

    def koma1(self, dt):
        '''
        Controls what happens after first floor button was pressed.
        :param dt: refresh rate of schedule interval
        :return:
        '''
        # initialize state machine
        if self.state == 'begin':
            # if door open and the car in second floor or car in third floor
            if self.checkColide(self.doorOpen, self.doorBar) and (
                    self.checkColide(self.bar, self.lSwitch2) or self.checkColide(self.bar, self.lSwitch3)):
                # turn off indicator lights
                self.ipusNoorot()
                # initials "loop" of close door.
                Clock.schedule_interval(self.closeDoor, 1.0 / 40.0)
                self.state = 'doorClosing1'
                print('koma1')
        elif self.state == 'doorClosing1':
            # if door is closed
            if self.checkColide(self.doorBar, self.doorClose):
                # finish "loop" of close door.
                Clock.unschedule(self.closeDoor)
                self.state = 'down1'
                # initials "loop" of door stop made for phisi class
                Clock.schedule_interval(self.doorStop, 1.0 / 40.0)
        elif self.state == 'down1':
            # light up indicator, and move car up.
            self.moveDown()
            # if the car reaches first floor
            if self.checkColide(self.bar, self.lSwitch1):
                # made for phisi class.
                self.moveEnd()
                self.state = 'inplace1'
        elif self.state == 'inplace1':
            # stops "loop" of door stop made for phisi class
            Clock.unschedule(self.doorStop)
            # initials "loop" of door open
            Clock.schedule_interval(self.openDoor, 1.0 / 40.0)
            # if door is opened
            if self.checkColide(self.doorOpen, self.doorBar):
                # stops "loop" of door open
                Clock.unschedule(self.openDoor)
                self.state = 'end1'
                Clock.schedule_interval(self.doorStop, 1.0 / 55.0)
        elif self.state == 'end1':
            # stops this "loop"
            Clock.unschedule(self.koma1)
            # turn on first floor indicator light
            self.lightOn(self.noora1, 'firstLighted.png')
            # close direction arrow.
            self.ipusDirection()
            # init state machine
            self.state = 'begin'
            # init selector "loop" in phisi class.
            Clock.schedule_interval(self.selector, 1.0 / 40)


class Phisi(Logi):
    '''
    The purpose of this class is to inharit from class Logi and adjust it to the raspberry pi,
    so that to program will work by pressing the raspberry pi and not the simulations's buttons
    '''

    status = ObjectProperty

    def __init__(self):
        super(Phisi, self).__init__()
        ##        leds
        self.ledUp = LED(14) # The number '14' is the number of physical leg in the raspberry pi  
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
        # holds the elevator status (open/close and which floor it's located)
        self.colides = {'dOpen': (self.doorOpen,),
                        'dClose': (self.doorClose,),
                        'ls2': (self.lSwitch2,),
                        'ls3': (self.lSwitch3,),
                        'ls1': (self.lSwitch1,),
                        }
        # loop to initiate the selector method to be shown every 1/40 seconds, which appears like the entire time
        Clock.schedule_interval(self.selector, 1.0 / 40.0)

    def selector(self, dt):
        '''
        This method checks the desired destination floor and the current location of the elevator.
        If that doesn't fit, there is a loop that we'll be running till the elevator reach the destination floor.
        :param dt: refresh rate of schedule interval
        :return: none
        '''
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
        '''
        Adjust the spinner view to Logi/Service as the operator choose.
        :return:none
        '''
        if self.status.text == 'Logi':
            self.clear_widgets()
            self.add_widget(Logi())
        if self.status.text == 'Service':
            self.clear_widgets()
            self.add_widget(Service())

    def lightOn(self, obj, src=None):
        '''
        Turn on the light of some pin on the raspberry pi.
        :param obj: the pin
        :param src: was been inherited from the predeccesor "Logi" class, and is not in use. this why we entered default value "None"
        :return: turning on the desired pin
        '''
        return obj.on()

    def ipusNoorot(self):
        '''
        Turns off all of the three noorot
        :return: none
        '''
        self.noora1.off()
        self.noora2.off()
        self.noora3.off()

    def closeDoor(self, dt):
        '''
        Defines the statues of both the Pwn and Dir to close elevator's door,
        as shown on the video, both Pwn and Dir should be turned on for this operation.
        :param dt: refresh rate schedule interval
        :return: none
        '''
        self.doPwm.on()
        self.doDir.on()

    def doorStop(self, dt):
        '''
        Defines the statues of both the Pwn and Dir to stop elevator's door, 
        both Pwn and Dir should be turned off for this operation.
        :param dt: refresh rate schedule interval
        :return: none
        '''
        self.doPwm.off()
        self.doDir.off() # Not necessary, but can help controlling the engine server later

    def openDoor(self, dt):
        '''
        Defines the statues of both the Pwn and Dir to open elevator's door, 
        Pwn should be turned on while Dir should be turned off for this operation.
        :param dt: refresh rate schedule interval
        :return: none
        '''
        self.doPwm.on()
        self.doDir.off()

    def checkButtns(self, but1, but2):
        '''
        Check if an elevator activation is needed.
        :param but1 + param 2 : The floor button and the limit switch
        :return: returns True if at least one of the but1/but2 are pressed or the elevator is already in that floor. Either return False.
        '''
        return but1.is_pressed or but2.is_pressed

    def checkColide(self, obj):
        '''
        Check the  statuד of a button/limit switch
        :param obj: a button object
        :return: returns True while it's already pressed, otherwise False.
        '''
        return obj.is_pressed

    def moveUp(self):
        '''
        As explaind, to make the elevator move forawrd both Pwn and Dir should be on.
        The light of moving up is also switched on
        '''
        self.ledUp.on()
        self.elPwm.on()
        self.elDir.on()

    def moveEnd(self):
        '''
        As explaind, to make the elevator stop forawrd both Pwn and Dir should be turned off.
        The lights which indicates moving up/down also will be turned off.
        '''
        self.ledUp.off()
        self.ledDown.off()
        self.elPwm.off()
        self.elDir.off()

    def moveDown(self):
        '''
        As explaind, to make the elevator move backwards both Pwn should be on while Dir should be turned off.
        The lights which indicates moving down will be turned on.
        '''
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
