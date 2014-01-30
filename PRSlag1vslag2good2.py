#################### ham cheese forgetting DM model ###################

# this model turns on the subsymbolic processing for DM, which causes forgetting


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  



# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    
    player_A=ccm.Model(signal='OK')
    hand_A=ccm.Model(move='scissors')
    score_A=ccm.Model(score=0)
    
    player_B=ccm.Model(signal='OK')
    hand_B=ccm.Model(move='scissors')
    score_B=ccm.Model(score=0)
    
    referee=ccm.Model(signal='go')
    trial_count=ccm.Model(trial=0)


# --------------- Motor Module ------------------

class MotorModule(ccm.Model):     ### defines actions on the environment
    def paper_A(self):           
        #print "A  hand = paper"
        self.parent.parent.hand_A.move='paper'
    def rock_A(self):           
        #print "A  hand = rock"
        self.parent.parent.hand_A.move='rock'
    def scissors_A(self):           
        #print "A  hand = scissors"
        self.parent.parent.hand_A.move='scissors'
    def closed_A(self):           
        #print "A  hand = scissors"
        self.parent.parent.hand_A.move='closed'
    def OK_A(self):           
        #print "A is OK"
        self.parent.parent.player_A.signal='OK'
    def busy_A(self):           
        #print "A is busy"
        self.parent.parent.player_A.signal='busy'

        

    def paper_B(self):           
        #print "B  hand = paper"
        self.parent.parent.hand_B.move='paper'
    def rock_B(self):           
        #print "B  hand = rock"
        self.parent.parent.hand_B.move='rock'
    def scissors_B(self):           
        #print "B  hand = scissors"
        self.parent.parent.hand_B.move='scissors'
    def closed_B(self):           
        #print "B  hand = scissors"
        self.parent.parent.hand_B.move='closed'
    def OK_B(self):           
        #print "B is OK"
        self.parent.parent.player_B.signal='OK'
    def busy_B(self):           
        #print "B is busy"
        self.parent.parent.player_B.signal='busy'

    def ref_go(self):           
        #print "ref says go"
        self.parent.parent.referee.signal='go'
    def ref_wait(self):           
        #print "ref says wait"
        self.parent.parent.referee.signal='wait'
        
    def A_win(self):           
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        A=A+1
        C=C+1
        print A,B,C
        self.parent.parent.score_A.score=A
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) # make string and store
        if C==150:
             f.write('%d,%d,%d\n'%(C,A,B)) # make string and store
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'
    def B_win(self):           
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        B=B+1
        C=C+1
        print A,B,C
        self.parent.parent.score_B.score=B
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) 
        if C==150:
             f.write('%d,%d,%d\n'%(C,A,B)) 
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'
    def tie(self):           
        A=self.parent.parent.score_A.score
        B=self.parent.parent.score_B.score
        C=self.parent.parent.trial_count.trial
        C=C+1
        print A,B,C
        self.parent.parent.trial_count.trial=C
        #f.write('%d,%d,%d\n'%(C,A,B)) 
        if C==150:
             f.write('%d,%d,%d\n'%(C,A,B)) 
             self.parent.parent.player_B.signal='stop'
             self.parent.parent.player_A.signal='stop'



#####
# create an act-r agent   ######## Referee

