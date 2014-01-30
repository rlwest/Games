#################### ham cheese forgetting DM model ###################

# this model turns on the subsymbolic processing for DM, which causes forgetting


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  



# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    
    player_A=ccm.Model(signal='OK')
    
    hand_A=ccm.Model(move='scissors')
    
    player_B=ccm.Model(signal='OK')
    
    hand_B=ccm.Model(move='scissors')
    
    referee=ccm.Model(signal='go')


# --------------- Motor Module ------------------

class MotorModule(ccm.Model):     ### defines actions on the environment
    def paper_A(self):           
        print "A  hand = paper"
        self.parent.parent.hand_A.move='paper'
    def rock_A(self):           
        print "A  hand = rock"
        self.parent.parent.hand_A.move='rock'
    def scissors_A(self):           
        print "A  hand = scissors"
        self.parent.parent.hand_A.move='scissors'
    def OK_A(self):           
        print "A is OK"
        self.parent.parent.player_A.signal='OK'
    def busy_A(self):           
        print "A is busy"
        self.parent.parent.player_A.signal='busy'

        

    def paper_B(self):           
        print "B  hand = paper"
        self.parent.parent.hand_B.move='paper'
    def rock_B(self):           
        print "B  hand = rock"
        self.parent.parent.hand_B.move='rock'
    def scissors_B(self):           
        print "B  hand = scissors"
        self.parent.parent.hand_B.move='scissors'
    def OK_B(self):           
        print "B is OK"
        self.parent.parent.player_B.signal='OK'
    def busy_B(self):           
        print "B is busy"
        self.parent.parent.player_B.signal='busy'

    def ref_go(self):           
        print "ref says go"
        self.parent.parent.referee.signal='go'
    def ref_wait(self):           
        print "ref says wait"
        self.parent.parent.referee.signal='wait'

#####
# create an act-r agent   ######## Referee

class Ref(ACTR):
    production_time=0.05
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('state:start')

    def OK(focus='state:start',
           player_B='signal:OK',
           player_A='signal:OK'):
        print "ref - both players are OK"
        focus.set('state:check')
        motor.ref_go()

    def B_busy(focus='state:check',
               player_B='signal:busy'):
        print "ref - B busy"
        motor.ref_wait()
        focus.set('state:evaluate')

    def A_busy(focus='state:check',
               player_A='signal:busy'):
        print "ref - A busy"
        motor.ref_wait()
        focus.set('state:evaluate')




     
    def evalp1(focus='state:evaluate',
               hand_B='move:paper',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "tie b paper  a paper"
        focus.set('state:start')
        
    def evalp2(focus='state:evaluate',
               hand_B='move:paper',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B win b paper  a rock"
        focus.set('state:start')
        
    def evalp3(focus='state:evaluate',
               hand_B='move:paper',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B loss b paper  a scissors"
        focus.set('state:start')
 
    def evalr1(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B loss b rock  a paper"
        focus.set('state:start')
        
    def evalr2(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "tie b rock  a rock"
        focus.set('state:start')
        
    def evalr3(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B win b rock  a scissors"
        focus.set('state:start')

    def evals1(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B win b scissors  a paper"
        focus.set('state:start')
        
    def evals2(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "B loss b scissors  a rock"
        focus.set('state:start')
        
    def evals3(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        print "tie b scissors  a scissors"
        focus.set('state:start')



#####
# create an act-r agent

class Lag2player(ACTR):  ######## Player B
    focus=Buffer()
    motor=MotorModule()

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=1,threshold=0)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=.5,limit=None)       # turn on for DM subsymbolic processing




    def init():
        focus.set('state:request lag1:unknown lag2:unknown')

## predict ####################

    def guess_request(focus='state:request lag1:?lag1 lag2:?lag2',
                      referee='signal:go'):
        DM.request('lag1:?lag1 lag2:?lag2')
        focus.set('state:retrieve lag1:?lag1 lag2:?lag2')
        motor.busy_B()
        print "B guess requested"

    def guesss_retrieved(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                         DMbuffer='lag0:?lag0'):
        print "guess retrieved"
        focus.set('state:play lag0:?lag0 lag1:?lag1 lag2:?lag2')
        DMbuffer.clear

## random guessing ###########
        
    def guess_paper(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:paper lag1:?lag1 lag2:?lag2')
        print "guess random"
        
    def guess_rock(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:rock lag1:?lag1 lag2:?lag2')
        print "guess random"
        
    def guess_scissors(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:scissors lag1:?lag1 lag2:?lag2')
        print "guess random"

## make the action #########        

    def paper(focus='state:play lag0:paper lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:paper lag1:?lag1 lag2:?lag2')
        motor.scissors_B()
        print "B plays scissors"
    def rock(focus='state:play lag0:rock lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:rock lag1:?lag1 lag2:?lag2')
        motor.paper_B()
        print "B plays paper"
    def scissors(focus='state:play lag0:scissors lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:scissors lag1:?lag1 lag2:?lag2')
        motor.rock_B()
        print "B plays rock"


## store result and start again ################

    def store_result(focus='state:evaluate lag1:?lag1 lag2:?lag2',
                     hand_A='move:?lag0'):
        print "store result"
        DM.add('lag0:?lag0 lag1:?lag1 lag2:?lag2')
        print "shift lags"
        focus.set('state:request lag1:?lag0 lag2:?lag1')
        motor.OK_B()

        

#####
# create an act-r agent

class Human(ACTR):   #### palyer A
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('state:request')

    def start(focus='state:request',
              referee='signal:go'):
        focus.set('state:get')
        motor.busy_A()
        print 'A guess requested'

    def get_move(focus='state:get'):
        x = raw_input("move? ")   # get input
        if x == 'p':
            print "p"
            motor.paper_A()
            motor.OK_A()
        elif x == 'r':
            print "r"
            motor.rock_A()
            motor.OK_A()
        elif x == 's':
            print "s"
            motor.scissors_A()
            motor.OK_A()
        else:
            print "wrong"
        focus.set('state:request')







john=Ref()
tim=Human()
tom=Lag2player()
subway=MyEnvironment()
subway.agent=john
subway.agent=tim
subway.agent=tom
ccm.log_everything(subway)                 # print out what happens in the environment
log=ccm.log(html=True)
subway.run()                               # run the environment
ccm.finished()                             # stop the environment