class Ref(ACTR):
    production_time=0.01   # referee is faster
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('state:start')

    def OK(focus='state:start',   # ref waits until A and B signal they are ready
           player_B='signal:OK',
           player_A='signal:OK'):
        focus.set('state:check')
        motor.ref_go()


    def B_busy(focus='state:check',
               player_B='signal:busy'):
        motor.ref_wait()                 # ref sets his signal to "wait" - players cannot start their process
        focus.set('state:evaluate')
                                         
    def A_busy(focus='state:check',
               player_A='signal:busy'):
        motor.ref_wait()                 # same as above, as soon as the first player is busy there is a signal to wait
        focus.set('state:evaluate')


     
    def evalp1(focus='state:evaluate',  # evaluation occurs when both players have signaled "OK"
               hand_B='move:paper',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')        # this loops back up to re start the cycle
        motor.tie()
        
    def evalp2(focus='state:evaluate',
               hand_B='move:paper',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.B_win()
        
    def evalp3(focus='state:evaluate',
               hand_B='move:paper',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.A_win()


 
    def evalr1(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.A_win()
        
    def evalr2(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.tie()
        
    def evalr3(focus='state:evaluate',
               hand_B='move:rock',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.B_win()


        

    def evals1(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:paper',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.B_win()
        
    def evals2(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:rock',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.A_win()
        
    def evals3(focus='state:evaluate',
               hand_B='move:scissors',
               hand_A='move:scissors',
               player_B='signal:OK',
               player_A='signal:OK'):
        focus.set('state:start')
        motor.tie()



#####
# create an act-r agent

class Lag2player(ACTR):  ######## Player B lag2
    focus=Buffer()
    motor=MotorModule()

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=1,threshold=1)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.28,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=.5,limit=None)       # turn on for DM subsymbolic processing




    def init():
        focus.set('state:request lag1:unknown lag2:unknown')

## predict ####################

    def guess_request(focus='state:request lag1:?lag1 lag2:?lag2',
                      referee='signal:go'):
        DM.request('lag1:?lag1 lag2:?lag2')
        focus.set('state:retrieve lag1:?lag1 lag2:?lag2')
        motor.busy_B()
        motor.closed_B()
        #print "B guess requested"

    def guesss_retrieved(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                         DMbuffer='lag0:?lag0'):
        #print "guess retrieved"
        focus.set('state:play lag0:?lag0 lag1:?lag1 lag2:?lag2')
        DMbuffer.clear()

## random guessing ###########
        
    def guess_paper(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:paper lag1:?lag1 lag2:?lag2')
        #print "guess random"
        
    def guess_rock(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:rock lag1:?lag1 lag2:?lag2')
        #print "guess random"
        
    def guess_scissors(focus='state:retrieve lag1:?lag1 lag2:?lag2',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:scissors lag1:?lag1 lag2:?lag2')
        #print "guess random"

## make the action #########        

    def paper(focus='state:play lag0:paper lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:paper lag1:?lag1 lag2:?lag2')
        motor.scissors_B()
        #print "B plays scissors"
        #DM.add('lag0:paper lag1:?lag1 lag2:?lag2')# harvest activation increase
    def rock(focus='state:play lag0:rock lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:rock lag1:?lag1 lag2:?lag2')
        motor.paper_B()
        #print "B plays paper"
        #DM.add('lag0:rock lag1:?lag1 lag2:?lag2')# harvest activation increase
    def scissors(focus='state:play lag0:scissors lag1:?lag1 lag2:?lag2'):
        focus.set('state:evaluate lag0:scissors lag1:?lag1 lag2:?lag2')
        motor.rock_B()
        #print "B plays rock"
        #DM.add('lag0:scissors lag1:?lag1 lag2:?lag2')# harvest activation increase


## store result and start again ################

    def store_result(focus='state:evaluate lag1:?lag1 lag2:?lag2',
                     hand_A='move:!closed?lag0'):
        #print "store result"
        DM.add('lag0:?lag0 lag1:?lag1 lag2:?lag2')
        #print "shift lags"
        focus.set('state:request lag1:?lag0 lag2:?lag1')
        motor.OK_B()

        

#####
# create an act-r agent


class Lag1player(ACTR):  ######## Player A lag1
    focus=Buffer()
    motor=MotorModule()

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=1,threshold=-14)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=1.25,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=.5,limit=None)       # turn on for DM subsymbolic processing




    def init():
        focus.set('state:request lag1:unknown')

## predict ####################

    def guess_request(focus='state:request lag1:?lag1',
                      referee='signal:go'):
        DM.request('lag1:?lag1')
        focus.set('state:retrieve lag1:?lag1')
        motor.busy_A()
        motor.closed_A()
        #print "A guess requested"

    def guesss_retrieved(focus='state:retrieve lag1:?lag1',
                         DMbuffer='lag0:?lag0'):
        #print "guess retrieved"
        focus.set('state:play lag0:?lag0 lag1:?lag1')
        DMbuffer.clear()

## random guessing ###########
        
    def guess_paper(focus='state:retrieve lag1:?lag1',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:paper lag1:?lag1')
        #print "guess random"
        
    def guess_rock(focus='state:retrieve lag1:?lag1',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:rock lag1:?lag1')
        #print "guess random"
        
    def guess_scissors(focus='state:retrieve lag1:?lag1',
                       DMbuffer=None,
                       DM='error:True'):
        focus.set('state:play lag0:scissors lag1:?lag1')
        #print "guess random"

## make the action #########        

    def paper(focus='state:play lag0:paper lag1:?lag1'):
        focus.set('state:evaluate lag0:paper lag1:?lag1')
        motor.scissors_A()
        #print "A plays scissors"
    def rock(focus='state:play lag0:rock lag1:?lag1'):
        focus.set('state:evaluate lag0:rock lag1:?lag1')
        motor.paper_A()
        #print "A plays paper"
    def scissors(focus='state:play lag0:scissors lag1:?lag1'):
        focus.set('state:evaluate lag0:scissors lag1:?lag1')
        motor.rock_A()
        #print "A plays rock"


## store result and start again ################

    def store_result(focus='state:evaluate lag1:?lag1',
                     hand_B='move:!closed?lag0'):
        #print "store result"
        DM.add('lag0:?lag0 lag1:?lag1')
        #print "shift lags"
        focus.set('state:request lag1:?lag0')
        motor.OK_A()







for i in range(100):
        f = open('newLg1t-14n125_Lg2t1n28.txt', 'a')
        john=Ref()
        tim=Lag1player()
        tom=Lag2player()
        octagon=MyEnvironment()
        octagon.agent=john
        octagon.agent=tim
        octagon.agent=tom
        #ccm.log_everything(octagon) 
        log=ccm.log(html=True)
        octagon.run() 
        ccm.finished()
        f.close()
        
